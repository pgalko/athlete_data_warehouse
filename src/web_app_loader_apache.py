#
# This web app loader is to be used on UNIX OS and Apache web server with mod_wsgi module(https://modwsgi.readthedocs.io/en/master).
# It sets the encryption passphrase, reloads Apache web server\mod_wsgi and re-starts the autosynch_loop.
# You will need a working Apache web server with configured mod_wsgi module
#

import os
import sys
import getpass
import urllib.request, urllib.error, urllib.parse
from database_ini_parser import config
from encypt_ini_file import create_encr_ini_file

#Admin to provide the encryption passphrase. This is not permanently stored anywhere on the system and is used to encrypt all sensitive user information.
#Everytime you restart the Apache/mod_wsgi service you will be asked to provide the same passphrase.
passphrase = getpass.getpass(prompt='Please enter encryption passphrase:')

#Check if the encrypted settings.ini file exists and try to create it if it does not.
encrypted_ini_file = 'encrypted_settings.ini'
plaintext_ini_file = 'settings.ini'

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
            print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(e)))
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



