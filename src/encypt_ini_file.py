#
# This script uses settings.ini as a base, encrypts all sensitive information in it and generates encrypted_settings.ini file which is then used by the application.
# The original settings.ini is automaticaly deleted when the application starts, or it can be deleted manualy after this script sucesfully executes. 
# This script is executed automaticaly when the app (web_app_loader_flask.py or web_app_loader_apache.py) is started for the first time, 
# or it can be executed prior, by running this script manualy. It will need to be executed with the same password argument as will be used later for the app.
# If it needs to be re-run (eg passphrase change etc) and the settings.ini has been deleted, simply rename encrypted_settings.ini back to settings.ini, replace all encrypted sections with the plain text, 
# and restart the application or run manualy providing the correct passphrase.
# 
# What gets encrypted: [app]: secret_key, smtp_password
#                      [postgresql]: password
#                      [dropbox]: app_secret, app_key
#                      [oura]: client_id, client_secret
#                      [strava]: client_id, client_secret
#                      [anticaptcha]: api_key
#
# At a very least you will need to provide [app]: secret_key,[postgresql]: password for the application to be able to function, the rest is optional.

from db_encrypt import generate_key,pad_text,unpad_text
import Crypto.Random
from Crypto.Cipher import AES
from configparser import ConfigParser 
import base64

#----Crypto Variables. Values must match the values in settings.ini----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16


def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    #iv = Crypto.Random.get_random_bytes(AES.block_size)12345
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt

def create_encr_ini_file(encr_pass_input,plaintext_ini,encrypted_ini):

    parser = ConfigParser()
    #Read clear text ini file
    with open(plaintext_ini, "U") as f:
            config_txt = f.read()
            f.close()
    parser.read_string(str(config_txt))

    #Encrypt and write/set sensitive items
    postgres_password_to_encrypt = parser.get('postgresql','password')
    encrypted_postgres_password = base64.b64encode(encrypt(postgres_password_to_encrypt,encr_pass_input))
    encrypted_postgres_password = encrypted_postgres_password.decode('utf-8')
    parser.set('postgresql', 'password', encrypted_postgres_password)

    app_secr_key_to_encrypt = parser.get('app','secret_key')
    encrypted_app_secr_key = base64.b64encode(encrypt(app_secr_key_to_encrypt,encr_pass_input))
    encrypted_app_secr_key = encrypted_app_secr_key.decode('utf-8')
    parser.set('app', 'secret_key', encrypted_app_secr_key)

    smtp_password_to_encrypt = parser.get('app','smtp_password')
    encrypted_smtp_password = base64.b64encode(encrypt(smtp_password_to_encrypt,encr_pass_input))
    encrypted_smtp_password = encrypted_smtp_password.decode('utf-8')
    parser.set('app', 'smtp_password', encrypted_smtp_password)

    dbx_app_key_to_encrypt = parser.get('dropbox','app_key')
    encrypted_dbx_app_key = base64.b64encode(encrypt(dbx_app_key_to_encrypt,encr_pass_input))
    encrypted_dbx_app_key = encrypted_dbx_app_key.decode('utf-8')
    parser.set('dropbox', 'app_key', encrypted_dbx_app_key)

    dbx_app_secret_to_encrypt = parser.get('dropbox','app_secret')
    encrypted_dbx_app_secret = base64.b64encode(encrypt(dbx_app_secret_to_encrypt,encr_pass_input))
    encrypted_dbx_app_secret = encrypted_dbx_app_secret.decode('utf-8')
    parser.set('dropbox', 'app_secret', encrypted_dbx_app_secret)

    oura_client_id_to_encrypt = parser.get('oura','oura_client_id')
    encrypted_oura_client_id = base64.b64encode(encrypt(oura_client_id_to_encrypt,encr_pass_input))
    encrypted_oura_client_id = encrypted_oura_client_id.decode('utf-8')
    parser.set('oura','oura_client_id', encrypted_oura_client_id)

    oura_client_secret_to_encrypt = parser.get('oura','oura_client_secret')
    encrypted_oura_client_secret = base64.b64encode(encrypt(oura_client_secret_to_encrypt,encr_pass_input))
    encrypted_oura_client_secret = encrypted_oura_client_secret.decode('utf-8')
    parser.set('oura','oura_client_secret', encrypted_oura_client_secret)

    strava_client_id_to_encrypt = parser.get('strava','strava_client_id')
    encrypted_strava_client_id = base64.b64encode(encrypt(strava_client_id_to_encrypt,encr_pass_input))
    encrypted_strava_client_id = encrypted_strava_client_id.decode('utf-8')
    parser.set('strava','strava_client_id', encrypted_strava_client_id)

    strava_client_secret_to_encrypt = parser.get('strava','strava_client_secret')
    encrypted_strava_client_secret = base64.b64encode(encrypt(strava_client_secret_to_encrypt,encr_pass_input))
    encrypted_strava_client_secret = encrypted_strava_client_secret.decode('utf-8')
    parser.set('strava','strava_client_secret', encrypted_strava_client_secret)

    anticaptcha_api_key_to_encrypt = parser.get('anticaptcha','api_key')
    encrypted_anticaptcha_api_key = base64.b64encode(encrypt(anticaptcha_api_key_to_encrypt,encr_pass_input))
    encrypted_anticaptcha_api_key = encrypted_anticaptcha_api_key.decode('utf-8')
    parser.set('anticaptcha','api_key', encrypted_anticaptcha_api_key)


    #Write the new encrypted ini file
    with open((encrypted_ini), "a") as configfile:
        parser.write(configfile)

    


if __name__ == "__main__":
    create_encr_ini_file('<<encryption_passphrase>>','settings.ini','encrypted_settings.ini')
