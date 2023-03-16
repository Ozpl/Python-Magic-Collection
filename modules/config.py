from typing import Any

class Config:
    '''Class which stores all settable variables as strings in .ini file using ConfigParser library. Use 'set_value' and 'get_x', where x can be 'bool', 'int', 'float' or 'value'.'''
    def __init__(self) -> None:
        from configparser import ConfigParser
        
        self.config_parser = ConfigParser()
        self.load()

    def create_default_config_file(self) -> None:
        from datetime import datetime, timedelta
        self.config_parser['DEFAULT'] = {}
        self.config_parser['FLAG'] = {
            'downloaded_from_scryfall': 'false',
            'database_was_created': 'false',
            'collections_was_created': 'false',
            'decks_was_created': 'false',
            'corner_refreshing': 'false',
            'collection_needs_refreshing': 'false',
            'progression_needs_refreshing': 'false',
            'decks_needs_refreshing': 'false',
            'wishlist_needs_refreshing': 'false'
        }
        self.config_parser['FOLDER'] = {
            'database': 'database',
            'images': 'images',
            'cards': 'images/cards',
            'symbols': 'images/symbols',
            'sets': 'images/sets'
        }
        self.config_parser['FILE'] = {
            'database': f"./{self.config_parser['FOLDER']['database']}/database.db",
            'collections': f"./{self.config_parser['FOLDER']['database']}/collections.db",
            'decks': f"./{self.config_parser['FOLDER']['database']}/decks.db"
        }
        self.config_parser['TIME'] = {
            'format_full': '%H:%M:%S %d/%m/%Y'.replace('%','%%')
        }
        self.config_parser['BULK'] = {
            'url': 'https://api.scryfall.com/bulk-data',
            'data_type': 'Default Cards',
            'time_period': str((60*60*24*7)),
            'last_updated': str((datetime.now() - timedelta(8)).strftime(self.config_parser['TIME']['format_full']))
        }
        self.config_parser['APP'] = {
            'name': 'Python Magic Collection',
            'style': 'Fusion',
            'font': 'MS Shell Dlg 2',
            'font_size': str(13),
            'collection': 'Collection',
            'progression': 'Progression',
            'decks': 'Decks',
            'add_cards': 'Add cards',
            'wishlist': "Wishlist",
            'import_export': 'Import/export',
            'settings': 'Settings'
        }
        self.config_parser['COLLECTION'] = {
            'show_database': 'false',
            'image_type': 'normal',
            'image_extension': 'jpg',
            'price_source': 'eur',
            'price_currency': 'pln',
            'exchange_rate': '1.0',
            'current_collection': 'maincollection',
            'current_page': '1',
            'current_filter': '',
            'current_filtered_page': '1'
        }
        self.config_parser['PROGRESSION_TYPES'] = {            
            'core' : 'true',
            'expansion' : 'true',
            'draft_innovation' : 'true',
            'masters' : 'true',
            'commander' : 'true',
            'box' : 'true',
            'spellbook' : 'true',
            'from_the_vault' : 'true',
            'duel_deck' : 'true',
            'premium_deck' : 'true',
            'masterpiece' : 'true',
            'arsenal' : 'true',
            'promo' : 'true',
            'starter' : 'false',
            'archenemy' : 'false',
            'planechase' : 'false',
            'treasure_chest' : 'false',
            'vanguard' : 'false',
            'alchemy' : 'false',
            'memorabilia' : 'false',
            'funny' : 'false',
            'token' : 'false',
            'minigame': 'false'
        }
        self.config_parser['PROGRESSION_SHOW'] = {
            'completed': 'false',
            'partial': 'false',
            'empty': 'true',
        }
        self.save()
        self.load()

    def save(self) -> None:
        with open(f'config.ini', 'w') as f: self.config_parser.write(f)

    def load(self) -> None:
        self.config_parser.read(f'config.ini')

    def get_boolean(self, section: str, option: str) -> bool:
        self.load()
        return self.config_parser.getboolean(section.upper(), option.lower())

    def get_int(self, section: str, option: str) -> int:
        self.load()
        return self.config_parser.getint(section.upper(), option.lower())
        
    def get_float(self, section: str, option: str) -> float:
        self.load()
        return self.config_parser.getfloat(section.upper(), option.lower())

    def get(self, section: str, option: str) -> str:
        self.load()
        return self.config_parser[section.upper()][option.lower()]

    def set(self, section: str, option: str, value: Any) -> None:
        self.config_parser[section.upper()][option.lower()] =  str(value)
        self.save()

    def build_folder_structure(self) -> None:
        from os import mkdir, path
        
        for folder in self.config_parser['FOLDER']:
            if not path.exists(f"./{self.config_parser['FOLDER'][folder]}"):
                mkdir(f"./{self.config_parser['FOLDER'][folder]}")
    
    def build_file_structure(self) -> None:
        from os import path

        for file in self.config_parser['FILE']:
            if file != 'config':
                if not path.exists(self.config_parser['FILE'][file]):
                    with open(self.config_parser['FILE'][file], 'w'): pass
                    self.set('FLAG', f'{file}_was_created', 'true')
                else:
                    self.set('FLAG', f'{file}_was_created', 'false')
