import json
from modules.database.functions import checksum_of_record, query_get_table_columns

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
        result_string = ''
        for x in element:
            if isinstance(x, int):
                result_string = result_string + str(x)
            else:
                result_string = result_string + f"'{x}'"
            result_string = result_string + ', '
        result_string = result_string[:-2]

        query = f'''
        INSERT INTO main_table({', '.join(insert_column_list[i])}) VALUES ({result_string})
        '''
        
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()