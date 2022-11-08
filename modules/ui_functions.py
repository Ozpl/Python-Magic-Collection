from sqlite3 import Connection
from typing import Any
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt5.QtWidgets import QCheckBox, QComboBox, QDoubleSpinBox, QGroupBox, QLabel, QPlainTextEdit
from modules.globals import config

#Global functions
def download_image_if_not_downloaded(connection: Connection, id: str, image_extension: str) -> None:
    from ast import literal_eval
    from os import path
    from shutil import copyfileobj
    from requests import get
    from modules.database.functions import get_card_from_db
    
    file_name = f"{config.get('FOLDER', 'cards')}/{id}.{image_extension}"

    if not path.exists(file_name):
        card = get_card_from_db(connection, id)
        
        if card['image_uris']:
            image_uris = card['image_uris']
        elif card['card_faces']:
            image_uris = literal_eval(card['card_faces'])[0]['image_uris']
            
        r = get(image_uris[config.get('COLLECTION', 'image_type')], stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(file_name,'wb') as f:
                copyfileobj(r.raw, f)
def split_line_to_list(card: str) -> list:
    last_index = 0
    opened_quatation = False
    split_card = []
    
    for i, char in enumerate(card):
        if char == '"':
            opened_quatation = False if opened_quatation else True
            
        if not opened_quatation and char == ',':
            if card[last_index:i][0] == '"' and card[last_index:i][-1] == '"':
                split_card.append(card[last_index+1:i-1])
            else:
                split_card.append(card[last_index:i])
            last_index = i + 1
    split_card.append(card[last_index:])
    return split_card

#Corner widget
def refresh_collection_names_in_corner(connection: Connection, combo_box: QComboBox, current_collection: str) -> None:
    from modules.database.collections import format_collection_name, get_all_collections_names_as_array
    
    config.set('FLAG', 'corner_refreshing', 'true')
    combo_box.clear()
    items = get_all_collections_names_as_array(connection)
    items_formatted = [format_collection_name(element) for element in items]
    combo_box.addItems(items)
    if current_collection in items_formatted:
        if items_formatted.index(current_collection) == 0 and combo_box.count() > 1:
            combo_box.setCurrentIndex(1)
        combo_box.setCurrentIndex(items_formatted.index(current_collection))
    config.set('FLAG', 'corner_refreshing', 'false')

#Collection
def calculate_grid_sizes(grid_widget: QGroupBox) -> dict:
    from math import floor
    
    current_grid_size = grid_widget.geometry().size()

    card_width = 215
    card_height = int(card_width * 1.39)

    cards_in_row = floor(current_grid_size.width() / card_width)
    cards_in_row = 8 if cards_in_row > 8 else cards_in_row
    cards_in_row = 3 if cards_in_row < 3 else cards_in_row

    cards_in_col = floor(current_grid_size.height() / card_height)
    cards_in_col = 4 if cards_in_col > 4 else cards_in_col
    cards_in_col = 2 if cards_in_col < 2 else cards_in_col
    
    cards_on_grid = cards_in_row * cards_in_col

    grid_width = current_grid_size.width()
    margin_horizontal = 20 * 2
    total_cards_width = cards_in_row * card_width
    horizontal_space_left = grid_width - total_cards_width - margin_horizontal
    number_of_horizontal_spacings = (cards_in_row - 1)
    spacing_horizontal = horizontal_space_left / number_of_horizontal_spacings

    #info labels are 15px high
    grid_height = current_grid_size.height()
    margin_vertical = 15 * 2 + 20
    total_cards_height = cards_in_col * card_height
    vertical_space_left = grid_height - total_cards_height - margin_vertical
    number_of_vertical_spacings = (cards_in_col - 1)
    spacing_vertical = vertical_space_left / number_of_vertical_spacings
    
    result = {
        'cards_on_grid': cards_on_grid,
        'card_width': card_width,
        'card_height': card_height,
        'cards_in_row': cards_in_row,
        'cards_in_col': cards_in_col,
        'spacing_horizontal': spacing_horizontal,
        'spacing_vertical': spacing_vertical
    }
    
    return result
def delete_widgets_from_layout(layout: Any) -> None:
    for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
def prepare_list_of_cards_to_show(filtered_cards: list, database_cards: dict, collection_cards: dict) -> list:
    cards_to_display = []
    
    if filtered_cards:
        if config.get_boolean('COLLECTION', 'show_database'):
            cards_to_display = filtered_cards
        else:
            for element in filtered_cards:
                if element in collection_cards['id']:
                    cards_to_display.append(element)
    elif config.get_boolean('COLLECTION', 'show_database'):
        cards_to_display = database_cards['id']
    else:
        cards_to_display = collection_cards['id']
        
    return cards_to_display
def set_maximum_number_of_pages_and_update_info(cards_to_display: list, cards_on_grid: int, page_control_widget: QDoubleSpinBox, info_widget: QLabel) -> None:
    if len(cards_to_display) == 0: page_control_widget.setMaximum(1)
    elif len(cards_to_display) % cards_on_grid == 0: page_control_widget.setMaximum(len(cards_to_display) / cards_on_grid)
    else: page_control_widget.setMaximum(len(cards_to_display) / cards_on_grid + 1)
    
    info_widget.setText(f'Found {len(cards_to_display)} cards and there are {int(page_control_widget.maximum())} pages.')
def download_card_images_for_current_page(connection: Connection, cards_to_display: list, start: int, end: int, image_extension: str) -> None:
    from ast import literal_eval
    from modules.database.functions import get_card_from_db
    
    for card in cards_to_display[start:end]:
        card_db = get_card_from_db(connection, card)
        if card_db['image_uris']:
            [download_image_if_not_downloaded(connection, card_db['id'], image_extension) for element in card_db['image_uris'] if element == config.get('COLLECTION', 'image_type')]
        elif card_db['card_faces']:
            card_faces = literal_eval(card_db['card_faces'])
            [download_image_if_not_downloaded(connection, card_db['id'], image_extension) for element in card_faces[0]['image_uris'] if element == config.get('COLLECTION', 'image_type')]
def create_price_string(card: str, database_cards: dict) -> str:
    price_string = ''
    
    db_index = database_cards['id'].index(card)
    
    if database_cards['prices_regular'][db_index] is not None: price_string += f"{database_cards['prices_regular'][db_index]}"
    else: price_string += 'N/A'
    
    price_string += ' / '
    
    if database_cards['prices_foil'][db_index] is not None: price_string += f"{database_cards['prices_foil'][db_index]}"
    else: price_string += 'N/A'
    
    return price_string
def create_currency_string(price_str: str) -> str:
    currency_symbol = ''
    if price_str:
        if config.get('COLLECTION', 'price_currency') == 'eur': currency_symbol = '€'
        elif config.get('COLLECTION', 'price_currency') == 'usd': currency_symbol = '$'
        else: currency_symbol += f" {config.get('COLLECTION', 'price_currency').upper()}"
    return currency_symbol
def create_card_image(card_image: QLabel, card: str, image_extension: str, card_width: int, card_height: int) -> None:
    card_image.setObjectName('image')
    card_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
    card_image.setStyleSheet("background-color: gainsboro; margin:5px")
    
    pixmap = QPixmap(f"{config.get('FOLDER', 'cards')}/{card}.{image_extension}")
    pixmap_scaled = pixmap.scaled(card_width, card_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    card_image.setPixmap(pixmap_scaled)
def create_card_info(card_info: QLabel, in_collection: bool, collection_cards: dict, card: str, price_string: str, currency_symbol: str) -> None:
    card_info.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    
    crd_idx = collection_cards['id'].index(card)
    card_info_text = ''
    price_slash = price_string.index(' / ')
    regular = collection_cards['regular'][crd_idx]
    foil = collection_cards['foil'][crd_idx]
    
    if in_collection:
        if regular is not None and regular > 0 and foil is not None and foil > 0:
            card_info_text += f"{regular + foil} ({regular}/{foil}) - {price_string}{currency_symbol}"
        elif regular is not None and regular > 0:
            card_info_text += f"{regular} (regular) - {price_string[0:price_slash]}{currency_symbol}"
        elif foil is not None and foil > 0:
            card_info_text += f"{foil} (foil) - {price_string[price_slash+2:]}{currency_symbol}"
    else:
        card_info_text = f"Not collected - {price_string}{currency_symbol}"
    
    card_info.setText(card_info_text)
def create_card_extra_info(card_extra_info: QLabel) -> None:
    card_extra_info.setText('Extra info')
    card_extra_info.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

#Add cards tab
def update_card_count_in_add_cards(connection: Connection, found_cards: list, current_row: int, label: QLabel) -> None:
    from modules.database.collections import get_card_from_collection
    selected_card = get_card_from_collection(connection, config.get('COLLECTION', 'current_collection'), found_cards[current_row])

    label.setText(f"You currently have {selected_card['regular']} regulars and {selected_card['foil']} foils in collection")
def add_card_to_collection_in_add_cards(db_connection: Connection, cl_connection: Connection, found_cards: list, sorted_list: list, current_row: int, regular: int, foil: int, mode: str) -> None:
    from modules.database.collections import add_card_to_collection
    from modules.database.functions import create_sort_key_string, get_card_from_db
    
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
    from modules.database.collections import create_collection
    from modules.database.functions import get_all_cards_from_pattern_as_joined_string, get_card_ids_list, get_database_table_name
    from modules.logging import console_log
    
    
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
    
    #TODO
    #Refresh collection list in corner
    
    console_log('INFO', f'Transaction completed, created new collection "{collection_name}"')
def handle_names_and_sets_exceptions(split_card: dict) -> dict:
    import re
    
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
    
    full_pattern = r'.* \(\d+\)'
    parenthesis = r' \(\d+\)'
    regex = re.compile(full_pattern)
    if regex.match(split_card['%n']) is not None:
        split_card['%n'] = re.sub(parenthesis, '', split_card['%n'])
    
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
