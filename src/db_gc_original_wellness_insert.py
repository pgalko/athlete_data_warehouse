import psycopg2
from database_ini_parser import config
from fitparse import FitFile
from fitparse.records import FieldData
from fitparse.profile import FIELD_TYPE_TIMESTAMP
import datetime
import time
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

#PG: Function to calculate timestamp from timestamp_16
def fix_times(messages):                                                       
    timestamp=None                                                              
    timestamp_16=None                                                           
    real_time=0                                                                 
    UTC_REFERENCE = 631065600  # timestamp for UTC 00:00 Dec 31 1989            
    for message in messages:                                                                                                           
        #message["full_timestamp"]="TIMESTAMP"                                  
        field = message.get("timestamp")                                        
        if field is not None:                                                   
            timestamp = field.raw_value                                         
            #I'm not sure if this is correct to set this to None. Without it records with just timestamp doesn't have same new timestamp anymore which could be a bug or it should be that way                                          
            timestamp_16 = None                                                 
        tm_16 = message.get("timestamp_16")                                     
        if tm_16 is not None:                                                   
            timestamp_16 = tm_16.raw_value                                                                               
        if timestamp_16 is None:                                                
            ts_value = timestamp                                                
        else:                                                                   
            new_time = int( timestamp/2**16) * 2**16 + timestamp_16             
            if new_time >= real_time:                                           
                real_time = new_time                                            
            else:                                                               
                real_time = new_time + 2**16                                    
            ts_value = real_time                                                
        if ts_value is not None and ts_value >= 0x10000000:                     
            value = datetime.datetime.utcfromtimestamp(UTC_REFERENCE            
                    + ts_value)                                                 
        else:                                                                   
            value = None
                                                               
        message.fields.append(FieldData(field_def=None,field=FIELD_TYPE_TIMESTAMP,parent_field=None,value=value,raw_value=ts_value))                                          
                                                                              
        yield message

