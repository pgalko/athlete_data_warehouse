import psycopg2
from database_ini_parser import config
from fitparse import FitFile
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_original_lap_insert(file_path,activity_id,username, db_host,db_name,superuser_un,superuser_pw,encr_pass):
    file2import = (file_path)
    gc_activity_id = (activity_id)
    username = (username)
    db_name = (db_name)
    avg_cadence,avg_combined_pedal_smoothness,avg_heart_rate,avg_left_pco,avg_left_pedal_smoothness,avg_left_torque_effectiveness,avg_power,avg_right_pco,avg_right_pedal_smoothness,avg_right_torque_effectiveness,avg_speed,end_position_lat,end_position_long,enhanced_avg_speed,enhanced_max_speed,event,event_group,event_type,intensity,lap_trigger,left_right_balance,max_cadence,max_heart_rate,max_power,max_speed,message_index,normalized_power,sport,stand_count,start_position_lat,start_position_long,start_time,time_standing,timestamp,total_ascent,total_calories,total_cycles,total_descent,total_distance,total_elapsed_time,total_fat_calories,total_timer_time,total_work = [None]*43
    avg_cadence_position = (None, None)
    avg_left_power_phase = (None, None, None, None)
    avg_left_power_phase_peak = (None, None, None, None)
    avg_power_position = (None, None)
    avg_right_power_phase = (None, None, None, None)
    avg_right_power_phase_peak = (None, None, None, None)
    max_cadence_position = (None, None)
    max_power_position = (None, None)
    
    fitfile = FitFile(file2import)

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + username + '_PID.txt'
    open(pidfile, 'w').write(pid)

    conn = None
         
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)


    # Get all data messages that are of type record
    for record in fitfile.get_messages('lap'):
        # Go through all the data entries in this record
        for record_data in record:
            if record_data.name == 'avg_cadence':
                avg_cadence = record_data.value
            if record_data.name == 'avg_cadence_position':
                avg_cadence_position = record_data.value
            if record_data.name == 'avg_combined_pedal_smoothness':
                avg_combined_pedal_smoothness = record_data.value
            if record_data.name == 'avg_heart_rate':
                avg_heart_rate = record_data.value
            if record_data.name == 'avg_left_pco':
                avg_left_pco = record_data.value       
            if record_data.name == 'avg_left_pedal_smoothness':
                avg_left_pedal_smoothness = record_data.value
            if record_data.name == 'avg_left_power_phase':
                avg_left_power_phase = record_data.value
            if record_data.name == 'avg_left_power_phase_peak':
                avg_left_power_phase_peak = record_data.value
            if record_data.name == 'avg_left_torque_effectiveness':
                avg_left_torque_effectiveness = record_data.value
            if record_data.name == 'avg_power':
                avg_power = record_data.value
            if record_data.name == 'avg_power_position':
                avg_power_position = record_data.value
            if record_data.name == 'avg_right_pco':
                avg_right_pco = record_data.value
            if record_data.name == 'avg_right_pedal_smoothness':
                avg_right_pedal_smoothness = record_data.value
            if record_data.name == 'avg_right_power_phase':
                avg_right_power_phase = record_data.value   
            if record_data.name == 'avg_right_power_phase_peak':
                avg_right_power_phase_peak = record_data.value
            if record_data.name == 'avg_right_torque_effectiveness':
                avg_right_torque_effectiveness = record_data.value
            if record_data.name == 'avg_speed':
                avg_speed = record_data.value       
            if record_data.name == 'end_position_lat':
                end_position_lat = record_data.value           
            if record_data.name == 'end_position_long':
                end_position_long = record_data.value
            if record_data.name == 'enhanced_avg_speed':
                enhanced_avg_speed = record_data.value
            if record_data.name == 'enhanced_max_speed':
                enhanced_max_speed = record_data.value
            if record_data.name == 'event':
                event = record_data.value
            if record_data.name == 'event_group':
                event_group = record_data.value
            if record_data.name == 'event_type':
                event_type = record_data.value
            if record_data.name == 'intensity':
                intensity = record_data.value
            if record_data.name == 'lap_trigger':
                lap_trigger = record_data.value
            if record_data.name == 'left_right_balance':
                left_right_balance = record_data.value
            if record_data.name == 'max_cadence':
                max_cadence = record_data.value
            if record_data.name == 'max_cadence_position':
                max_cadence_position = record_data.value    
            if record_data.name == 'max_heart_rate':
                max_heart_rate = record_data.value        
            if record_data.name == 'max_power':
                max_power = record_data.value 
            if record_data.name == 'max_power_position':
                max_power_position = record_data.value     
            if record_data.name == 'max_speed':
                max_speed = record_data.value 
            if record_data.name == 'message_index':
                message_index = record_data.value  
            if record_data.name == 'normalized_power':
                normalized_power = record_data.value 
            if record_data.name == 'sport':
                sport = record_data.value   
            if record_data.name == 'stand_count':
                stand_count = record_data.value 
            if record_data.name == 'start_position_lat':
                start_position_lat = record_data.value   
            if record_data.name == 'start_position_long':
                start_position_long = record_data.value 
            if record_data.name == 'start_time':
                start_time = record_data.value
            if record_data.name == 'time_standing':
                time_standing = record_data.value 
            if record_data.name == 'timestamp':
                timestamp = record_data.value 
            if record_data.name == 'total_ascent':
                total_ascent = record_data.value
            if record_data.name == 'total_calories':
                total_calories = record_data.value
            if record_data.name == 'total_cycles':
                total_cycles = record_data.value
            if record_data.name == 'total_descent':
                total_descent = record_data.value
            if record_data.name == 'total_distance':
                total_distance = record_data.value
            if record_data.name == 'total_elapsed_time':
                total_elapsed_time = record_data.value 
            if record_data.name == 'total_fat_calories':
                total_fat_calories = record_data.value
            if record_data.name == 'total_timer_time':
                total_timer_time = record_data.value 
            if record_data.name == 'total_work':
                total_work = record_data.value   

        sql = """

            INSERT INTO garmin_connect_original_lap (avg_cadence,avg_cadence_position,avg_combined_pedal_smoothness,avg_heart_rate,avg_left_pco,avg_left_pedal_smoothness,avg_left_power_phase,
            avg_left_power_phase_peak,avg_left_torque_effectiveness,avg_power,avg_power_position,avg_right_pco,avg_right_pedal_smoothness,avg_right_power_phase,avg_right_power_phase_peak,
            avg_right_torque_effectiveness,avg_speed,end_position_lat,end_position_long,enhanced_avg_speed,enhanced_max_speed,event,event_group,event_type,intensity,lap_trigger,left_right_balance,
            max_cadence,max_cadence_position,max_heart_rate,max_power,max_power_position,max_speed,message_index,normalized_power,sport,stand_count,start_position_lat,start_position_long,
            start_time,time_standing,timestamp,total_ascent,total_calories,total_cycles,total_descent,total_distance,total_elapsed_time,total_fat_calories,total_timer_time,total_work,gc_activity_id)

            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

            ON CONFLICT (timestamp,gc_activity_id) DO NOTHING;
            """

        try:
            
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            with StdoutRedirection(username):
                print(('Inserting lap from session: ' + str(gc_activity_id) + ' with timestamp:' + str(timestamp)))
            with ProgressStdoutRedirection(username):
                print(('Inserting lap from session: ' + str(gc_activity_id) + ' with timestamp:' + str(timestamp)))
            cur.execute(sql,(avg_cadence,list(avg_cadence_position),avg_combined_pedal_smoothness,avg_heart_rate,avg_left_pco,avg_left_pedal_smoothness,list(avg_left_power_phase),
                                list(avg_left_power_phase_peak),avg_left_torque_effectiveness,avg_power,list(avg_power_position),avg_right_pco,avg_right_pedal_smoothness,list(avg_right_power_phase),list(avg_right_power_phase_peak),
                                avg_right_torque_effectiveness,avg_speed,end_position_lat,end_position_long,enhanced_avg_speed,enhanced_max_speed,event,event_group,event_type,intensity,lap_trigger,left_right_balance,
                                max_cadence,list(max_cadence_position),max_heart_rate,max_power,list(max_power_position),max_speed,message_index,normalized_power,sport,stand_count,start_position_lat,start_position_long,
                                start_time,time_standing,timestamp,total_ascent,total_calories,total_cycles,total_descent,total_distance,total_elapsed_time,total_fat_calories,total_timer_time,total_work,gc_activity_id))
            conn.commit()       
            # close the communication with the PostgreSQL
            cur.close()
        except Exception as e:
            with ErrorStdoutRedirection(username):
                print(e)

     # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()  
                
    with StdoutRedirection(username):
        print(('--- All lap data for session: ' + str(gc_activity_id) + ' inserted successfully. ---'))
    with ProgressStdoutRedirection(username):
        print(('--- All lap data for session: ' + str(gc_activity_id) + ' inserted successfully. ---'))


