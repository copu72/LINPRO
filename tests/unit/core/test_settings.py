"""Tests para las preferencias de usuario de LINPRO."""

from linpro.core.settings import UserSettings


class TestUserSettings:
    def test_singleton(self):
        a = UserSettings.get_instance()
        b = UserSettings.get_instance()
        assert a is b

    def test_valores_por_defecto(self):
        settings = UserSettings()
        assert settings.get("ui.language") == "es"
        assert settings.get("ui.theme") == "light"
        assert settings.get("ui.font_size") == 10
        assert settings.get("ui.show_grid") is True
        assert settings.get("ui.snap_to_grid") is False

    def test_valores_por_defecto_window(self):
        settings = UserSettings()
        assert settings.get("window.width") == 1280
        assert settings.get("window.height") == 800
        assert settings.get("window.maximized") is False

    def test_valores_por_defecto_recent_files(self):
        settings = UserSettings()
        assert settings.get("recent_files") == []

    def test_valores_por_defecto_last_project(self):
        settings = UserSettings()
        assert settings.get("last_project") == ""

    def test_get_default(self):
        settings = UserSettings()
        assert settings.get("no.existe", "fallback") == "fallback"

    def test_get_default_none(self):
        settings = UserSettings()
        assert settings.get("no.existe") is None

    def test_set_y_get(self):
        settings = UserSettings()
        settings.set("custom.test", "valor")
        assert settings.get("custom.test") == "valor"

    def test_set_anidado(self):
        settings = UserSettings()
        settings.set("a.b.c", 123)
        assert settings.get("a.b.c") == 123

    def test_persistencia_en_memoria(self):
        settings = UserSettings()
        settings.set("test.key", "memoria")
        assert settings.get("test.key") == "memoria"

    def test_add_recent_file(self):
        settings = UserSettings()
        settings._data["recent_files"] = []
        settings.add_recent_file("ruta/archivo.linpro")
        settings.add_recent_file("ruta/archivo.linpro")
        recent = settings.get("recent_files")
        assert len(recent) == 1

    def test_add_recent_file_duplicado_se_mueve_al_inicio(self):
        settings = UserSettings()
        settings._data["recent_files"] = []
        settings.add_recent_file("archivo1.linpro")
        settings.add_recent_file("archivo2.linpro")
        settings.add_recent_file("archivo1.linpro")
        recent = settings.get("recent_files")
        assert len(recent) == 2
        assert recent[0] == "archivo1.linpro"
        assert recent[1] == "archivo2.linpro"