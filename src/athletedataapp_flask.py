#
# This module is loaded when web_app_loader_flask.py executes (calling create_app() function)
# It is to be used on WIN OS and the build-in Flask web server (use only for testing and development).
#

from flask import Flask,render_template,request,flash,session,redirect, url_for
import jwt
import datetime
import os
import time
import mfp_data_download_db_insert as mfp
import gc_data_download as gc
import delete_data as clr
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
import sys
from athlete_auth import ath_auth_register,ath_auth_login,ath_auth_reset
from db_create_user_database import create_user_db,restore_db_schema,check_user_db_exists,check_host_record_exists,backup_user_db,create_sample_db,check_db_server_connectivity
from db_user_insert import update_autosynch_prefrnc,user_tokens_insert,insert_last_synch_timestamp,gc_user_insert,check_user_exists
from db_dropbox import check_user_token_exists
from db_oura_auth import check_oura_token_exists
from db_strava_auth import check_strava_token_exists
from diasend_data_download_db_insert import diasend_data_export_insert
from glimp_data_download_db_insert import glimp_data_insert
from mind_monitor_data_download_db_insert import mm_data_insert
from cstm_data_download_db_insert import cstm_data_insert
from weather import get_weather
from time_interval_streams_data import update_intervals_range
from send_email import send_email
from oura_data_download import dwnld_insert_oura_data
from strava_data_download import dwnld_insert_strava_data
from db_auto_sync import retrieve_decrypt_creds
import psutil
import urllib.request, urllib.error, urllib.parse
from database_ini_parser import config
import dropbox
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
import psycopg2
from plotly_dashboard_1 import create_dashboard1
import Crypto.Random
from Crypto.Cipher import AES
import base64
from requests_oauthlib import OAuth2Session
                      
#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    #iv = Crypto.Random.get_random_bytes(AES.block_size)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt

