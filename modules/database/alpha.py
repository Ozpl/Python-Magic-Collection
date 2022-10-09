import json
from modules.database.database_functions import add_card_to_db
from modules.logging import console_log
from tqdm import tqdm

def database_alpha_load(connection):
    with open('./downloads/Default Cards.json', 'r', encoding='utf8') as f:
        data = json.load(f)

        console_log('info', 'Alpha load started')
        for card in tqdm(data):
            add_card_to_db(connection, card)
        console_log('info', f'Alpha load done, added {len(data)} cards')