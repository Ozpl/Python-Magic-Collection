from sqlite3 import OperationalError
from modules.logging import console_log
from modules.database.functions import query_get_table_columns, format_card_values
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
                tags VARCHAR(255))
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