import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pytz import timezone

LOGGER_NAME = "connexion_example"

def create_log():
    def timetz(*args):
        return datetime.now(tz).timetuple()

    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    tz = timezone('America/Chicago')  # UTC, Asia/Shanghai, Europe/Berlin
    logging.Formatter.converter = timetz

    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                f"./logs/{LOGGER_NAME}.log", mode="a", maxBytes=50000, backupCount=10
            )
        ],
    )

    logger = logging.getLogger(LOGGER_NAME)

    return logger
