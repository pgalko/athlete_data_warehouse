#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os
import datetime
import pandas as pd
import numpy as np
from xml.etree.ElementTree import parse

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_bodycomposition_insert(file_path,athlete,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        """ Connect to the PostgreSQL database server """
        athlete_id = (athlete, )
        db_name = (db_name)
        body_water=[]
        muscle_mass_gm=[]
        visceral_fat=[]
        weight_gm=[]
        bmi=[]
        body_fat=[]
        physique_rating=[]
        timestamp=[]
        calendar_date=[]
        metabolic_age=[]
        bone_mass_gm=[]
        caloric_intake=[]
        source_type=[]
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + athlete + '_PID.txt'
        open(pidfile, 'w').write(pid)

        # PG Amend path for postgres "pg_read_file()" function.
        text = file_path
        head, sep, tail = text.partition('temp/')
        pg_read_file = (tail, )

        sql = """

        INSERT INTO garmin_connect_body_composition(athlete_id,body_water,muscle_mass_gm,visceral_fat,weight_gm,bmi,
                                                                                        body_fat,physique_rating,timestamp,calendar_date,metabolic_age,
                                                                                        bone_mass_gm,caloric_intake,source_type)

        SELECT

        (select id from athlete where gc_email=%s),
        unnest (xpath('//*[local-name()="item"]/*[local-name()="bodyWater"]/text()', x))::text::numeric AS body_water,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="muscleMass"]/text()', x))::text::int AS muscle_mass_gm,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="visceralFat"]/text()', x))::text::int AS visceral_fat,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="weight"]/text()', x))::text::numeric AS weight_gm,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="bmi"]/text()', x))::text::numeric AS bmi,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="bodyFat"]/text()', x))::text::numeric AS body_fat,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="physiqueRating"]/text()', x))::text::text AS physique_rating,
        to_char(to_timestamp(unnest (xpath('//*[local-name()="item"]/*[local-name()="samplePk"]/text()', x))::text::numeric/1000) AT TIME ZONE 'UTC','YYYY-MM-DD HH24:MI:SS')  AS timestamp,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="calendarDate"]/text()', x))::text::text AS calendar_date,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="metabolicAge"]/text()', x))::text::text AS metabolic_age,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="boneMass"]/text()', x))::text::int AS bone_mass_gm,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="caloricIntake"]/text()', x))::text::text AS caloric_intake,
        unnest (xpath('//*[local-name()="item"]/*[local-name()="sourceType"]/text()', x))::text::text AS source_type
        
        
        FROM UNNEST (xpath('//*[local-name()="root"]', pg_read_file(%s)::xml)) x
                                        
        ON CONFLICT (athlete_id,timestamp) DO NOTHING;
                
        """

        pd_df_sql = """
        INSERT INTO garmin_connect_body_composition(athlete_id,body_water,muscle_mass_gm,visceral_fat,weight_gm,bmi,
                                                        body_fat,physique_rating,timestamp,calendar_date,metabolic_age,
                                                        bone_mass_gm,caloric_intake,source_type)

        VALUES ((select id from athlete where gc_email=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
          
        ON CONFLICT (athlete_id,timestamp) DO NOTHING;
        """

        #Parse the XML document, and append the data to lists
        xml_document = parse(file_path)
        for item in xml_document.iterfind('item'):
            body_water.append(item.findtext('bodyWater'))
            muscle_mass_gm.append(item.findtext('muscleMass'))
            visceral_fat.append(item.findtext('visceralFat'))
            weight_gm.append(item.findtext('weight'))
            bmi.append(item.findtext('bmi'))
            body_fat.append(item.findtext('bodyFat'))
            physique_rating.append(item.findtext('physiqueRating'))
            timestamp.append(datetime.datetime.utcfromtimestamp(float(item.findtext('samplePk'))/1000).strftime('%Y-%m-%d %H:%M:%S'))
            calendar_date.append(item.findtext('calendarDate'))
            metabolic_age.append(item.findtext('metabolicAge'))
            bone_mass_gm.append(item.findtext('boneMass'))
            caloric_intake.append(item.findtext('caloricIntake'))
            source_type.append(item.findtext('sourceType'))
        
        #Get the data from lists to dataframe
        df = pd.DataFrame({'body_water':body_water,'muscle_mass_gm':muscle_mass_gm,'visceral_fat':visceral_fat,'weight_gm':weight_gm,'bmi':bmi,
                           'body_fat':body_fat,'physique_rating':physique_rating,'timestamp':timestamp,'calendar_date':calendar_date,'metabolic_age':metabolic_age,
                           'bone_mass_gm':bone_mass_gm,'caloric_intake':caloric_intake,'source_type':source_type})
        #Replace empty string with None.Required for SQL insert
        df.replace(r'',np.nan,inplace=True)
        df = df.where(pd.notnull(df), None)

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                with StdoutRedirection(athlete):
                    print('Inserting Body composition Data into postgreSQL:')
                with ProgressStdoutRedirection(athlete):
                    print('Inserting Body composition Data into postgreSQL:')
                #Iterate through rows in pandas dataframe
                for row in df.itertuples():
                        df_body_water = row.body_water
                        df_muscle_mass_gm = row.muscle_mass_gm
                        df_visceral_fat = row.visceral_fat
                        df_weight_gm = row.weight_gm
                        df_bmi = row.bmi
                        df_body_fat = row.body_fat
                        df_physique_rating = row.physique_rating
                        df_timestamp = row.timestamp
                        df_calendar_date = row.calendar_date
                        df_metabolic_age = row.metabolic_age
                        df_bone_mass_gm = row.bone_mass_gm
                        df_caloric_intake = row.caloric_intake
                        df_source_type = row.source_type

                        cur.execute(pd_df_sql,(athlete_id,df_body_water,df_muscle_mass_gm,df_visceral_fat,df_weight_gm,df_bmi,df_body_fat,df_physique_rating,df_timestamp,df_calendar_date,df_metabolic_age,df_bone_mass_gm,df_caloric_intake,df_source_type))
                
                ### Insert using Xpath method ###
                #cur.execute(xpath_sql,(athlete_id,pg_read_file))
                conn.commit()
                
                # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(athlete):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
        finally:
                if conn is not None:
                        conn.close()
                        with StdoutRedirection(athlete):
                            print('Body composition Data Inserted Successfully')


