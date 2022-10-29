from modules.config import Config

#CONFIG
config = Config()

#DATABASE
DATABASE_INSERT_TO_MAIN = []
DEFAULT_SEARCH_COLUMNS = ['name', 'type_line', 'oracle_text']
UI_PATTERN_LEGEND = """Available symbols:
Required:
    %n - card's name
    Choose at least one:
        %e - set (abbreviation, i.e. "DOM")
        %s - set name (full name, i.e. "Dominaria")
    %c - collector's number
    %q - quantity
    %f - is foil?
    
Optional:
    %p - price
    %r - rarity
    %* - ignore phrase
    
Available separators: ','
"""
IMPORT_PATTERN_MAP = {'%n': 'name', '%e': 'set', '%s': 'set_name', '%q': 'quantity', '%f': 'foil', 'p': 'price', '%r': 'rarity', '%c': 'collector_number', '%*': 'wildcard'}
TEMPLATE_PATTERNS = [
    {'name': 'MTG Collection Builder', 'pattern': '%n,%s,%q,%f,%p,%r,%c', 'header': True}
]