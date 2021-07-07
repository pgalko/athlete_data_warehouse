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
def data_file_path_insert(file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    file2import = (file_path)
    athlete_id = (ath_un)
    db_name = (db_name)

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    conn = None

    sql = """

    INSERT INTO files (data_file_path,athlete_id)

    VALUES
    (%s,(select id from athlete where ath_un=%s))

    ON CONFLICT (data_file_path) DO NOTHING;
    """
    try:
        
        # connect to the PostgreSQL server
        with ProgressStdoutRedirection(ath_un):
            print('Connecting to the PostgreSQL server to insert data_file_path...')
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        
        cur.execute(sql,(file2import,athlete_id))
        conn.commit()
        
        # close the communication with the PostgreSQL
        cur.close()
 
    except Exception as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    finally:
        if conn is not None:
            conn.close()

@processify
def check_data_file_exists(data_file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    conn = None
    ath_un = (ath_un)
    data_file_path = (data_file_path)
    db_name = db_name

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)


    sql_check_file_exists = """
    SELECT data_file_path FROM files WHERE athlete_id = (select id from athlete where ath_un=%s) and data_file_path =%s;
    """

    try:
         
        # connect to the PostgreSQL server
        with ProgressStdoutRedirection(ath_un):
            print('Connecting to the PostgreSQL server to check if the data_file already exists...')
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement      
        cur.execute(sql_check_file_exists,(ath_un,data_file_path))
        result = cur.fetchone()
        if not result:  
            data_file_exists = False
        else:
            data_file_exists = True
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ProgressStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()
            
    return data_file_exists
