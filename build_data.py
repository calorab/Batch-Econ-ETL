import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os
import csv
import time
import pandas as p
from pandas import io
import sqlite3
from sqlite3 import OperationalError, Error
import logging

from mapping import field_mapping as map

# Accessing the .env file in order to grab the URL's fopr GET requests to the API's listed in the below tuple
load_dotenv()
logging.basicConfig(filename='api_calls.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s')

AV_POOL = ('AV_FOREX_URL','AV_OIL_WTI_URL','AV_COMMODITIES_INDEX_URL','AV_GDP_URL','AV_TYIELD_URL', 'AV_FUNDS_RATE_URL','AV_CPI_URL','AV_INFLATION_URL','AV_UNEMPLOYMENT_URL','MD_DJI_INDICES_URL')
MD_POOL = ('MD_COMP_INDICES_URL', 'MD_NYA_INDICES_URL', 'MD_SPX_INDICES_URL', 'MD_XAU_INDICES_URL', 'MD_DJI_INDICES_URL')

def main():
    # GET data from Alpha-Vantage API
    av_api_call()

    # GET data from Market Data API
    md_api_call()

    # Build views for Dashboard
    build_views()


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
        logging.info('Connection error \n', err)

    curr = conn.cursor()
    if field_type == 'dateValue':
         
        try:
            curr.execute('''CREATE TABLE IF NOT EXISTS ''' + data_base_table + '''(date TEXT, value TEXT)''')
            curr.execute('''DELETE FROM ''' + data_base_table)
            
            for record in data_set:
                curr.execute('''INSERT INTO ''' + data_base_table + ''' (date, value) VALUES (?,?)''', (record['date'], record['value']))
        except OperationalError as err:
            logging.info(f'    Opp Error: {err}')
        except Error as err:
            logging.info(err)
        

    else:

        try:
            curr.execute('''CREATE TABLE IF NOT EXISTS ''' + data_base_table + '''(date Text, open TEXT, high TEXT, low TEXT, close TEXT)''')
            curr.execute('''DELETE FROM ''' + data_base_table)
        
            for key, val in data_set.items():
                curr.execute('''INSERT INTO ''' + data_base_table + ''' (date, open, high, low, close) VALUES (?,?,?,?,?)''', (key, val['1. open'], val['2. high'], val['3. low'], val['4. close']))
        except OperationalError as err:
            logging.info(f'    Opp Error: {err}')
        except Error as err:
            logging.info(err)
        

    # After creating a connection to sqlite DB I have to committhe changes and close the connection
    conn.commit()
    conn.close()


def build_md_data(data, source):
    data_base_table = map[source]['db_table']
    
    csv_data = data.splitlines()
    reader = csv.reader(csv_data)

    # Extract the header row and remaining data rows
    header = next(reader)
    data_rows = list(reader)

    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        logging.info('Connection error \n', err)

    curr = conn.cursor()

    try:
        curr.execute(f"CREATE TABLE IF NOT EXISTS {data_base_table} ( open TEXT, close TEXT, high TEXT, low TEXT, volume TEXT, date Text)") 
        curr.execute('''DELETE FROM ''' + data_base_table)

        insert_query = f"INSERT INTO {data_base_table} VALUES ({', '.join(['?'] * len(header))})"

        for row in data_rows:
            curr.execute(insert_query, row)
    except OperationalError as err:
        logging.info(f'    Opp Error: {err}')
    except Error as err:
        logging.info(err)
    finally:
        # After creating a connection to sqlite DB I have to committhe changes and closethe connection
        conn.commit()
        conn.close()



def av_api_call():
    # For each link in URL_POOL above do the below
    for link in AV_POOL:
        
        try:
            # get the link from .env file and make the API request. Check for errors and decode the JSON.
            url = os.getenv(link)
            logging.info(link, '\n', url, '\n')
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()
        except HTTPError as http_err:
            logging.info(f'An HTTP error occurred on {link}: {http_err}')
        except Exception as err:
            logging.info(f'There was an error with {link}:', err)
        finally:

            # Insert data into Sqlite Database
            build_av_data(data, link)

            # 15 second delay due to API call limits for Alpha vantage (5 calls/min Max)
            logging.info(f'15 second delay after call to {link}')
            time.sleep(15)
        
 
def md_api_call():
     for link in MD_POOL:
        try:
            # get the link from .env file and make the API request. Check for errors and decode the JSON.
            url = os.getenv(link)
            logging.info(link,)
            response = requests.get(url)

            response.raise_for_status()
            data = response.text

        except HTTPError as http_err:
            logging.info(f'An HTTP error occurred on {link}: {http_err}')
        except Exception as err:
            logging.info(f'There was an error with {link}:', err)
        finally:

            # Insert data into Sqlite Database
            build_md_data(data, link)

def build_views():
    # Check for innitial DB connection issue
    try:
        conn = sqlite3.connect('MACRO_ECONOMIC_DATA.db')
    except Error as err:
        logging.info('Connection error \n', err)

    curr = conn.cursor()

    # Build CONSUMER_ECON_VW View
    curr.execute('''DROP VIEW IF EXISTS CONSUMER_ECON_VW;''')
    curr.execute('''CREATE VIEW CONSUMER_ECON_VW AS
        SELECT 'INFLATION' AS indicator, inf.value AS value
        FROM US_INFLATION inf
        WHERE inf.date = (SELECT MAX(date) FROM US_INFLATION)
        UNION ALL
        SELECT 'GDP (Quarterly)' AS indicator, gdp.value AS value
        FROM US_GDP_Quarterly gdp
        WHERE gdp.date = (SELECT MAX(date) FROM US_GDP_Quarterly)
        UNION ALL
        SELECT 'CPI' AS indicator, cpi.value AS value
        FROM US_CPI cpi
        WHERE cpi.date = (SELECT MAX(date) FROM US_CPI)
        UNION ALL
        SELECT 'Treasury Yield' AS indicator, ty.value AS value
        FROM US_TREASURY_YIELD ty
        WHERE ty.date = (SELECT MAX(date) FROM US_TREASURY_YIELD)
        UNION ALL
        SELECT 'Fed Funds Rate' AS indicator, ffr.value AS value
        FROM US_FEDERAL_FUNDS_RATE ffr
        WHERE ffr.date = (SELECT MAX(date) FROM US_FEDERAL_FUNDS_RATE);''')
    
    # # Build FED_RATES_VW View
    # curr.execute('''DROP VIEW IF EXISTS FED_RATES_VW;''')
    # curr.execute('''CREATE VIEW FED_RATES_VW AS
    #     SELECT date, value, 'Tresury Yield' as indicator FROM US_TREASURY_YIELD
    #     UNION ALL
    #     SELECT date, value, 'Federal Funds Rate' as indicator FROM US_FEDERAL_FUNDS_RATE;''')
    
    conn.commit()
    conn.close()




main()


