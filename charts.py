import numpy as np
import pandas as pd
import sqlite3
from sqlite3 import OperationalError, Error
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px # for creating figures for graphs

#  CALEB - you need ECON data, CONSUMER data and INTERACTIVE data

def get_bank_data():
    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)

    query = '''SELECT * FROM FED_RATES_VW ORDER BY date ASC'''
    df = pd.read_sql_query(query, conn)
    df['value'] = df['value'].astype(float)
    
    conn.close()
    return df

def get_cons_data():
    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)

    query = '''SELECT * FROM CONSUMER_ECON_VW'''
    df = pd.read_sql_query(query, conn)
    
    
    conn.close()
    return df

app = Dash(__name__)
bank_df = get_bank_data()
cons_df = get_cons_data()
bank_figure = px.line(bank_df, x='date', y='value', color='indicator')

app.layout = html.Div([
    html.Div([
        html.Label('Consumer Economic Indicators'),
        html.Table([
            html.Thead(
                html.Tr([html.Td(cons_df.columns[0]), html.Td(cons_df.columns[1])])
            ),
            html.Tbody([html.Tr([html.Th(cons_df.iloc[0][0]), html.Td(cons_df.iloc[0][1])]), html.Tr([html.Th(cons_df.iloc[1][0]), html.Td(cons_df.iloc[1][1])]), html.Tr([html.Th(cons_df.iloc[2][0]), html.Td(cons_df.iloc[2][1])])])
            ], style={'padding': 10, 'flex': 1}), # CALEB Need to turn this into a loop or something eventually,

        html.Br(),
        html.Label('Banking Indicators'),
        dcc.Graph(id='econ-graph-small', figure=bank_figure)
    ], style={'padding': 10, 'flex': 1}),

    html.Div([
        dcc.Graph(id='main-graph'), #update function that returns a figure
        dcc.Checklist([]), 
    ], style={'padding': 10, 'flex': 1}) 
        
], style={'display': 'flex', 'flex-direction': 'row'})


# fig = px.line(df, x='date', y='value', color='indicator')
def update_interactive_graph(table):
    pass

app.run_server(debug=True)
# app.run_server(dev_tools_hot_reload=False) to remove hot-reloading
# The location of the app: http://127.0.0.1:8050/ 