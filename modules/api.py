import os
import json
import requests
from settings import load_settings_json
from dotenv import load_dotenv

load_dotenv()

def get_bulk_data(url):
    request = requests.get(url)
    response = request.json()
    return response['data']

def download_bulk_json_file(url, name):
    response = requests.get(url)
    with open(f'./downloads/{name}.json', 'w', encoding='utf8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)

settings = load_settings_json(os.getenv('SETTINGS_FILE_PATH'))

bulk_response = get_bulk_data(settings['bulk_url'])
bulk_data_type = settings['bulk_file_type']
bulk_uri = [element['download_uri'] for element in bulk_response if element['name'] == bulk_data_type][0]

download_bulk_json_file(bulk_uri, bulk_data_type)