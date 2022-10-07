import logging

def console_log(type, message):
    level = logging.DEBUG
    format = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=format)

    match str(type).lower():
        case 'debug':
            logging.debug(message)
        case 'info':
            logging.info(message)
        case 'warning':
            logging.warning(message)
        case 'error':
            logging.error(message)
        case 'critical':
            logging.critical(message)