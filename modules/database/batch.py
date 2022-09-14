import json
from datetime import datetime, timedelta
from modules.database.functions import checksum_of_record, query_get_table_columns, query_get_max_date, query_get_id_and_checksum, query_delete_record

def batch_load(connection):
    available_columns = query_get_table_columns(connection, 'main')
    
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        insert_list = []
        insert_column_list = []
        max_date = query_get_max_date(connection, 'main')

        id_and_checksum = query_get_id_and_checksum(connection, 'main')

        for card in data[:5]:
            current_date = datetime.strptime(card['released_at'], '%Y-%m-%d')
            #if date is newer then insert to db
            if (max_date - current_date) < timedelta(0):
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
            else:
                json_id = card['id']
                json_checksum = checksum_of_record(card)

                database_checksum = [element[1] for element in id_and_checksum if json_id == element[0]][0]
                if json_checksum != database_checksum:
                    query_delete_record(connection, 'main', json_id)
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
            #if id match
            ##check checksum
            ##if different then update record
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