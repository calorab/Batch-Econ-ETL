import numpy as np
import pandas as pd
import sqlite3
from sqlite3 import OperationalError, Error
from dash import Dash, html, dcc
import plotly.express as px # for creating figures for graphs


def build_dashboard():

    build_layout()


def get_data():
    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Database Connection error \n', err)
    
    df = pd.read_sql("SELECT date, value FROM COMMODITIES_INDEX WHERE date >= '2003-01-01' ORDER BY date ASC ", conn)
    df['value'] = df['value'].astype(float)
    
    conn.close()
    return df


def build_layout():
    df = get_data()
    app = Dash(__name__)

    app.layout = html.Div([ 
        html.Div(Children=[
            html.label('Consumer Economic Indicators'),
            # insert table function here

            html.Br(),
            html.label('Banking Indicators'),
            # insert T/Fed graph
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            # insert main graph
            dcc.Checklist([]), # CALEB checklist items here - must be list!!!
        ], style={'padding': 10, 'flex': 1}) 
           
    ],style={'display': 'flex', 'flex-direction': 'row'})

    app.run_server(debug=True)
    # app.run_server(dev_tools_hot_reload=False) to remove hot-reloading

def build_econ_table():
    # get data - need MAX('value') for Inflation, GDP and CPI. May take some building html-wise
    # NEED A VIEW to get table titles**
    # Need a figure (px.[graph-type])
    return html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in df.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(df.iloc[i][col]) for col in df.columns
                    ]) for i in range(min(len(df), 10))
                ])
            ]), # CALEB Inflation, GDP, and CPI most recent numbers (more??)


def build_fed_graph():
    # need series for 'values' for 100 days for both T-Yield and Fed Funds Rate
    # Need a figure (px.[graph-type])
    return dcc.Graph([]) #CALEB T-Yield and Fed Funds Rate

def build_interactive_graph():
    # need funcs for callbacks
    # need figure for graph
    # need data from 
    return dcc.Graph([]), 


build_dashboard()