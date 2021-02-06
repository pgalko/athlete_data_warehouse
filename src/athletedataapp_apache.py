#
# This module is loaded when web_app_loader_apache.py executes
# It is to be used on UNIX OS and Apache web server with mod_wsgi module(https://modwsgi.readthedocs.io/en/master).
#

from flask import Flask,render_template,request,flash,session,redirect, url_for
import datetime
import os
import time
import mfp_data_download_db_insert as mfp
import gc_data_download as gc
import delete_data as clr
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
from db_create_user_database import check_user_db_exists,check_host_record_exists,backup_user_db,create_sample_db,check_db_server_connectivity
from db_user_insert import gc_user_update
from db_dropbox import check_user_token_exists
from diasend_data_download_db_insert import diasend_data_export_insert
from glimp_data_download_db_insert import glimp_data_insert
from mind_monitor_data_download_db_insert import mm_data_insert
from send_email import send_email
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
from geoip import geolite2
from geopy.geocoders import Nominatim

                                              
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
                                                
path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = str(path_params.get("pid_file_dir"))
DOWNLOAD_DIR = str(path_params.get("download_dir"))
TEMP_FILE_PATH = str(path_params.get("temp_file_path"))

#Retrieve passphrase from the .temp file and delete it
f=open(TEMP_FILE_PATH,"r")
passphrase_input=f.read()
f.close
os.remove(TEMP_FILE_PATH)
encr_pass = passphrase_input

dbx_params = config(filename="encrypted_settings.ini", section="dropbox",encr_pass=encr_pass)
APP_KEY = str(dbx_params.get("app_key"))
APP_SECRET = str(dbx_params.get("app_secret"))
REDIRECT_URI = str(dbx_params.get("redirect_uri"))
integrated_with_dropbox = str(dbx_params.get("integrated_with_dropbox"))

anticaptcha_params = config(filename="encrypted_settings.ini", section="anticaptcha",encr_pass=encr_pass)
anticaptcha_api_key = str(anticaptcha_params.get("api_key"))
if anticaptcha_api_key == "":
    diasend_enabled = False
else:
    diasend_enabled = True

def get_dropbox_auth_flow(session):
    return dropbox.oauth.DropboxOAuth2Flow(
        APP_KEY, REDIRECT_URI, session, "athletedataapp_dropbox-auth-csrf-token", APP_SECRET)

