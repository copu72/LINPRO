"""LINPRO — Ingeniería Lineal Profesional.

Plataforma Python modular para el análisis, diseño y gestión
de infraestructuras lineales.
"""

from linpro.core import (
    LINPROApp,
    Configuration,
    EventBus,
    Event,
    LINPROError,
    ProjectError,
    ConfigError,
    PluginError,
    LINPROLogger,
    LogLevel,
    PluginManager,
    BasePlugin,
    PluginInfo,
    Project,
    Workspace,
    ProjectMetadata,
    ProjectState,
    UserSettings,
    get_version,
    get_version_info,
    compare_versions,
)

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