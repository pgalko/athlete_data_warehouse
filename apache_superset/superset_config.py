## SUPERSET DATABASE (postgres)##
#Comment out if you want to use the deault db that comes with superset
SQLALCHEMY_DATABASE_URI = 'postgresql://<USERNAME>:<PASSWORD>@localhost/superset'

## MUTATE CONNECTION URI BASED ON USERNAME ##
#Requires DB connection created by admin via GUI, pointing to athlete_db or sample_db(for multiuser) and "impersonate_user" field value set to true in "public.dbs" table.
import hashlib

def str2md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()
#Function to mutate the db connection string based on the username.
def DB_CONNECTION_MUTATOR(uri, params, username, security_manager, source):
    user = security_manager.find_user(username=username)
    if user.username != "admin":
	    #this condition can be removed if sample_user or sample_db have not been setup
        if user.username == "sample_user":
            uri.username = 'public_ro'
            uri.port = "5433"
            uri.database = 'sample_db'
        else: 
        #		
            uri.database = str(str2md5(user.username)) + "_Athlete_Data_DB"
            uri.port = "5432"
            uri.username = 'postgres'
    else:
        uri.username = 'postgres'
    return uri, params

## SUPERSET AUTO LOGIN ##
# This is to autologin the athletedata user to superset. Refer to sample "custop_security.py" for details.
from custom_security import CustomSecurityManager
CUSTOM_SECURITY_MANAGER = CustomSecurityManager


