import json
import sqlite3
from modules.globals import DATABASE_INSERT_TO_MAIN
from modules.config import Config
from modules.database.database_functions import prepare_records_for_transaction, get_database_table_name
from modules.logging import console_log
from tqdm import tqdm

def database_load(connection: sqlite3.Connection) -> None:
    config = Config()
    
    with open(f"./{config.get_value('FOLDER', 'downloads')}/{config.get_value('BULK', 'data_type')}.json", 'r', encoding='utf8') as f:
        console_log('info', 'Alpha load started')
        data = json.load(f)
        console_log('info', 'Loaded .json file')

        transaction_main = []
        
        for card in tqdm(data):
            prepare_records_for_transaction(card, transaction_main)

        #Main
        column_names = ['id', *DATABASE_INSERT_TO_MAIN, 'sort_key']
        placeholders = ', '.join('?' * len(column_names))
        query = f"INSERT INTO {get_database_table_name()}({', '.join(column_names)}) VALUES ({placeholders})"

        #Exception for 'set' column name
        try: column_names[column_names.index('set')] = '"set"'
        except ValueError: pass

        cur = connection.cursor()
        cur.executemany(query, transaction_main)
        connection.commit()
        
        console_log('info', f'Alpha load done, added {len(data)} cards')

        #TODO
        #Delete all json files in downloads folder