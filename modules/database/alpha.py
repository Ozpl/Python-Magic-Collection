import json
from modules.consts import DATABASE_MAIN, DATABASE_SIDE, DATABASE_FREQUENT_UPDATING
from modules.database.database_functions import prepare_records_for_transaction, create_sort_key_string, checksum_of_a_record
from modules.logging import console_log
from tqdm import tqdm

def database_alpha_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        console_log('info', 'Alpha load started')
        data = json.load(f)
        console_log('info', 'Loaded .json file')

        transaction_main = []
        transaction_side = []
        
        for card in tqdm(data):
            prepare_records_for_transaction(card, transaction_main, transaction_side)

        #Main
        column_names = ['id', *DATABASE_MAIN, 'sort_key', 'checksum_card', 'checksum_frequent_updating']
        placeholders = ', '.join('?' * len(column_names))
        query = f"INSERT INTO main_table({', '.join(column_names)}) VALUES ({placeholders})"

        #Exception for 'set' column name
        try: column_names[column_names.index('set')] = '"set"'
        except ValueError: pass

        cur = connection.cursor()
        cur.executemany(query, transaction_main)
        connection.commit()

        #Side
        column_names = ['id', *DATABASE_SIDE]
        placeholders = ', '.join('?' * len(column_names))
        query = f"INSERT INTO side_table({', '.join(column_names)}) VALUES ({placeholders})"

        cur = connection.cursor()
        cur.executemany(query, transaction_side)
        connection.commit()
        
        console_log('info', f'Alpha load done, added {len(data)} cards')

        print()
