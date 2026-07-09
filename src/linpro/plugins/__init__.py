"""Sistema de plugins de LINPRO.

Los plugins son módulos independientes que extienden la funcionalidad
del Core. Cada plugin se descubre automáticamente en los directorios
configurados.

Uso:
    manager = PluginManager.get_instance()
    manager.discover()
    manager.load("catastro")
    manager.run_all(project)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from linpro.exceptions import PluginError


@dataclass
class PluginInfo:
    name: str
    version: str
    description: str = ""
    author: str = ""
    dependencies: List[str] = field(default_factory=list)


class BasePlugin(ABC):
    """Clase base que todo plugin debe implementar."""

    @abstractmethod
    def get_info(self) -> PluginInfo:
        ...

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def execute(self, project: Any, **kwargs: Any) -> Dict[str, Any]:
        ...

    def shutdown(self) -> None:
        ...


class PluginManager:
    _instance: Optional["PluginManager"] = None

    def __init__(self) -> None:
        self._plugins: Dict[str, BasePlugin] = {}
        self._search_paths: List[Path] = []

    @classmethod
    def get_instance(cls) -> "PluginManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_search_path(self, path: Path) -> None:
        if path.exists() and path not in self._search_paths:
            self._search_paths.append(path)

    def discover(self) -> List[PluginInfo]:
        discovered = []
        for search_path in self._search_paths:
            if not search_path.exists():
                continue
            for plugin_dir in search_path.iterdir():
                if not plugin_dir.is_dir() or plugin_dir.name.startswith("_"):
                    continue
                init_file = plugin_dir / "__init__.py"
                if init_file.exists():
                    try:
                        self._load_plugin(plugin_dir.name, plugin_dir)
                        info = self._plugins[plugin_dir.name].get_info()
                        discovered.append(info)
                    except Exception as e:
                        raise PluginError(f"Error descubriendo plugin '{plugin_dir.name}': {e}") from e
        return discovered

    def _load_plugin(self, name: str, path: Path) -> None:
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location(name, path / "__init__.py")
        if spec is None or spec.loader is None:
            raise PluginError(f"No se pudo cargar el plugin '{name}'")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        if hasattr(module, "Plugin"):
            plugin_instance = module.Plugin()
            self._plugins[name] = plugin_instance
            plugin_instance.initialize()

    def load(self, name: str) -> bool:
        if name in self._plugins:
            return True
        for search_path in self._search_paths:
            plugin_path = search_path / name
            if plugin_path.exists() and (plugin_path / "__init__.py").exists():
                self._load_plugin(name, plugin_path)
                return True
        return False

    def unload(self, name: str) -> None:
        if name in self._plugins:
            self._plugins[name].shutdown()
            del self._plugins[name]

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        return self._plugins.get(name)

    def run_all(self, project: Any, **kwargs: Any) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        for name, plugin in self._plugins.items():
            results[name] = plugin.execute(project, **kwargs)
        return results

    def list_plugins(self) -> List[str]:
        return list(self._plugins.keys())