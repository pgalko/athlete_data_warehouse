import psycopg2
from database_ini_parser import config
from fitparse import FitFile
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
from processify import processify
import os
from tzwhere import tzwhere
import datetime
import pytz

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_original_session_insert(file_path,activity_id,athlete, db_host,db_name,superuser_un,superuser_pw,encr_pass):
    file2import = (file_path)
    gc_activity_id = (activity_id)
    athlete_id = (athlete)
    db_name = (db_name)
    avg_cadence,avg_combined_pedal_smoothness,avg_heart_rate,avg_left_pco,avg_left_pedal_smoothness,avg_left_torque_effectiveness,avg_power,avg_right_pco,avg_right_pedal_smoothness,avg_right_torque_effectiveness,avg_speed,enhanced_avg_speed,enhanced_max_speed,event,event_group,event_type, first_lap_index,intensity_factor,left_right_balance,max_cadence, max_heart_rate,max_power,max_speed,message_index,nec_lat,nec_long,normalized_power,num_laps,sport,stand_count,start_position_lat,start_position_long,start_time,sub_sport,swc_lat,swc_long,threshold_power,time_standing,timestamp,total_ascent,total_calories,total_cycles,total_descent,total_distance,total_elapsed_time,total_fat_calories,total_timer_time,total_work,training_stress_score,trigger = [None]*50
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
    pidfile = PID_FILE_DIR + athlete + '_PID.txt'
    open(pidfile, 'w').write(pid)

    conn = None
         
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

    tz = tzwhere.tzwhere()

    # Get all data messages that are of type record
    for record in fitfile.get_messages('session'):
        # Go through all the data entries in this record
        for record_data in record:
            if record_data.name is 'avg_cadence':
                avg_cadence = record_data.value
            if record_data.name is 'avg_cadence_position':
                avg_cadence_position = record_data.value
            if record_data.name is 'avg_combined_pedal_smoothness':
                avg_combined_pedal_smoothness = record_data.value
            if record_data.name is 'avg_heart_rate':
                avg_heart_rate = record_data.value
            if record_data.name is 'avg_left_pco':
                avg_left_pco = record_data.value
            if record_data.name is 'avg_left_pedal_smoothness':
                avg_left_pedal_smoothness = record_data.value
            if record_data.name is 'avg_left_power_phase':
                avg_left_power_phase = record_data.value
            if record_data.name is 'avg_left_power_phase_peak':
                avg_left_power_phase_peak = record_data.value
            if record_data.name is 'avg_left_torque_effectiveness':
                avg_left_torque_effectiveness = record_data.value
            if record_data.name is 'avg_power':
                avg_power = record_data.value
            if record_data.name is 'avg_power_position':
                avg_power_position = record_data.value
            if record_data.name is 'avg_right_pco':
                avg_right_pco = record_data.value
            if record_data.name is 'avg_right_pedal_smoothness':
                avg_right_pedal_smoothness = record_data.value
            if record_data.name is 'avg_right_power_phase':
                avg_right_power_phase = record_data.value
            if record_data.name is 'avg_right_power_phase_peak':
                avg_right_power_phase_peak = record_data.value
            if record_data.name is 'avg_right_torque_effectiveness':
                avg_right_torque_effectiveness = record_data.value
            if record_data.name is 'avg_speed':
                avg_speed = record_data.value
            if record_data.name is 'enhanced_avg_speed':
                enhanced_avg_speed = record_data.value
            if record_data.name is 'enhanced_max_speed':
                enhanced_max_speed = record_data.value
            if record_data.name is 'event':
                event = record_data.value
            if record_data.name is 'event_group':
                event_group = record_data.value
            if record_data.name is 'event_type':
                event_type = record_data.value
            if record_data.name is 'first_lap_index':
                first_lap_index = record_data.value
            if record_data.name is 'intensity_factor':
                intensity_factor = record_data.value
            if record_data.name is 'left_right_balance':
                left_right_balance = record_data.value
            if record_data.name is 'max_cadence':
                max_cadence = record_data.value
            if record_data.name is 'max_cadence_position':
                max_cadence_position = record_data.value    
            if record_data.name is 'max_heart_rate':
                max_heart_rate = record_data.value        
            if record_data.name is 'max_power':
                max_power = record_data.value 
            if record_data.name is 'max_power_position':
                max_power_position = record_data.value 
            if record_data.name is 'max_speed':
                max_speed = record_data.value 
            if record_data.name is 'message_index':
                message_index = record_data.value
            if record_data.name is 'nec_lat':
                nec_lat = record_data.value 
            if record_data.name is 'nec_long':
                nec_long = record_data.value   
            if record_data.name is 'normalized_power':
                normalized_power = record_data.value
            if record_data.name is 'num_laps':
                num_laps = record_data.value 
            if record_data.name is 'sport':
                sport = record_data.value
            if record_data.name is 'stand_count':
                stand_count = record_data.value 
            if record_data.name is 'start_position_lat':
                start_position_lat = record_data.value   
                if start_position_lat is not None:
                    #Convert semicircles to degrees
                    start_position_lat_degr = start_position_lat*(180./(2**31))
                else: 
                    start_position_lat_degr = None  
            if record_data.name is 'start_position_long':
                start_position_long = record_data.value
                if start_position_long is not None:
                    #Convert semicircles to degrees
                    start_position_long_degr = start_position_long*(180./(2**31))
                else: 
                    start_position_long_degr = None
            if record_data.name is 'sub_sport':
                sub_sport = record_data.value
            if record_data.name is 'swc_lat':
                swc_lat = record_data.value
            if record_data.name is 'swc_long':
                swc_long = record_data.value
            if record_data.name is 'threshold_power':
                threshold_power = record_data.value
            if record_data.name is 'time_standing':
                time_standing = record_data.value
            if record_data.name is 'timestamp':
                timestamp = record_data.value
            if record_data.name is 'total_ascent':
                total_ascent = record_data.value
            if record_data.name is 'total_calories':
                total_calories = record_data.value
            if record_data.name is 'total_cycles':
                total_cycles = record_data.value
            if record_data.name is 'total_descent':
                total_descent = record_data.value
            if record_data.name is 'total_distance':
                total_distance = record_data.value
            if record_data.name is 'total_elapsed_time':
                total_elapsed_time = record_data.value 
            if record_data.name is 'total_fat_calories':
                total_fat_calories = record_data.value
            if record_data.name is 'total_timer_time':
                total_timer_time = record_data.value 
            if record_data.name is 'total_work':
                total_work = record_data.value   
            if record_data.name is 'training_stress_score':
                training_stress_score = record_data.value 
            if record_data.name is 'trigger':
                trigger = record_data.value 

        try:
            #Get timezone from lat/long
            timezone = None
            local_time_str = None
            if start_position_lat_degr is not None and start_position_long_degr is not None:
                timezone = tz.tzNameAt(start_position_lat_degr,start_position_long_degr)
                local_tz = pytz.timezone(timezone)

                #Get local time from timestamp(gmt)
                gmt_time_dt = datetime.datetime.strptime((str(timestamp)), "%Y-%m-%d %H:%M:%S")      
                local_dt = gmt_time_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
                local_dt_norm = local_tz.normalize(local_dt)
                local_time_str = datetime.datetime.strftime((local_dt_norm), "%Y-%m-%d %H:%M:%S") 
        except Exception as e:
            with ErrorStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + '  ' + str(e)))
            pass

        sql = """

            INSERT INTO garmin_connect_original_session (avg_cadence,avg_cadence_position,avg_combined_pedal_smoothness,avg_heart_rate,avg_left_pco,
            avg_left_pedal_smoothness,avg_left_power_phase,avg_left_power_phase_peak,avg_left_torque_effectiveness,avg_power,avg_power_position,avg_right_pco,
            avg_right_pedal_smoothness,avg_right_power_phase,avg_right_power_phase_peak,avg_right_torque_effectiveness,avg_speed,enhanced_avg_speed,
            enhanced_max_speed,event,event_group,event_type, first_lap_index,intensity_factor,left_right_balance,max_cadence,max_cadence_position, max_heart_rate,
            max_power,max_power_position,max_speed,message_index,nec_lat,nec_long,normalized_power,num_laps,sport,stand_count,start_position_lat,
            start_position_long,start_time,sub_sport,swc_lat,swc_long,threshold_power,time_standing,timestamp,total_ascent,total_calories,total_cycles,
            total_descent,total_distance,total_elapsed_time,total_fat_calories,total_timer_time,total_work,training_stress_score,trigger,gc_activity_id,athlete_id)

            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,(select id from athlete where gc_email=%s))

            ON CONFLICT (gc_activity_id) DO NOTHING;
            """
                
        sql_timezone = """
            INSERT INTO timezones(gc_activity_id,timestamp_local,timestamp_gmt,timezone)
            
            VALUES
            (%s,%s,%s,%s)

            ON CONFLICT (gc_activity_id,timestamp_gmt) DO NOTHING;
            """
        try:
            #Insert session data into garmin_connect_original_session table
            cur = conn.cursor()
            # execute a statement
            with StdoutRedirection(athlete):
                print(('Inserting session: ' + str(gc_activity_id) + ' with timestamp:' + str(timestamp)))
            with ProgressStdoutRedirection(athlete):
                print(('Inserting session: ' + str(gc_activity_id) + ' with timestamp:' + str(timestamp)))
            
            cur.execute(sql,(avg_cadence,list(avg_cadence_position),avg_combined_pedal_smoothness,avg_heart_rate,avg_left_pco,
                                avg_left_pedal_smoothness,list(avg_left_power_phase),list(avg_left_power_phase_peak),avg_left_torque_effectiveness,avg_power,list(avg_power_position),avg_right_pco,
                                avg_right_pedal_smoothness,list(avg_right_power_phase),list(avg_right_power_phase_peak),avg_right_torque_effectiveness,avg_speed,enhanced_avg_speed,
                                enhanced_max_speed,event,event_group,event_type, first_lap_index,intensity_factor,left_right_balance,max_cadence,list(max_cadence_position), max_heart_rate,
                                max_power,list(max_power_position),max_speed,message_index,nec_lat,nec_long,normalized_power,num_laps,sport,stand_count,start_position_lat,
                                start_position_long,start_time,sub_sport,swc_lat,swc_long,threshold_power,time_standing,timestamp,total_ascent,total_calories,total_cycles,
                                total_descent,total_distance,total_elapsed_time,total_fat_calories,total_timer_time,total_work,training_stress_score,trigger,gc_activity_id,athlete_id))
            conn.commit()
            # close the communication with the PostgreSQL
            cur.close()

            #Insert timezone and local time into timezones table
            cur = conn.cursor()
            # execute a statement
            with StdoutRedirection(athlete):
                print(('Inserting timezone info: ' + str(timezone) + ' and local tz timestamp:' + str(local_time_str)))
            with ProgressStdoutRedirection(athlete):
                print(('Inserting timezone info: ' + str(timezone) + ' and local tz timestamp:' + str(local_time_str)))
            cur.execute(sql_timezone,(gc_activity_id,local_time_str,timestamp,timezone))
            conn.commit()
            # close the communication with the PostgreSQL
            cur.close()       
        except Exception as e:
            with ErrorStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + '  ' + str(e)))
                        
    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close() 
                
    with StdoutRedirection(athlete):
        print(('--- All summary data for session: ' + str(gc_activity_id) + ' inserted successfully. ---'))
    with ProgressStdoutRedirection(athlete):
        print(('--- All summary data for session: ' + str(gc_activity_id) + ' inserted successfully. ---'))


