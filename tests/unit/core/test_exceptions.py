"""Tests para el sistema de excepciones de LINPRO."""

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


class TestLINPROError:
    def test_es_base_de_todas(self):
        assert issubclass(ProjectError, LINPROError)
        assert issubclass(ConfigError, LINPROError)
        assert issubclass(PluginError, LINPROError)
        assert issubclass(EventError, LINPROError)
        assert issubclass(LogError, LINPROError)
        assert issubclass(SettingsError, LINPROError)
        assert issubclass(VersionError, LINPROError)
        assert issubclass(WorkspaceError, LINPROError)

    def test_hereda_de_exception(self):
        assert issubclass(LINPROError, Exception)

    def test_mensaje_personalizado(self):
        msg = "Error de prueba"
        err = LINPROError(msg)
        assert str(err) == msg

    def test_mensaje_personalizado_en_subclases(self):
        msg = "Error del proyecto"
        err = ProjectError(msg)
        assert str(err) == msg

    def test_project_error_es_linpro_error(self):
        assert isinstance(ProjectError("proyecto"), LINPROError)

    def test_config_error_es_linpro_error(self):
        assert isinstance(ConfigError("config"), LINPROError)

    def test_plugin_error_es_linpro_error(self):
        assert isinstance(PluginError("plugin"), LINPROError)

    def test_event_error_es_linpro_error(self):
        assert isinstance(EventError("evento"), LINPROError)

    def test_log_error_es_linpro_error(self):
        assert isinstance(LogError("log"), LINPROError)

    def test_settings_error_es_linpro_error(self):
        assert isinstance(SettingsError("settings"), LINPROError)

    def test_version_error_es_linpro_error(self):
        assert isinstance(VersionError("version"), LINPROError)

    def test_workspace_error_es_linpro_error(self):
        assert isinstance(WorkspaceError("workspace"), LINPROError)