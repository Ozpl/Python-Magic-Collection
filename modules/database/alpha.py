import json
from modules.database.functions import add_card_to_db

def alpha_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)

        for card in data:
            add_card_to_db(connection, card)