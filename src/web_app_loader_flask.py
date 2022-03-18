#
# This web app loader is to be used on WIN OS and the build-in Flask web server (use only for testing and development).
# It sets the encryption passphrase, loads Flask web server/athletedataapp_flask.py and re-starts the autosynch_loop.
#

import os
import getpass
import sys
import time
from encypt_ini_file import create_encr_ini_file
from multiprocessing import Process
from threading import Thread

encrypted_ini_file = os.path.join("work_dir","config","encrypted_settings.ini")
plaintext_ini_file = os.path.join("work_dir","config","settings.ini")

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

def load_apps():
    encr_pass = get_pass()
    
    #Check if the encrypted settings.ini file exists and try to create it if it does not.
    if not os.path.isfile(encrypted_ini_file):
        print('Can not find enrypted .ini file. Will search for plaintext .ini file and try to encrypt it.')
        if not os.path.isfile(plaintext_ini_file):
            print('Can not find plaintext .ini file. Please create one and retry. Exiting...')
            sys.exit()
        else:
            create_encr_ini_file(encr_pass,plaintext_ini_file,encrypted_ini_file)
            print('Success. Found plaintext .ini file and saccessfully encrypted it.')
            #Delete the plaintext .ini file.Can be commented out for testing.
            print('Deleting plaintext .ini file...')
            os.unlink(plaintext_ini_file)
    else:
        print('Found encrypted .ini file. Proceeding....')
        #Delete the plaintext .ini file.Can be commented out for testing.
        if os.path.isfile(plaintext_ini_file):
            print('Deleting plaintext .ini file...')
            os.unlink(plaintext_ini_file)
    
    #Start the Autosynch task in a separate thread and pass the encryption passphrase to it
    #Disabled for testing !

    from autosynch_loader import start_autosynch_loop
    autosynch_thread = Thread(target=start_autosynch_loop, name='autosynch_loop', args=(encr_pass,)) 
    autosynch_thread.daemon = True
    autosynch_thread.start()
    
    #Start the Flask app and pass the encryption passphrase to it
    from athletedataapp_flask import create_app
    web_app = create_app(encr_pass,debug=True)
    web_app.run(host='0.0.0.0')

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #To be able to use oauth over http (for oura) 
    load_apps()