# Clases del Core de LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09

---

## LINPROApp

**Módulo:** `linpro.app`  
**Tipo:** Singleton — `get_instance()`  
**Propósito:** Fachada principal de la aplicación. Orquesta el ciclo de vida completo: inicio, configuración, logging, plugins y cierre.

| Método / Propiedad     | Descripción |
|------------------------|-------------|
| `get_instance()`       | Devuelve la única instancia de la aplicación |
| `start()`              | Inicializa todos los subsistemas en orden |
| `stop()`               | Detiene plugins y publica eventos de cierre |
| `is_running`           | `True` si la aplicación está en ejecución |
| `logger`               | Instancia compartida de `LINPROLogger` |
| `config`               | Instancia compartida de `Configuration` |
| `settings`             | Instancia compartida de `UserSettings` |
| `event_bus`            | Instancia compartida de `EventBus` |
| `plugin_manager`       | Instancia compartida de `PluginManager` |
| `workspace`            | Instancia compartida de `Workspace` |

---

## Configuration

**Módulo:** `linpro.config`  
**Tipo:** Singleton — `get_instance()`  
**Propósito:** Gestiona la configuración global de LINPRO. Almacena valores por defecto en un diccionario interno y permite fusionar configuración de usuario desde archivos YAML.

| Método / Propiedad | Descripción |
|---------------------|-------------|
| `get_instance()`    | Devuelve la única instancia de configuración |
| `load_file(path)`   | Carga un archivo YAML y lo fusiona con los valores actuales |
| `get(key, default)` | Obtiene un valor por clave anidada (ej. `"project.default_epsg"`) |
| `set(key, value)`   | Establece un valor por clave anidada |
| `to_dict()`         | Devuelve una copia del diccionario interno de configuración |
| `save(path)`        | Guarda la configuración actual en un archivo YAML |

**Secciones de configuración por defecto:** `project`, `core`, `geometry`, `analysis`, `export`, `gis`.

---

## EventBus

**Módulo:** `linpro.events`  
**Tipo:** Singleton — `get_instance()`  
**Propósito:** Bus de eventos que implementa el patrón publicador-subscriptor. Permite comunicación desacoplada entre módulos.

| Método          | Descripción |
|-----------------|-------------|
| `get_instance()`| Devuelve la única instancia del bus |
| `subscribe(name, handler)` | Suscribe un manejador a un evento |
| `unsubscribe(name, handler)` | Elimina una suscripción existente |
| `publish(event)` | Publica un evento, ejecutando todos los manejadores suscritos |
| `clear()`       | Elimina todas las suscripciones |

---

## Event

**Módulo:** `linpro.events`  
**Tipo:** `@dataclass`  
**Propósito:** Representa un evento dentro del bus. Contiene el nombre, datos asociados, timestamp y origen.

| Campo       | Tipo         | Descripción |
|-------------|--------------|-------------|
| `name`      | `str`        | Nombre del evento (ej. `"core.started"`) |
| `data`      | `Dict[str, Any]` | Datos adicionales del evento |
| `timestamp` | `datetime`   | Momento en que se creó el evento |
| `source`    | `str`        | Identificador del módulo que emitió el evento |

---

## PluginManager

**Módulo:** `linpro.plugins`  
**Tipo:** Singleton — `get_instance()`  
**Propósito:** Descubre, carga, ejecuta y descarga plugins dinámicamente.

| Método              | Descripción |
|---------------------|-------------|
| `get_instance()`    | Devuelve la única instancia del gestor |
| `add_search_path(path)` | Agrega un directorio donde buscar plugins |
| `discover()`        | Escanea los directorios de búsqueda y carga todos los plugins encontrados |
| `load(name)`        | Carga un plugin específico por nombre |
| `unload(name)`      | Descarga un plugin (llama a `shutdown()` y lo elimina) |
| `get_plugin(name)`  | Obtiene la instancia de un plugin cargado |
| `run_all(project, **kwargs)` | Ejecuta todos los plugins cargados sobre un proyecto |
| `list_plugins()`    | Devuelve la lista de nombres de plugins cargados |

