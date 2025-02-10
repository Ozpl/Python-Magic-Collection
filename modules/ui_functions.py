from sqlite3 import Connection
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt5.QtWidgets import QCheckBox, QComboBox, QDoubleSpinBox, QGridLayout, QGroupBox, QLabel, QPlainTextEdit
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
        image_uris = []
        try:
            if card['image_uris']: image_uris.append(card['image_uris'])
            elif card['card_faces']:
                cards_faces = literal_eval(card['card_faces'])
                for face in cards_faces:
                    image_uris.append(face['image_uris'])
        except KeyError: return
                    
        for i, uris in enumerate(image_uris):
            face_number = f"-{i}" if i > 0 else ''
            file_name = f"{config.get('FOLDER', 'cards')}/{id}{face_number}.{image_extension}"
            r = get(uris[config.get('COLLECTION', 'image_type')], stream = True)
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
def download_all_images_in_collection(connection: Connection, collection_ids: list) -> None:
    for id in collection_ids:
        download_image_if_not_downloaded(connection, id, config.get('COLLECTION', 'image_extension'))

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

    #card_width = 215
    card_width = 205
    card_height = int(card_width * 1.39)
    labels_height = 30

    cards_in_row = floor(current_grid_size.width() / (card_width + 50))
    cards_in_row = 8 if cards_in_row > 8 else cards_in_row
    cards_in_row = 2 if cards_in_row < 2 else cards_in_row

    cards_in_col = floor(current_grid_size.height() / (card_height + 50))
    cards_in_col = 4 if cards_in_col > 4 else cards_in_col
    cards_in_col = 1 if cards_in_col < 1 else cards_in_col
    
    cards_on_grid = cards_in_row * cards_in_col

    grid_width = current_grid_size.width()
    total_cards_width = cards_in_row * card_width
    horizontal_space_left = grid_width - total_cards_width
    number_of_horizontal_spacings = (cards_in_row - 1) if cards_in_row > 1 else 1
    spacing_horizontal = horizontal_space_left / number_of_horizontal_spacings

    grid_height = current_grid_size.height()
    total_cards_height = cards_in_col * card_height + cards_in_col * labels_height
    vertical_space_left = grid_height - total_cards_height
    number_of_vertical_spacings = (cards_in_col - 1) if cards_in_col > 1 else 1
    spacing_vertical = vertical_space_left / number_of_vertical_spacings
    
    result = {
        'cards_on_grid': cards_on_grid,
        'cards_in_row': cards_in_row,
        'cards_in_col': cards_in_col,
        'card_width': card_width,
        'card_height': card_height,
        'spacing_horizontal': spacing_horizontal,
        'spacing_vertical': spacing_vertical
    }
    
    return result
def delete_widgets_from_layout(layout: QGridLayout) -> None:
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
    from math import floor
    
    maximum = 1
    if len(cards_to_display) % cards_on_grid == 0: maximum = (len(cards_to_display) / cards_on_grid)
    else: maximum = floor(len(cards_to_display) / cards_on_grid + 1)
    if maximum < 1: maximum = 1
    
    page_control_widget.setMaximum(maximum)
    
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
def create_currency_string() -> str:
    currency_symbol = ''
    if config.get('COLLECTION', 'price_currency') == 'eur': currency_symbol = '€'
    elif config.get('COLLECTION', 'price_currency') == 'usd': currency_symbol = '$'
    else: currency_symbol += f" {config.get('COLLECTION', 'price_currency').upper()}"
    return currency_symbol
