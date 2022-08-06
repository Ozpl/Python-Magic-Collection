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
    CREATE TABLE IF NOT EXISTS mtg_table (
        id VARCHAR(255) NOT NULL PRIMARY KEY,
        arena_id INT,
        lang VARCHAR(255),
        mtgo_id INT,
        mtgo_foil_id INT,
        multiverse_ids_1 INT,
        multiverse_ids_2 INT,
        tcgplayer_id INT,
        tcgplayer_etched_id INT,
        cardmarket_id INT,
        object VARCHAR(255),
        oracle_id VARCHAR(255),
        prints_search_uri VARCHAR(255),
        rulings_uri VARCHAR(255),
        scryfall_uri VARCHAR(255),
        uri VARCHAR(255),
        
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
         VARCHAR(255),
        
    )
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def debug_insert(connection, columns, tuple):
    placeholders = ', '.join('?' * len(columns))
    query = f'''
    INSERT INTO mtg_table({columns}) VALUES {placeholders}
    '''
    cursor = connection.cursor()
    cursor.execute(query, tuple)
    connection.commit()

connection = create_connection(DATABASE_PATH)
create_main_table(connection)
#debug_insert(connection, ('3445', 456, 'us'))
connection.close()