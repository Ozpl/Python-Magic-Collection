import sqlite3
import json
import re
from modules.logging import console_log
from modules.consts import DATABASE_MAIN, DATABASE_SIDE

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

def get_column_names_and_types():
    with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
        j = json.load(f)
        names_and_types = {}
        for card in j:
            try:
                for key in card.keys():
                    if key not in names_and_types:
                        names_and_types[key] = assign_data_type(card[key])
                        if key == 'set':
                            names_and_types['"set"'] = names_and_types.pop('set')
            except KeyError:
                pass
        return names_and_types

def create_database_main_table(connection):
    console_log('info', 'Creating main_table in database')
    main_column_names_and_types = get_column_names_and_types()

    query = 'CREATE TABLE IF NOT EXISTS main_table (\nid TEXT NOT NULL PRIMARY KEY,'
    for element in main_column_names_and_types:
        if element == 'id':
            continue
        match main_column_names_and_types[element]:
            case 'string':
                query += f'\n{element} TEXT,'
                DATABASE_MAIN.append(element)
            case 'float':
                query += f'\n{element} FLOAT,'
                DATABASE_MAIN.append(element)
            case 'bool':
                query += f'\n{element} BOOL,'
                DATABASE_MAIN.append(element)
            case 'int':
                query += f'\n{element} INT,'
                DATABASE_MAIN.append(element)
            case 'datetime':
                query += f'\n{element} DATETIME,'
                DATABASE_MAIN.append(element)
            case 'list' | 'object':
                DATABASE_SIDE.append(element)

    query += '\nsort_key TEXT,\nchecksum_card BIGINT,\nchecksum_frequent_updating BIGINT\n)'

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_database_side_table(connection):
    query = 'CREATE TABLE IF NOT EXISTS side_table (db_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL,'

    for element in DATABASE_SIDE:
        query += f'\n{element} TEXT,'

    query = f"{query[:-1]})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()