import sqlite3
import zlib
from modules.consts import DATABASE_MAIN, DATABASE_SIDE, DATABASE_SUBTABLES_NAMES_EXCEPTIONS, DATABASE_SUBTABLES_NAMES_ARRAY, DATABASE_SUBTABLES_NAMES_OBJECT, DATABASE_FREQUENT_UPDATING

def create_connection(db_path: str) -> sqlite3.Connection:
    '''Create connection to .db file via sqlite3 function from given path.'''
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except sqlite3.Error as e:
        print(e)

def prepare_records_for_transaction(card: dict, main: list, side: list) -> None:
    '''This function appends given list with tuples, each containing card's properties designated to be stored in main or side table.'''
    to_main = []
    to_side = []
    frequent_updating = {}
    
    #side_table
    to_side.append(card['id'])

    for element in DATABASE_SIDE:
        try: to_side.append(str(card[element]))
        except KeyError: to_side.append('')

    to_side = tuple(to_side)
    side.append(to_side)

    #main_table
    to_main.append(card['id'])

    for element in DATABASE_MAIN:
        try: to_main.append(card[element])
        except KeyError: to_main.append('')

    for element in DATABASE_FREQUENT_UPDATING:
        if element in card.keys():
            frequent_updating[element] = card[element]
            del card[element]

    sort_key = create_sort_key_string(card)
    to_main.append(sort_key)

    checksum_card = checksum_of_a_record(card)
    to_main.append(checksum_card)

    checksum_frequent_updating = checksum_of_a_record(frequent_updating)
    to_main.append(checksum_frequent_updating)

    to_main = tuple(to_main)
    main.append(to_main)

def checksum_of_a_record(card: dict) -> int:
    '''Given certain dict, return its unique checksum value.'''
    checksum = 0
    for item in card.items():
        c1 = 1
        for t in item:
            c1 = zlib.adler32(bytes(repr(t), "utf-8"), c1)
        checksum = checksum ^ c1
    return checksum

def sort_key_colors_mapping(array: list, color_map: dict) -> str:
    '''Helper function to sort_key generation, used for assigning numeral value to given color combination.'''
    found_colors = 0
    for element in color_map:
        for char in element:
            if char in array:
                found_colors = found_colors + 1
                if found_colors == len(array):
                    return color_map[element]
            else:
                found_colors = 0
                continue
    return '32'

def create_sort_key_string(card: dict) -> str:
    '''Create sort_key string, to properly sort cards in collection by its value.'''
    sort_key = ''
    
    try:
        color_map_one = { 'W': '01', 'U': '02', 'B': '03', 'R': '04', 'G': '05' }
        color_map_two = { 'WU': '06', 'WB': '07', 'UB': '08', 'UR': '09', 'BR': '10', 'BG': '11', 'RG': '12', 'WR': '13', 'WG': '14', 'UG': '15' }
        color_map_three = { 'WUB': '16', 'UBR': '17', 'BRG': '18', 'WRG': '19', 'WUG': '20', 'WBR': '21', 'URG': '22', 'WBG': '23', 'WBR': '24', 'UBG': '25' }
        color_map_four = { 'UBRG': '26', 'WBRG': '27', 'WURG': '28', 'WUBG': '29', 'WUBR': '30' }

        match (len(card['colors'])):
            case 1: sort_key += sort_key_colors_mapping(card['colors'], color_map_one)
            case 2: sort_key += sort_key_colors_mapping(card['colors'], color_map_two)
            case 3: sort_key += sort_key_colors_mapping(card['colors'], color_map_three)
            case 4: sort_key += sort_key_colors_mapping(card['colors'], color_map_four)
            case 5: sort_key += '31'
            case 0: sort_key += '32'
    except KeyError:
        sort_key += '32'

    try:
        cmc = str(int(card['cmc']))
        sort_key += cmc if len(cmc) > 1 else f'0{cmc}'
    except KeyError: sort_key += '0'

    try: sort_key += card['name'].lower().replace(' ', '')
    except KeyError: pass

    try: sort_key += card['released_at']
    except: pass
        
    return sort_key

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
                    card[subtable] = record[0]['array_value'].split(', ')
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

def find_cards_in_db(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()

    card_ids = [element[0] for element in record]

    return card_ids