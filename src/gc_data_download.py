
from db_gc_activity_insert import gc_activity_insert
from db_gc_wellness_insert import gc_wellness_insert
from db_gc_original_session_insert import gc_original_session_insert
from db_gc_original_lap_insert import gc_original_lap_insert
from db_gc_original_record_insert import gc_original_record_insert
from db_gc_dailysummary_insert import gc_dailysummary_insert
from db_gc_original_wellness_insert import gc_original_wellness_insert
from db_gc_bodycomposition_insert import gc_bodycomposition_insert
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from db_create_user_database import check_user_db_exists,create_user_db,restore_db_schema
from archive_data_dropbox import check_if_file_exists_in_dbx, download_files_to_dbx
from db_files import data_file_path_insert,check_data_file_exists
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
from database_ini_parser import config
import dicttoxml
from xml.dom.minidom import parseString
import json
import cloudscraper
import datetime
import time
import base64
import os
from os import remove, stat
from shutil import rmtree,move
import psutil
import re
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import zipfile
import Crypto.Random
from Crypto.Cipher import AES
from func_timeout import func_timeout, FunctionTimedOut

#-------------------------------
#A custom adapter that specifies a different security level to address CloudFlare rejecting default TLS fingerprints
#Credit (Steffen Ullrich) - https://stackoverflow.com/questions/64967706/python-requests-https-code-403-without-but-code-200-when-using-burpsuite
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

