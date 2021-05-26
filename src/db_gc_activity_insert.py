#!/usr/bin/python

####
# Not currently used. Uses PostgreSQL's pg_read_file and xpath to parse the data from the export xml file.
####

import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os
import datetime

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_activity_insert(file_path,athlete,activity,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    """ Connect to the PostgreSQL database server """
    file2import = (file_path, )
    athlete_id = (athlete, )
    activity_id = (activity, )
    db_name = db_name
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + athlete + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """DO
      $do$
      BEGIN
      IF

      (SELECT
      count(xpath('//*[local-name()="Lap"]/@StartTime', x))::text::int
      FROM unnest(xpath('//*[local-name()="Lap"]', pg_read_file(%s)::xml)) x) = 1

      THEN

      INSERT INTO garmin_connect_activity (activity_timestamp,sport,athlete_id,gc_activity_id)
      SELECT
            (xpath('//*[local-name()="Activity"]/*[local-name()="Id"]/text()', x))[1]::text::text AS activity_timestamp,
            (xpath('//*[local-name()="Activity"]/@Sport', x))[1]::text::text AS sport,
            (select id from athlete where gc_email=%s),
            %s
      FROM UNNEST 
            (xpath('//*[local-name()="Activity"]',pg_read_file(%s)::xml)) x;



      INSERT INTO garmin_connect_lap (gc_activity_id,lap_id,activity_timestamp,total_time_seconds,distance_meters,maximum_speed,calories,average_hr_bpm,maximum_hr_bpm,intensity,cadence,trigger_method,
                                    extensions_ns3_lx_avgspeed,extensions_ns3_lx_maxbikecadence,extensions_ns3_lx_steps,extensions_ns3_lx_avgwatts,extensions_ns3_lx_maxwatts,extensions_ns3_lx_avgruncadence,
                                    extensions_ns3_lx_maxruncadence)

      SELECT
      %s,
      unnest (xpath('//*[local-name()="Lap"]/@StartTime', x))::text::text AS lap_id,
            (xpath('//*[local-name()="Activity"]/*[local-name()="Id"]/text()', x))[1]::text::text AS activity_timestamp,  
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="TotalTimeSeconds"]/text()', x))::text::numeric AS total_time_seconds,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="DistanceMeters"]/text()', x))::text::numeric AS distance_meters,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="MaximumSpeed"]/text()', x))::text::numeric AS maximum_speed,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Calories"]/text()', x))::text::numeric AS calories,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="AverageHeartRateBpm"]/*[local-name()="Value"]/text()', x))::text::integer AS average_hr_bpm,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="MaximumHeartRateBpm"]/*[local-name()="Value"]/text()', x))::text::integer AS maximum_hr_bpm,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Intensity"]/text()', x))::text::text AS intensity,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Cadence"]/text()', x))::text::integer AS cadence,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="TriggerMethod"]/text()', x))::text::text AS trigger_method,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="AvgSpeed"]/text()', x))::text::numeric AS extensions_ns3_lx_avgspeed,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="MaxBikeCadence"]/text()', x))::text::integer AS extensions_ns3_lx_maxbikecadence,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="Steps"]/text()', x))::text::integer AS extensions_ns3_lx_steps,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="AvgWatts"]/text()', x))::text::integer AS extensions_ns3_lx_avgwatts,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="MaxWatts"]/text()', x))::text::integer AS extensions_ns3_lx_maxwatts,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="AvgRunCadence"]/text()', x))::text::integer AS extensions_ns3_lx_avgruncadence,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="MaxRunCadence"]/text()', x))::text::integer AS extensions_ns3_lx_maxruncadence
      FROM UNNEST (xpath('//*[local-name()="Activity"]', pg_read_file(%s)::xml)) x;

      INSERT INTO garmin_connect_trackpoint (trackpoint_time, lap_id, position_latitude_degrees, position_longitude_degrees,altitude_meters,distance_meters,hr_bpm,extensions_ns3_tpx_speed,extensions_ns3_tpx_watts,extensions_ns3_tpx_runcadence)

      SELECT
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="Time"]/text()', x))::text::text AS trackpoint_time,
      (select unnest (xpath('//*[local-name()="Lap"]/@StartTime', x))::text::text AS lap_id
      from unnest(xpath('//*[local-name()="Lap"]', pg_read_file(%s)::xml)) x),
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="Position"]/*[local-name()="LatitudeDegrees"]/text()', x))::text::numeric AS position_latitude_degrees,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="Position"]/*[local-name()="LongitudeDegrees"]/text()', x))::text::numeric AS position_longitude_degrees,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="AltitudeMeters"]/text()', x))::text::numeric AS altitude_meters,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="DistanceMeters"]/text()', x))::text::numeric AS distance_meters,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="HeartRateBpm"]/*[local-name()="Value"]/text()', x))::text::integer AS hr_bpm,
      unnest(xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/*[local-name()="Extensions"]
            /*[local-name()="TPX"]/*[local-name()="Speed"]/text()', x))::text::numeric AS extensions_ns3_tpx_speed,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/*[local-name()="Extensions"]
            /*[local-name()="TPX"]/*[local-name()="Watts"]/text()', x))::text::integer AS extensions_ns3_tpx_watts,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/*[local-name()="Extensions"]
            /*[local-name()="TPX"]/*[local-name()="RunCadence"]/text()', x))::text::integer AS extensions_ns3_tpx_runcadence

      FROM unnest(xpath('//*[local-name()="Lap"]', pg_read_file(%s)::xml)) x;

      ELSE

      INSERT INTO garmin_connect_activity (activity_timestamp,sport,athlete_id,gc_activity_id)
      SELECT
            (xpath('//*[local-name()="Activity"]/*[local-name()="Id"]/text()', x))[1]::text::text AS activity_timestamp,
            (xpath('//*[local-name()="Activity"]/@Sport', x))[1]::text::text AS sport,(select id from athlete where gc_email=%s),
            %s
      FROM UNNEST (xpath('//*[local-name()="Activity"]',pg_read_file(%s)::xml)) x;


      INSERT INTO garmin_connect_lap (gc_activity_id,lap_id,activity_timestamp,total_time_seconds,distance_meters,maximum_speed,calories,average_hr_bpm,maximum_hr_bpm,intensity,cadence,trigger_method,
                                    extensions_ns3_lx_avgspeed,extensions_ns3_lx_maxbikecadence,extensions_ns3_lx_steps,extensions_ns3_lx_avgwatts,extensions_ns3_lx_maxwatts,extensions_ns3_lx_avgruncadence,
                                    extensions_ns3_lx_maxruncadence)

      SELECT
      %s,
      unnest (xpath('//*[local-name()="Lap"]/@StartTime', x))::text::text AS lap_id,
            (xpath('//*[local-name()="Activity"]/*[local-name()="Id"]/text()', x))[1]::text::text AS activity_timestamp,  
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="TotalTimeSeconds"]/text()', x))::text::numeric AS total_time_seconds,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="DistanceMeters"]/text()', x))::text::numeric AS distance_meters,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="MaximumSpeed"]/text()', x))::text::numeric AS maximum_speed,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Calories"]/text()', x))::text::numeric AS calories,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="AverageHeartRateBpm"]/*[local-name()="Value"]/text()', x))::text::integer AS average_hr_bpm,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="MaximumHeartRateBpm"]/*[local-name()="Value"]/text()', x))::text::integer AS maximum_hr_bpm,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Intensity"]/text()', x))::text::text AS intensity,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Cadence"]/text()', x))::text::integer AS cadence,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="TriggerMethod"]/text()', x))::text::text AS trigger_method,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="AvgSpeed"]/text()', x))::text::numeric AS extensions_ns3_lx_avgspeed,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="MaxBikeCadence"]/text()', x))::text::integer AS extensions_ns3_lx_maxbikecadence,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="Steps"]/text()', x))::text::integer AS extensions_ns3_lx_steps,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="AvgWatts"]/text()', x))::text::integer AS extensions_ns3_lx_avgwatts,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="MaxWatts"]/text()', x))::text::integer AS extensions_ns3_lx_maxwatts,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="AvgRunCadence"]/text()', x))::text::integer AS extensions_ns3_lx_avgruncadence,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Extensions"]/*[local-name()="LX"]/*[local-name()="MaxRunCadence"]/text()', x))::text::integer AS extensions_ns3_lx_maxruncadence
      FROM UNNEST (xpath('//*[local-name()="Activity"]', pg_read_file(%s)::xml)) x;

      INSERT INTO garmin_connect_trackpoint (trackpoint_time, lap_id, position_latitude_degrees, position_longitude_degrees,altitude_meters,distance_meters,hr_bpm,extensions_ns3_tpx_speed,extensions_ns3_tpx_watts,extensions_ns3_tpx_runcadence)

      SELECT
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="Time"]/text()', x))::text::text AS trackpoint_time,
            (xpath('//*[local-name()="Lap"]/@StartTime', x))[1]::text::text AS lap_id,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="Position"]/*[local-name()="LatitudeDegrees"]/text()', x))::text::numeric AS position_latitude_degrees,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="Position"]/*[local-name()="LongitudeDegrees"]/text()', x))::text::numeric AS position_longitude_degrees,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="AltitudeMeters"]/text()', x))::text::numeric AS altitude_meters,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="DistanceMeters"]/text()', x))::text::numeric AS distance_meters,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/
            *[local-name()="HeartRateBpm"]/*[local-name()="Value"]/text()', x))::text::integer AS hr_bpm,
      unnest(xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/*[local-name()="Extensions"]
            /*[local-name()="TPX"]/*[local-name()="Speed"]/text()', x))::text::numeric AS extensions_ns3_tpx_speed,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/*[local-name()="Extensions"]
            /*[local-name()="TPX"]/*[local-name()="Watts"]/text()', x))::text::integer AS extensions_ns3_tpx_watts,
      unnest (xpath('//*[local-name()="Lap"]/*[local-name()="Track"]/*[local-name()="Trackpoint"]/*[local-name()="Extensions"]
            /*[local-name()="TPX"]/*[local-name()="RunCadence"]/text()', x))::text::integer AS extensions_ns3_tpx_runcadence

      FROM unnest(xpath('//*[local-name()="Lap"]', pg_read_file(%s)::xml)) x;

      END IF;

      END
      $do$
      """


    try:
         
        # connect to the PostgreSQL server
        with ProgressStdoutRedirection(athlete):
            print('Connecting to the PostgreSQL server to insert TCX activity data...')
        try:
            conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)
        except Exception as e:
            with ProgressStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e))) 
        # create a cursor
        try:
            cur = conn.cursor()
        except Exception as e:
            with ErrorStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e))) 

        # execute a statement
        with StdoutRedirection(athlete):
            print('Inserting Activity Data into postgreSQL:')
        with ProgressStdoutRedirection(athlete):
            print('Inserting Activity Data into postgreSQL:')
        cur.execute(sql,(file2import,athlete_id,activity_id,file2import,activity_id,file2import,file2import,file2import,athlete_id,activity_id,file2import,activity_id,file2import,file2import))
        conn.commit()
        
        # close the communication with the PostgreSQL
        cur.close()
    
    except (Exception, psycopg2.IntegrityError) as ex:
        if ex.pgcode == '23505':
            with StdoutRedirection(athlete):
                print('The record for this activity already exists in the database.Skipping...')
            with ErrorStdoutRedirection(athlete):
                print('The record for this activity already exists in the database.Skipping...')
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(athlete):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
    
    finally:
        if conn is not None:
            conn.close()



