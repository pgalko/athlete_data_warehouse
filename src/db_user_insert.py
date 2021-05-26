#!/usr/bin/python
import psycopg2
from database_ini_parser import config
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from processify import processify
import os

path_params = config(filename="encrypted_settings.ini", section="path")
PID_FILE_DIR = path_params.get("pid_file_dir")

@processify
def gc_user_insert(gc_username,gc_decr_pw,gc_password,mfp_username,db_host,db_name,superuser_un,superuser_pw,dbx_auth_token,oura_refresh_token,encr_pass):
        gc_user = (gc_username, )
        gc_pwd = (gc_password, )
        mfp_user = (mfp_username, )
        head, sep, tail = gc_username.partition('@')
        db_user = head
        db_password = gc_decr_pw
        db_name = (db_name)
        auth_token_tuple = (dbx_auth_token, )
        oura_token_tuple = (oura_refresh_token, )
        
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
        open(pidfile, 'w').write(pid)

        sql = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET gc_password = %s where gc_email= %s;
                
        ELSE
        INSERT INTO athlete (gc_email, gc_password, mfp_username, mfp_password, dropbox_access_token) VALUES 
        (%s,%s,null,null,null);

        END IF;
        
        END
        $do$

        """

        sql_alter_dbuser = "ALTER USER \""+db_user+"\" WITH PASSWORD \'"+ db_password +"\';"

        sql_insert_dbx_auth_token = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET dropbox_access_token = %s where gc_email= %s;


        END IF;
        
        END
        $do$

        """

        sql_insert_oura_refresh_token = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET oura_refresh_token = %s where gc_email= %s;

        END IF;
        
        END
        $do$

        """

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name,host=db_host, user=superuser_un, password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting GC User Data into postgreSQL:')
                cur.execute(sql,(gc_user,gc_pwd,gc_user,gc_user,gc_pwd))
                cur.execute(sql_alter_dbuser)							 
                conn.commit()

                if dbx_auth_token is not None:
                    with ProgressStdoutRedirection(gc_username):
                        print('Inserting Dropbox user authentication token into postgreSQL:')
                    cur.execute(sql_insert_dbx_auth_token,(gc_user,auth_token_tuple,gc_user))
                    conn.commit()

                if oura_refresh_token is not None:
                    with ProgressStdoutRedirection(gc_username):
                        print('Inserting Oura refresh token into postgreSQL:')
                    cur.execute(sql_insert_oura_refresh_token,(gc_user,oura_token_tuple,gc_user))
                    conn.commit()

                # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(gc_username):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn is not None:
                        conn.close()
                        
@processify
def mfp_user_insert(mfp_username,mfp_password,gc_username,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        mfp_user = (mfp_username, )
        mfp_pwd = (mfp_password, )
        gc_user = (gc_username, )
        db_name = (db_name)
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
        open(pidfile, 'w').write(pid)

        sql = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE mfp_username = %s) THEN

        UPDATE athlete SET mfp_password = %s where mfp_username= %s;

        ELSEIF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET mfp_password = %s,mfp_username = %s where gc_email= %s;


        END IF;
        
        END
        $do$

        """
        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting MFP User Data into postgreSQL:')
                cur.execute(sql,(mfp_user,mfp_pwd,mfp_user,gc_user,mfp_pwd,mfp_user,gc_user))
                conn.commit()
                
                        # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(gc_username):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn is not None:
                        conn.close()

@processify
def diasend_user_insert(diasend_username,diasend_password,gc_username,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        diasend_user = (diasend_username, )
        diasend_pwd = (diasend_password, )
        gc_user = (gc_username, )
        db_name = (db_name)
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
        open(pidfile, 'w').write(pid)

        sql = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE diasend_username = %s) THEN

        UPDATE athlete SET diasend_password = %s where diasend_username= %s;

        ELSEIF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET diasend_password = %s,diasend_username = %s where gc_email= %s;

        END IF;
        
        END
        $do$

        """

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting Diasend User Data into postgreSQL:')
                cur.execute(sql,(diasend_user,diasend_pwd,diasend_user,gc_user,diasend_pwd,diasend_user,gc_user))
                conn.commit()
                
                # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
                with ErrorStdoutRedirection(gc_username):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn is not None:
                        conn.close()
@processify  
def glimp_user_insert(glimp_export_link,gc_username,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        glimp_export_link = (glimp_export_link, )
        gc_user = (gc_username, )
        db_name = (db_name)
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
        open(pidfile, 'w').write(pid)

        sql = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET glimp_export_link = %s where gc_email= %s;

        END IF;
        
        END
        $do$

        """

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting Glimp User Data into postgreSQL:')
                cur.execute(sql,(gc_user,glimp_export_link,gc_user))
                conn.commit()
                
                        # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
                with ErrorStdoutRedirection(gc_username):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn is not None:
                        conn.close()

