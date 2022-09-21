import sqlite3
from sqlite3 import Error
import zlib
from datetime import datetime
from modules.consts import DATABASE_SUBTABLES_NAMES_EXCEPTIONS, DATABASE_SUBTABLES_NAMES_ARRAY, DATABASE_SUBTABLES_NAMES_OBJECT

def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except Error as e:
        print(e)

def checksum_of_a_record(card):
    checksum = 0
    for item in card.items():
        c1 = 1
        for t in item:
            c1 = zlib.adler32(bytes(repr(t), "utf-8"), c1)
        checksum = checksum ^ c1
    return checksum

def add_card_to_db(connection, card):
    insert_to_main = {}
    insert_to_sub_exceptions = {}
    insert_to_sub_array = {}
    insert_to_sub_object = {}

    for key in card:
        if key in DATABASE_SUBTABLES_NAMES_EXCEPTIONS:
            insert_to_sub_exceptions[key] = card[key]
        elif key in DATABASE_SUBTABLES_NAMES_ARRAY:
            insert_to_sub_array[key] = card[key]
        elif key in DATABASE_SUBTABLES_NAMES_OBJECT:
            insert_to_sub_object[key] = card[key]
        else:
            insert_to_main[key] = card[key]
    insert_to_main['checksum'] = checksum_of_a_record(card)

    #main_table
    column_names = [*insert_to_main.keys()]
    column_names[column_names.index('set')] = '"set"'
    unpacked_dict = [*[insert_to_main[element] for element in insert_to_main.keys()]]
    
    placeholders = ', '.join('?' * len(column_names))
    query = f'''
    INSERT INTO main_table({', '.join(column_names)}) VALUES ({placeholders})
    '''

    cursor = connection.cursor()
    cursor.execute(query, format_card_values(unpacked_dict))
    connection.commit()

    #sub_tables
    for key in insert_to_sub_exceptions.keys():
        if key == 'all_parts':
            query_sub_table_all_parts(connection, card['id'], key, card[key])
        elif key == 'card_faces':
            query_sub_table_card_faces(connection, card['id'], key, card[key])

    for key in insert_to_sub_array.keys():
        query_sub_table_array(connection, card['id'], key, card[key])

    for key in insert_to_sub_object.keys():
        query_sub_table_object(connection, card['id'], key, card[key])

def query_sub_table_all_parts(connection, card_id, sub_table_name, value):
    column_names = query_get_table_columns(connection, sub_table_name)[1:]
    
    for element in value:
        placeholders = ', '.join('?' * len(column_names))
        query = f'''
        INSERT INTO {sub_table_name}_table({', '.join(column_names)}) VALUES ({placeholders})
        '''

        cursor = connection.cursor()
        cursor.execute(query, [card_id, *[element[x] for x in element.keys()]])
        connection.commit()

def query_sub_table_card_faces(connection, card_id, sub_table_name, value):
    for face in value:
        column_names = ['card_id', *face.keys()]
        unpacked_dict = [card_id, *[face[element] for element in face.keys()]]

        '''
        #delete image_uris
        for i, x in enumerate(column_names):
            if x == 'image_uris':
                del column_names[i]
                del unpacked_dict[i]
        '''

        placeholders = ', '.join('?' * len(column_names))
        query = f'''
        INSERT INTO {sub_table_name}_table({', '.join(column_names)}) VALUES ({placeholders})
        '''

        cursor = connection.cursor()
        cursor.execute(query, format_card_values(unpacked_dict))
        connection.commit()

def query_sub_table_array(connection, card_id, sub_table_name, value):
    column_names = query_get_table_columns(connection, sub_table_name)[1:]

    placeholders = ', '.join('?' * len(column_names))
    query = f'''
    INSERT INTO {sub_table_name}_table({', '.join(column_names)}) VALUES ({placeholders})
    '''

    cursor = connection.cursor()
    cursor.execute(query, [card_id, ','.join(format_card_values(value))])
    connection.commit()

def query_sub_table_object(connection, card_id, sub_table_name, value):
    column_names = ['card_id', *value.keys()]
    unpacked_dict = [card_id, *[value[element] for element in value.keys()]]

    placeholders = ', '.join('?' * len(column_names))
    query = f'''
    INSERT INTO {sub_table_name}_table({', '.join(column_names)}) VALUES ({placeholders})
    '''

    cursor = connection.cursor()
    cursor.execute(query, format_card_values(unpacked_dict))
    connection.commit()

def delete_card_from_db(connection, card):
    sub_tables_names = [*DATABASE_SUBTABLES_NAMES_EXCEPTIONS, *DATABASE_SUBTABLES_NAMES_ARRAY, *DATABASE_SUBTABLES_NAMES_OBJECT]

    #main
    query = f'''
    DELETE FROM main_table
    WHERE id = '{card['id']}'
    '''

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    
    #sub tables
    for element in sub_tables_names:
        try:
            _check_if_key_exists = card[element]
            query = f'''
            DELETE FROM {element}_table
            WHERE card_id = '{card['id']}'
            '''

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except KeyError:
            pass

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
    record_dict = {element[0].replace("'", ""): element[1] for element in record}
    return record_dict

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
            result.append(f"{x}")
    return result