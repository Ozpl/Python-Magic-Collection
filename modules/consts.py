SETTINGS_JSON_PATH = './settings.json'
DATABASE_DB_PATH = './database/database.db'
APP_NAME = 'Python Magic Collection'
APP_STYLE = 'Fusion'
APP_FOLDER_STRUCTURE = {
    'collections': 'collections',
    'database': 'database',
    'decks': 'decks',
    'downloads': 'downloads',
    'images': 'images'
}
DATABASE_SUBTABLES_NAMES_EXCEPTIONS = [
    'all_parts',
    'card_faces'
]
DATABASE_SUBTABLES_NAMES_ARRAY = [
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
APP_TAB_NAMES = [
    'Collections',
    'Decks',
    'Add cards',
    'Import/export',
    'Settings'
]