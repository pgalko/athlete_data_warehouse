#!/usr/bin/python
from db_encrypt import generate_key,pad_text,unpad_text
from configparser import ConfigParser
import Crypto.Random
from Crypto.Cipher import AES
import base64

#######################################################################################################################
#This script decrypts,reads and returns contents of .ini file.
#Presumes that the file has been previously encrypted using the "encrypt_ini_file.py script and the correct passphrase.
#######################################################################################################################


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
 
#Decrypt the sensitive sections of the .ini file
def config(filename, section, encr_pass=None):
    # create a parser
    parser = ConfigParser()

    # read config file
    with open(filename, "U") as f:
        config_txt = f.read()
        f.close()

    # read decrypted text
    parser.read_string(str(config_txt))
 
    # get and decrypt(if encrypted)section
    db = {}
    if parser.has_section(section):
        if section == 'postgresql':
            params = parser.items(section)
            for param in params:
                if param[0] == 'password':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                else:
                    db[param[0]] = param[1]
        elif section == 'app':
            params = parser.items(section)
            for param in params:
                if param[0] == 'secret_key':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                elif param[0] == 'smtp_password':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                else:
                    db[param[0]] = param[1]
        elif section == 'dropbox':
            params = parser.items(section)
            for param in params:
                if param[0] == 'app_key':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                elif param[0] == 'app_secret':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                else:
                    db[param[0]] = param[1]
        elif section == 'oura':
            params = parser.items(section)
            for param in params:
                if param[0] == 'oura_client_id':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                elif param[0] == 'oura_client_secret':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                else:
                    db[param[0]] = param[1]
        elif section == 'anticaptcha':
            params = parser.items(section)
            for param in params:
                if param[0] == 'api_key':
                    try:
                        decrypted_param = decrypt(base64.b64decode(param[1]), encr_pass)
                        db[param[0]] = str(decrypted_param)
                    except:
                        db[param[0]] = ""
                else:
                    db[param[0]] = param[1]
        else:
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


