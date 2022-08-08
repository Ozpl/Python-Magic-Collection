import sqlite3
import os
import json
from sqlite3 import Error

SETTINGS_FILE_PATH = './settings.json'
DATABASE_PATH = './database/database.db'

def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except Error as e:
        print(e)

def get_table_columns(connection, table_name):
    query = f'''
    SELECT * FROM {table_name}_table LIMIT 1
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def main_table_insert(connection):
    available_columns = get_table_columns(connection, 'main')
    #placeholders = ', '.join('?' * len(available_columns))

    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        insert_list = []
        insert_column_list = []

        for card in data:
            found_atr = []
            found_col = []
            keys_list = card.keys()
            for key in keys_list:
                if key in available_columns:
                    found_atr.append(card[key])
                    found_col.append(key)
            insert_list.append(found_atr)
            insert_column_list.append(found_col)
    
    for i, element in enumerate(insert_list):
        result_string = ''
        for x in element:
            if isinstance(x, int):
                result_string = result_string + str(x)
            else:
                result_string = result_string + f"'{x}'"
            result_string = result_string + ', '
        result_string = result_string[:-2]
        #print(f'Columns: {len(available_columns)} and element: {len(element)}')

        query = f'''
        INSERT INTO main_table({', '.join(insert_column_list[i])}) VALUES ({result_string})
        '''
        
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

connection = create_connection(DATABASE_PATH)
main_table_insert(connection)
connection.close()