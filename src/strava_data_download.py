import os
import sys
import requests
import psycopg2
import pandas as pd
from datetime import datetime,timezone,timedelta
import time
import json
import numpy as np
import base64
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
import Crypto.Random
from Crypto.Cipher import AES
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
from db_files import data_file_path_insert,check_data_file_exists
from processify import processify


#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt 

@processify
def api_rate_limits(response):
    #Retrieve API limits status from response headers
    response_headers = response.headers
    for key, value in response_headers.items():
        if key == "X-RateLimit-Limit":
            limit = value.split(",")
            min15_limit = limit[0]
            day_limit  = limit[1]
        elif key == "X-RateLimit-Usage":
            usage = value.split(",")
            min15_usage = usage[0]
            day_usage  = usage[1]

    #----Depending on API limits and current usage, check whether the download rate needs to be time limited----
    #Calculate "now" in UTC
    utc_now = datetime.now(timezone.utc)
    #Remove timezone info
    utc_now = utc_now.replace(tzinfo=None)

    #Set UTC midnight
    utc_midnight = utc_now.replace(hour=23, minute=59, second=59, microsecond=999999)
    #Calculate the difference in seconds between now and the UTC midnight
    midnight_difference = (utc_midnight-utc_now).total_seconds()

    #Calculate start of the next 15 min block
    utc_15min_block = utc_now + (datetime.min - utc_now) % timedelta(minutes=15)
    #Calculate the difference in seconds between now and start of the next 15 min block
    min15_difference = (utc_15min_block-utc_now).total_seconds()
    
    # Check if the limits have been reached, and if yes, calculate how long to pause the download for
    if int(day_usage) < int(day_limit):
        if int(min15_usage) < int(min15_limit):
            sleep_sec = 0
        else:
            with ConsolidatedProgressStdoutRedirection():
                print((str(datetime.now()) +' The Strava API 15 min download limit has been reached. Will pause for {} seconds.'.format(min15_difference)))
            sleep_sec = int(min15_difference)+2
    else:
        with ConsolidatedProgressStdoutRedirection():
            print((str(datetime.now()) + ' The Strava API daily download limit has been reached. Will pause for {} seconds.'.format(midnight_difference)))
        sleep_sec = int(midnight_difference)+2

    return  sleep_sec

