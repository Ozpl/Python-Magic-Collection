import os
import json
from datetime import datetime, timedelta
from os import path
from modules.consts import APP_FOLDER_STRUCTURE

class DefaultSettings:
    def __init__(self):
        self.debug_mode = False
        self.bulk_url = 'https://api.scryfall.com/bulk-data'
        self.time_format_full = '%H:%M:%S %d/%m/%Y'
        self.bulk_data_type = 'Default Cards'
        self.bulk_time_period = (60*60*24)
        self.bulk_last_updated = str((datetime.now()-timedelta(60)).strftime(self.time_format_full))
    
    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def create_file(self, file_path):
        json_file = json.loads(self.get_json())
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

def check_if_settings_exist(file_path):
    if not path.exists(file_path):
        settings = DefaultSettings()
        settings.create_file(file_path)

def load_settings(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        settings = json.load(f)
    return settings

def build_folder_structure():
    for element in APP_FOLDER_STRUCTURE:
        if not path.exists(f'./{APP_FOLDER_STRUCTURE[element]}'):
            os.mkdir(f'./{APP_FOLDER_STRUCTURE[element]}')