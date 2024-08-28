import logging
import sys


def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    # ref: https://nigimitama.hatenablog.jp/entry/2021/01/27/084458
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(handler)
    return logger
