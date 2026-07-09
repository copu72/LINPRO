# Módulo Core de LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Estado:** Estable

---

## Propósito

El módulo **Core** es el corazón de la plataforma **LINPRO (Ingeniería Lineal Profesional)**. Proporciona los servicios fundamentales sobre los que se construyen todos los demás módulos: gestión del ciclo de vida de la aplicación, configuración global, logging, bus de eventos, sistema de plugins, gestión de proyectos y preferencias de usuario.

El Core es la primera capa que se inicia al ejecutar LINPRO y la última que se detiene al cerrar. Ningún otro módulo puede funcionar sin él.

## Dependencias

El Core **no tiene dependencias internas** dentro de LINPRO. Es el módulo base y todos los demás módulos dependen de él.

Dependencias externas:
- `PyYAML` — carga/guardado de configuraciones en formato YAML (opcional en tiempo de ejecución).

## Estructura del módulo

| Submódulo     | Descripción |
|---------------|-------------|
| `app`         | Punto de entrada: clase `LINPROApp`, ciclo de vida de la aplicación |
| `config`      | Sistema de configuración con defaults en YAML y fusión jerárquica |
| `events`      | Bus de eventos desacoplado para comunicación entre módulos |
| `exceptions`  | Jerarquía de excepciones base del sistema |
| `logging`     | Logger profesional con formato consistente, archivo y consola |
| `plugins`     | Sistema de descubrimiento y carga dinámica de plugins |
| `project`     | Clase `Project` (objeto central), `Workspace` y data classes auxiliares |
| `settings`    | Preferencias de usuario persistidas en JSON |
| `version`     | Información de versión semver, comparación y funciones de consulta |

## Fachada pública (`linpro/core/__init__.py`)

El Core expone una API unificada a través de `linpro.core`. Todo lo que un módulo externo necesita del núcleo se importa desde este único punto:

```python
from linpro.core import (
    LINPROApp, Configuration, EventBus, Event,
    LINPROError, ProjectError, ConfigError, PluginError,
    LINPROLogger, LogLevel,
    PluginManager, BasePlugin, PluginInfo,
    Project, Workspace, ProjectMetadata, ProjectState,
    UserSettings,
    get_version, get_version_info, compare_versions,
)
```

## Uso básico

```python
from linpro.core import LINPROApp

app = LINPROApp.get_instance()
app.start()

print(app.config.get("project.default_epsg"))  # 25830
print(app.logger)                               # LINPROLogger

app.stop()
```

## Pruebas

El Core cuenta con **109 tests unitarios** distribuidos en 8 archivos, ejecutables con `pytest` desde la raíz del proyecto:

```bash
pytest tests/
```
