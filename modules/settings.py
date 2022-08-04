import json
from os import path

class DefaultSettings:
    def __init__(self):
        self.bulk_url = 'https://api.scryfall.com/bulk-data'
        self.bulk_file_type = 'Default Cards'
    
    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def create_file(self, file_path):
        json_file = json.loads(self.get_json())
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

def check_if_settings_exists(file_path):
    file_found = path.exists(file_path)
    if not file_found:
        settings = DefaultSettings()
        settings.create_file(file_path)

def load_settings_json(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        settings_json = json.load(f)
    return settings_json