#SETTINGS
SETTINGS_FOLDER_STRUCTURE = {
    'collections': 'collections',
    'database': 'database',
    'decks': 'decks',
    'downloads': 'downloads',
    'images': 'images',
    'cards': 'images/cards',
    'symbols': 'images/symbols',
    'sets': 'images/sets'
}
SETTINGS_FILE_STRUCTURE = {
    'config': 'config.ini',
    'database': f"./{SETTINGS_FOLDER_STRUCTURE['database']}/database.db",
    'collections': f"./{SETTINGS_FOLDER_STRUCTURE['database']}/collections.db",
    'decks': f"./{SETTINGS_FOLDER_STRUCTURE['database']}/decks.db"
}

#APP
APP_NAME = 'Python Magic Collection'
APP_STYLE = 'Fusion'
APP_FONT_NAME = 'MS Shell Dlg 2'
APP_FONT_SIZE = 13
APP_TAB_NAMES = {
    'collection': 'Collection',
    'decks': 'Decks',
    'add_cards': 'Add cards',
    'wishlist': "Wishlist",
    'import_export': 'Import/export',
    'settings': 'Settings'
}

#DATABASE
#DATABASE_SUBTABLES are now demonstrative, they are being wiped and build again in create.py
DATABASE_SUBTABLES_NAMES_EXCEPTIONS = [
    'all_parts',
    'card_faces',
    'card_faces_image_uris'
]
DATABASE_SUBTABLES_NAMES_ARRAY = [
    'attraction_lights',
    'artist_ids',
    'color_identity',
    'color_indicator',
    'colors',
    'finishes',
    'frame_effects',
    'games',
    'keywords',
    'multiverse_ids',
    'produced_mana',
    'promo_types'
]
DATABASE_SUBTABLES_NAMES_OBJECT = [
    'image_uris',
    'legalities',
    'prices',
    'related_uris',
    'preview'
]
DATABASE_FREQUENT_UPDATING = [
    'prices',
    'edhrec_rank',
    'penny_rank'
]