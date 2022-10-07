from sqlite3 import OperationalError
from modules.logging import console_log
from modules.database.database_functions import query_get_table_columns, format_card_values
import string

def create_collections_main_table(connection):
    query = '''CREATE TABLE IF NOT EXISTS main_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        formatted_name VARCHAR(255))
        '''

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_collection(connection, name):
    try:
        whitelist = string.ascii_letters + string.digits
        formatted_name = ''
        for char in name.lower():
            if char in whitelist:
                formatted_name += char
        column_names = query_get_table_columns(connection, 'main')[1:]

        console_log('info', f'Creating {formatted_name}_table as collections subtable')

        placeholders = ', '.join('?' * len(column_names))
        query = f'''
        INSERT INTO main_table({', '.join(column_names)}) VALUES ({placeholders})
        '''

        cursor = connection.cursor()
        cursor.execute(query, format_card_values([name, formatted_name]))
        connection.commit()
        
        query = f'''
        CREATE TABLE IF NOT EXISTS {formatted_name}_table (
                card_id VARCHAR(255) NOT NULL PRIMARY KEY,
                regular INT,
                foil INT,
                tags VARCHAR(255),
                sort_key VARCHAR(255))
                '''
                
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except OperationalError:
        console_log('error', f'Failed to create "{name}" collection')

def get_all_collections_names_as_array(connection):
    query = "SELECT name FROM main_table"
                
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    record = cursor.fetchall()
    
    collection_names = [element[0] for element in record]

    collection_names.sort()

    return collection_names

def get_card_ids_from_collection(connection, collection):
    query = f"SELECT card_id FROM {collection}_table"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    record = cursor.fetchall()

    card_ids = [element[0] for element in record]
    card_ids.sort()

    return card_ids

def get_card_from_collection(connection, collection, id):
    query = f"SELECT * FROM {collection}_table WHERE card_id = '{id}'"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    record = cursor.fetchone()

    card = {'card_id': id, 'regular': 0, 'foil': 0, 'tags': '', 'sort_key': ''}

    if record:
        return {'card_id': record[0], 'regular': record[1], 'foil': record[2], 'tags': record[3], 'sort_key': record[4]}
    else:
        return card

def add_card_to_collection(connection, collection, id, regular, foil, operation, sort_key):
    column = 'regular' if regular > 0 else 'foil'
    query = f"SELECT {column} FROM {collection}_table WHERE card_id = '{id}'"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    record = cursor.fetchone()

    if record:
        record = record[0]
        if operation == 'add':
            new_value = record + regular + foil
        elif operation == 'set':
            new_value = regular + foil

        query = f'''            
            UPDATE {collection}_table
            SET {column} = {new_value}
            WHERE card_id = '{id}'
            '''
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    else:
        column_names = query_get_table_columns(connection, collection)
        placeholders = ', '.join('?' * len(column_names))
        query = f'''
        INSERT INTO {collection}_table({', '.join(column_names)}) VALUES ({placeholders})
        '''

        cursor = connection.cursor()
        cursor.execute(query, format_card_values([id, regular, foil, '', sort_key]))
        connection.commit()