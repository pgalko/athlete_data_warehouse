#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os
import pandas as pd
import numpy as np
from xml.etree.ElementTree import parse
import datetime

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_wellness_insert(file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        db_name = (db_name)
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
        open(pidfile, 'w').write(pid)

        #Create empty dataframe using sorted db fields as headers. This will be converted to empty dataframe and merged with xml dataframe
        db_fields_list = {'athlete_id','calendar_date','wellness_min_heart_rate','wellness_total_steps_goal','sleep_sleep_duration','wellness_floors_descended','wellness_floors_ascended','wellness_bodybattery_drained','wellness_max_heart_rate','wellness_total_distance',
        'wellness_vigorous_intensity_minutes','food_calories_consumed','wellness_user_intensity_minutes_goal','wellness_common_active_calories','food_calories_remaining','wellness_moderate_intensity_minutes','wellness_bmr_calories',
        'common_total_distance','wellness_active_calories','wellness_total_calories','wellness_resting_heart_rate','wellness_max_stress','wellness_average_steps','wellness_max_avg_heart_rate','wellness_abnormalhr_alerts_count',
        'wellness_total_steps','wellness_average_stress','common_total_calories','wellness_user_floors_ascended_goal','wellness_min_avg_heart_rate','wellness_bodybattery_charged'}   
        #Sort alphabeticaly
        db_fields_list = sorted(db_fields_list)
        db_df = pd.DataFrame(columns=db_fields_list)

        #List to store XML tags for xml_df column names
        column_list=[]
        #List to store XML values in xml_df dataframe and used as params for SQL insert/update query
        xml_list=[]

        xml_list.append(ath_un)
        column_list.append('athlete_id')

        #Parse the XML document, and append the data to column_list and xml_list lists.
        root = parse(file_path).getroot()
        for startDate in root.iter('statisticsStartDate'):
            date = startDate.text
            xml_list.append(date)
            column_list.append('calendar_date')
        for category in root.findall('.//metricsMap/*'):
            if category.tag != 'SLEEP_SLEEP_DURATION':
                column_list.append(category.tag.lower())
                for tag in root.iter(category.tag):
                    for item in tag.iterfind('item'):
                        xml_list.append(item.findtext('value'))
            else:
                column_list.append(category.tag.lower())
                for tag in root.iter(category.tag):
                    for item in tag.iterfind('item'):
                        if item.findtext('calendarDate')==date:
                            xml_list.append(item.findtext('value'))
        
        #Combine xml_list and column_list in a xml_df dataframe
        xml_df = pd.DataFrame(xml_list).T  # Write in DF and transpose it
        xml_df.columns = column_list  # Update column names
        xml_df = xml_df.reindex(sorted(xml_df.columns), axis=1) # Sort alphabeticaly
        #Combine the dataframes
        combined_df = db_df.append(xml_df)
        #Drop all columns that do not exist as DB fields
        combined_df = combined_df[db_fields_list]
        #Export all values to list
        df2list = combined_df.values.tolist()
        #Flatten the list
        df2list = [item for sublist in df2list for item in sublist]
        
        #Build a list of parameters to pass to sql query
        query_params = df2list+df2list
        query_params.append(date)

        # PG Amend path for postgres "pg_read_file()" function.
        text = file_path
        head, sep, tail = text.partition('temp/')
        pg_read_file = (tail, )
        
        list_sql = """
        INSERT INTO garmin_connect_wellness (athlete_id, calendar_date, common_total_calories, common_total_distance, food_calories_consumed, 
        food_calories_remaining, sleep_duration, wellness_abnormalhr_alerts_count, wellness_active_calories, wellness_average_steps, wellness_average_stress, 
        wellness_bmr_calories, wellness_body_battery_drained, wellness_bodybattery_charged, wellness_common_active_calories, wellness_floors_ascended, 
        wellness_floors_descended, wellness_max_avg_heart_rate, wellness_max_heart_rate, wellness_max_stress, wellness_min_avg_heart_rate, 
        wellness_min_heart_rate, wellness_moderate_intensity_minutes, wellness_resting_heart_rate, wellness_total_calories, wellness_total_distance, 
        wellness_total_steps, wellness_total_steps_goal, wellness_user_floors_ascended_goal, wellness_user_intensity_goal, wellness_vigorous_intensity_minutes)
        
        VALUES ((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (calendar_date) DO UPDATE

        SET (athlete_id, calendar_date, common_total_calories, common_total_distance, food_calories_consumed, food_calories_remaining, sleep_duration, 
        wellness_abnormalhr_alerts_count, wellness_active_calories, wellness_average_steps, wellness_average_stress, wellness_bmr_calories, 
        wellness_body_battery_drained, wellness_bodybattery_charged, wellness_common_active_calories, wellness_floors_ascended, wellness_floors_descended, 
        wellness_max_avg_heart_rate, wellness_max_heart_rate, wellness_max_stress, wellness_min_avg_heart_rate, wellness_min_heart_rate, 
        wellness_moderate_intensity_minutes, wellness_resting_heart_rate, wellness_total_calories, wellness_total_distance, wellness_total_steps, 
        wellness_total_steps_goal, wellness_user_floors_ascended_goal, wellness_user_intensity_goal, wellness_vigorous_intensity_minutes)
        = ((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        WHERE garmin_connect_wellness.calendar_date
        = %s;
        """

        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            with StdoutRedirection(ath_un):
                print('Inserting Wellness Data into postgreSQL:')
            with ProgressStdoutRedirection(ath_un):
                print('Inserting Wellness Data into postgreSQL:')
            #cur.execute(xpath_sql,(athlete_id,pg_read_file,athlete_id,file2import,file2import,file2import))
            cur.execute(list_sql,(query_params))
            conn.commit()
            
                    # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
        finally:
            if conn is not None:
                conn.close()
                with StdoutRedirection(ath_un):
                    print('Wellness Data Inserted Successfully')
                with ProgressStdoutRedirection(ath_un):
                    print('Wellness Data Inserted Successfully')


