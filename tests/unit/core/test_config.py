"""Tests para el sistema de configuración de LINPRO."""

from linpro.core.config import Configuration, DEFAULT_CONFIG


class TestConfiguration:
    def test_singleton(self):
        a = Configuration.get_instance()
        b = Configuration.get_instance()
        assert a is b

    def test_valores_por_defecto(self):
        config = Configuration.get_instance()
        assert config.get("project.author") == ""
        assert config.get("project.default_epsg") == 25830

    def test_get_clave_simple(self):
        config = Configuration()
        assert config.get("export.pdf_orientation") == "landscape"

    def test_get_clave_anidada(self):
        config = Configuration()
        assert config.get("core.log_level") == "INFO"
        assert config.get("core.event_bus_enabled") is True

    def test_get_default_devuelve_default(self):
        config = Configuration()
        assert config.get("clave.inexistente", "fallback") == "fallback"

    def test_get_default_none(self):
        config = Configuration()
        assert config.get("clave.inexistente") is None

    def test_set_y_get(self):
        config = Configuration()
        config.set("custom.key", "valor")
        assert config.get("custom.key") == "valor"

    def test_set_anidado(self):
        config = Configuration()
        config.set("nivel1.nivel2.nivel3", 42)
        assert config.get("nivel1.nivel2.nivel3") == 42

    def test_persistencia_en_memoria(self):
        config = Configuration()
        config.set("test.valor", "persistente")
        assert config.get("test.valor") == "persistente"

    def test_default_config_tiene_claves_esperadas(self):
        assert "project" in DEFAULT_CONFIG
        assert "core" in DEFAULT_CONFIG
        assert "geometry" in DEFAULT_CONFIG
        assert "analysis" in DEFAULT_CONFIG
        assert "export" in DEFAULT_CONFIG
        assert "gis" in DEFAULT_CONFIG

    def test_set_sobrescribe_default(self):
        config = Configuration()
        config.set("project.default_epsg", 4326)
        assert config.get("project.default_epsg") == 4326

    def test_to_dict_devuelve_copia(self):
        Configuration._instance = None
        config = Configuration.get_instance()
        original = config.get("project.default_epsg")
        d = config.to_dict()
        d["project"]["default_epsg"] = 9999
        assert config.get("project.default_epsg") == original