# URL handler for /dropbox-auth-finish
def dropbox_auth_finish(session,request):
    try:
        auth_result = get_dropbox_auth_flow(session).finish(request.args)
        access_token = auth_result.access_token
    except Exception as e:
        with ConsolidatedProgressStdoutRedirection():
            print(e)

    return access_token

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
    output =None
    start_date = None
    end_date = None
    end_date_today =None
    del_progress = None
    mfp_progress = None
    diasend_progress = None
    glimp_progress = None
    mm_progress = None
    gc_login_progress = None
    gc_fit_activ_progress = None
    gc_tcx_activ_progress = None
    gc_fit_well_progress = None
    gc_json_well_progress = None
    gc_json_dailysum_progress = None
    progress_error = False
    archive_to_dropbox = False
    archive_radio = None
    dbx_auth_token = session.get('dbx_auth_token',None)
    auto_synch = False

    output = DOWNLOAD_DIR
        
                
    if request.method == 'POST':

        #----GC Login variables----
        if request.form.get('GCCheckbox') is not None:
            gc_login_radio = request.form.get('GCcredRadio')
            if gc_login_radio == 'enterGCcredRadio':
                gc_username = str(request.form.get('gcUN'))
                gc_password = str(request.form.get('gcPW'))
            elif gc_login_radio == 'getGCcredfromCSV':
                gc_username = str(request.form.get('gcUN'))
                gc_password = str(request.form.get('gcPW'))
                  
        #----Destination DB variables-----
        db_name = str(str2md5(gc_username)) + '_Athlete_Data_DB'
        
        #If user  wishes to download to his db, credentials to be provided and retrieved from the form.
        data_destination = request.form.get('dbSvr')
        if data_destination == 'remoteDbSvr':
            superuser_un = str(request.form.get('dbUser'))
            superuser_pw = str(request.form.get('dbPass'))
            encrypted_superuser_pw = base64.b64encode(encrypt(superuser_pw, encr_pass))
            db_host = str(request.form.get('dbHost'))
            #Test Connectivity to user db
            connection = check_db_server_connectivity(gc_username,db_host,superuser_un,superuser_pw)
            if connection != 'SUCCESS':
                flash('  Could cot connect to the DB Host.The host returned an error:  '+connection,'danger')
                return render_template("index.html",admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)
        else:
            #If user does not wish to download to his db, credentials to be retrieved from .ini.
            params = config(filename="encrypted_settings.ini", section="postgresql",encr_pass=encr_pass)
            superuser_un = params.get("user")
            superuser_pw = params.get("password")
            encrypted_superuser_pw = base64.b64encode(encrypt(superuser_pw, encr_pass))
            db_host = params.get("host")

        #Check if the user has a DB recorded in the info_db. If yes, stop execution and show warning message, otherwise proceed
        host_record_exists = check_host_record_exists(gc_username,db_name,db_host,encr_pass)
        if host_record_exists == True:
            flash('  You can only download to one db host. Please correct the db_hostname and try again','warning')
            return render_template("index.html",admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)

        #----Check if the provided GC credentials are valid-----
        gc_cred_valid = gc.check_gc_creds(gc_username,gc_password)
        if gc_cred_valid == False:
            flash('  The Garmin Connect login credentials are not valid. Please try again','warning')
            return render_template("index.html",admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)


        #----- Set Auto_Synch variables--------

        if request.form.get('AutoSynchCheckbox') is not None:
            auto_synch_checkbox = True
            save_pwd = True
        else:
            auto_synch_checkbox = False 
            save_pwd = False

        #----PID File check to prevent concurrent executions for the same user-----

        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'

        if os.path.isfile(pidfile):
            #read PID from file
            with open(pidfile, "U") as f:
                pid_from_file = f.read()
            #check whether the PID from file is still running
            if psutil.pid_exists(int(pid_from_file)):
                with ProgressStdoutRedirection(gc_username):
                    print((str(datetime.datetime.now()) + "  %s already exists, the previous execution of the task is still running... Web App exiting!" % pidfile))
                continue_btn = 'none'
                user=gc_username
                flash('  The previous execution of the task for: ' +user+ ' is still running... You can check the status below.','danger')
                return redirect(url_for('process_running',user=user)) 
            else:
                os.remove(pidfile)#Remove old PID file
            
        
        #-----MFP Login variables------        
        if request.form.get('MFPCheckbox') is not None:
            mfp_login_radio = request.form.get('MFPcredRadio')
            if mfp_login_radio == 'enterMFPcredRadio':
                mfp_username = str(request.form.get('mfpUN'))
                mfp_password = str(request.form.get('mfpPW'))
            elif mfp_login_radio == 'getMFPcredfromCSV':
                mfp_username = str(request.form.get('mfpUN'))
                mfp_password = str(request.form.get('mfpPW'))
                
        #-----Diasend Login variables------        
        if request.form.get('diasendCheckbox') is not None:
            diasend_login_radio = request.form.get('diasendCredRadio')
            if diasend_login_radio == 'enterDiasendCredRadio':
                diasend_username = str(request.form.get('diasendUN'))
                diasend_password = str(request.form.get('diasendPW'))
            elif diasend_login_radio == 'getDiasendCredfromCSV':
                diasend_username = str(request.form.get('diasendUN'))
                diasend_password = str(request.form.get('diasendPW'))
        
        #-----Link to Glimp export file------
        if request.form.get('glimpCheckbox') is not None:
            glimp_export_link = str(request.form.get('GlimpExportLink'))
            
        #-----Link to Mind Monitor export folder------
        if request.form.get('mmCheckbox') is not None:
            mm_export_link = str(request.form.get('mmExportLink'))
        
        #----Check for and Retrieve Dropbox token----   
        if request.form.get('archiveDataCheckbox') is not None:
            archive_radio = request.form.get('archiveData')
            if dbx_auth_token is None:
                db_exists = check_user_db_exists(gc_username,gc_password,db_host,superuser_un,superuser_pw,encr_pass)       
                if db_exists == True:
                    dbx_token_exists, dbx_token_from_db = check_user_token_exists(gc_username,db_host,db_name,superuser_un,superuser_pw,encr_pass) 
                    if dbx_token_exists == True: # token exists in database and it is not None
                        dbx_auth_token = dbx_token_from_db    
                        archive_to_dropbox = True
                    else:
                        return redirect(url_for('dropbox_auth_request'))
                else:
                    return redirect(url_for('dropbox_auth_request'))                
            else:
                archive_to_dropbox = True
        
        # CLEANUP BEFORE DOWNLOAD -----------------   
                
        #----Delete Files and DB Data variables----
        try:            
            if request.form.get('dataDeleteCheckbox') is not None:
                clearall_radio = request.form.get('deleteData')
                db_exists = check_user_db_exists(gc_username,gc_password,db_host,superuser_un,superuser_pw,encr_pass)       
                if db_exists == True:
                    if clearall_radio == 'deleteAllData':
                        try:
                            del_progress = 'Delete started'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            clr.delete_all_files(output, gc_username)  
                            clr.delete_all_db_data(gc_username,mfp_username,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                            del_progress = 'All data deleted succesfully'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ProgressStdoutRedirection(gc_username):
                                print(del_progress)
                        except:
                            del_progress = 'Error deleting data'
                            progress_error = True
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ErrorStdoutRedirection(gc_username):
                                print((str(datetime.datetime.now()) + '  ' + del_progress))
                    elif clearall_radio == 'deleteFiles':
                        try:
                            del_progress = 'Delete started'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            clr.delete_all_files(output, gc_username)
                            del_progress = 'All data deleted succesfully'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ProgressStdoutRedirection(gc_username):
                               print(del_progress)
                        except:
                            del_progress = 'Error deleting data'
                            progress_error = True
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ErrorStdoutRedirection(gc_username):
                                print((str(datetime.datetime.now()) + '  ' + del_progress))
                    elif clearall_radio == 'deleteDBdata':
                        try:
                            del_progress = 'Delete started'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            clr.delete_all_db_data(gc_username,mfp_username,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                            del_progress = 'All data deleted succesfully'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ProgressStdoutRedirection(gc_username):
                                print(del_progress)
                        except:
                            del_progress = 'Error deleting data'
                            progress_error = True
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ErrorStdoutRedirection(gc_username):
                                print((str(datetime.datetime.now()) + '  ' + del_progress))
                    elif clearall_radio == 'deleteAlldataExit':
                        try:
                            del_progress = 'Delete started'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            clr.delete_all_files(output, gc_username)
                            clr.delete_all_db_data(gc_username,mfp_username,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                            del_progress = 'All data deleted succesfully'
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ProgressStdoutRedirection(gc_username):
                                print(del_progress)
                            return render_template("index.html",del_progress=del_progress,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)
                        except:
                            del_progress = 'Error deleting data'
                            progress_error = True
                            with StdoutRedirection(gc_username):
                                print(del_progress)
                            time.sleep(1)
                            with ErrorStdoutRedirection(gc_username):
                                print((str(datetime.datetime.now()) + '  ' + del_progress))
                            return render_template("index.html",del_progress=del_progress,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)

                    
            if gc_username is None and gc_password is None and mfp_username is None and mfp_password is None:
                progress_error = True
                continue_btn = 'none'
                flash(' Must either specify a garmin connect or/and MFP login credentials. Or a path to garmin connect or/and MFP CSV credentials file.','danger')    
                    

            #----Check and set start_date and end_date variables and proceed with download----
            try:
                start_date = datetime.datetime.strptime((request.form.get('startDate')), "%Y-%m-%d")
                text = gc_username
                head, sep, tail = text.partition('@')
                display_name = head
                if request.form.get('endDate') != "": 
                    end_date = datetime.datetime.strptime((request.form.get('endDate')), "%Y-%m-%d")
                    if end_date >= datetime.datetime.today(): #today
                        end_date = datetime.datetime.today() - datetime.timedelta(days=1) #yesterday
                else:
                    end_date = datetime.datetime.today() - datetime.timedelta(days=1)#PG: end_date = yesterday
                    end_date_today = datetime.datetime.today()  #"PG: end_date_today = today
            except Exception as e:
                with ErrorStdoutRedirection(gc_username):
                    print((str(datetime.datetime.now()) + '  ' + str(e)))
                #PG:If start date not provided render index and flash warning   
                flash('  Please provide a valid start date and try again!','danger')
                return render_template("index.html",admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)

            # DATA DOWNLOAD -------------------------------------- 
                                    
            #PG:Call to execute "GC login" script
            if gc_username is not None:
                try:        
                    gc_agent = gc.login(gc_username, gc_password, mfp_username,db_host,superuser_un,superuser_pw,dbx_auth_token,encr_pass,save_pwd)
                    gc_user_update(gc_username,db_host,db_name,superuser_un,superuser_pw,encrypted_superuser_pw,auto_synch_checkbox,encr_pass)  #----Set Auto_Synch switch---- 
                    gc_login_progress = 'Login to GC successfull'
                    with StdoutRedirection(gc_username):
                        print(gc_login_progress)
                    with ProgressStdoutRedirection(gc_username):
                        print(gc_login_progress)                                
                except Exception as e:
                    with ErrorStdoutRedirection(gc_username):
                        print((str(datetime.datetime.now()) + '  ' + str(e)))
                    gc_login_progress = 'GC login error.Check UN and PW'
                    progress_error = True
                    with StdoutRedirection(gc_username):
                        print(gc_login_progress)
                    with ErrorStdoutRedirection(gc_username):
                        print((str(datetime.datetime.now()) + '  ' + gc_login_progress))
                    flash('  There was a problem logging in to Garmin Connect. Please try again later','warning')
                    return render_template("index.html",admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)

                #----------------------------------  Activity  ---------------------------------------    
                
                #PG:Call to execute "Parse and insert FIT activities" script
                try:
                    gc_fit_activ_progress = 'GC FIT activities download started'
                    with StdoutRedirection(gc_username):
                        print(gc_fit_activ_progress)
                    time.sleep(1)        
                    gc.dwnld_insert_fit_activities(gc_agent, gc_username, gc_password, mfp_username, start_date, end_date, output, db_host, db_name, superuser_un,superuser_pw,archive_to_dropbox,archive_radio,dbx_auth_token, auto_synch,encr_pass)
                    gc_fit_activ_progress = 'GC FIT activities downloaded successfully'
                    with StdoutRedirection(gc_username):
                        print(gc_fit_activ_progress)
                    time.sleep(1)
                    with ProgressStdoutRedirection(gc_username):
                        print(gc_fit_activ_progress) 
                except Exception as e:
                    with ErrorStdoutRedirection(gc_username):
                        print((str(datetime.datetime.now()) + '  ' + str(e)))
                    gc_fit_activ_progress = 'Error downloading GC FIT activities'
                    progress_error = True
                    with StdoutRedirection(gc_username):
                        print(gc_fit_activ_progress)
                    time.sleep(1)
                    with ErrorStdoutRedirection(gc_username):
                        print((str(datetime.datetime.now()) + '  ' + gc_fit_activ_progress))
                    
                #----------------------------------  Wellness  ----------------------------------------
                
                #PG:Call to execute "Parse and insert FIT wellness data" script
                if request.form.get('wellnessCheckbox') is not None:
                    try:
                        gc_fit_well_progress = 'GC FIT wellness download started'
                        with StdoutRedirection(gc_username):
                            print(gc_fit_well_progress)
                        time.sleep(1)        
                        gc.dwnld_insert_fit_wellness(gc_agent,start_date,end_date,gc_username, gc_password, mfp_username, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox,archive_radio,dbx_auth_token,encr_pass)
                        gc_fit_well_progress = 'GC FIT wellness data downloaded successfully'
                        with StdoutRedirection(gc_username):
                            print(gc_fit_well_progress)
                        time.sleep(1)
                        with ProgressStdoutRedirection(gc_username):
                            print(gc_fit_well_progress) 
                    except Exception as e:
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
                        gc_fit_well_progress = 'Error downloading GC FIT wellness data'
                        progress_error = True
                        with StdoutRedirection(gc_username):
                            print(gc_fit_well_progress)
                        time.sleep(1)
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + gc_fit_well_progress))
                    #PG:Call to execute "Parse and insert JSON wellness data" script
                    try:
                        gc_json_well_progress = 'GC JSON wellness download started'
                        with StdoutRedirection(gc_username):
                            print(gc_json_well_progress)
                        time.sleep(1)                
                        gc.dwnld_insert_json_wellness(gc_agent, start_date, end_date, gc_username, gc_password, mfp_username, display_name, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox,archive_radio,dbx_auth_token,encr_pass)
                        gc.dwnld_insert_json_body_composition(gc_agent, start_date, end_date, gc_username, gc_password, mfp_username, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox, archive_radio, dbx_auth_token,encr_pass)
                        gc_json_well_progress = 'GC JSON wellness data downloaded successfully'
                        with StdoutRedirection(gc_username):
                            print(gc_json_well_progress)
                        time.sleep(1)
                        with ProgressStdoutRedirection(gc_username):
                            print(gc_json_well_progress) 
                    except Exception as e:
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
                        gc_json_well_progress = 'Error downloading GC JSON wellness data'
                        progress_error = True
                        with StdoutRedirection(gc_username):
                            print(gc_json_well_progress)
                        time.sleep(1)
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + gc_json_well_progress))

                    #PG:Call to execute "Parse and insert JSON Daily summary data" script
                    try:
                        gc_json_dailysum_progress = 'GC JSON daily summary download started'
                        with StdoutRedirection(gc_username):
                            print(gc_json_dailysum_progress)
                        time.sleep(1)        
                        gc.dwnld_insert_json_dailysummary(gc_agent, start_date, end_date, gc_username, gc_password, mfp_username, display_name, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox,archive_radio,dbx_auth_token,encr_pass)
                        gc_json_dailysum_progress = 'GC JSON daily summary data downloaded successfully'
                        with StdoutRedirection(gc_username):
                            print(gc_json_dailysum_progress)
                        time.sleep(1)
                        with ProgressStdoutRedirection(gc_username):
                            print(gc_json_dailysum_progress) 
                    except Exception as e:
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
                        gc_json_dailysum_progress = 'Error downloading GC JSON daily summary'
                        progress_error = True
                        with StdoutRedirection(gc_username):
                            print(gc_json_dailysum_progress)
                        time.sleep(1)
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + gc_json_dailysum_progress)) 
                
                #----------------- Nutrition MFP ---------------------------    
                #PG:Call to execute "parse and insert MFP data" script
                if mfp_username is not None:   
                    try:
                        mfp_progress = 'MFP download started'
                        with StdoutRedirection(gc_username):
                            print(mfp_progress)
                        time.sleep(1)
                        mfp.dwnld_insert_nutrition(mfp_username,mfp_password,gc_username,start_date,end_date,encr_pass,save_pwd,auto_synch,db_host,superuser_un,superuser_pw)
                        mfp_progress = 'MFP nutrition data downloaded successfully'
                        with StdoutRedirection(gc_username):
                            print(mfp_progress)
                        time.sleep(1)
                        with ProgressStdoutRedirection(gc_username):
                            print(mfp_progress)
                    except Exception as e:
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
                        mfp_progress = 'Error downloading MFP nutrition data'
                        with StdoutRedirection(gc_username):
                            print(mfp_progress)
                        time.sleep(1)
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + mfp_progress))
                
                #-------------------- BG Diasend --------------------------            
                #PG:Call to execute "parse and insert Diasend data" script
                if diasend_username is not None:   
                    try:
                        diasend_progress = 'Diasend CGM download started'
                        with StdoutRedirection(gc_username):
                            print(diasend_progress)
                        time.sleep(1)
                        diasend_data_export_insert(output,start_date,end_date,gc_username,diasend_username,diasend_password,encr_pass,save_pwd,archive_to_dropbox,archive_radio,dbx_auth_token,db_host,superuser_un,superuser_pw)
                        diasend_progress = 'Diasend CGM data downloaded successfully'
                        with StdoutRedirection(gc_username):
                            print(diasend_progress)
                        time.sleep(1)
                    except Exception as e:
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
                        diasend_progress = 'Error downloading Diasend GCM data'
                        with StdoutRedirection(gc_username):
                            print(diasend_progress)
                        time.sleep(1)
                        
                #------------------ BG Glimp --------------------------        
                #PG:Call to execute "parse and insert Glimp data" script
                if glimp_export_link is not None:
                    try:
                        glimp_progress = 'Glimp CGM download started'
                        with StdoutRedirection(gc_username):
                            print(glimp_progress)
                        time.sleep(1)
                        glimp_data_insert(output,start_date,end_date,gc_username,encr_pass,glimp_export_link,save_pwd,db_host,db_name,superuser_un,superuser_pw)
                        glimp_progress = 'Glimp CGM data downloaded successfully'
                        with StdoutRedirection(gc_username):
                            print(glimp_progress)
                        time.sleep(1)
                    except Exception as e:
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
                        glimp_progress = 'Error downloading Glimp CGM data'
                        with StdoutRedirection(gc_username):
                            print(glimp_progress)
                        time.sleep(1)

                #------------------ EEG Mind Monitor --------------------------
                #PG:Call to execute "parse and insert MM data" script
                if mm_export_link is not None:
                    try:
                        mm_progress = 'Mind Monitor download started'
                        with StdoutRedirection(gc_username):
                            print(mm_progress)
                        time.sleep(1)
                        mm_data_insert(output,start_date,end_date,gc_username,encr_pass,mm_export_link,save_pwd,db_host,db_name,superuser_un,superuser_pw)
                        mm_progress = 'Mind Monitor data downloaded successfully'
                        with StdoutRedirection(gc_username):
                            print(mm_progress)
                        time.sleep(1)
                    except Exception as e:
                        with ErrorStdoutRedirection(gc_username):
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
                        mm_progress = 'Error downloading Mind Monitor data'
                        with StdoutRedirection(gc_username):
                            print(mm_progress)
                        time.sleep(1)

                #------Archive DB to Dropbox-------
                try:
                    if archive_to_dropbox == True:
                        if archive_radio == "archiveAllData" or archive_radio == "archiveDBdata":
                            backup_user_db(db_name,gc_username,output,dbx_auth_token,encr_pass)
                except Exception as e:
                    with ErrorStdoutRedirection(gc_username):
                        print((str(datetime.datetime.now()) + '  ' + str(e)))
                    pass

                                

                       
            
            if progress_error is True:
                error_log_entry = 'With Errors'
                continue_btn_entry = 'no_delete'
                flash('  There was a problem downloading or processing the data. When you choose "Continue" the app will check the data integrity and it will pick up where it left off, skipping the already downloaded and processed data.','danger')
                if send_emails == 'true':
                    send_email(
                        encr_pass,
                        'The athlete data download has failed',
                        'There was a problem downloading or processing the data.Please start the download process again. The app will check the data integrity and it will pick up where it left off, skipping the already downloaded and processed data.',
                        None,
                        gc_username
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
                            gc_username
                        ) 


            with ErrorStdoutRedirection(gc_username):
                print(('--------------- ' + str(datetime.datetime.now()) + '  User ' + gc_username + '  Finished Data Download ' + error_log_entry +' -------------' ))
            with ProgressStdoutRedirection(gc_username):
                print(('--------------- ' + str(datetime.datetime.now()) + '  User ' + gc_username + '  Finished Data Download ' + error_log_entry +' -------------' ))

            return render_template("index.html",del_progress = del_progress,mfp_progress = mfp_progress,diasend_progress = diasend_progress,glimp_progress = glimp_progress, mm_progress = mm_progress, gc_login_progress = gc_login_progress,
                                gc_fit_activ_progress = gc_fit_activ_progress,gc_tcx_activ_progress = gc_tcx_activ_progress,
                                gc_fit_well_progress = gc_fit_well_progress, gc_json_well_progress = gc_json_well_progress,
                                gc_json_dailysum_progress = gc_json_dailysum_progress, progress_error = progress_error, continue_btn = continue_btn,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)

        except Exception as e:
            with ErrorStdoutRedirection(gc_username):
                print((str(datetime.datetime.now()) + '  ' + str(e)))
            os.unlink(pidfile)

        finally:
            if os.path.isfile(pidfile):
                os.unlink(pidfile)

    else: # Request method is GET
        continue_btn = request.args.get('continue_btn')
        return render_template("index.html",continue_btn = continue_btn,admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)

