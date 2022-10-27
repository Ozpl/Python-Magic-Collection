from modules.config import Config

#CONFIG
config = Config()

#DATABASE
DATABASE_INSERT_TO_MAIN = []
DEFAULT_SEARCH_COLUMNS = ['name', 'type_line', 'oracle_text']
IMPORT_PATTERN_MAP = {'%n': 'name', '%s': 'set_name', '%q': 'quantity', '%f': 'foil', '%r': 'rarity', '%c': 'collector_number', '%*': 'wildcard'}