import os
from datetime import datetime, timedelta
import configparser
from modules.consts import SETTINGS_FILE_STRUCTURE
from modules.config import Config
from modules.ui import create_user_interface
from modules.api import get_data_from_scryfall
from modules.collection import create_default_collection
from modules.deck import create_default_deck
from modules.database.create import create_main_table, create_sub_tables
from modules.database.alpha import alpha_load
from modules.database.batch import batch_load
from modules.database.functions import create_connection
from modules.logging import log

#Initiate configuration
if not os.path.exists(SETTINGS_FILE_STRUCTURE['config']):
    config = Config()
    config.create_default_config_file()
else:
    config = Config()
    config.load()

#Download new bulk_data if needed
get_data_from_scryfall()

#Refresh configuration
config.load()

#Manage cards database
database_connection = create_connection(SETTINGS_FILE_STRUCTURE['database'])
if config.get_boolean('FLAG', 'database_was_created'):
    create_main_table(database_connection)
    create_sub_tables(database_connection)
    alpha_load(database_connection)
if config.get_boolean('FLAG', 'downloaded_from_scryfall'):
    batch_load(database_connection)

#Manage collections database
collections_connection = create_connection(SETTINGS_FILE_STRUCTURE['collections'])
#create_default_collection()

#Manage decks database
decks_connection = create_connection(SETTINGS_FILE_STRUCTURE['decks'])
#create_default_deck()

#Build UI
create_user_interface(database_connection, collections_connection, decks_connection)

#Close all .db connections
database_connection.close()
collections_connection.close()
decks_connection.close()