CIPHERS = ('DEFAULT:@SECLEVEL=2')
class CipherAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(CipherAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(CipherAdapter, self).proxy_manager_for(*args, **kwargs)
#------------------------------------

#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16

BASE_URL = "https://sso.garmin.com/sso/signin"
HOSTNAME = "https://connect.garmin.com"
GAUTH = "https://connect.garmin.com/auth/hostname"
SSO = "https://sso.garmin.com/sso"
CSS = "https://static.garmincdn.com/com.garmin.connect/ui/css/gauth-custom-v1.2-min.css"
REDIRECT = "https://connect.garmin.com/"
ACTIVITIES = "https://connect.garmin.com/proxy/activitylist-service/activities/search/activities?start=%s&limit=%s"
WELLNESS = "https://connect.garmin.com/proxy/userstats-service/wellness/daily/%s?fromDate=%s&untilDate=%s"
DAILYSUMMARY = "https://connect.garmin.com/proxy/wellness-service/wellness/dailySummaryChart/%s?date=%s"
BODY_COMPOSION = "https://connect.garmin.com/proxy/userprofile-service/userprofile/personal-information/weightWithOutbound/filterByDay?from=%s&until=%s"

TCX = "https://connect.garmin.com/proxy/download-service/export/tcx/activity/%s"
GPX = "https://connect.garmin.com/proxy/download-service/export/gpx/activity/%s"
ZIP_ACT = "https://connect.garmin.com/proxy/download-service/files/activity/%s"
ZIP_WELL = "https://connect.garmin.com/proxy/download-service/files/wellness/%s"

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = str(path_params.get("pid_file_dir"))

archive_params = config(filename="encrypted_settings.ini", section="archive")
preserve_files = str(archive_params.get("preserve_files"))

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    #iv = Crypto.Random.get_random_bytes(AES.block_size)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt  

def check_gc_creds(username,password):
    agent = cloudscraper.create_scraper()
    #mount the custom adapter
    agent.mount(BASE_URL, CipherAdapter())
    cred_valid = None 
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    auth_response = agent.post(BASE_URL,headers={"origin": "https://sso.garmin.com","User-Agent": user_agent,},
                                        params={"service": "https://connect.garmin.com/modern"},
                                        data={"username": username,"password": password,"embed": "false",},)
    #use regular expression to search for auth ticket url in response. If there is a nmatch the login has ben successfull
    match = re.search(r'response_url\s*=\s*"(https:[^"]+)"', auth_response.text)
    if not match:
        with ErrorStdoutRedirection(username):
            print(str(datetime.datetime.now()) + " Garmin Auth failure. Status code: " + str(auth_response.status_code))
        cred_valid = False
    else:
        with ProgressStdoutRedirection(username):
            print(str(datetime.datetime.now()) + " Garmin Auth success. Status code: " + str(auth_response.status_code))
        cred_valid = True
        
    return cred_valid
    
def login(username, password):
    agent = cloudscraper.create_scraper()
    #mount the custom adapter
    agent.mount(BASE_URL, CipherAdapter())
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    
    with StdoutRedirection(username):
        print("Attempting to login to Garmin Connect...")
    with ProgressStdoutRedirection(username):
        print("Attempting to login to Garmin Connect...")
    
    # Submit the login credentials!
    try:
        auth_response = agent.post(BASE_URL,headers={"origin": "https://sso.garmin.com","User-Agent": user_agent,},
                                            params={"service": "https://connect.garmin.com/modern"},
                                            data={"username": username,"password": password,"embed": "false",},)
        #use regular expression to search for auth ticket url in response
        match = re.search(r'response_url\s*=\s*"(https:[^"]+)"', auth_response.text)

        if match:                                               
            try:
                #create auth ticket url.eg https://connect.garmin.com/modern?ticket=ST-2112503-Ez4g4H9bWnU0dOo9S06b-cas
                auth_ticket_url = match.group(1).replace("\\", "")
                #login to garmin
                agent.get(auth_ticket_url)
                with StdoutRedirection(username):
                    print('GC Login successful! Proceeding...')
                with ProgressStdoutRedirection(username):
                    print('GC Login successful! Proceeding...')
                return agent
            except Exception as e:
                with ErrorStdoutRedirection(username):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
            # In theory, we're in.
        else:
            raise Exception('Garmin Auth failure: unable to extract auth ticket URL.')   
    except Exception as e:
        with ErrorStdoutRedirection(username):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        #yield start_date + datetime.timedelta(n) #ascending start date to end date
        yield end_date - datetime.timedelta(n) #descending end date to start date

def getDateToEpoch(myDateTime):
    epoch = (datetime.datetime(myDateTime.year,myDateTime.month,myDateTime.day,myDateTime.hour,myDateTime.minute,myDateTime.second) - datetime.datetime(1970,1,1)).total_seconds()
    epoch_milisec = int(epoch)*1000
    return epoch_milisec

def dwnld_insert_fit_activities(ath_un, agent, gc_username, gc_password, mfp_username, start_date, end_date, output, db_host, db_name, superuser_un,superuser_pw,archive_to_dropbox,archive_radio,dbx_auth_token,auto_synch,encr_pass,increment = 100):
    currentIndex = 0
    initUrl = ACTIVITIES % (currentIndex, increment)  # 100 activities at a time    
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'GC_Historical_Original_Activity')
    archive_folder = os.path.join(download_folder, 'Archive')
    download_folder_dbx = 'GC_Historical_Original_Activity'
    dbx_file_exists = None
    
    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create Archive directory (if it does not already exist).
    if preserve_files == "true":  
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)
    
    try:
        response = agent.get(initUrl)
    except Exception as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
        with StdoutRedirection(ath_un):
            print(('Error connecting to Garmin Connect for: {}.Retrying.'.format(ath_un)))
        #Retry login to GarminConnect
        agent = login(gc_username, gc_password)
        response = agent.get(initUrl)
        pass
  
    search = json.loads(response.text)
    while True:
        if len(search) == 0:
            # All done!
            with StdoutRedirection(ath_un):
                print('Download and import complete')
            with ProgressStdoutRedirection(ath_un):
                print('Download and import complete')
            break

        for item in search:
            # Read this list of activities and save the files.

            activityId = item['activityId']
            activityDate = item['startTimeLocal'][:10]
            activityDate_dt = datetime.datetime.strptime((activityDate), "%Y-%m-%d")
            
            
            # Compare if the activityDate is within the download Date range
            if activityDate_dt > end_date + datetime.timedelta(days=1): 
                continue
            if activityDate_dt < start_date:
                break
            url = ZIP_ACT % activityId
            file_name = '{}_{}.zip'.format(activityDate, activityId)
            file_name_unzipped = '{}_ACTIVITY.fit'.format(activityId) # 20201105 Garmin added "_ACTIVITY" to the filename
            file_path = os.path.join(download_folder, file_name)
            file_path_unzipped = os.path.join(download_folder, file_name_unzipped)
            file_path_archive = os.path.join(archive_folder, file_name_unzipped)

            # PG Check if the file exists in dropbox.
            try:
                if archive_to_dropbox == True:
                    if archive_radio == "archiveAllData" or archive_radio == "archiveFiles":
                        dbx_file_exists = check_if_file_exists_in_dbx(file_name_unzipped,dbx_auth_token,download_folder_dbx,encr_pass)
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

            #PG: Check whether the data from this file "file_path_unzipped" have been inserted into to DB during one of the previous runs          
            data_file_exists = check_data_file_exists(file_path_unzipped,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            if data_file_exists == True:
                with StdoutRedirection(ath_un):
                    print(('{} already downloaded and inserted to DB. Skipping.'.format(file_name_unzipped)))
                with ProgressStdoutRedirection(ath_un):
                    print(('{} already downloaded to {} and inserted to DB. Skipping.'.format(file_name_unzipped, download_folder)))
                # PG Archive to dbx already localy existing file
                if dbx_file_exists == False:
                    #PG: Check whether the file needs to be re-downloaded or still exists in the download folder
                    if not os.path.exists(file_path_unzipped):             
                        with StdoutRedirection(ath_un):
                            print(('{} is downloading...'.format(file_name)))
                        with ProgressStdoutRedirection(ath_un):
                            print(('{} is downloading...'.format(file_name)))
                        try:
                            datafile = agent.get(url).content
                        except urllib.error.HTTPError as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Retrying...'.format(file_name)))
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            try:
                                #Pause and Retry login
                                time.sleep(10)
                                agent = login(gc_username, gc_password)
                                datafile = agent.get(url).content
                                pass
                            except:
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Aborting...'.format(file_name)))
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                                #Abort and continue to next file
                                continue
                        except urllib.error.URLError as e:
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Retrying...'.format(file_name)))
                            with ErrorStdoutRedirection(ath_un):
                                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                            try: 
                                #Pause and Retry login
                                time.sleep(10)
                                agent = login(gc_username, gc_password)
                                datafile = agent.get(url).content
                                pass
                            except:
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Aborting...'.format(file_name)))
                                with ErrorStdoutRedirection(ath_un):
                                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                                #Abort and continue to next file
                                continue
                        f = open(file_path, "wb")
                        f.write(datafile)
                        f.close()
                    
                        #PG: Unzip the fit files and delete archive
                        with StdoutRedirection(ath_un):
                            print("Unzipping and removing original files...")
                        with ProgressStdoutRedirection(ath_un):
                           print("Unzipping and removing original files...")
                        with StdoutRedirection(ath_un):
                            print(('Filesize is: ' + str(stat(file_path).st_size)))
                        with ProgressStdoutRedirection(ath_un):
                            print(('Filesize is: ' + str(stat(file_path).st_size)))
                        if stat(file_path).st_size > 0:
                                zip_file = open(file_path, 'rb')
                                z = zipfile.ZipFile(zip_file)
                                for name in z.namelist():
                                    z.extract(name, download_folder)
                                zip_file.close()
                        else:
                            with ProgressStdoutRedirection(ath_un):
                                print('Skipping 0Kb zip file.')
                        remove(file_path) #Remove .zip file
                        download_files_to_dbx(file_path_unzipped,file_name_unzipped,dbx_auth_token, download_folder_dbx,encr_pass)
                        if preserve_files == "false":
                            #Remove the csv file from download folder
                            os.remove(file_path_unzipped)
                        else:
                            #Move the csv to archive folder
                            if not os.path.exists(file_path_archive):
                                os.rename(file_path_unzipped,file_path_archive)
                            else:
                                os.remove(file_path_unzipped)
                    else:
                        download_files_to_dbx(file_path_unzipped,file_name_unzipped,dbx_auth_token, download_folder_dbx,encr_pass)
                        if preserve_files == "false":
                            #Remove the csv file from download folder
                            os.remove(file_path_unzipped)
                        else:
                            #Move the csv to archive folder
                            if not os.path.exists(file_path_archive):
                                os.rename(file_path_unzipped,file_path_archive)
                            else:
                                os.remove(file_path_unzipped)
                continue

            #PG: Check whether the file needs to be downloaded or still exists in the download folder
            if not os.path.exists(file_path_unzipped):             
                with StdoutRedirection(ath_un):
                    print(('{} is downloading...'.format(file_name)))
                with ProgressStdoutRedirection(ath_un):
                    print(('{} is downloading...'.format(file_name)))
                try:
                    datafile = agent.get(url).content
                except urllib.error.HTTPError as e:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Retrying...'.format(file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    try:
                        #Pause and Retry login
                        time.sleep(10)
                        agent = login(gc_username, gc_password)
                        datafile = agent.get(url).content
                        pass
                    except:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Aborting...'.format(file_name)))
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                        #Abort and continue to next file
                        continue
                except urllib.error.URLError as e:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Retrying...'.format(file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    try: 
                        #Pause and Retry login
                        time.sleep(10)
                        agent = login(gc_username, gc_password)
                        datafile = agent.get(url).content
                        pass
                    except:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit activity {}. Aborting...'.format(file_name)))
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                        #Abort and continue to next file
                        continue
                f = open(file_path, "wb")
                f.write(datafile)
                f.close()
               
                #PG: Unzip the fit files and delete archive
                with StdoutRedirection(ath_un):
                    print("Unzipping and removing original files...")
                with ProgressStdoutRedirection(ath_un):
                    print("Unzipping and removing original files...")
                with StdoutRedirection(ath_un):
                    print(('Filesize is: ' + str(stat(file_path).st_size)))
                with ProgressStdoutRedirection(ath_un):
                    print(('Filesize is: ' + str(stat(file_path).st_size)))
                if stat(file_path).st_size > 0:
                    zip_file = open(file_path, 'rb')
                    z = zipfile.ZipFile(zip_file)
                    for name in z.namelist():
                        z.extract(name, download_folder)
                        #Check if the unzipped file has a .fit extension
                        z_filename, z_file_extension = os.path.splitext(name)
                        if z_file_extension != '.fit':
                            with ProgressStdoutRedirection(ath_un):
                                print(('The downloaded activity file has an extension: '+z_file_extension+' and will be skipped.'))
                            data_file_exists = check_data_file_exists((os.path.join(download_folder, name)),ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                            if data_file_exists == False:
                                data_file_path_insert((os.path.join(download_folder, name)),ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                            if archive_to_dropbox == True:
                                if archive_radio == "archiveAllData" or archive_radio == "archiveFiles":
                                    dbx_file_exists = check_if_file_exists_in_dbx((os.path.join(download_folder, name)),dbx_auth_token,download_folder_dbx,encr_pass)
                                    if dbx_file_exists == False:
                                        download_files_to_dbx((os.path.join(download_folder, name)),name,dbx_auth_token, download_folder_dbx,encr_pass)
                            remove(os.path.join(download_folder, name))
                    zip_file.close()
                    remove(file_path)
                else:
                    with ProgressStdoutRedirection(ath_un):
                        print('Skipping 0Kb zip file.')
                    remove(file_path)
                    continue

            if not os.path.exists(file_path_unzipped):
                continue

            # PG Archive to dbx newly downloaded file
            if dbx_file_exists == False:
                download_files_to_dbx(file_path_unzipped,file_name_unzipped,dbx_auth_token, download_folder_dbx,encr_pass)
            
            #Function that combines several functions to parse the fit file and insert the data to db
            def fit_db_insert_function(file_path_unzipped,file_path_archive,activityId, ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass):
                gc_original_session_insert(file_path_unzipped,activityId, ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass)
                gc_original_lap_insert(file_path_unzipped,activityId,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass)
                gc_original_record_insert(file_path_unzipped,activityId,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass)
                data_file_path_insert(file_path_unzipped,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                if preserve_files == "false":
                    #Remove the csv file from download folder
                    os.remove(file_path_unzipped)
                else:
                    #Move the csv to archive folder
                    if not os.path.exists(file_path_archive):
                        os.rename(file_path_unzipped,file_path_archive)
                    else:
                        os.remove(file_path_unzipped)
            
            try:
                #Run fit_db_insert_function() within func_timeout() to limit the execution time. If the limit is reached kill the process
                func_timeout(1440,fit_db_insert_function, args=(file_path_unzipped,file_path_archive,activityId,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass))
            except FunctionTimedOut:
                pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
                if os.path.isfile(pidfile):
                    #read PID from file
                    with open(pidfile, "U") as f:
                        pid_from_file = f.read()
                    #check whether the PID from file is still running
                    if psutil.pid_exists(int(pid_from_file)):
                        p = psutil.Process(int(pid_from_file))
                        #Kill running process
                        p.kill()
                        time.sleep(1)
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + ' The insert function with PID:{} has timed out parsing and inserting data from {}. Will now clean up, and move onto next fit file !'.format(pid_from_file, file_name)))        
                if preserve_files == "false":
                    #Remove the csv file from download folder
                    os.remove(file_path_unzipped)
                else:
                    #Move the csv to archive folder
                    if not os.path.exists(file_path_archive):
                        os.rename(file_path_unzipped,file_path_archive)
                    else:
                        os.remove(file_path_unzipped)
                continue
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                if preserve_files == "false":
                    #Remove the csv file from download folder
                    os.remove(file_path_unzipped)
                else:
                    #Move the csv to archive folder
                    if not os.path.exists(file_path_archive):
                        os.rename(file_path_unzipped,file_path_archive)
                    else:
                        os.remove(file_path_unzipped)
                continue
            
        # We still have at least 1 activity.
        currentIndex += increment
        url = ACTIVITIES % (currentIndex, increment)
        try:
            response = agent.get(url)
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
            # Retry logging in to GarminConnect
            agent = login(gc_username, gc_password)
            response = agent.get(url)
        search = json.loads(response.text)      

def dwnld_insert_fit_wellness(ath_un, agent, start_date, end_date, gc_username, gc_password, mfp_username, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox, archive_radio, dbx_auth_token, encr_pass):
    
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'GC_Historical_Original_Wellness')
    archive_folder = os.path.join(download_folder, 'Archive')
    download_folder_dbx = 'GC_Historical_Original_Wellness'
    dbx_file_exists = None
    
    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create Archive directory (if it does not already exist).
    if preserve_files == "true":  
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)
   
    for single_date in daterange(start_date, end_date):
        date_in_range = single_date.strftime("%Y-%m-%d")
        url = ZIP_WELL % (date_in_range)
        file_name = '{}.zip'.format(date_in_range)
        file_name_unzipped = '{}'.format(date_in_range)
        file_path_unzipped = os.path.join(download_folder, file_name_unzipped)
        file_path_archive = os.path.join(archive_folder, file_name_unzipped)
        
        # PG Check if the file exists in dropbox.
        try:
            if archive_to_dropbox == True:
                if archive_radio == "archiveAllData" or archive_radio == "archiveFiles":
                    dbx_file_exists = check_if_file_exists_in_dbx(file_name_unzipped,dbx_auth_token,download_folder_dbx,encr_pass)
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
        
        #PG: Check whether the data from this file "file_path_unzipped" have been inserted into to DB during one of the previous runs 
        data_file_exists = check_data_file_exists(file_path_unzipped,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
        #PG: Check whether the file needs to be downloaded or still exists in the download folder
        if not os.path.exists(file_path_unzipped):
            with StdoutRedirection(ath_un):
                print(('{} is downloading...'.format(file_name)))
            with ProgressStdoutRedirection(ath_un):
                print(('{} is downloading...'.format(file_name)))
            try:
                datafile = agent.get(url).content
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit wellness {}. The error code 404: Not Found. Moving onto next file'.format(file_name)))
                    continue
                else:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit wellness {}. Retrying...'.format(file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    try:
                        #Pause and Retry login
                        time.sleep(10)
                        agent = login(gc_username, gc_password)
                        datafile = agent.get(url).content
                        pass
                    except:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit wellness {}. Aborting...'.format(file_name)))
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                        #Abort and continue to next file
                        continue
            except urllib.error.URLError as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit wellness {}. Retrying...'.format(file_name)))
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                try: 
                    #Pause and Retry login
                    time.sleep(10)
                    agent = login(gc_username, gc_password)
                    datafile = agent.get(url).content
                    pass
                except:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading fit wellness {}. Aborting...'.format(file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #Abort and continue to next file
                    continue

            file_path = os.path.join(download_folder, file_name)       
            f = open(file_path, "wb")
            f.write(datafile)
            f.close()
                
            #PG: Unzip the fit files and delete archive
            with StdoutRedirection(ath_un):
                print("Unzipping and removing original files...")
            with ProgressStdoutRedirection(ath_un):
                print("Unzipping and removing original files...")
            with StdoutRedirection(ath_un):
                print(('Filesize is: ' + str(stat(file_path).st_size)))
            with ProgressStdoutRedirection(ath_un):
                print(('Filesize is: ' + str(stat(file_path).st_size)))
            if stat(file_path).st_size > 0:
                    zip_file = open(file_path, 'rb')
                    z = zipfile.ZipFile(zip_file)
                    for name in z.namelist():
                        z.extract(name,file_path_unzipped)
                    zip_file.close()
            else:
                with ProgressStdoutRedirection(ath_un):
                    print('Skipping 0Kb zip file.')
            remove(file_path)
            with ProgressStdoutRedirection(ath_un):
                print('Done.')

        # TODO:Archive to dbx newly downloaded file but only if the day is complete
        if dbx_file_exists == False and single_date.date() < datetime.datetime.today().date():
               download_subfolder_dbx = download_folder_dbx+'/'+file_name_unzipped
               for filename in os.listdir(file_path_unzipped):
                   path_to_file = file_path_unzipped+'/'+filename
                   download_files_to_dbx(path_to_file,filename,dbx_auth_token, download_subfolder_dbx,encr_pass)
        
        for filename in os.listdir(file_path_unzipped):
            #Function that combines several functions to parse the fit file and insert the data to db
            def wellness_fit_db_insert_function(file2import,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass):
                gc_original_wellness_insert(file2import,ath_un,db_host,db_name,superuser_un,superuser_pw, encr_pass)

            file2import = os.path.join(file_path_unzipped, filename)
            try:
                #Run wellness_fit_db_insert_function() within func_timeout() to limit the execution time. If the limit is reached kill the process
                func_timeout(1440,wellness_fit_db_insert_function, args=(file2import,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass))
            except FunctionTimedOut:
                pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
                if os.path.isfile(pidfile):
                    #read PID from file
                    with open(pidfile, "U") as f:
                        pid_from_file = f.read()
                    #check whether the PID from file is still running
                    if psutil.pid_exists(int(pid_from_file)):
                        p = psutil.Process(int(pid_from_file))
                        #Kill running process
                        p.kill()
                        time.sleep(1)
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + ' The insert function with PID:{} has timed out parsing and inserting data from {}. Will now clean up, and move onto next fit file !'.format(pid_from_file,file2import)))        
                continue
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                continue
        data_file_path_insert(file_path_unzipped,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
        if preserve_files == "false":
            #Remove the csv file from download folder
            rmtree(file_path_unzipped)
        else:
            #Move the csv to archive folder if the day is complete
            if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                move(file_path_unzipped,file_path_archive)
            else:
                rmtree(file_path_unzipped)
     
def dwnld_insert_json_wellness(ath_un, agent, start_date, end_date, gc_username, gc_password, mfp_username, display_name, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox, archive_radio, dbx_auth_token, encr_pass):
    
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'GC_Historical_XML_Wellness')
    archive_folder = os.path.join(download_folder, 'Archive')
    download_folder_dbx = 'GC_Historical_XML_Wellness'
    dbx_file_exists = None
  
    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create Archive directory (if it does not already exist).
    if preserve_files == "true":  
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)
         
    for single_date in daterange(start_date, end_date):
        date_in_range = single_date.strftime("%Y-%m-%d")
        url = WELLNESS % (display_name, date_in_range, date_in_range)
        json_file_name = 'Wellness_{}.json'.format(date_in_range)   
        json_file_path = os.path.join(download_folder, json_file_name)
        xml_file_name = 'Wellness_{}.xml'.format(date_in_range)
        xml_file_path = os.path.join(download_folder, xml_file_name)
        file_path_archive = os.path.join(archive_folder, xml_file_name)

        # PG Check if the file exists in dropbox.
        try:
            if archive_to_dropbox == True:
                if archive_radio == "archiveAllData" or archive_radio == "archiveFiles":
                    dbx_file_exists = check_if_file_exists_in_dbx(xml_file_name,dbx_auth_token,download_folder_dbx,encr_pass)
        except Exception as e:
             with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
        
        data_file_exists = check_data_file_exists(xml_file_path,ath_un,db_host,db_name,superuser_un,superuser_pw, encr_pass)

        #PG: Check whether the file needs to be downloaded or still exists in the download folder
        if not os.path.exists(xml_file_path):
            with StdoutRedirection(ath_un):    
                print(('{} is downloading...'.format(json_file_name)))
            with ProgressStdoutRedirection(ath_un):
                print(('{} is downloading...'.format(json_file_name)))
            
            try:
                datafile = agent.get(url).content
            except urllib.error.HTTPError as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json wellness {}. Retrying...'.format(json_file_name)))
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                try:
                    #Pause and Retry login
                    time.sleep(10)
                    agent = login(gc_username, gc_password)
                    datafile = agent.get(url).content
                    pass
                except:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json wellness {}. Aborting...'.format(json_file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #Abort and continue to next file
                    continue
            except urllib.error.URLError as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json wellness {}. Retrying...'.format(json_file_name)))
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                try: 
                    #Pause and Retry login
                    time.sleep(10)
                    agent = login(gc_username, gc_password)
                    datafile = agent.get(url).content
                    pass
                except:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json wellness {}. Aborting...'.format(json_file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #Abort and continue to next file
                    continue

            #PG:Convert wellness data from json to xml
            try:
                obj = json.loads(datafile)
                xml = dicttoxml.dicttoxml(obj)
                dom = parseString(xml)
                pretty_xml = dom.toprettyxml()
                with open(xml_file_path, "w") as f:
                    f.write(pretty_xml)
                    f.close()
                #PG:Remove "null" values from the xml file         
                with open(xml_file_path, "U") as f:
                    not_null_xml = f.read()
                    while '<value type="null"/>' in not_null_xml:
                        not_null_xml = not_null_xml.replace('<value type="null"/>', '<value type="float">0.0</value>')
                with open(xml_file_path, "w") as f:
                    f.write(not_null_xml)
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                continue

        # Archive to dbx newly downloaded file but only if the day is complete
        if dbx_file_exists == False and single_date.date() < datetime.datetime.today().date():
            download_files_to_dbx(xml_file_path,xml_file_name,dbx_auth_token,download_folder_dbx,encr_pass)
        

        #Function that combines several functions to parse the wellness xml file and insert the data to db
        def wellness_xml_db_insert_function(xml_file_path,file_path_archive,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass):
            gc_wellness_insert(xml_file_path,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass)
            data_file_path_insert(xml_file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)

        try:
            #Run fit_db_insert_function() within func_timeout() to limit the execution time. If the limit is reached kill the process
            func_timeout(1440,wellness_xml_db_insert_function, args=(xml_file_path,file_path_archive,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass))
        except FunctionTimedOut:
            pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
            if os.path.isfile(pidfile):
                #read PID from file
                with open(pidfile, "U") as f:
                    pid_from_file = f.read()
                #check whether the PID from file is still running
                if psutil.pid_exists(int(pid_from_file)):
                    p = psutil.Process(int(pid_from_file))
                    #Kill running process
                    p.kill()
                    time.sleep(1)
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + ' The insert function with PID:{} has timed out parsing and inserting data from {}. Will now clean up, and move onto next file !'.format(pid_from_file,xml_file_path)))
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
            continue
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
            continue
    with StdoutRedirection(ath_un):
        print('Welness data downloaded,converted to xml and inserted to postgeSQL database successfully')
    with ProgressStdoutRedirection(ath_un):
        print('Welness data downloaded,converted to xml and inserted to postgeSQL database successfully')
    
