import logging
import sys

from config.settings import settings


def setup_logger(name: str = "hse_doc") -> logging.Logger:
    logger = logging.getLogger(name)

    # Чтобы при повторном вызове не добавлялись дублирующие хендлеры
    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = setup_logger()