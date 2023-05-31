import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import panel as pn
import hvplot.pandas
import sqlite3
from sqlite3 import OperationalError, Error

pn.extension() # for using panel inside vscode

def main():

    df = get_data()
    chart = df.plot(x='date',y='value', color='#88d8b0')
    # create pandas' data pipeline for widgets
    # make widgets
    # plot 
    # Use panel to display in browser
    plt.show()
    
    




def get_data():
    print('inside get data')

     # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Database Connection error \n', err)
    
    df = pd.read_sql("SELECT date, value FROM COMMODITIES_INDEX WHERE date >= '2003-01-01' ORDER BY date DESC ", conn)
    df['value'] = df['value'].astype(float)
    
    return df




def chart_test():

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    fig, axs = plt.subplots(2,2) 
    fig, axs = plt.subplot_mosaic([['left', 'right-top'], ['left', 'right_bottom']])
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.
    axs.plot([1, 2, 3, 4], [1, 4, 2, 3])

    plt.show()





main()