@processify
def gc_original_wellness_insert(file_path,athlete,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    start=time.time()
    file2import = (file_path)
    athlete_id = (athlete)
    db_name = (db_name)
    active_calories, active_time, activity_type, distance, duration_min, steps, timestamp, heart_rate, timestamp_16,intensity, stress_level_time, stress_level_value = [None]*12
    current_activity_type_intensity = (None)
    fitfile = FitFile(file2import)

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + athlete + '_PID.txt'
    open(pidfile, 'w').write(pid)
    
    messages = fitfile.get_messages()

    conn = None
         
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)
    #two-phase insert
    conn.tpc_begin(conn.xid(42, 'transaction ID', athlete))

    # Get all data messages 
    for message in fix_times(messages):
    # Go through all the data entries in this record
        for message_data in message:
            if message_data.name == 'active_calories':
                active_calories = message_data.value       
            if message_data.name == 'active_time':
                active_time = message_data.value
            if message_data.name == 'activity_type':
                activity_type = message_data.value
            if message_data.name == 'distance':
                distance = message_data.value
            if message_data.name == 'duration_min':
                duration_min = message_data.value
            if message_data.name == 'steps':
                steps = message_data.value
            if message_data.name == 'timestamp':
                timestamp = message_data.value
            if message_data.name == 'heart_rate':
                heart_rate = message_data.value
            if message_data.name == 'timestamp_16':
                timestamp_16 = message_data.value
            if message_data.name == 'intensity':
                intensity = message_data.value
            if message_data.name == 'stress_level_time':
                stress_level_time = message_data.value
            if message_data.name == 'stress_level_value':
                stress_level_value = message_data.value
            if message_data.name == 'current_activity_type_intensity':
                current_activity_type_intensity = message_data.value

        sql_act_type_summary = """

            INSERT INTO gc_original_wellness_act_type_summary(active_calories, active_time, activity_type, distance, duration_min, steps, timestamp,athlete_id)

            VALUES
            (%s,%s,%s,%s,%s,%s,%s,(select id from athlete where gc_email=%s))
            
            ON CONFLICT (athlete_id,activity_type,timestamp) DO NOTHING;

            """
        sql_hr_tracking = """

            INSERT INTO gc_original_wellness_hr_tracking(heart_rate, timestamp_16, timestamp,athlete_id)

            VALUES
            (%s,%s,%s,(select id from athlete where gc_email=%s))
            
            ON CONFLICT (athlete_id,timestamp) DO NOTHING;

            """
        sql_activity_tracking = """

            INSERT INTO gc_original_wellness_activity_tracking(activity_type, current_activity_type_intensity,intensity,timestamp,athlete_id)

            VALUES
            (%s,%s,%s,%s,(select id from athlete where gc_email=%s))
            
            ON CONFLICT (athlete_id,timestamp) DO NOTHING;

            """
            
        sql_stress_tracking = """

            INSERT INTO gc_original_wellness_stress_tracking(stress_level_time, stress_level_value,timestamp,athlete_id)

            VALUES
            (%s,%s,%s,(select id from athlete where gc_email=%s))
            
            ON CONFLICT (athlete_id,timestamp) DO NOTHING;

            """
        try:
            # create a cursor
            cur = conn.cursor()
            if duration_min is not None:
                # execute a statement
                with StdoutRedirection(athlete):
                    print(('Inserting Activity Type Summary record : ' + ' with timestamp:' + str(timestamp)))
                cur.execute(sql_act_type_summary,(active_calories, active_time, activity_type, distance, duration_min, steps, timestamp,athlete_id))
                # close the communication with the PostgreSQL
                cur.close()
                active_calories, active_time, activity_type, distance, duration_min, steps, timestamp, heart_rate, timestamp_16,intensity, stress_level_time, stress_level_value = [None]*12
                current_activity_type_intensity = (None)
                
            if heart_rate is not None:
                # execute a statement
                with StdoutRedirection(athlete):
                    print(('Inserting Heart Rate Tracking record : ' + ' with timestamp:' + str(timestamp)))
                cur.execute(sql_hr_tracking,(heart_rate, timestamp_16, timestamp,athlete_id))
                # close the communication with the PostgreSQL
                cur.close()
                active_calories, active_time, activity_type, distance, duration_min, steps, timestamp, heart_rate, timestamp_16,intensity, stress_level_time, stress_level_value = [None]*12
                current_activity_type_intensity = (None)
            
            if intensity is not None:
                # execute a statement
                with StdoutRedirection(athlete):
                    print(('Inserting Activity Tracking record : ' + ' with timestamp:' + str(timestamp)))
                cur.execute(sql_activity_tracking,(activity_type, list(current_activity_type_intensity),intensity,timestamp,athlete_id))
                # close the communication with the PostgreSQL
                cur.close()
                active_calories, active_time, activity_type, distance, duration_min, steps, timestamp, heart_rate, timestamp_16,intensity, stress_level_time, stress_level_value = [None]*12
                current_activity_type_intensity = (None)
                
            if stress_level_value is not None:
                # execute a statement
                with StdoutRedirection(athlete):
                    print(('Inserting Stress Tracking record : ' + ' with timestamp:' + str(timestamp)))
                cur.execute(sql_stress_tracking,(stress_level_time, stress_level_value,timestamp,athlete_id))
                # close the communication with the PostgreSQL
                cur.close()
                active_calories, active_time, activity_type, distance, duration_min, steps, timestamp, heart_rate, timestamp_16,intensity, stress_level_time, stress_level_value = [None]*12
                current_activity_type_intensity = (None)
                    
        except  (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    #two-phase insert commit or rollback
    try:
        conn.tpc_prepare()
    except  (Exception, psycopg2.DatabaseError) as error:
        conn.tpc_rollback()
        with ErrorStdoutRedirection(athlete):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
    else:
        try:
            conn.tpc_commit()
        except Exception as e:
            with ErrorStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))      
       
    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()  
                
    with StdoutRedirection(athlete):
        print('--- All wellness record data inserted successfully. ---')
    with ProgressStdoutRedirection(athlete):
        print('--- All wellness record data inserted successfully. ---')

    end = time.time()
    with ProgressStdoutRedirection(athlete):
        print('\nExecution_time:')
    with ProgressStdoutRedirection(athlete):
        print((end-start))
    
        
