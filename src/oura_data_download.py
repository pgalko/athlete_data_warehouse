import os
import requests
import pandas as pd
import psycopg2
import datetime
import pytz
import base64
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
import Crypto.Random
from Crypto.Cipher import AES
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
import sys
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
def dwnld_insert_oura_data(ath_un,db_host,db_name,superuser_un,superuser_pw,oura_refresh_token,start_date_dt,end_date_dt,save_pwd,encr_pass):

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)
    
    oura_params = config(filename="encrypted_settings.ini", section="oura",encr_pass=encr_pass)
    OURA_CLIENT_ID = str(oura_params.get("oura_client_id"))
    OURA_CLIENT_SECRET = str(oura_params.get("oura_client_secret"))
    OURA_TOKEN_URL = str(oura_params.get("oura_token_url"))
    
    #Refresh the access token
    payload = dict(grant_type='refresh_token', refresh_token=oura_refresh_token,client_id=OURA_CLIENT_ID,client_secret=OURA_CLIENT_SECRET)
    refresh = requests.post(OURA_TOKEN_URL, data=payload)
    response = refresh.json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']

    if save_pwd == True:
        encrypted_refresh_token = base64.b64encode(encrypt(refresh_token, encr_pass))
        encrypted_refresh_token = encrypted_refresh_token.decode('utf-8')
    else:
        encrypted_refresh_token = None

    end_date_today_dt = end_date_dt + datetime.timedelta(days=1)

    start_date = datetime.datetime.strftime(start_date_dt,"%Y-%m-%d")
    end_date = datetime.datetime.strftime(end_date_dt,"%Y-%m-%d")
    end_date_today = datetime.datetime.strftime(end_date_today_dt,"%Y-%m-%d")

    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)
 
    sql_insert_oura_refresh_token = """

        DO
            $do$
                BEGIN
                    IF EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN
                        UPDATE athlete SET oura_refresh_token = %s where ath_un= %s;
                    END IF;
                END
            $do$

    """

    sql_insert_sleep_summary = """

        INSERT INTO oura_sleep_daily_summary(athlete_id,summary_date,period_id,is_longest,timezone,bedtime_start,bedtime_end,score,score_total,score_disturbances,
        score_efficiency,score_latency,score_rem,score_deep,score_alignment,total,duration,awake,light,rem,deep,onset_latency,restless,efficiency,midpoint_time,hr_lowest,
        hr_average ,rmssd,breath_average ,temperature_delta ,bedtime_end_delta,midpoint_at_delta,bedtime_start_delta,temperature_deviation,temperature_trend_deviation)

        VALUES
        ((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (summary_date,period_id) DO NOTHING;
        
    """

    sql_insert_activity_summary = """

        INSERT INTO oura_activity_daily_summary(athlete_id,summary_date,day_start,day_end,timezone,score,score_stay_active,score_move_every_hour,score_meet_daily_targets,
        score_training_frequency,score_training_volume,score_recovery_time,daily_movement,non_wear,rest,inactive,inactivity_alerts,low,medium,high,steps,cal_total,
        cal_active,met_min_inactive,met_min_low,met_min_medium,met_min_high,average_met,rest_mode_state,to_target_km,target_miles,total,to_target_miles,target_calories,target_km)

        VALUES
        ((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (summary_date) DO UPDATE
        
        SET (athlete_id,summary_date,day_start,day_end,timezone,score,score_stay_active,score_move_every_hour,score_meet_daily_targets,
        score_training_frequency,score_training_volume,score_recovery_time,daily_movement,non_wear,rest,inactive,inactivity_alerts,low,medium,high,steps,cal_total,
        cal_active,met_min_inactive,met_min_low,met_min_medium,met_min_high,average_met,rest_mode_state,to_target_km,target_miles,total,to_target_miles,target_calories,target_km)
        =((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        WHERE oura_activity_daily_summary.summary_date
        = %s
    """

    sql_insert_readiness_summary = """

        INSERT INTO oura_readiness_daily_summary(athlete_id,summary_date,period_id,score,score_previous_night,score_sleep_balance,score_previous_day,
        score_activity_balance,score_resting_hr,score_hrv_balance,score_recovery_index,score_temperature,rest_mode_state)

        VALUES
        ((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (summary_date,period_id) DO NOTHING;
        
    """

    sql_insert_sleep_detail = """

        INSERT INTO oura_sleep_detail(oura_sleep_id,timestamp_gmt,hypnogram_5min,hr_5min,rmssd_5min)

        VALUES
        ((select id from oura_sleep_daily_summary where summary_date=%s and period_id=%s),%s,%s,%s,%s)

        ON CONFLICT (timestamp_gmt) DO NOTHING;
        
    """

    sql_insert_activity_detail = """

        INSERT INTO oura_activity_detail(oura_activity_id,timestamp_gmt,class_5min,met_1min)

        VALUES
        ((select id from oura_activity_daily_summary where summary_date=%s),%s,%s,%s)

        ON CONFLICT (timestamp_gmt) DO UPDATE

        SET (oura_activity_id,timestamp_gmt,class_5min,met_1min)
        = ((select id from oura_activity_daily_summary where summary_date=%s),%s,%s,%s)

        WHERE oura_activity_detail.timestamp_gmt = %s;
        
    """

    sql_insert_utc_offset = """
        INSERT INTO gmt_local_time_difference (athlete_id,local_date,local_midnight_timestamp,gmt_midnight_timestamp,gmt_local_difference)

        VALUES
            ((select id from athlete where ath_un=%s),%s,%s,%s,%s)

        ON CONFLICT (local_date) DO NOTHING;
    """

    try:       
        cur = conn.cursor()
        cur.execute(sql_insert_oura_refresh_token,(ath_un,encrypted_refresh_token,ath_un))
        conn.commit()       
        cur.close()
    except Exception as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))


    #------------------- Retrieve Sleep data ---------------------------

    sleep_data = requests.get('https://api.ouraring.com/v1/sleep?'
                              'start={}&end={}&access_token={}'
                              .format(start_date, end_date, access_token))
    json_sleep = sleep_data.json()
    sleep_df = pd.DataFrame(json_sleep['sleep'])
    ####sleep_df = sleep_df.fillna(0)
    sleep_df = sleep_df.where(pd.notnull(sleep_df), None)

    for row in sleep_df.itertuples():
        awake = row.awake
        bedtime_end = row.bedtime_end
        #convert bedtime_end to utc
        bedtime_end = datetime.datetime.strptime((bedtime_end), "%Y-%m-%dT%H:%M:%S%z")
        bedtime_end = bedtime_end.astimezone(pytz.utc)
        bedtime_end_delta = row.bedtime_end_delta
        bedtime_start = row.bedtime_start
        #convert bedtime_start to utc
        bedtime_start = datetime.datetime.strptime((bedtime_start), "%Y-%m-%dT%H:%M:%S%z")
        bedtime_start = bedtime_start.astimezone(pytz.utc)
        bedtime_start_delta = row.bedtime_start_delta
        breath_average = row.breath_average
        deep = row.deep
        duration = row.duration
        efficiency = row.efficiency
        hr_5min = row.hr_5min
        hr_average = row.hr_average
        hr_lowest = row.hr_lowest
        hypnogram_5min = row.hypnogram_5min
        is_longest = row.is_longest
        light = row.light
        midpoint_at_delta = row.midpoint_at_delta
        midpoint_time = row.midpoint_time
        onset_latency = row.onset_latency
        period_id = row.period_id
        rem = row.rem
        restless = row.restless
        rmssd = row.rmssd
        rmssd_5min = row.rmssd_5min
        score = row.score
        score_alignment = row.score_alignment
        score_deep = row.score_deep
        score_disturbances = row.score_disturbances
        score_efficiency = row.score_efficiency
        score_latency = row.score_latency
        score_rem = row.score_rem
        score_total = row.score_total
        summary_date = row.summary_date
        temperature_delta = row.temperature_delta
        temperature_deviation = row.temperature_deviation
        temperature_trend_deviation = row.temperature_trend_deviation
        timezone = row.timezone
        total = row.total

        with StdoutRedirection(ath_un):
            print('Downloading Oura sleep data from: {}'.format(summary_date))
        with ProgressStdoutRedirection(ath_un):
            print('Downloading Oura sleep data from: {}'.format(summary_date))

        try:       
            cur = conn.cursor()
            cur.execute(sql_insert_sleep_summary,(ath_un,summary_date,period_id,is_longest,timezone,datetime.datetime.strftime(bedtime_start,"%Y-%m-%d %H:%M:%S"),
                       datetime.datetime.strftime(bedtime_end,"%Y-%m-%d %H:%M:%S"),score,score_total,score_disturbances,score_efficiency,score_latency,score_rem,score_deep,
                       score_alignment,total,duration,awake,light,rem,deep,onset_latency,restless,efficiency,midpoint_time,hr_lowest,hr_average ,rmssd,breath_average ,
                       temperature_delta,bedtime_end_delta,midpoint_at_delta,bedtime_start_delta,temperature_deviation,temperature_trend_deviation)
                       )
            conn.commit()       
            cur.close()
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

        #Create and populate a list of 5min intervals starting from bedtime_start
        rmssd_ints = []
        #add first value (bedtime_start) to 5 min intervals list
        rmssd_ints.append(datetime.datetime.strftime(bedtime_start,"%Y-%m-%d %H:%M:%S"))
        rmssd_int = bedtime_start
        
        for i in range (len(rmssd_5min)-1):
            rmssd_int = rmssd_int + datetime.timedelta(seconds=300)
            rmssd_int_str = datetime.datetime.strftime(rmssd_int,"%Y-%m-%d %H:%M:%S")
            rmssd_ints.append(rmssd_int_str)
        
        #Create sleep detail dataframe
        sleep_detail_df = pd.DataFrame({'timestamp': pd.Series(rmssd_ints), 'hr_5min': pd.Series(hr_5min),'hypnogram_5min': pd.Series(list(hypnogram_5min)),'rmssd_5min': pd.Series(rmssd_5min)})
        ####sleep_detail_df = sleep_detail_df.fillna(0)
        sleep_detail_df = sleep_detail_df.where(pd.notnull(sleep_detail_df), None)
        
        for row in sleep_detail_df.itertuples():
            timestamp_row = row.timestamp
            hr_5min_row = row.hr_5min
            hypnogram_5min_row = row.hypnogram_5min
            rmssd_5min_row = row.rmssd_5min

            try:       
                cur = conn.cursor()
                cur.execute(sql_insert_sleep_detail,(summary_date,period_id,timestamp_row,hypnogram_5min_row,hr_5min_row,rmssd_5min_row))
                conn.commit()       
                cur.close()
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))



    #------------------- Retrieve Activity data ---------------------------
    
    
    activity_data = requests.get('https://api.ouraring.com/v1/activity?'
                              'start={}&end={}&access_token={}'
                              .format(start_date, end_date_today, access_token))
    json_activity = activity_data.json()
    activity_df = pd.DataFrame(json_activity['activity'])
    ####activity_df = activity_df.fillna(0)
    activity_df = activity_df.where(pd.notnull(activity_df), None)

    for row in activity_df.itertuples(): 
        average_met = row.average_met
        cal_active = row.cal_active
        cal_total = row.cal_total
        class_5min = row.class_5min
        daily_movement = row.daily_movement
        day_end = row.day_end
        #convert day_end to utc
        day_end = datetime.datetime.strptime((day_end), "%Y-%m-%dT%H:%M:%S%z")
        day_end = day_end.astimezone(pytz.utc)
        day_start = row.day_start
        #convert day_start to utc
        day_start = datetime.datetime.strptime((day_start), "%Y-%m-%dT%H:%M:%S%z")
        day_start = day_start.astimezone(pytz.utc)
        high = row.high
        inactive = row.inactive
        inactivity_alerts = row.inactivity_alerts
        low = row.low
        medium = row.medium
        met_1min = row.met_1min
        met_min_high = row.met_min_high
        met_min_inactive = row.met_min_inactive
        met_min_low = row.met_min_low
        met_min_medium = row.met_min_medium
        non_wear = row.non_wear
        rest = row.rest
        try:
            rest_mode_state = row.rest_mode_state
        except:
            rest_mode_state = None
        try:
            score = row.score
            score_meet_daily_targets = row.score_meet_daily_targets
            score_move_every_hour = row.score_move_every_hour
            score_recovery_time = row.score_recovery_time
            score_stay_active = row.score_stay_active
            score_training_frequency = row.score_training_frequency
            score_training_volume = row.score_training_volume
        #If Ouraring rest mode enabled
        except:
            score=score_meet_daily_targets=score_move_every_hour=score_recovery_time=score_stay_active=score_training_frequency=score_training_volume=None
        steps = row.steps
        summary_date = row.summary_date
        target_calories = row.target_calories
        target_km = row.target_km
        target_miles = row.target_miles
        timezone = row.timezone
        to_target_km = row.to_target_km
        to_target_miles = row.to_target_miles
        total = row.total


        with StdoutRedirection(ath_un):
            print('Downloading Oura activity data from: {}'.format(summary_date))
        with ProgressStdoutRedirection(ath_un):
            print('Downloading Oura activity data from: {}'.format(summary_date))

        try:       
            cur = conn.cursor()
            cur.execute(sql_insert_activity_summary,(ath_un,summary_date,datetime.datetime.strftime(day_start,"%Y-%m-%d %H:%M:%S"),datetime.datetime.strftime(day_end,"%Y-%m-%d %H:%M:%S"),
                        timezone,score,score_stay_active,score_move_every_hour,score_meet_daily_targets,score_training_frequency,score_training_volume,score_recovery_time,daily_movement,
                        non_wear,rest,inactive,inactivity_alerts,low,medium,high,steps,cal_total,cal_active,met_min_inactive,met_min_low,met_min_medium,met_min_high,average_met,
                        rest_mode_state,to_target_km,target_miles,total,to_target_miles,target_calories,target_km,
                        ath_un,summary_date,datetime.datetime.strftime(day_start,"%Y-%m-%d %H:%M:%S"),datetime.datetime.strftime(day_end,"%Y-%m-%d %H:%M:%S"),
                        timezone,score,score_stay_active,score_move_every_hour,score_meet_daily_targets,score_training_frequency,score_training_volume,score_recovery_time,daily_movement,
                        non_wear,rest,inactive,inactivity_alerts,low,medium,high,steps,cal_total,cal_active,met_min_inactive,met_min_low,met_min_medium,met_min_high,average_met,
                        rest_mode_state,to_target_km,target_miles,total,to_target_miles,target_calories,target_km,summary_date)
                        )
            conn.commit()       
            cur.close()

            #Insert utc offset into gmt_local_time_difference table if the record not already present from gc
            gmt_local_difference = datetime.timedelta(minutes=timezone)
            local_midnight = datetime.datetime.strptime(summary_date, '%Y-%m-%d')
            gmt_midnight = local_midnight-gmt_local_difference
            local_date = local_midnight.date()

            cur = conn.cursor()
            cur.execute(sql_insert_utc_offset,(ath_un,local_date,local_midnight,gmt_midnight,gmt_local_difference))
            conn.commit()       
            cur.close()
        
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
  
        #Create and populate a list of 1min intervals starting from day_start
        met_ints = []
        #add first value (day_start) to 1 min intervals list
        met_ints.append(datetime.datetime.strftime(day_start,"%Y-%m-%d %H:%M:%S"))
        met_int = day_start
        
        for i in range (len(met_1min)-1):
            met_int = met_int + datetime.timedelta(seconds=60)
            met_int_str = datetime.datetime.strftime(met_int,"%Y-%m-%d %H:%M:%S")
            met_ints.append(met_int_str)
        
        #Pad class_5min_list to match the size of 1min list's
        class_5min_list = list(class_5min)
        def insert_element_list(lst, x, n):
            i = n
            while i < len(lst):
                lst.insert(i, x)
                i+= n+1
            return lst
        
        #Add 4 new "0" elements after every original element
        n=1
        for i in range(4):
            insert_element_list(class_5min_list,'0',n)
            n=n+1

        activity_detail_df = pd.DataFrame({'timestamp': pd.Series(met_ints), 'met_1min': pd.Series(met_1min),'class_5min': pd.Series(class_5min_list)})
        ####activity_detail_df = activity_detail_df.fillna(0)
        activity_detail_df = activity_detail_df.where(pd.notnull(activity_detail_df), None)
        
        for row in activity_detail_df.itertuples():
            timestamp_row = row.timestamp
            met_1min_row = row.met_1min
            class_5min_row = row.class_5min

            try:       
                cur = conn.cursor()
                cur.execute(sql_insert_activity_detail,(summary_date,timestamp_row,class_5min_row,met_1min_row,
                           summary_date,timestamp_row,class_5min_row,met_1min_row,timestamp_row))
                conn.commit()       
                cur.close()
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

    
    #------------------- Retrieve Readiness data ---------------------------
     
    readiness_data = requests.get('https://api.ouraring.com/v1/readiness?'
                              'start={}&end={}&access_token={}'
                              .format(start_date, end_date, access_token))
    json_readiness = readiness_data.json()
    readiness_df = pd.DataFrame(json_readiness['readiness'])
    ####readiness_df = readiness_df.fillna(0)
    readiness_df = readiness_df.where(pd.notnull(readiness_df), None)


    for row in readiness_df.itertuples(): 
        try:
            period_id = row.period_id
            rest_mode_state = row.rest_mode_state
        except:
            period_id = rest_mode_state = None
        score = row.score
        score_activity_balance = row.score_activity_balance
        score_hrv_balance = row.score_hrv_balance
        score_previous_day = row.score_previous_day
        score_previous_night = row.score_previous_night 
        score_recovery_index = row.score_recovery_index
        score_resting_hr = row.score_resting_hr
        score_sleep_balance = row.score_sleep_balance 
        score_temperature = row.score_temperature
        summary_date = row.summary_date

        with StdoutRedirection(ath_un):
            print('Downloading Oura readiness data from: {}'.format(summary_date))
        with ProgressStdoutRedirection(ath_un):
            print('Downloading Oura readiness data from: {}'.format(summary_date))

        try:       
            cur = conn.cursor()
            cur.execute(sql_insert_readiness_summary,(ath_un,summary_date,period_id,score,score_previous_night,score_sleep_balance,score_previous_day,
                    score_activity_balance,score_resting_hr,score_hrv_balance,score_recovery_index,score_temperature,rest_mode_state)
                        )
            conn.commit()       
            cur.close()

        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
