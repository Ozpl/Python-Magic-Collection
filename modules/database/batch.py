import json
from modules.database.database_functions import checksum_of_a_record, delete_card_from_db, query_get_id_and_checksum, add_card_to_db, update_frequent_updating, update_checksum_in_main, get_freqeunt_updating_dict
from modules.logging import console_log
from tqdm import tqdm

def batch_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        count = {
            'new': 0,
            'frequent': 0,
            'card': 0
        }

        console_log('info', 'Batch load started')
        database_checksum = query_get_id_and_checksum(connection, 'main')

        for card in tqdm(data):
            #add card if not in db
            if card['id'] not in database_checksum:
                add_card_to_db(connection, card)
                count['new'] = count['new'] + 1
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
                count['card'] = count['card'] + 1
            #check most freqeunt changes
            elif database_checksum[card['id']]['checksum_frequent_updating'] != current_frequent_updating_checksum:
                update_frequent_updating(connection, card, current_frequent_updating)
                update_checksum_in_main(connection, card['id'], 'checksum_frequent_updating', current_frequent_updating_checksum)
                count['frequent'] = count['frequent'] + 1
                
        console_log('info', f'''Batch load done
        -Cards added: {count['new']}
        -Cards with updated prices and ranks: {count['frequent']}
        -Cards that changed: {count['card']}
        -Cards without updates: {len(data) - count['new'] - count['frequent'] - count['card']}''')