import json
from modules.database.functions import checksum_of_record, query_get_table_columns, format_card_values
from modules.consts import DATABASE_SUBTABLES_NAMES_EXCEPTIONS, DATABASE_SUBTABLES_NAMES_ARRAY, DATABASE_SUBTABLES_NAMES_OBJECT

def alpha_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)

        for card in data:
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
            insert_to_main['checksum'] = checksum_of_record(card)

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