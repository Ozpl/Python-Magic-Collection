from os import path
from shutil import copyfileobj
from sqlite3 import Connection
from PyQt5.QtWidgets import QCheckBox, QComboBox, QLabel, QPlainTextEdit
from requests import get
from modules.database.collections import add_card_to_collection, create_collection, get_all_collections_names_as_array, get_card_from_collection
from modules.database.database_functions import create_sort_key_string, get_all_cards_from_pattern_as_joined_string, get_all_cards_from_pattern_map, get_card_from_db, get_card_ids_list, get_database_table_name
from modules.logging import console_log
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
def add_card_to_collection_in_add_cards(db_connection: Connection, cl_connection: Connection, found_cards: list, sorted_list: list, current_row: int, regular: int, foil: int, mode: str) -> None:
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
def process_import_list(db_connection: Connection, col_connection: Connection, import_list: list, pattern: str, results_plaintextedit: QPlainTextEdit, header_checkbox: QCheckBox) -> None:
    console_log('INFO', 'Importing has started')
    results_plaintextedit.setPlainText('')
    results = {'ids': [], 'quantities': [], 'lines': [], 'sort_keys': []}
    
    db_cards_ids = get_card_ids_list(db_connection, f'SELECT id FROM {get_database_table_name()}')
    db_cards_sort_keys = get_card_ids_list(db_connection, f'SELECT sort_key FROM {get_database_table_name()}')
    
    db_cards_sc = get_all_cards_from_pattern_as_joined_string(db_connection, ['set_name', 'collector_number'])
    db_cards_nc = get_all_cards_from_pattern_as_joined_string(db_connection, ['name', 'collector_number'])
    db_cards_ns = get_all_cards_from_pattern_as_joined_string(db_connection, ['name', 'set_name'])
    db_cards = [db_cards_sc, db_cards_nc, db_cards_ns]
    
    console_log('INFO', 'Compiled all combinations of cards\' joined strings, reading imported list')
    
    cards_to_import = []
    unpacked_pattern = [*pattern.split(',')]
    
    if header_checkbox.isChecked():
        import_list = import_list[1:]
    
    for line in import_list:
        card_dict = {}
        card_list = split_line_to_list(line)
        for i, card_name in enumerate(card_list):
            card_dict[unpacked_pattern[i]] = card_name
        cards_to_import.append(card_dict)
        
    quantities = get_card_quantities_and_remove_duplicates(cards_to_import)
    cards_to_add = len(cards_to_import)        
    
    import_cards_search_sc = [f"{element['%s']}{element['%c']}" for element in cards_to_import]
    import_cards_search_nc = [f"{element['%n']}{element['%c']}" for element in cards_to_import]
    import_cards_search_ns = [f"{element['%n']}{element['%s']}" for element in cards_to_import]
    import_cards_searches = [import_cards_search_sc, import_cards_search_nc, import_cards_search_ns]
    
    console_log('INFO', 'Imported list processed, preparing transaction')
    
    card_ids = get_card_results(import_cards_searches, db_cards, cards_to_import, db_cards_ids, quantities, db_cards_sort_keys)
    results['ids'] =  card_ids['ids']
    results['lines'] = card_ids['lines']
    results['quantities'] = card_ids['quantities']
    results['sort_keys'] = card_ids['sort_keys']
    
    transaction = []
    for i in range(len(results['ids'])):
        card = []
        card.append(results['ids'][i])
        card.append(results['quantities'][i]['regular'])
        card.append(results['quantities'][i]['foil'])
        card.append('')
        card.append(results['sort_keys'][i])
        transaction.append(tuple(card))
        
    results_plaintextedit_string = f"Successfully added {len(results['ids'])} cards out of {cards_to_add}, scroll to the bottom to see errors.\n------------\n"
    for i in range(len(results['lines'])):
        results_plaintextedit_string = f"{results_plaintextedit_string}{results['lines'][i]}\n"
    
    results_plaintextedit.setPlainText(results_plaintextedit_string)
        
    console_log('INFO', 'Transation prepared, commiting to collection.db')
    
    column_names = ['id', 'regular', 'foil', 'tags', 'sort_key']
    placeholders = ', '.join('?' * len(column_names))
    
    #DEBUG
    collection_name = 'Imported collection'
    collection_name_formatted = 'importedcollection'
    create_collection(col_connection, collection_name)
    
    query = f"INSERT OR REPLACE INTO {collection_name_formatted}({', '.join(column_names)}) VALUES ({placeholders})"
    
    cur = col_connection.cursor()
    cur.executemany(query, transaction)
    col_connection.commit()
    
    console_log('INFO', f'Transaction completed, created new collection "{collection_name}"')
        
