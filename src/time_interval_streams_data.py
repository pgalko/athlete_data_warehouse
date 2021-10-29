
from datetime import datetime,timedelta
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify

@processify
def insert_intervals_min(ath_un,ath_un_id,db_host,db_name,superuser_un,superuser_pw,start_time,end_time): 

    intervals = []

    sql_insert_intervals = """

        INSERT INTO time_interval_min(athlete_id,timestamp_gmt)

        VALUES
        (%s,%s)

        ON CONFLICT (timestamp_gmt) DO NOTHING;
        
    """

    while start_time < end_time:
        intervals.append(datetime.strftime(start_time,"%Y-%m-%d %H:%M:%S"))
        start_time = start_time + timedelta(seconds=60)

    conn = None
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)
    # two-phase insert prepapre
    conn.tpc_begin(conn.xid(42, 'transaction ID', ath_un))
    
    with StdoutRedirection(ath_un):
        print('Creating and inserting 1min intervals from oldest data-point to present.')
    with ProgressStdoutRedirection(ath_un):
        print('Creating and inserting 1min intervals from oldest data-point to present.')
    cur = conn.cursor()
    for i in intervals:
        try:          
            cur.execute(sql_insert_intervals,(ath_un_id,i))
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e))) 
    cur.close()

    # two-phase insert commit or rollback
    try:
        conn.tpc_prepare()
    except  (Exception, psycopg2.DatabaseError) as e:
        conn.tpc_rollback()
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

    else:
        try:
            conn.tpc_commit()
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

def  update_intervals_range(ath_un,db_host,db_name,superuser_un,superuser_pw):
    sql_select_last_interval = '''
    SELECT timestamp_gmt 
    FROM time_interval_min
    ORDER BY timestamp_gmt DESC LIMIT 1;
    '''
    sql_select_oldest_record_gc = '''
    SELECT timestamp_gmt 
    FROM timezones
    ORDER BY timestamp_gmt ASC LIMIT 1;
    '''
    sql_select_oldest_record_strava = '''
    SELECT start_date 
    FROM strava_activity_summary
    ORDER BY start_date ASC LIMIT 1;
    '''
    sql_ath_un_id = '''
    SELECT id from athlete where ath_un=%s
    '''
    try:
        conn = None
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)
        #Select Athlete UN ID
        cur = conn.cursor()
        cur.execute(sql_ath_un_id,(ath_un,))
        ath_un_id = cur.fetchone()
        ath_un_id = str(ath_un_id[0])
        cur.close()
        #Start Time
        cur = conn.cursor()
        #If exists, retrieve latest record from time_interval_min table, and use it as a start_time
        cur.execute(sql_select_last_interval)
        start_time = cur.fetchone()
        cur.close()  
        #If there are no records in time_interval_min table, retrieve the oldest record from timezones table and use it as a start_time
        if start_time is None:
            cur = conn.cursor()
            cur.execute(sql_select_oldest_record_gc)
            start_time = cur.fetchone()
            cur.close()
            if start_time is not None:
                start_time = datetime.strptime(start_time[0],"%Y-%m-%d %H:%M:%S")
            #If there are no records in timezones table, retrieve the oldest record from strava_activities_summary table and use it as a start_time
            else:
                cur = conn.cursor()
                cur.execute(sql_select_oldest_record_strava)
                start_time = cur.fetchone()
                cur.close()
                if start_time is not None:
                    start_time = datetime.strptime(start_time[0],"%Y-%m-%d %H:%M:%S")
                else:
                    start_time = datetime.utcnow()
        else:
            start_time = datetime.strptime(start_time[0],"%Y-%m-%d %H:%M:%S")
    
        #End Time
        end_time = datetime.utcnow()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close

    insert_intervals_min(ath_un,ath_un_id,db_host,db_name,superuser_un,superuser_pw,start_time,end_time)  
        