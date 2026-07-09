"""LINPRO Core — Núcleo unificado.

Todos los módulos del Core están bajo este paquete:
app, config, events, exceptions, logging, plugins, project,
settings, version, utils.

No debe haber ningún otro módulo de Core fuera de aquí.
"""

from linpro.core.app import LINPROApp
from linpro.core.config import Configuration
from linpro.core.events import EventBus, Event
from linpro.core.exceptions import (
    LINPROError,
    ProjectError,
    ConfigError,
    PluginError,
    EventError,
    LogError,
    SettingsError,
    VersionError,
    WorkspaceError,
)
from linpro.core.logging import LINPROLogger, LogLevel
from linpro.core.plugins import PluginManager, BasePlugin, PluginInfo
from linpro.core.project import Project, Workspace, ProjectMetadata, ProjectState
from linpro.core.settings import UserSettings
from linpro.core.version import get_version, get_version_info, compare_versions, VersionInfo

__all__ = [
    "LINPROApp",
    "Configuration",
    "EventBus",
    "Event",
    "LINPROError",
    "ProjectError",
    "ConfigError",
    "PluginError",
    "EventError",
    "LogError",
    "SettingsError",
    "VersionError",
    "WorkspaceError",
    "LINPROLogger",
    "LogLevel",
    "PluginManager",
    "BasePlugin",
    "PluginInfo",
    "Project",
    "Workspace",
    "ProjectMetadata",
    "ProjectState",
    "UserSettings",
    "get_version",
    "get_version_info",
    "compare_versions",
    "VersionInfo",
]