def split_line_to_list(card: str) -> list:
    last_index = 0
    opened_quatation = False
    split_card = []
    
    for i, char in enumerate(card):
        if char == '"':
            opened_quatation = False if opened_quatation else True
            
        if not opened_quatation and char == ',':
            if card[last_index:i].startswith('"') and card[last_index:i].endswith('"'):
                split_card.append(card[last_index+1:i-1])
            else:
                split_card.append(card[last_index:i])
            last_index = i + 1
    split_card.append(card[last_index:])
    
    return split_card

def get_card_quantities_and_remove_duplicates(cards_to_import: list) -> list:
    unique_cards_names = []
    unique_cards_quantity = []
    duplicate_indexes = []
    for i, card in enumerate(cards_to_import):
        name = f"{card['%n']}{card['%s']}{card['%c']}"
        
        if name in unique_cards_names:
            if card['%f'].upper() == 'TRUE': unique_cards_quantity[unique_cards_names.index(name)]['foil'] += int(card['%q'])
            else: unique_cards_quantity[unique_cards_names.index(name)]['regular'] += int(card['%q'])
            duplicate_indexes.append(i)
        else:
            unique_cards_names.append(name)
            quantities = {'regular': 0, 'foil': 0}
            
            if card['%f'].upper() == 'TRUE': quantities['foil'] = int(card['%q'])
            else: quantities['regular'] = int(card['%q'])
            
            unique_cards_quantity.append(quantities)
    
    duplicate_indexes.sort()
    duplicate_indexes.reverse()
    for element in duplicate_indexes:
        cards_to_import.pop(element)
    
    return unique_cards_quantity 

def get_card_results(all_imports: list, all_db: list, cards_to_import: list, db_ids: list, cards_quantities: list, db_cards_sort_keys: list) -> dict:
    result_lines = []
    result_ids = []
    result_quantities = []
    result_sort_keys = []
    
    for i in range(len(all_imports)):
        cards_indexes_found_in_db = []
        cards_indexes_found_in_import = []
        for j, card_name in enumerate(all_imports[i]):
            if card_name in all_db[i]:
                cards_indexes_found_in_db.append(all_db[i].index(card_name))
                cards_indexes_found_in_import.append(j)
                result_ids.append(db_ids[cards_indexes_found_in_db[j]])
                result_quantities.append(cards_quantities[cards_indexes_found_in_import[j]])
                result_sort_keys.append(db_cards_sort_keys[cards_indexes_found_in_db[j]])
                result_lines.append(f"Card found during search #{i+1} - {cards_to_import[j]['%n']} ({cards_to_import[j]['%c']}) [{cards_to_import[j]['%s']}]")
            else:
                cards_indexes_found_in_db.append(None)
                cards_indexes_found_in_import.append(None)
                result_lines.append(f"Card NOT found during search #{i+1} - {cards_to_import[j]['%n']} ({cards_to_import[j]['%c']}) [{cards_to_import[j]['%s']}]")
        
        while None in cards_indexes_found_in_db:
            cards_indexes_found_in_db.remove(None)
        cards_indexes_found_in_db.sort()
        cards_indexes_found_in_db.reverse()
        for index in cards_indexes_found_in_db:
            db_ids.pop(index)
            [element.pop(index) for element in all_db]
            
        while None in cards_indexes_found_in_import:
            cards_indexes_found_in_import.remove(None)
        cards_indexes_found_in_import.sort()
        cards_indexes_found_in_import.reverse()
        for index in cards_indexes_found_in_import:
            cards_to_import.pop(index)
            cards_quantities.pop(index)
            [element.pop(index) for element in all_imports]

    return {'ids': result_ids, 'lines': result_lines, 'quantities': result_quantities, 'sort_keys': result_sort_keys}