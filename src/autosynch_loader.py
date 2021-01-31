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
def start_autosynch_loop(encr_pass):     
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

