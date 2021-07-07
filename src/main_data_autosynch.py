import sys
import datetime
import os
import psutil
from os import remove
import mfp_data_download_db_insert as mfp
import diasend_data_download_db_insert as cgm
import glimp_data_download_db_insert as glimp
import mind_monitor_data_download_db_insert as mm
import gc_data_download as gc
import oura_data_download as oura
import delete_data as clr
from db_create_user_database import check_user_db_exists
from db_user_insert import insert_last_synch_timestamp
from weather import get_weather
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
from database_ini_parser import config

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = str(path_params.get("pid_file_dir"))
DOWNLOAD_DIR = str(path_params.get("download_dir"))

def run_dwnld_functions(start_date, end_date, end_date_today, ath_un, gc_username, gc_password, mfp_username, mfp_password, cgm_username, cgm_password, glimp_export_link, libreview_export_link, mm_export_link,display_name, output, db_name, db_host, superuser_un, superuser_pw, dbx_auth_token,oura_refresh_token,auto_synch,encr_pass):
    if dbx_auth_token is not None:
        archive_to_dropbox = True
    else:
        archive_to_dropbox = False
    
    #Insert the current synch timestamp to db_info table
    insert_last_synch_timestamp(ath_un,encr_pass,db_name)
    
    #PG:Call to execute "parse and insert GC data" script
    if gc_username is not None:                
        gc_agent = gc.login(gc_username, gc_password)   
        gc.dwnld_insert_fit_activities(ath_un, gc_agent, gc_username, gc_password, mfp_username, start_date, end_date_today, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox, "archiveFiles", dbx_auth_token, auto_synch,encr_pass)
        gc.dwnld_insert_fit_wellness(ath_un, gc_agent,start_date,end_date,gc_username, gc_password, mfp_username, output,db_host,db_name,superuser_un,superuser_pw,archive_to_dropbox, "archiveFiles", dbx_auth_token,encr_pass)
        gc.dwnld_insert_json_body_composition(ath_un, gc_agent, start_date, end_date, gc_username, gc_password, mfp_username, output, db_host,db_name,superuser_un,superuser_pw, archive_to_dropbox, "archiveFiles", dbx_auth_token,encr_pass)
        gc.dwnld_insert_json_wellness(ath_un, gc_agent, start_date, end_date, gc_username, gc_password, mfp_username, display_name, output, db_host,db_name,superuser_un,superuser_pw, archive_to_dropbox, "archiveFiles", dbx_auth_token,encr_pass)
        gc.dwnld_insert_json_dailysummary(ath_un, gc_agent, start_date, end_date, gc_username, gc_password, mfp_username, display_name, output, db_host,db_name,superuser_un,superuser_pw, archive_to_dropbox, "archiveFiles", dbx_auth_token,encr_pass)

    #PG:Call to execute "parse and insert MFP data" script 
    if mfp_username is not None:   
        try:
            mfp.dwnld_insert_nutrition(mfp_username,mfp_password,ath_un,start_date,end_date,encr_pass,True,True,db_host,superuser_un,superuser_pw)
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    if cgm_username is not None:   
        try:
            cgm.diasend_data_export_insert(output,start_date,end_date_today,ath_un,cgm_username,cgm_password,encr_pass,True,archive_to_dropbox,"archiveFiles",dbx_auth_token,db_host,superuser_un,superuser_pw)
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    if glimp_export_link is not None:   
        try:
            glimp.glimp_data_insert(output,start_date,end_date_today,ath_un,encr_pass,glimp_export_link,True,db_host,db_name,superuser_un,superuser_pw) 
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    if libreview_export_link is not None:   
        try:
            glimp.glimp_data_insert(output,start_date,end_date_today,ath_un,encr_pass,libreview_export_link,True,db_host,db_name,superuser_un,superuser_pw) 
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    if mm_export_link is not None:   
        try: 
            mm.mm_data_insert(output,start_date,end_date_today,ath_un,encr_pass,mm_export_link,True,db_host,db_name,superuser_un,superuser_pw) 
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    if oura_refresh_token is not None:   
        try: 
            oura.dwnld_insert_oura_data(ath_un,db_host,db_name,superuser_un,superuser_pw,oura_refresh_token,start_date,end_date,True,encr_pass) 
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    try:
        get_weather(ath_un,db_host, db_name, superuser_un,superuser_pw,start_date,end_date_today,encr_pass)
    except Exception as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    
def auto_synch(ath_un, db_name, db_host, superuser_un, superuser_pw, gc_username,gc_password,mfp_username,mfp_password,cgm_username,cgm_password,glimp_export_link, libreview_export_link, mm_export_link, dbx_auth_token,oura_refresh_token,encr_pass):
    output = DOWNLOAD_DIR
    auto_synch = True

    # Get PID from PID file -> Write PID to file -> keep PID file while process running -> delete when failed or completed
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    if os.path.isfile(pidfile):
        #read PID from file
        with open(pidfile, "U") as f:
            pid_from_file = f.read()
        #check whether the PID from file is still running
        if psutil.pid_exists(int(pid_from_file)):
            with ProgressStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + " %s already exists, the previous execution of the task is still running... AutoSynch exiting!" % pidfile))
            return
        else:
            os.remove(pidfile)#Remove old PID file

    try:       
        # Get startdate enddate and displayname vars 
        start_date = datetime.datetime.today() - datetime.timedelta(days=2) #PG: start_day = one day before yesterday 
        end_date = datetime.datetime.today() - datetime.timedelta(days=1) #PG: end_date = yesterday
        end_date_today = datetime.datetime.today() #"PG: end_date_today = today
        text = ath_un
        head, sep, tail = text.partition('@')
        display_name = head
      
        #DATA DOWNLOAD ------------------------------
    
        #PG:Call to execute "parse and insert GC and MFP data" functions
        run_dwnld_functions(start_date, end_date, end_date_today, ath_un, gc_username, gc_password, mfp_username, mfp_password,cgm_username,cgm_password,glimp_export_link,libreview_export_link,mm_export_link, display_name, output, db_name, db_host, superuser_un, superuser_pw, dbx_auth_token, oura_refresh_token, auto_synch, encr_pass)
                    
    except Exception as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + " The Autosynch download/insert process has failed, deleting %s file. Please try to run the script again" % pidfile))
        os.unlink(pidfile)

    finally:
        if os.path.isfile(pidfile):
            os.unlink(pidfile)
        with ProgressStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + '---- AutoSynch for user: '+ath_un+' completed ----'))

    
