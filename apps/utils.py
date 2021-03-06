import pandas as pd
import requests
from requests.exceptions import HTTPError

# host = "http://tribedemo.expertsoftware.in/"
host = "http://95.217.5.215:8080/"


def fetch_data(path):
    url = host + path
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
    response = fetch_data('states/')
    data = pd.read_json(response)
    data_states = pd.json_normalize(data['data'])
    return data_states


def fetch_districts():
    response = fetch_data('districts/')
    data = pd.read_json(response)
    data_districts = pd.json_normalize(data['data'])
    return data_districts


def fetch_district_pop(state):
    state_code = get_state_code(state)
    response = fetch_data('population/' + state_code)
    data = pd.read_json(response)
    district_pop = pd.json_normalize(data['data'])
    return district_pop


def fetch_district_lit(state):
    state_code = get_state_code(state)
    response = fetch_data('literacy/' + state_code)
    data = pd.read_json(response)
    district_lit = pd.json_normalize(data['data'])
    return district_lit


def fetch_district_gratio(state):
    state_code = get_state_code(state)
    response = fetch_data('genderratio/' + state_code)
    data = pd.read_json(response)
    district_gratio = pd.json_normalize(data['data'])
    return district_gratio


def fetch_server_data(path):
    url = path
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


def fetch_local_data(path):
    try:
        data = open(path, 'r').read()
        # data = pd.json_normalize(file['data'])
    except Exception as err:
        print(f'Error occurred: {err}')
    else:
        pass
    return data


state_list = fetch_states()
districts_list = fetch_districts()


ind_state_list = [{'label': 'India', 'value': 'India'}, {'label': '-----', 'value': '-----', 'disabled': True}]
for state in state_list['state_name'].sort_values():
    ind_state_list.append({'label': state, 'value': state})

# state_pop = fetch_server_data('http://95.217.5.215:8080/population/')
# state_gratio = fetch_server_data('http://95.217.5.215:8080/genderratio/')
# state_lit = fetch_server_data('http://95.217.5.215:8080/literacy/')

# state_pop = fetch_data('population')
# state_lit = fetch_local_data('data/literacy.json')
# state_gratio = fetch_data('genderratio')


def get_state_code(state):
    state_code = state_list.loc[state_list['state_name'] == state, 'state_code'].iloc[0]
    return state_code


def get_district_name(district_code):
    district_name = districts_list.loc[districts_list['district_code'] == district_code, 'district_name'].iloc[0]
    return district_name


def get_district_code(district):
    district_code = districts_list.loc[districts_list['district_name'] == district, 'district_code'].iloc[0]
    return district_code


# print(get_district_name('1'))
# print(get_district_code('Chennai'))

# Religion Page


# religious_demo = fetch_data('religiousdemo')


def fetch_rel_district_demo(state):
    state_code = get_state_code(state)
    response = fetch_data('religiousdemo/all/' + state_code)
    data = pd.read_json(response)
    district_rel_demo = pd.json_normalize(data['data'])
    return district_rel_demo