@processify
def libreview_user_insert(libreview_export_link,gc_username,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        libreview_export_link = (libreview_export_link, )
        gc_user = (gc_username, )
        db_name = (db_name)
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
        open(pidfile, 'w').write(pid)

        sql = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET libreview_export_link = %s where gc_email= %s;

        END IF;
        
        END
        $do$

        """

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting LIbreView User Data into postgreSQL:')
                cur.execute(sql,(gc_user,libreview_export_link,gc_user))
                conn.commit()
                
                        # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
                with ErrorStdoutRedirection(gc_username):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn is not None:
                        conn.close()

@processify
def mm_user_insert(mm_export_link,gc_username,db_host,db_name,superuser_un,superuser_pw,encr_pass):
        mm_export_link = (mm_export_link, )
        gc_user = (gc_username, )
        db_name = (db_name)
        conn = None

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
        open(pidfile, 'w').write(pid)

        sql = """
        DO
        $do$
        BEGIN
        IF

        EXISTS (SELECT id FROM athlete WHERE gc_email = %s) THEN

        UPDATE athlete SET mm_export_link = %s where gc_email= %s;

        END IF;
        
        END
        $do$

        """

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting Mind Monitor User Data into postgreSQL:')
                cur.execute(sql,(gc_user,mm_export_link,gc_user))
                conn.commit()
                
                        # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
                with ErrorStdoutRedirection(gc_username):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn is not None:
                        conn.close()

@processify
def gc_user_update(gc_username,db_host,db_name,superuser_un,superuser_pw,encrypted_superuser_pw,enable_auto_synch,encr_pass):
        gc_user = (gc_username,)
        db_name = (db_name)

        #Get PID of the current process and write it in the file
        pid = str(os.getpid())
        pidfile = PID_FILE_DIR + gc_username + '_PID.txt'
        open(pidfile, 'w').write(pid)

        #Do not save pw to db_info if no autosynch or db_host=localhost
        if enable_auto_synch == True:
            if db_host != 'localhost':
                encrypted_superuser_pw = (encrypted_superuser_pw,)
            else:
                encrypted_superuser_pw = None
        else:
            encrypted_superuser_pw = None
        enable_auto_synch = (enable_auto_synch,)
        conn = None

        sql = """

        UPDATE athlete SET auto_sync = %s where gc_email= %s;
                
        """
        
        sql_postgres_db ="""
        
        UPDATE db_info SET db_auto_synch = %s,db_un = %s,db_pw = %s where db_name= %s;

        """

        try:
         
                # connect to the PostgreSQL server
                conn = psycopg2.connect(dbname=db_name, host=db_host, user=superuser_un, password=superuser_pw)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting Auto_Sych preferences into postgreSQL:')
                cur.execute(sql,(enable_auto_synch,gc_user))
                conn.commit()
                
                # close the communication with the PostgreSQL
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(gc_username):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn is not None:
                        conn.close()

        #Insert user autosynch preference into postgres/db_info table 
        try:
                params = config(filename="encrypted_settings.ini", section="postgresql", encr_pass=encr_pass)
                conn_localhost = psycopg2.connect(**params)
                conn_localhost.autocommit = True

                # create a cursor
                cur_localhost = conn_localhost.cursor()

                # execute a statement
                with ProgressStdoutRedirection(gc_username):
                    print('Inserting Auto_Sych preferences into postgres/db_info table:')
                
                cur_localhost.execute(sql_postgres_db,(enable_auto_synch,superuser_un,encrypted_superuser_pw,db_name))
                
                # close the communication with the PostgreSQL
                cur_localhost.close()
        except (Exception, psycopg2.DatabaseError) as error:
            with ErrorStdoutRedirection(gc_username):
                print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '  ' + str(error)))

        finally:
                if conn_localhost is not None:
                    conn_localhost.close



