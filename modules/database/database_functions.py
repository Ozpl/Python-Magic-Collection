import sqlite3
from sqlite3 import Error
import zlib
from modules.consts import DATABASE_SUBTABLES_NAMES_EXCEPTIONS, DATABASE_SUBTABLES_NAMES_ARRAY, DATABASE_SUBTABLES_NAMES_OBJECT, DATABASE_FREQUENT_UPDATING

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
            
    frequent_updating = get_freqeunt_updating_dict(card)
    insert_to_main['checksum_card'] = checksum_of_a_record(card)
    insert_to_main['checksum_frequent_updating'] = checksum_of_a_record(frequent_updating)

    #main_table
    column_names = [*insert_to_main.keys()]
    try:
        column_names[column_names.index('set')] = '"set"'
    except ValueError:
        pass
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
            query_sub_table_all_parts(connection, card['id'], key, insert_to_sub_exceptions[key])
        elif key == 'card_faces':
            query_sub_table_card_faces(connection, card['id'], key, insert_to_sub_exceptions[key])

    for key in insert_to_sub_array.keys():
        query_sub_table_array(connection, card['id'], key, insert_to_sub_array[key])

    for key in insert_to_sub_object.keys():
        query_sub_table_object(connection, card['id'], key, insert_to_sub_object[key])

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
        unpacked_dict = [card_id]
        
        for element in face.keys():
            if 'color' not in element:
                unpacked_dict.append(face[element])
            else:
                value = str(face[element])
                unpacked_dict.append(value.replace("'", '').replace("[", '').replace("]", ''))

        #put image_uris from here to another subtable card_faces_image_uris
        for i, element in enumerate(column_names):
            if element == 'image_uris':
                query_sub_table_object(connection, card_id, 'card_faces_image_uris', unpacked_dict[i])
                del column_names[i]
                del unpacked_dict[i]

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

def query_get_id_and_checksum(connection, table_name):
    query = f'''
    SELECT id, checksum_card, checksum_frequent_updating FROM {table_name}_table
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()
    record_dict = {element[0].replace("'", ""): {'checksum_card': element[1], 'checksum_frequent_updating': element[2]} for element in record}
    return record_dict

def format_card_values(element):
    result = []
    for x in element:
        if isinstance(x, int):
            result.append(str(x))
        else:
            result.append(f'{x}')
    return result

def get_card_from_db(connection, card_id) -> dict:
    sub_tables_names = [*DATABASE_SUBTABLES_NAMES_EXCEPTIONS, 'card_faces_image_uris', *DATABASE_SUBTABLES_NAMES_ARRAY, *DATABASE_SUBTABLES_NAMES_OBJECT]

    query = f'''
        SELECT * FROM main_table
        WHERE id = '{card_id}'
        '''

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()

    card = {key: record[0][key] for key in record[0].keys() if 'checksum' not in key}

    for subtable in sub_tables_names:
            query = f'''
            SELECT * FROM {subtable}_table
            WHERE card_id = '{card_id}'
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            record = cursor.fetchall()

            if record:
                if subtable in DATABASE_SUBTABLES_NAMES_ARRAY:
                    card[subtable] = record[0]['array_value'].split(',')
                elif subtable == 'card_faces_image_uris':
                    for row in range(len(record)):
                        card['card_faces'][row]['image_uris'] = {}
                        for key in record[row].keys()[2:]:
                            card['card_faces'][row]['image_uris'][key] = record[row][key]
                else:
                    if len(record) > 1:
                        card[subtable] = []
                        for row in range(len(record)):
                            temp_object = {}
                            for key in record[row].keys()[2:]:
                                temp_object[key] = record[row][key]
                            card[subtable].append(temp_object)
                    else:
                        card[subtable] = {}
                        for key in record[0].keys()[2:]:
                            card[subtable][key] = record[0][key]

    return card

def get_card_from_db_to_add_cards(connection, card_id) -> dict:
    query = f'''
        SELECT * FROM main_table
        WHERE id = '{card_id}'
        '''

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()

    card = {key: record[0][key] for key in record[0].keys() if 'checksum' not in key}

    return card

def update_frequent_updating(connection, card, frequent_updating):
    for key in frequent_updating:
        if key == 'prices':
            query = f'''
                DELETE FROM {key}_table
                WHERE card_id = '{card['id']}'
                '''

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            query_sub_table_object(connection, card['id'], key, frequent_updating[key])
        else:
            query = f'''
            UPDATE main_table
            SET {key} = {frequent_updating[key]}
            WHERE id = '{card['id']}'
            '''

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

def update_checksum_in_main(connection, id, which_checksum, checksum_value):
    query = f'''
    UPDATE main_table
    SET {which_checksum} = {checksum_value}
    WHERE id = '{id}'
    '''

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def get_freqeunt_updating_dict(card):
    frequent_updating = {}
    for key in card:
        if key in DATABASE_FREQUENT_UPDATING:
            frequent_updating[key] = card[key]
    for key in DATABASE_FREQUENT_UPDATING:
        try:
            del card[key]
        except KeyError:
            pass
    return frequent_updating

def find_cards_in_db(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()

    card_ids = [element[0] for element in record]

    return card_ids