@processify
def dwnld_insert_strava_data(ath_un,db_host,db_name,superuser_un,superuser_pw,strava_refresh_token,start_date_dt,end_date_dt,save_pwd,encr_pass):
 
    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    strava_params = config(filename="encrypted_settings.ini", section="strava",encr_pass=encr_pass)
    STRAVA_CLIENT_ID = str(strava_params.get("strava_client_id"))
    STRAVA_CLIENT_SECRET = str(strava_params.get("strava_client_secret"))
    STRAVA_TOKEN_URL = str(strava_params.get("strava_token_url"))

    sql_insert_strava_refresh_token = """

        DO
            $do$
                BEGIN
                    IF EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN
                        UPDATE athlete SET strava_refresh_token = %s where ath_un= %s;
                    END IF;
                END
            $do$

    """
    sql_insert_activity_summary = """

        INSERT INTO strava_activity_summary(athlete_id,strava_activity_id,strava_athlete_id,name,distance,moving_time,elapsed_time,total_elevation_gain,type,
        workout_type,external_id,upload_id,start_date,start_date_local,timezone,utc_offset,start_latitude,start_longitude,end_latitude,end_longitude,location_city,
        location_state,location_country,map,summary_polyline,trainer,commute,manual,gear_id,average_speed,max_speed,average_cadence,average_temp,average_watts,
        weighted_average_watts,kilojoules,device_watts,average_heartrate,max_heartrate,max_watts,elev_high,elev_low,suffer_score)

        VALUES
        ((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (start_date) DO NOTHING;
        
    """

    sql_insert_activity_streams = """

        INSERT INTO strava_activity_streams(activity_id,altitude,cadence,distance,grade_smooth,heartrate,latitude,longitude,moving,temp,time_gmt,velocity_smooth,watts)

        VALUES
        ((select id from strava_activity_summary where strava_activity_id=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (time_gmt) DO NOTHING;
    """
    
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

    def refresh_oauth_tokens():   
        #Refresh the access token
        payload = dict(grant_type='refresh_token', refresh_token=strava_refresh_token,client_id=STRAVA_CLIENT_ID,client_secret=STRAVA_CLIENT_SECRET)
        refresh = requests.post(STRAVA_TOKEN_URL, data=payload)
        response = refresh.json()
        oauth_token = response['access_token']
        refresh_token = response['refresh_token']
        expires_at = response['expires_at']

        if save_pwd == True:
            encrypted_refresh_token = base64.b64encode(encrypt(refresh_token, encr_pass))
            encrypted_refresh_token = encrypted_refresh_token.decode('utf-8')
        else:
            encrypted_refresh_token = None

        try:       
            cur = conn.cursor()
            cur.execute(sql_insert_strava_refresh_token,(ath_un,encrypted_refresh_token,ath_un))
            conn.commit()       
            cur.close()
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
        
        return oauth_token,expires_at
    
    oauth_token,expires_at = refresh_oauth_tokens()
    header = {'Authorization':'Bearer {}'.format(oauth_token)}
    epoch_start_date = start_date_dt.timestamp()
    epoch_end_date = end_date_dt.timestamp()

    #Loop through all activities
    page = 1
    activities_url = "https://www.strava.com/api/v3/activities"

    while True:   
        # Retry 3 times if request fails
        tries = 3
        for i in range(tries):
            try:
                #Check if the oauth token is stil valid, and refresh if not.
                if int(datetime.now().timestamp()) > expires_at:
                    oauth_token,expires_at = refresh_oauth_tokens()
                    header = {'Authorization':'Bearer {}'.format(oauth_token)}
                    with ProgressStdoutRedirection(ath_un):
                        print(str(datetime.now()) + 'The Strava oauth token expired and has been refreshed')
                # get page of 200 activities from Strava
                r = requests.get('{}?before={}&after={}&page={}&per_page=200'.format(activities_url,epoch_end_date,epoch_start_date,str(page)),headers=header)
                sleep_sec = api_rate_limits(r)
            except Exception as e:
                if i < tries - 1:
                    time.sleep(10)
                    continue
                else:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    raise
            break

        if sleep_sec == 0:
            pass
        else:
            time.sleep(sleep_sec)
            pass

        # if no results then exit loop
        if (not r.json()):
            if conn is not None:
                conn.close()
                with StdoutRedirection(ath_un):
                    print('Strava Activities Inserted Successfully')
                with ProgressStdoutRedirection(ath_un):
                    print('Strava Activities Inserted Successfully')
            break

        #Do something with the response/data
        activity_data = json.loads(r.text)
        
        #assign activity values to variables
        for activity in activity_data:
            if "id" in activity:
                strava_activity_id = activity['id']
                #PG: Check whether the data for this activity have been inserted into to DB during one of the previous runs
                data_exist_for_activity = 'Strava activity {} data'.format(strava_activity_id)
                data_exists = check_data_file_exists(data_exist_for_activity,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                if data_exists == True:
                    with StdoutRedirection(ath_un):
                        print(('Strava activity {} data already downloaded and inserted to DB. Skipping.'.format(strava_activity_id)))
                    with ProgressStdoutRedirection(ath_un):
                        print(('Strava activity {} data already downloaded and inserted to DB. Skipping'.format(strava_activity_id)))
                    continue 
            else:
                strava_activity_id = None
            if "id" in activity['athlete']:
                strava_athlete_id = activity['athlete']['id']
            else:
                strava_athlete_id = None
            if "name" in activity:
                name = activity['name']
            else:
                name = None
            if "distance" in activity:
                distance = activity['distance']
            else:
                distance = None
            if "moving_time" in activity:
                moving_time = activity['moving_time']
            else:
                moving_time = None
            if "elapsed_time" in activity:
                elapsed_time = activity['elapsed_time'] 
            else:
                elapsed_time = None
            if "total_elevation_gain" in activity:
                total_elevation_gain = activity['total_elevation_gain']
            else:
                total_elevation_gain = None
            if "type" in activity:
                type = activity['type']
            else:
                type = None
            if "workout_type" in activity:
                workout_type = activity['workout_type']
            else:
                workout_type = None
            if "external_id" in activity:
                external_id = activity['external_id']
            else:
                external_id = None
            if "upload_id" in activity:
                upload_id = activity['upload_id']
            else:
                upload_id = None
            if "start_date" in activity:
                start_date = activity['start_date']
                start_date_dt = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
                start_date = datetime.strftime(start_date_dt, '%Y-%m-%d %H:%M:%S')
            else:
                start_date = None
            if "start_date_local" in activity:
                start_date_local = activity['start_date_local']
                start_date_local_dt = datetime.strptime(start_date_local, '%Y-%m-%dT%H:%M:%SZ')
                start_date_local = datetime.strftime(start_date_local_dt, '%Y-%m-%d %H:%M:%S')
            else:
                start_date_local = None
            if "timezone" in activity:
               timezone = activity['timezone']
            else:
                timezone = None
            if "utc_offset" in activity:
                utc_offset = activity['utc_offset']
            else:
                utc_offset = None
            if "start_latlng" in activity:
                start_latlng = activity['start_latlng']
                #if start_latlng is not None: #Changed 2021/10/29
                if start_latlng:
                    start_latitude = start_latlng[0]
                    start_longitude  = start_latlng[1]
                else:
                    start_latitude = None
                    start_longitude  = None
            else:
                start_latitude = None
                start_longitude  = None
            if "end_latlng" in activity:
                end_latlng = activity['end_latlng']
                #if end_latlng is not None: #Changed 2021/10/29
                if end_latlng:
                    end_latitude = end_latlng[0]
                    end_longitude  = end_latlng[1]
                else:
                    end_latitude = None
                    end_longitude  = None
            else:
                end_latitude = None
                end_longitude  = None
            if "location_city" in activity:
                location_city = activity['location_city']
            else:
                location_city = None
            if "location_state" in activity:
                location_state = activity['location_state']
            else:
                location_state = None
            if "location_country" in activity:
                location_country = activity['location_country']
            else:
                location_country = None
            if "id" in activity['map']:
                map = activity['map']['id']
            else:
                map = None
            if "summary_polyline" in activity['map']:
                summary_polyline = activity['map']['summary_polyline']
            else:
                summary_polyline = None
            if "trainer" in activity:
                trainer = activity['trainer']
            else:
                trainer = None
            if "commute" in activity:
                commute = activity['commute']
            else:
                commute = None
            if "manual" in activity:
                manual = activity['manual']
            else:
                manual = None
            if "gear_id" in activity:
                gear_id = activity['gear_id']
            else:
                gear_id = None
            if "average_speed" in activity:
                average_speed = activity['average_speed']
            else:
                average_speed = None
            if "max_speed" in activity:
                max_speed = activity['max_speed']
            else:
                max_speed = None
            if "average_cadence" in activity:
                average_cadence = activity['average_cadence']
            else:
                average_cadence =  None
            if "average_temp" in activity:
                average_temp = activity['average_temp']
            else:
                average_temp = None
            if "average_watts" in activity:
                average_watts = activity['average_watts']
            else:
                average_watts = None
            if "weighted_average_watts" in activity:
                weighted_average_watts = activity['weighted_average_watts']
            else:
                weighted_average_watts = None
            if "kilojoules" in activity:
                kilojoules = activity['kilojoules']
            else:
                kilojoules = None
            if "device_watts" in activity:
                device_watts = activity['device_watts']
            else:
                device_watts = None
            if "average_heartrate" in activity:
                average_heartrate = activity['average_heartrate']
            else:
                average_heartrate = None
            if "max_heartrate" in activity:
                max_heartrate = activity['max_heartrate']
            else:
                max_heartrate = None
            if "max_watts" in activity:
                max_watts = activity['max_watts']
            else:
                max_watts = None
            if  "elev_high" in activity:
                elev_high = activity['elev_high']
            else:
                elev_high = None
            if "elev_low" in activity:
                elev_low = activity['elev_low']
            else:
                elev_low = None
            if "suffer_score" in activity:
                suffer_score = activity['suffer_score']
            else:
                suffer_score = None

            with StdoutRedirection(ath_un):
                print('Downloading Strava activity {} from: {}'.format(strava_activity_id,start_date_local))
            with ProgressStdoutRedirection(ath_un):
                 print('Downloading Strava activity {} from: {}'.format(strava_activity_id,start_date_local))

            #Insert activity summary data to DB
            try:       
                cur = conn.cursor()
                cur.execute(sql_insert_activity_summary,(ath_un,strava_activity_id,strava_athlete_id,name,distance,moving_time,elapsed_time,total_elevation_gain,
                           type,workout_type,external_id,upload_id,start_date,start_date_local,timezone,utc_offset,start_latitude,start_longitude,end_latitude,
                           end_longitude,location_city,location_state,location_country,map,summary_polyline,trainer,commute,manual,gear_id,average_speed,
                           max_speed,average_cadence,average_temp,average_watts,weighted_average_watts,kilojoules,device_watts,average_heartrate,max_heartrate,
                           max_watts,elev_high,elev_low,suffer_score)
                           )
                conn.commit()       
                cur.close()
                # Update the files table 
                data_file_path_insert(data_exist_for_activity,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
            
            #Get all available streams for the activity 
            types = 'time,distance,latlng,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth'
            df_columns = {'activity_id','time_gmt','distance','latitude','longitude','altitude','velocity_smooth','heartrate','cadence','watts','temp','moving','grade_smooth'}
            df_columns = sorted(df_columns)

            # Retry 3 times if request fails
            tries = 3
            for i in range(tries):
                try:
                    #Check if the oauth token is stil valid, and refresh if not.
                    if int(datetime.now().timestamp()) > expires_at:
                        oauth_token,expires_at = refresh_oauth_tokens()
                        header = {'Authorization':'Bearer {}'.format(oauth_token)}
                        with ProgressStdoutRedirection(ath_un):
                            print(str(datetime.now()) + 'The Strava oauth token expired and has been refreshed')
                    streams = requests.get("https://www.strava.com/api/v3/activities/{}/streams?keys={}".format(strava_activity_id,types),headers=header)
                    sleep_sec = api_rate_limits(streams)
                except Exception as e:
                    if i < tries - 1:
                        time.sleep(10)
                        continue
                    else:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                        raise
                break
            
            if sleep_sec == 0:
                pass
            else:
                time.sleep(sleep_sec)
                pass
            
            #TODO: if sleep_sec > 6hrs request a new access_token
            
            #Do something with the response/data

            activity_streams = json.loads(streams.text)
            #Check if there is data in activity_streams
            if 'message' in activity_streams:
                if "Resource Not Found" in activity_streams['message']:
                    with ErrorStdoutRedirection(ath_un):
                        print(str(datetime.now()) + ' No streams retrieved for {}. Moving onto next activity.'.format(strava_activity_id))
                    continue
                if "Rate Limit Exceeded" in activity_streams['message']:
                    with ErrorStdoutRedirection(ath_un):
                        print(str(datetime.now()) + ' Download Rate limit exceeded. This attempt did not get caught by api_rate_limits() function!')
                    #Usualy due to failed request on a very last attempt before limit, and subsequent succesfull retry.Too messy, move onto next activity and see what happens. 
                    continue
            else:
                pass

            activity_streams_df = pd.DataFrame(columns=df_columns)

            for stream in activity_streams:
                if "time" in stream['type']:
                    activity_id_list = []
                    time_stream = stream['data']
                    for i in range(len(time_stream)):
                        time_stream[i] = start_date_dt + timedelta(0,int(time_stream[i]))
                        time_stream[i] = datetime.strftime(time_stream[i], '%Y-%m-%d %H:%M:%S')
                        activity_id_list.append(strava_activity_id)
                    activity_streams_df['activity_id']=activity_id_list
                    activity_streams_df['time_gmt']=time_stream

                if "distance" in stream['type']:
                    distance_stream = stream['data']
                    activity_streams_df['distance']=distance_stream

                if "latlng" in stream['type']:
                    latlng_stream = stream['data']
                    latitude = []
                    longitude = []
                    if latlng_stream is not None:
                        for i in range(len(latlng_stream)):
                            latitude.append(latlng_stream[i][0])
                            longitude.append(latlng_stream[i][1])
                    activity_streams_df['latitude']=latitude
                    activity_streams_df['longitude']=longitude

                if "altitude" in stream['type']:
                    altitude_stream = stream['data']
                    activity_streams_df['altitude']=altitude_stream

                if "velocity_smooth" in stream['type']:
                    velocity_smooth_stream = stream['data']
                    activity_streams_df['velocity_smooth']=velocity_smooth_stream

                if "heartrate" in stream['type']:
                    heartrate_stream = stream['data']
                    activity_streams_df['heartrate']=heartrate_stream

                if "cadence" in stream['type']:
                    cadence_stream = stream['data']
                    activity_streams_df['cadence']=cadence_stream
 
                if "watts" in stream['type']:
                    watts_stream = stream['data']
                    activity_streams_df['watts']=watts_stream

                if "temp" in stream['type']:
                    temp_stream = stream['data']
                    activity_streams_df['temp']=temp_stream

                if "moving" in stream['type']:
                    moving_stream = stream['data']
                    activity_streams_df['moving']=moving_stream

                if "grade_smooth" in stream['type']:
                    grade_smooth_stream = stream['data']
                    activity_streams_df['grade_smooth']=grade_smooth_stream

            activity_streams_df = activity_streams_df.reindex(sorted(activity_streams_df.columns), axis=1) # Sort df alphabeticaly
            activity_streams_df = activity_streams_df.where(pd.notnull(activity_streams_df), None) # Replace NaN with None
            df2list = activity_streams_df.values.tolist()

            #Insert activity streams data to DB
            try:
                cur = conn.cursor()  
                for sublist in df2list:         
                    cur.execute(sql_insert_activity_streams,(sublist))
                    conn.commit()       
                cur.close()
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

        # increment page
        page += 1
   