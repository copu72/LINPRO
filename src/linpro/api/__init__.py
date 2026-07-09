"""API pública de LINPRO.

Toda la aplicación habla con la API. Ningún módulo externo
se comunica directamente con los módulos internos.

La API expone los casos de uso del programa y orquesta
los servicios, modelos, y el Core.
"""

from linpro.core import (
    LINPROApp,
    Configuration,
    EventBus,
    Event,
    LINPROLogger,
    LogLevel,
    PluginManager,
    BasePlugin,
    PluginInfo,
    Workspace,
    UserSettings,
    get_version,
    get_version_info,
    LINPROError,
    ProjectError,
    ConfigError,
    PluginError,
)
from linpro.models import (
    Project,
    Alignment,
    Municipality,
    Parcel,
    Road,
    River,
    Infrastructure,
    AnalysisResult,
)

__all__ = [
    "LINPROApp",
    "Configuration",
    "EventBus",
    "Event",
    "LINPROLogger",
    "LogLevel",
    "PluginManager",
    "BasePlugin",
    "PluginInfo",
    "Workspace",
    "UserSettings",
    "get_version",
    "get_version_info",
    "LINPROError",
    "ProjectError",
    "ConfigError",
    "PluginError",
    "Project",
    "Alignment",
    "Municipality",
    "Parcel",
    "Road",
    "River",
    "Infrastructure",
    "AnalysisResult",
]