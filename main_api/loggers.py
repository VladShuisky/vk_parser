import logging
import os.path

LOGS_BASE_DIR='log'

if not os.path.exists(LOGS_BASE_DIR):
    os.mkdir(LOGS_BASE_DIR)

def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(LOGS_BASE_DIR + f'/{name}.log')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger

db_logger = create_logger('db_logger')
community_parser_logger = create_logger('community_parser_logger')
get_groups_users_logger = create_logger('get_groups_users_logger')
