import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os

load_dotenv()

URL_POOL = ('AV_FOREX_URL','AV_OIL_WTI_URL','AV_COMMODITIES_INDEX_URL','AV_GDP_URL','AV_TYIELD_URL', 'AV_FUNDS_RATE_URL','AV_CPI_URL','AV_INFLATION_URL','AV_UNEMPLOYMENT_URL','MD_DJI_INDICES_URL')


def main():
    print("Inside main()")
    
    for link in URL_POOL:
        if link == 'MD_DJI_INDICES_URL':
            print(link, " ...Bypassing")
            continue
        try:
            print("Inside Try \n")
            url = os.getenv(link)
            print(link, '\n', url, '\n')
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()
        except HTTPError as http_err:
            print(f'An HTTP error occurred on {link}: {http_err}')
        except Exception as err:
            print(f'There was an error with {link}', err)
        finally:
            print("DONE!\n")
            print(" ... ...\n")
            print(data)

main()

# tested as of 5/11 at nopon and all works as expected. Although Alpha Vantage limts API calls to 5 per min so need to adjust process for that
