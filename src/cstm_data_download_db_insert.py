import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras
import urllib.request, urllib.error, urllib.parse
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
from database_ini_parser import config
from db_encrypt import str2md5
from processify import processify
import zipfile
import io
import os
import sys
import re
import datefinder
import datetime
import pytz
from string import punctuation
import csv
from db_user_insert import cstm_user_insert


#Function to format header names
def format_column_name(header):
    if type(header) is int:
        header = "clmn_{}".format(str(header))
    for i in header:
        # check whether the char is punctuation. Replace with "_" if match.
        if i in punctuation: 
            header = header.replace(i, "_")
    #convert to lowercase
    header = header.lower()
    #replace spaces with "_"
    header = header.replace(" ","_")
    #replace double "__" with "_"
    header = header.replace("__","_")
    #remove first character if "_"
    if header[0] == "_":
        header = header[1:]
    #remove last character if "_"
    if header[-1] == "_":
        header = header[:-1]
    return header

def csv_match_columns2data(ath_un,csv_data):
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(csv_data.read())
    delimiter = dialect.delimiter
    csv_data.seek(0)#Move pointer to the beginning
    for i, line in enumerate(csv_data):
        if i == 0:
            headerCount = line.count(delimiter)
        elif i == 1:
            dataCount = line.count(delimiter)  
            if (headerCount != dataCount):
                with ProgressStdoutRedirection(ath_un):
                    print("Warning: Header and data size mismatch in {}. Columns beyond header size will be removed.".format(csv))        
        elif i > 1:
            break
    return range(dataCount)

#Function to generate create cstm table sql query
def gen_tbl_sql(df,table_name,unique):
    dmap = {'object' : 'CHARACTER VARYING',
        'int64' : 'BIGINT',
        'float64' : 'NUMERIC',
        'datetime64' : 'TIMESTAMP',
        'bool' : 'BOOLEAN',
        'category' : 'CHARACTER VARYING',
        'timedelta[ns]' : 'CHARACTER VARYING'}
    sql_columns_list = "(id INTEGER NOT NULL"
    df1 = df.rename(columns = {"" : "clmn_noname"})
    hdrs = df1.dtypes.index
    hdrs_list = [(hdr, str(df1[hdr].dtype)) for hdr in hdrs]
    for i, hl in enumerate(hdrs_list):
        sql_columns_list += ", {} {}".format(hl[0], dmap[hl[1]])

    sql_table_owner = "ALTER TABLE public.{0} OWNER TO postgres;".format(table_name)
    sql_create_sequence = "CREATE SEQUENCE public.{0}_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;".format(table_name)
    sql_alter_table_1 = "ALTER TABLE public.{0}_id_seq OWNER TO postgres;".format(table_name)
    sql_alter_sequence = "ALTER SEQUENCE public.{0}_id_seq OWNED BY public.{0}.id;".format(table_name)
    sql_alter_table_2 = "ALTER TABLE ONLY public.{0} ALTER COLUMN id SET DEFAULT nextval('public.{0}_id_seq'::regclass);".format(table_name)
    sql_primary_key = "ALTER TABLE ONLY public.{0} ADD CONSTRAINT {0}_pkey PRIMARY KEY (id);".format(table_name)
    sql_unique = "ALTER TABLE ONLY public.{0} ADD CONSTRAINT unique_{0} UNIQUE ({1});".format(table_name,','.join(unique))
    sql_foreign_key = "ALTER TABLE ONLY public.{0} ADD CONSTRAINT fk_{0}_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);".format(table_name)
    sql_create_custom_table = "CREATE TABLE IF NOT EXISTS public.{0} {1}); {2} {3} {4} {5} {6} {7} {8} {9}".format(table_name,sql_columns_list,sql_table_owner,sql_create_sequence,
                                                                                     sql_alter_table_1,sql_alter_sequence,sql_alter_table_2,sql_primary_key,
                                                                                     sql_unique,sql_foreign_key)

    return sql_create_custom_table

