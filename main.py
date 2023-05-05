import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os

load_dotenv()

URL_POOL = ('AV_FOREX_URL','AV_OIL_WTI_URL','AV_COMMODITIES_INDEX_URL','AV_GDP_URL','AV_TYIELD_URL', 'AV_FUNDS_RATE_URL','AV_CPI_URL','AV_INFLATION_URL','AV_UNEMPLOYMENT_URL','MD_DJI_INDICES_URL')


def main():
    print("Inside main.py")
    
    for link in URL_POOL:
        print("inside for loop")
        if link == 'MD_DJI_INDICES_URL':
            pass
        try:
            print("Inside Try")
            url = os.get_env(link)
            response = requests.get(url)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'An HTTP error occurred on {link}: {http_err}')
        except Exception as err:
            print(f'There was an error with {link} /n', err)
        finally:
            print("DONE!")



# The above is untested as of 5/5/23