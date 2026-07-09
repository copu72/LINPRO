"""Preferencias de usuario de LINPRO.

Las preferencias se almacenan en un archivo JSON en el directorio
de configuración del usuario. Son independientes de la configuración
del proyecto.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from linpro.exceptions import SettingsError


_DEFAULT_SETTINGS: Dict[str, Any] = {
    "ui": {
        "language": "es",
        "theme": "light",
        "font_size": 10,
        "show_grid": True,
        "snap_to_grid": False,
    },
    "recent_files": [],
    "last_project": "",
    "window": {
        "width": 1280,
        "height": 800,
        "maximized": False,
    },
}


class UserSettings:
    _instance: Optional["UserSettings"] = None

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
        self._path: Optional[Path] = None
        self._load_defaults()

    @classmethod
    def get_instance(cls) -> "UserSettings":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_defaults(self) -> None:
        self._data = _DEFAULT_SETTINGS.copy()

    def load(self, path: Path) -> None:
        self._path = path
        if not path.exists():
            self.save()
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
            self._data.update(user_data)
        except json.JSONDecodeError as e:
            raise SettingsError(f"Error al leer preferencias: {e}") from e

    def save(self) -> None:
        if self._path is None:
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise SettingsError(f"Error al guardar preferencias: {e}") from e

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
        self.save()

    def add_recent_file(self, path: str) -> None:
        recent = self._data.get("recent_files", [])
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        self._data["recent_files"] = recent[:10]
        self.save()