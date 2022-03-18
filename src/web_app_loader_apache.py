#
# This web app loader is to be used on UNIX OS and Apache web server with mod_wsgi module(https://modwsgi.readthedocs.io/en/master).
# It sets the encryption passphrase, reloads Apache web server\mod_wsgi and re-starts the autosynch_loop.
# You will need a working Apache web server with configured mod_wsgi module
#

import os
import sys
import time
import getpass
import urllib.request, urllib.error, urllib.parse
from database_ini_parser import config
from encypt_ini_file import create_encr_ini_file

def get_pass():
    #Admin to provide the encryption passphrase. This is not permanently stored anywhere on the system and is used to encrypt all sensitive user information.
    #Everytime you restart the Flask service you will be asked to provide the same passphrase. If you decide not to provide the passphrase the default 
    #passphrase will be used after input timeout.
    timeout = 20 #Time in secs to provide passphrase
    default_passphrase = os.environ.get('ENCR_PASS')
    print('Waiting for input... please press "Ctrl-C" within {} seconds to type-in the encryption passphrase.'.format(timeout))
    try:
        for i in range(timeout,0,-1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(i))
            sys.stdout.flush()   
            time.sleep(1)
        #If no input detected within timeout window the default passphrase will be used.
        if default_passphrase is not None:   
            passphrase = default_passphrase
            print("\nNo input was received. Using default encryption passphrase.")
        else:
            passphrase = getpass.getpass(prompt='\nNo stored passphrase found. Please enter encryption passphrase:')
            print ("Using your chosen encryption passphrase.")
    except KeyboardInterrupt:
        passphrase = getpass.getpass(prompt='\nPlease enter encryption passphrase:')
        print ("Using your chosen encryption passphrase.")
    return passphrase

passphrase = get_pass()
#passphrase = getpass.getpass(prompt='Please enter encryption passphrase:')

#Check if the encrypted settings.ini file exists and try to create it if it does not.
encrypted_ini_file = os.path.join("work_dir","config","encrypted_settings.ini")
plaintext_ini_file = os.path.join("work_dir","config","settings.ini")

if not os.path.isfile(encrypted_ini_file):
    print('Can not find enrypted .ini file. Will search for plaintext .ini file and try to encrypt it.')
    if not os.path.isfile(plaintext_ini_file):
        print('Can not find plaintext .ini file. Please create one and retry. Exiting...')
        sys.exit()
    else:
        try:
            create_encr_ini_file(passphrase,plaintext_ini_file,encrypted_ini_file)
            print('Success. Found plaintext .ini file and successfully encrypted it.')
            #Delete the plaintext .ini file.Can be commented out for testing.
            print('Deleting plaintext .ini file...')
            os.unlink(plaintext_ini_file)
        except Exception as e:
            print(e)
            sys.exit()
else:
    print('Found encrypted .ini file. Proceeding....')
    #Delete the plaintext .ini file.Can be commented out for testing.
    if os.path.isfile(plaintext_ini_file):
        print('Deleting plaintext .ini file...')
        os.unlink(plaintext_ini_file)
    

path_params = config(filename="encrypted_settings.ini", section="path")
TEMP_FILE_PATH = path_params.get("temp_file_path")

#Write passphrase to the .temp file. Flask app will retrieve from here and subsequently delete .temp file.
f=open(TEMP_FILE_PATH,"w")
f.write(passphrase)
f.close

#Change permission on the .temp file(unix)
os.chown(TEMP_FILE_PATH,33,33)
os.chmod(TEMP_FILE_PATH, 0o600)

#Restart Apache(unix)
print("Current apache2 PIDs:")
os.system("lsof -i :443")
os.system("systemctl restart apache2")

print("New apache2 PIDs:")
os.system("lsof -i :443")

print("Apache restart with a new pasphrase complete!")

#Restart Autosynch(unix)
print("Starting Autosynch process")
os.system("sudo pkill -f autosynch_loader.py")
os.system("sudo -H -u www-data python autosynch_loader.py")