---

## BasePlugin

**Módulo:** `linpro.plugins`  
**Tipo:** Clase base abstracta (`ABC`)  
**Propósito:** Define la interfaz que todo plugin debe implementar.

| Método         | Descripción |
|----------------|-------------|
| `get_info()`   | Devuelve un `PluginInfo` con metadatos del plugin |
| `initialize()` | Inicializa el plugin (recursos, conexiones, etc.) |
| `execute(project, **kwargs)` | Ejecuta la lógica principal del plugin |
| `shutdown()`   | Libera recursos (opcional, no abstracto) |

---

## PluginInfo

**Módulo:** `linpro.plugins`  
**Tipo:** `@dataclass`  
**Propósito:** Metadatos de un plugin.

| Campo          | Tipo         | Descripción |
|----------------|--------------|-------------|
| `name`         | `str`        | Nombre único del plugin |
| `version`      | `str`        | Versión del plugin |
| `description`  | `str`        | Descripción breve |
| `author`       | `str`        | Autor del plugin |
| `dependencies` | `List[str]`  | Lista de dependencias |

---

## Project

**Módulo:** `linpro.project`  
**Propósito:** Objeto central de datos de LINPRO. Todo módulo lee y escribe datos en él. Contiene metadatos, estado interno y un diccionario genérico de datos.

| Método / Propiedad | Descripción |
|---------------------|-------------|
| `__init__(name)`    | Crea un proyecto con nombre y metadatos por defecto |
| `metadata`          | `ProjectMetadata` del proyecto |
| `state`             | `ProjectState` del proyecto |
| `path`              | Ruta del archivo de proyecto (get/set) |
| `set_data(key, value)` | Almacena un valor en el diccionario interno |
| `get_data(key, default)` | Recupera un valor del diccionario interno |
| `mark_loaded()`     | Marca el proyecto como cargado y no modificado |
| `mark_saved()`      | Marca el proyecto como no modificado |
| `to_dict()`         | Convierte el proyecto a diccionario serializable |
| `from_dict(data)`   | Crea un proyecto desde un diccionario (classmethod) |

---

## Workspace

**Módulo:** `linpro.project`  
**Tipo:** Singleton — `get_instance()`  
**Propósito:** Gestiona el espacio de trabajo: proyecto actual y lista de proyectos abiertos.

| Método / Propiedad | Descripción |
|---------------------|-------------|
| `get_instance()`    | Devuelve la única instancia del workspace |
| `current_project`   | Proyecto activo actual (o `None`) |
| `open_project(project)` | Abre un proyecto y lo establece como activo |
| `close_project()`   | Cierra el proyecto activo |
| `list_open_projects()` | Lista todos los proyectos abiertos |

---

## ProjectMetadata

**Módulo:** `linpro.project`  
**Tipo:** `@dataclass`  
**Propósito:** Metadatos descriptivos de un proyecto LINPRO.

| Campo       | Tipo       | Descripción |
|-------------|------------|-------------|
| `name`      | `str`      | Nombre del proyecto |
| `description` | `str`    | Descripción |
| `author`    | `str`      | Autor del proyecto |
| `company`   | `str`      | Compañía o entidad |
| `created`   | `datetime` | Fecha de creación |
| `modified`  | `datetime` | Fecha de última modificación |
| `version`   | `str`      | Versión del proyecto (semver) |
| `epsg`      | `int`      | Código EPSG del sistema de referencia (default: 25830) |

---

## ProjectState

**Módulo:** `linpro.project`  
**Tipo:** `@dataclass`  
**Propósito:** Estado operativo del proyecto.

| Campo             | Tipo      | Descripción |
|-------------------|-----------|-------------|
| `is_dirty`        | `bool`    | `True` si hay cambios sin guardar |
| `is_loaded`       | `bool`    | `True` si el proyecto está cargado desde archivo |
| `has_alignment`   | `bool`    | `True` si tiene un trazado definido |
| `has_analysis`    | `bool`    | `True` si se ha ejecutado algún análisis |
| `has_results`     | `bool`    | `True` si hay resultados disponibles |

