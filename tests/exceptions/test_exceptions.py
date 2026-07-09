"""Tests para el sistema de excepciones de LINPRO."""

import pytest
from linpro.exceptions import (
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
    def test_es_excepcion_base(self):
        assert issubclass(LINPROError, Exception)

    def test_mensaje_personalizado(self):
        mensaje = "Error crítico en el sistema"
        with pytest.raises(LINPROError, match=mensaje):
            raise LINPROError(mensaje)

    def test_mensaje_predeterminado(self):
        with pytest.raises(LINPROError) as exc_info:
            raise LINPROError()
        assert str(exc_info.value) == ""


class TestProjectError:
    def test_hereda_de_linproerror(self):
        assert issubclass(ProjectError, LINPROError)
        assert issubclass(ProjectError, Exception)

    def test_mensaje_personalizado(self):
        mensaje = "Proyecto no encontrado"
        with pytest.raises(ProjectError, match=mensaje):
            raise ProjectError(mensaje)


class TestConfigError:
    def test_hereda_de_linproerror(self):
        assert issubclass(ConfigError, LINPROError)

    def test_mensaje_personalizado(self):
        mensaje = "Configuración inválida"
        with pytest.raises(ConfigError, match=mensaje):
            raise ConfigError(mensaje)


class TestPluginError:
    def test_hereda_de_linproerror(self):
        assert issubclass(PluginError, LINPROError)

    def test_mensaje_personalizado(self):
        mensaje = "Plugin no compatible"
        with pytest.raises(PluginError, match=mensaje):
            raise PluginError(mensaje)


class TestOtrasExcepciones:
    def test_event_error_hereda(self):
        assert issubclass(EventError, LINPROError)

    def test_log_error_hereda(self):
        assert issubclass(LogError, LINPROError)

    def test_settings_error_hereda(self):
        assert issubclass(SettingsError, LINPROError)

    def test_version_error_hereda(self):
        assert issubclass(VersionError, LINPROError)

    def test_workspace_error_hereda(self):
        assert issubclass(WorkspaceError, LINPROError)