from os import path
from shutil import copyfileobj
from sqlite3 import Connection
from PyQt5.QtWidgets import QComboBox, QLabel, QPlainTextEdit
from requests import get
from modules.database.collections import add_card_to_collection, get_all_collections_names_as_array, get_card_from_collection
from modules.database.database_functions import create_sort_key_string, get_all_cards_from_pattern, get_card_from_db
from modules.database.query import construct_query
from modules.globals import config
from tqdm import tqdm

#Global functions
def download_image_if_not_downloaded(connection: Connection, id: str, image_extension: str) -> None:
    file_name = f"{config.get('FOLDER', 'cards')}/{id}.{image_extension}"

    if not path.exists(file_name):
        card = get_card_from_db(connection, id)
        if card['image_uris']:
            image_uris = card['image_uris']
        else:
            #FIXME Handle card_faces and lack of image_uris
            return
        r = get(image_uris[config.get('COLLECTION', 'image_type')], stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(file_name,'wb') as f:
                copyfileobj(r.raw, f)

#Corner widget
def refresh_collection_names_in_corner(connection: Connection, combo_box: QComboBox) -> None:
    combo_box.clear()
    combo_box.addItems(get_all_collections_names_as_array(connection))

#Add cards tab
def update_card_count_in_add_cards(connection: Connection, found_cards: list, current_row: int, label: QLabel) -> None:
    selected_card = get_card_from_collection(connection, config.get('COLLECTION', 'current_collection'), found_cards[current_row])

    label.setText(f"You currently have {selected_card['regular']} regulars and {selected_card['foil']} foils in collection")
def add_card_to_collection_in_add_cards(db_connection: Connection, cl_connection: Connection, found_cards: list, sorted_list: list, current_row: int, regular: int, foil: int, mode: str):
    add_card_to_collection(
        cl_connection,
        config.get('COLLECTION', 'current_collection'), 
        found_cards[current_row],
        regular,
        foil,
        mode,
        create_sort_key_string(get_card_from_db(db_connection, sorted_list[current_row]['id']))
        )

#Import/export tab
def process_import_list(connection: Connection, import_list: list, pattern: str, results_plain_edit_text: QPlainTextEdit):
    results_plain_edit_text.setPlainText('')
    cards_to_import = []
    unpacked_pattern = [*pattern.split(',')]

    for card in import_list:
        last_index = 0
        pattern_index = 0
        opened_quatation = False
        card_info = {}

        for i, char in enumerate(card):
            if char == '"':
                opened_quatation = False if opened_quatation else True
            if not opened_quatation and char == ',':
                if card[last_index:i].startswith('"') and card[last_index:i].endswith('"'):
                    card_info[unpacked_pattern[pattern_index]] = card[last_index+1:i-1]
                else:
                    card_info[unpacked_pattern[pattern_index]] = card[last_index:i]
                last_index = i + 1
                pattern_index = pattern_index + 1
            card_info[unpacked_pattern[pattern_index]] = card[last_index:]
        cards_to_import.append(card_info)
        
    all_cards = get_all_cards_from_pattern(connection, ['%s', '%c'])
    stored_ids = []
    
    for to_import in cards_to_import:
        for card in all_cards:
            if to_import['%s'] == card[1] and to_import['%c'] == card[2]:
                stored_ids.append(card[0])
                break
    
    transcation = []
    for i, to_import in enumerate(cards_to_import):
        #TODO
        #Add sort_key at last position
        if eval(to_import['%f'].capitalize()):
            transcation.append((stored_ids[i], 0, to_import['%q'], None, None))
        else:
            transcation.append((stored_ids[i], to_import['%q'], 0, None, None))
            
    #TODO
    #Insert into collection if there's no such id, if there is - set only one value
    print(transcation)
    
    
    
    '''
    if records:
        for i, record in enumerate(records):
            card = cards_to_import[i]
            if len(record) == 0:
                result = result + f"0 cards with given criteria found - {card['%n']} ({card['%c']}) [{card['%s']}]\n"
            elif len(record) == 1:
                result = result + f"Success - {card['%n']} ({card['%c']}) [{card['%s']}]\n"
            else:
                result = result + f"Found more than one - ({len(record)}) card with given criteria - {card['%n']} ({card['%c']}) [{card['%s']}]\n"
                
    results_plain_edit_text.setPlainText(f'{result}')
    '''