#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os
import pandas as pd
import datetime
from xml.etree.ElementTree import parse

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_dailysummary_insert(file_path,athlete,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        """ Connect to the PostgreSQL database server """
        file2import = (file_path, )
        athlete_id = (athlete, )
        db_name = (db_name)
        conn = None
        #Lists to store the data from xml
        startGMT = []
        endGMT = []
        activityLevelConstant = []
        steps = []
        primaryActivityLevel = []
        
        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + athlete + '_PID.txt'
        open(pidfile, 'w').write(pid)

        # PG Amend path for postgres "pg_read_file()" function.
        text = file_path
        head, sep, tail = text.partition('temp/')
        pg_read_file = (tail, )

        xpath_sql = """
        INSERT INTO garmin_connect_daily_summary (athlete_id,start_gmt,end_gmt,activity_level_constant,steps,primary_activity_level)
        
        SELECT
        
        (select id from athlete where gc_email=%s),
        to_char(to_timestamp(unnest (xpath('//*[local-name()="item"]/*[local-name()="startGMT"]/text()', x))::text::text,'YYYY-MM-DD HH24:MI:SS'),'YYYY-MM-DD HH24:MI:SS') AS start_gmt,
        to_char(to_timestamp(unnest (xpath('//*[local-name()="item"]/*[local-name()="endGMT"]/text()', x))::text::text,'YYYY-MM-DD HH24:MI:SS'),'YYYY-MM-DD HH24:MI:SS') AS end_gmt,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="activityLevelConstant"]/text()', x))::text::bool AS activity_level_constant,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="steps"]/text()', x))::text::int AS steps,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="primaryActivityLevel"]/text()', x))::text::text AS primary_activity_level
        
        
        FROM UNNEST (xpath('//*[local-name()="root"]', pg_read_file(%s)::xml)) x

        ON CONFLICT (athlete_id,start_gmt) DO NOTHING;
                    
        """
        
        pd_df_sql = """
        INSERT INTO garmin_connect_daily_summary (athlete_id,start_gmt,end_gmt,activity_level_constant,steps,primary_activity_level)

        VALUES
            ((select id from athlete where gc_email=%s),%s,%s,%s,%s,%s)
        
        ON CONFLICT (athlete_id,start_gmt) DO NOTHING;

        """

        sql_time_diff = """
        INSERT INTO gmt_local_time_difference (athlete_id,local_date,local_midnight_timestamp,gmt_midnight_timestamp,gmt_local_difference)

        VALUES
            ((select id from athlete where gc_email=%s),%s,%s,%s,%s)

        ON CONFLICT (local_date) DO NOTHING;
        """
        
        sql_sleep_tracking = """
        INSERT INTO gc_original_wellness_sleep_tracking (timestamp_gmt,timestamp_local,activity_tracking_id,hr_tracking_id,stress_tracking_id)

        VALUES
            (%s,%s,(select id from gc_original_wellness_activity_tracking where timestamp=%s),(select id from gc_original_wellness_hr_tracking where timestamp=%s),(select id from gc_original_wellness_stress_tracking where timestamp=%s))

        ON CONFLICT (timestamp_gmt) DO NOTHING;
        """
        
        #Parse the XML document, and append the data to lists
        xml_document = parse(file_path)
        for item in xml_document.iterfind('item'):
            startGMT.append(item.findtext('startGMT'))
            endGMT.append(item.findtext('endGMT'))
            activityLevelConstant.append(item.findtext('activityLevelConstant'))
            steps.append(item.findtext('steps'))
            primaryActivityLevel.append(item.findtext('primaryActivityLevel'))
            
        #Create pandas dataframe and populate with data from lists
        df = pd.DataFrame({'startGMT': startGMT, 'endGMT':endGMT, 'activityLevelConstant':activityLevelConstant, 'steps':steps, 'primaryActivityLevel':primaryActivityLevel})
        #Convert startGMT and endGMT to datetime
        df['startGMT'] = pd.to_datetime(df['startGMT'])
        df['endGMT'] = pd.to_datetime(df['endGMT'])
        #Locate gmt midnight
        midnight_gmt_dt = df['startGMT'].iloc[0]
        #Retrieve date form the xml file name
        date_str = file_path[-22:-12]
        #Convert local date midnight to datetime
        midnight_local_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        #Get time difference (timedelta) by subtracting gmt from local
        local_gmt_time_diff = midnight_local_dt-midnight_gmt_dt

        try:
            
            # connect to the PostgreSQL server
            conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)
            conn.tpc_begin(conn.xid(42, 'transaction ID', 'connection 1'))

            ### Insert sleep tracking data to gc_original_wellness_sleep_tracking ###
            #Iterate through rows in pandas df
            for row in df.itertuples():
                row_startGMT = row.startGMT
                row_endGMT = row.endGMT
                row_activityLevelConstant = row.activityLevelConstant
                row_steps = row.steps
                row_primaryActivityLevel = row.primaryActivityLevel

                ### Insert daily summary data to garmin_connect_daily_summary ###
                # create a cursor
                cur = conn.cursor()
                # execute a statement
                with StdoutRedirection(athlete):
                    print('Inserting Daily Summary Data into postgreSQL:')
                cur.execute(pd_df_sql,(athlete,row_startGMT,row_endGMT,row_activityLevelConstant,row_steps,row_primaryActivityLevel))
                #conn.commit() 
                # close the communication with the PostgreSQL
                cur.close()

                #If activity level eq sleeping, extract start and end times (15min intervals)
                if row_primaryActivityLevel == 'sleeping':
                    #Break down 15min intervals in to 1min and convert each to local time 
                    while (row_startGMT<row_endGMT):
                        row_startGMT = row_startGMT + datetime.timedelta(minutes = 1)
                        row_startLocal = row_startGMT+local_gmt_time_diff
                        #Convert datetimes to strings
                        row_startGMT_str = datetime.datetime.strftime((row_startGMT), "%Y-%m-%d %H:%M:%S")
                        row_startLocal_str = datetime.datetime.strftime((row_startLocal), "%Y-%m-%d %H:%M:%S")
                        # create a cursor
                        cur = conn.cursor()
                        # execute a statement
                        with StdoutRedirection(athlete):
                            print('Inserting Sleep Tracking Data into postgreSQL:')
                        cur.execute(sql_sleep_tracking,(row_startGMT_str,row_startLocal_str,row_startGMT_str,row_startGMT_str,row_startGMT_str))
                        # close the communication with the PostgreSQL
                        cur.close()

            ### Insert Local to GMT time differnce to gmt_local_time_difference table ###
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            with StdoutRedirection(athlete):
                print('Inserting Local to GMT time difference into postgreSQL:')
            cur.execute(sql_time_diff,(athlete,date_str,midnight_local_dt,midnight_gmt_dt,local_gmt_time_diff))
            # close the communication with the PostgreSQL
            cur.close()
            with StdoutRedirection(athlete):
                print('Local to GMT time difference Data Inserted Successfully')
            with ProgressStdoutRedirection(athlete):
                print('Local to GMT time difference Data Inserted Successfully')
            try:
                conn.tpc_prepare()
            except  (Exception, psycopg2.DatabaseError) as error:
                conn.tpc_rollback()
                with ErrorStdoutRedirection(athlete):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
            else:
                conn.tpc_commit()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
        finally:
                if conn is not None:
                    conn.close()
                        