@app.route("/datamodel_preview")
def datamodel_preview():
    #Currently defaults to /static/images/Athlete_DB_Model_Visualisation_New.jpg Data Model image until I figure out the best way to highlight selected tables.
    datamodel = None
    if (request.args.get('gc')=='1') and (request.args.get('wel')=='1') and (request.args.get('mfp')=='1') and (request.args.get('dia')=='1'):
        datamodel = "all_data_datamodel"
    elif (request.args.get('gc')=='1') and (request.args.get('wel')=='1') and (request.args.get('dia')=='1'):
        datamodel = "gc_wel_dia_datamodel"
    elif (request.args.get('gc')=='1') and (request.args.get('dia')=='1'):
        datamodel = "gc_dia_datamodel"
    elif (request.args.get('gc')=='1') and (request.args.get('wel')=='1') and (request.args.get('mfp')=='1'):
        datamodel = "gc_wel_mfp_datamodel"
    elif (request.args.get('gc')=='1') and (request.args.get('wel')=='1'):
        datamodel = "gc_wel_datamodel"
    elif (request.args.get('gc')=='1'):
        datamodel = "gc_datamodel"
    else:
        datamodel = "empty_datamodel"
    #return render_template('datamodel_preview.html',datamodel=datamodel)
    return render_template('datamodel_preview.html',datamodel="empty_datamodel")

