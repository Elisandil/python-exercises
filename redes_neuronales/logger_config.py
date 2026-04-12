"""
logger_config.py — Configuración centralizada de logging para los 3 scripts.
Uso: from logger_config import get_logger
     log = get_logger("mi_script")
     log.info("mensaje")
"""

import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    fmt = logging.Formatter(
        fmt="%(asctime)s [%(name)s] %(levelname)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    return logger