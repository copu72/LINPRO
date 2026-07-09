"""Aplicación principal LINPRO.

LINPROApp gestiona el ciclo de vida completo de la aplicación:
inicialización, configuración, logging, plugins y cierre.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from linpro.core.config import Configuration
from linpro.core.events import EventBus, CORE_STARTING, CORE_STARTED, CORE_STOPPING, CORE_STOPPED, Event
from linpro.core.exceptions import LINPROError
from linpro.core.logging import LINPROLogger, LogLevel
from linpro.core.plugins import PluginManager
from linpro.core.project import Project, Workspace
from linpro.core.settings import UserSettings
from linpro.core.version import get_version, get_version_info


class LINPROApp:
    _instance: Optional["LINPROApp"] = None

    def __init__(self) -> None:
        self._is_running = False
        self._logger: Optional[LINPROLogger] = None
        self._config: Optional[Configuration] = None
        self._settings: Optional[UserSettings] = None
        self._event_bus: Optional[EventBus] = None
        self._plugin_manager: Optional[PluginManager] = None
        self._workspace: Optional[Workspace] = None

    @classmethod
    def get_instance(cls) -> "LINPROApp":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start(self) -> None:
        if self._is_running:
            return

        self._is_running = True
        version_info = get_version_info()
        print(f"\n{version_info}")
        print(f"{'=' * len(version_info)}\n")

        # 1. Logger
        self._logger = LINPROLogger.get_instance()
        self._logger.info("Core initialized")

        # 2. Configuration
        self._config = Configuration.get_instance()
        self._logger.info("Configuration loaded")

        # 3. Settings
        self._settings = UserSettings.get_instance()
        settings_path = self._get_settings_path()
        self._settings.load(settings_path)
        self._logger.info("User settings loaded")

        # 4. Event bus
        self._event_bus = EventBus.get_instance()
        self._logger.info("Event bus initialized")

        # 5. Plugin manager
        self._plugin_manager = PluginManager.get_instance()
        self._logger.info("Plugin manager initialized")

        # 6. Workspace
        self._workspace = Workspace.get_instance()
        self._logger.info("Workspace ready")

        # 7. Evento de inicio
        self._event_bus.publish(Event(name=CORE_STARTED, source="LINPROApp"))

        self._logger.info("LINPRO Professional started successfully")

    def stop(self) -> None:
        if not self._is_running:
            return

        self._logger.info("Shutting down LINPRO Professional...")
        self._event_bus.publish(Event(name=CORE_STOPPING, data={}))

        if self._plugin_manager:
            for plugin_name in self._plugin_manager.list_plugins():
                self._plugin_manager.unload(plugin_name)

        self._event_bus.publish(Event(name=CORE_STOPPED, data={}))
        self._is_running = False
        self._logger.info("LINPRO Professional stopped")

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def logger(self) -> Optional[LINPROLogger]:
        return self._logger

    @property
    def config(self) -> Configuration:
        if self._config is None:
            self._config = Configuration.get_instance()
        return self._config

    @property
    def settings(self) -> UserSettings:
        return self._settings

    @property
    def event_bus(self) -> EventBus:
        if self._event_bus is None:
            self._event_bus = EventBus.get_instance()
        return self._event_bus

    @property
    def plugin_manager(self) -> PluginManager:
        if self._plugin_manager is None:
            self._plugin_manager = PluginManager.get_instance()
        return self._plugin_manager

    @property
    def workspace(self) -> Workspace:
        if self._workspace is None:
            self._workspace = Workspace.get_instance()
        return self._workspace

    @staticmethod
    def _get_settings_path() -> Path:
        import os
        if os.name == "nt":
            base = Path(os.environ.get("APPDATA", Path.home() / ".config"))
        else:
            base = Path.home() / ".config"
        path = base / "linpro" / "settings.json"
        return path