---

## UserSettings

**Módulo:** `linpro.settings`  
**Tipo:** Singleton — `get_instance()`  
**Propósito:** Preferencias de usuario persistentes en JSON (idioma, tema, tamaño de ventana, archivos recientes).

| Método / Propiedad | Descripción |
|---------------------|-------------|
| `get_instance()`    | Devuelve la única instancia de preferencias |
| `load(path)`        | Carga preferencias desde un archivo JSON |
| `save()`            | Guarda las preferencias actuales a JSON |
| `get(key, default)` | Obtiene un valor por clave anidada |
| `set(key, value)`   | Establece un valor y guarda automáticamente |
| `add_recent_file(path)` | Agrega una ruta a la lista de archivos recientes |

---

## LINPROLogger

**Módulo:** `linpro.logging`  
**Tipo:** Singleton — `get_instance()`  
**Propósito:** Logger profesional con formato consistente. Soporta salida a consola y archivo con rotación de niveles.

| Método / Propiedad | Descripción |
|---------------------|-------------|
| `get_instance()`    | Devuelve la única instancia del logger |
| `set_file_output(path)` | Habilita salida a archivo |
| `set_level(level)`  | Cambia el nivel de logging |
| `debug(msg)`        | Registra mensaje de depuración |
| `info(msg)`         | Registra mensaje informativo |
| `warning(msg)`      | Registra advertencia |
| `error(msg)`        | Registra error |
| `critical(msg)`     | Registra error crítico |
| `name`              | Nombre del logger |

---

## LogLevel

**Módulo:** `linpro.logging`  
**Tipo:** `Enum`  
**Propósito:** Niveles de logging estándar.

| Miembro    | Valor | Descripción |
|------------|-------|-------------|
| `DEBUG`    | 10    | Información detallada para depuración |
| `INFO`     | 20    | Mensajes informativos generales |
| `WARNING`  | 30    | Advertencias que no impiden la ejecución |
| `ERROR`    | 40    | Errores recuperables |
| `CRITICAL` | 50    | Errores fatales |

---

## VersionInfo

**Módulo:** `linpro.version`  
**Tipo:** `@dataclass`  
**Propósito:** Información estructurada de versión.

| Campo    | Tipo  | Descripción |
|----------|-------|-------------|
| `major`  | `int` | Versión mayor |
| `minor`  | `int` | Versión menor |
| `patch`  | `int` | Parche |
| `suffix` | `str` | Sufijo opcional (`"alpha"`, `"beta"`, `"rc1"`) |
| `string` | `str` | Representación completa (ej. `"0.1.0"`) |

---

## Jerarquía de excepciones

**Módulo:** `linpro.exceptions`

| Clase            | Hereda de      | Propósito |
|------------------|----------------|-----------|
| `LINPROError`    | `Exception`    | Base de todas las excepciones de LINPRO |
| `ProjectError`   | `LINPROError`  | Error en operaciones de proyecto |
| `ConfigError`    | `LINPROError`  | Error en configuración |
| `PluginError`    | `LINPROError`  | Error en el sistema de plugins |
| `EventError`     | `LINPROError`  | Error en el bus de eventos |
| `LogError`       | `LINPROError`  | Error en el sistema de logging |
| `SettingsError`  | `LINPROError`  | Error en preferencias de usuario |
| `VersionError`   | `LINPROError`  | Error en versionado |
| `WorkspaceError` | `LINPROError`  | Error en el workspace |

---

## Funciones auxiliares

**Módulo:** `linpro.version`

| Función              | Descripción |
|----------------------|-------------|
| `get_version()`      | Devuelve un objeto `VersionInfo` con la versión actual |
| `get_version_info()` | Devuelve un string formateado (ej. `"LINPRO Professional v0.1.0"`) |
| `compare_versions(v1, v2)` | Compara dos versiones semver. Devuelve `-1`, `0` o `1` |
