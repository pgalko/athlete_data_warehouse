import psycopg2
from database_ini_parser import config
from fitparse import FitFile
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
from processify import processify
import os
from tzwhere import tzwhere
import datetime
import pytz
from numpy import mean
from meteostat import Stations

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
    enhanced_altitude = []

    start_position_lat_degr = None
    start_position_long_degr = None
    end_time_gmt_str = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + athlete + '_PID.txt'
    open(pidfile, 'w').write(pid)

    conn = None
         
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

    tz = tzwhere.tzwhere()

    # Get all data messages that are of type record
    try:
        for record in fitfile.get_messages('record'):
        # Go through all the data entries in this record
            for record_data in record:
                # Append altitude values to list
                if record_data.name == 'enhanced_altitude':
                    enhanced_altitude.append(record_data.value)
        #Calculate avereage altitude for a better weather data accuracy
        avg_altitude = int(mean(enhanced_altitude))
        fitfile.close
    except:
        avg_altitude = None
    
    fitfile = FitFile(file2import)
    # Get all data messages that are of type session
    for record in fitfile.get_messages('session'):
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
            if record_data.name == 'first_lap_index':
                first_lap_index = record_data.value
            if record_data.name == 'intensity_factor':
                intensity_factor = record_data.value
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
            if record_data.name == 'nec_lat':
                nec_lat = record_data.value 
            if record_data.name == 'nec_long':
                nec_long = record_data.value   
            if record_data.name == 'normalized_power':
                normalized_power = record_data.value
            if record_data.name == 'num_laps':
                num_laps = record_data.value 
            if record_data.name == 'sport':
                sport = record_data.value
            if record_data.name == 'stand_count':
                stand_count = record_data.value 
            if record_data.name == 'start_position_lat':
                start_position_lat = record_data.value   
                if start_position_lat is not None:
                    #Convert semicircles to degrees
                    start_position_lat_degr = start_position_lat*(180./(2**31))
                else: 
                    start_position_lat_degr = None  
            if record_data.name == 'start_position_long':
                start_position_long = record_data.value
                if start_position_long is not None:
                    #Convert semicircles to degrees
                    start_position_long_degr = start_position_long*(180./(2**31))
                else: 
                    start_position_long_degr = None
            if record_data.name == 'sub_sport':
                sub_sport = record_data.value
            if record_data.name == 'swc_lat':
                swc_lat = record_data.value
            if record_data.name == 'swc_long':
                swc_long = record_data.value
            if record_data.name == 'threshold_power':
                threshold_power = record_data.value
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
            if record_data.name == 'training_stress_score':
                training_stress_score = record_data.value 
            if record_data.name == 'trigger':
                trigger = record_data.value 

        try:
            #Get timezone from lat/long
            timezone = None
            local_time_str = None
            if start_position_lat_degr is not None and start_position_long_degr is not None:
                timezone = tz.tzNameAt(start_position_lat_degr,start_position_long_degr)
                local_tz = pytz.timezone(timezone)

                gmt_time_dt = datetime.datetime.strptime((str(timestamp)), "%Y-%m-%d %H:%M:%S")      
                #Calculate activity_end time 
                activity_duration_dt =  datetime.timedelta(0,int(total_elapsed_time))
                end_time_gmt_dt = gmt_time_dt + activity_duration_dt 
                end_time_gmt_str = datetime.datetime.strftime((end_time_gmt_dt), "%Y-%m-%d %H:%M:%S")
                
                #Get local time from timestamp(gmt)
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
            INSERT INTO timezones(gc_activity_id,timestamp_local,timestamp_gmt,timezone,long_degr,lat_degr,alt_avrg,end_time_gmt)
            
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s)

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

            if timezone is not None:
                #Insert timezone and local time into timezones table
                cur = conn.cursor()
                # execute a statement
                with StdoutRedirection(athlete):
                    print(('Inserting timezone info: ' + str(timezone) + ' and local tz timestamp:' + str(local_time_str)))
                with ProgressStdoutRedirection(athlete):
                    print(('Inserting timezone info: ' + str(timezone) + ' and local tz timestamp:' + str(local_time_str)))
                cur.execute(sql_timezone,(gc_activity_id,local_time_str,timestamp,timezone,start_position_long_degr,start_position_lat_degr,avg_altitude,end_time_gmt_str))
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


