from config.settings import app_config
import logging
import sys

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(app_config.LOG_LEVEL)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s:%(name)s: %(message)s'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger 
