from requests import get
from modules.globals import config
from modules.logging import console_log

def get_bulk_data_response(url: str) -> list[dict]:
    request = get(url)
    response = request.json()
    return response['data']

def download_bulk_json_file(url: str, file_name: str) -> None:
    from json import dump

    console_log('info', 'Downloading new bulk_data')
    response = get(url)
    with open(f"./{config.get('FOLDER', 'database')}/{file_name}.json", 'w', encoding='utf8') as f:
        dump(response.json(), f, ensure_ascii=False, indent=4)
    console_log('info', 'bulk_data was downloaded successfully')

def get_data_from_scryfall() -> None:
    from datetime import datetime
    from forex_python.converter import CurrencyRates, RatesNotAvailableError
    
    bulk_response = get_bulk_data_response(config.get('BULK', 'url'))
    bulk_data_type = config.get('BULK', 'data_type')
    bulk_uri = [element['download_uri'] for element in bulk_response if element['name'] == bulk_data_type][0]

    time_difference = (datetime.now() - datetime.strptime(config.get('BULK', 'last_updated'), config.get('TIME', 'format_full'))).total_seconds()

    if time_difference > config.get_float('BULK', 'time_period'):
        config.set('FLAG', 'downloaded_from_scryfall', 'true')
        download_bulk_json_file(bulk_uri, bulk_data_type)
        config.set('BULK', 'last_updated', str(datetime.now().strftime(config.get('TIME', 'format_full'))))
        
        cr = CurrencyRates()
        try: currency_exchange_rate = cr.get_rate('USD', config.get('COLLECTION', 'price_currency').upper())
        except RatesNotAvailableError: currency_exchange_rate = 1
        config.set('COLLECTION', 'exchange_rate', str(currency_exchange_rate))
    else:
        config.set('FLAG', 'downloaded_from_scryfall', 'false')
