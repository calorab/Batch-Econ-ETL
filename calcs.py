import numpy as np
import pandas as pd
import sqlite3
from mapping import field_mapping as map

# THE BELOW NEEDS TO BE TESTED!!!!! 
# ALSO MAY NEED TO BE EDITED FOR NON CANDLE FORMATTED TABLES (i.e date/value format) 
# Although that would only be for Oil and Commodities Indices which I won't be charting in version 1

def build_sma_crossover(table,field_type):
    conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')

    query = f'SELECT * FROM {table} ORDER BY date ASC'

    df = pd.read_sql_query(query, conn)

    if field_type == 'candles':
        df['close'] = df['close'].astype(float)
        # Calculating SMA (Smple Moving Average)
        sma_one = 20
        sma_two = 50

        sma_short = df['close'].rolling(sma_one).mean()
        print('The SMA one: \n', type(sma_short)) #pandas series

        sma_long = df['close'].rolling(sma_two).mean()
        print('The SMA two: \n', type(sma_long)) #pandas series
    else:
        df['value'] = df['value'].astype(float)
        # Calculating SMA (Smple Moving Average)
        sma_one = 20
        sma_two = 50

        sma_short = df['value'].rolling(sma_one).mean()
        print('The SMA one: \n', type(sma_short)) #pandas series

        sma_long = df['value'].rolling(sma_two).mean()
        print('The SMA two: \n', type(sma_long)) #pandas series

    conn.close()
    return sma_short,sma_long


def build_ema(table,field_type):
    conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')

    query = f'SELECT * FROM {table} ORDER BY date ASC'

    df = pd.read_sql_query(query, conn)
    if field_type == 'candles':

        df['close'] = df['close'].astype(float)
        
        # Calculating EMA (Exponential Moving Average)
        ema_period = 20
        ema = df['close'].rolling(ema_period).mean()
    else:
        df['value'] = df['value'].astype(float)
        
        # Calculating EMA (Exponential Moving Average)
        ema_period = 20
        ema = df['value'].rolling(ema_period).mean()
    
    conn.close()
    return ema


def build_bands(table,field_type):
    conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')

    query = f'SELECT * FROM {table} ORDER BY date ASC'

    df = pd.read_sql_query(query, conn)

    if field_type == 'candles':
        # Step 3: Convert string values to numbers
        df['close'] = df['close'].astype(float)
        df['sma'] = df['close'].rolling(20).mean()
        df['date'] = df['date'] # maybe don't need this??

        # Calculating Bolinger bands
        bb_period = 20
        df['std'] = df['close'].rolling(bb_period).std()
        df['upper_band'] = df['sma'] + 2 * df['std']
        df['lower_band'] = df['sma'] - 2 * df['std']
    else:
        # Step 3: Convert string values to numbers
        df['value'] = df['value'].astype(float)
        df['sma'] = df['value'].rolling(20).mean()
        df['date'] = df['date'] # maybe don't need this??

        # Calculating Bolinger bands
        bb_period = 20
        df['std'] = df['value'].rolling(bb_period).std()
        df['upper_band'] = df['sma'] + 2 * df['std']
        df['lower_band'] = df['sma'] - 2 * df['std']
    # print(df)

    df.to_sql(table, conn, if_exists='replace', index=False)


    conn.close()
