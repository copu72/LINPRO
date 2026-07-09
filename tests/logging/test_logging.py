"""Tests para el sistema de logging de LINPRO."""

import pytest
from linpro.logging import LINPROLogger, LogLevel
from linpro.exceptions import LogError


class TestLINPROLogger:
    def setup_method(self):
        LINPROLogger._instance = None

    def test_singleton(self):
        logger1 = LINPROLogger.get_instance()
        logger2 = LINPROLogger.get_instance()
        assert logger1 is logger2

    def test_get_instance_devuelve_siempre_la_misma(self):
        LINPROLogger._instance = None
        instancia = LINPROLogger.get_instance()
        assert instancia is LINPROLogger.get_instance()

    def test_info_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        try:
            logger.info("Mensaje de prueba")
        except Exception:
            pytest.fail("info() lanzó una excepción")

    def test_warning_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        try:
            logger.warning("Advertencia de prueba")
        except Exception:
            pytest.fail("warning() lanzó una excepción")

    def test_error_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        try:
            logger.error("Error de prueba")
        except Exception:
            pytest.fail("error() lanzó una excepción")

    def test_debug_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        try:
            logger.debug("Depuración de prueba")
        except Exception:
            pytest.fail("debug() lanzó una excepción")

    def test_critical_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        try:
            logger.critical("Crítico de prueba")
        except Exception:
            pytest.fail("critical() lanzó una excepción")

    def test_set_level_info(self):
        logger = LINPROLogger.get_instance()
        logger.set_level(LogLevel.INFO)
        assert logger._logger.level == LogLevel.INFO.value

    def test_set_level_debug(self):
        logger = LINPROLogger.get_instance()
        logger.set_level(LogLevel.DEBUG)
        assert logger._logger.level == LogLevel.DEBUG.value

    def test_set_level_warning(self):
        logger = LINPROLogger.get_instance()
        logger.set_level(LogLevel.WARNING)
        assert logger._logger.level == LogLevel.WARNING.value

    def test_set_level_error(self):
        logger = LINPROLogger.get_instance()
        logger.set_level(LogLevel.ERROR)
        assert logger._logger.level == LogLevel.ERROR.value

    def test_nombre_predeterminado(self):
        logger = LINPROLogger.get_instance()
        assert logger.name == "linpro"

    def test_nombre_personalizado(self):
        logger = LINPROLogger(name="test_modulo")
        assert logger.name == "test_modulo"