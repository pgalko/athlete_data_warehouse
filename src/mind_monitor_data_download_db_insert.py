import pandas as pd
import os
import datetime
import psycopg2
from database_ini_parser import config
import base64
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
import Crypto.Random
from Crypto.Cipher import AES
from db_user_insert import mm_user_insert
from db_files import data_file_path_insert,check_data_file_exists
import urllib.request, urllib.error, urllib.parse
import zipfile
import io
from processify import processify
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection,ConsolidatedProgressStdoutRedirection
import sys

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
def mm_data_insert(output,start_date,end_date,ath_un,encr_pass,mm_dbx_link,save_pwd,db_host,db_name,superuser_un,superuser_pw):
    # Before executing the script go to your droppox Apps/Mind Monitor folder.
    # Right click on the folder, select 'Share' option and copy the generated link.
    # Assign the link string to the 'mm_dbx_link' parameter.
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'MM_Historical_EEG')
    archive_folder = os.path.join(download_folder, 'Archive')

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    path_params = config(filename="encrypted_settings.ini", section="archive")
    preserve_files = str(path_params.get("preserve_files"))

    if save_pwd == True:
        encrypted_link = base64.b64encode(encrypt(mm_dbx_link, encr_pass))
        encrypted_link = encrypted_link.decode('utf-8')
    else:
        encrypted_link = None

    #PG: insert MM export link into database
    mm_user_insert(encrypted_link,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
    

    # Download the MM export csv file from dropbox using share link 
    mm_dbx_link = mm_dbx_link[:-1]+'1' # Replace the 0 at the end of the link with 1.Will download as .zip file.
    response = urllib.request.urlopen(mm_dbx_link)

    # Extract the downloaded folder in to variable
    compressedFile = io.BytesIO()
    compressedFile.write(response.read())
    compressedFile.seek(0)

    #Check if the date variable are of string or datetime type
    if type(start_date)==str:#Script run as standalone 
        start_date_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    else:#Script run from flask server (variable passes as datetime type)
        start_date_dt = start_date
    if type(end_date)==str:#Script run as standalone
        end_date_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    else:#Script run from flask server (variable passes as datetime type)
        end_date_dt = end_date

    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create Archive directory (if it does not already exist).
    if preserve_files == "true":  
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)

    with zipfile.ZipFile(compressedFile, 'r') as z:
        #List the content of the zip file
        zipfile_content = z.namelist() 
        #Iterate through list and only extract files within date range
        for item in zipfile_content:
            #Extract date from filename
            item_date = item[12:22]
            if item_date != '':
                item_date_dt = datetime.datetime.strptime(item_date, "%Y-%m-%d")
            else:
                continue
            # Check if the file date is within the download Date range.
            if item_date_dt > end_date_dt + datetime.timedelta(days=1) or item_date_dt < start_date_dt: 
                continue
            else:
                #PG: Check whether the data from this file "file_path" have been inserted into to DB during one of the previous runs
                data_file_exists = check_data_file_exists(os.path.join(download_folder,item),ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
                if data_file_exists == True:
                    with StdoutRedirection(ath_un):
                        print(('{} already exists in {}. Skipping.'.format(item, download_folder)))
                    with ProgressStdoutRedirection(ath_un):
                        print(('{} already exists in {}. Skipping.'.format(item, download_folder)))
                    continue
                z.extract(item,download_folder)
                #Insert filepath into the db
                try:
                    data_file_path_insert(os.path.join(download_folder,item),ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)           
                except Exception as e:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

    for filename in os.listdir(download_folder):
        if filename.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(download_folder,filename), 'r') as z:
                z.extractall(download_folder)
            os.remove(os.path.join(download_folder,filename))
            with StdoutRedirection(ath_un):
                print(('The content of \"{}\" extracted into csv and the original removed'.format(filename)))
            with ProgressStdoutRedirection(ath_un):
                print(('The content of \"{}\" extracted into csv and the original removed'.format(filename)))

    db_name = str(str2md5(ath_un)) + '_Athlete_Data_DB'

    conn = None
         
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

    sql = """

        INSERT INTO mind_monitor_eeg(timestamp,delta_tp9,
        delta_af7,delta_af8,delta_tp10,athlete_id,theta_tp9,theta_af7,theta_af8,theta_tp10,alpha_tp9,alpha_af7,alpha_af8,alpha_tp10,beta_tp9,beta_af7,beta_af8,
        beta_tp10,gamma_tp9,gamma_af7,gamma_af8,gamma_tp10,raw_tp9,raw_af7,raw_af8,raw_tp10,aux_right,accelerometer_x,accelerometer_y,accelerometer_z,
        gyro_x,gyro_y,gyro_z,head_band_on,hsi_tp9,hsi_af7,hsi_af8,hsi_tp10,battery,elements,timestamp_gmt)

        VALUES
        (%s,%s,%s,%s,%s,(select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (athlete_id,timestamp) DO NOTHING;
        
    """

    sql_local2gmt = """

        SELECT gmt_local_difference FROM gmt_local_time_difference WHERE local_date = %s;

    """

    for filename in os.listdir(download_folder):
        if filename.endswith(".csv"):        
            # Read/Parse the .csv file and load the data into pandas dataset
            with StdoutRedirection(ath_un):
                print(('Parsing and inserting the content of \"{}\" into the DB'.format(filename)))
            with ProgressStdoutRedirection(ath_un):
                print(('Parsing and inserting the content of \"{}\" into the DB'.format(filename)))
            dataset = pd.read_csv(os.path.join(download_folder,filename), sep=",",header=None)
            dataset.drop(dataset.index[:1], inplace=True) #Drop the first row

            for row in dataset.itertuples():
                local_time = row._1
                local_time_dt = datetime.datetime.strptime((local_time), "%Y-%m-%d %H:%M:%S.%f")
                local_time_str = datetime.datetime.strftime(local_time_dt,"%Y-%m-%d %H:%M:%S.%f")
                local_date_str = datetime.datetime.strftime((local_time_dt), "%Y-%m-%d")
                utc_time_str = None
                delta_tp9 = row._2
                delta_af7 = row._3
                delta_af8 = row._4
                delta_tp10 = row._5
                theta_tp9 = row._6
                theta_af7 = row._7
                theta_af8 = row._8
                theta_tp10 = row._9
                alpha_tp9 = row._10
                alpha_af7 = row._11
                alpha_af8 = row._12
                alpha_tp10 = row._13
                beta_tp9 = row._14
                beta_af7 = row._15
                beta_af8 = row._16
                beta_tp10 = row._17
                gamma_tp9 = row._18
                gamma_af7 = row._19
                gamma_af8 = row._20
                gamma_tp10 = row._21
                raw_tp9 = row._22
                raw_af7 = row._23
                raw_af8 = row._24
                raw_tp10 = row._25
                aux_right = row._26
                accelerometer_x = row._27
                accelerometer_y = row._28
                accelerometer_z = row._29
                gyro_x = row._30
                gyro_y = row._31
                gyro_z = row._32
                head_band_on = row._33
                hsi_tp9 = row._34
                hsi_af7 = row._35
                hsi_af8 = row._36
                hsi_tp10 = row._37
                battery = row._38
                elements = row._39
                
                # Check if the Record Date is within the download Date range.
                if local_time_dt > end_date_dt + datetime.timedelta(days=1) or local_time_dt < start_date_dt: 
                    break
                else:
                    try:
                        # create a cursor
                        cur = conn.cursor()
                        # execute a statement
                        cur.execute(sql_local2gmt,(local_date_str,))
                        result = cur.fetchone()
                        # close the communication with the PostgreSQL
                        conn.commit()
                        cur.close()
                        if result is not None:
                            utc_time_dt = local_time_dt - result[0]
                            utc_time_str = datetime.datetime.strftime((utc_time_dt), "%Y-%m-%d %H:%M:%S.%f")
                    except (Exception, psycopg2.DatabaseError) as error:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.now()) + '  ' + str(error))) 
                    try:
                        # create a cursor
                        cur = conn.cursor()
                        # execute a statement
                        cur.execute(sql,(local_time_str,delta_tp9,delta_af7,delta_af8,delta_tp10,ath_un,theta_tp9,theta_af7,theta_af8,theta_tp10,alpha_tp9,alpha_af7,alpha_af8,
                                        alpha_tp10,beta_tp9,beta_af7,beta_af8,beta_tp10,gamma_tp9,gamma_af7,gamma_af8,gamma_tp10,raw_tp9,raw_af7,raw_af8,raw_tp10,aux_right,accelerometer_x,accelerometer_y,accelerometer_z,
                                        gyro_x,gyro_y,gyro_z,head_band_on,hsi_tp9,hsi_af7,hsi_af8,hsi_tp10,battery,elements,utc_time_str))
                        conn.commit()
                        # close the communication with the PostgreSQL
                        cur.close()
                        
                    except (Exception, psycopg2.DatabaseError) as error:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.now()) + '  ' + str(error)))

            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(os.path.join(download_folder,filename))
                with StdoutRedirection(ath_un):
                    print(('The content of \"{}\" parsed and inserted into DB and the original csv file removed'.format(filename)))
                with ProgressStdoutRedirection(ath_un):
                    print(('The content of \"{}\" parsed and inserted into DB and the original csv file removed'.format(filename)))

            else:
                #Move the csv to archive folder
                if not os.path.exists(os.path.join(archive_folder,filename)):
                    os.rename(os.path.join(download_folder,filename), os.path.join(archive_folder,filename))
                    with StdoutRedirection(ath_un):
                        print(('The content of \"{}\" parsed and inserted into DB and the original csv file archived'.format(filename)))
                    with ProgressStdoutRedirection(ath_un):
                        print(('The content of \"{}\" parsed and inserted into DB and the original csv file archived'.format(filename)))
                else:
                    #Remove the csv file from download folder
                    os.remove(os.path.join(download_folder,filename))

    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close() 
