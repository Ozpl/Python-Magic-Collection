import json
from modules.database.functions import checksum_of_a_record, delete_card_from_db, query_get_id_and_checksum, add_card_to_db, update_frequent_updating, update_checksum_in_main, get_freqeunt_updating_dict
from modules.consts import DATABASE_FREQUENT_UPDATING
from datetime import datetime

def batch_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        count_new = 0
        count_updated_frequent_updating = 0
        count_updated_card = 0
        count_up_to_date = 0

        print(f'Batch load started - {datetime.now()}')
        database_checksum = query_get_id_and_checksum(connection, 'main')

        for card in data:
            #add card if not in db
            if card['id'] not in database_checksum:
                add_card_to_db(connection, card)
                count_new = count_new + 1
                continue

            current_frequent_updating = get_freqeunt_updating_dict(card)
            current_frequent_updating_checksum = checksum_of_a_record(current_frequent_updating)
            current_card_checksum = checksum_of_a_record(card)

            #check all other changes
            if database_checksum[card['id']]['checksum_card'] != current_card_checksum:
                delete_card_from_db(connection, card)
                add_card_to_db(connection, card)
                update_frequent_updating(connection, card, current_frequent_updating)
                update_checksum_in_main(connection, card['id'], 'checksum_frequent_updating', current_frequent_updating_checksum)
                count_updated_card = count_updated_card + 1
            #check most freqeunt changes
            elif database_checksum[card['id']]['checksum_frequent_updating'] != current_frequent_updating_checksum:
                update_frequent_updating(connection, card, current_frequent_updating)
                update_checksum_in_main(connection, card['id'], 'checksum_frequent_updating', current_frequent_updating_checksum)
                count_updated_frequent_updating = count_updated_frequent_updating + 1
            #no changes
            else:
                count_up_to_date = count_up_to_date + 1
                
        print(f'''Batch load done - {datetime.now()}
        Cards added: {count_new}
        Cards with updated prices and ranks: {count_updated_frequent_updating}
        Cards that changed: {count_updated_card}
        Cards without updates: {count_up_to_date}
        ''')