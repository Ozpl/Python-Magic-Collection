import json
from modules.database.functions import checksum_of_record, query_get_table_columns, format_card_values
from modules.consts import DATABASE_SUBTABLES_NAMES_EXCEPTIONS, DATABASE_SUBTABLES_NAMES_ARRAY, DATABASE_SUBTABLES_NAMES_OBJECT

def alpha_load(connection):
    available_columns = query_get_table_columns(connection, 'main')

    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        insert_list = []
        insert_column_list = []
        cards_sub_tables = {}

        for card in data[:20]:
            checksum = checksum_of_record(card)
            cards_sub_tables[card['id']] = {'checksum': checksum}
            found_atr = []
            found_col = []
            keys_list = card.keys()
            for key in keys_list:
                if key in available_columns:
                    found_atr.append(card[key])
                    found_col.append(key)
                else:
                    cards_sub_tables[card['id']][key] = card[key]
            found_col.append('checksum')
            found_atr.append(checksum)
            insert_list.append(found_atr)
            insert_column_list.append(found_col)
    
    for i, element in enumerate(insert_list):
        #EXCEPTION Escape characters for 'set'
        set_element_index = insert_column_list[i].index('set')
        insert_column_list[i][set_element_index] = '"set"'

        placeholders = ', '.join('?' * len(insert_column_list[i]))
        query = f'''
        INSERT INTO main_table({', '.join(insert_column_list[i])}) VALUES ({placeholders})
        '''

        cursor = connection.cursor()
        cursor.execute(query, format_card_values(element))
        connection.commit()

    for element in cards_sub_tables.keys():
        for sub_table_name in cards_sub_tables[element].keys():
            value = cards_sub_tables[element][sub_table_name]
            if sub_table_name in DATABASE_SUBTABLES_NAMES_EXCEPTIONS:
                pass
            elif sub_table_name in DATABASE_SUBTABLES_NAMES_ARRAY:
                query_sub_table_array(connection, element, sub_table_name, value)
            elif sub_table_name in DATABASE_SUBTABLES_NAMES_OBJECT:
                query_sub_table_object(connection, element, sub_table_name, value)
        pass

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