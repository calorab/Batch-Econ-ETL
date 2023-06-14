import numpy as np
import pandas as pd
import sqlite3
from sqlite3 import OperationalError, Error
from dash import Dash, html, dcc


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
    
    return df


def build_layout():
    df = get_data()
    app = Dash(__name__)

    app.layout = html.Div([
        '''

        html.Div(Children=[
            html.label('Consumer Economic Indicators'),
            html.Table([CALEB Inflation, GDP, and CPI most recent numbers (more??)]),

            html.Br(),
            html.label('Banking Indicators'),
            dcc.Graph([CALEB T-Yield and Fed Funds Rate])
        ], CALEB styling goes here),

        html.Div([
            dcc.Graph([CALEB MEAT AND POTATOES!!!]),
            dcc.Checklist([CALEB checklist items here - must be list!!!]),

        ], CALEB Styling again)
        
        '''
        
    ])

    app.run_server(debug=True)
    # app.run_server(dev_tools_hot_reload=False) to remove hot-reloading



build_dashboard()