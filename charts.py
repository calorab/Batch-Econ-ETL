import numpy as np
import pandas as pd
import sqlite3
from sqlite3 import OperationalError, Error
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px # for creating figures for graphs


def build_dashboard():

    build_layout()


def get_data():
    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)

    query = '''SELECT * FROM CONSUMER_ECON_VW'''
    df = pd.read_sql_query(query, conn) 
    
    conn.close()
    return df


def build_layout():
    # df = get_data()
    app = Dash(__name__)

    app.layout = html.Div([ 
        html.Div([
            html.Label('Consumer Economic Indicators'),
            build_econ_table(),

            html.Br(),
            html.Label('Banking Indicators'),
            build_fed_graph(),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            # insert main graph
            dcc.Checklist([]), # CALEB checklist items here - must be list!!!
        ], style={'padding': 10, 'flex': 1}) 
           
    ], style={'display': 'flex', 'flex-direction': 'row'})

    app.run_server(debug=True)
    # app.run_server(dev_tools_hot_reload=False) to remove hot-reloading
    # The location of the app: http://127.0.0.1:8050/ 



def build_econ_table():
    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)

    query = '''SELECT * FROM CONSUMER_ECON_VW'''
    df = pd.read_sql_query(query, conn)
    # df['Value'] = df['Value'].astype(float)
    # Need a figure (px.[graph-type])
    return html.Table([
                html.Thead(
                    html.Tr([html.Td(df.columns[0]), html.Td(df.columns[1])])
                ),
                html.Tbody([html.Tr([html.Th(df.iloc[0][0]), html.Td(df.iloc[0][1])]), html.Tr([html.Th(df.iloc[1][0]), html.Td(df.iloc[1][1])]), html.Tr([html.Th(df.iloc[2][0]), html.Td(df.iloc[2][1])])])
                ], style={'padding': 10, 'flex': 1}) # CALEB Need to turn this into a loops or something eventually


def build_fed_graph():
    # need series for 'values' for 100 days for both T-Yield and Fed Funds Rate
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)
    
    query = '''SELECT * FROM FED_RATES_VW ORDER BY date DESC LIMIT 150'''
    df = pd.read_sql_query(query, conn)
    df['value'] = df['value'].astype(float)

    # Need a figure
    fig = px.line(df, x='date', y='value', color='indicator') # CALEB - NEEDS TESTING**
    return dcc.Graph(figure=fig, id='econ-graph-small') # CALEB T-Yield and Fed Funds Rate

def build_interactive_graph():
    # need funcs for callbacks
    # need figure for graph
    # need data from 
    return dcc.Graph(), 


build_dashboard()