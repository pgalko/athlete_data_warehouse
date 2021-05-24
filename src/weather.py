
from meteostat import Stations,Hourly,Point
from datetime import datetime,timedelta
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import inspect
from processify import processify
import os
from db_encrypt import str2md5
import math
import pandas as pd

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def get_weather(gc_username,db_host, db_name, superuser_un,superuser_pw,start_date,end_date,encr_pass):

    sql_timezones_select = '''
    SELECT timestamp_gmt,end_time_gmt,long_degr,lat_degr,alt_avrg from timezones 
    WHERE timestamp_gmt::date >= %s and timestamp_gmt::date <= %s 
    ORDER BY timestamp_gmt asc;
    '''

    pd_df_sql = """
    INSERT INTO weather(athlete_id,timestamp_gmt,temperature,dew_point,relative_humidity,precipitation,snow,wind_direction,wind_speed,wind_gust,sea_air_pressure,total_sunshine,condition_code)
    VALUES ((select id from athlete where gc_email=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (athlete_id,timestamp_gmt) DO NOTHING;
    """

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
    open(pidfile, 'w').write(pid)

    try:
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(sql_timezones_select,(start_date,end_date))

        long_degr = None
        lat_degr = None
        alt_avrg = None
        row_start_time = None
        row_end_time = None
        row_start_time_dt = None
        row_end_time_dt = None
        start_time = None
        end_time = None
        #Earth radius
        R = 6373.0
        row_nr = 1
        combined_df = pd.DataFrame()

        def meteostat(lat_degr,long_degr,alt_avrg,start_time,end_time):
            #Retrieve nearest weather station
            stations = Stations()
            stations = stations.nearby(lat_degr, long_degr)
            station = stations.fetch(1)

            #Use Point to agregate nearby weather stations data for better accuracy
            weather_point = Point(lat_degr, long_degr,alt_avrg)
            weather_data = Hourly(weather_point, start_time - timedelta(0,7200), end_time + timedelta(0,7200))
            weather_data = weather_data.fetch()
            #Use weather data from nearest station if Point returns an empty dataset
            if weather_data.empty:
                weather_data = Hourly(station, start_time - timedelta(0,7200), end_time + timedelta(0,7200))
                weather_data = weather_data.fetch()
            return weather_data
        
        for row in cur:
            #Retrieve activity start and end times and convert to datetime
            row_start_time = row[0]
            row_start_time_dt = datetime.strptime((str(row_start_time)), "%Y-%m-%d %H:%M:%S")
            row_end_time = row[1]
            row_end_time_dt = datetime.strptime((str(row_end_time)), "%Y-%m-%d %H:%M:%S")
            #Retrieve activity average altitude
            row_alt_avrg = row[4]

            #This is the first row,set initial values.
            if row_nr == 1:
                long_degr = row[2]
                lat_degr = row[3]
                start_time = row_start_time_dt
                end_time = row_end_time_dt

            #Calculate distance between subsequent activity locations
            lon1 = math.radians(long_degr)
            lat1 = math.radians(lat_degr)
            lon2 = math.radians(row[2])
            lat2 = math.radians(row[3])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c

            #If subsequent activities within 30km update endtime and move onto next row
            if distance < 30:
                end_time = row_end_time_dt
                #start_time stays the same
                #move onto next row
            #If subsequent activities not within 30km, download weather data and reset end and start times   
            else:
                combined_df = combined_df.append(meteostat(lat_degr,long_degr,alt_avrg,start_time,end_time))
                with StdoutRedirection(gc_username):
                    print(('Inserting weather data for period from: ' + str(start_time) + ' until: ' + str(end_time)))
                with ProgressStdoutRedirection(gc_username):
                    print(('Inserting weather data for period from: ' + str(start_time) + ' until: ' + str(end_time)))
                start_time = row_start_time_dt
                end_time = row_end_time_dt
                
            #Update variables with values from the current row and move onto the next one
            long_degr = row[2]
            lat_degr = row[3]
            alt_avrg = row[4]
            
            #Incrememt the row number variable
            row_nr = row_nr+1

        #There is one more block to be retrieved   
        combined_df = combined_df.append(meteostat(lat_degr,long_degr,alt_avrg,start_time,end_time))
        with StdoutRedirection(gc_username):
            print(('Inserting weather data for period from: ' + str(start_time) + ' until: ' + str(end_time)))
        with ProgressStdoutRedirection(gc_username):
            print(('Inserting weather data for period from: ' + str(start_time) + ' until: ' + str(end_time)))
        cur.close()

        #Iterate through rows in the consolidated pandas df
        combined_df = combined_df.reset_index()
        for row in combined_df.itertuples():
            row_timeGMT = row.time
            row_temp = row.temp
            row_dwpt = row.dwpt
            row_rhum = row.rhum
            row_prcp = row.prcp
            row_snow = row.snow
            row_wdir = row.wdir
            row_wspd = row.wspd
            row_wpgt = row.wpgt
            row_pres = row.pres
            row_tsun = row.tsun
            row_coco = row.coco

            ### Insert weather data to weather ###
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            cur.execute(pd_df_sql,(gc_username,row_timeGMT,row_temp,row_dwpt,row_rhum,row_prcp,row_snow,row_wdir,row_wspd,row_wpgt,row_pres,row_tsun,row_coco))
            conn.commit() 
            # close the communication with the PostgreSQL
            cur.close()
    except Exception as e:
        with ErrorStdoutRedirection(gc_username):
            print((str(datetime.now()) + '  ' + str(e)))
    finally:
        if conn is not None:
            conn.close
    
