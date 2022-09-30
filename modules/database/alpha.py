import json
from modules.database.functions import add_card_to_db
from modules.logging import log
from tqdm import tqdm

def alpha_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)

        log('info', 'Alpha load started')
        for card in tqdm(data):
            add_card_to_db(connection, card)
        log('info', f'Alpha load done, added {len(data)} cards')