"""Tests para el sistema de plugins de LINPRO."""

from pathlib import Path

from linpro.core.plugins import PluginManager, PluginInfo, BasePlugin


class TestPluginInfo:
    def test_dataclass_campos_obligatorios(self):
        info = PluginInfo(name="test", version="1.0.0")
        assert info.name == "test"
        assert info.version == "1.0.0"

    def test_dataclass_campos_opcionales(self):
        info = PluginInfo(name="test", version="1.0.0", description="desc", author="autor")
        assert info.description == "desc"
        assert info.author == "autor"
        assert info.dependencies == []

    def test_dataclass_con_dependencias(self):
        info = PluginInfo(name="test", version="1.0.0", dependencies=["base"])
        assert info.dependencies == ["base"]


class TestPluginManager:
    def test_singleton(self):
        a = PluginManager.get_instance()
        b = PluginManager.get_instance()
        assert a is b

    def test_add_search_path(self):
        manager = PluginManager()
        path = Path(".")
        manager.add_search_path(path)
        assert path in manager._search_paths

    def test_add_search_path_ignora_inexistente(self):
        manager = PluginManager()
        path = Path("/ruta/inexistente/xyz123")
        manager.add_search_path(path)
        assert path not in manager._search_paths

    def test_list_plugins_inicialmente_vacia(self):
        manager = PluginManager()
        assert manager.list_plugins() == []

    def test_get_plugin_devuelve_none_si_no_existe(self):
        manager = PluginManager()
        assert manager.get_plugin("no_existe") is None

    def test_list_plugins_despues_de_discover(self):
        manager = PluginManager()
        resultado = manager.list_plugins()
        assert isinstance(resultado, list)

    def test_base_plugin_es_abstracto(self):
        import inspect
        assert inspect.isabstract(BasePlugin)