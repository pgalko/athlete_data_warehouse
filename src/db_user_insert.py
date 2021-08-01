#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os
import datetime
import Crypto.Random
from Crypto.Cipher import AES
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
import base64

#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    #iv = Crypto.Random.get_random_bytes(AES.block_size)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt

@processify
def insert_last_synch_timestamp(ath_un,encr_pass,db_name):
    last_synch = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    last_synch = (last_synch, )
    user_db = (db_name, )

    sql_postgres_db ="""     
    UPDATE db_info SET last_synch = %s where db_name= %s;
    """
    #Insert last_synch into postgres/db_info table 
    try:
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        postgres_db = params.get("database")
        postgres_un = params.get("user")
        postgres_pw = params.get("password")

        conn_localhost = psycopg2.connect(dbname=postgres_db, user=postgres_un, password=postgres_pw)
        conn_localhost.autocommit = True

        # create a cursor
        cur_localhost = conn_localhost.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting last_synch timestamp into postgres/db_info table:')
        
        cur_localhost.execute(sql_postgres_db,(last_synch,user_db))
        
        # close the communication with the PostgreSQL
        cur_localhost.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn_localhost is not None:
            conn_localhost.close

@processify
def user_tokens_insert(ath_un,db_host,db_name,superuser_un,superuser_pw,dbx_auth_token,oura_refresh_token,strava_refresh_token,encr_pass,save_pwd):
        
    if save_pwd == True:
        #Encrypt dbx token
        if dbx_auth_token is not None:
            encrypted_dbx_auth_token = base64.b64encode(encrypt(dbx_auth_token, encr_pass))
            encrypted_dbx_auth_token = encrypted_dbx_auth_token.decode('utf-8')
        else:
            encrypted_dbx_auth_token = None
        #Encrypt oura token
        if oura_refresh_token is not None:
            encrypted_oura_refresh_token = base64.b64encode(encrypt(oura_refresh_token, encr_pass))
            encrypted_oura_refresh_token = encrypted_oura_refresh_token.decode('utf-8')
        else:
            encrypted_oura_refresh_token = None
        #Encrypt strava token
        if strava_refresh_token is not None:
            encrypted_strava_refresh_token = base64.b64encode(encrypt(strava_refresh_token, encr_pass))
            encrypted_strava_refresh_token = encrypted_strava_refresh_token.decode('utf-8')
        else:
            encrypted_strava_refresh_token = None
    else:
        encrypted_dbx_auth_token = None
        encrypted_oura_refresh_token = None
        encrypted_strava_refresh_token = None
    
    #Query params lists
    ath_user = (ath_un, )
    auth_token_tuple = (encrypted_dbx_auth_token, )
    oura_token_tuple = (encrypted_oura_refresh_token, )
    strava_token_tuple = (encrypted_strava_refresh_token, )
    
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN  

    UPDATE athlete SET ath_un = %s where ath_un = %s;
            
    ELSE
    INSERT INTO athlete (ath_un) VALUES 
    (%s);

    END IF;
    
    END
    $do$
    """

    sql_insert_dbx_auth_token = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET dropbox_access_token = %s where ath_un= %s;


    END IF;
    
    END
    $do$

    """

    sql_insert_oura_refresh_token = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET oura_refresh_token = %s where ath_un= %s;

    END IF;
    
    END
    $do$

    """

    sql_insert_strava_refresh_token = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET strava_refresh_token = %s where ath_un= %s;

    END IF;
    
    END
    $do$

    """

    try:
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name,host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting GC User Data into postgreSQL:')
        cur.execute(sql,(ath_user,ath_user,ath_user,ath_user))							 
        conn.commit()

        if dbx_auth_token is not None:
            with ProgressStdoutRedirection(ath_un):
                print('Inserting Dropbox user authentication token into postgreSQL:')
            cur.execute(sql_insert_dbx_auth_token,(ath_user,auth_token_tuple,ath_user))
            conn.commit()

        if oura_refresh_token is not None:
            with ProgressStdoutRedirection(ath_un):
                print('Inserting Oura refresh token into postgreSQL:')
            cur.execute(sql_insert_oura_refresh_token,(ath_user,oura_token_tuple,ath_user))
            conn.commit()

        if strava_refresh_token is not None:
            with ProgressStdoutRedirection(ath_un):
                print('Inserting Strava refresh token into postgreSQL:')
            cur.execute(sql_insert_strava_refresh_token,(ath_user,strava_token_tuple,ath_user))
            conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
            if conn is not None:
                    conn.close()
                                   
@processify
def gc_user_insert(ath_un,gc_username, gc_password, db_host,db_name,superuser_un,superuser_pw,encr_pass,save_pwd):
        
    if save_pwd == True:
        #Encrypt gc password.
        if gc_password is not None:
            encrypted_pwd = base64.b64encode(encrypt(gc_password, encr_pass))
            encrypted_pwd = encrypted_pwd.decode('utf-8')
        else:
            encrypted_pwd = None
    else:
        encrypted_pwd = None
    
    #Query params lists
    gc_user = (gc_username, )
    gc_pwd = (encrypted_pwd, )
    ath_user = (ath_un, )
    
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

    UPDATE athlete SET gc_password = %s where gc_email= %s;

    ELSEIF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET gc_password = %s,gc_email = %s where ath_un= %s;


    END IF;
    
    END
    $do$

    """

    try:   
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name,host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting GC User Data into postgreSQL:')
        cur.execute(sql,(gc_user,gc_pwd,gc_user,ath_user,gc_pwd,gc_user,ath_user))							 
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()
@processify
def mfp_user_insert(mfp_username,mfp_password,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    mfp_user = (mfp_username, )
    mfp_pwd = (mfp_password, )
    gc_user = (ath_un, )
    db_name = (db_name)
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE mfp_username = %s) THEN

    UPDATE athlete SET mfp_password = %s where mfp_username= %s;

    ELSEIF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET mfp_password = %s,mfp_username = %s where ath_un= %s;


    END IF;
    
    END
    $do$

    """
    try:
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting MFP User Data into postgreSQL:')
        cur.execute(sql,(mfp_user,mfp_pwd,mfp_user,gc_user,mfp_pwd,mfp_user,gc_user))
        conn.commit()
        
                # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()

