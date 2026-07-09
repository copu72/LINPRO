"""Tests para el sistema de preferencias de usuario de LINPRO."""

import pytest
from linpro.settings import UserSettings
from linpro.exceptions import SettingsError


class TestUserSettings:
    def setup_method(self):
        UserSettings._instance = None

    def test_singleton(self):
        us1 = UserSettings.get_instance()
        us2 = UserSettings.get_instance()
        assert us1 is us2

    def test_get_instance_devuelve_siempre_la_misma(self):
        UserSettings._instance = None
        us = UserSettings.get_instance()
        assert us is UserSettings.get_instance()

    def test_valores_por_defecto_idioma(self):
        us = UserSettings.get_instance()
        assert us.get("ui.language") == "es"

    def test_valores_por_defecto_tema(self):
        us = UserSettings.get_instance()
        assert us.get("ui.theme") == "light"

    def test_valores_por_defecto_font_size(self):
        us = UserSettings.get_instance()
        assert us.get("ui.font_size") == 10

    def test_valores_por_defecto_ventana(self):
        us = UserSettings.get_instance()
        assert us.get("window.width") == 1280
        assert us.get("window.height") == 800
        assert us.get("window.maximized") is False

    def test_valores_por_defecto_recent_files(self):
        us = UserSettings.get_instance()
        assert us.get("recent_files") == []

    def test_valores_por_defecto_last_project(self):
        us = UserSettings.get_instance()
        assert us.get("last_project") == ""

    def test_get_clave_inexistente_devuelve_default(self):
        us = UserSettings.get_instance()
        assert us.get("clave.inexistente", 42) == 42

    def test_get_clave_inexistente_sin_default_devuelve_none(self):
        us = UserSettings.get_instance()
        assert us.get("clave.inexistente") is None

    def test_set_y_get_simple(self):
        us = UserSettings.get_instance()
        us.set("ui.language", "en")
        assert us.get("ui.language") == "en"

    def test_set_y_get_anidado(self):
        us = UserSettings.get_instance()
        us.set("ui.font_size", 12)
        assert us.get("ui.font_size") == 12

    def test_set_crea_claves_nuevas(self):
        us = UserSettings.get_instance()
        us.set("custom.preferencia", "valor_personalizado")
        assert us.get("custom.preferencia") == "valor_personalizado"