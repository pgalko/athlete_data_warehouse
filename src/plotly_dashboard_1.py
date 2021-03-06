from dash import dash
from flask import request
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import dash_table
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import psycopg2
import os
import numpy as np
import re
import time
import datetime
from Athlete_Data_Utills import StdoutRedirection,ErrorStdoutRedirection,ProgressStdoutRedirection
import sys
from db_encrypt import generate_key,pad_text,unpad_text,str2md5
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

def create_dashboard1(flask_server,encr_pass,sample_db_un,sample_db_pw,sample_db_host,sample_db_port,sample_db=None,):

    ################################
    ####       Create app       ####
    ################################
    
    app = dash.Dash(__name__,server=flask_server,url_base_pathname='/dashboard_1/')

    ##########################################
    ####### Retrieve data from Sample DB #####
    ##########################################

    db_host = 'localhost'
    conn = None


    sql_fit_run = """
    --QUERY TO SELECT ALL RUNNING ACTIVITIES AND TRIM DOMAIN FROM EMAIL AND CALCULATE LOCAL TIME AND PACE PER 1K:

    select distinct SUBSTRING(t1.gc_email FROM 1 FOR POSITION('@' IN t1.gc_email)-1) as "Athlete", 
        t2.timestamp::timestamp at time zone 'utc' at time zone 'Australia/Victoria' as "Local Time Australia", 
        date_part('epoch', t2.timestamp::timestamp) as "Epoch Timestamp",
        t2.sport as "Sport", 
        t2.total_distance as "Distance (m)",
        to_char(((t2.total_timer_time/(t2.total_distance/1000)) || ' second')::interval, 'MI.SS') as "Avg Time per 1000m",
        t2.total_calories as "Calories",
        t2.avg_heart_rate as "Average HR",
        t2.total_timer_time::integer/60 as "Duration minutes"
    from athlete t1 
    inner join garmin_connect_original_session t2 on t1.id = t2.athlete_id
    inner join garmin_connect_original_lap t3 on t2.gc_activity_id=t3.gc_activity_id 
    where t2.sport = 'running' and t2.total_timer_time>0 and t2.total_timer_time/(t2.total_distance/1000)<420;
    """

    sql_fit_swim = """
    --QUERY TO SELECT ALL SWIMMING ACTIVITIES AND TRIM DOMAIN FROM EMAIL AND CALCULATE LOCAL TIME AND AVERAGE SPEED PER 100M:

    select distinct SUBSTRING(t1.gc_email FROM 1 FOR POSITION('@' IN t1.gc_email)-1) as "Athlete", 
        t2.timestamp::timestamp at time zone 'utc' at time zone 'Australia/Victoria' as "Local Time Australia", 
        date_part('epoch', t2.timestamp::timestamp) as "Epoch Timestamp",
        t2.sport as "Sport", 
        t2.total_distance as "Distance (m)",
        to_char(((t2.total_timer_time/(t2.total_distance/100)) || ' second')::interval, 'MI.SS') as "Avg Time per 100m",
        t2.total_calories as "Calories",
        t2.total_cycles/(t2.total_timer_time::integer/60) as "Strokes per minute",
        t2.total_timer_time::integer/60 as "Duration minutes"
    from athlete t1 
    inner join garmin_connect_original_session t2 on t1.id = t2.athlete_id
    inner join garmin_connect_original_lap t3 on t2.gc_activity_id=t3.gc_activity_id 
    where t2.sport = 'swimming' and t2.total_timer_time>0 and t2.total_distance>50 and t2.total_timer_time/(t2.total_distance/100)>60;
    """

    sql_fit_ride = """
    --QUERY TO SELECT ALL CYCLING ACTIVITIES AND TRIM DOMAIN FROM EMAIL AND CALCULATE LOCAL TIME AND AVERAGE SPEED PER HOUR:

    select distinct SUBSTRING(t1.gc_email FROM 1 FOR POSITION('@' IN t1.gc_email)-1) as "Athlete", 
        t2.timestamp::timestamp at time zone 'utc' at time zone 'Australia/Victoria' as "Local Time Australia", 
        date_part('epoch', t2.timestamp::timestamp) as "Epoch Timestamp",
        t2.sport as "Sport", 
        t2.total_distance as "Distance (m)",
        t2.avg_speed*3.6 as "Avg Speed (km/h)",
        t2.normalized_power as "Normalized Power",
        t2.total_calories as "Calories",
        t2.avg_heart_rate as "Average HR",
        t2.total_timer_time::integer/60 as "Duration minutes"
    from athlete t1 
    inner join garmin_connect_original_session t2 on t1.id = t2.athlete_id
    inner join garmin_connect_original_lap t3 on t2.gc_activity_id=t3.gc_activity_id 
    where t2.sport = 'cycling' and t2.total_timer_time>0;
    """
    conn = psycopg2.connect(dbname=sample_db, host=sample_db_host, port=sample_db_port, user=sample_db_un, password=sample_db_pw)
    cur = conn.cursor()
    cur.execute(sql_fit_swim,())
    rows0 = cur.fetchall()
    str(rows0)[0:300]
    cur.close()

    cur = conn.cursor()
    cur.execute(sql_fit_run,())
    rows1 = cur.fetchall()
    str(rows1)[0:300]
    cur.close()

    cur = conn.cursor()
    cur.execute(sql_fit_ride,())
    rows2 = cur.fetchall()
    str(rows2)[0:300]
    cur.close()

    conn.close()

    #####################################
    ## Create sample pandas Dataframes ##
    #####################################


    #Create pandas swim dataframe
    df0_smpl = pd.DataFrame( [[ij for ij in i] for i in rows0] )
    df0_smpl.rename(columns={0: 'Athlete', 1: 'DateTime', 2: 'DateTime_Epoch', 3: 'Sport', 4: 'Distance', 5:'Pace', 6:'Calories', 7:'Strokes_PerMin', 8:'Duration_Min'}, inplace=True)
    df0_smpl['Pace'] = df0_smpl['Pace'].apply(pd.to_numeric)
    df0_smpl = df0_smpl.sort_values(['DateTime'], ascending=[1])

    #Create pandas run dataframe
    df1_smpl = pd.DataFrame( [[ij for ij in i] for i in rows1] )
    df1_smpl.rename(columns={0: 'Athlete', 1: 'DateTime', 2: 'DateTime_Epoch', 3: 'Sport', 4: 'Distance', 5:'Pace', 6:'Calories', 7:'Avrg_HR', 8:'Duration_Min'}, inplace=True)
    df1_smpl['Pace'] = df1_smpl['Pace'].apply(pd.to_numeric)
    df1_smpl = df1_smpl.sort_values(['DateTime'], ascending=[1])
 
    #Create pandas ride dataframe
    df2_smpl = pd.DataFrame( [[ij for ij in i] for i in rows2] )
    df2_smpl.rename(columns={0: 'Athlete', 1: 'DateTime', 2: 'DateTime_Epoch', 3: 'Sport', 4: 'Distance', 5:'Pace', 6:'Norm_Power', 7:'Calories', 8:'Avrg_HR', 9:'Duration_Min'}, inplace=True)
    df2_smpl = df2_smpl.sort_values(['DateTime'], ascending=[1])

    ################################
    # Create html components #######
    ################################

    app.layout = html.Div(children=[
        html.Div(
            dcc.Location(
            id='url', 
            refresh=False
            ),
        ),

        html.Div(
            dcc.Input(
            id = 'df_type',
            style={"display":"None"},
            )
        ),

        html.Div(
            dcc.Dropdown(
            id='Dropdown1',
            options=[
                {'label': 'Swim', 'value': 'SWIM'},
                {'label': 'Run', 'value': 'RUN'},
                {'label': 'Ride', 'value': 'RIDE'}
            ],
            value='SWIM'
            ),
        ),

        html.Div(
            id = 'Stats1',
            style={"height" : "80vh", "width" : "10vw", "display": "inline-block", "overflow":"auto"},
        ),

        html.Div(
            id='Graph2',
            style={"height" : "80vh", "width" : "88vw", "display": "inline-block",},
            ), 

        html.Div( 
            dash_table.DataTable(
                id='Table1',
                style_table={"height" : "20vh", "width" : "98vw"},
                columns=[{"name": i, "id": i, "deletable": False} for i in df0_smpl.columns],
                data=df0_smpl.to_dict('records'),
                fixed_rows={ 'headers': True, 'data': 0 },
                style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}],
                style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="multi",
                row_deletable=True,
                selected_rows=[],
                #selected_row_indices=[],
                page_action="native",
                page_current= 0,
            )
        )
    ])
    

    ###########################################################################
    #### Create user pandas dataframes and Filter table columns callback ######
    ###########################################################################

    @app.callback([Output('Table1', 'columns'),
        Output('Table1', 'data'),
        Output('df_type','value')],
        [Input('Dropdown1', 'value'),
        Input('url', 'pathname')])
    def update_table_columns(selected_dropdown_value,pathname):
        pathname = str(pathname)
        if pathname.startswith('/dashboard_1'):
            encr_username = pathname.split('/')[-2]
            decr_username = decrypt((base64.urlsafe_b64decode(encr_username)), encr_pass)
            user_db_name = str(str2md5(decr_username)) + '_Athlete_Data_DB'
            #Connect to user db and retrieve user data. If fails revert to sample data
            try:
                #Retrieve user DB details from db_info
                try: 
                    sql_select_dbsu_creds ="""
                    SELECT
                        db_host,db_un,db_pw
                    FROM
                        db_info
                    WHERE
                    db_name = %s;
                    """               
                    # connect to the PostgreSQL server
                    dbsu_conn = psycopg2.connect(dbname='postgres', user=sample_db_un, password=sample_db_pw)

                    # create a cursor
                    dbsu_cur = dbsu_conn.cursor()

                    dbsu_cur.execute(sql_select_dbsu_creds,(user_db_name,))
                    dbsu_conn.commit()
                    dbsu_result = dbsu_cur.fetchone()
                    usr_db_host = dbsu_result[0]
                    db_un = dbsu_result[1]
                    db_pw = dbsu_result[2]
                    
                    if usr_db_host != 'localhost':#User database is hosted remotely
                        superuser_un = db_un
                        superuser_pw = decrypt(base64.b64decode(db_pw), encr_pass)
                    else:
                        usr_db_host = db_host
                        superuser_un = sample_db_un
                        superuser_pw = sample_db_pw

                except (Exception, psycopg2.DatabaseError) as error:
                    with ErrorStdoutRedirection(decr_username):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(error)))
                finally:
                    if dbsu_conn is not None:
                        dbsu_conn.close()
                #Connect to user db
                conn = psycopg2.connect(dbname=user_db_name, host=usr_db_host, user=superuser_un, password=superuser_pw)
                cur = conn.cursor()
                cur.execute(sql_fit_swim,())
                rows0 = cur.fetchall()
                str(rows0)[0:300]
                cur.close()

                cur = conn.cursor()
                cur.execute(sql_fit_run,())
                rows1 = cur.fetchall()
                str(rows1)[0:300]
                cur.close()

                cur = conn.cursor()
                cur.execute(sql_fit_ride,())
                rows2 = cur.fetchall()
                str(rows2)[0:300]
                cur.close()

                conn.close()

                ##############################
                ## Create pandas Dataframes ##
                ##############################


                #Create pandas swim dataframe
                try:
                    df0 = pd.DataFrame( [[ij for ij in i] for i in rows0] )
                    df0.rename(columns={0: 'Athlete', 1: 'DateTime', 2: 'DateTime_Epoch', 3: 'Sport', 4: 'Distance', 5:'Pace', 6:'Calories', 7:'Strokes_PerMin', 8:'Duration_Min'}, inplace=True)
                    df0['Pace'] = df0['Pace'].apply(pd.to_numeric)
                    df0 = df0.sort_values(['DateTime'], ascending=[1])
                    swim_sample_df = False
                except Exception as e:
                    with ErrorStdoutRedirection(decr_username):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(e)))
                    df0 = df0_smpl
                    swim_sample_df = True

                #Create pandas run dataframe
                try:
                    df1 = pd.DataFrame( [[ij for ij in i] for i in rows1] )
                    df1.rename(columns={0: 'Athlete', 1: 'DateTime', 2: 'DateTime_Epoch', 3: 'Sport', 4: 'Distance', 5:'Pace', 6:'Calories', 7:'Avrg_HR', 8:'Duration_Min'}, inplace=True)
                    df1['Pace'] = df1['Pace'].apply(pd.to_numeric)
                    df1 = df1.sort_values(['DateTime'], ascending=[1])
                    run_sample_df = False
                except Exception as e:
                    with ErrorStdoutRedirection(decr_username):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(e)))
                    df1 = df1_smpl
                    run_sample_df = True

                #Create pandas ride dataframe
                try:
                    df2 = pd.DataFrame( [[ij for ij in i] for i in rows2] )
                    df2.rename(columns={0: 'Athlete', 1: 'DateTime', 2: 'DateTime_Epoch', 3: 'Sport', 4: 'Distance', 5:'Pace', 6:'Norm_Power', 7:'Calories', 8:'Avrg_HR', 9:'Duration_Min'}, inplace=True)
                    df2 = df2.sort_values(['DateTime'], ascending=[1])
                    ride_sample_df = False
                except Exception as e:
                    with ErrorStdoutRedirection(decr_username):
                        print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(e)))
                    df2 = df2_smpl
                    ride_sample_df = True
            except Exception as e:
                with ErrorStdoutRedirection(decr_username):
                    print((str(datetime.datetime.now()) + ' [' + sys._getframe().f_code.co_name + ']' + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + str(e)))
                df0 = df0_smpl
                df1 = df1_smpl
                df2 = df2_smpl
                swim_sample_df = True
                run_sample_df = True
                ride_sample_df = True

            #Create data columns from df in table based on selection
            if selected_dropdown_value == "SWIM":
                cols=[{"name": i, "id": i, "deletable": False} for i in df0.columns]
                records=df0.to_dict('records')
                if swim_sample_df == False:
                    html_output = 'User Data'
                else:
                    html_output = 'Sample Data'
            elif selected_dropdown_value == "RUN":
                cols=[{"name": i, "id": i, "deletable": False} for i in df1.columns]
                records=df1.to_dict('records')
                if run_sample_df == False:
                    html_output = 'User Data'
                else:
                    html_output = 'Sample Data'
            elif selected_dropdown_value == "RIDE":
                cols=[{"name": i, "id": i, "deletable": False} for i in df2.columns]
                records=df2.to_dict('records')
                if ride_sample_df == False:
                    html_output = 'User Data'
                else:
                    html_output = 'Sample Data'

            df_type_value = html_output
            return cols,records,df_type_value

        else:
            cols=[{"name": i, "id": i, "deletable": False} for i in df0_smpl.columns]
            records=df0_smpl.to_dict('records')
            html_output = 'Sample Data'

            df_type_value = html_output
            return cols,records,df_type_value


    ###############################
    #### Compute Stats callback ###
    ###############################

    @app.callback(Output('Stats1', 'children'), 
        [Input('Table1', "derived_virtual_data"),
        Input('Table1', "derived_virtual_selected_rows")])
    def update_stats(rows, derived_virtual_selected_rows):

        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []

        df = df0_smpl if rows is None else pd.DataFrame(rows)

        #Calculate average and median pace over time.Cycling pace is in kmph
        if df['Sport'].any() == 'cycling':
            pace_column = df['Pace'].astype(float)
            #pace_column = pd.to_timedelta(pace_column,unit ='m')
            pace_column_secs = pace_column
            avrg_pace_secs = pace_column.mean()
            median_pace_secs = pace_column.median()
            avrg_pace_mins = avrg_pace_secs
            median_pace_mins = median_pace_secs
        else:
            pace_column = df['Pace'].astype(float)
            pace_column = pd.to_timedelta(pace_column,unit ='m')
            pace_column_secs = pace_column.dt.seconds
            avrg_pace_secs = pace_column_secs.mean()
            median_pace_secs = pace_column_secs.median()
            avrg_pace_mins = time.strftime("%H:%M:%S", time.gmtime(avrg_pace_secs))
            median_pace_mins = time.strftime("%H:%M:%S", time.gmtime(median_pace_secs))

        #Calcuate average and median distance over time
        distance_column = df['Distance'].astype(float)
        avrg_distance = distance_column.mean()
        median_distance = distance_column.median()

        #Calculate pace rate of change
        pace_series = pd.Series( pace_column_secs)
        pace_series_change = pace_series.pct_change(periods=14)
        pace_series_change_avrg = pace_series_change.median()

        #Calculate distance rate of change
        distance_series = pd.Series(distance_column)
        distance_series_change = distance_series.pct_change(periods=14)
        distance_series_change_avrg = distance_series_change.median()

        #Calcuate average and median HR over time
        if 'Avrg_HR' in df.columns:
            hr_column = df['Avrg_HR']
            avrg_hr = hr_column.mean()
            median_hr = hr_column.median()

            #Calculate distance rate of change
            hr_series = pd.Series(hr_column)
            hr_series_change = hr_series.pct_change(periods=14)
            hr_series_change_avrg =hr_series_change.median()
        
        if 'Avrg_HR' in df.columns:
            html_output = html.Div([
                #html.H3('Key Stats:'),
                html.Div([
                    html.P(html.Hr()),
                    html.Em('Pace Stats:'),
                    html.P(),
                    html.B('Average Pace:'),
                    html.P(avrg_pace_mins),
                    html.B('Median Pace:'),
                    html.P(median_pace_mins),
                    html.B('Median Fortnightly Rate of change/Pace(%):'),
                    html.P(pace_series_change_avrg*(100)),
                    html.P(html.Hr()),
                    html.Em('Distance Stats:'),
                    html.P(),
                    html.B('Average Distance(m):'),
                    html.P(int(avrg_distance)),
                    html.B('Median Distance(m):'),
                    html.P(int(median_distance)),
                    html.B('Median Fortnightly Rate of change/Distance(%):'),
                    html.P(distance_series_change_avrg*(100)),
                    html.P(html.Hr()),
                    html.Em('HR Stats:'),
                    html.P(),
                    html.B('Average HR:'),
                    html.P(int(avrg_hr)),
                    html.B('Median HR:'),
                    html.P(int(median_hr)),
                    html.B('Median Fortnightly Rate of change/HR(%):'),
                    html.P(hr_series_change_avrg*(100)),
                    html.P(html.Hr()),
                    #html.P(str(text)),
                    #html.Code('Data Frame End:')
                ])
            ])
        else:
            html_output = html.Div([
                #html.H3('Key Stats:'),
                html.Div([
                    html.P(html.Hr()),
                    html.Em('Pace Stats:'),
                    html.P(),
                    html.B('Average Pace:'),
                    html.P(avrg_pace_mins),
                    html.B('Median Pace:'),
                    html.P(median_pace_mins),
                    html.B('Median Fortnightly Rate of change/Pace(%):'),
                    html.P(pace_series_change_avrg*(-100)),
                    html.P(html.Hr()),
                    html.Em('Distance Stats:'),
                    html.P(),
                    html.B('Average Distance(m):'),
                    html.P(int(avrg_distance)),
                    html.B('Median Distance(m):'),
                    html.P(int(median_distance)),
                    html.B('Median Fortnightly Rate of change/Distance(%):'),
                    html.P(distance_series_change_avrg*(100)),
                    #html.P(str(text)),
                    #html.Code('Data Frame End:')
                ])
            ])

        return html_output

    ###################################################
    ############ Draw subplots callback #############
    ###################################################


    @app.callback(Output('Graph2', "children"),
        [Input('Table1', "derived_virtual_data"),
        Input('Table1', "derived_virtual_selected_rows"),
        Input('df_type','value')])
    def update_graphs(rows, derived_virtual_selected_rows,df_type):
        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []

        dff = df0_smpl if rows is None else pd.DataFrame(rows)

        # Check what columns and data there are in the table and set variables accordingly
        if 'Strokes_PerMin' in dff.columns:
            dff_variable = dff['Strokes_PerMin']
            #Replace NaN values from the 'Storokes_PerMin column'
            dff_variable.fillna(23, inplace=True)
            text='<b>Swimming pace, distance and stroke count over time</b>'
            colorscale='blues'
            activity='SWIM'
            y1_title='Pace (min per 100m)'
            y2_title='Strokes per min'
            y1_dtick=0.5
            y2_dtick=5
            dist_trend=1000
        elif 'Norm_Power' in dff.columns:
            dff_variable = dff['Avrg_HR']
            #Replace NaN values from the 'Avrg_HR column'
            dff_variable.fillna(135, inplace=True)
            text='<b>Riding pace, distance and HR over time</b>'
            colorscale='mint'
            activity='RIDE'
            y1_title='Speed (kmph)'
            y2_title='HR (Beats per min)'
            y1_dtick=5
            y2_dtick=20
            dist_trend=10000
        else :
            dff_variable = dff['Avrg_HR']
            #Replace NaN values from the 'Avrg_HR column'
            dff_variable.fillna(135, inplace=True)
            text='<b>Running pace, distance and HR over time</b>'
            colorscale='peach'
            activity='RUN'
            y1_title='Pace (min per km)'
            y2_title='HR (Beats per min)'
            y1_dtick=0.5
            y2_dtick=20
            dist_trend=3000

        #Draw Pace Trendline
        m1,b1 = np.polyfit(dff['DateTime_Epoch'].astype(float),dff['Pace'].astype(float), 1)
        bestfit_y_pace = (dff['DateTime_Epoch'].astype(float) * m1 + b1)
        lineOfBestFit_Pace=go.Scattergl(x=dff['DateTime'],y=bestfit_y_pace,name='Pace Trend Line',line=dict(width=0.5,color='tomato',))

        #Draw Distance Trendline
        m2,b2 = np.polyfit(dff['DateTime_Epoch'].astype(float),dff['Distance'].astype(float)/dist_trend, 1)
        bestfit_y_distance = (dff['DateTime_Epoch'].astype(float) * m2 + b2)
        lineOfBestFit_Distance=go.Scattergl(x=dff['DateTime'],y=bestfit_y_distance,name='Distance Trend Line',text=(bestfit_y_distance)*1000,line=dict(width=0.5,color='tomato',))

        #Draw Stroke Count/Average HR Trendline
        m3,b3 = np.polyfit(dff['DateTime_Epoch'].astype(float),dff_variable.astype(float), 1)
        bestfit_y_variable = (dff['DateTime_Epoch'].astype(float) * m3 + b3)
        lineOfBestFit_Variable=go.Scattergl(x=dff['DateTime'],y=bestfit_y_variable,name='Variable Trend Line',text=bestfit_y_variable,line=dict(width=0.5,color='tomato',))

        # (!) Set 'size' values to be proportional to rendered area,
        #     instead of diameter. This makes the range of bubble sizes smaller
        sizemode='area'
        # (!) Set a reference for 'size' values (i.e. a distance-to-pixel scaling).
        #     Here the max bubble area will be on the order of 100 pixels
        sizeref=dff['Calories'].astype(float).max()/1000

        #Create an array of distances from dff
        calories_array = []
        for calories in dff['Calories']:
            calories_array.append(calories)

        colors = ['red' if i in derived_virtual_selected_rows else 'white'
            for i in range(len(dff))]

        colors2 = ['red' if i in derived_virtual_selected_rows else 'lightgrey'
            for i in range(len(dff))]

        outline = [6 if i in derived_virtual_selected_rows else 1
            for i in range(len(dff))]

        opacity = [1 if i in derived_virtual_selected_rows else 0.6
            for i in range(len(dff))]
        
        #Set Graph Watermark
        if df_type=='Sample Data':
            graph_watermark=str(df_type)
        else:
            graph_watermark=''

        #Function to set text on Datapoint hover
        def make_text(dff):
            if activity == 'SWIM':
                return 'Distance: %s meters\
                <br>Pace: %s min.sec\
                <br>Calories: %s kcal\
                <br>Strokes: %s per min'\
                % (dff['Distance'], dff['Pace'], dff['Calories'], dff['Strokes_PerMin'])
            elif activity == 'RUN':
                return 'Distance: %s meters\
                <br>Pace: %s min.sec\
                <br>Calories: %s kcal\
                <br>Avrg HR: %s beats per min'\
                % (dff['Distance'], dff['Pace'], dff['Calories'], dff['Avrg_HR'])
            elif activity == 'RIDE':
                return 'Distance: %s meters\
                <br>Pace: %s min.sec\
                <br>Calories: %s kcal\
                <br>Avrg HR: %s beats per min\
                <br>Norm Power: %s wats'\
                % (dff['Distance'], dff['Pace'], dff['Calories'], dff['Avrg_HR'], dff['Norm_Power'])

        trace1 = go.Scattergl(
            x=dff['DateTime'],
            y=dff['Pace'],
            text=dff.apply(make_text, axis=1).tolist(),
            name="Sessions",
            mode='markers',
            marker=dict(
                size=calories_array,
                sizeref=sizeref,
                sizemode=sizemode,
                opacity=opacity,
                color=dff['Distance'],
                showscale=True,
                colorscale=colorscale,
                colorbar=dict(
                    title='Distance',),
                line=dict
                (width=outline,color=colors,),
                    )
        )

        trace2 = go.Bar(
            x=dff['DateTime'],
            y=dff_variable,
            name='Stroke count',
            text=dff.apply(make_text, axis=1).tolist(),
            marker=dict
                (color='lightgrey',
                line=dict
                    (color=colors2,width=3,
                )
            )
        )

        layout1 = go.Layout(
            title=dict(
                text=text,
                font=dict(
                color='rgb(120, 120, 120)',
                )   
            ),
            xaxis=dict(
                type='date', 
                #title='DateTime',
                gridcolor='rgb(240, 240, 240)',
                gridwidth=0.5,
                ),
            xaxis2=dict(
                type='date', 
                #title='DateTime',
                gridcolor='rgb(240, 240, 240)',
                gridwidth=0.5,
                ),
            yaxis=dict(
                title=y1_title,
                gridcolor='rgb(240, 240, 240)',
                gridwidth=0.5,
                dtick=y1_dtick,
                ),
            yaxis2=dict(
                title=y2_title,
                gridcolor='rgb(240, 240, 240)',
                gridwidth=0.5,
                dtick=y2_dtick,
                ),
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='white',
            legend=go.layout.Legend(
                x=0.89,
                y=1,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="black"
                ),
                bgcolor="white",
                bordercolor="lightgrey",
                borderwidth=0.5
            ),
            annotations=[go.layout.Annotation(
                name="watermark",
                text=graph_watermark,
                textangle=-30,
                opacity=0.1,
                font=dict(color="black", size=100),
                xref="paper",
                yref="paper",
                #x=0.5,
                #y=0.5,
                #showarrow=False,
                ),
            ]
        )

        fig = make_subplots(rows=2, cols=1,shared_xaxes=True,vertical_spacing=0.01,row_heights=[0.45,0.15])



        fig.add_trace(trace1, row=1, col=1)
        fig.add_trace(trace2, row=2, col=1)
        fig.add_trace(lineOfBestFit_Pace, row=1, col=1)
        fig.add_trace(lineOfBestFit_Distance, row=1, col=1)
        fig.add_trace(lineOfBestFit_Variable, row=2, col=1)
        fig.update_layout(layout1)
        

        return [
            dcc.Graph(
                style={"height" : "80vh", "width" : "87vw",},
                figure=fig,)
        ]
    
    return app




