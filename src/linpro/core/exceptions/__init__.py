"""Excepciones base del sistema LINPRO.

Todas las excepciones personalizadas heredan de LINPROError.
"""


class LINPROError(Exception):
    """Excepción base de todo LINPRO."""


class ProjectError(LINPROError):
    """Error relacionado con el proyecto."""


class ConfigError(LINPROError):
    """Error en la configuración."""


class PluginError(LINPROError):
    """Error en el sistema de plugins."""


class EventError(LINPROError):
    """Error en el sistema de eventos."""


class LogError(LINPROError):
    """Error en el sistema de logging."""


class SettingsError(LINPROError):
    """Error en las preferencias de usuario."""


class VersionError(LINPROError):
    """Error en el sistema de versionado."""


class WorkspaceError(LINPROError):
    """Error en el workspace del proyecto."""
