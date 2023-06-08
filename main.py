import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os
import time
import pandas as p
import sqlite3
from sqlite3 import OperationalError, Error

from mapping import field_mapping as map

# Accessing the .env file in order to grab the URL's fopr GEt requests to the API's listed in the below tuple
load_dotenv()

AV_POOL = ('AV_FOREX_URL','AV_OIL_WTI_URL','AV_COMMODITIES_INDEX_URL','AV_GDP_URL','AV_TYIELD_URL', 'AV_FUNDS_RATE_URL','AV_CPI_URL','AV_INFLATION_URL','AV_UNEMPLOYMENT_URL','MD_DJI_INDICES_URL')
MD_POOL = ('MD_COMP_INDICES_URL', 'MD_NYA_INDICES_URL', 'MD_SPX_INDICES_URL', 'MD_XAU_INDICES_URL', 'MD_DJI_INDICES_URL')

def main():
    # av_api_call()

    md_api_call()


def build_av_data(data, source):
    
    # Define the mapped data for each API call
    data_set = data[map[source]['data_set']]
    data_base_table = map[source]['db_table']
    field_type = map[source]['fields']
    data_type = map[source]['data_set']
    # meta_data = map[source]['meta_data']

    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        print('Connection error \n', err)

    curr = conn.cursor()
    if field_type == 'dateValue':
         
        try:
            curr.execute('''CREATE TABLE IF NOT EXISTS ''' + data_base_table + '''(date TEXT, value TEXT)''')
            curr.execute('''DELETE FROM ''' + data_base_table)
            
            for record in data_set:
                curr.execute('''INSERT INTO ''' + data_base_table + ''' (date, value) VALUES (?,?)''', (record['date'], record['value']))
        except OperationalError as err:
            print(f'    Opp Error: {err}')
        except Error as err:
            print(err)
        

    else:

        try:
            curr.execute('''CREATE TABLE IF NOT EXISTS ''' + data_base_table + '''(date Text, open TEXT, high TEXT, low TEXT, close TEXT)''')
            curr.execute('''DELETE FROM ''' + data_base_table)
        
            for key, val in data_set.items():
                curr.execute('''INSERT INTO ''' + data_base_table + ''' (date, open, high, low, close) VALUES (?,?,?,?,?)''', (key, val['1. open'], val['2. high'], val['3. low'], val['4. close']))
        except OperationalError as err:
            print(f'    Opp Error: {err}')
        except Error as err:
            print(err)
        

        try:
            curr.execute('''CREATE TABLE IF NOT EXISTS ''' + data_base_table + '''(date Text, open TEXT, high TEXT, low TEXT, close TEXT)''')
            curr.execute('''DELETE FROM ''' + data_base_table)
         
            for key, val in data_set.items():
                curr.execute('''INSERT INTO ''' + data_base_table + ''' (date, open, high, low, close) VALUES (?,?,?,?,?)''', (key, val['1. open'], val['2. high'], val['3. low'], val['4. close']))
        except OperationalError as err:
            print(f'    Opp Error: {err}')
        except Error as err:
            print(err)
        

    # After creating a connection to sqlite DB I have to committhe changes and closethe connection
    conn.commit()
    conn.close()


def build_md_data(data, link):
    print(f'    Inside Build MD Data: {link}')



def av_api_call():
    # For each link in URL_POOL above do the below
    for link in AV_POOL:
        
        try:

            # get the link from .env file and make the API request. Check for errors and decode the JSON.
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

            # Insert data into Sqlite Database
            build_av_data(data, link)

            # 15 second delay due to API call limits for Alpha vantage (5 calls/min Max)
            print(f'15 second delay after call to {link}')
            time.sleep(15)

def md_api_call():
     for link in MD_POOL:
        try:
            # get the link from .env file and make the API request. Check for errors and decode the JSON.
            url = os.getenv(link)
            print(link,)
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()
        except HTTPError as http_err:
            print(f'An HTTP error occurred on {link}: {http_err}')
        except Exception as err:
            print(f'There was an error with {link}:', err)
        finally:

            # Insert data into Sqlite Database
            build_md_data(data, link)




# def format_md_response(res,name):
#     open = res['o']
#     print(name)
#     print(open)

main()


