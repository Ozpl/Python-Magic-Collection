import json
from modules.database.functions import checksum_of_a_record, query_get_id_and_checksum, add_card_to_db, update_prices, update_checksum_in_main
from datetime import datetime

def batch_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        
        print(f'Batch load started - {datetime.now()}')
        database_checksum = query_get_id_and_checksum(connection, 'main')

        for card in data:
            current_card_checksum = checksum_of_a_record(card)

            if card['id'] not in database_checksum:
                #card not in db, add to it
                add_card_to_db(connection, card)
                
            elif database_checksum[card['id']] != current_card_checksum:
                #card is in db, update it
                update_prices(connection, card)
                update_checksum_in_main(connection, card['id'], current_card_checksum)
                #TODO
                #If card changed in some other way than only price - how to update it efficiently
                #Get copy of a card and change 'None' to None in prices (x = dict(y))
                
        print(f'Batch load done - {datetime.now()}')