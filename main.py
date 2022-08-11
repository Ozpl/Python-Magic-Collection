import json
from modules.consts import SETTINGS_FILE_PATH, DATABASE_PATH, SUBTABLES_NAMES
from modules.settings import check_if_settings_exist, build_folder_structure, load_settings
from modules.ui import create_ui
from modules.api import get_data_from_scryfall
from modules.collection import create_default_collection
from modules.deck import create_default_deck
from modules.database.create import create_main_table, create_sub_table
from modules.database.alpha import alpha_load
from modules.database.batch import batch_load
from modules.database.functions import create_connection

def build_database():
    connection = create_connection(DATABASE_PATH)
    #create_main_table(connection)
    #just one subtable for now
    #create_sub_table(connection, SUBTABLES_NAMES[0])
    #alpha_load(connection)
    batch_load(connection)
    connection.close()

build_folder_structure()
check_if_settings_exist(SETTINGS_FILE_PATH)
#settings = load_settings() - unnecessary for now
get_data_from_scryfall()
create_default_collection()
create_default_deck()
build_database()
#create_ui()

#debug
'''
with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
    j = json.load(f)
'''