\"\"\"Sistema de plugins de LINPRO.

Cada plugin es un módulo independiente que puede cargarse dinámicamente.
Para crear un nuevo plugin, crear una carpeta en plugins/ con:
- __init__.py con la clase Plugin que hereda de BasePlugin
- plugin.yaml con metadatos (nombre, versión, autor, dependencias)
\"\"\"

import importlib
import pkgutil
from pathlib import Path
from typing import Optional


__all__: list[str] = []


def discover_plugins() -> list[str]:
    return [name for _, name, _ in pkgutil.iter_modules([str(Path(__file__).parent)]) if name != "__init__"]


def load_plugin(name: str) -> Optional[object]:
    try:
        module = importlib.import_module(f"linpro.plugins.{name}")
        if hasattr(module, "Plugin"):
            return module.Plugin()
    except ImportError:
        return None
    return None
