#!/usr/bin/python

import psycopg2
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
from database_ini_parser import config
import subprocess
import gzip
import os
import zipfile
import datetime
from archive_data_dropbox import check_if_file_exists_in_dbx, download_files_to_dbx
from Athlete_Data_Utills import StdoutRedirection
from processify import processify
from db_encrypt import str2md5

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

def check_db_server_connectivity(gc_username,db_host,superuser_un,superuser_pw):
    conn = None
    
    sql_svr_conn = """
    select version();
    """

    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(dbname='postgres', host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()
        
        cur.execute(sql_svr_conn)
        result = cur.fetchone()
        if result:  
            connection = 'SUCCESS'
        # close the communication with the PostgreSQL
        cur.close()
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(gc_username):
            print((str(datetime.datetime.now()) + ' ' + str(error)))
        connection = str(error)
        return connection
    finally:
        if conn is not None:
            conn.close()
        
def check_user_db_exists(gc_username,gc_password,db_host,superuser_un,superuser_pw,encr_pass):
    conn = None
    username = (gc_username)
    db_name = str(str2md5(username)) + '_Athlete_Data_DB'
    with ProgressStdoutRedirection(gc_username):
        print(('User DB Name: '+str(db_name)))

    sql_check_db_exists = """
    select exists(SELECT datname FROM pg_catalog.pg_database WHERE datname = %s);
    """

    try:
        # read connection parameters

        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname='postgres', host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(gc_username):
            print('Executing SQL to check whether the database aleady exists')
        
        cur.execute(sql_check_db_exists,(db_name,))
        result = cur.fetchone()
        if result[0] is True:  
            db_exists = True
        else:
            db_exists = False
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
         with ErrorStdoutRedirection(gc_username):
             print((str(datetime.datetime.now()) + '  ' + str(error))) 

    finally:
        if conn is not None:
            conn.close()
            with ProgressStdoutRedirection(gc_username):
                print('Database connection closed.')
            
    return db_exists

def check_host_record_exists(gc_username,db_name,db_host,encr_pass):
    conn_localhost = None

    sql_create_info_db_table = """
    CREATE TABLE IF NOT EXISTS public.db_info
        (id serial NOT NULL,
        db_name character varying(50) COLLATE pg_catalog."default",
        db_host character varying(50) COLLATE pg_catalog."default",
        db_un character varying(50) COLLATE pg_catalog."default",
        db_pw character varying(50) COLLATE pg_catalog."default",
        db_auto_synch boolean,
        CONSTRAINT db_info_pkey PRIMARY KEY (id),
        CONSTRAINT db_info_unique UNIQUE (db_name))
    WITH (OIDS = FALSE)
    TABLESPACE pg_default;
    ALTER TABLE public.db_info OWNER to postgres;
    """

    sql_check_db_host_exists = """
    SELECT db_host FROM db_info WHERE db_name = %s;
    """

    try:
        # connect to the PostgreSQL server
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        conn_localhost = psycopg2.connect(**params)
        conn_localhost.autocommit = True

        # create a cursor
        cur = conn_localhost.cursor()

        # execute a statement
        with ProgressStdoutRedirection(gc_username):
            print('Checking whether the db_host record aleady exists')
        
        cur.execute(sql_create_info_db_table)
        cur.execute(sql_check_db_host_exists,(db_name,))
        result = cur.fetchone()

        if result is not None:#Previous record exists
            stored_db_host = result[0]
            if stored_db_host != db_host:#Previous record does not match
                db_host_diff = True
            else:
                db_host_diff = False
        else:#No previous record exists
            db_host_diff = False
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(gc_username):
            print(error)

    finally:
        if conn_localhost is not None:
            conn_localhost.close()

    return db_host_diff

@processify
def create_user_db(gc_username,gc_password,db_host,db_name,superuser_un,superuser_pw,encrypted_superuser_pw,save_pwd,encr_pass):
    conn = None
    username = (gc_username)
    db_name = (db_name)
    head, sep, tail = username.partition('@')
    db_username = head

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
    open(pidfile, 'w').write(pid)
    
    sql_get_lc_collate = "SHOW LC_COLLATE"
    sql_create_db = "CREATE DATABASE \""+ db_name +"\" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = %s LC_CTYPE = %s;"
    sql_create_dbuser = "CREATE USER \""+db_username+"\" WITH PASSWORD \'"+ gc_password +"\';"
    sql_insert_db_info_record = "INSERT INTO db_info (db_name, db_host, db_un, db_pw,db_auto_synch) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (db_name) DO NOTHING; "
    
    try:    
        conn = psycopg2.connect(dbname='postgres', host=db_host, user=superuser_un, password=superuser_pw)
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(gc_username):
            print('Creating user database...')
        
        cur.execute(sql_get_lc_collate)
        lc_collate = cur.fetchone()
        cur.execute(sql_create_db,(lc_collate[0],lc_collate[0]))
        cur.execute(sql_create_dbuser)
        

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(gc_username):
            print(error)

    finally:
        if conn is not None:
            conn.close()

    #Insert user db connection info into postgres/db_info table 
    try:
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        conn_localhost = psycopg2.connect(**params)
        conn_localhost.autocommit = True

        # create a cursor
        cur_localhost = conn_localhost.cursor()

        # execute a statement
        with ProgressStdoutRedirection(gc_username):
            print('Inserting DB connection info...')
        
        cur_localhost.execute(sql_insert_db_info_record,(db_name,db_host,superuser_un,encrypted_superuser_pw,save_pwd))
        
        # close the communication with the PostgreSQL
        cur_localhost.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(gc_username):
            print(error)

    finally:
        if conn_localhost is not None:
            conn_localhost.close 

@processify
def backup_user_db(db_name,gc_username,output,dbx_auth_token, encr_pass):

    db_name = (db_name)
    if os.name == 'nt':
        backup_file_path = output+'\\'+gc_username+'\DB_Backup.gz'
    else:
        backup_file_path = output+'/'+gc_username+'/DB_Backup.gz'

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
    open(pidfile, 'w').write(pid)
    open(pidfile).close

    # read connection parameters
    params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
    superuser_un = params.get("user")
    superuser_pw = params.get("password")
    db_host = params.get("host")
    
    try:
        with gzip.open(backup_file_path, 'wb') as f:
            with StdoutRedirection(gc_username):
                print('Backing up DB, please wait....')
            with ProgressStdoutRedirection(gc_username):
                print('Backing up DB, please wait....')
     
            # create .pgpass in user's AppData or home directory 
            if os.name == 'nt':
                appdata_dir  = os.getenv('APPDATA')
                pgpass_dir = os.path.join(appdata_dir,"postgresql")
                pgpassfile = os.path.join(pgpass_dir,"pgpass.conf")
                if not os.path.exists(pgpass_dir):
                    os.makedirs(pgpass_dir)
                if not os.path.exists(pgpassfile):
                    open(pgpassfile,'w+').write(db_host+':5432:*:postgres:'+superuser_pw)
                    open(pgpassfile).close
            else:
                pgpassfile = os.path.expanduser('~')+'/.pgpass'
                if not os.path.exists(pgpassfile):
                    open(pgpassfile,'w+').write(db_host+':5432:*:postgres:'+superuser_pw)
                    open(pgpassfile).close
                    os.chmod(pgpassfile, 0o600)
            # execute pg_dump
            popen = subprocess.Popen(['pg_dump','-h', db_host, '-U', superuser_un, db_name], stdout=subprocess.PIPE, universal_newlines=True)
            for stdout_line in iter(popen.stdout.readline, ""):
                f.write(stdout_line.encode())
            popen.stdout.close()
            popen.wait()
            try:
                os.remove(pgpassfile)
            except Exception as e:
                 with ErrorStdoutRedirection(gc_username):
                     print((str(datetime.datetime.now()) + '  ' + str(e)))
            with StdoutRedirection(gc_username):
                print('DB backup completed. The backup file will be uploaded to Dropbox now.')
            with ProgressStdoutRedirection(gc_username):
                print('DB backup completed. The backup file will be uploaded to Dropbox now.')
    except Exception as e:
        with ErrorStdoutRedirection(gc_username):
            print((str(datetime.datetime.now()) + '  ' + str(e)))
    
    today = datetime.datetime.today().strftime('%Y%m%d')
    download_folder_dbx = 'DB_Backup'
    file_name_to = today+'_DB_Backup.gz'

    dbx_file_exists = check_if_file_exists_in_dbx(file_name_to,dbx_auth_token,download_folder_dbx)
    if dbx_file_exists == True:
        with StdoutRedirection(gc_username):
            print((file_name_to+' already exists in Dropbox, skipping.'))
        with ProgressStdoutRedirection(gc_username):
            print((file_name_to+' already exists in Dropbox, skipping.'))
    else:
        try:
            with StdoutRedirection(gc_username):
                print(('Uploading '+file_name_to+' Dropbox, please wait.'))
            download_files_to_dbx(backup_file_path,file_name_to,dbx_auth_token, download_folder_dbx)
            with StdoutRedirection(gc_username):
                print('DB Backup file uploaded to Dropbox successfuly')
            with ProgressStdoutRedirection(gc_username):
                print('DB Backup file uploaded to Dropbox successfuly')
        except Exception as e:
            with ErrorStdoutRedirection(gc_username):
                print((str(datetime.datetime.now()) + '  ' + str(e)))

@processify
def restore_db_schema(gc_username,gc_password,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    conn = None
    username = (gc_username)
    db_name = (db_name)
    head, sep, tail = username.partition('@')
    db_username = head

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
    open(pidfile, 'w').write(pid)

    
    #PG: Read SQL query to restore db schema from file
    sql_file = open('db_schema.sql', 'r')
    sql_restore_db_schema = s = " ".join(sql_file.readlines())
    
    sql_grant_userpriv = "GRANT ALL PRIVILEGES ON DATABASE \""+ db_name +"\" to \""+db_username+"\";"
    sql_grant_table_permissions = "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \""+db_username+"\";"    
    sql_revoke_public = "REVOKE ALL ON DATABASE \""+ db_name +"\" FROM PUBLIC;"


    try:
         
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(gc_username):
            print('Restoring DB schema...')
        
        cur.execute(sql_restore_db_schema)
        cur.execute(sql_grant_userpriv)
        cur.execute(sql_grant_table_permissions)
        cur.execute(sql_revoke_public)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(gc_username):
            print(error)

    finally:
        if conn is not None:
            conn.close()
            
@processify
def create_sample_db(encr_pass):
    conn = None
    db_name = "sample_db"
    
    sql_get_lc_collate = "SHOW LC_COLLATE"
    sql_check_db_exists = "select exists(SELECT datname FROM pg_catalog.pg_database WHERE datname = %s);"
    sql_create_db = "CREATE DATABASE \""+ db_name +"\" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = %s LC_CTYPE = %s;"

    try:
        # read connection parameters
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ConsolidatedProgressStdoutRedirection():
            print('Checking whether the sample DB aleady exists')
        
        cur.execute(sql_check_db_exists,(db_name,))
        result = cur.fetchone()
        if result[0] is True:  
            db_exists = True
            with ConsolidatedProgressStdoutRedirection():
                print('Sample DB already exists, exiting...')
        else:
            db_exists = False

        if db_exists == False:
            with ConsolidatedProgressStdoutRedirection():
                print("Creating sample DB...")
            cur.execute(sql_get_lc_collate)
            lc_collate = cur.fetchone()
            cur.execute(sql_create_db,(lc_collate[0],lc_collate[0]))
            cur.close()
            conn.close
            #PG: Read SQL query to restore db schema from file
            sql_file = open('db_schema.sql', 'r')
            sql_restore_db_schema = s = " ".join(sql_file.readlines())
            try:
                # read connection parameters
                params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
                superuser_un = params.get("user")
                superuser_pw = params.get("password")
                
                # connect to the PostgreSQL server (sample_db)
                conn = psycopg2.connect(dbname=db_name, user=superuser_un, password=superuser_pw)
                conn.autocommit = True
                # create a cursor
                cur = conn.cursor()
                with ConsolidatedProgressStdoutRedirection():
                    print("Restoring sample DB schema...")
                cur.execute(sql_restore_db_schema)
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                with ConsolidatedProgressStdoutRedirection():
                    print(error)
        else:
            cur.close()
            conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ConsolidatedProgressStdoutRedirection():
            print(error)

    finally:
        if conn is not None:
            conn.close()

