import numpy as np
import pandas as pd
import sqlite3
from sqlite3 import OperationalError, Error
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px 
from mapping import field_mapping as map
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

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
    df['value'] = df['value'].astype(float)
    
    conn.close()
    return df

def build_dropdown():
    options = []
    options_map = {}

    for item in map.values():
        options.append(item['name'])
    
    for key,item in map.items():
       options_map[item['name']] = item['db_table']

    return options, options_map
    

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template("LUX")
                     
bank_df = get_bank_data()
cons_df = get_cons_data()
bank_figure = px.line(bank_df, x='date', y='value', color='indicator')
dp_options, dp_dict = build_dropdown()


app.layout = html.Div([
    html.H3('Economics dashboard', style={'font-weight': 'bold', 'text-align': 'center'}),
    html.Hr(),
    html.Div([
        html.Label('Consumer Economic Indicators', style={'font-weight': 'bold'}),
        html.Table([
            html.Thead(
                html.Tr([html.Td(cons_df.columns[0]), html.Td(cons_df.columns[1])])
            ),
            html.Tbody([html.Tr([html.Th(cons_df.iloc[0][0]), html.Td(cons_df.iloc[0][1])]), html.Tr([html.Th(cons_df.iloc[1][0]), html.Td(cons_df.iloc[1][1])]), html.Tr([html.Th(cons_df.iloc[2][0]), html.Td(cons_df.iloc[2][1])])])
            ], style={'padding': 10, 'flex': 1, 'textAlign': 'left'}), # CALEB Need to turn this into a loop or something eventually,

        html.Br(),
        html.Label('Banking Indicators', style={'font-weight': 'bold'}),
        dcc.Graph(id='econ-graph-small', figure=bank_figure)
    ], style={'padding': 10, 'flex': 1}),

    html.Div([
        dcc.Dropdown(dp_options, 'S&P 500', id='main-dropdown'),
        dcc.Graph(id='main-graph') #update function that returns a figure 
    ], style={'padding': 20, 'flex': 1, 'padding-top': 50}) 
        
], style={'display': 'flex', 'flex-direction': 'column', 'padding': 20, 'margin': 40,'border-style': 'solid', 'border-color': 'lightgrey', 'border-width': '1px', 'box-shadow': '2px 4px 4px rgba(0, 0, 0, 0.4)'})


@callback(
    Output('main-graph', 'figure'),
    Input('main-dropdown', 'value'))
def update_interactive_graph(index):
    # Here I need to (1) get the dataframe, (2) build the figure and (3) return the figure
    table = dp_dict[index]
    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)

    query = f'SELECT * FROM {table} ORDER BY date ASC'
    df = pd.read_sql_query(query, conn)

    y_axis = None
    if index in ['WTI OIL', 'Commodities Index']:
        y_axis = 'value'
    else:
        y_axis = 'close'
    
    df[y_axis] = df[y_axis].astype(float)
    fig = px.line(df, x='date', y=y_axis)
    conn.close()
    # also need dropdown list for interactivity (line 60)
    return fig

app.run_server(debug=True)
# app.run_server(dev_tools_hot_reload=False) to remove hot-reloading
# The location of the app: http://127.0.0.1:8050/ 
