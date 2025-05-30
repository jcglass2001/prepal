import logging
import sys
from config.settings import AppSettings

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(AppSettings.LOG_LEVEL)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s:%(name)s: %(message)s'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger 
