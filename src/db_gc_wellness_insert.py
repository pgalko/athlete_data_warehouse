#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import inspect
from processify import processify
import os
import pandas as pd
import numpy as np
from xml.etree.ElementTree import parse

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_wellness_insert(file_path,athlete,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        file2import = (file_path, )
        athlete_id = (athlete, )
        db_name = (db_name)
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + athlete + '_PID.txt'
        open(pidfile, 'w').write(pid)
        
        #List to store values from xml doc
        xml_list=[]

        xml_list.append(athlete)

        #Parse the XML document, and append the data to dictionary
        root = parse(file_path).getroot()
        for startDate in root.iter('statisticsStartDate'):
            date = startDate.text
            xml_list.append(date)
        for category in root.findall('.//metricsMap/*'):
            if category.tag != 'SLEEP_SLEEP_DURATION':
                for tag in root.iter(category.tag):
                    for item in tag.iterfind('item'):
                        xml_list.append(item.findtext('value'))
            else:
                for tag in root.iter(category.tag):
                    for item in tag.iterfind('item'):
                        if item.findtext('calendarDate')==date:
                            xml_list.append(item.findtext('value'))
        
        #Build a list of parameters to pass to sql query
        query_params = xml_list+xml_list
        query_params.append(date)

        # PG Amend path for postgres "pg_read_file()" function.
        text = file_path
        head, sep, tail = text.partition('temp/')
        pg_read_file = (tail, )
        
        list_sql = """
        INSERT INTO garmin_connect_wellness (athlete_id,calendar_date,wellness_min_heart_rate,wellness_total_steps_goal,sleep_duration,wellness_floors_descended,wellness_floors_ascended,wellness_body_battery_drained,wellness_max_heart_rate,wellness_total_distance,
        wellness_vigorous_intensity_minutes,food_calories_consumed,wellness_user_intensity_goal,wellness_common_active_calories,food_calories_remaining,wellness_moderate_intensity_minutes,wellness_bmr_calories,
        common_total_distance,wellness_active_calories,wellness_total_calories,wellness_resting_heart_rate,wellness_max_stress,wellness_average_steps,wellness_max_avg_heart_rate,wellness_abnormalhr_alerts_count,
        wellness_total_steps,wellness_average_stress,common_total_calories,wellness_user_floors_ascended_goal,wellness_min_avg_heart_rate,wellness_bodybattery_charged)
        
        VALUES ((select id from athlete where gc_email=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (calendar_date) DO UPDATE

        SET (athlete_id,calendar_date,wellness_min_heart_rate,wellness_total_steps_goal,sleep_duration,wellness_floors_descended,wellness_floors_ascended,wellness_body_battery_drained,wellness_max_heart_rate,wellness_total_distance,
        wellness_vigorous_intensity_minutes,food_calories_consumed,wellness_user_intensity_goal,wellness_common_active_calories,food_calories_remaining,wellness_moderate_intensity_minutes,wellness_bmr_calories,
        common_total_distance,wellness_active_calories,wellness_total_calories,wellness_resting_heart_rate,wellness_max_stress,wellness_average_steps,wellness_max_avg_heart_rate,wellness_abnormalhr_alerts_count,
        wellness_total_steps,wellness_average_stress,common_total_calories,wellness_user_floors_ascended_goal,wellness_min_avg_heart_rate,wellness_bodybattery_charged)
        =

        ((select id from athlete where gc_email=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        WHERE garmin_connect_wellness.calendar_date
        =
        
        %s;
        """

        xpath_sql = """
 
        INSERT INTO garmin_connect_wellness (food_calories_consumed,wellness_user_intensity_goal,calendar_date,wellness_total_steps,wellness_common_active_calories,wellness_floors_ascended,wellness_max_heart_rate,
        wellness_min_avg_heart_rate,
        wellness_min_heart_rate,wellness_average_stress,wellness_resting_heart_rate,wellness_max_stress,wellness_abnormalhr_alerts_count,wellness_max_avg_heart_rate,wellness_total_steps_goal,
        wellness_user_floors_ascended_goal,
        wellness_moderate_intensity_minutes,wellness_total_calories,wellness_bodybattery_charged,wellness_floors_descended,wellness_bmr_calories,food_calories_remaining,common_total_calories,wellness_body_battery_drained,
        wellness_average_steps,wellness_vigorous_intensity_minutes,wellness_total_distance,common_total_distance,wellness_active_calories,athlete_id)
        
        SELECT

        unnest (xpath('//*[local-name()="FOOD_CALORIES_CONSUMED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS food_calories_consumed,
        unnest (xpath('//*[local-name()="WELLNESS_USER_INTENSITY_MINUTES_GOAL"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_user_intensity_goal,
        unnest (xpath('//*[local-name()="WELLNESS_MIN_HEART_RATE"]/*[local-name()="item"]/*[local-name()="calendarDate"]/text()', x))::text::date AS calendar_date,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_STEPS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_steps,
        unnest (xpath('//*[local-name()="COMMON_ACTIVE_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_common_active_calories,
        unnest (xpath('//*[local-name()="WELLNESS_FLOORS_ASCENDED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_floors_ascended,
        unnest (xpath('//*[local-name()="WELLNESS_MAX_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_max_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_MIN_AVG_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_min_avg_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_MIN_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_min_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_AVERAGE_STRESS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_average_stress,
        unnest (xpath('//*[local-name()="WELLNESS_RESTING_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_resting_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_MAX_STRESS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_max_stress,
        unnest (xpath('//*[local-name()="WELLNESS_ABNORMALHR_ALERTS_COUNT"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_abnormalhr_alerts_count,
        unnest (xpath('//*[local-name()="WELLNESS_MAX_AVG_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_max_avg_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_STEP_GOAL"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_steps_goal,
        unnest (xpath('//*[local-name()="WELLNESS_USER_FLOORS_ASCENDED_GOAL"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_user_floors_ascended_goal,
        unnest (xpath('//*[local-name()="WELLNESS_MODERATE_INTENSITY_MINUTES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_moderate_intensity_minutes,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_calories,
        unnest (xpath('//*[local-name()="WELLNESS_BODYBATTERY_CHARGED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_bodybattery_charged,
        unnest (xpath('//*[local-name()="WELLNESS_FLOORS_DESCENDED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_floors_descended,
        unnest (xpath('//*[local-name()="WELLNESS_BMR_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_bmr_calories,
        unnest (xpath('//*[local-name()="FOOD_CALORIES_REMAINING"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS food_calories_remaining,
        unnest (xpath('//*[local-name()="COMMON_TOTAL_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS common_total_calories,
        unnest (xpath('//*[local-name()="WELLNESS_BODYBATTERY_DRAINED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_body_battery_drained,
        unnest (xpath('//*[local-name()="WELLNESS_AVERAGE_STEPS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_average_steps,
        unnest (xpath('//*[local-name()="WELLNESS_VIGOROUS_INTENSITY_MINUTES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_vigorous_intensity_minutes,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_DISTANCE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_distance,
        unnest (xpath('//*[local-name()="COMMON_TOTAL_DISTANCE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS common_total_distance,
        unnest (xpath('//*[local-name()="WELLNESS_ACTIVE_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_active_calories,
        (select id from athlete where gc_email=%s)
        
        
        FROM UNNEST (xpath('//*[local-name()="metricsMap"]', pg_read_file(%s)::xml)) x

        ON CONFLICT (calendar_date) DO UPDATE
        
        SET (food_calories_consumed, wellness_user_intensity_goal,calendar_date,wellness_total_steps,wellness_common_active_calories,wellness_floors_ascended,wellness_max_heart_rate,
        wellness_min_avg_heart_rate,
        wellness_min_heart_rate,wellness_average_stress,wellness_resting_heart_rate,wellness_max_stress,wellness_abnormalhr_alerts_count,wellness_max_avg_heart_rate,wellness_total_steps_goal,
        wellness_user_floors_ascended_goal,
        wellness_moderate_intensity_minutes,wellness_total_calories,wellness_bodybattery_charged,wellness_floors_descended,wellness_bmr_calories,food_calories_remaining,common_total_calories,wellness_body_battery_drained,
        wellness_average_steps,wellness_vigorous_intensity_minutes,wellness_total_distance,common_total_distance,wellness_active_calories,athlete_id)
        
        =
        
        (SELECT

        unnest (xpath('//*[local-name()="FOOD_CALORIES_CONSUMED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS food_calories_consumed,
        unnest (xpath('//*[local-name()="WELLNESS_USER_INTENSITY_MINUTES_GOAL"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_user_intensity_goal,
        unnest (xpath('//*[local-name()="WELLNESS_MIN_HEART_RATE"]/*[local-name()="item"]/*[local-name()="calendarDate"]/text()', x))::text::date AS calendar_date,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_STEPS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_steps,
        unnest (xpath('//*[local-name()="COMMON_ACTIVE_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_common_active_calories,
        unnest (xpath('//*[local-name()="WELLNESS_FLOORS_ASCENDED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_floors_ascended,
        unnest (xpath('//*[local-name()="WELLNESS_MAX_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_max_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_MIN_AVG_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_min_avg_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_MIN_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_min_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_AVERAGE_STRESS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_average_stress,
        unnest (xpath('//*[local-name()="WELLNESS_RESTING_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_resting_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_MAX_STRESS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_max_stress,
        unnest (xpath('//*[local-name()="WELLNESS_ABNORMALHR_ALERTS_COUNT"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_abnormalhr_alerts_count,
        unnest (xpath('//*[local-name()="WELLNESS_MAX_AVG_HEART_RATE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_max_avg_heart_rate,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_STEP_GOAL"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_steps_goal,
        unnest (xpath('//*[local-name()="WELLNESS_USER_FLOORS_ASCENDED_GOAL"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_user_floors_ascended_goal,
        unnest (xpath('//*[local-name()="WELLNESS_MODERATE_INTENSITY_MINUTES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_moderate_intensity_minutes,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_calories,
        unnest (xpath('//*[local-name()="WELLNESS_BODYBATTERY_CHARGED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_bodybattery_charged,
        unnest (xpath('//*[local-name()="WELLNESS_FLOORS_DESCENDED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_floors_descended,
        unnest (xpath('//*[local-name()="WELLNESS_BMR_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_bmr_calories,
        unnest (xpath('//*[local-name()="FOOD_CALORIES_REMAINING"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS food_calories_remaining,
        unnest (xpath('//*[local-name()="COMMON_TOTAL_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS common_total_calories,
        unnest (xpath('//*[local-name()="WELLNESS_BODYBATTERY_DRAINED"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_body_battery_drained,
        unnest (xpath('//*[local-name()="WELLNESS_AVERAGE_STEPS"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_average_steps,
        unnest (xpath('//*[local-name()="WELLNESS_VIGOROUS_INTENSITY_MINUTES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_vigorous_intensity_minutes,
        unnest (xpath('//*[local-name()="WELLNESS_TOTAL_DISTANCE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_total_distance,
        unnest (xpath('//*[local-name()="COMMON_TOTAL_DISTANCE"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS common_total_distance,
        unnest (xpath('//*[local-name()="WELLNESS_ACTIVE_CALORIES"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))::text::real AS wellness_active_calories,
        (select id from athlete where gc_email=%s)
            
        FROM UNNEST (xpath('//*[local-name()="metricsMap"]', pg_read_file(%s)::xml)) x)

        WHERE garmin_connect_wellness.calendar_date
        = 
        (SELECT

        unnest (xpath('//*[local-name()="WELLNESS_MIN_HEART_RATE"]/*[local-name()="item"]/*[local-name()="calendarDate"]/text()', x))::text::date AS calendar_date
        
        FROM UNNEST (xpath('//*[local-name()="metricsMap"]', pg_read_file(%s)::xml)) x);


        CREATE TEMPORARY TABLE temp_garmin_connect_sleep( duration real, calendar_date date) ON COMMIT DROP;

        INSERT INTO temp_garmin_connect_sleep (calendar_date, duration)

        SELECT
        
        unnest (xpath('//*[local-name()="SLEEP_SLEEP_DURATION"]/*[local-name()="item"]/*[local-name()="calendarDate"]/text()', x))
                    ::text::date AS calendar_date,
        unnest (xpath('//*[local-name()="SLEEP_SLEEP_DURATION"]/*[local-name()="item"]/*[local-name()="value"]/text()', x))
                    ::text::real AS duration
                    
        FROM UNNEST (xpath('//*[local-name()="metricsMap"]', pg_read_file(%s)::xml)) x;

        UPDATE garmin_connect_wellness
        SET sleep_duration = temp_garmin_connect_sleep.duration
        FROM temp_garmin_connect_sleep
        WHERE temp_garmin_connect_sleep.calendar_date = garmin_connect_wellness.calendar_date;
        
        """

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

# execute a statement
                with StdoutRedirection(athlete):
                    print('Inserting Wellness Data into postgreSQL:')
                with ProgressStdoutRedirection(athlete):
                    print('Inserting Wellness Data into postgreSQL:')
                #cur.execute(xpath_sql,(athlete_id,pg_read_file,athlete_id,file2import,file2import,file2import))
                cur.execute(list_sql,(query_params))
                conn.commit()
                
                        # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(athlete_id):
                print(error)
        finally:
                if conn is not None:
                        conn.close()
                        with StdoutRedirection(athlete):
                            print('Wellness Data Inserted Successfully')
                        with ProgressStdoutRedirection(athlete):
                            print('Wellness Data Inserted Successfully')


