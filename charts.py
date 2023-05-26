import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import hvplot.pandas
import panel as pn
import pandas as pd
import sqlite3
from sqlite3 import OperationalError, Error


def main():

    table = get_data()
    chart = table.plot(x='date',y='value', color='#88d8b0',line_width=6)
    return chart
    




def get_data():
    print('inside get data')

     # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Database Connection error \n', err)
    
    df = pd.read_sql("SELECT date, value FROM COMMODITIES_INDEX", conn)
    # Here we need to change the txts to date and float respectively
    return df




def chart_test():

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    fig, axs = plt.subplots(2,2) 
    fig, axs = plt.subplot_mosaic([['left', 'right-top'], ['left', 'right_bottom']])
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.
    axs.plot([1, 2, 3, 4], [1, 4, 2, 3])

    plt.show()





main()