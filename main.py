import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os
import time
import pandas as p
import sqlite3
from sqlite3 import OperationalError, Error

from mapping import field_mapping as map


load_dotenv()

URL_POOL = ('AV_FOREX_URL','AV_OIL_WTI_URL','AV_COMMODITIES_INDEX_URL','AV_GDP_URL','AV_TYIELD_URL', 'AV_FUNDS_RATE_URL','AV_CPI_URL','AV_INFLATION_URL','AV_UNEMPLOYMENT_URL','MD_DJI_INDICES_URL')


def main():

    for link in URL_POOL:
        if link == 'MD_DJI_INDICES_URL':
            print(link, " ...Bypassing")
            continue
        try:
            url = os.getenv(link)
            print(link, '\n', url, '\n')
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()
        except HTTPError as http_err:
            print(f'An HTTP error occurred on {link}: {http_err}')
        except Exception as err:
            print(f'There was an error with {link}:', err)
        finally:
            print('Inside Finally block')
            # HERE INSERT format_data function call
            build_data(data, link)
            print(f'15 second delay after call to {link}')
            time.sleep(15)


def build_data(data, source):
    # Define the mapped data for each API call
    data_set = data[map[source]['data_set']]
    data_base_table = map[source]['db_table']
    field_type = map[source]['fields']
    meta_data = map[source]['meta_data']

# tested the below and get the correct info YAY! (5/16/23 @ 4:15)
    print(f'Data table name for {source}: ', data_base_table)
    print(f'Field type for {source}: ', field_type)
    print(f'Meta data for {source}?: ', meta_data)
    # print(f'Data set example for {source} (first only): \n', data_set)

    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)

    curr = conn.cursor()
    if field_type == 'dateValue':
        try:
            curr.execute('''CREATE TABLE IF NOT EXISTS ''' + data_base_table + '''(date TEXT, value TEXT)''')
            print('after create table')
            curr.execute('''DELETE FROM ''' + data_base_table)
            print('after vacuum')

            for record in data_set:
                curr.execute('''INSERT INTO ''' + data_base_table + ''' (date, value) VALUES (?,?)''', (record['date'], record['value']))
        except OperationalError as err:
            print(f'    Opp Error: {err}')
        except Error as err:
            print('Ya done fucked up! dateValue-style', err)
        

    else:
        try:
            curr.execute('''CREATE TABLE IF NOT EXISTS ''' + data_base_table + '''(open TEXT, high TEXT, low TEXT, close TEXT)''')
            print('after create table')

            curr.execute('''DELETE FROM ''' + data_base_table)
         
            for record in data_set:
                curr.execute('''INSERT INTO ''' + data_base_table + ''' (open, high, low, close) VALUES (?,?,?,?)''', (record[0], record[1], record[2], record[3]))
        except OperationalError as err:
            print(f'    Opp Error: {err}')
        except Error as err:
            print('Ya done fucked up! candle-style', err)
        

    
    conn.commit()
    conn.close()


main()


