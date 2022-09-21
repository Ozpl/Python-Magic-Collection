import json
from modules.database.functions import checksum_of_a_record, query_get_id_and_checksum, add_card_to_db, delete_card_from_db

def batch_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        
        database_checksum = query_get_id_and_checksum(connection, 'main')

        for card in data:
            current_card_checksum = checksum_of_a_record(card)

            if card['id'] not in database_checksum:
                #card not in db, add to it
                add_card_to_db(connection, card)
                
            elif database_checksum[card['id']] != current_card_checksum:
                #card is in db, update it
                delete_card_from_db(connection, card)
                add_card_to_db(connection, card)



            #TODO
            #First, update only prices in prices_table if checksum is different and then check again to update everything else