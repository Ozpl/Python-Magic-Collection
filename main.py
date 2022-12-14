from os import path
from modules.api import get_data_from_scryfall
from modules.globals import config
from modules.database.collections import create_collections_list, create_collection
from modules.database.create import create_database_table
from modules.database.functions import create_connection, close_all_connections
from modules.database.load import database_load
from modules.ui import create_user_interface

#Initiate configuration
if not path.exists('config.ini'): config.create_default_config_file()
config.build_folder_structure()
config.build_file_structure()
    
#Download new bulk_data if needed
get_data_from_scryfall()

#Manage cards database
database_connection = create_connection(config.get('FILE', 'database'))
if config.get_boolean('FLAG', 'database_was_created') or config.get_boolean('FLAG', 'downloaded_from_scryfall'):
    create_database_table(database_connection)
    database_load(database_connection)

#Manage collections database
collections_connection = create_connection(config.get('FILE', 'collections'))
if config.get_boolean('FLAG', 'collections_was_created'):
    create_collections_list(collections_connection)
    create_collection(collections_connection, 'Main collection')
    config.set('COLLECTION', 'current_collection', 'maincollection')

#Manage decks database
decks_connection = create_connection(config.get('FILE', 'decks'))
#if config.get_boolean('FLAG', 'decks_was_created'):
    #create_deck()

#Build UI
create_user_interface(database_connection, collections_connection, decks_connection)

#Close all .db connections
close_all_connections(database_connection, collections_connection, decks_connection)
