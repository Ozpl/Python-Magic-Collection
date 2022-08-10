import sqlite3
import zlib
import json
from sqlite3 import Error
from modules.consts import DATABASE_PATH
from datetime import datetime, timedelta

def check_sum(card):
    checksum = 0
    for item in card.items():
        c1 = 1
        for t in item:
            c1 = zlib.adler32(bytes(repr(t), "utf-8"), c1)
        checksum = checksum ^ c1
    return checksum

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

def get_max_date(connection, table_name):
    query = f'''
    SELECT MAX(released_at) FROM {table_name}_table
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    max_date = cursor.fetchone()[0]
    return datetime.strptime(max_date, '%Y-%m-%d')

def get_card_from_db(connection, table_name, id):
    query = f'''
    SELECT * FROM {table_name}_table
    WHERE id = '{id}'
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()[0]
    return record

def get_id_and_checksum(connection, table_name):
    query = f'''
    SELECT id, checksum FROM {table_name}_table
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()
    return record


def delete_record(connection, table_name, id):
    query = f'''
    DELETE FROM {table_name}_table
    WHERE id = '{id}'
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def batch_load(connection):
    available_columns = get_table_columns(connection, 'main')
    
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        insert_list = []
        insert_column_list = []
        max_date = get_max_date(connection, 'main')

        id_and_checksum = get_id_and_checksum(connection, 'main')

        for card in data[:5]:
            current_date = datetime.strptime(card['released_at'], '%Y-%m-%d')
            #if date is newer then insert to db
            if (max_date - current_date) < timedelta(0):
                checksum = check_sum(card)
                found_atr = []
                found_col = []
                keys_list = card.keys()
                for key in keys_list:
                    if key in available_columns:
                        found_atr.append(card[key])
                        found_col.append(key)
                found_col.append('checksum')
                found_atr.append(checksum)
                insert_list.append(found_atr)
                insert_column_list.append(found_col)
            else:
                json_id = card['id']
                json_checksum = check_sum(card)

                database_checksum = [element[1] for element in id_and_checksum if json_id == element[0]][0]
                if json_checksum != database_checksum:
                    delete_record(connection, 'main', json_id)
                    checksum = check_sum(card)
                    found_atr = []
                    found_col = []
                    keys_list = card.keys()
                    for key in keys_list:
                        if key in available_columns:
                            found_atr.append(card[key])
                            found_col.append(key)
                    found_col.append('checksum')
                    found_atr.append(checksum)
                    insert_list.append(found_atr)
                    insert_column_list.append(found_col)
            #if id match
            ##check checksum
            ##if different then update record
    for i, element in enumerate(insert_list):
        result_string = ''
        for x in element:
            if isinstance(x, int):
                result_string = result_string + str(x)
            else:
                result_string = result_string + f"'{x}'"
            result_string = result_string + ', '
        result_string = result_string[:-2]

        query = f'''
        INSERT INTO main_table({', '.join(insert_column_list[i])}) VALUES ({result_string})
        '''
        
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
            