import numpy as np
import pandas as pd
import sqlite3

# THE BELOW NEEDS TO BE EDITED FOR NON CANDLE FORMATTED TABLES (i.e date/value format) 
# Although that would only be for Oil and Commodities Indices which I won;'t be investing in or charting in version 1

def build_calcs_table(table):
    conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')

    query = f'SELECT * FROM {table} ORDER BY date ASC'

    df = pd.read_sql_query(query, conn)

    # Step 3: Convert string values to numbers
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['open'] = df['open'].astype(float)
    df['low'] = df['low'].astype(float)

    # Calculating SMA (Smple Moving Average)
    sma_period = 20
    df['sma'] = df['close'].rolling(sma_period).mean()

     # Calculating EMA (Exponential Moving Average)
    ema_period = 20
    df['ema'] = df['close'].rolling(ema_period).mean()

    #  Calculating Bolinger bands
    bb_period = 20
    df['std'] = df['close'].rolling(bb_period).std()
    df['upper_band'] = df['sma'] + 2 * df['std']
    df['lower_band'] = df['sma'] - 2 * df['std']

    # print(df)

    df.to_sql(table, conn, if_exists='replace', index=False)


    conn.close()