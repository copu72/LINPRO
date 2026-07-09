"""LINPRO Core — Fachada pública del núcleo.

Este módulo expone las clases y funciones principales del Core.
Todo lo que un módulo externo necesita está aquí.
"""

from linpro.app import LINPROApp
from linpro.config import Configuration
from linpro.events import EventBus, Event
from linpro.exceptions import LINPROError, ProjectError, ConfigError, PluginError
from linpro.logging import LINPROLogger, LogLevel
from linpro.plugins import PluginManager, BasePlugin, PluginInfo
from linpro.project import Project, Workspace, ProjectMetadata, ProjectState
from linpro.settings import UserSettings
from linpro.version import get_version, get_version_info, compare_versions

__all__ = [
    "LINPROApp",
    "Configuration",
    "EventBus",
    "Event",
    "LINPROError",
    "ProjectError",
    "ConfigError",
    "PluginError",
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
]