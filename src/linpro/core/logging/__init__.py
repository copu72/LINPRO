"""Sistema de logging profesional para LINPRO.

Proporciona un logger configurable con niveles, formato y salida
a archivo y consola. Nunca se usa print() en LINPRO.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class LINPROLogger:
    _instance: Optional["LINPROLogger"] = None

    def __init__(self, name: str = "linpro", level: LogLevel = LogLevel.INFO) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level.value)
        self._logger.handlers.clear()
        self._name = name
        self._file_handler: Optional[logging.Handler] = None
        self._init_console_handler()

    @classmethod
    def get_instance(cls) -> "LINPROLogger":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _init_console_handler(self) -> None:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
        self._logger.addHandler(handler)

    def set_file_output(self, path: Path) -> None:
        if self._file_handler:
            self._logger.removeHandler(self._file_handler)
        self._file_handler = logging.FileHandler(path, encoding="utf-8")
        self._file_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
        self._logger.addHandler(self._file_handler)

    def set_level(self, level: LogLevel) -> None:
        self._logger.setLevel(level.value)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)

    @property
    def name(self) -> str:
        return self._name