def dwnld_insert_json_dailysummary(ath_un, agent, start_date, end_date, gc_username, gc_password, mfp_username, display_name, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox, archive_radio, dbx_auth_token,encr_pass):
    
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'GC_Historical_XML_Wellness')
    archive_folder = os.path.join(download_folder, 'Archive')
    download_folder_dbx = 'GC_Historical_XML_Wellness'
    dbx_file_exists = None

    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder) 

    # Create Archive directory (if it does not already exist).
    if preserve_files == "true":  
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)      
    
    for single_date in daterange(start_date, end_date):
        date_in_range = single_date.strftime("%Y-%m-%d")
        url = DAILYSUMMARY % (display_name, date_in_range)
        json_file_name = '{}_summary.json'.format(date_in_range)   
        json_file_path = os.path.join(download_folder, json_file_name)
        xml_file_name = '{}_summary.xml'.format(date_in_range)
        xml_file_path = os.path.join(download_folder, xml_file_name)
        file_path_archive = os.path.join(archive_folder, xml_file_name)

        # PG Check if the file exists in dropbox.
        try:
            if archive_to_dropbox == True:
                if archive_radio == "archiveAllData" or archive_radio == "archiveFiles":
                    dbx_file_exists = check_if_file_exists_in_dbx(xml_file_name,dbx_auth_token,download_folder_dbx,encr_pass)
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

        data_file_exists = check_data_file_exists(xml_file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)

        if not os.path.exists(xml_file_path): 
            with StdoutRedirection(ath_un):    
                print(('{} is downloading...'.format(json_file_name)))
            with ProgressStdoutRedirection(ath_un):
                print(('{} is downloading...'.format(json_file_name)))
                
            try:
                datafile = agent.get(url).content
            except urllib.error.HTTPError as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json dailysummary {}. Retrying...'.format(json_file_name)))
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                try:
                    #Pause and Retry login
                    time.sleep(10)
                    agent = login(gc_username, gc_password)
                    datafile = agent.get(url).content
                    pass
                except:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json dailysummary {}. Aborting...'.format(json_file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #Abort and continue to next file
                    continue
            except urllib.error.URLError as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json dailysummary {}. Retrying...'.format(json_file_name)))
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                try: 
                    #Pause and Retry login
                    time.sleep(10)
                    agent = login(gc_username, gc_password)
                    datafile = agent.get(url).content
                    pass
                except:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json dailysummary {}. Aborting...'.format(json_file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #Abort and continue to next file
                    continue

            #PG:Convert daily_summary data from json to xml
            try:
                obj = json.loads(datafile)
                xml = dicttoxml.dicttoxml(obj)
                dom = parseString(xml)
                pretty_xml = dom.toprettyxml()
                with open(xml_file_path, "w") as f:
                    f.write(pretty_xml)
                    f.close()          
                #PG:Remove "null" values from the xml file         
                with open(xml_file_path, "U") as f:
                    not_null_xml = f.read()
                    while '<value type="null"/>' in not_null_xml:
                        not_null_xml = not_null_xml.replace('<value type="null"/>', '<value type="float">0.0</value>')
                with open(xml_file_path, "w") as f:
                    f.write(not_null_xml)
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                continue

        # PG Archive to dbx newly downloaded  file if the day is complete.
        if dbx_file_exists == False and single_date.date() < datetime.datetime.today().date():
            download_files_to_dbx(xml_file_path,xml_file_name,dbx_auth_token,download_folder_dbx,encr_pass)
        
        #Function that combines several functions to parse the dailysummary xml file and insert the data to db
        def dailysummary_xml_db_insert_function(xml_file_path,file_path_archive,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass):
            gc_dailysummary_insert(xml_file_path, ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass)
            data_file_path_insert(xml_file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete.
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
        try:
            #Run dailysummary_xml_db_insert_function() within func_timeout() to limit the execution time. If the limit is reached kill the process
            func_timeout(1440,dailysummary_xml_db_insert_function, args=(xml_file_path,file_path_archive,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass))
        except FunctionTimedOut:
            pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
            if os.path.isfile(pidfile):
                #read PID from file
                with open(pidfile, "U") as f:
                    pid_from_file = f.read()
                #check whether the PID from file is still running
                if psutil.pid_exists(int(pid_from_file)):
                    p = psutil.Process(int(pid_from_file))
                    #Kill running process
                    p.kill()
                    time.sleep(1)
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + ' The insert function with PID:{} has timed out parsing and inserting data from {}. Will now clean up, and move onto next file !'.format(pid_from_file,xml_file_path)))        
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
            continue
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
            continue

        with StdoutRedirection(ath_un):
            print('DailySummary data downloaded,converted to xml and inserted to postgeSQL database successfully')
        with ProgressStdoutRedirection(ath_un): 
            print('DailySummary data downloaded,converted to xml and inserted to postgeSQL database successfully')


