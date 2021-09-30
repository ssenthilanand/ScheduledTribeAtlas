import pandas as pd
import requests
from requests.exceptions import HTTPError

host = "http://tribedemo.expertsoftware.in/"


def fetch_data(path):
    url = host + path + '/'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        pass
    return response.text


def fetch_states():
    response = fetch_data('states')
    data = pd.read_json(response)
    data_states = pd.json_normalize(data['data'])
    return data_states


def fetch_districts():
    response = fetch_data('districts')
    data = pd.read_json(response)
    data_districts = pd.json_normalize(data['data'])
    return data_districts