def create_app(encr_pass_input,debug=False):												
    path_params = config(filename="encrypted_settings.ini", section="path")
    PID_FILE_DIR = str(path_params.get("pid_file_dir"))
    DOWNLOAD_DIR = str(path_params.get("download_dir"))
    TEMP_FILE_PATH = str(path_params.get("temp_file_path"))
    
    encr_pass = encr_pass_input

    dbx_params = config(filename="encrypted_settings.ini", section="dropbox",encr_pass=encr_pass)
    APP_KEY = str(dbx_params.get("app_key"))
    APP_SECRET = str(dbx_params.get("app_secret"))
    REDIRECT_URI = str(dbx_params.get("redirect_uri"))
    integrated_with_dropbox = str(dbx_params.get("integrated_with_dropbox"))

    oura_params = config(filename="encrypted_settings.ini", section="oura",encr_pass=encr_pass)
    OURA_CLIENT_ID = str(oura_params.get("oura_client_id"))
    OURA_CLIENT_SECRET = str(oura_params.get("oura_client_secret"))
    OURA_AUTH_URL = str(oura_params.get("oura_auth_url"))
    OURA_TOKEN_URL = str(oura_params.get("oura_token_url"))
    if OURA_CLIENT_ID == "":
        oura_enabled = False
    else:
        oura_enabled = True

    strava_params = config(filename="encrypted_settings.ini", section="strava",encr_pass=encr_pass)
    STRAVA_CLIENT_ID = str(strava_params.get("strava_client_id"))
    STRAVA_CLIENT_SECRET = str(strava_params.get("strava_client_secret"))
    STRAVA_AUTH_URL = str(strava_params.get("strava_auth_url"))
    STRAVA_TOKEN_URL = str(strava_params.get("strava_token_url"))
    STRAVA_REDIRECT_URI = str(strava_params.get("strava_redirect_uri"))
    if STRAVA_CLIENT_ID == "":
        strava_enabled = False
    else:
        strava_enabled = True

    anticaptcha_params = config(filename="encrypted_settings.ini", section="anticaptcha",encr_pass=encr_pass)
    anticaptcha_api_key = str(anticaptcha_params.get("api_key"))
    if anticaptcha_api_key == "":
        diasend_enabled = False
    else:
        diasend_enabled = True

    superset_params = config(filename="encrypted_settings.ini", section="superset", encr_pass=encr_pass)
    superset_installed = str(superset_params.get("superset"))
    superset_url = str(superset_params.get("url"))
    if superset_installed == 'true':
        superset_enabled = True
    else:
        superset_enabled = False

    pgweb_params = config(filename="encrypted_settings.ini", section="pgweb", encr_pass=encr_pass)
    pgweb_installed = str(pgweb_params.get("pgweb"))
    pgweb_smpl_url = str(pgweb_params.get("url_smpl"))
    pgweb_usr_url = str(pgweb_params.get("url_usr"))
    if pgweb_installed == 'true':
        pgweb_enabled = True
    else:
        pgweb_enabled = False

    def get_dropbox_auth_flow(session):
        return dropbox.oauth.DropboxOAuth2Flow(
            APP_KEY, REDIRECT_URI, session, "athletedataapp_dropbox-auth-csrf-token", APP_SECRET,token_access_type="offline")

    # URL handler for /dropbox-auth-finish
    def dropbox_auth_finish(session,request):
        try:
            auth_result = get_dropbox_auth_flow(session).finish(request.args)
            refresh_token = auth_result.refresh_token
        except Exception as e:
            with ConsolidatedProgressStdoutRedirection():
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
        return refresh_token

    app = Flask(__name__)
    app_params = config(filename="encrypted_settings.ini", section="app",encr_pass=encr_pass)
    app.secret_key = str(app_params.get("secret_key"))
    send_emails = str(app_params.get("send_emails"))
    admin_email = str(app_params.get("admin_email"))


    @app.route('/', methods = ['GET','POST'])
    def index():
        
        gc_username = None
        gc_password = None
        mfp_username = None
        mfp_password = None
        diasend_username =  None
        diasend_password = None
        glimp_export_link = None
        mm_export_link = None
        cstm_str_params = []
        cstm_int_params = []
        cstm_export_link = None
        cstm_tab_name = None
        cstm_dt_column = None
        cstm_timezone = None
        cstm_date_format = None
        cstm_unique_columns = None
        output =None
        start_date = None
        end_date = None
        end_date_today =None
        del_progress = None
        mfp_progress = None
        diasend_progress = None
        glimp_progress = None
        mm_progress = None
        cstm_progress = None
        gc_login_progress = None
        gc_fit_activ_progress = None
        strava_activ_progress = None
        gc_tcx_activ_progress = None
        gc_fit_well_progress = None
        oura_well_progress = None
        gc_json_well_progress = None
        gc_json_dailysum_progress = None
        progress_error = False
        archive_to_dropbox = False
        archive_radio = None
        dbx_auth_token = session.get('dbx_auth_token',None)
        oura_refresh_token = session.get('oura_refresh_token',None)
        strava_refresh_token = session.get('strava_refresh_token',None)
        signin_valid = session.get('signin_valid',None)
        ath_pw = session.get('ath_pw',None)
        ath_un = signin_valid
        auto_synch = False

        output = DOWNLOAD_DIR
            
                    
        if request.method == 'POST':

            #----GC Login variables----
            if request.form.get('GCCheckbox') is not None or request.form.get('wellnessCheckbox') is not None:
                gc_username = str(request.form.get('gcUN'))
                gc_password = str(request.form.get('gcPW'))

                        
            #----Destination DB variables-----
            db_name = str(str2md5(ath_un)) + '_Athlete_Data_DB'
            
            #If user  wishes to download to his db, credentials to be provided and retrieved from the form.
            data_destination = request.form.get('dbSvr')
            if data_destination == 'remoteDbSvr':
                superuser_un = str(request.form.get('dbUser'))
                superuser_pw = str(request.form.get('dbPass'))
                encrypted_superuser_pw = base64.b64encode(encrypt(superuser_pw, encr_pass))
                encrypted_superuser_pw = encrypted_superuser_pw.decode('utf-8')
                db_host = str(request.form.get('dbHost'))
                #Test Connectivity to user db
                connection = check_db_server_connectivity(ath_un,db_host,superuser_un,superuser_pw)
                if connection != 'SUCCESS':
                    flash('  Could cot connect to the DB Host.The host returned an error:  '+connection,'danger')
                    return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
            else:
                #If user does not wish to download to his db, credentials to be retrieved from .ini.
                params = config(filename="encrypted_settings.ini", section="postgresql",encr_pass=encr_pass)
                superuser_un = params.get("user")
                superuser_pw = params.get("password")
                encrypted_superuser_pw = base64.b64encode(encrypt(superuser_pw, encr_pass))
                encrypted_superuser_pw = encrypted_superuser_pw.decode('utf-8')
                db_host = params.get("host")

            #Check if the user has a DB recorded in the info_db. If yes, stop execution and show warning message, otherwise proceed
            host_record_exists = check_host_record_exists(ath_un,db_name,db_host,encr_pass)
            if host_record_exists == True:
                flash('  You can only download to one db host. Please correct the db_hostname and try again','warning')
                return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)

            #----Check if the provided GC credentials are valid-----
            #gc_cred_valid = gc.check_gc_creds(gc_username,gc_password)
            #if gc_cred_valid == False:
                #flash('  The Garmin Connect login credentials are not valid. Please try again','warning')
                #return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)

            #----- Set Auto_Synch variables--------

            if request.form.get('AutoSynchCheckbox') is not None:
                auto_synch_checkbox = True
                save_pwd = True
            else:
                auto_synch_checkbox = False 
                save_pwd = False

            #-----Check if the user DB already exists----

            db_exists = check_user_db_exists(ath_un,db_host,superuser_un,superuser_pw)

            #----PID File check to prevent concurrent executions for the same user-----

            pidfile = PID_FILE_DIR + ath_un + '_PID.txt'

            if os.path.isfile(pidfile):
                #read PID from file
                with open(pidfile, "U") as f:
                    pid_from_file = f.read()
                #check whether the PID from file is still running
                if psutil.pid_exists(int(pid_from_file)):
                    with ProgressStdoutRedirection(ath_un):
                        print(str(datetime.datetime.now()) + "  %s already exists, the previous execution of the task is still running... Web App exiting!" % pidfile)
                    continue_btn = 'none'
                    user=ath_un
                    flash('  The previous execution of the task for: ' +user+ ' is still running... You can check the status below.','danger')
                    return redirect(url_for('process_running',user=user)) 
                else:
                    os.remove(pidfile)#Remove old PID file
                
            
            #-----MFP Login variables------        
            if request.form.get('MFPCheckbox') is not None:
                mfp_username = str(request.form.get('mfpUN'))
                mfp_password = str(request.form.get('mfpPW'))
                    
            #-----Diasend Login variables------        
            if request.form.get('diasendCheckbox') is not None:
                diasend_username = str(request.form.get('diasendUN'))
                diasend_password = str(request.form.get('diasendPW'))
            
            #-----Link to Glimp export file------
            if request.form.get('glimpCheckbox') is not None:
                glimp_export_link = str(request.form.get('GlimpExportLink'))
                
            #-----Link to Mind Monitor export folder------
            if request.form.get('mmCheckbox') is not None:
                mm_export_link = str(request.form.get('mmExportLink'))

            #-----Cstm STR and INT params-----
            if request.form.get('cstmCheckbox') is not None:
                cstm_export_link = request.form.get('cstmExportLink')
                cstm_tab_name = request.form.get('cstmTabName')
                cstm_dt_column = request.form.get('cstmDTColumn')
                if cstm_dt_column == 'None':
                    cstm_dt_column = None
                cstm_timezone = request.form.get('cstmTimeZone')
                cstm_date_format = request.form.get('cstmDateFormat')
                cstm_unique_columns = request.form.getlist('cstmUniqueColumns')
                cstm_output = os.path.join(output,ath_un)
                cstm_str_params.extend([cstm_export_link,cstm_output,cstm_tab_name,cstm_date_format,cstm_timezone,cstm_dt_column])
                cstm_int_params.extend([int(i) for i in cstm_unique_columns])

            #----Check for and Retrieve Dropbox token----   
            if request.form.get('archiveDataCheckbox') is not None:
                archive_radio = request.form.get('archiveData')
                if dbx_auth_token is None:       
                    if db_exists == True:
                        dbx_token_exists, dbx_token_from_db = check_user_token_exists(ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass) 
                        if dbx_token_exists == True: # token exists in database and it is not None
                            dbx_auth_token = dbx_token_from_db    
                            archive_to_dropbox = True
                        else:
                            return redirect(url_for('dropbox_auth_request'))
                    else:
                        return redirect(url_for('dropbox_auth_request'))                
                else:
                    archive_to_dropbox = True

            #----Check for and Retrieve Oura token----
            if request.form.get('ouraCheckbox') is not None:
                if oura_refresh_token is None:     
                    if db_exists == True:
                        oura_token_exists, oura_token_from_db = check_oura_token_exists(ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                        if oura_token_exists == True: # token exists in database and it is not None
                            oura_refresh_token = oura_token_from_db
                            print('Refresh Token: {}'.format(oura_refresh_token))
                        else:
                            return redirect(url_for('oura_auth_request'))
                    else:
                        return redirect(url_for('oura_auth_request'))

            #----Check for and Retrieve Strava token----
            if request.form.get('stravaCheckbox') is not None:
                if strava_refresh_token is None:     
                    if db_exists == True:
                        strava_token_exists, strava_token_from_db = check_strava_token_exists(ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                        if strava_token_exists == True: # token exists in database and it is not None
                            strava_refresh_token = strava_token_from_db
                            print('Refresh Token: {}'.format(strava_refresh_token))
                        else:
                            return redirect(url_for('strava_auth_request'))
                    else:
                        return redirect(url_for('strava_auth_request'))

            # CLEANUP BEFORE DOWNLOAD -----------------   
                    
            #----Delete Files and DB Data variables----
            try:            
                if request.form.get('dataDeleteCheckbox') is not None:
                    clearall_radio = request.form.get('deleteData')      
                    if db_exists == True:
                        if clearall_radio == 'deleteAllData':
                            try:
                                del_progress = 'Delete started'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                clr.delete_all_files(output, ath_un)  
                                clr.delete_all_db_data(ath_un,mfp_username,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                                del_progress = 'All data deleted succesfully'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(del_progress)
                            except:
                                del_progress = 'Error deleting data'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + del_progress))
                        elif clearall_radio == 'deleteFiles':
                            try:
                                del_progress = 'Delete started'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                clr.delete_all_files(output, ath_un)
                                del_progress = 'All data deleted succesfully'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(del_progress)
                            except:
                                del_progress = 'Error deleting data'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + del_progress))
                        elif clearall_radio == 'deleteDBdata':
                            try:
                                del_progress = 'Delete started'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                clr.delete_all_db_data(ath_un,mfp_username,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                                del_progress = 'All data deleted succesfully'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(del_progress)
                            except:
                                del_progress = 'Error deleting data'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + del_progress))
                        elif clearall_radio == 'deleteAlldataExit':
                            try:
                                del_progress = 'Delete started'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                clr.delete_all_files(output, ath_un)
                                clr.delete_all_db_data(ath_un,mfp_username,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                                del_progress = 'All data deleted succesfully'
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(del_progress)
                                return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,del_progress=del_progress,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
                            except:
                                del_progress = 'Error deleting data'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(del_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + del_progress))
                                return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,del_progress=del_progress,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
                        

                #----Check and set start_date and end_date variables and proceed with download----
                try:
                    start_date = datetime.datetime.strptime((request.form.get('startDate')), "%Y-%m-%d")
                    text = ath_un
                    head, sep, tail = text.partition('@')
                    display_name = head
                    #user provided end_date 
                    if request.form.get('endDate') != "": 
                        end_date = datetime.datetime.strptime((request.form.get('endDate')), "%Y-%m-%d")
                        if end_date >= datetime.datetime.today(): #user input is greater or eq today
                            end_date = datetime.datetime.today() - datetime.timedelta(days=1) #yesterday
                            end_date_today = datetime.datetime.today()  #today
                        else:
                            end_date_today = end_date
                    #user did not provide end_date
                    else:
                        end_date = datetime.datetime.today() - datetime.timedelta(days=1)#yesterday
                        end_date_today = datetime.datetime.today()  #today
                except Exception as e:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #PG:If start date not provided render index and flash warning   
                    flash('  Please provide a valid start date and try again!','danger')
                    return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)

                # DATA DOWNLOAD -------------------------------------- 
                                       
                if ath_un is not None:    
                    if db_exists == True:
                        # PG: Insert user details into postgreSQL
                        user_tokens_insert(ath_un,db_host,db_name,superuser_un,superuser_pw,dbx_auth_token,oura_refresh_token,strava_refresh_token,encr_pass,save_pwd)
                        insert_last_synch_timestamp(ath_un,encr_pass,db_name)
                        update_autosynch_prefrnc(ath_un,db_host,db_name,superuser_un,superuser_pw,encrypted_superuser_pw,auto_synch_checkbox,encr_pass)  #----Set Auto_Synch switch----
                    else:
                        create_user_db(ath_un,ath_pw,db_host,db_name,superuser_un,superuser_pw,encrypted_superuser_pw,save_pwd,encr_pass)
                        restore_db_schema(ath_un,db_host,db_name,superuser_un,superuser_pw)
                        user_tokens_insert(ath_un,db_host,db_name,superuser_un,superuser_pw,dbx_auth_token,oura_refresh_token,strava_refresh_token,encr_pass,save_pwd)
                        insert_last_synch_timestamp(ath_un,encr_pass,db_name)
                        update_autosynch_prefrnc(ath_un,db_host,db_name,superuser_un,superuser_pw,encrypted_superuser_pw,auto_synch_checkbox,encr_pass)  #----Set Auto_Synch switch----
                    session['oura_refresh_token'] = None
                    session['strava_refresh_token'] = None

                    #---------------------------------- GC Login ---------------------------------------   

                    if gc_username is not None:
                        #PG:Call to execute "GC login" script
                        try:        
                            gc_agent = gc.login(gc_username, gc_password)
                            if gc_agent is not None: 
                                gc_login_progress = 'Login to GC successfull'
                                gc_user_insert(ath_un,gc_username, gc_password, db_host,db_name,superuser_un,superuser_pw,encr_pass,save_pwd)
                                with StdoutRedirection(ath_un):
                                    print(gc_login_progress)
                                with ProgressStdoutRedirection(ath_un):
                                    print(gc_login_progress)
                            else:
                                raise Exception('There was a problem logging in to Garmin Connect.')                                
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            gc_login_progress = 'GC login error.Check UN and PW'
                            progress_error = True
                            with StdoutRedirection(ath_un):
                                print(gc_login_progress)
                            flash('  There was a problem logging in to Garmin Connect. The script will now continue, but will skip the Garmin data. Please try again later','warning')
                            #return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)

                        #---------------------------------- GC Activities ---------------------------------------
                        
                        #PG:Call to execute "Parse and insert FIT activities" script
                        if request.form.get('GCCheckbox') is not None:
                            try:
                                gc_fit_activ_progress = 'GC FIT activities download started'
                                with StdoutRedirection(ath_un):
                                    print(gc_fit_activ_progress)
                                time.sleep(1)        
                                gc.dwnld_insert_fit_activities(ath_un, gc_agent, gc_username, gc_password, mfp_username, start_date, end_date_today, output, db_host, db_name, superuser_un,superuser_pw,archive_to_dropbox,archive_radio,dbx_auth_token, auto_synch,encr_pass)
                                gc_fit_activ_progress = 'GC FIT activities downloaded successfully'
                                with StdoutRedirection(ath_un):
                                    print(gc_fit_activ_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(gc_fit_activ_progress) 
                            except Exception as e:
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                                gc_fit_activ_progress = 'Error downloading GC FIT activities'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(gc_fit_activ_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + gc_fit_activ_progress))
                            
                        #----------------------------------  Wellness  ----------------------------------------
                        
                        #PG:Call to execute "Parse and insert FIT wellness data" script
                        if request.form.get('wellnessCheckbox') is not None:
                            try:
                                gc_fit_well_progress = 'GC FIT wellness download started'
                                with StdoutRedirection(ath_un):
                                    print(gc_fit_well_progress)
                                time.sleep(1)        
                                gc.dwnld_insert_fit_wellness(ath_un, gc_agent,start_date,end_date_today,gc_username, gc_password, mfp_username, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox,archive_radio,dbx_auth_token,encr_pass)
                                gc_fit_well_progress = 'GC FIT wellness data downloaded successfully'
                                with StdoutRedirection(ath_un):
                                    print(gc_fit_well_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(gc_fit_well_progress) 
                            except Exception as e:
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                                gc_fit_well_progress = 'Error downloading GC FIT wellness data'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(gc_fit_well_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + gc_fit_well_progress))

                            #PG:Call to execute "Parse and insert JSON wellness data" script
                            try:
                                gc_json_well_progress = 'GC JSON wellness download started'
                                with StdoutRedirection(ath_un):
                                    print(gc_json_well_progress)
                                time.sleep(1)                
                                gc.dwnld_insert_json_wellness(ath_un, gc_agent, start_date, end_date_today, gc_username, gc_password, mfp_username, display_name, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox,archive_radio,dbx_auth_token,encr_pass)
                                gc.dwnld_insert_json_body_composition(ath_un, gc_agent, start_date, end_date_today, gc_username, gc_password, mfp_username, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox, archive_radio, dbx_auth_token,encr_pass)
                                gc_json_well_progress = 'GC JSON wellness data downloaded successfully'
                                with StdoutRedirection(ath_un):
                                    print(gc_json_well_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(gc_json_well_progress) 
                            except Exception as e:
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                                gc_json_well_progress = 'Error downloading GC JSON wellness data'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(gc_json_well_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + gc_json_well_progress))

                            #PG:Call to execute "Parse and insert JSON Daily summary data" script
                            try:
                                gc_json_dailysum_progress = 'GC JSON daily summary download started'
                                with StdoutRedirection(ath_un):
                                    print(gc_json_dailysum_progress)
                                time.sleep(1)        
                                gc.dwnld_insert_json_dailysummary(ath_un,gc_agent, start_date, end_date_today, gc_username, gc_password, mfp_username, display_name, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox,archive_radio,dbx_auth_token,encr_pass)
                                gc_json_dailysum_progress = 'GC JSON daily summary data downloaded successfully'
                                with StdoutRedirection(ath_un):
                                    print(gc_json_dailysum_progress)
                                time.sleep(1)
                                with ProgressStdoutRedirection(ath_un):
                                    print(gc_json_dailysum_progress) 
                            except Exception as e:
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                                gc_json_dailysum_progress = 'Error downloading GC JSON daily summary'
                                progress_error = True
                                with StdoutRedirection(ath_un):
                                    print(gc_json_dailysum_progress)
                                time.sleep(1)
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + gc_json_dailysum_progress)) 
                     
                    #PG:Call to execute "Parse and insert Oura wellness data" script 
                    if request.form.get('ouraCheckbox') is not None:
                        try:
                            oura_well_progress = 'Oura wellness download started'
                            with StdoutRedirection(ath_un):
                                print(oura_well_progress)
                            time.sleep(1)        
                            dwnld_insert_oura_data(ath_un,db_host,db_name,superuser_un,superuser_pw,oura_refresh_token,start_date,end_date,save_pwd,encr_pass)
                            oura_well_progress = 'Oura wellness data downloaded successfully'
                            with StdoutRedirection(ath_un):
                                print(oura_well_progress)
                            time.sleep(1)
                            with ProgressStdoutRedirection(ath_un):
                                print(oura_well_progress) 
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            oura_well_progress = 'Error downloading Oura wellness data'
                            progress_error = True
                            with StdoutRedirection(ath_un):
                                print(oura_well_progress)
                            time.sleep(1)
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + oura_well_progress))

                    #----------------- Nutrition MFP ---------------------------    
                    #PG:Call to execute "parse and insert MFP data" script
                    if mfp_username is not None:   
                        try:
                            mfp_progress = 'MFP download started'
                            with StdoutRedirection(ath_un):
                                print(mfp_progress)
                            time.sleep(1)
                            mfp.dwnld_insert_nutrition(mfp_username,mfp_password,ath_un,start_date,end_date_today,encr_pass,save_pwd,auto_synch,db_host,superuser_un,superuser_pw)
                            mfp_progress = 'MFP nutrition data downloaded successfully'
                            with StdoutRedirection(ath_un):
                                print(mfp_progress)
                            time.sleep(1)
                            with ProgressStdoutRedirection(ath_un):
                                print(mfp_progress)
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            mfp_progress = 'Error downloading MFP nutrition data'
                            with StdoutRedirection(ath_un):
                                print(mfp_progress)
                            time.sleep(1)
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + mfp_progress))
                    
                    #-------------------- BG Diasend --------------------------            
                    #PG:Call to execute "parse and insert Diasend data" script
                    if diasend_username is not None:   
                        try:
                            diasend_progress = 'Diasend CGM download started'
                            with StdoutRedirection(ath_un):
                                print(diasend_progress)
                            time.sleep(1)
                            diasend_data_export_insert(output,start_date,end_date_today,ath_un,diasend_username,diasend_password,encr_pass,save_pwd,archive_to_dropbox,archive_radio,dbx_auth_token,db_host,superuser_un,superuser_pw)
                            diasend_progress = 'Diasend CGM data downloaded successfully'
                            with StdoutRedirection(ath_un):
                                print(diasend_progress)
                            time.sleep(1)
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            diasend_progress = 'Error downloading Diasend GCM data'
                            with StdoutRedirection(ath_un):
                                print(diasend_progress)
                            time.sleep(1)
                            
                    #------------------ BG Glimp --------------------------        
                    #PG:Call to execute "parse and insert Glimp data" script
                    if glimp_export_link is not None:
                        try:
                            glimp_progress = 'Glimp CGM download started'
                            with StdoutRedirection(ath_un):
                                print(glimp_progress)
                            time.sleep(1)
                            glimp_data_insert(output,start_date,end_date_today,ath_un,encr_pass,glimp_export_link,save_pwd,db_host,db_name,superuser_un,superuser_pw)
                            glimp_progress = 'Glimp CGM data downloaded successfully'
                            with StdoutRedirection(ath_un):
                                print(glimp_progress)
                            time.sleep(1)
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            glimp_progress = 'Error downloading Glimp CGM data'
                            with StdoutRedirection(ath_un):
                                print(glimp_progress)
                            time.sleep(1)

                    #------------------ EEG Mind Monitor --------------------------
                    #PG:Call to execute "parse and insert MM data" script
                    if mm_export_link is not None:
                        try:
                            mm_progress = 'Mind Monitor download started'
                            with StdoutRedirection(ath_un):
                                print(mm_progress)
                            time.sleep(1)
                            mm_data_insert(output,start_date,end_date_today,ath_un,encr_pass,mm_export_link,save_pwd,db_host,db_name,superuser_un,superuser_pw)
                            mm_progress = 'Mind Monitor data downloaded successfully'
                            with StdoutRedirection(ath_un):
                                print(mm_progress)
                            time.sleep(1)
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            mm_progress = 'Error downloading Mind Monitor data'
                            with StdoutRedirection(ath_un):
                                print(mm_progress)
                            time.sleep(1)
                    
                    #------------------ CSTM Data from csv --------------------------
                    #PG:Call to execute "parse and insert CSTM csv data" script
                    if cstm_export_link is not None:
                        try:
                            cstm_progress = 'Custom data download started'
                            with StdoutRedirection(ath_un):
                                print(cstm_progress)
                            time.sleep(1)
                            cstm_data_insert(ath_un,cstm_str_params,cstm_int_params,db_host,superuser_un,superuser_pw)
                            cstm_progress = 'Custom data downloaded successfully'
                            with StdoutRedirection(ath_un):
                                print(cstm_progress)
                            time.sleep(1)
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            cstm_progress = 'Error downloading custom data'
                            with StdoutRedirection(ath_un):
                                print(cstm_progress)
                            time.sleep(1)
                
                    #----------------------- Activities Strava (Beacause of API limits, can be slow with larger downloads)----------------------
                    
                    #PG:Call to execute "Parse and insert Strava activity data" script 
                    if request.form.get('stravaCheckbox') is not None:
                        try:
                            strava_activ_progress = 'Strava activity download started'
                            with StdoutRedirection(ath_un):
                                print(strava_activ_progress)
                            time.sleep(1)        
                            dwnld_insert_strava_data(ath_un,db_host,db_name,superuser_un,superuser_pw,strava_refresh_token,start_date,end_date_today,save_pwd,encr_pass)
                            strava_activ_progress = 'Strava activity data downloaded successfully'
                            with StdoutRedirection(ath_un):
                                print(strava_activ_progress)
                            time.sleep(1)
                            with ProgressStdoutRedirection(ath_un):
                                print(strava_activ_progress) 
                        except Exception as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            strava_activ_progress = 'Error downloading Strava activity data'
                            progress_error = True
                            with StdoutRedirection(ath_un):
                                print(strava_activ_progress)
                            time.sleep(1)
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + strava_activ_progress))

                    #--------------- Weather --------------
                    #PG:Call to execute "retrieve and insert weather/meteostat data" script
                    try:
                        get_weather(ath_un,db_host, db_name, superuser_un,superuser_pw,start_date,end_date_today,encr_pass)
                    except Exception as e:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

                    #---------------------- Generate Time intervals, and populate "time_interval_min" table -------------------------

                    #PG:Call to execute "update intervals range" script
                    try:
                        flash('  The data download has completed. Setting up and updating the db views. This process might take a while.','info')
                        update_intervals_range(ath_un,db_host,db_name,superuser_un,superuser_pw)
                    except Exception as e:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))    

                    #------Archive DB to Dropbox-------
                    try:
                        if archive_to_dropbox == True:
                            if archive_radio == "archiveAllData" or archive_radio == "archiveDBdata":
                                backup_user_db(db_name,ath_un,output,dbx_auth_token,encr_pass)
                    except Exception as e:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                        pass       
                
                if progress_error is True:
                    error_log_entry = 'With Errors'
                    continue_btn = 'no_delete'
                    flash('  There was a problem downloading or processing the data. When you choose "Continue" the app will check the data integrity and it will pick up where it left off, skipping the already downloaded and processed data.','danger')
                    if send_emails == 'true':
                        send_email(
                            encr_pass,
                            'The athlete data download has failed',
                            'There was a problem downloading or processing the data.Please start the download process again. The app will check the data integrity and it will pick up where it left off, skipping the already downloaded and processed data.',
                            None,
                            ath_un
                        )
            
                else:
                    error_log_entry = 'Successfully'
                    continue_btn = 'none'
                    flash('  The download and insert of your data has been successfully completed.','success')
                    if send_emails == 'true':
                        send_email(
                            encr_pass,
                            'The athlete data download has completed successfully',
                            'The athlete data download has completed successfully',
                            None,
                            ath_un
                        ) 


                with ErrorStdoutRedirection(ath_un):
                    print(('--------------- ' + str(datetime.datetime.now()) + '  User ' + ath_un + '  Finished Data Download ' + error_log_entry +' -------------' ))
                with ProgressStdoutRedirection(ath_un):
                    print(('--------------- ' + str(datetime.datetime.now()) + '  User ' + ath_un + '  Finished Data Download ' + error_log_entry +' -------------' ))

                return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,del_progress = del_progress,mfp_progress = mfp_progress,diasend_progress = diasend_progress,
                                        glimp_progress = glimp_progress, mm_progress = mm_progress, cstm_progress = cstm_progress, gc_login_progress = gc_login_progress,gc_fit_activ_progress = gc_fit_activ_progress,
                                        gc_tcx_activ_progress = gc_tcx_activ_progress,gc_fit_well_progress = gc_fit_well_progress, gc_json_well_progress = gc_json_well_progress,
                                        gc_json_dailysum_progress = gc_json_dailysum_progress, oura_well_progress = oura_well_progress, strava_activ_progress=strava_activ_progress,
                                        progress_error = progress_error, continue_btn = continue_btn,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,
                                        diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled
                                        )
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                os.unlink(pidfile)

            finally:
                if os.path.isfile(pidfile):
                    os.unlink(pidfile)

        else: # Request method is GET
            continue_btn = request.args.get('continue_btn')
            return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,continue_btn = continue_btn,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
    
    @app.route("/ath_register", methods = ['GET', 'POST'])
    def ath_register():
        ath_un = str(request.form.get('athUsernameReg'))
        ath_pw = str(request.form.get('athPasswordReg'))
        signin_valid = ath_auth_register(ath_un,ath_pw,encr_pass)

        if signin_valid == ath_un:
            session['signin_valid'] = signin_valid
            session['ath_pw'] = ath_pw
            flash('  Account created successfuly. You are now logged-in','success')
            return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
        else:
            flash('  An account with this email address already exists','danger')
            return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
    
    @app.route("/ath_login", methods = ['GET', 'POST'])
    def ath_login():
        ath_un = str(request.form.get('athUsernameLogin'))
        ath_pw = str(request.form.get('athPasswordLogin'))
        signin_valid = ath_auth_login(ath_un,ath_pw,encr_pass)

        if signin_valid == ath_un:
            session['signin_valid'] = signin_valid
            session['ath_pw'] = ath_pw
            flash('  Login successfull.','success')
            return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
        else:
            flash('  Login failed, please try again.','danger')
            return render_template("index.html",superset_enabled=superset_enabled,superset_url=superset_url,pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,signin_valid=signin_valid,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled,oura_enabled=oura_enabled,strava_enabled=strava_enabled)
    
    @app.route("/ath_logout", methods = ['GET', 'POST'])
    def ath_logout():
        if 'signin_valid' in session:
            session['signin_valid'] = None
        return redirect(url_for('index'))

    @app.route("/ath_superset", methods = ['GET', 'POST'])
    def superset_login_request():
        superset_params = config(filename="encrypted_settings.ini", section="superset", encr_pass=encr_pass)
        superset_url = str(superset_params.get("url"))
        if request.args.get('user') == 'user':
            if 'signin_valid' not in session:#User not logged in
                flash('  You need to be logged in to access this link.','danger')
            else:
                ath_un = session['signin_valid']
                user_exists = check_user_exists(ath_un,encr_pass)
                if not user_exists:
                    flash('  This email address does not exist in the superset database.','danger')
                    return redirect(url_for('index'))
                else:
                    usr_token = jwt.encode({'ath_un': ath_un,'exp': time.time() + 10},key=app.secret_key, algorithm="HS256")
                    if type(usr_token) != str:
                        usr_token = usr_token.decode('UTF-8')
                    return redirect(superset_url+ 'login?username={}'.format(usr_token))
        else:#Sample User
            ath_un = 'sample_user'
            usr_token = jwt.encode({'ath_un': ath_un,'exp': time.time() + 10},key=app.secret_key, algorithm="HS256")
            if type(usr_token) != str:
                usr_token = usr_token.decode('UTF-8')
            return redirect(superset_url+ 'login?username={}'.format(usr_token))

    @app.route("/ath_reset_password", methods = ['GET', 'POST'])
    def reset_request():
        ath_un = str(request.form.get('athUserReset'))
        if 'signin_valid' not in session:
            session['signin_valid'] = None
        if ath_un == session['signin_valid']:#User already logged in
            #Log the user out
            session['signin_valid'] = None
            return redirect(url_for('index'))
        else:
            user_exists = check_user_exists(ath_un,encr_pass)
            if not user_exists:
                flash('  The submited email address does not exist in the database.','danger')
                return redirect(url_for('index'))
            else:
                password_reset_token = jwt.encode({'reset_password': ath_un,'exp': time.time() + 300},key=app.secret_key, algorithm="HS256")
                #Check whether the token is of type string, and decode if not.
                if type(password_reset_token) != str:
                    password_reset_token = password_reset_token.decode('UTF-8')
                if send_emails == 'true':
                    send_email(
                        encr_pass,
                        'athletedata.net password reset link',
                        'You can reset your athletedata.net login password here: ' + str(request.host_url)+ 'password_reset_verified/'+password_reset_token, 
                        None,
                        ath_un
                    )
                flash('  The password reset link has been sent to your email.','success')
                return redirect(url_for('index'))
    
    @app.route('/password_reset_verified/<password_reset_token>', methods=['GET', 'POST'])
    def reset_verified(password_reset_token):
        try:
            #Decode and retrieve ath_un from the link
            ath_un = jwt.decode(password_reset_token, key=app.secret_key, algorithms="HS256")['reset_password']
            if not ath_un:
                flash('  Something went wrong. Please request a new password reset link.','danger')
                return redirect(url_for('index'))
        except:
            #Token expired
            jwt.exceptions.ExpiredSignatureError
            flash('  You used an expired password reset link. Please request a new one.','danger')
            return redirect(url_for('index')) 

        new_password = request.form.get('newPwd')
        if new_password:
            #Log user in
            session['signin_valid'] = ath_un
            session['ath_pw'] = new_password
            #Save the new password in db
            ath_auth_reset(ath_un,new_password,encr_pass)
            flash('  Password reset successfull. You are now logged in with the new password','success')
            return redirect(url_for('index'))
        return render_template('reset_verified.html',admin_email=admin_email)
 
        
    @app.route("/datamodel_preview")
    def datamodel_preview():
        return render_template('datamodel_preview.html')

    @app.route("/db_info", methods=['GET', 'POST'])
    def db_info():
        password_info = '\"Your login password\"'
        metadata = None
        host_param = request.args.get('dbhost')
        
        if 'signin_valid' in session:
            user = session['signin_valid']
            text = user
            head, sep, tail = text.partition('@')
            db_username = head
            db_info = str(str2md5(user)) + '_Athlete_Data_DB'
            
            # Check if the sample DB exists, and create it if it does not.
            create_sample_db(encr_pass)

            conn = None
            # read DB connection parameters from ini file
            params = config(filename="encrypted_settings.ini", section="postgresql",encr_pass=encr_pass)
            # read pgweb parameters from ini file
            pgweb_params = config(filename="encrypted_settings.ini", section="pgweb",encr_pass=encr_pass)
            #Connection params for 'sample_db' DB.
            sample_db_host = params.get("sample_db_host")
            sample_db_port = params.get("sample_db_port")
            if sample_db_port == "":
                sample_db_port == "5432"
            sample_db = params.get("sample_db")
            ro_user = params.get("ro_user")
            ro_password = params.get("ro_password")
            #Connection params for 'db_info' DB.
            postgres_host = params.get("host")
            postgres_db = params.get("database")
            postgres_un = params.get("user")
            postgres_pw = params.get("password")
            postgres_host = params.get("host")
            #pgweb params
            pgweb_installed = pgweb_params.get("pgweb")
            pgweb_smpl_url = pgweb_params.get("url_smpl")
            pgweb_usr_url = pgweb_params.get("url_usr")

            if pgweb_installed == 'true':
                pgweb_enabled = True
            else:
                pgweb_enabled = False

            # connect to the PostgreSQL server (sample_db)
            conn = psycopg2.connect(dbname=sample_db, user=ro_user, password=ro_password, host=sample_db_host, port=sample_db_port)
            conn_postgres = psycopg2.connect(dbname=postgres_db, user=postgres_un, password=postgres_pw, host=postgres_host)

            sql = """
            SELECT table_name,column_name,data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name;  
            """
            sql_last_synch = """
            SELECT last_synch,db_auto_synch,db_host 
            FROM db_info 
            WHERE ath_un=%s;
            """

            try:
                cur = conn.cursor()
                cur.execute(sql,())
                conn.commit()
                metadata = cur.fetchall()
                cur.close
                
                cur = conn_postgres.cursor()
                cur.execute(sql_last_synch,(user,))
                conn_postgres.commit()
                result = cur.fetchone()
                last_synch = result[0]
                auto_synch_enabled = result[1]
                db_host_from_db = result[2]
                cur.close

            except  (Exception, psycopg2.DatabaseError) as error:
                with ErrorStdoutRedirection(user):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
            finally:
                if conn is not None:
                    conn.close()
                if conn_postgres is not None:
                    conn_postgres.close()

            #Get hostname/IP address
            if host_param is not None:#refered from index.html
                if host_param =='':# Local DB host
                    try:
                        host_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
                    except:
                        text = request.host
                        head, sep, tail = text.partition(':')
                        host_ip = head
                else:# Remote DB host
                    host_ip = host_param
            else:#rendered after Data Re-Synch
                if db_host_from_db == 'localhost':
                    try:
                        host_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
                    except:
                        text = request.host
                        head, sep, tail = text.partition(':')
                        host_ip = head
                else:
                    host_ip = db_host_from_db

            if request.method == 'POST':
                synch_req_db_list = []
                synch_req_db_list.append((db_info,))
                full_synch=True
                retrieve_decrypt_creds(synch_req_db_list,encr_pass,full_synch)
                flash('  The data re-synch has finished successfully.','success')
                return render_template('db_info.html',pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,db_info=db_info,ath_un=user,db_username=db_username,host_ip=host_ip,password_info=password_info,metadata=metadata,last_synch=last_synch,auto_synch_enabled=auto_synch_enabled)
            else:
                return render_template('db_info.html',pgweb_enabled=pgweb_enabled,pgweb_smpl_url=pgweb_smpl_url,pgweb_usr_url=pgweb_usr_url,db_info=db_info,ath_un=user,db_username=db_username,host_ip=host_ip,password_info=password_info,metadata=metadata,last_synch=last_synch,auto_synch_enabled=auto_synch_enabled)
        else:
            db_info = None
            db_username = None
            password_info = None
            flash('  The DB name, DB role and DB permissions are generated based on your username(email). Please log-in and try again. This information is not recorded anywhere until you proceed with the download and the AutoSynch option is enabled.','warning')
            return redirect(url_for('index'))

    @app.route("/dropbox_auth_request")
    def dropbox_auth_request():
        try:
            authorize_url = get_dropbox_auth_flow(session).start()
            return redirect(authorize_url, 301)
        except Exception as e:
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
            pass
        
    @app.route("/dropbox_confirm")
    def dropbox_confirm():
        try: 
            refresh_token = dropbox_auth_finish(session,request)
            session['dbx_auth_token'] = refresh_token
            continue_btn = 'delete'
            flash('  You have successfuly authenticated with Dropbox. Click "Continue" to proceed with download.','success')
            return redirect(url_for('index',continue_btn = continue_btn))
        except Exception as e:
            session['dbx_auth_token'] = None
            flash('  There was a problem authenticating with Dropbox.','warning')
            return redirect(url_for('index'))


    @app.route('/oura_auth_request')
    def oura_auth_request():
        try:
            oura_session = OAuth2Session(OURA_CLIENT_ID)
            authorization_url, state = oura_session.authorization_url(OURA_AUTH_URL)
            session['oura_oauth_state'] = state
            return redirect(authorization_url, 301)
        except Exception as e:
            pass

    @app.route('/oura_confirm')# Must match Redirect URI specified in https://cloud.ouraring.com/oauth/applications.
    def oura_confirm():
        oura_session = OAuth2Session(OURA_CLIENT_ID, state=session['oura_oauth_state'])
        try:
            response = oura_session.fetch_token(
                                OURA_TOKEN_URL,
                                client_secret=OURA_CLIENT_SECRET,
                                authorization_response=request.url)

            oura_refresh_token = response['refresh_token']
        
            session['oura_refresh_token'] = oura_refresh_token
            continue_btn = 'delete'
            flash('  You have successfuly authenticated with Oura. Click "Continue" to proceed with download.','success')
            return redirect(url_for('index',continue_btn = continue_btn))
        except Exception as e:
            session['oura_refresh_token'] = None
            flash('  There was a problem authenticating with Oura.','warning')
            return redirect(url_for('index'))

    @app.route('/strava_auth_request')
    def strava_auth_request():
        try:
            strava_session = OAuth2Session(STRAVA_CLIENT_ID,redirect_uri=STRAVA_REDIRECT_URI,scope='activity:read_all')
            authorization_url, state = strava_session.authorization_url(STRAVA_AUTH_URL)
            session['strava_oauth_state'] = state
            return redirect(authorization_url, 301)
        except Exception as e:
            pass

    @app.route('/strava_confirm')
    def strava_confirm():
        strava_session = OAuth2Session(STRAVA_CLIENT_ID, state=session['strava_oauth_state'])
        try:
            response = strava_session.fetch_token(
                                STRAVA_TOKEN_URL,
                                client_secret=STRAVA_CLIENT_SECRET,
                                include_client_id=True,
                                authorization_response=request.url)
            
            strava_refresh_token = response['refresh_token']

            session['strava_refresh_token'] = strava_refresh_token
            continue_btn = 'delete'
            flash('  You have successfuly authenticated with Strava. Click "Continue" to proceed with download.','success')
            return redirect(url_for('index',continue_btn = continue_btn))
        except Exception as e:
            session['strava_refresh_token'] = None
            flash('  There was a problem authenticating with Strava.','warning')
            return redirect(url_for('index'))

    @app.route("/process_running", methods = ['GET','POST'])
    def process_running():
        if request.method == 'POST':
            post_user = urllib.parse.unquote(request.form.get('ath_un'))
            pidfile = PID_FILE_DIR + post_user + '_PID.txt'
            if os.path.isfile(pidfile):
                #read PID from file
                with open(pidfile, "U") as f:
                    pid_from_file = f.read()
                #check whether the PID from file is still running
                if psutil.pid_exists(int(pid_from_file)):
                    p = psutil.Process(int(pid_from_file))
                    #Kill running process if initiated by user using web app
                    if p.ppid()==os.getpid():
                        try:
                            p.kill()
                            flash('  All tasks for ' +post_user+ ' have been suspended','success')
                        except Exception as e:
                            with ErrorStdoutRedirection(post_user):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    else:
                        flash('  The task can not be suspended as it is an automated auto_sych task that runs periodicaly to keep your DB in sync. This process will stop on its own in few minutes','warning') 
            return render_template('process_running.html',post_user=post_user)
        #Request method is GET
        else:
            referer = request.referrer
            good_referer = request.url_root
            if referer != good_referer:
                return redirect(url_for('index',referer=referer))
            else:
                user = request.args.get('user')
                return render_template('process_running.html',user=user,referer=referer,good_referer=good_referer)   

    return app
