from logging import basicConfig, critical, DEBUG, debug, error, info, warning

def console_log(type: str, message: str) -> None:
    '''Types message to terminal using logging library.'''
    level = DEBUG
    format = '[%(levelname)s] %(asctime)s - %(message)s'
    basicConfig(level=level, format=format)

    match str(type).lower():
        case 'debug': debug(message)
        case 'info': info(message)
        case 'warning': warning(message)
        case 'error': error(message)
        case 'critical': critical(message)