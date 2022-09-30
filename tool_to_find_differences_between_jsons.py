import json
from modules.database.functions import checksum_of_a_record, get_freqeunt_updating_dict

dict_cards = {}
dict_check_cards = {}
dict_check_prices = {}
how_much = 5

def go_through_cards(file_number):

    with open(f'./downloads/Default Cards {file_number}.json', 'r', encoding='utf8') as f:
        data = json.load(f)

        for card in data[:how_much]:
            if card['id'] not in dict_cards:
                dict_cards[card['id']] = []
            if card['id'] not in dict_check_cards:
                dict_check_cards[card['id']] = []
            if card['id'] not in dict_check_prices:
                dict_check_prices[card['id']] = []

            current_frequent_updating = get_freqeunt_updating_dict(card)
            current_frequent_updating_checksum = checksum_of_a_record(current_frequent_updating)
            current_card_checksum = checksum_of_a_record(card)

            dict_check_cards[card['id']].append(current_card_checksum)
            dict_check_prices[card['id']].append(current_frequent_updating_checksum)
            dict_cards[card['id']].append(card)

go_through_cards('28')
go_through_cards('29')
go_through_cards('30')

for id in dict_cards:
        for card in dict_cards[id]:
            print(card)

print('Done')