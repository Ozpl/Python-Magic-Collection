import json
import requests
from os import path
from datetime import datetime
from modules.settings import load_settings
from modules.consts import SETTINGS_JSON_PATH

def get_bulk_data_response(url):
    request = requests.get(url)
    response = request.json()
    return response['data']

def download_bulk_json_file(url, file_name):
    print(f'New bulk data is being downloaded - {datetime.now()}')
    response = requests.get(url)
    with open(f'./downloads/{file_name}.json', 'w', encoding='utf8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)
    print(f'New bulk data downloaded - {datetime.now()}')

def get_data_from_scryfall():
    SETTINGS_JSON = load_settings(SETTINGS_JSON_PATH)
    bulk_response = get_bulk_data_response(SETTINGS_JSON['bulk_url'])
    bulk_data_type = SETTINGS_JSON['bulk_data_type']
    bulk_uri = [element['download_uri'] for element in bulk_response if element['name'] == bulk_data_type][0]

    time_difference = (datetime.now() - datetime.strptime(SETTINGS_JSON['bulk_last_updated'], SETTINGS_JSON['time_format_full'])).total_seconds()

    if time_difference > SETTINGS_JSON['bulk_time_period']:
        download_bulk_json_file(bulk_uri, bulk_data_type)
        with open(SETTINGS_JSON_PATH, 'w', encoding='utf8') as f:
            file_content = SETTINGS_JSON
            file_content['bulk_last_updated'] = str(datetime.now().strftime(SETTINGS_JSON['time_format_full']))
            json.dump(file_content, f, ensure_ascii=False, indent=4)

    if not path.exists(f'./downloads/{bulk_data_type}.json'):
        download_bulk_json_file(bulk_uri, bulk_data_type)


def restore_old_json_and_update_db_from_it():
    pass
    #TODO
    #Save old copy as backup and fall back to it if you get db error