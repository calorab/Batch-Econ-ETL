import numpy as np
import pandas as pd
import sqlite3

# THE BELOW NEEDS TO BE TESTED!!!!! 
# ALSO MAY NEED TO BE EDITED FOR NON CANDLE FORMATTED TABLES (i.e date/value format) 
# Although that would only be for Oil and Commodities Indices which I won't be charting in version 1

def build_sma_crossover(table):
    conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')

    query = f'SELECT * FROM {table} ORDER BY date ASC'

    df = pd.read_sql_query(query, conn)
    df['close'] = df['close'].astype(float)
    # Calculating SMA (Smple Moving Average)
    sma_one = 20
    sma_two = 50

    sma1 = df['close'].rolling(sma_one).mean()
    print('The SMA one: \n', type(sma1)) #pandas series

    sma2 = df['close'].rolling(sma_two).mean()
    print('The SMA two: \n', type(sma2)) #pandas series

    return sma1,sma2

def build_ema(table):
    conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')

    query = f'SELECT * FROM {table} ORDER BY date ASC'

    df = pd.read_sql_query(query, conn)
    df['close'] = df['close'].astype(float)
    
    # Calculating EMA (Exponential Moving Average)
    ema_period = 20
    ema = df['close'].rolling(ema_period).mean()

    return ema


def build_bands(table):
    conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')

    query = f'SELECT * FROM {table} ORDER BY date ASC'

    df = pd.read_sql_query(query, conn)

    # Step 3: Convert string values to numbers
    df['close'] = df['close'].astype(float)

    # #  Calculating Bolinger bands
    bb_period = 20
    df['std'] = df['close'].rolling(bb_period).std()
    df['upper_band'] = df['sma'] + 2 * df['std']
    df['lower_band'] = df['sma'] - 2 * df['std']

    # print(df)

    df.to_sql(table, conn, if_exists='replace', index=False)


    conn.close()


build_sma_crossover('NASDAQ_COMPOSITE_INDEX')