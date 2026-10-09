import logging
import sys


def setup_logger(name: str = "hse_doc") -> logging.Logger:
    doc_logger = logging.getLogger(name)

    if doc_logger.handlers:
        return doc_logger

    doc_logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    doc_logger.addHandler(handler)
    doc_logger.propagate = False

    return doc_logger


logger = setup_logger()
