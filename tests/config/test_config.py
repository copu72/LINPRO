"""Tests para el sistema de configuración de LINPRO."""

import pytest
from linpro.config import Configuration
from linpro.exceptions import ConfigError


class TestConfiguration:
    def setup_method(self):
        Configuration._instance = None

    def test_singleton(self):
        cfg1 = Configuration.get_instance()
        cfg2 = Configuration.get_instance()
        assert cfg1 is cfg2

    def test_get_instance_devuelve_siempre_la_misma(self):
        Configuration._instance = None
        cfg = Configuration.get_instance()
        assert cfg is Configuration.get_instance()

    def test_get_clave_simple(self):
        cfg = Configuration.get_instance()
        assert cfg.get("core.log_level") == "INFO"

    def test_get_clave_anidada(self):
        cfg = Configuration.get_instance()
        assert cfg.get("project.default_epsg") == 25830

    def test_get_clave_inexistente_devuelve_default(self):
        cfg = Configuration.get_instance()
        assert cfg.get("clave.inexistente", "valor_default") == "valor_default"

    def test_get_clave_inexistente_sin_default_devuelve_none(self):
        cfg = Configuration.get_instance()
        assert cfg.get("clave.inexistente") is None

    def test_set_y_get_verifica_persistencia(self):
        cfg = Configuration.get_instance()
        cfg.set("prueba.valor", 42)
        assert cfg.get("prueba.valor") == 42

    def test_set_crea_claves_anidadas(self):
        cfg = Configuration.get_instance()
        cfg.set("nivel1.nivel2.nivel3", "profundo")
        assert cfg.get("nivel1.nivel2.nivel3") == "profundo"

    def test_set_sobrescribe_valor_existente(self):
        cfg = Configuration.get_instance()
        cfg.set("core.log_level", "DEBUG")
        assert cfg.get("core.log_level") == "DEBUG"

    def test_valores_por_defecto_del_config(self):
        cfg = Configuration.get_instance()
        assert cfg.get("project.author") == ""
        assert cfg.get("project.company") == ""
        assert cfg.get("geometry.pk_precision") == 3
        assert cfg.get("analysis.municipalities") is True
        assert cfg.get("export.dxf_version") == "AC1027"
        assert cfg.get("gis.cache_enabled") is True

    def test_to_dict_es_copia_independiente(self):
        cfg = Configuration.get_instance()
        d = cfg.to_dict()
        d["core"] = {"log_level": "MODIFICADO"}
        assert cfg.get("core.log_level") != "MODIFICADO", "to_dict debe devolver una copia"

    def test_dos_instancias_comparten_mismo_estado(self):
        Configuration._instance = None
        cfg_a = Configuration.get_instance()
        cfg_a.set("compartida.clave", "valor_compartido")
        cfg_b = Configuration.get_instance()
        assert cfg_b.get("compartida.clave") == "valor_compartido"