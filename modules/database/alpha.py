import json
from modules.database.functions import checksum_of_record, query_get_table_columns, format_card_values

def alpha_load(connection):
    available_columns = query_get_table_columns(connection, 'main')

    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        insert_list = []
        insert_column_list = []

        for card in data[:20]:
            checksum = checksum_of_record(card)
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