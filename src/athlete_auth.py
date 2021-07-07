import psycopg2
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
import sys
from database_ini_parser import config
import os
import datetime
from processify import processify
from db_encrypt import str2md5
from werkzeug.security import generate_password_hash, check_password_hash

def ath_auth_register(ath_un,ath_pw,encr_pass):

    sql_create_info_db_table = """
    CREATE TABLE IF NOT EXISTS public.db_info
        (id serial NOT NULL,
        ath_un character varying(300) COLLATE pg_catalog."default",
        ath_pw character varying(300) COLLATE pg_catalog."default",
        db_name character varying(300) COLLATE pg_catalog."default",
        db_host character varying(300) COLLATE pg_catalog."default",
        db_un character varying(300) COLLATE pg_catalog."default",
        db_pw character varying(300) COLLATE pg_catalog."default",
        last_synch character varying(300) COLLATE pg_catalog."default",
        db_auto_synch boolean,
        CONSTRAINT db_info_pkey PRIMARY KEY (id),
        CONSTRAINT db_info_unique UNIQUE (db_name))
    WITH (OIDS = FALSE)
    TABLESPACE pg_default;
    ALTER TABLE public.db_info OWNER to postgres;
    """
    sql_insert_db_info_record = "INSERT INTO db_info (ath_un,ath_pw,db_name) VALUES (%s,%s,%s);"

    ath_pw_hash = generate_password_hash(ath_pw)

    db_name = str(str2md5(ath_un)) + '_Athlete_Data_DB'
    query_params = (ath_un,ath_pw_hash,db_name)

    try:
        # connect to the PostgreSQL server
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        postgres_db = params.get("database")
        superuser_un = params.get("user")
        superuser_pw = params.get("password")

        conn_localhost = psycopg2.connect(dbname=postgres_db, user=superuser_un, password=superuser_pw)
        conn_localhost.autocommit = True

        # create a cursor
        cur = conn_localhost.cursor()

        cur.execute(sql_create_info_db_table)
        cur.execute(sql_insert_db_info_record,query_params)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.IntegrityError) as error:
        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
        return None
    finally:
        if conn_localhost is not None:
            conn_localhost.close()
    return ath_un

def ath_auth_login(ath_un,ath_pw,encr_pass):

    sql_select_usr_pwd = "SELECT ath_pw FROM db_info WHERE ath_un = %s;"

    query_params = (ath_un,)

    try:
        # connect to the PostgreSQL server
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        postgres_db = params.get("database")
        superuser_un = params.get("user")
        superuser_pw = params.get("password")

        conn_localhost = psycopg2.connect(dbname=postgres_db, user=superuser_un, password=superuser_pw)
        conn_localhost.autocommit = True

        # create a cursor
        cur = conn_localhost.cursor()
        cur.execute(sql_select_usr_pwd,query_params)
        result = cur.fetchone()
        cur.close()
        if check_password_hash(result[0],ath_pw):       
            return ath_un
        else:
            return None        
    except Exception as error:
        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
        return None
    finally:
        if conn_localhost is not None:
            conn_localhost.close()

def ath_auth_reset(ath_un,ath_pw,encr_pass):

    sql_update_usr_pwd = "UPDATE db_info SET ath_pw = %s where ath_un= %s;"
    
    ath_pw_hash = generate_password_hash(ath_pw)
    query_params = (ath_pw_hash,ath_un)

    try:
        # connect to the PostgreSQL server
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        postgres_db = params.get("database")
        superuser_un = params.get("user")
        superuser_pw = params.get("password")

        conn_localhost = psycopg2.connect(dbname=postgres_db, user=superuser_un, password=superuser_pw)
        conn_localhost.autocommit = True

        # create a cursor
        cur = conn_localhost.cursor()
        cur.execute(sql_update_usr_pwd,query_params)

    except Exception as error:
        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
        return None
    finally:
        if conn_localhost is not None:
            conn_localhost.close()