#Function to insert dataframe values to db
@processify
def insert_df_values(ath_un,conn, datafrm, table,unique):
    # Creating a list of tupples from the dataframe values
    tpls = [tuple(x) for x in datafrm.to_numpy()]
    # dataframe columns with Comma-separated
    cols = ','.join(list(datafrm.columns))
    unique = ','.join(unique)

    # SQL query to execute
    sql = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT (%s) DO NOTHING;" % (table, cols, unique)
    cur = conn.cursor()
    try:
        psycopg2.extras.execute_values(cur, sql, tpls)
        conn.commit()
        with StdoutRedirection(ath_un):
            print('Custom data succesfully inserted to: {}'.format(table))
        with ProgressStdoutRedirection(ath_un):
            print('Custom data succesfully inserted to: {}'.format(table)) 
    except (Exception, psycopg2.DatabaseError) as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

        cur.close()

#Main function to parse csv, convert to df and insert the values to db
def cstm_data_insert(ath_un,usr_params_str,usr_params_int,db_host,superuser_un,superuser_pw):
    cstm_dbx_link = usr_params_str[0]
    download_folder = usr_params_str[1]
    download_folder = os.path.join(download_folder, 'CSTM_Temp_CSV')
    archive_folder = os.path.join(download_folder, 'Archive')
    table_name = usr_params_str[2]
    date_format = usr_params_str[3]
    timezone = usr_params_str[4]
    datetime_clmn = usr_params_str[5]
    unique = usr_params_int
    dataframes = []

    # Download the csv file from dropbox using share link
    with StdoutRedirection(ath_un):
        print('Downloading custom csv files from: {}'.format(cstm_dbx_link))
    with ProgressStdoutRedirection(ath_un):
        print('Downloading custom csv files from: {}'.format(cstm_dbx_link)) 
    cstm_dbx_link = cstm_dbx_link[:-1]+'1' # Replace the 0 at the end of the link with 1.Will download as .zip file.
    table_name= 'cstm_{}'.format(table_name)
    response = urllib.request.urlopen(cstm_dbx_link)
    sniffer = csv.Sniffer()
    db_name = str(str2md5(ath_un)) + '_Athlete_Data_DB'

    archive_params = config(filename="encrypted_settings.ini", section="archive")
    preserve_files = str(archive_params.get("preserve_files"))   

    #Insert usr_params to athlete table..
    cstm_user_insert(ath_un,usr_params_str,usr_params_int,table_name,db_host,db_name,superuser_un,superuser_pw)

    conn = None   
    # connect to the PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un,password=superuser_pw)

    sql_select_athlete_id = """
        SELECT id FROM athlete WHERE ath_un = %s;
    """
    
    # Extract the downloaded file in to variable
    downloadFile = io.BytesIO()
    downloadFile.write(response.read())
    downloadFile.seek(0)#Move pointer to the beginning

    # Create output directory (if it does not already exist).
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Create Archive directory (if it does not already exist).
    if preserve_files == "true":  
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)
    
    #Insert the data from csv to dataframe
    if zipfile.is_zipfile(downloadFile):
        with zipfile.ZipFile(downloadFile, 'r') as z:
            #List the content of the zip file
            zipfile_content = z.namelist() 
            #Iterate through list and only extract files
            for item in zipfile_content:
                z.extract(item,download_folder)
        downloadFile.close()
        for filename in os.listdir(download_folder):
            if os.path.isfile(os.path.join(download_folder,filename)):
                #Detect whether the csv file has a header.
                with open(os.path.join(download_folder,filename),'r') as f:
                    has_header = sniffer.has_header(f.read())
                    if has_header:
                        f.seek(0)#Move pointer to the beginning
                        data_count = csv_match_columns2data(ath_un,f)
                        df = pd.read_csv(os.path.join(download_folder,filename),usecols=data_count)
                    else:
                        df = pd.read_csv(os.path.join(download_folder,filename),header=None)   
                dataframes.append(df)
                f.close()
                #Archive csv files
                if preserve_files == "false":
                    #Remove the csv file from download folder
                    os.remove(os.path.join(download_folder,filename))
                    with StdoutRedirection(ath_un):
                        print(('The content of \"{}\" parsed and inserted into DB.'.format(filename)))
                    with ProgressStdoutRedirection(ath_un):
                        print(('The content of \"{}\" parsed and inserted into DB.'.format(filename)))
                else:
                    #Move the csv to archive folder and remove from download
                    if os.path.exists(os.path.join(archive_folder,filename)):
                        #Replace the existing file with the updated one
                        os.remove(os.path.join(archive_folder,filename))
                        os.rename(os.path.join(download_folder,filename), os.path.join(archive_folder,filename))
                        with StdoutRedirection(ath_un):
                            print(('The content of \"{}\" parsed and inserted into DB and the original csv file archived'.format(filename)))
                        with ProgressStdoutRedirection(ath_un):
                            print(('The content of \"{}\" parsed and inserted into DB and the original csv file archived'.format(filename)))
                    else:
                        #Remove the csv file from download folder
                        os.remove(os.path.join(download_folder,filename))
    else:
        filename = re.search(r'([^\/]+)\?.*$', cstm_dbx_link).group(1) #Exctract the filename from the link
        downloadFile.seek(0)#Move pointer to the beginning
        #Detect whether the csv file has a header.
        wrapper = io.TextIOWrapper(downloadFile, encoding='utf-8')
        has_header = sniffer.has_header(wrapper.read())
        downloadFile.seek(0)#Move pointer to the beginning
        if has_header:
            data_count = csv_match_columns2data(ath_un,wrapper)
            downloadFile.seek(0)#Move pointer to the beginning
            df = pd.read_csv(downloadFile,usecols=data_count)
        else:
            df = pd.read_csv(downloadFile,header=None)
        #Archive downloaded File
        if preserve_files == "true":
            downloadFile.seek(0)#Move pointer to the beginning
            with open(os.path.join(archive_folder,filename),'wb') as f:
                f.write(downloadFile.read())
                with StdoutRedirection(ath_un):
                    print(('The content of \"{}\" parsed and inserted into DB and the original csv file archived'.format(filename)))
                with ProgressStdoutRedirection(ath_un):
                    print(('The content of \"{}\" parsed and inserted into DB and the original csv file archived'.format(filename)))
        else:
            with StdoutRedirection(ath_un):
                print(('The content of \"{}\" parsed and inserted into DB.'.format(filename)))
            with ProgressStdoutRedirection(ath_un):
                print(('The content of \"{}\" parsed and inserted into DB.'.format(filename)))
        wrapper.close()
        dataframes.append(df)
        downloadFile.close()

    #Remove duplicates
    dataframes = pd.concat(dataframes).drop_duplicates().reset_index(drop=True)
    
    #---- Parse and format datetime values ----
    cur = conn.cursor()
    #Iterate through values in df datetime column
    if datetime_clmn is not None:
        datetime_clmn = int(datetime_clmn)
        #set how to to interpret the the first value in an ambiguous 3-integer date
        #eu date format dd/mm/yyyy
        if date_format == "eu":
            first_val = "day"
        #us date format mm/dd/yyyy
        else:
            first_val = 'month'
        #add timestamp_gmt and timestamp_local columns
        datetime_clmn_gmt = "timestamp_gmt"
        datetime_clmn_local = "timestamp_local"
        dataframes[datetime_clmn_gmt] = np.nan
        dataframes[datetime_clmn_local] = np.nan
        
        item_row_nr = 0
        for item in dataframes[dataframes.columns[datetime_clmn]]:
            timestamps = datefinder.find_dates(str(item),first=first_val)
            for timestamp in timestamps:
                #If the timestamp is timezone aware
                if timestamp.tzinfo is not None:
                    timestamp_utc = timestamp.astimezone(pytz.UTC)
                    timestamp_utc = datetime.datetime.strftime(timestamp_utc,"%Y-%m-%d %H:%M:%S.%f")
                    timestamp_local = datetime.datetime.strftime(timestamp,"%Y-%m-%d %H:%M:%S.%f %Z")
                #If the timestamp is timezone naive
                else:
                    local_timezone = pytz.timezone(timezone)
                    timestamp_local_tz = local_timezone.localize(timestamp, is_dst=True)
                    timestamp_utc = timestamp_local_tz.astimezone(pytz.UTC)
                    timestamp_utc = datetime.datetime.strftime(timestamp_utc,"%Y-%m-%d %H:%M:%S.%f")
                    timestamp_local = datetime.datetime.strftime(timestamp_local_tz,"%Y-%m-%d %H:%M:%S.%f %Z")

            #insert timestamp_utc and timezone_local values to the newly created df columns
            row_index = dataframes.index[item_row_nr]
            dataframes.loc[row_index, datetime_clmn_gmt] = timestamp_utc
            dataframes.loc[row_index, datetime_clmn_local] = timestamp_local

            item_row_nr+=1
    
    cur.execute(sql_select_athlete_id,(ath_un,))
    result = cur.fetchone()
    conn.commit()
    ath_un_id = result[0]
    dataframes['athlete_id'] = ath_un_id
    cur.close()
    
    #format column names to comply with postgres rules
    dataframes.rename(columns = { i: format_column_name(i) for i in  df.columns}, inplace=True)
    
    #Get list of unique column names from column numbers (suplied by user) and add athlete_id column to the list
    for i in unique:
        x = unique.index(i)
        unique[x] = dataframes.columns[i]
    unique.append("athlete_id")
    
    #Check if the table already exists
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename  = '{}');".format(table_name))
    result = cur.fetchone()
    conn.commit()
    if result[0] is True:
        with StdoutRedirection(ath_un):
            print('The custom table {} already exists. Will now insert the new data'.format(table_name))
        with ProgressStdoutRedirection(ath_un):
            print('The custom table {} already exists. Will now insert the new data'.format(table_name))
        pass
    else:
        with StdoutRedirection(ath_un):
            print('Creating custom table: {}'.format(table_name))
        with ProgressStdoutRedirection(ath_un):
            print('Creating custom table: {}'.format(table_name))
        cur.execute(gen_tbl_sql(dataframes,table_name,unique))
        conn.commit()
        cur.close()
    
    insert_df_values(ath_un,conn, dataframes, table_name, unique)
    
    # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()

def retrieve_cstm_tables_params(ath_un,db_host,db_name,superuser_un,superuser_pw):
    conn = None
    sql_select_cstm_tables = """
    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME LIKE 'cstm_%'
    ORDER BY TABLE_NAME;
    """
    try:   
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)
        cur = conn.cursor()
        cur.execute(sql_select_cstm_tables)
        conn.commit()
        tables = cur.fetchall()
        cur.close()
        for row in tables:
            for table in row:
                str_param_columns = 'str_up_{}'.format(table)
                int_param_columns = 'int_up_{}'.format(table) 
                cur = conn.cursor()
                cur.execute('SELECT {},{} from athlete;'.format(str_param_columns,int_param_columns))
                conn.commit()
                cstm_params = cur.fetchall()
                cur.close() 
                for row in cstm_params:
                    usr_params_str = cstm_params[0][0]
                    usr_params_int = cstm_params[0][1]  
                    cstm_data_insert(ath_un,usr_params_str,usr_params_int,db_host,superuser_un,superuser_pw)
    except (Exception, psycopg2.DatabaseError) as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))

    finally:
        if conn is not None:
            conn.close()

    