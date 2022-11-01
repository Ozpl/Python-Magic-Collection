from os import path
from shutil import copyfileobj
from sqlite3 import Connection
from PyQt5.QtWidgets import QCheckBox, QComboBox, QLabel, QPlainTextEdit
from re import compile
from requests import get
from modules.database.collections import add_card_to_collection, create_collection, get_all_collections_names_as_array, get_card_from_collection
from modules.database.database_functions import create_sort_key_string, get_all_cards_from_pattern_as_joined_string, get_card_from_db, get_card_ids_list, get_database_table_name
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
def process_import_list(db_connection: Connection, col_connection: Connection, import_list: list, pattern: str, results_plaintextedit: QPlainTextEdit, errors_plaintextedit: QPlainTextEdit, header_checkbox: QCheckBox) -> None:
    console_log('INFO', 'Importing has started')
    
    results_plaintextedit.setPlainText('')
    unpacked_pattern = [*pattern.split(',')]
    
    patterned_cards = []
    cards_to_import = []
    
    if header_checkbox.isChecked():
        import_list = import_list[1:]
    for line in import_list:
        card_dict = {}
        card_list = split_line_to_list(line)
        for i, card in enumerate(card_list):
            card_dict[unpacked_pattern[i]] = card
        card_dict = handle_names_and_sets_exceptions(card_dict)
        patterned_cards.append(card_dict)
    
    console_log('INFO', 'Imported list processed, compiling database info')
    
    cards_to_import = get_unique_cards_to_import(patterned_cards)
    db_info = {
        'ids': get_card_ids_list(db_connection, f'SELECT id FROM {get_database_table_name()}'),
        'sort_keys': get_card_ids_list(db_connection, f'SELECT sort_key FROM {get_database_table_name()}'),
        '%s%c': get_all_cards_from_pattern_as_joined_string(db_connection, ['set_name', 'collector_number']),
        '%n%c': get_all_cards_from_pattern_as_joined_string(db_connection, ['name', 'collector_number']),
        '%n%s': get_all_cards_from_pattern_as_joined_string(db_connection, ['name', 'set_name'])
    }
    
    console_log('INFO', 'Database info compiled, searching cards in database')
    
    compiled_results = find_cards_in_db_and_compile_results(cards_to_import, db_info)
    
    console_log('INFO', 'Cards found, preparing transaction')
    
    transaction = []
    success_count = int(len(compiled_results['id']) - compiled_results['id'].count(''))
    results_string = ''
    errors_string = f"Successfully added {success_count} cards out of {len(compiled_results['id'])}, there are {len(compiled_results['id']) - success_count} errors.\n------------\n"
    
    for i in range(len(compiled_results['id'])):
        if compiled_results['id'][i] != '':
            transaction.append((compiled_results['id'][i], compiled_results['regular'][i], compiled_results['foil'][i], '', compiled_results['sort_key'][i]))
        else:
            errors_string = f"{errors_string}{compiled_results['line'][i]}\n"
        results_string = f"{results_string}{compiled_results['line'][i]}\n"
    
    results_plaintextedit.setPlainText(results_string)
    errors_plaintextedit.setPlainText(errors_string)

    console_log('INFO', 'Transaction prepared, commiting to collection.db')
    
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
def handle_names_and_sets_exceptions(split_card: dict) -> dict:
    names = [
        ' (Showcase)',
        ' (Borderless)' ,
        ' (Foil Etched)',
        ' (Showcase)',
        ' (Extended Art)',
        ' (Retro Frame)',
        ' (a)',
        ' (b)',
        ' (No PW Symbol)',
        ' (Dracula)',
        ' (Skyscraper)' ,
        ' (Gilded Foil)',
        ' (Thick Stock)',
        ' (Non-Foil)'
    ]
    sets = [
        ' Variants'
    ]

    #FIXME
    #Pattern is never matched, even though there are cards like 'Plains (79)' or 'Mountain (36)'
    pattern = r' \(\d+\)'
    re = compile(pattern)
    if re.match(split_card['%n']) is not None:
        re.sub(pattern, '', split_card['%n'])
    
    for element in names:
        if element in split_card['%n']:
            split_card['%n'] = split_card['%n'].replace(element, '')
    
    for element in sets:
        if element in split_card['%s']:
            split_card['%s'] = split_card['%s'].replace(element, '')
    
    return split_card