@app.route("/db_info")
def db_info():
    password_info = '\"Your Garmin Connect password\"'
    metadata = None
    #Get hostname/IP address
    if request.args.get('dbhost')=='':# Local DB host
        try:
            host_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        except:
            text = request.host
            head, sep, tail = text.partition(':')
            host_ip = head
    else:# Remote DB host
        host_ip = request.args.get('dbhost')
    if request.args.get('user')!='':
        user = urllib.parse.unquote(request.args.get('user'))
        text = user
        head, sep, tail = text.partition('@')
        db_username = head
        db_info = str(str2md5(user)) + '_Athlete_Data_DB'
        sample_db = "sample_db"
        
        # Check if the sample DB exists, and create it if it does not.
        create_sample_db(encr_pass)

        # read DB connection parameters from ini file
        conn = None
        params = config(filename="encrypted_settings.ini", section="postgresql",encr_pass=encr_pass)
        superuser_un = params.get("user")
        superuser_pw = params.get("password")
        host = params.get("host")

        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=sample_db, host=host, user=superuser_un, password=superuser_pw)

        sql = """
        SELECT table_name,column_name,data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name;  
        """
        sql_table_list = """
        SELECT DISTINCT table_name FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name;          
        """
        try:
            cur = conn.cursor()
            cur.execute(sql,())
            conn.commit()
            metadata = cur.fetchall()
            cur.close
            
            cur = conn.cursor()
            cur.execute(sql_table_list,())
            conn.commit()
            table_list = cur.fetchall()
            cur.close()
        except  (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(user):
                print((str(datetime.datetime.now()) + '  ' + str(error)))
        return render_template('db_info.html',db_info = db_info,db_username=db_username,host_ip=host_ip,password_info=password_info,metadata=metadata,table_list=table_list)
    else:
        db_info = None
        db_username = None
        password_info = None
        flash('  The DB name, DB role and DB permissions are generated based on your Garmin Connect username. Please fill in your GC credentials and try again. This information is not recorded anywhere until you proceed with the download and the AutoSynch option is enabled.','warning')
        return render_template("index.html",admin_email=admin_email,integrated_with_dropbox=integrated_with_dropbox,diasend_enabled=diasend_enabled)

@app.route("/dropbox_auth_request")
def dropbox_auth_request():
    try:
        authorize_url = get_dropbox_auth_flow(session).start()
        return redirect(authorize_url, 301)
    except Exception as e:
        print(e)
        pass
    
@app.route("/dropbox_confirm")
def dropbox_confirm(): 
    token = dropbox_auth_finish(session,request)
    session['dbx_auth_token'] = token
    continue_btn = 'delete'
    flash('  You have successfuly authenticated with Dropbox. Click "Continue" to proceed with download.','success')
    return redirect(url_for('index',continue_btn = continue_btn))

@app.route("/process_running", methods = ['GET','POST'])
def process_running():
    if request.method == 'POST':
        post_user = urllib.parse.unquote(request.form.get('gcUN'))
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
                            print((str(datetime.datetime.now()) + '  ' + str(e)))
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

@app.route("/dummy_1", methods=['POST']) #This is not used as it requires data in sample_db to work (element in index.html hidden).
def dummy1():
    try:
        post_user = urllib.parse.unquote(request.form.get('dash_un'))
        post_pw = urllib.parse.unquote(request.form.get('dash_pw'))
        gc_cred_valid = gc.check_gc_creds(post_user,post_pw)
        if gc_cred_valid == False:
            flash('  The Garmin Connect login credentials are not valid. Please try again','warning')
            return redirect(url_for('index'))
        else:
            encrypted_un = base64.urlsafe_b64encode(encrypt(post_user, encr_pass))
            return redirect('/dashboard_1/'+encrypted_un+'/')
    except Exception as e:
        with ErrorStdoutRedirection(post_user):
            print((str(datetime.datetime.now()) + '  ' + str(e)))
        flash('  There was a problem generating dashboard. Either your database does not exist in the system yet or there was a problem accessing the data','warning')
        return redirect(url_for('index'))

# read DB connection parameters from ini file
params = config(filename="encrypted_settings.ini", section="postgresql",encr_pass=encr_pass)
db_user = params.get("user")
db_pw = params.get("password")

db = 'sample_db'

# Check if the sample DB exists, and create it if it does not.
create_sample_db(encr_pass)                                       

#Uncomment if you want to enable the sample visualisation (needs data in sample db to work)                                
#dash_app = create_dashboard1(app,encr_pass,db_user,db_pw,db)


if __name__ == '__main__':
    app.run()
