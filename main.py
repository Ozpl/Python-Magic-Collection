import os
from modules.consts import SETTINGS_FILE_STRUCTURE
from modules.config import Config
from modules.ui import create_user_interface
from modules.api import get_data_from_scryfall
from modules.database.create import create_database_main_table, create_database_side_table
from modules.database.alpha import database_alpha_load
from modules.database.batch import database_batch_load
from modules.database.database_functions import create_connection
from modules.database.collections import create_collections_main_table, create_collection

#TODO
#Setup different databases for cards for different bulk_data types (i.e 'Default Cards', 'Oracle')

#Initiate configuration
config = Config()
if not os.path.exists(SETTINGS_FILE_STRUCTURE['config']): config.create_default_config_file()
config.build_folder_structure()
config.build_file_structure()

#Download new bulk_data if needed
get_data_from_scryfall()

#Manage cards database
database_connection = create_connection(SETTINGS_FILE_STRUCTURE['database'])
if config.get_boolean('FLAG', 'database_was_created'):
    create_database_main_table(database_connection)
    create_database_side_table(database_connection)
    database_alpha_load(database_connection)
if config.get_boolean('FLAG', 'downloaded_from_scryfall'):
    database_batch_load(database_connection)

#Manage collections database
collections_connection = create_connection(SETTINGS_FILE_STRUCTURE['collections'])
if config.get_boolean('FLAG', 'collections_was_created'):
    create_collections_main_table(collections_connection)
    create_collection(collections_connection, 'Main collection')

#Manage decks database
decks_connection = create_connection(SETTINGS_FILE_STRUCTURE['decks'])
#if config.get_boolean('FLAG', 'decks_was_created'):
    #create_deck()

#Build UI
create_user_interface(database_connection, collections_connection, decks_connection)

#Close all .db connections
database_connection.close()
collections_connection.close()
decks_connection.close()