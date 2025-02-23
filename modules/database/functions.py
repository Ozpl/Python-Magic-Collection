from sqlite3 import connect, Connection, Error
from modules.globals import config, DATABASE_INSERT_TO_MAIN

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
    sort_key_colors = create_sort_key_string(card, 'colors')
    to_main.append(sort_key_colors)
    sort_key_produced_mana = create_sort_key_string(card, 'produced_mana')
    to_main.append(sort_key_produced_mana)
    sort_key_cmc = create_sort_key_string(card, 'cmc')
    to_main.append(sort_key_cmc)
    sort_key_name = create_sort_key_string(card, 'name')
    to_main.append(sort_key_name)
    sort_key_released_at = create_sort_key_string(card, 'released_at')
    to_main.append(sort_key_released_at)
    sort_key_price = create_sort_key_string(card, 'price')
    to_main.append(sort_key_price)

    to_main = tuple(to_main)
    main.append(to_main)

def sort_key_colors_mapping(array: list, color_map: dict) -> str:
    '''Helper function to sort_key generation, used for assigning numeral value to given color combination.'''
    for element in color_map:
        found_colors = 0
        for char in element:
            if char in array:
                found_colors = found_colors + 1
                if found_colors == len(array):
                    return color_map[element]
            else:
                found_colors = 0
                continue
    return '35'

def create_sort_key_string(card: dict, attribute: str) -> str:
    '''Create sort_key string, to properly sort cards in collection by its value.'''
    sort_key = ''
    
    color_map_one = { 'W': '01', 'U': '02', 'B': '03', 'R': '04', 'G': '05' }
    color_map_two = { 'WU': '06', 'WB': '07', 'UB': '08', 'UR': '09', 'BR': '10', 'BG': '11', 'RG': '12', 'WR': '13', 'WG': '14', 'UG': '15' }
    color_map_three = { 'WUB': '16', 'UBR': '17', 'BRG': '18', 'WRG': '19', 'WUG': '20', 'WBR': '21', 'URG': '22', 'WBG': '23', 'WUR': '24', 'UBG': '25' }
    color_map_four = { 'UBRG': '26', 'WBRG': '27', 'WURG': '28', 'WUBG': '29', 'WUBR': '30' }
    
    if attribute == 'colors':
        colors_flag = False
        #Colors for double cards
        try:
            colors = []
            if card['card_faces']:
                if card['card_faces'][0]['colors']:
                    for color in card['card_faces'][0]['colors']:
                        colors.append(color)
                colors = list(set(colors))
                
            match (len(colors)):
                case 1: sort_key = sort_key_colors_mapping(colors, color_map_one)
                case 2: sort_key = sort_key_colors_mapping(colors, color_map_two)
                case 3: sort_key = sort_key_colors_mapping(colors, color_map_three)
                case 4: sort_key = sort_key_colors_mapping(colors, color_map_four)
                case 5: sort_key = '31'
                case 0: sort_key = '32'
            if 'Basic' in card['type_line']: sort_key = '33'
            elif 'Land' in card['type_line']: sort_key = '34'
            elif 'Token' in card['type_line']: sort_key = '35'
            colors_flag = True
        except KeyError:
            sort_key = '36'
            
        #Colors
        if not colors_flag:
            try:
                colors = card['colors']
                match (len(colors)):
                    case 1: sort_key = sort_key_colors_mapping(colors, color_map_one)
                    case 2: sort_key = sort_key_colors_mapping(colors, color_map_two)
                    case 3: sort_key = sort_key_colors_mapping(colors, color_map_three)
                    case 4: sort_key = sort_key_colors_mapping(colors, color_map_four)
                    case 5: sort_key = '31'
                    case 0: sort_key = '32'
                if 'Basic' in card['type_line']: sort_key = '33'
                elif 'Land' in card['type_line']: sort_key = '34'
                elif 'Token' in card['type_line']: sort_key = '35'
            except KeyError:
                sort_key = '36'
    elif attribute == 'produced_mana':
        #Mana produced
        #FIXME
        #Land can produce C as a color and can also produce nothing and have None as a type
        try:
            '''
            if 'Evolving Wilds' in card['name']:
                print()
            '''
            produced_mana = card['produced_mana']
            
            if 'Land' not in card['type_line']:
                sort_key = '00'
            else:
                match (len(produced_mana)):
                    case 1: sort_key = sort_key_colors_mapping(produced_mana, color_map_one)
                    case 2: sort_key = sort_key_colors_mapping(produced_mana, color_map_two)
                    case 3: sort_key = sort_key_colors_mapping(produced_mana, color_map_three)
                    case 4: sort_key = sort_key_colors_mapping(produced_mana, color_map_four)
                    case 5: sort_key = '31'
                    case 0: sort_key = '32'
        except KeyError:
            sort_key = '00'
    elif attribute == 'cmc':
    #CMC
        try:
            cmc = str(int(card['cmc']))
            sort_key = cmc if len(cmc) > 1 else f'0{cmc}'
        except KeyError: sort_key = '99'
    elif attribute == 'name':
        #Name
        try: sort_key = card['name'].lower().replace(' ', '')
        except KeyError: pass
    elif attribute == 'released_at':
        #Date
        try: sort_key = card['released_at']
        except: pass
    elif attribute == 'price':
        #TODO
        sort_key = '000000'
        
    return sort_key

