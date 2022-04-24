
import psycopg2
from database_ini_parser import config
from fitparse import FitFile
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os
import time
import datetime
import numpy as np
from scipy.stats import zscore				  

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_original_record_insert(file_path,activity_id,ath_un,db_host,db_name,superuser_un,superuser_pw, encr_pass):
    start=time.time()
    file2import = (file_path)
    gc_activity_id = (activity_id)
    ath_un = (ath_un)
    db_name = (db_name)
    activity_type,altitude,cadence,distance,enhanced_altitude,enhanced_speed,fractional_cadence,heart_rate,position_lat,position_long,speed,stance_time,stance_time_balance,step_length,timestamp,vertical_oscillation,vertical_ratio,accumulated_power,left_pedal_smoothness,left_torque_effectiveness,power,right_pedal_smoothness,right_torque_effectiveness,temperature,avg_speed,avg_swimming_cadence,event,event_group,event_type,length_type,message_index,start_time,swim_stroke,total_calories,total_elapsed_time,total_strokes,total_timer_time,respiration_rate,performance_condition,est_core_temp,alpha1,alpha1_raw = [None]*42
    hrv_record_list = (None, None, None, None)
    hrv_record_list_combined = []
    hrv_rmssd = None
    hrv_sdrr = None
    hrv_pnn50 = None
    hrv_pnn20 = None										  
    fitfile = FitFile(file2import)

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)
 
    conn = None
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)
    # two-phase insert prepapre
    conn.tpc_begin(conn.xid(42, 'transaction ID', ath_un))

    # Get all data messages that are of type record
    for record in fitfile.get_messages('record'):
    # Go through all the data entries in this record
        for record_data in record:
            if record_data.name == 'activity_type':
                activity_type = record_data.value
            if record_data.name == 'altitude':
                altitude = record_data.value
            if record_data.name == 'cadence':
                cadence = record_data.value
            if record_data.name == 'distance':
                distance = record_data.value
            if record_data.name == 'enhanced_altitude':
                enhanced_altitude = record_data.value     
            if record_data.name == 'enhanced_speed':
                enhanced_speed = record_data.value
            if record_data.name == 'fractional_cadence':
                fractional_cadence = record_data.value
            if record_data.name == 'heart_rate':
                heart_rate = record_data.value
            if record_data.name == 'position_lat':
                position_lat = record_data.value
            if record_data.name == 'position_long':
                position_long = record_data.value
            if record_data.name == 'speed':
                speed = record_data.value
            if record_data.name == 'stance_time':
                stance_time = record_data.value
            if record_data.name == 'stance_time_balance':
                stance_time_balance = record_data.value
            if record_data.name == 'step_length':
                step_length = record_data.value
            if record_data.name == 'timestamp':
                timestamp = record_data.value
            if record_data.name == 'vertical_oscillation':
                vertical_oscillation = record_data.value
            if record_data.name == 'vertical_ratio':
                vertical_ratio = record_data.value
            if record_data.name == 'accumulated_power':
                accumulated_power = record_data.value
            if record_data.name == 'left_pedal_smoothness':
                left_pedal_smoothness = record_data.value
            if record_data.name == 'left_torque_effectiveness':
                left_torque_effectiveness = record_data.value
            if record_data.name == 'power':
                power = record_data.value
            if record_data.name == 'right_pedal_smoothness':
                right_pedal_smoothness = record_data.value
            if record_data.name == 'right_torque_effectiveness':
                right_torque_effectiveness = record_data.value
            if record_data.name == 'temperature':
                temperature = record_data.value
            if record_data.name == 'unknown_108':
                respiration_rate = record_data.value/100
            if record_data.name == 'unknown_90':
                performance_condition = record_data.value
            if record_data.name == 'Est Core Temp':
                est_core_temp = record_data.value
            if record_data.name == 'Alpha1':
                alpha1 = record_data.value
            if record_data.name == 'Alpha1 (raw)':
                alpha1_raw = record_data.value									   

        sql = """

            INSERT INTO garmin_connect_original_record (activity_type,altitude,cadence,distance,enhanced_altitude,enhanced_speed,fractional_cadence,heart_rate,position_lat
            ,position_long,speed,stance_time,stance_time_balance,step_length,timestamp,vertical_oscillation,vertical_ratio,accumulated_power
            ,left_pedal_smoothness,left_torque_effectiveness,power,right_pedal_smoothness,right_torque_effectiveness,temperature
            ,respiration_rate,performance_condition,est_core_temp,alpha1,alpha1_raw,gc_activity_id,lap_id)

            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,(select id from garmin_connect_original_lap where timestamp >= %s and start_time < %s LIMIT 1))
            
            ON CONFLICT (timestamp,lap_id) DO NOTHING;


            """
        try:
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            with StdoutRedirection(ath_un):
                print(('Inserting track record from session: ' + str(gc_activity_id) + ' with timestamp:' + str(timestamp)))
            cur.execute(sql,(activity_type,altitude,cadence,distance,enhanced_altitude,enhanced_speed,fractional_cadence,heart_rate,position_lat,position_long,speed,stance_time,
                            stance_time_balance,step_length,timestamp,vertical_oscillation,vertical_ratio,accumulated_power,left_pedal_smoothness,left_torque_effectiveness,
                            power,right_pedal_smoothness,right_torque_effectiveness,temperature,respiration_rate,performance_condition,
                            est_core_temp,alpha1,alpha1_raw,gc_activity_id,str(timestamp),str(timestamp)))

            cur.close()       
        except  (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    # Get all data messages that are of type hrv
    for record in fitfile.get_messages('hrv'):
        # Go through all the data entries in this record
        for record_data in record:
            if record_data.name == 'time':
                hrv_record_list = record_data.value
                for i in hrv_record_list:
                    if i != None:
                        hrv_record = i
                        hrv_record_list_combined.append(hrv_record*1000)

                        sql_hrv = """
                        INSERT INTO garmin_connect_hrv_tracking(gc_activity_id,hrv)
                        VALUES
                        (%s,%s);
                        """
                        try:
                            # create a cursor
                            cur = conn.cursor()
                            # execute a statement
                            with StdoutRedirection(ath_un):
                                print(('Inserting hrv record from session: ' + str(gc_activity_id)))
                            cur.execute(sql_hrv,(gc_activity_id,hrv_record))
                            # close the communication with the PostgreSQL 
                            cur.close()              
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    else:
                        continue

    # two-phase insert commit or rollback
    try:
        conn.tpc_prepare()
    except  (Exception, psycopg2.DatabaseError) as error:
        conn.tpc_rollback()
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
    else:
        try:
            conn.tpc_commit()
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

    #PG: Add Pool Swim specific data
    for record in fitfile.get_messages('sport'):  
        for record_data in record:
            sport = record_data.value
            if sport == 'Pool Swim':
                with StdoutRedirection(ath_un):
                    print(('Activity ' + str(gc_activity_id) + ' is a Pool Swim. Inserting additional data'))  
                
                for record in fitfile.get_messages('length'):

                    for record_data in record:
                        if record_data.name == 'avg_speed':
                            avg_speed = record_data.value  
                        if record_data.name == 'avg_swimming_cadence':
                            avg_swimming_cadence = record_data.value  
                        if record_data.name == 'event_group':
                            event_group = record_data.value  
                        if record_data.name == 'event_type':
                            event_type = record_data.value    
                        if record_data.name == 'length_type':
                            length_type = record_data.value    
                        if record_data.name == 'message_index':
                            message_index = record_data.value     
                        if record_data.name == 'start_time':
                            start_time = record_data.value      
                        if record_data.name == 'swim_stroke':
                            swim_stroke = record_data.value     
                        if record_data.name == 'timestamp':
                            timestamp = record_data.value      
                        if record_data.name == 'total_calories':
                            total_calories = record_data.value       
                        if record_data.name == 'total_elapsed_time':
                            total_elapsed_time = record_data.value      
                        if record_data.name == 'total_strokes':
                            total_strokes = record_data.value       
                        if record_data.name == 'total_timer_time':
                            total_timer_time = record_data.value

                    sql_swim = """

                    CREATE TEMPORARY TABLE temp_garmin_connect_original_record(avg_speed real,avg_swimming_cadence int,event varchar,event_group varchar,event_type varchar,length_type varchar,message_index int
                                                ,start_time varchar,swim_stroke varchar,total_calories int,total_elapsed_time real,total_strokes int,total_timer_time real, timestamp varchar) ON COMMIT DROP;

                    INSERT INTO temp_garmin_connect_original_record (avg_speed,avg_swimming_cadence,event,event_group,event_type,length_type,message_index
                                    ,start_time,swim_stroke,total_calories,total_elapsed_time,total_strokes,total_timer_time,timestamp)

                    VALUES

                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);

                    UPDATE garmin_connect_original_record
                    SET avg_speed = temp_garmin_connect_original_record.avg_speed,
                        avg_swimming_cadence = temp_garmin_connect_original_record.avg_swimming_cadence,
                        event = temp_garmin_connect_original_record.event,
                        event_group = temp_garmin_connect_original_record.event_group,
                        event_type = temp_garmin_connect_original_record.event_type,
                        length_type = temp_garmin_connect_original_record.length_type,
                        message_index = temp_garmin_connect_original_record.message_index,
                        start_time = temp_garmin_connect_original_record.start_time,
                        swim_stroke = temp_garmin_connect_original_record.swim_stroke,
                        total_calories = temp_garmin_connect_original_record.total_calories,
                        total_elapsed_time = temp_garmin_connect_original_record.total_elapsed_time,
                        total_strokes = temp_garmin_connect_original_record.total_strokes,
                        total_timer_time = temp_garmin_connect_original_record.total_timer_time
                    FROM temp_garmin_connect_original_record
                    WHERE temp_garmin_connect_original_record.timestamp = garmin_connect_original_record.timestamp and garmin_connect_original_record.gc_activity_id = %s;


                    """
                    try:
                        # create a cursor
                        cur = conn.cursor()
                        # execute a statement
                        with StdoutRedirection(ath_un):
                            print(('Inserting Pool swim data record from session: ' + str(gc_activity_id) + ' with timestamp:' + str(timestamp)))
                        cur.execute(sql_swim,(avg_speed,avg_swimming_cadence,event,event_group,event_type,length_type,message_index,start_time,swim_stroke,total_calories,total_elapsed_time,total_strokes,total_timer_time,timestamp,gc_activity_id))
                        conn.commit()
                        # close the communication with the PostgreSQL
                        cur.close()            
                    except Exception as e:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    
    with StdoutRedirection(ath_un):
        print(('--- All record data for session: ' + str(gc_activity_id) + ' inserted successfully. ---'))
    with ProgressStdoutRedirection(ath_un):
        print(('--- All record data for session: ' + str(gc_activity_id) + ' inserted successfully. ---'))
    
    #Correct Errors(as per https://medium.com/orikami-blog/exploring-heart-rate-variability-using-python-483a7037c64d). 
    #Change all values with SD > 2 to mean
    hrv_record_list_combined = np.array(hrv_record_list_combined)
    hrv_record_list_combined[np.abs(zscore(hrv_record_list_combined)) > 2] = np.median(hrv_record_list_combined)

    #Calculate the square root of the mean square of the differences of RR-intervals
    hrv_rmssd = np.sqrt(np.mean(np.square(np.diff(hrv_record_list_combined))))
    #Calculate the standard deviation of the RR-intervals
    hrv_sdrr = np.std(hrv_record_list_combined)
    #Calculate the number of pairs of successive RR-intervals that differ by more than 50/20 ms
    nn50 = np.sum(np.abs(np.diff(hrv_record_list_combined)) > 50)*1
    nn20 = np.sum(np.abs(np.diff(hrv_record_list_combined)) > 20)*1
    #Calculate he proportion of NN50/NN20 divided by the total number of RR-intervals.
    hrv_pnn50 = 100 * nn50 / len(hrv_record_list_combined)
    hrv_pnn20 = 100 * nn20 / len(hrv_record_list_combined)

    sql_hrv_stats = '''
    UPDATE garmin_connect_original_session
    SET hrv_rmssd = %s,
        hrv_sdrr = %s,
        hrv_pnn50 = %s,
        hrv_pnn20 = %s
    WHERE gc_activity_id = %s;
    '''
    
    try:
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        with StdoutRedirection(ath_un):
            print(('Inserting hrv stats for session: ' + str(gc_activity_id)))
        cur.execute(sql_hrv_stats,(hrv_rmssd,hrv_sdrr,hrv_pnn50,hrv_pnn20,gc_activity_id))
        conn.commit()
        # close the communication with the PostgreSQL 
        cur.close()
            
    except Exception as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()

    end = time.time()
    with ProgressStdoutRedirection(ath_un):
        print('\nExecution_time:')
    with ProgressStdoutRedirection(ath_un):
        print((end-start))
