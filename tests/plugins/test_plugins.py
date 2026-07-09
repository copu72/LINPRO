"""Tests para el sistema de plugins de LINPRO."""

import pytest
from pathlib import Path
from linpro.plugins import PluginManager, PluginInfo, BasePlugin
from linpro.exceptions import PluginError


class TestPluginInfo:
    def test_dataclass_campos_obligatorios(self):
        info = PluginInfo(name="catastro", version="1.0.0")
        assert info.name == "catastro"
        assert info.version == "1.0.0"

    def test_dataclass_campos_opcionales(self):
        info = PluginInfo(
            name="catastro",
            version="1.0.0",
            description="Plugin de catastro",
            author="LINPRO Team",
            dependencies=["numpy"],
        )
        assert info.description == "Plugin de catastro"
        assert info.author == "LINPRO Team"
        assert info.dependencies == ["numpy"]

    def test_dataclass_valores_por_defecto(self):
        info = PluginInfo(name="test", version="0.1.0")
        assert info.description == ""
        assert info.author == ""
        assert info.dependencies == []


class TestPluginManager:
    def setup_method(self):
        PluginManager._instance = None

    def test_singleton(self):
        pm1 = PluginManager.get_instance()
        pm2 = PluginManager.get_instance()
        assert pm1 is pm2

    def test_get_instance_devuelve_siempre_la_misma(self):
        PluginManager._instance = None
        pm = PluginManager.get_instance()
        assert pm is PluginManager.get_instance()

    def test_list_plugins_inicial_vacia(self):
        pm = PluginManager.get_instance()
        assert pm.list_plugins() == []

    def test_add_search_path_ruta_existente(self):
        pm = PluginManager.get_instance()
        pm.add_search_path(Path("."))
        assert len(pm._search_paths) == 1

    def test_add_search_path_ruta_inexistente_no_se_agrega(self):
        pm = PluginManager.get_instance()
        pm.add_search_path(Path("/ruta/inexistente/plugin"))
        assert len(pm._search_paths) == 0

    def test_add_search_path_no_duplica_rutas(self):
        pm = PluginManager.get_instance()
        pm.add_search_path(Path("."))
        pm.add_search_path(Path("."))
        assert len(pm._search_paths) == 1

    def test_get_plugin_devuelve_none_si_no_existe(self):
        pm = PluginManager.get_instance()
        assert pm.get_plugin("plugin_inexistente") is None