import requests
import configparser

# Here I grab the API key from the config file
config = configparser.ConfigParser()
config.read('config.conf')
BEA_API_KEY = config['APIKEYS']['BEA_API_KEY']

# Below is the URL for BEA testing and try statement below that.
url = 'https://apps.bea.gov/api/data?&' + 'UserId=' + BEA_API_KEY + '&method=GETDATASETLIST&' 
try:
    response = requests.get(url)
except Exception as err:
    print(f'There was an error: {err}')
else:
    print('Success!!')
    print(response.status_code)
finally:
    data = response.json()
    for dataset in data['BEAAPI']['Results']['Dataset']:
        print(dataset)

## AS OF Wed 5/3 the above works and prints the list of datasets to the consol