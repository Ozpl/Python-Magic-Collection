import json, os
from modules.consts import SETTINGS_JSON_PATH, DATABASE_DB_PATH
from modules.settings import check_if_settings_exist, build_folder_structure, load_settings
from modules.ui import create_user_interface
from modules.api import get_data_from_scryfall
from modules.collection import create_default_collection
from modules.deck import create_default_deck
from modules.database.create import create_main_table, create_sub_tables
from modules.database.alpha import alpha_load
from modules.database.batch import batch_load
from modules.database.functions import create_connection

def build_database():
    if not os.path.exists('./database/database.db'):
        with open('./database/database.db', 'w'): pass
    connection = create_connection(DATABASE_DB_PATH)
    create_main_table(connection)
    create_sub_tables(connection)
    alpha_load(connection)
    #batch_load(connection)
    connection.close()

build_folder_structure()
check_if_settings_exist(SETTINGS_JSON_PATH)
#settings = load_settings() #unnecessary for now
get_data_from_scryfall()
create_default_collection()
create_default_deck()
build_database()
#create_user_interface()

#debug
'''
with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
    j = json.load(f)
    keys = []
    for i, element in enumerate(j):
        try:
            #if element['name'] == 'Arlinn Kord // Arlinn, Embraced by the Moon':
            for key in element.keys():
                if key not in keys:
                    keys.append(key)
        except Exception:
            pass
    print(keys)
'''