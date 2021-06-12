
import os, shutil
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import datetime

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def delete_all_files(output,gc_username):
    folder = os.path.join(output,gc_username)

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
    open(pidfile, 'w').write(pid)

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path): 
            shutil.rmtree(file_path)
    with StdoutRedirection(gc_username):
        print(('All XML,JSON and FIT files for user: ' + str(gc_username)+' deleted successfully.'))
    with ProgressStdoutRedirection(gc_username):
        print(('All XML,JSON and FIT files for user: ' + str(gc_username)+' deleted successfully.'))

@processify            
def delete_all_db_data(gc_username,mfp_username,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    db_name = (db_name)
    conn = None

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
    open(pidfile, 'w').write(pid)

    sql = """
         TRUNCATE mfp_nutrition,timezones,gmt_local_time_difference,mind_monitor_eeg,diasend_cgm,garmin_connect_hrv_tracking,gc_original_wellness_sleep_tracking,gc_original_wellness_stress_tracking,gc_original_wellness_hr_tracking,gc_original_wellness_activity_tracking,
         gc_original_wellness_act_type_summary,garmin_connect_wellness,garmin_connect_daily_summary,garmin_connect_body_composition,garmin_connect_original_record,garmin_connect_original_lap,
         garmin_connect_original_session,files,athlete RESTART IDENTITY;
         """ 

    sql_shared_db = """
         delete from mfp_nutrition where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from mind_monitor_eeg where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from diasend_cgm where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from gc_original_wellness_stress_tracking where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from garmin_connect_hrv_tracking where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from gc_original_wellness_hr_tracking where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from gc_original_wellness_activity_tracking where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from gc_original_wellness_act_type_summary where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from garmin_connect_wellness where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from garmin_connect_daily_summary where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from garmin_connect_body_composition where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from garmin_connect_original_record TP
         using garmin_connect_original_lap LP, garmin_connect_original_session AC
         where (TP.lap_id = LP.id) and (LP.gc_activity_id=AC.gc_activity_id) and AC.athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from garmin_connect_original_lap LP
         using garmin_connect_original_session AC
         where (LP.gc_activity_id=AC.gc_activity_id) and AC.athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from garmin_connect_original_session where athlete_id = (select id from athlete where gc_email=%s or mfp_username = %s);

         delete from files where athlete_id = (select id from athlete where gc_email=%s);

         delete from athlete where gc_email=%s or mfp_username = %s;

         
         """
    try:
         
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        with StdoutRedirection(gc_username):            
            print(('Deleting DB data for user: ' + str(gc_username)+'....'))
        cur.execute(sql)
        conn.commit()
                    
        # close the communication with the PostgreSQL
        cur.close()

                    
    except  (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(gc_username):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
    finally:
            if conn is not None:
                conn.close()
                with StdoutRedirection(gc_username):
                    print(('All DB data for user: ' + str(gc_username)+' deleted successfully.'))
                with ProgressStdoutRedirection(gc_username):
                    print(('All DB data for user: ' + str(gc_username)+' deleted successfully.'))
                            
        
    