def get_combined_sort_keys_from_db(connection: Connection) -> list:
    from modules.globals import SORTING_ATTRIBUTES
    
    sort_keys = []    
    sort_key_string = ''
    for attribute in SORTING_ATTRIBUTES:
        sort_key_string += f"sort_key_{attribute}, "
    sort_key_string = sort_key_string[:-2]
    
    query = f'''
        SELECT {sort_key_string} FROM {get_database_table_name()}
        '''
        
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    
    for record in records:
        sort_key = ''
        for element in record:
            sort_key += element
        sort_keys.append(sort_key)
        
    return sort_keys

def get_combined_card_sort_key(connection: Connection, id: str) -> str:
    from modules.globals import SORTING_ATTRIBUTES
    
    sort_key_string = ''
    for attribute in SORTING_ATTRIBUTES:
        sort_key_string += f"sort_key_{attribute}, "
    sort_key_string = sort_key_string[:-2]
    
    query = f'''
        SELECT {sort_key_string} FROM {get_database_table_name()}
        WHERE id = "{id}"
        '''
        
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchone()
    
    sort_key = ''
    for element in record:
        sort_key += element
        
    return sort_key

def query_get_table_columns(connection: Connection, table_name: str) -> list:
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
    from ast import literal_eval
    
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

def get_cards_ids_prices_sets_flip_list(connection: Connection, price_source: str) -> list:
    from ast import literal_eval
    from modules.globals import SORTING_ATTRIBUTES
    from forex_python.converter import CurrencyRates, RatesNotAvailableError
    
    currency_rates = CurrencyRates()
    currency = config.get('COLLECTION', 'price_currency')
    try: exchange_rate = currency_rates.get_rate('USD', currency.upper())
    except RatesNotAvailableError: exchange_rate = 1
    except ValueError: exchange_rate = 1

    query = f'''SELECT id, prices, "set", card_faces FROM {get_database_table_name()} ORDER BY '''
    for attribute in SORTING_ATTRIBUTES: query += f'sort_key_{attribute}, '
    query = query[:-2]
    
    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchall()

    price_currency = config.get('COLLECTION', 'price_currency')
    cards = {'id': [], 'prices_regular': [], 'prices_foil': [], 'set': [], 'flip': []}
    
    cards['id'] = [element[0] for element in record]
    
    for element in record:
        prices = literal_eval(element[1])
        if price_source == 'eur':
            cards['prices_regular'].append(prices['eur'])
            cards['prices_foil'].append(prices['eur_foil'])
        elif price_source == 'tix':
            cards['prices_regular'].append(prices['tix'])
            cards['prices_foil'].append(None)
        else:
            if prices['usd_etched']:
                if prices['usd']:
                    cards['prices_regular'].append(prices['usd'])
                else:
                    cards['prices_regular'].append(None)
                cards['prices_foil'].append(prices['usd_etched'])
            else:
                cards['prices_regular'].append(prices['usd'])
                cards['prices_foil'].append(prices['usd_foil'])
            
        if price_currency not in ['usd', 'eur', 'tix']:
            if cards['prices_regular'][-1] is not None:
                cards['prices_regular'][-1] = str(round(float(cards['prices_regular'][-1]) * exchange_rate, 2))
                if cards['prices_regular'][-1].index('.') == len(cards['prices_regular'][-1])-2: cards['prices_regular'][-1] = cards['prices_regular'][-1] + '0'
            if cards['prices_foil'][-1] is not None:
                cards['prices_foil'][-1] = str(round(float(cards['prices_foil'][-1]) * exchange_rate, 2))
                if cards['prices_foil'][-1].index('.') == len(cards['prices_foil'][-1])-2: cards['prices_foil'][-1] = cards['prices_foil'][-1] + '0'
    
    cards['set'] = [element[2] for element in record]
    
    for element in record:
        if element[3]:
            card_faces = literal_eval(element[3])
            if card_faces[0].get('image_uris'):
                cards['flip'].append(True)
            else: cards['flip'].append(False)
        else: cards['flip'].append(False)
    
    return cards

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
