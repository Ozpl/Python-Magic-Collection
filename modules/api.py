import json
import requests
from os import path
from datetime import datetime
from modules.consts import SETTINGS_FOLDER_STRUCTURE
from modules.config import Config
from modules.logging import console_log

def get_bulk_data_response(url):
    request = requests.get(url)
    response = request.json()
    return response['data']

def download_bulk_json_file(url, file_name):
    console_log('info', 'Downloading new bulk_data')
    response = requests.get(url)
    with open(f'./{SETTINGS_FOLDER_STRUCTURE["downloads"]}/{file_name}.json', 'w', encoding='utf8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)
    console_log('info', 'bulk_data was downloaded successfully')

def get_data_from_scryfall():
    config = Config()
    
    bulk_response = get_bulk_data_response(config.get_value('BULK', 'url'))
    bulk_data_type = config.get_value('BULK', 'data_type')
    bulk_uri = [element['download_uri'] for element in bulk_response if element['name'] == bulk_data_type][0]

    time_difference = (datetime.now() - datetime.strptime(config.get_value('BULK', 'last_updated'), config.get_value('TIME', 'format_full'))).total_seconds()

    if time_difference > config.get_float('BULK', 'time_period'):
        config.set_value('FLAG', 'downloaded_from_scryfall', 'true')
        download_bulk_json_file(bulk_uri, bulk_data_type)
        config.set_value('BULK', 'last_updated', str(datetime.now().strftime(config.get_value('TIME', 'format_full'))))
    else:
        config.set_value('FLAG', 'downloaded_from_scryfall', 'false')

    if not path.exists(f'./{SETTINGS_FOLDER_STRUCTURE["downloads"]}/{bulk_data_type}.json'):
        config.set_value('FLAG', 'downloaded_from_scryfall', 'true')
        download_bulk_json_file(bulk_uri, bulk_data_type)

def restore_old_json_and_update_db_from_it():
    #TODO
    #Save old copy as backup and fall back to it if you get db error
    pass