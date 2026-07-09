"""Tests para la aplicacion principal LINPRO."""

from linpro.core.app import LINPROApp


class TestLINPROApp:
    def test_singleton(self):
        a = LINPROApp.get_instance()
        b = LINPROApp.get_instance()
        assert a is b

    def test_is_running_false_inicial(self):
        app = LINPROApp()
        assert app.is_running is False

    def test_start_no_lanza_excepcion(self):
        app = LINPROApp()
        app.start()

    def test_is_running_true_despues_de_start(self):
        app = LINPROApp()
        app.start()
        assert app.is_running is True

    def test_stop_despues_de_start(self):
        app = LINPROApp()
        app.start()
        app.stop()
        assert app.is_running is False

    def test_stop_sin_start_no_lanza_error(self):
        app = LINPROApp()
        app.stop()

    def test_start_dos_veces(self):
        app = LINPROApp()
        app.start()
        app.start()
        assert app.is_running is True

    def test_propiedades_no_nulas_despues_de_start(self):
        app = LINPROApp()
        app.start()
        assert app.logger is not None
        assert app.config is not None
        assert app.event_bus is not None
        assert app.plugin_manager is not None
        assert app.workspace is not None