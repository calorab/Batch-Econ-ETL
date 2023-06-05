import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import panel as pn
import hvplot.pandas
import sqlite3
from sqlite3 import OperationalError, Error
from dash import Dash, html, dash_table


def main():

    build_dashboard()


    
    
    




def get_data():
    print('inside get data')

     # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Database Connection error \n', err)
    
    df = pd.read_sql("SELECT date, value FROM COMMODITIES_INDEX WHERE date >= '2003-01-01' ORDER BY date ASC ", conn)
    df['value'] = df['value'].astype(float)
    print(df)
    
    return df




def build_dashboard():
    df = get_data()
    app = Dash(__name__)

    app.layout = html.Div([
        html.Div(children="Caleb's First App with Data"),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10)
    ])

    app.run_server(debug=True)





main()