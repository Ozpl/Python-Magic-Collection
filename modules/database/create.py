import sqlite3
import json
import re
from modules.logging import console_log
from modules.consts import DATABASE_SUBTABLES_NAMES_EXCEPTIONS, DATABASE_SUBTABLES_NAMES_ARRAY, DATABASE_SUBTABLES_NAMES_OBJECT

def assign_data_type(element):
    data_type = ''

    if isinstance(element, list):
        data_type = 'list'
    elif isinstance(element, bool):
        data_type = 'bool'
    elif isinstance(element, float):
        data_type = 'float'
    elif isinstance(element, str):
        data_type = 'string'
    elif isinstance(element, int):
        data_type = 'int'
    elif isinstance(element, object):
        data_type = 'object'

    #Exception for null in value
    if element is None:
        data_type = 'string'

    #Exception for datetime values
    if isinstance(element, str):
        r = re.compile('\d\d\d\d-\d\d-\d\d')
        if r.match(element) is not None:
            data_type = 'datetime'

    return data_type

def get_column_names_and_types(case):
    with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
        j = json.load(f)
        names_and_types = {}
        for card in j:
            try:
                if case == 'main':
                    for key in card.keys():
                        if key not in names_and_types:
                            names_and_types[key] = assign_data_type(card[key])
                            if key == 'set':
                                names_and_types['"set"'] = names_and_types.pop('set')

                elif case == 'all_parts' or case == 'card_faces':
                    for element in card[case]:
                        for key in element.keys():
                            if key not in names_and_types:
                                names_and_types[key] = assign_data_type(element[key])
                                
                elif case == 'card_faces_image_uris':
                    for face in card['card_faces']:
                        for key in face['image_uris'].keys():
                            if key not in names_and_types:
                                names_and_types[key] = assign_data_type(key)
                                
                else:
                    for key in card[case].keys():
                        if key not in names_and_types:
                            names_and_types[key] = assign_data_type(card[case][key])
            except KeyError:
                pass
        return names_and_types

def parse_subtable_query(subtable, column_names_and_types):
    query = ''

    query = f'CREATE TABLE IF NOT EXISTS {subtable}_table (\ndb_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\ncard_id VARCHAR(255) NOT NULL,'
    for element in column_names_and_types:
        match column_names_and_types[element]:
            case 'string' | 'list':
                query += f'\n{element} VARCHAR(255),'
            case 'float':
                query += f'\n{element} FLOAT,'
            case 'bool':
                query += f'\n{element} BOOL,'
            case 'int':
                query += f'\n{element} INT,'
            case 'datetime':
                query += f'\n{element} DATETIME,'
    query = query[:-1] + '\n)'

    return query

def create_main_table(connection):
    main_column_names_and_types = get_column_names_and_types('main')
    DATABASE_SUBTABLES_NAMES_EXCEPTIONS = []
    DATABASE_SUBTABLES_NAMES_ARRAY = []
    DATABASE_SUBTABLES_NAMES_OBJECT = []

    console_log('info', 'Creating main_table in database')

    query = 'CREATE TABLE IF NOT EXISTS main_table (\nid VARCHAR(255) NOT NULL PRIMARY KEY,'
    for element in main_column_names_and_types:
        if element == 'id':
            continue
        elif element == 'all_parts':
            DATABASE_SUBTABLES_NAMES_EXCEPTIONS.append(element)
            continue
        elif element == 'card_faces':
            DATABASE_SUBTABLES_NAMES_EXCEPTIONS.append(element)
            DATABASE_SUBTABLES_NAMES_EXCEPTIONS.append('card_faces_image_uris')
            continue

        match main_column_names_and_types[element]:
            case 'string':
                query += f'\n{element} VARCHAR(255),'
            case 'float':
                query += f'\n{element} FLOAT,'
            case 'bool':
                query += f'\n{element} BOOL,'
            case 'int':
                query += f'\n{element} INT,'
            case 'datetime':
                query += f'\n{element} DATETIME,'
            case 'list':
                DATABASE_SUBTABLES_NAMES_ARRAY.append(element)
            case 'object':
                DATABASE_SUBTABLES_NAMES_OBJECT.append(element)

    #TODO
    #Add new column named sort_key and fill with "card['cmc']card['name'].lower()""
    query += '\nchecksum_card BIGINT,\nchecksum_frequent_updating BIGINT\n)'

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_sub_tables(connection):
    console_log('info', 'Creating subtables')
    for element in DATABASE_SUBTABLES_NAMES_EXCEPTIONS:
        create_subt_exceptions(connection, element)
    for element in DATABASE_SUBTABLES_NAMES_ARRAY:
        create_subt_array(connection, element)
    for element in DATABASE_SUBTABLES_NAMES_OBJECT:
        create_subt_object(connection, element)

def create_subt_exceptions(connection, subtable):
    if subtable == 'all_parts':
        column_names_and_types = get_column_names_and_types('all_parts')

    elif subtable == 'card_faces':
        column_names_and_types = get_column_names_and_types('card_faces')
        column_names_and_types.pop('image_uris')
        
    elif subtable == 'card_faces_image_uris':
        column_names_and_types = get_column_names_and_types('card_faces_image_uris')
    
    query = parse_subtable_query(subtable, column_names_and_types)

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_subt_array(connection, subtable):
    column_names_and_types = {'array_value': 'string'}
    
    query = parse_subtable_query(subtable, column_names_and_types)
    
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_subt_object(connection, subtable):
    column_names_and_types = get_column_names_and_types(subtable)

    query = parse_subtable_query(subtable, column_names_and_types)

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()