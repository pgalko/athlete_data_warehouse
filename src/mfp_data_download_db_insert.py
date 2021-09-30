import myfitnesspal
import datetime
import psycopg2
import os
from database_ini_parser import config
from db_user_insert import mfp_user_insert
from db_files import data_file_path_insert,check_data_file_exists
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import Crypto.Random
from Crypto.Cipher import AES
import base64

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        #yield start_date + datetime.timedelta(n) #ascending start date to end date
        yield end_date - datetime.timedelta(n) #descending end date to start date

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt  

@processify
def dwnld_insert_nutrition(mfp_username,mfp_password,ath_un,start_date,end_date,encr_pass,save_pwd,auto_synch,db_host,superuser_un,superuser_pw):
    Crypto.Random.atfork() 
    db_name = str(str2md5(ath_un)) + '_Athlete_Data_DB'

    if save_pwd == True:
        encrypted_pwd = base64.b64encode(encrypt(mfp_password, encr_pass))
        encrypted_pwd = encrypted_pwd.decode('utf-8')
    else:
        encrypted_pwd = None

    #Get PID of the current process and write it in the file
    pid = (str(os.getpid()))
    pidfile = PID_FILE_DIR + ath_un + '_PID.txt'
    open(pidfile, 'w').write(pid)

    with StdoutRedirection(ath_un):
        print("Attempting to login to MFP...")     
    with ProgressStdoutRedirection(ath_un):
        print("Attempting to login to MFP...")
    try:
        client = myfitnesspal.Client(mfp_username,mfp_password)       
    except ValueError as e:
        with ErrorStdoutRedirection(ath_un):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '-E1- ' + str(e)))
        with StdoutRedirection(ath_un):
            print(('Wrong MFP credentials for user {}. Skipping.'.format(mfp_username)))
        return
    with StdoutRedirection(ath_un):
        print('MFP Login successful! Proceeding...')
    with ProgressStdoutRedirection(ath_un):
        print('MFP Login successful! Proceeding...')

    mfp_user_insert(mfp_username,encrypted_pwd,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass) #PG: insert MFP user details into database

    # read DB connection parameters from ini file
    conn = None

    # connect to the PostgreSQL server
    with ProgressStdoutRedirection(ath_un):
        print('Connecting to the PostgreSQL server...')

    conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)
    
    for single_date in daterange(start_date, end_date):
        date_in_range = single_date.strftime("%Y-%m-%d")
        data_exist_for_date = 'Nutrition_Data_For_'+date_in_range

        #PG: Check whether the data for this date have been inserted into to DB during one of the previous runs         
        data_exists = check_data_file_exists(data_exist_for_date,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
        if data_exists == True:
            with StdoutRedirection(ath_un):
                print(('Nutrition data for {} already downloaded and inserted to DB. Skipping.'.format(date_in_range)))
            with ProgressStdoutRedirection(ath_un):
                print(('Nutrition data for {} already downloaded and inserted to DB. Skipping.'.format(date_in_range)))
            continue

        with StdoutRedirection(ath_un):
            print(('Downloading nutrition data: '+date_in_range))
        with ProgressStdoutRedirection(ath_un):
            print(('Downloading nutrition data: '+date_in_range))

        try:
            day = client.get_date(single_date)
            meals = day.meals

            for meal in meals:
                meal_name = meal.name
                entry = meal.entries
                with StdoutRedirection(ath_un):
                    print(('****' + meal_name + '****'))
                for item in entry:
                    food_item = item.short_name
                    if food_item is None:
                        food_item = 'Generic'
                    with StdoutRedirection(ath_un):
                        print((food_item.encode("utf-8")))
                    units = item.unit
                    if units is None:
                        units = 'piece'
                    quantity = item.quantity
                    if quantity is None:
                        quantity = 1.0
                    nutrients = item.nutrition_information
                    for nutrient,value in nutrients.items():
                        if nutrient == 'fiber':
                            fiber_value = value
                        if nutrient == 'sodium':
                            sodium_value = value
                        if nutrient == 'carbohydrates':
                            carbohydrates_value = value
                        if nutrient == 'calories':
                            calories_value = value
                        if nutrient == 'fat':
                            fat_value = value
                        if nutrient == 'protein':
                            protein_value = value

                    sql = """

                    INSERT INTO mfp_nutrition(athlete_id,date,meal,food_item,units,quantity,fiber,sodium,carbohydrates,calories,fat,protein)

                    VALUES
                    ((select id from athlete where mfp_username=%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                    
                    """
                    try:
                        # create a cursor
                        cur = conn.cursor()
                        # execute a statement
                        with StdoutRedirection(ath_un):
                            print('Inserting record....')
                        with ProgressStdoutRedirection(ath_un):
                            print('Inserting record....')
                        cur.execute(sql,(mfp_username,date_in_range,meal_name,food_item,units,quantity,fiber_value,sodium_value,carbohydrates_value,calories_value,fat_value,protein_value))
                        conn.commit()
                        # close the communication with the PostgreSQL
                        cur.close()
                        
                    except  (Exception, psycopg2.DatabaseError) as error:
                        with ErrorStdoutRedirection(ath_un):
                            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '-E2-  ' + str(error)))

                    # Update the files table 
                    data_file_path_insert(data_exist_for_date,ath_un,db_host,db_name,superuser_un,superuser_pw,encr_pass)
        except Exception as e:
             with ErrorStdoutRedirection(ath_un):
                 print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '-E3-  ' + str(e)))
             continue
     
     # close the communication with the PostgreSQL
    if conn is not None:
        conn.close()             
                    
    with StdoutRedirection(ath_un):    
        print('--- All nutrition data inserted successfully. ---')
    with ProgressStdoutRedirection(ath_un):   
        print('--- All nutrition data inserted successfully. ---') 
