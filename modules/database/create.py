import sqlite3
from modules.consts import DATABASE_SUBTABLES_NAMES_EXCEPTIONS, DATABASE_SUBTABLES_NAMES_ARRAY, DATABASE_SUBTABLES_NAMES_OBJECT

def create_main_table(connection):
    query = '''
    CREATE TABLE IF NOT EXISTS main_table (
        id VARCHAR(255) NOT NULL PRIMARY KEY,
        arena_id INT,
        lang VARCHAR(255),
        mtgo_id INT,
        mtgo_foil_id INT,
        tcgplayer_id INT,
        tcgplayer_etched_id INT,
        cardmarket_id INT,
        object VARCHAR(255),
        oracle_id VARCHAR(255),
        prints_search_uri VARCHAR(255),
        rulings_uri VARCHAR(255),
        scryfall_uri VARCHAR(255),
        uri VARCHAR(255),
        cmc INT,
        edhrec_rank INT,
        hand_modifier VARCHAR(255),
        layout VARCHAR(255),
        life_modifier VARCHAR(255),
        loyalty VARCHAR(255),
        mana_cost VARCHAR(255),
        name VARCHAR(255),
        oracle_text VARCHAR(255),
        oversized VARCHAR(255),
        penny_rank INT,
        power VARCHAR(255),
        reserved VARCHAR(255),
        toughness VARCHAR(255),
        type_line VARCHAR(255),
        artist VARCHAR(255),
        booster VARCHAR(255),
        border_color VARCHAR(255),
        card_back_id VARCHAR(255),
        collector_number VARCHAR(255),
        content_warning VARCHAR(255),
        digital VARCHAR(255),
        flavor_name VARCHAR(255),
        flavor_text VARCHAR(255),
        frame VARCHAR(255),
        full_art VARCHAR(255),
        highres_image VARCHAR(255),
        illustration_id VARCHAR(255),
        image_status VARCHAR(255),
        printed_name VARCHAR(255),
        printed_text VARCHAR(255),
        printed_type_line VARCHAR(255),
        promo VARCHAR(255),
        rarity VARCHAR(255),
        released_at DATETIME,
        reprint VARCHAR(255),
        scryfall_set_uri VARCHAR(255),
        set_name VARCHAR(255),
        set_search_uri VARCHAR(255),
        set_type VARCHAR(255),
        set_uri VARCHAR(255),
        "set" VARCHAR(255),
        set_id VARCHAR(255),
        story_spotlight VARCHAR(255),
        textless VARCHAR(255),
        variation VARCHAR(255),
        variation_of VARCHAR(255),
        security_stamp VARCHAR(255),
        watermark VARCHAR(255),
        checksum BIGINT
    )
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_subt_exceptions(connection, subtable):
    if subtable == 'all_parts':
        columns = ['object', 'id', 'component', 'name', 'type_line', 'uri']
        query = f'''
        CREATE TABLE IF NOT EXISTS {subtable}_table (
            db_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            card_id VARCHAR(255) NOT NULL,
            {', '.join([f'{element} VARCHAR(255)' for element in columns])}
        )
        '''

    elif subtable == 'card_faces':
        #'image_uris' is skipped for now
        columns = ['artist', 'artist_id', 'cmc', 'color_indicator', 'colors', 'flavor_name', 'flavor_text', 'illustration_id', 'layout', 'loyalty', 'mana_cost', 'name', 'object', 'oracle_id', 'oracle_text', 'power', 'printed_name', 'printed_text', 'printed_type_line', 'toughness', 'type_line', 'watermark']
        query = f'''
        CREATE TABLE IF NOT EXISTS {subtable}_table (
            db_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            card_id VARCHAR(255) NOT NULL,
            {', '.join([f'{element} VARCHAR(255)' for element in columns])}
        )
        '''
    
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_subt_array(connection, subtable):
    query = f'''
    CREATE TABLE IF NOT EXISTS {subtable}_table (
        db_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        card_id VARCHAR(255) NOT NULL,
        array_value VARCHAR(255) NOT NULL
    )
    '''
    
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_subt_object(connection, subtable):
    columns = []
    match subtable:
        case 'image_uris':
            columns = ['small', 'normal', 'large', 'png', 'art_crop', 'border_crop']
        case 'legalities':
            columns = ['standard', 'future', 'historic', 'gladiator', 'pioneer', 'explorer', 'modern', 'legacy', 'pauper', 'vintage', 'penny', 'commander', 'brawl', 'historicbrawl', 'alchemy', 'paupercommander', 'duel', 'oldschool', 'premodern']
        case 'prices':
            columns = ['usd', 'usd_foil', 'usd_etched', 'eur', 'eur_foil', 'tix']
        case 'related_uris':
            columns = ['gatherer', 'tcgplayer_infinite_articles', 'tcgplayer_infinite_decks', 'edhrec']
        case 'preview':
            columns = ['source', 'source_uri', 'previewed_at']

    query = f'''
    CREATE TABLE IF NOT EXISTS {subtable}_table (
        db_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        card_id VARCHAR(255) NOT NULL,
        {', '.join([f'{element} VARCHAR(255)' for element in columns])}
    )
    '''

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_sub_tables(connection):
    for element in DATABASE_SUBTABLES_NAMES_EXCEPTIONS:
        create_subt_exceptions(connection, element)
    for element in DATABASE_SUBTABLES_NAMES_ARRAY:
        create_subt_array(connection, element)
    for element in DATABASE_SUBTABLES_NAMES_OBJECT:
        create_subt_object(connection, element)