def get_unique_cards_to_import(patterned_cards: list) -> list:
    cards_to_import = []
    unique_names = []
    
    for card in patterned_cards:
        card_dict = {'name': '', '%s%c': '', '%n%c': '', '%n%s': '', 'regular': 0, 'foil': 0}
        name = f"{card['%n']} ({card['%c']}) [{card['%s']}]"
        if name in unique_names:
            index = [i for i in range(len(cards_to_import)) if cards_to_import[i]['name'] == name][0]
            if card['%f'].upper() == 'FALSE':
                cards_to_import[index]['regular'] += int(card['%q'])
            else:
                cards_to_import[index]['foil'] += int(card['%q'])
        else:
            unique_names.append(name)
            card_dict['name'] = name
            card_dict['%s%c'] = f"{card['%s']}{card['%c']}"
            card_dict['%n%c'] = f"{card['%n']}{card['%c']}"
            card_dict['%n%s'] = f"{card['%n']}{card['%s']}"
            if card['%f'].upper() == 'FALSE':
                card_dict['regular'] = int(card['%q'])
            else:
                card_dict['foil'] = int(card['%q'])
            cards_to_import.append(card_dict)
    
    return cards_to_import
def find_cards_in_db_and_compile_results(cards_to_import: list, db_info: dict) -> dict:
    compiled_results = {'name': [], 'id': [], 'regular': [], 'foil': [], 'sort_key': [], 'line': []}
    
    for card in cards_to_import:
        index = -1
        if find_card_by_search_pattern(card, db_info['%s%c'], '%s%c'):
            index = db_info['%s%c'].index(card['%s%c'])
            add_card_to_compiled_results(card, compiled_results, db_info['ids'][index], db_info['sort_keys'][index], 1)
        elif find_card_by_search_pattern(card, db_info['%n%c'], '%n%c'):
            index = db_info['%n%c'].index(card['%n%c'])
            add_card_to_compiled_results(card, compiled_results, db_info['ids'][index], db_info['sort_keys'][index], 2)
        elif find_card_by_search_pattern(card, db_info['%n%s'], '%n%s'):
            index = db_info['%n%s'].index(card['%n%s'])
            add_card_to_compiled_results(card, compiled_results, db_info['ids'][index], db_info['sort_keys'][index], 3)
        else:
            add_card_to_compiled_results(card, compiled_results, '', '', 0)
        
        if index > -1:
            for key in db_info:
                db_info[key].pop(index)
        
    return compiled_results
def find_card_by_search_pattern(card: dict, db_info_pattern: list, pattern: str) -> bool:
    if card[pattern] in db_info_pattern:
        return True
    else:
        return False
def add_card_to_compiled_results(card: dict, compiled_results: dict, id: str, sort_key: str, number_of_search: int) -> None:
    if number_of_search > 0:
        compiled_results['name'].append(card['name'])
        compiled_results['id'].append(id)
        compiled_results['regular'].append(card['regular'])
        compiled_results['foil'].append(card['foil'])
        compiled_results['sort_key'].append(sort_key)
        compiled_results['line'].append(f"Found in search #{number_of_search} - {card['name']}")
    else:
        compiled_results['name'].append(card['name'])
        compiled_results['id'].append('')
        compiled_results['regular'].append(0)
        compiled_results['foil'].append(0)
        compiled_results['sort_key'].append('')
        compiled_results['line'].append(f"NOT FOUND IN DB - {card['name']}")