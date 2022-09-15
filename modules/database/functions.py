import sqlite3
from sqlite3 import Error
import zlib
from datetime import datetime

def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except Error as e:
        print(e)

def checksum_of_record(card):
    checksum = 0
    for item in card.items():
        c1 = 1
        for t in item:
            c1 = zlib.adler32(bytes(repr(t), "utf-8"), c1)
        checksum = checksum ^ c1
    return checksum

def query_get_table_columns(connection, table_name):
    query = f'''
    SELECT * FROM {table_name}_table LIMIT 1
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def query_get_max_date(connection, table_name):
    query = f'''
    SELECT MAX(released_at) FROM {table_name}_table
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    max_date = cursor.fetchone()[0]
    return datetime.strptime(max_date, '%Y-%m-%d')

def query_get_card_from_db(connection, table_name, id):
    query = f'''
    SELECT * FROM {table_name}_table
    WHERE id = '{id}'
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()[0]
    return record

def query_get_id_and_checksum(connection, table_name):
    query = f'''
    SELECT id, checksum FROM {table_name}_table
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()
    return record

def query_delete_record(connection, table_name, id):
    query = f'''
    DELETE FROM {table_name}_table
    WHERE id = '{id}'
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def format_card_values(element):
    result = []
    for x in element:
        if isinstance(x, int):
            result.append(str(x))
        else:
            result.append(f"'{x}'")
    return result