def create_card_image(card_image: QLabel, card: str, image_extension: str, card_width: int, card_height: int) -> None:
    card_image.setObjectName('image')
    card_image.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    card_image.setMaximumHeight(int(205*1.39))
    #card_image.setStyleSheet("background-color: gainsboro")
    
    pixmap = QPixmap(f"{config.get('FOLDER', 'cards')}/{card}.{image_extension}")
    pixmap_scaled = pixmap.scaled(card_width, card_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    card_image.setPixmap(pixmap_scaled)
def create_card_info(card_info: QLabel, in_collection: bool, collection_cards: dict, card: str, price_string: str, currency_symbol: str) -> None:
    card_info.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    card_info.setMaximumHeight(20)
    #card_info.setStyleSheet("background-color: gainsboro")
    
    card_info_text = ''
    price_slash = price_string.index(' / ')
    
    if in_collection:
        crd_idx = collection_cards['id'].index(card)
        regular = collection_cards['regular'][crd_idx]
        foil = collection_cards['foil'][crd_idx]
        
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
    card_extra_info.setText('')
    card_extra_info.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    #card_extra_info.setStyleSheet("background-color: gainsboro")
    card_extra_info.setMaximumHeight(20)
def prepare_card_description(card: dict) -> str:
    from ast import literal_eval
    
    description = ''
    if card['flavor_name']: description += f"{card['flavor_name']}"
    else: description += f"{card['name']}"
    if card['mana_cost']: description +=  f" - {card['mana_cost']}"
    if card['type_line']: description +=  f"\n\n{card['type_line']}"
        
    description += f"\n"
    
    if card['rarity']: description += f"{'Mythic rare' if card['rarity'] == 'mythic' else card['rarity'].capitalize()} — "
    if card['set_name']: description += f"{card['set_name']}"
    if card['collector_number']: description += f" ({card['collector_number']})"
    if card['set']: description += f" [{card['set'].upper()}]"
        
    description += f"\n-----------"
    
    if card['oracle_text']: card['oracle_text'] = card['oracle_text'].replace('\n', '\n\n')
    
    if not card['card_faces']:
        if card['oracle_text']: description += f"\n\n{card['oracle_text']}"
        if card['power']: description += f"\n{card['power']}/{card['toughness']}"
        if card['flavor_text']: description += f"\n\n---\n{card['flavor_text']}"
    else:
        card_faces = literal_eval(card['card_faces'])
        for i, face in enumerate(card_faces):
            if face.get('oracle_text'):
                if i == 0: description += f"\nFront side"
                elif i == 1: description += f"\n-----------\nBack side"
                description += f"\n\n{face['oracle_text']}"
            if face.get('power'): description += f"\n{face['power']}/{face['toughness']}"
            if face.get('flavor_text'): description += f"\n\n---\n{face['flavor_text']}"
        
    return description

#Progression
def find_all_sets_in_db(connection: Connection) -> dict:
    from modules.database.functions import get_database_table_name
    
    sets = {}
    
    query = f'''
        SELECT DISTINCT "set", set_name, set_type, released_at
        FROM {get_database_table_name()}
        ORDER BY released_at DESC
        '''

    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()

    for record in records:
        if record[0] not in sets:
            sets[record[0]] = [record[1], record[2], record[3]]

    query = f'''
        SELECT "set", count("set")
        FROM {get_database_table_name()}
        GROUP by "set"
    '''
    
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()

    for record in records:
        sets[record[0]].append(record[1])

    return sets

#Add cards tab
def update_card_count_in_add_cards(connection: Connection, found_cards: list, current_row: int, label: QLabel) -> None:
    from modules.database.collections import get_card_from_collection
    selected_card = get_card_from_collection(connection, config.get('COLLECTION', 'current_collection'), found_cards[current_row])

    label.setText(f"You currently have {selected_card['regular']} regulars and {selected_card['foil']} foils in collection")
def add_card_to_collection_in_add_cards(db_connection: Connection, cl_connection: Connection, found_cards: list, sorted_list: list, current_row: int, regular: int, foil: int, mode: str) -> None:
    from modules.database.collections import add_card_to_collection
    from modules.database.functions import get_combined_card_sort_key
        
    add_card_to_collection(
        cl_connection,
        config.get('COLLECTION', 'current_collection'), 
        found_cards[current_row],
        regular,
        foil,
        mode,
        get_combined_card_sort_key(db_connection, found_cards[current_row])
        )    

#Import/export tab
def process_import_list(db_connection: Connection, col_connection: Connection, import_list: list, pattern: str, results_plaintextedit: QPlainTextEdit, errors_plaintextedit: QPlainTextEdit, header_checkbox: QCheckBox) -> None:
    from modules.database.collections import create_collection
    from modules.database.functions import get_combined_sort_keys_from_db, get_all_cards_from_pattern_as_joined_string, get_card_ids_list, get_database_table_name
    from modules.globals import SORTING_ATTRIBUTES
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
        'sort_keys': get_combined_sort_keys_from_db(db_connection),
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
    
    #Most cases for MTGBollectionBuilder
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
        ' (Schematic)',
        ' (Skyscraper)' ,
        ' (Gilded Foil)',
        ' (Thick Stock)',
        ' (Non-Foil)',
        ' (Scene)'
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
    
    #Single cards for MTGBollectionBuilder
    mtg_cb_singles = [     
        { 'from_s': 'FNM Promos', 'to_s': 'Friday Night Magic 2013', 'from_n': 'Grisly Salvage', 'from_c': '162', 'to_c': '11'},
        { 'from_s': 'Release Event Promos', 'to_s': 'Rise of the Eldrazi Promos', 'from_n': 'Lord of Shatterskull Pass', 'from_c': '24', 'to_c': '156★'},
        { 'from_s': 'Release Event Promos', 'to_s': 'Journey into Nyx Promos', 'from_n': 'Dictate of the Twin Gods', 'from_c': '41', 'to_c': '93★'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Magic Origins Promos', 'from_n': 'Relic Seeker', 'from_c': '25', 'to_c': '29'},
        { 'from_s': 'Release Event Promos', 'to_s': 'Oath of the Gatewatch Promos', 'from_n': 'Endbringer', 'from_c': '49', 'to_c': '3'},
        { 'from_s': 'Clash Pack Promos', 'to_s': 'Fate Reforged Clash Pack', 'from_n': 'Necropolis Fiend', 'from_c': '7', 'to_c': '1'},
        { 'from_s': 'Clash Pack Promos', 'to_s': 'Fate Reforged Clash Pack', 'from_n': "Hero's Downfall", 'from_c': '8', 'to_c': '2'},
        { 'from_s': 'Clash Pack Promos', 'to_s': 'Fate Reforged Clash Pack', 'from_n': 'Sultai Ascendancy', 'from_c': '9', 'to_c': '3'},
        { 'from_s': 'Clash Pack Promos', 'to_s': 'Fate Reforged Clash Pack', 'from_n': 'Reaper of the Wilds', 'from_c': '10', 'to_c': '4'},
        { 'from_s': 'Clash Pack Promos', 'to_s': 'Fate Reforged Clash Pack', 'from_n': 'Whip of Erebos', 'from_c': '11', 'to_c': '5'},
        { 'from_s': 'Clash Pack Promos', 'to_s': 'Fate Reforged Clash Pack', 'from_n': 'Courser of Kruphix', 'from_c': '12', 'to_c': '6'},
        { 'from_s': 'Gift Box Promos', 'to_s': 'Khans of Tarkir Promos', 'from_n': 'Sultai Charm', 'from_c': '3', 'to_c': '204'},
        { 'from_s': 'Game Day Promos', 'to_s': 'Eldritch Moon Promos', 'from_n': 'Unsubstantiate', 'from_c': '61', 'to_c': '79'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Amonkhet Promos', 'from_n': 'Archfiend of Ifnir', 'from_c': '32', 'to_c': '78'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Core Set 2020', 'from_n': 'Rienne, Angel of Rebirth', 'from_c': '52', 'to_c': '281'},
        { 'from_s': 'Promo Pack: Core Set 2020', 'to_s': 'Dominaria Promos', 'from_n': 'Gilded Lotus', 'from_c': '118', 'to_c': '215p'},
        { 'from_s': 'Promo Pack: Throne of Eldraine', 'to_s': 'Throne of Eldraine', 'from_n': 'Improbable Alliance', 'from_c': '4', 'to_c': '396'},
        { 'from_s': 'Promo Pack: Throne of Eldraine', 'to_s': 'Throne of Eldraine Promos', 'from_n': 'Wishclaw Talisman', 'to_n': 'Wishclaw Talisman', 'from_c': '34', 'to_c': '110p'},
        { 'from_s': 'Promo Pack: Throne of Eldraine', 'to_s': 'Throne of Eldraine Promos', 'from_n': 'Emry, Lurker of the Loch', 'from_c': '17', 'to_c': '43p'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Theros Beyond Death', 'from_n': 'Athreos, Shroud-Veiled', 'from_c': '54', 'to_c': '269'},
        { 'from_s': 'Prerelease Cards', 'to_s': 'Theros Beyond Death Promos', 'from_n': 'Atris, Oracle of Half-Truths', 'from_c': '1473', 'to_c': '209s'},
        { 'from_s': 'Promo Pack: Theros Beyond Death', 'to_s': 'Theros Beyond Death', 'from_n': 'Thirst for Meaning', 'from_c': '2', 'to_c': '354'},
        { 'from_s': 'Promo Pack: Theros Beyond Death', 'to_s': 'Theros Beyond Death Promos', 'from_n': 'Underworld Breach', 'from_c': '41', 'to_c': '161p'},
        { 'from_s': 'Prerelease Cards', 'to_s': 'Ikoria: Lair of Behemoths Promos', 'from_n': 'Emergent Ultimatum', 'from_c': '1531', 'to_c': '185s'},
        { 'from_s': 'Promo Pack: Ikoria', 'to_s': 'Ikoria: Lair of Behemoths Promos', 'from_n': 'Gyruda, Doom of Depths', 'from_c': '56', 'to_c': '221p'},
        { 'from_s': 'Promo Pack: Ikoria', 'to_s': 'Ikoria: Lair of Behemoths Promos', 'from_n': 'Keruga, the Macrosage', 'from_c': '59', 'to_c': '225p'},
        { 'from_s': 'Prerelease Cards', 'to_s': 'Double Masters', 'from_n': 'Chord of Calling', 'from_c': '1644', 'to_c': '384'},
        { 'from_s': 'Promo Pack: Zendikar Rising', 'to_s': 'Zendikar Rising Promos', 'from_n': 'Thieving Skydiver', 'from_c': '25', 'to_c': '85p'},
        { 'from_s': 'Promo Pack: Zendikar Rising', 'to_s': 'Zendikar Rising Promos', 'from_n': 'Skyclave Relic', 'from_c': '71', 'to_c': '252p'},
        { 'from_s': 'Prerelease Cards', 'to_s': 'Commander Legends', 'from_n': 'Sengir, the Dark Baron', 'from_c': '1729', 'to_c': '722'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Kaldheim', 'from_n': 'Realmwalker', 'from_c': '59', 'to_c': '399'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Throne of Eldraine', 'from_n': 'Kenrith, the Returned King (Non-Foil)', 'to_n': 'Kenrith, the Returned King', 'from_c': '53b', 'to_c': '303'},
        { 'from_s': 'Promo Pack: Strixhaven', 'to_s': 'Strixhaven: School of Mages Promos', 'from_n': 'Culling Ritual', 'from_c': '62', 'to_c': '172p'},
        { 'from_s': 'Bundle Promos', 'to_s': 'Modern Horizons 2', 'from_n': "Yusri, Fortune's Flame", 'from_c': '9', 'to_c': '492'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Plains', 'from_c': '594', 'to_c': '481'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Plains', 'from_c': '595', 'to_c': '482'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Island', 'from_c': '596', 'to_c': '483'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Island', 'from_c': '597', 'to_c': '484'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Swamp', 'from_c': '598', 'to_c': '485'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Swamp', 'from_c': '599', 'to_c': '486'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Mountain', 'from_c': '600', 'to_c': '487'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Mountain', 'from_c': '601', 'to_c': '488'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Forest', 'from_c': '602', 'to_c': '489'},
        { 'from_s': 'Modern Horizons 2', 'from_n': 'Forest', 'from_c': '603', 'to_c': '490'},
        { 'from_s': 'Promo Pack: Forgotten Realms', 'to_s': 'Adventures in the Forgotten Realms', 'from_n': 'Prosperous Innkeeper', 'from_c': '5', 'to_c': '402'},
        { 'from_s': 'Love Your LGS', 'to_s': 'Love Your LGS 2021', 'from_n': 'Dig Through Time', 'from_c': '4', 'to_c': '2'},
        { 'from_s': 'Love Your LGS', 'to_s': 'Love Your LGS 2021', 'from_n': "Bolas's Citadel", 'from_c': '5', 'to_c': '3'},
        { 'from_s': 'Store Championship Promos', 'to_s': 'Wizards Play Network 2021', 'from_n': 'Arbor Elf', 'from_c': '6', 'to_c': '1'},
        { 'from_s': 'Bring-a-Friend Promos', 'to_s': 'Wizards Play Network 2021', 'from_n': 'Mind Stone', 'from_c': '1', 'to_c': '5'},
        { 'from_s': 'Promo Pack: Innistrad Midnight Hunt', 'to_s': 'Innistrad: Midnight Hunt Promos', 'from_n': 'Slogurk, the Overslime', 'from_c': '63', 'to_c': '242p'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Innistrad: Crimson Vow', 'from_n': 'Voldaren Estate', 'from_c': '66', 'to_c': '403'},
        { 'from_s': 'Prerelease Cards', 'to_s': 'Kamigawa: Neon Dynasty Promos', 'from_n': 'Tatsunari, Toad Rider', 'from_c': '2284', 'to_c': '123s'},
        { 'from_s': 'Prerelease Cards', 'to_s': 'Kamigawa: Neon Dynasty Promos', 'from_n': 'Satoru Umezawa', 'from_c': '2317', 'to_c': '234s'},
        { 'from_s': 'Promo Pack: Kamigawa', 'to_s': 'Kamigawa: Neon Dynasty Promos', 'from_n': 'Lizard Blades', 'from_c': '39', 'to_c': '153s'},
        { 'from_s': 'Buy-a-Box Promos', 'to_s': 'Streets of New Capenna', 'from_n': 'Jaxis, the Troublemaker', 'from_c': '68', 'to_c': '461'},
        { 'from_s': 'Prerelease Cards', 'to_s': "Battle for Baldur's Gate Promos", 'from_n': 'Astarion, the Decadent', 'from_c': '2474', 'to_c': '265s'},
        { 'from_s': 'Bundle Promos', 'to_s': 'Dominaria United', 'from_n': 'Herd Migration', 'from_c': '70', 'to_c': '429'},
        { 'from_s': 'Prerelease Cards', 'to_s': 'Phyrexia: All Will Be One Promos', 'from_n': 'Blackcleave Cliffs', 'from_c': '2750', 'to_c': '248s'},
        { 'from_s': 'Bundle Promos', 'to_s': 'March of the Machine', 'from_n': 'Ghalta and Mavren', 'from_c': '23', 'to_c': '386'},
        #To do, stamped with year
        #{ 'from_s': 'Prerelease Cards', 'to_s': '', 'from_n': 'Blackcleave Cliffs', 'from_c': '2750', 'to_c': ''}
    ]
    
    #DEBUG
    if "Plains" in split_card['%n'] and '594' in split_card['%c']:
        pass
    
    for card in mtg_cb_singles:
        if split_card['%n'] in card['from_n'] and split_card['%c'] in card['from_c']:
            if 'to_s' in card: split_card['%s'] = card['to_s']
            if 'to_n' in card: split_card['%n'] = card['to_n']
            if 'to_c' in card: split_card['%c'] = card['to_c']
    
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
