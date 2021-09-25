
import pandas as pd
import numpy as np
import os
import re
import datetime
import psycopg2
from database_ini_parser import config
import base64
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
import Crypto.Random
from Crypto.Cipher import AES
from db_user_insert import glimp_user_insert,libreview_user_insert
import urllib.request, urllib.error, urllib.parse
import gzip
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
def glimp_data_insert(output,start_date,end_date,ath_un,encr_pass,glimp_dbx_link,save_pwd,db_host,db_name,superuser_un,superuser_pw):
    # Before executing the script go to your droppox Apps/Glimp folder and locate ClicemiaMisurazioni.csv.gz file.
    # Right click on the file, select 'Share' option and copy the generated link.
    # Assign the link string to the 'glimp_dbx_link' parameter.
    glimp_export_csv = 'GlicemiaMisurazioni.csv'
    glimp_export_csv_gz = 'GlicemiaMisurazioni.csv.gz'
    user_output = os.path.join(output, ath_un)
    download_folder = os.path.join(user_output, 'CGM_Historical_BG')
    archive_folder = os.path.join(download_folder, 'Archive')
    glimp_file_path = os.path.join(download_folder, glimp_export_csv)
    glimp_file_path_gz = os.path.join(download_folder, glimp_export_csv_gz)

    #Get PID of the current process and write it in the file
    pid = str(os.getpid())
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    path_params = config(filename="encrypted_settings.ini", section="archive")
    preserve_files = str(path_params.get("preserve_files"))

    if save_pwd == True:
        encrypted_link = base64.b64encode(encrypt(glimp_dbx_link, encr_pass))
        encrypted_link = encrypted_link.decode('utf-8')
    else:
        encrypted_link = None

    #Check if the date variable are of string or datetime type
    if type(start_date)==str:#Script runs as standalone 
        start_date_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    else:#Script runs from flask server (variable passes as datetime type)
        start_date_dt = start_date
    if type(end_date)==str:#Script run as standalone
        end_date_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    else:#Script runs from flask server (variable passes as datetime type)
        end_date_dt = end_date

    # Download the glimp export csv file from dropbox using share link 
    glimp_dbx_link = glimp_dbx_link[:-1]+'1' # Replace the 0 at the end of the link with 1.
    response = urllib.request.urlopen(glimp_dbx_link)
    # Extract the downloaded file
    compressedFile = io.BytesIO()
    compressedFile.write(response.read())
    compressedFile.seek(0)

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
        #Iterate through list and only extract files matching the name
        for item in zipfile_content:
            if item == glimp_export_csv_gz:#The File is generated by Glimp app
                z.extract(item,download_folder)
                # Write the extracted content to a new csv file
                glimp_export = gzip.GzipFile(glimp_file_path_gz, mode='rb')
                with open(glimp_file_path, 'wb') as f:
                    f.write(glimp_export.read())
                glimp_export.close
                #os.remove(os.path.join(download_folder,item)) #Delete the GZ file after content extracted
            else:#The file is manualy download from LibreView
                z.extract(item,download_folder)
    db_name = str(str2md5(ath_un)) + '_Athlete_Data_DB'

    conn = None
         
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

    sql = """

        INSERT INTO diasend_cgm(athlete_id,timestamp,glucose_nmol_l,glucose_nmol_l_15min_avrg,ketone_nmol_l,data_source,timestamp_gmt)

        VALUES
        ((select id from athlete where ath_un=%s),%s,%s,%s,%s,%s,%s)

        ON CONFLICT (athlete_id,timestamp,data_source) DO NOTHING;
        
        """

    sql_local2gmt = """

        SELECT gmt_local_difference FROM gmt_local_time_difference WHERE local_date = %s;

    """

    def parse_dataset(dataset,conn,start_date_dt,end_date_dt,data_source):
        for row in dataset.itertuples():
            glucose_nmol = None
            glucose_nmol_avrg = None
            ketone_nmol = None
            utc_time_str = None
            if data_source == 'glimp_android':
                record_type = row._9 #Current(5) or 15min average(3)
                if record_type == 5:
                    glucose_nmol = round((float(row._6)/18),2)
                else:
                    glucose_nmol_avrg = round((float(row._6)/18),2)
                local_time = row._2
                epoch_time = row._3
                local_time_dt = datetime.datetime.strptime((local_time), "%d/%m/%Y %H.%M.%S")
                local_time_str = datetime.datetime.strftime((local_time_dt), "%Y-%m-%d %H:%M:%S")
                utc_time_str = datetime.datetime.utcfromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
            else:
                ketone_nmol = row._7
                glucose_nmol = row._6
                glucose_nmol_avrg = row._5
                local_time = row._3
                local_time_dt = local_time.to_pydatetime()#Convert from pandas to python datetime
                local_time_str = datetime.datetime.strftime((local_time_dt), "%Y-%m-%d %H:%M:%S")
                local_date_str = datetime.datetime.strftime((local_time_dt), "%Y-%m-%d")
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
                        utc_time_str = datetime.datetime.strftime((utc_time_dt), "%Y-%m-%d %H:%M:%S")
                except (Exception, psycopg2.DatabaseError) as error:
                    with ErrorStdoutRedirection(ath_un):
                        print((str(datetime.now()) + '  ' + str(error)))

            # Compare if the Record Date is within the download Date range. This only works if parsed from top of the csv file.
            # The most recent record at the top 
            if local_time_dt > end_date_dt + datetime.timedelta(days=1): 
                continue
            if local_time_dt < start_date_dt:
                break 

            with ProgressStdoutRedirection(ath_un):
                print(('Inserting BG record from Glimp/LibreView. Time: '+str(local_time_str)+'  Glucose: '+str(glucose_nmol)))
            with StdoutRedirection(ath_un):
                print(('Inserting BG record from Glimp/LibreView. Time: '+str(local_time_str)+'  Glucose: '+str(glucose_nmol)))

            try:
                # create a cursor
                cur = conn.cursor()
                # execute a statement
                cur.execute(sql,(ath_un,local_time_str,glucose_nmol,glucose_nmol_avrg,ketone_nmol,data_source,utc_time_str))
                conn.commit()
                # close the communication with the PostgreSQL
                cur.close()
                
            except (Exception, psycopg2.DatabaseError) as error:
                with ErrorStdoutRedirection(ath_un):
                    print((str(datetime.now()) + '  ' + str(error)))

    # Iterate throught files in the download folder
    for item in os.listdir(download_folder):
        #The file is an export from Glimp app
        if item == glimp_export_csv:
            #Insert Glimp export link into database
            glimp_user_insert(encrypted_link,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            data_source = 'glimp_android'
            # Read/Parse the .csv file
            dataset = pd.read_csv(glimp_file_path, sep=";", encoding='UTF-16 LE', header=None)
            parse_dataset(dataset,conn,start_date_dt,end_date_dt,data_source)
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(os.path.join(download_folder,item))
            else:
                #Move the csv to archive folder
                if not os.path.exists(os.path.join(archive_folder,item)):
                    os.rename(os.path.join(download_folder,item), os.path.join(archive_folder,item))
                else:
                    os.remove(os.path.join(download_folder,item))
        #The file is an export from LibreView
        elif re.match(r"^[a-zA-Z0-9]+_glucose_[0-9|-]+.csv",item): #Search for pattern FirstLast_glucose_dd-mm-yyyy.csv
            #Insert LIbreView export link into database
            libreview_user_insert(encrypted_link,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
            data_source = 'libre_view'
            dataset = pd.read_csv(os.path.join(download_folder,item), sep=",",skiprows=1)
            dataset = dataset.iloc[:, [0,1,2,3,4,5,15]]# Keep first 6 columns and column 16 and drop everything else
            dataset['Device Timestamp'] = pd.to_datetime(dataset['Device Timestamp'],format="%d-%m-%Y %H:%M")
            dataset = dataset.sort_values(by='Device Timestamp',ascending=False)
            dataset = dataset.dropna(subset = ['Historic Glucose mmol/L', 'Scan Glucose mmol/L','Ketone mmol/L'],thresh=1)#Drop row if NaN in all three columns
            dataset = dataset.replace({np.nan: None})#Replace NaN values with None
            parse_dataset(dataset,conn,start_date_dt,end_date_dt,data_source)
            if preserve_files == "false":
                #Remove the csv file from download folder
                os.remove(os.path.join(download_folder,item))
            else:
                #Move the csv to archive folder
                if not os.path.exists(os.path.join(archive_folder,item)):
                    os.rename(os.path.join(download_folder,item), os.path.join(archive_folder,item))
                else:
                    os.remove(os.path.join(download_folder,item))
        else:
            continue
   
    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close() 
