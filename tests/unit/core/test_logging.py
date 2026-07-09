"""Tests para el sistema de logging de LINPRO."""

from linpro.core.logging import LINPROLogger, LogLevel


class TestLINPROLogger:
    def test_singleton(self):
        a = LINPROLogger.get_instance()
        b = LINPROLogger.get_instance()
        assert a is b

    def test_nombre_predeterminado(self):
        logger = LINPROLogger.get_instance()
        assert logger.name == "linpro"

    def test_nombre_personalizado(self):
        logger = LINPROLogger(name="test")
        assert logger.name == "test"

    def test_info_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        logger.info("mensaje de info")

    def test_warning_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        logger.warning("mensaje de warning")

    def test_error_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        logger.error("mensaje de error")

    def test_debug_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        logger.debug("mensaje de debug")

    def test_critical_no_lanza_excepcion(self):
        logger = LINPROLogger.get_instance()
        logger.critical("mensaje de critical")

    def test_set_level_debug(self):
        logger = LINPROLogger(name="level_test")
        logger.set_level(LogLevel.DEBUG)
        logger.debug("debug despues de set_level DEBUG")
        logger.info("info despues de set_level DEBUG")

    def test_set_level_info(self):
        logger = LINPROLogger(name="level_info_test")
        logger.set_level(LogLevel.INFO)
        logger.info("info despues de set_level INFO")

    def test_set_level_warning(self):
        logger = LINPROLogger(name="level_warning_test")
        logger.set_level(LogLevel.WARNING)
        logger.warning("warning despues de set_level WARNING")

    def test_set_level_error(self):
        logger = LINPROLogger(name="level_error_test")
        logger.set_level(LogLevel.ERROR)
        logger.error("error despues de set_level ERROR")

    def test_set_level_critical(self):
        logger = LINPROLogger(name="level_critical_test")
        logger.set_level(LogLevel.CRITICAL)
        logger.critical("critical despues de set_level CRITICAL")