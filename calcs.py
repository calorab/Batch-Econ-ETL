import numpy as np
import pandas as pd
import sqlite3
from mapping import field_mapping as map


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
