#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ConsolidatedProgressStdoutRedirection
import sys
from db_encrypt import generate_key,pad_text,unpad_text
from main_data_autosynch import auto_synch
import Crypto.Random
from Crypto.Cipher import AES
import base64
import datetime

#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16


def decrypt(ciphertext, password):
    salt = ciphertext[0:SALT_SIZE]
    #iv = ciphertext[:AES.block_size]
    ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    return plaintext 

#Return list of all DBs
def get_databases_list(encr_pass):
    conn = None

    sql_get_databases = """
    SELECT
        datname
    FROM
       pg_database 
    WHERE 
       datname like '%_Athlete_Data_DB';
    """
    # Retrieve list of databases with last synch older than n
    sql_get_databases_db_info = """
    SELECT
        db_name
    FROM
       db_info 
    WHERE 
       db_auto_synch = 'true' AND last_synch::timestamp < %s::timestamp;
    """

    try:
        # read connection parameters
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        autosynch_params = config(filename="encrypted_settings.ini", section="autosynch",encr_pass=encr_pass)
        
        postgres_db = params.get("database")
        postgres_un = params.get("user")
        postgres_pw = params.get("password")

        interval = int(autosynch_params.get("interval")) #The amount of time in seconds to wait before attempting next synch
        time_now = datetime.datetime.now()
        now_less_interval_dt = time_now - datetime.timedelta(seconds=interval)
        now_less_interval_str = now_less_interval_dt.strftime("%Y-%m-%d %H:%M:%S")

        conn = psycopg2.connect(dbname=postgres_db, user=postgres_un, password=postgres_pw)
         
        # connect to the PostgreSQL server
        with ConsolidatedProgressStdoutRedirection():
            print('Connecting to the PostgreSQL server to get list of databases...')

        # create a cursor
        cur = conn.cursor()
        # Retrieve list of databases with last synch older than n
        cur.execute(sql_get_databases_db_info,(now_less_interval_str,))
        conn.commit()
        databases = cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        with ConsolidatedProgressStdoutRedirection():
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()

    return databases

def retrieve_decrypt_creds(synch_req_db_list,encr_pass,full_synch=False):
    sql_get_creds = """
    SELECT 
        gc_email,gc_password,mfp_username,mfp_password,diasend_username,diasend_password,dropbox_access_token,glimp_export_link,libreview_export_link,mm_export_link,oura_refresh_token,strava_refresh_token,ath_un
    FROM
        athlete;
    """

    sql_select_dbsu_creds ="""
    SELECT
        db_host,db_un,db_pw
    FROM
        db_info
    WHERE
       db_name = %s;
    """

    for row in synch_req_db_list:          
        for db in row:
            try:
                #Reset all user variables
                conn = None
                ath_un = None

                gc_un = None
                gc_encr_pw = None
                gc_decr_pw = None

                mfp_un = None
                mfp_encr_pw = None
                mfp_decr_pw = None

                cgm_un = None
                cgm_encr_pw = None
                cgm_decr_pw = None

                dbx_encr_token = None
                dbx_decr_token = None

                oura_encr_token = None
                oura_decr_token = None

                strava_encr_token = None
                strava_decr_token = None
                
                glimp_encr_export_link = None
                glimp_decr_export_link = None

                libreview_encr_export_link = None
                libreview_decr_export_link = None

                mm_encr_export_link = None
                mm_decr_export_link = None

                # read connection parameters
                dbsu_params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
                superuser_un = dbsu_params.get("user")
                superuser_pw = dbsu_params.get("password")
            
                dbsu_conn = psycopg2.connect(dbname='postgres', user=superuser_un, password=superuser_pw)
                dbsu_cur = dbsu_conn.cursor()
                dbsu_cur.execute(sql_select_dbsu_creds,(db,))
                dbsu_conn.commit()
                dbsu_result = dbsu_cur.fetchone()
                db_host = dbsu_result[0]
                db_un = dbsu_result[1]
                db_pw = dbsu_result[2]
                
                if db_host != 'localhost':#User database is hosted remotely
                    superuser_un = db_un
                    superuser_pw = decrypt(base64.b64decode(db_pw), encr_pass)
            except (Exception, psycopg2.DatabaseError) as error:
                with ConsolidatedProgressStdoutRedirection():
                    print('Autosynch DB Error: '+str(error))
            finally:
                if dbsu_conn is not None:
                    dbsu_conn.close()

            try:
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db, host=db_host, user=superuser_un, password=superuser_pw)
                cur = conn.cursor()  
                cur.execute(sql_get_creds)
                conn.commit()
                result = cur.fetchone()
                gc_un=result[0]
                gc_encr_pw=result[1]
                mfp_un=result[2]
                mfp_encr_pw=result[3]
                cgm_un=result[4]
                cgm_encr_pw=result[5]
                dbx_encr_token=result[6]
                glimp_encr_export_link=result[7]
                libreview_encr_export_link=result[8]
                mm_encr_export_link=result[9]
                oura_encr_token=result[10]
                strava_encr_token=result[11]
                ath_un=result[12]

                #Now decrypt (gc_encr_pw,mfp_encr_pw,dbx_encr_token and others)
                if gc_encr_pw is not None:
                    gc_decr_pw = decrypt(base64.b64decode(gc_encr_pw), encr_pass)
                if mfp_encr_pw is not None:
                    mfp_decr_pw = decrypt(base64.b64decode(mfp_encr_pw), encr_pass)
                if cgm_encr_pw is not None:
                    cgm_decr_pw = decrypt(base64.b64decode(cgm_encr_pw), encr_pass)
                if dbx_encr_token is not None:
                    dbx_decr_token = decrypt(base64.b64decode(dbx_encr_token), encr_pass) 
                if glimp_encr_export_link is not None:
                    glimp_decr_export_link = decrypt(base64.b64decode(glimp_encr_export_link), encr_pass)
                if libreview_encr_export_link is not None:
                    libreview_decr_export_link = decrypt(base64.b64decode(libreview_encr_export_link), encr_pass)
                if mm_encr_export_link is not None:
                    mm_decr_export_link = decrypt(base64.b64decode(mm_encr_export_link), encr_pass)	
                if oura_encr_token is not None:
                    oura_decr_token = decrypt(base64.b64decode(oura_encr_token), encr_pass)
                if strava_encr_token is not None:
                    strava_decr_token = decrypt(base64.b64decode(strava_encr_token), encr_pass)

                ###Execute auto synch from "main_data_autosynch.py"###
                auto_synch(ath_un, db, db_host, superuser_un, superuser_pw, gc_un, gc_decr_pw, mfp_un, mfp_decr_pw, cgm_un, cgm_decr_pw, glimp_decr_export_link, libreview_decr_export_link, mm_decr_export_link, dbx_decr_token, oura_decr_token, strava_decr_token, encr_pass,full_synch)
                
            except (Exception, psycopg2.DatabaseError) as error:
                with ConsolidatedProgressStdoutRedirection():
                    print(('Autosynch DB Error: '+str(error)))

            finally:
                if conn is not None:
                    conn.close()
