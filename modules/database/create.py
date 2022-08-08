import sqlite3
from sqlite3 import Error

DATABASE_PATH = './database/database.db'

def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except Error as e:
        print(e)

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
        uri VARCHAR(255)
    )
    '''

    '''
        ...all_parts
        ...card_faces
        cmc
        color_identity
        color_indicator
        colors
        edhrec_rank
        hand_modifier
        keywords
        layout
        legalities
        life_modifier
        loyalty
        mana_cost
        name
        oracle_text
        oversized
        penny_rank
        power
        produced_mana
        reserved
        toughness
        type_line

        artist
        booster
        border_color
        card_back_id
        collector_number
        content_warning
        digital
        finishes
        flavor_name
        flavor_text
        frame_effects
        frame
        full_art
        games
        highres_image
        illustration_id
        image_status
        image_uris
        prices
        printed_name
        printed_text
        printed_type_line
        promo
        promo_types
        purchase_uris
        rarity
        related_uris
        released_at
        reprint
        scryfall_set_uri
        set_name
        set_search_uri
        set_type
        set_uri
        set
        set_id
        story_spotlight
        textless
        variation
        variation_of
        security_stamp
        watermark
        preview.previewed_at
        preview.source_uri
        preview.source

        artist
        cmc
        color_indicator
        colors
        flavor_text
        illustration_id
        image_uris
        layout
        loyalty
        mana_cost
        name
        object
        oracle_id
        oracle_text
        power
        printed_name
        printed_text
        printed_type_line
        toughness
        type_line
        watermark

        id
        object
        component
        name
        type_line
        uri        
    )
    '''
    
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_sub_table(connection, attribute):
    '''
    multiverse
    all_parts
    card_faces
    keywords
    finishes
    frame_effects
    games
    promo_types
    '''
    
    att_type = 'VARCHAR(255)'

    match attribute:
        case 'multiverse_id':
            att_type = 'INT'


    query = f'''
    CREATE TABLE IF NOT EXISTS {attribute}_table (
        id INTEGER NOT NULL PRIMARY KEY,
        main_id VARCHAR(255) NOT NULL,
        value {att_type} NOT NULL
    )
    '''
        
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

connection = create_connection(DATABASE_PATH)
create_main_table(connection)
create_sub_table(connection, 'multiverse_id')
connection.close()