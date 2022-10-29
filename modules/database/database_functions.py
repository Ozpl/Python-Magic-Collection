from ast import literal_eval
from sqlite3 import connect, Connection, Error
from modules.globals import config, DATABASE_INSERT_TO_MAIN, IMPORT_PATTERN_MAP

def create_connection(db_path: str) -> Connection:
    '''Create connection to .db file via sqlite3 function from given path.'''
    connection = None
    try:
        connection = connect(db_path)
        return connection
    except Error as e:
        print(e)

def close_all_connections(*connections: Connection) -> None:
    for connection in connections:
        connection.close()

def prepare_records_for_load_transaction(card: dict, main: list) -> None:
    '''This function appends given list with tuples, each containing card's properties to be inserted into database.'''
    to_main = []

    #main_table
    to_main.append(card['id'])

    for element in DATABASE_INSERT_TO_MAIN:
        try:
            if element == '"set"':
                to_main.append(card['set'])
            else:
                if isinstance(card[element], list) or isinstance(card[element], object):
                    to_main.append(str(card[element]))
                else:
                    to_main.append(card[element])
        except KeyError:
            to_main.append(None)

    sort_key = create_sort_key_string(card)
    to_main.append(sort_key)

    to_main = tuple(to_main)
    main.append(to_main)

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
            case 1: sort_key = sort_key_colors_mapping(card['colors'], color_map_one)
            case 2: sort_key = sort_key_colors_mapping(card['colors'], color_map_two)
            case 3: sort_key = sort_key_colors_mapping(card['colors'], color_map_three)
            case 4: sort_key = sort_key_colors_mapping(card['colors'], color_map_four)
            case 5: sort_key = '31'
            case 0: sort_key = '32'
        if 'Land' in card['type_line']: sort_key = '33'
    except KeyError:
        sort_key = '34'

    try:
        cmc = str(int(card['cmc']))
        sort_key += cmc if len(cmc) > 1 else f'0{cmc}'
    except KeyError: sort_key += '99'

    try: sort_key += card['name'].lower().replace(' ', '')
    except KeyError: pass

    try: sort_key += card['released_at']
    except: pass
        
    return sort_key

def query_get_table_columns(connection: Connection, table_name: str):
    query = f'''
    SELECT * FROM {table_name} LIMIT 1
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def format_card_values(element: list) -> list:
    result = []
    for x in element:
        if isinstance(x, int):
            result.append(str(x))
        elif x is None:
            result.append(None)
        else:
            result.append(f'{x}')
    return result

def get_database_table_name() -> str:
    return config.get('BULK', 'data_type').replace(' ', '_').lower()

def get_card_from_db(connection: Connection, card_id: str) -> dict:
    query = f'''
        SELECT * FROM {get_database_table_name()}
        WHERE id = '{card_id}'
        '''

    column_names = query_get_table_columns(connection, get_database_table_name())

    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchone()

    card = {column_names[i]: element for i, element in enumerate(record)}

    for key in card.keys():
        if card[key]:
            if isinstance(card[key], str):
                if card[key][0] in ["{", "["] and card[key][1] in "'":
                    card[key] = literal_eval(card[key])

    return card

def get_card_ids_list(connection: Connection, query: str) -> list:
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()

    card_ids = [element[0] for element in record]

    return card_ids

def get_all_cards_from_pattern_as_joined_string(connection: Connection, pattern: list) -> list:    
    
    query = f"SELECT {', '.join(pattern)} FROM {get_database_table_name()}"
    
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    
    results = []
    
    for record in records:
        s = ''
        for element in record:
            s = s + element
        results.append(s)
        
    return results

def get_all_cards_from_pattern_map(connection: Connection, pattern: list) -> list:
    column_names = [IMPORT_PATTERN_MAP[element] for element in pattern]
    
    query = f"SELECT id, {', '.join(column_names)}, sort_key FROM {get_database_table_name()}"
    
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()