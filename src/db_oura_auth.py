#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from db_encrypt import generate_key,pad_text,unpad_text
import Crypto.Random
from Crypto.Cipher import AES
import base64

#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16


def decrypt(ciphertext, password):
    salt = ciphertext[0:SALT_SIZE]
    #iv = ciphertext[:AES.block_size]
    ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    return plaintext 

def check_oura_token_exists(gc_username,db_host,db_name,superuser_un,superuser_pw,encr_pass):
    conn = None
    gc_username = gc_username
    db_name = db_name
    decrypted_oura_token = None

    sql_check_oura_token_exists = """
    SELECT oura_refresh_token FROM athlete WHERE gc_email = %s;
    """

    try: 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        try:
            cur.execute(sql_check_oura_token_exists,(gc_username,))
            result = cur.fetchone()
            if result[0] is not None:  
                token_exists = True
                oura_token = result[0]
                #Decrypt oura token
                decrypted_oura_token = decrypt(base64.b64decode(oura_token), encr_pass)
            else:
                token_exists = False
            conn.commit()
        except:
            token_exists = False

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        with ErrorStdoutRedirection(gc_username):
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

    finally:
        if conn is not None:
            conn.close()
    
    return token_exists, decrypted_oura_token


