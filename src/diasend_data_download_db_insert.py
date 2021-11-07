import mechanize as me
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import base64
import datetime
from python_anticaptcha import AnticaptchaClient, ImageToTextTask, AnticatpchaException
import psycopg2
from database_ini_parser import config
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
import Crypto.Random
from Crypto.Cipher import AES
from db_user_insert import diasend_user_insert
from processify import processify
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
import sys
from archive_data_dropbox import check_if_file_exists_in_dbx, download_files_to_dbx
from db_files import data_file_path_insert,check_data_file_exists

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
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt  

@processify
def diasend_data_export_insert(output,start_date,end_date,ath_un,cgm_username,cgm_password,encr_pass,save_pwd,archive_to_dropbox,archive_radio,dbx_auth_token,db_host,superuser_un,superuser_pw):
    agent = me.Browser()    
    agent.set_handle_robots(False)   # no robots
    agent.set_handle_refresh(False)  # can sometimes hang without this
    agent.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2')]

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    path_params = config(filename="encrypted_settings.ini", section="path")
    TEMP_FILE_PATH = str(path_params.get("pid_file_dir"))

    anticaptcha_params = config(filename="encrypted_settings.ini", section="anticaptcha", encr_pass=encr_pass)
    api_key = str(anticaptcha_params.get("api_key"))

    path_params = config(filename="encrypted_settings.ini", section="archive")
    preserve_files = str(path_params.get("preserve_files"))

    login_url = 'https://diasend.com//'
    export_data_url = 'https://international.diasend.com/patient/account/export-data'
    login_form_action = 'https://international.diasend.com/diasend/includes/account/login.php'
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'CGM_Historical_BG')
    archive_folder = os.path.join(download_folder, 'Archive')
    download_folder_dbx = 'CGM_Historical_BG'
    dbx_file_exists = None
    xls_export_file = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '_diasend_export.xls'
    xls_file_path = os.path.join(download_folder, xls_export_file)
    captcha_file_path = os.path.join(TEMP_FILE_PATH, ath_un + '_captcha.jpg')
    solved_captcha_file_path = os.path.join(TEMP_FILE_PATH, ath_un + '_captcha.txt')

    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create Archive directory (if it does not already exist).
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    if save_pwd == True:
        encrypted_pwd = base64.b64encode(encrypt(cgm_password, encr_pass))
        encrypted_pwd = encrypted_pwd.decode('utf-8')
    else:
        encrypted_pwd = None

    # Open 'Login' url
    agent.open(login_url)
    # Set up the login form.
    agent.select_form(nr=1)

    country_dropdown = agent.find_control(name='country')
    country_dropdown.readonly = False
    locale = agent.find_control(name='locale')
    locale.readonly = False
    
    agent.form['country'] = '1000'
    agent.form['locale']  = 'en_US'
    agent.form['user'] = cgm_username
    agent.form['passwd'] = cgm_password

    # Submit the login!
    agent.form.action = login_form_action
    res_login = agent.submit()

    # Open 'Export Data' url
    export_data = agent.open(export_data_url)
    # Get base64 captcha image
    soup = BeautifulSoup(export_data)
    captcha = soup('img', alt='CAPTCHA code')
    captcha_src = captcha[0]
    img_data = captcha_src['src']
    # Decode base64 captcha image
    b64_data = img_data.replace('data:image/jpeg;base64,', '')
    imgdata = base64.b64decode(b64_data)
    # Save decoded image
    with open(captcha_file_path, 'wb') as f:
        f.write(imgdata)

    # Solve captcha (experimental, relies on a third party paid service)
    try:
        captcha_fp = open(captcha_file_path, 'rb')
        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        solved_captcha = job.get_captcha_text()
        #Save solved captcha in a text file for debuging and manual accuracy check
        #with open(solved_captcha_file_path, 'wb') as f:
            #f.write(solved_captcha)
    except AnticatpchaException as e:
        if e.error_code == 'ERROR_ZERO_BALANCE':
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e.error_id, e.error_code, e.error_description)))
        else:
            raise
     
    # Set up the download form.
    agent.select_form(nr=0)
    agent['code'] = solved_captcha
    agent.set_handle_robots(False)   # no robots
    agent.set_handle_refresh(False)  # can sometimes hang without this

    # Submit the captcha!
    res_download = agent.submit()
    
    # Write download to xls file
    try:
        fileobj = open(xls_file_path,"wb")
        fileobj.write(res_download.read())
    except Exception as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
    finally:
        fileobj.close()
    
    db_name = str(str2md5(ath_un)) + '_Athlete_Data_DB'
    conn = None
    #PG: insert Diasend user credentials into database
    diasend_user_insert(cgm_username,encrypted_pwd,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass) 

    # connect to the PostgreSQL server
    with StdoutRedirection(ath_un):
        print('Connecting to the PostgreSQL server to insert CGM data...')
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

    # Iterate over files in the download directory and insert data to db
    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)
        # PG Check if the file exists in dropbox.
        try:
            if archive_to_dropbox == True:
                if archive_radio == "archiveAllData" or archive_radio == "archiveFiles":
                    dbx_file_exists = check_if_file_exists_in_dbx(filename,dbx_auth_token,download_folder_dbx,encr_pass)
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

        #PG: Check whether the data from this file "file_path" have been inserted into to DB during one of the previous runs
        data_file_exists = check_data_file_exists(file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
        if data_file_exists == True:
            with StdoutRedirection(ath_un):
                print(('{} already exists in {}. Skipping.'.format(filename, download_folder)))
            with ProgressStdoutRedirection(ath_un):
                print(('{} already exists in {}. Skipping.'.format(filename, download_folder)))
            # PG Archive to dbx already localy existing file
            if dbx_file_exists == False:
                download_files_to_dbx(file_path,filename,dbx_auth_token,download_folder_dbx,encr_pass)
            #Move the csv to archive folder
            if not os.path.exists(os.path.join(archive_folder,filename)):
                os.rename(os.path.join(download_folder,filename), os.path.join(archive_folder,filename))
            else:
                #Remove the csv file from download folder
                os.remove(os.path.join(download_folder,filename))
            continue

        sql = """

            INSERT INTO diasend_cgm(athlete_id,timestamp,glucose_nmol_l,data_source)

            VALUES
            ((select id from athlete where ath_un=%s),%s,%s,%s)

            ON CONFLICT (athlete_id,timestamp) DO NOTHING;
            
            """

        # Read/Parse the .xls file ('Name and glucose' worksheet)
        try:
            z_filename, z_file_extension = os.path.splitext(file_path)
            if z_file_extension == '.xls':
                dataset = pd.read_excel(file_path, sheet_name="CGM", header=None, skiprows=5) #Parse CGM worksheet
                #Parse Glucose worksheet use: dataset = pd.read_excel(file_path, header=None, skiprows=5)
            else:
                continue
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +'  '+str(file_path)+': '+ str(e)))
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) +'  '+str(file_path)+' could not be imported and will be deleted.'))
                os.remove(file_path)
            continue

        with StdoutRedirection(ath_un):
            print(('Parsing and Inserting cgm records from '+str(filename)+'....'))
        with ProgressStdoutRedirection(ath_un):
            print(('Parsing and Inserting cgm records from '+str(filename)+'....'))
        for row in dataset.itertuples():
            timestamp = row._1 # Format: 01/01/2017 00:21
            timestamp_dt = datetime.datetime.strptime((timestamp), "%d/%m/%Y %H:%M")
            timestamp_str = datetime.datetime.strftime((timestamp_dt), '%Y-%m-%d %H:%M:%S')

            # Compare if the Record Date is within the download Date range. This only works if parsed from top of the csv file.
            if timestamp_dt > end_date + datetime.timedelta(days=1): 
                continue
            if timestamp_dt < start_date:
                break 

            glucose = float(row._2)
            with StdoutRedirection(ath_un):
                print(('Time: '+str(timestamp_str)+'  Glucose: '+str(glucose)))
            # Insert parsed data to db
            try:
                # create a cursor
                cur = conn.cursor()
                # execute a statement
                cur.execute(sql,(ath_un,timestamp_str,glucose,"diasend_web"))
                conn.commit()
                # close the communication with the PostgreSQL
                cur.close()
                
            except  (Exception, psycopg2.DatabaseError) as error:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))
        
        # PG Archive to dbx newly downloaded file
        if dbx_file_exists == False:
            download_files_to_dbx(file_path,filename,dbx_auth_token,download_folder_dbx,encr_pass)
        
        try:
            data_file_path_insert(file_path,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            #Move the csv to archive folder
            if not os.path.exists(os.path.join(archive_folder,filename)):
                os.rename(os.path.join(download_folder,filename), os.path.join(archive_folder,filename))
            else:
                #Remove the csv file from download folder
                os.remove(os.path.join(download_folder,filename))
        except Exception as e:
            with ErrorStdoutRedirection(ath_un):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

        with StdoutRedirection(ath_un):
            print(('Diasend cgm records from '+str(filename)+' inserted successfully'))
        with ProgressStdoutRedirection(ath_un):
            print(('Diasend cgm records from '+str(filename)+' inserted successfully'))

    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close() 