def dwnld_insert_json_body_composition(ath_un, agent, start_date, end_date, gc_username, gc_password, mfp_username, output, db_host, db_name, superuser_un,superuser_pw, archive_to_dropbox, archive_radio, dbx_auth_token, encr_pass):
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'GC_Historical_XML_Wellness')
    archive_folder = os.path.join(download_folder, 'Archive')
    download_folder_dbx = 'GC_Historical_XML_Wellness'
    dbx_file_exists = None
    
    json_file_name = 'Body_composition_{}.json'.format(start_date)   
    json_file_path = os.path.join(download_folder, json_file_name)
    xml_file_name = 'Body_composition_{}.xml'.format(start_date)
    xml_file_path = os.path.join(download_folder, xml_file_name)

    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create Archive directory (if it does not already exist).
    if preserve_files == "true":  
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)

    for single_date in daterange(start_date, end_date):
        date_in_range = single_date.strftime("%Y-%m-%d")
        epoch_single_date = str(getDateToEpoch(single_date))
        url = BODY_COMPOSION % (epoch_single_date,epoch_single_date)
        json_file_name = 'Body_Composition_{}.json'.format(date_in_range)   
        json_file_path = os.path.join(download_folder, json_file_name)
        xml_file_name = 'Body_composition_{}.xml'.format(date_in_range)
        xml_file_path = os.path.join(download_folder, xml_file_name)
        file_path_archive = os.path.join(archive_folder, xml_file_name)

        # PG Check if the file exists in dropbox.
        try:
            if archive_to_dropbox == True:
                if archive_radio == "archiveAllData" or archive_radio == "archiveFiles":
                    dbx_file_exists = check_if_file_exists_in_dbx(xml_file_name,dbx_auth_token,download_folder_dbx,encr_pass)
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

        data_file_exists = check_data_file_exists(xml_file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)

        #PG: Check whether the file needs to be downloaded or still exists in the download folder
        if not os.path.exists(xml_file_path):

            with StdoutRedirection(ath_un):    
                print(('{} is downloading...'.format(json_file_name)))
            with ProgressStdoutRedirection(ath_un):
                print(('{} is downloading...'.format(json_file_name)))
            
            try:
                datafile = agent.get(url).content
            except urllib.error.HTTPError as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json body composition {}. Retrying...'.format(json_file_name)))
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                try:
                    #Pause and Retry login
                    time.sleep(10)
                    agent = login(gc_username, gc_password)
                    datafile = agent.get(url).content
                    pass
                except:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json body composition {}. Aborting...'.format(json_file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #Abort and continue to next file
                    continue
            except urllib.error.URLError as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json body composition {}. Retrying...'.format(json_file_name)))
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                try: 
                    #Pause and Retry login
                    time.sleep(10)
                    agent = login(gc_username, gc_password)
                    datafile = agent.get(url).content
                    pass
                except:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + 'The GarminConnect server couldn\'t fulfill the request downloading json body composition {}. Aborting...'.format(json_file_name)))
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                    #Abort and continue to next file
                    continue
            
            #PG:Convert wellness data from json to xml
            try:
                obj = json.loads(datafile)
                xml = dicttoxml.dicttoxml(obj)
                dom = parseString(xml)
                pretty_xml = dom.toprettyxml()
                with open(xml_file_path, "w") as f:
                    f.write(pretty_xml)
                    f.close()
                #PG:Remove "null" values from the xml file         
                with open(xml_file_path, "U") as f:
                    not_null_xml = f.read()
                    while '<value type="null"/>' in not_null_xml:
                        not_null_xml = not_null_xml.replace('<value type="null"/>', '<value type="float">0.0</value>')
                with open(xml_file_path, "w") as f:
                    f.write(not_null_xml)
            except Exception as e:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
                continue

        # Archive to dbx newly downloaded file but only if the day is complete
        if dbx_file_exists == False and single_date.date() < datetime.datetime.today().date():
            download_files_to_dbx(xml_file_path,xml_file_name,dbx_auth_token,download_folder_dbx,encr_pass)


        #Function that combines several functions to parse the bodycomposition xml file and insert the data to db
        def bodycomposition_xml_db_insert_function(xml_file_path,file_path_archive,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass):
            gc_bodycomposition_insert(xml_file_path,ath_un, db_host,db_name,superuser_un,superuser_pw,encr_pass)
            data_file_path_insert(xml_file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
        try:
            #bodycomposition_xml_db_insert_function() within func_timeout() to limit the execution time. If the limit is reached kill the process
            func_timeout(1440,bodycomposition_xml_db_insert_function, args=(xml_file_path,file_path_archive,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass))
        except FunctionTimedOut:
            pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
            if os.path.isfile(pidfile):
                #read PID from file
                with open(pidfile, "U") as f:
                    pid_from_file = f.read()
                #check whether the PID from file is still running
                if psutil.pid_exists(int(pid_from_file)):
                    p = psutil.Process(int(pid_from_file))
                    #Kill running process
                    p.kill()
                    time.sleep(1)
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + ' The insert function with PID:{} has timed out parsing and inserting data from {}. Will now clean up, and move onto next file !'.format(pid_from_file,xml_file_path)))        
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
            continue
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(xml_file_path)
            else:
                #Move the csv to archive folder if the day is complete
                if not os.path.exists(file_path_archive) and single_date.date() < datetime.datetime.today().date():
                    os.rename(xml_file_path,file_path_archive)
                else:
                    os.remove(xml_file_path)
            continue

        with StdoutRedirection(ath_un):
            print('Body Composition data downloaded,converted to xml and inserted to postgeSQL database successfully')
        with ProgressStdoutRedirection(ath_un): 
            print('Body Composition data downloaded,converted to xml and inserted to postgeSQL database successfully')

