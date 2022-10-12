from json import load
from os import path, listdir, remove
from sqlite3 import Connection
from tqdm import tqdm
from modules.globals import DATABASE_INSERT_TO_MAIN
from modules.globals import config
from modules.database.database_functions import get_database_table_name, prepare_records_for_transaction
from modules.logging import console_log

def database_load(connection: Connection) -> None:    
    with open(f"./{config.get('FOLDER', 'downloads')}/{config.get('BULK', 'data_type')}.json", 'r', encoding='utf8') as f:
        console_log('info', 'Alpha load started')
        data = load(f)
        console_log('info', 'Successfully loaded .json file')

        transaction = []
        
        for card in tqdm(data):
            prepare_records_for_transaction(card, transaction)

        #Main
        column_names = ['id', *DATABASE_INSERT_TO_MAIN, 'sort_key']
        placeholders = ', '.join('?' * len(column_names))
        query = f"INSERT OR REPLACE INTO {get_database_table_name()}({', '.join(column_names)}) VALUES ({placeholders})"

        #Exception for 'set' column name
        try: column_names[column_names.index('set')] = '"set"'
        except ValueError: pass

        cur = connection.cursor()
        cur.executemany(query, transaction)
        connection.commit()

        console_log('info', f'Alpha load done, added {len(data)} cards')

    for file in listdir(config.get('FOLDER', 'downloads')):
        f = path.join(config.get('FOLDER', 'downloads'), file)
        if path.isfile(f):
            remove(f)