@processify
def diasend_user_insert(diasend_username,diasend_password,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    diasend_user = (diasend_username, )
    diasend_pwd = (diasend_password, )
    gc_user = (ath_un, )
    db_name = (db_name)
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE diasend_username = %s) THEN

    UPDATE athlete SET diasend_password = %s where diasend_username= %s;

    ELSEIF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET diasend_password = %s,diasend_username = %s where ath_un= %s;

    END IF;
    
    END
    $do$

    """

    try:  
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting Diasend User Data into postgreSQL:')
        cur.execute(sql,(diasend_user,diasend_pwd,diasend_user,gc_user,diasend_pwd,diasend_user,gc_user))
        conn.commit()
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()

@processify  
def glimp_user_insert(glimp_export_link,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    glimp_export_link = (glimp_export_link, )
    gc_user = (ath_un, )
    db_name = (db_name)
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET glimp_export_link = %s where ath_un= %s;

    END IF;
    
    END
    $do$

    """

    try:
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting Glimp User Data into postgreSQL:')
        cur.execute(sql,(gc_user,glimp_export_link,gc_user))
        conn.commit()
        
                # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()

@processify
def libreview_user_insert(libreview_export_link,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    libreview_export_link = (libreview_export_link, )
    gc_user = (ath_un, )
    db_name = (db_name)
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET libreview_export_link = %s where ath_un= %s;

    END IF;
    
    END
    $do$

    """

    try:
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting LIbreView User Data into postgreSQL:')
        cur.execute(sql,(gc_user,libreview_export_link,gc_user))
        conn.commit()
        
                # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()

@processify
def mm_user_insert(mm_export_link,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    mm_export_link = (mm_export_link, )
    gc_user = (ath_un, )
    db_name = (db_name)
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
    DO
    $do$
    BEGIN
    IF

    EXISTS (SELECT id FROM athlete WHERE ath_un = %s) THEN

    UPDATE athlete SET mm_export_link = %s where ath_un= %s;

    END IF;
    
    END
    $do$

    """

    try:
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting Mind Monitor User Data into postgreSQL:')
        cur.execute(sql,(gc_user,mm_export_link,gc_user))
        conn.commit()
        
                # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()

@processify
def update_autosynch_prefrnc(ath_un,db_host,db_name,superuser_un,superuser_pw,encrypted_superuser_pw,enable_auto_synch,encr_pass):

    ath_user = (ath_un,)

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    #Do not save pw to db_info if no autosynch or db_host=localhost
    if enable_auto_synch == True:
        if db_host != 'localhost':
            encrypted_superuser_pw = (encrypted_superuser_pw,)
        else:
            encrypted_superuser_pw = None
    else:
        encrypted_superuser_pw = None

    enable_auto_synch = (enable_auto_synch,)
    conn = None

    sql = """

    UPDATE athlete SET auto_sync = %s where ath_un= %s;
            
    """
    
    sql_postgres_db ="""
    
    UPDATE db_info SET db_auto_synch = %s,db_un = %s,db_pw = %s where db_name= %s;

    """
    #Insert user autosynch preference into user db athlete table
    try:
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting Auto_Sych preferences into postgreSQL:')
        cur.execute(sql,(enable_auto_synch,ath_user))
        conn.commit()
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()

    #Insert user autosynch preference into postgres/db_info table 
    try:
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        postgres_db = params.get("database")
        postgres_un = params.get("user")
        postgres_pw = params.get("password")

        conn_localhost = psycopg2.connect(dbname=postgres_db, user=postgres_un, password=postgres_pw)
        conn_localhost.autocommit = True

        # create a cursor
        cur_localhost = conn_localhost.cursor()

        # execute a statement
        with ProgressStdoutRedirection(ath_un):
            print('Inserting Auto_Sych preferences into postgres/db_info table:')
        
        cur_localhost.execute(sql_postgres_db,(enable_auto_synch,superuser_un,encrypted_superuser_pw,db_name))
        
        # close the communication with the PostgreSQL
        cur_localhost.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn_localhost is not None:
            conn_localhost.close

def check_user_exists(ath_un,encr_pass):

    conn_localhost = None

    sql_check_user_exists = """
    SELECT ath_un FROM db_info WHERE ath_un = %s;
    """

    try:
        params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
        postgres_db = params.get("database")
        postgres_un = params.get("user")
        postgres_pw = params.get("password")

        conn_localhost = psycopg2.connect(dbname=postgres_db, user=postgres_un, password=postgres_pw)
        conn_localhost.autocommit = True

        # create a cursor
        cur_localhost = conn_localhost.cursor()

        # execute a statement
        cur_localhost.execute(sql_check_user_exists,(ath_un,))
        
        result = cur_localhost.fetchone()
        if result[0] is not None:#User record exists
            user_exists = True
            return user_exists
        else:
            user_exists = False

        # close the communication with the PostgreSQL
        cur_localhost.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn_localhost is not None:
            conn_localhost.close
    
    

