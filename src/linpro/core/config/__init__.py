"""Sistema de configuración de LINPRO.

Carga configuración por defecto (YAML) y permite fusionarla
con configuración de usuario y de proyecto.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from linpro.core.exceptions import ConfigError

DEFAULT_CONFIG: Dict[str, Any] = {
    "project": {
        "author": "",
        "company": "",
        "default_epsg": 25830,
        "default_crs": "EPSG:25830",
    },
    "core": {
        "log_level": "INFO",
        "log_file": "linpro.log",
        "console_output": True,
        "file_output": False,
        "event_bus_enabled": True,
    },
    "geometry": {
        "pk_precision": 3,
        "buffer_segments": 8,
        "min_tangent_length": 0.001,
    },
    "analysis": {
        "municipalities": True,
        "cadastre": True,
        "roads": True,
        "rivers": True,
        "infrastructure": True,
    },
    "export": {
        "excel_template": "default.xlsx",
        "dxf_version": "AC1027",
        "pdf_orientation": "landscape",
    },
    "gis": {
        "cache_enabled": True,
        "cache_expiry_days": 30,
        "download_timeout_seconds": 60,
        "wfs_max_features": 5000,
    },
}


class Configuration:
    _instance: Optional["Configuration"] = None

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
        self._load_defaults()

    @classmethod
    def get_instance(cls) -> "Configuration":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_defaults(self) -> None:
        self._data = DEFAULT_CONFIG.copy()

    def load_file(self, path: Path) -> None:
        if not path.exists():
            raise ConfigError(f"Archivo de configuración no encontrado: {path}")
        try:
            import yaml
            with open(path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f)
            if user_config:
                self._merge(user_config)
        except ImportError:
            raise ConfigError("Se necesita PyYAML para cargar configuraciones YAML")
        except Exception as e:
            raise ConfigError(f"Error al cargar configuración: {e}") from e

    def _merge(self, user_config: Dict[str, Any]) -> None:
        for key, value in user_config.items():
            if key in self._data and isinstance(self._data[key], dict) and isinstance(value, dict):
                self._data[key].update(value)
            else:
                self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        keys = key.split(".")
        target = self._data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        import copy
        return copy.deepcopy(self._data)

    def save(self, path: Path) -> None:
        try:
            import yaml
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(self._data, f, default_flow_style=False, allow_unicode=True)
        except ImportError:
            raise ConfigError("Se necesita PyYAML para guardar configuraciones YAML")
