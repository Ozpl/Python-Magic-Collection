from forex_python.converter import CurrencyRates, RatesNotAvailableError
from modules.config import Config

#CONFIG
config = Config()

#CURRENCY
CURRENCY_RATES = CurrencyRates()
CURRENCY = config.get('COLLECTION', 'price_currency')
try: EXCHANGE_RATE = CURRENCY_RATES.get_rate('USD', CURRENCY.upper())
except RatesNotAvailableError: EXCHANGE_RATE = 1

#DATABASE
DATABASE_INSERT_TO_MAIN = []
DEFAULT_SEARCH_COLUMNS = ['name', 'type_line', 'oracle_text']
UI_PATTERN_LEGEND = """Available symbols:
Required:
    %n - card's name
    Choose at least one:
        %e - set (abbreviation, e.g. "DOM")
        %s - set name (full name, e.g. "Dominaria")
    %c - collector's number
    %q - quantity
    %f - is foil? (e.g. True or False)
    #TODO
    #%regular and %foil
    
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