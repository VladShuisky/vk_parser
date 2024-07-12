import logging
import os.path

LOGS_BASE_DIR = "log"

if not os.path.exists(LOGS_BASE_DIR):
    os.mkdir(LOGS_BASE_DIR)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(LOGS_BASE_DIR + f"/{name}.log")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger

community_parser_logger = create_logger('com_pars_logger')
csv_file_write_logger = create_logger('csv_writer_logger')
script_parsing_logger = create_logger('script_parsing_logger')