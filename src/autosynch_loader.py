#------------------------------------------------------------------------------------
#                                                                                 
#
#  Always exexute as 'www-data' user: sudo -H -u www-data python autosynch_loader.py
#
#
#------------------------------------------------------------------------------------
from db_auto_sync import get_databases_list,retrieve_decrypt_creds
import time
import os
import sys
import multiprocessing
import getpass
from datetime import datetime
from Athlete_Data_Utills import ConsolidatedProgressStdoutRedirection
from database_ini_parser import config


#Run infinite loop repeating periodicaly to sych user DBs with GC and MFP
def start_autosynch_loop(encr_pass=None):
    #Retrieve encr_pass from .temp file if running on unix, else the encr_pass will be passed as argument
    if os.name != 'nt':
        if os.fork(): # The script will run in the background.Returns 0 in the child, pid of the child in the parent
            sys.exit()
        time.sleep(1)
        print('The autosynch process has been started and will continue running in the background...') 

        path_params = config(filename="encrypted_settings.ini", section="path")
        TEMP_FILE_PATH = str(path_params.get("temp_file_path"))

        #Retrieve passphrase from the .temp file
        f=open(TEMP_FILE_PATH,"r")
        passphrase_input=f.read()
        f.close

        encr_pass = passphrase_input 

    while True:
        autosynch_params = config(filename="encrypted_settings.ini", section="autosynch",encr_pass=encr_pass)
        interval = int(autosynch_params.get("interval")) #number of seconds to wait between runs
        task_start = time.time()
        retrieve_decrypt_creds(get_databases_list(encr_pass),encr_pass)
        task_end = time.time()
        
        previous_task_duration = task_end-task_start
        #Previous run time exceeds interval, start next run immediately.
        if previous_task_duration > interval:
            with ConsolidatedProgressStdoutRedirection():            
                print((str(datetime.now())+'\n---- Last run took '+str(previous_task_duration)+' seconds, which exceeds the '+str(interval)+' seconds interval.Starting the next run now.----\n'))
            retrieve_decrypt_creds(get_databases_list(encr_pass),encr_pass)
        #Previous run time is less then interval. Sleep for the time difference.
        else:
            with ConsolidatedProgressStdoutRedirection():
                print((str('\n---- Previous run finished at:'+str(datetime.now()))+', and took '+str(previous_task_duration)+' seconds to complete. Next run will start in '+str(interval-previous_task_duration)+' seconds.----\n'))
            time.sleep((task_start+interval)-task_end)


if __name__ == "__main__":
    start_autosynch_loop()