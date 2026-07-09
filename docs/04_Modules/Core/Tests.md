# Tests del Core de LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09

---

## Estrategia de pruebas

Los tests del Core siguen una estrategia de **pruebas unitarias** con **pytest** como framework. Cada submódulo del Core tiene su propio archivo de tests dentro de `tests/`. No se utilizan dependencias externas de mocking; los tests crean instancias directas de las clases o utilizan los singletons según corresponda.

## Resumen de cobertura

El Core cuenta con **109 tests unitarios** distribuidos en 8 archivos:

| Archivo de tests           | Módulo bajo prueba   | Tests | Cobertura |
|----------------------------|----------------------|-------|-----------|
| `tests/app/test_app.py`    | `linpro.app`         | 8     | Ciclo de vida de LINPROApp, propiedades, singleton |
| `tests/config/test_config.py` | `linpro.config`   | 12    | Carga YAML, fusión, get/set por clave anidada, save |
| `tests/events/test_events.py` | `linpro.events`  | 14    | Pub-sub, handlers múltiples, errores, constantes |
| `tests/exceptions/test_exceptions.py` | `linpro.exceptions` | 14 | Jerarquía, herencia, captura de excepciones |
| `tests/logging/test_logging.py` | `linpro.logging` | 13 | Niveles, singleton, salida a archivo |
| `tests/plugins/test_plugins.py` | `linpro.plugins` | 10 | PluginManager, descubrimiento, carga/descarga |
| `tests/project/test_project.py` | `linpro.project` | 25 | Project, Workspace, serialización, estado |
| `tests/settings/test_settings.py` | `linpro.settings` | 13 | Carga JSON, get/set, archivos recientes |
| **Total**                  |                      | **109** | |

## Ejecución

```bash
# Todos los tests del Core
pytest tests/

# Tests de un módulo específico
pytest tests/config/test_config.py -v

# Tests con cobertura
pytest tests/ --cov=linpro.core --cov-report=term-missing
```

## Casos de prueba por módulo

### app (8 tests)
- `test_singleton` — `get_instance()` devuelve siempre la misma instancia
- `test_start_stop` — ciclo de vida completo
- `test_start_twice` — `start()` repetido es seguro (idempotente)
- `test_stop_without_start` — `stop()` sin `start()` no falla
- `test_properties_not_none_after_start` — todas las propiedades existen tras start
- `test_is_running` — estado correcto antes y después de start/stop
- `test_config_property` — propiedad `config` devuelve instancia válida
- `test_event_bus_property` — propiedad `event_bus` devuelve instancia válida

### config (12 tests)
- `test_default_values` — valores por defecto cargados correctamente
- `test_get_simple` — `get("key")` funciona con claves simples
- `test_get_nested` — `get("project.default_epsg")` funciona con claves anidadas
- `test_get_default` — devuelve default si la clave no existe
- `test_set_nested` — `set("a.b.c", value)` crea diccionarios intermedios
- `test_to_dict` — `to_dict()` devuelve una copia independiente
- `test_load_file_not_found` — `load_file()` con path inexistente lanza `ConfigError`
- `test_merge` — la fusión respeta y sobreescribe valores existentes
- `test_save_and_reload` — guardar y recargar YAML mantiene los valores
- `test_config_singleton` — `get_instance()` es singleton
- `test_load_file_yaml_error` — YAML mal formado lanza `ConfigError`
- `test_pyaml_not_available` — error controlado si falta PyYAML

### events (14 tests)
- `test_subscribe` — suscripción a evento
- `test_publish` — handler se ejecuta al publicar
- `test_publish_with_data` — los datos del evento llegan al handler
- `test_unsubscribe` — handler no se ejecuta tras darse de baja
- `test_multiple_handlers` — múltiples handlers para un mismo evento
- `test_publish_no_subscribers` — publicar sin suscriptores no falla
- `test_clear` — `clear()` elimina todas las suscripciones
- `test_handler_error` — error en handler se propaga como `EventError`
- `test_event_dataclass_defaults` — valores por defecto de `Event`
- `test_core_started_constant` — la constante `CORE_STARTED` existe y es string
- `test_core_stopped_constant` — `CORE_STOPPED` existe y es string
- `test_project_opened_constant` — `PROJECT_OPENED` existe y es string
- `test_plugin_loaded_constant` — `PLUGIN_LOADED` existe y es string
- `test_event_timestamp` — el timestamp se genera automáticamente

### exceptions (14 tests)
- `test_linpro_error_base` — `LINPROError` hereda de `Exception`
- `test_project_error` — `ProjectError` hereda de `LINPROError`
- `test_config_error` — `ConfigError` hereda de `LINPROError`
- `test_plugin_error` — `PluginError` hereda de `LINPROError`
- `test_event_error` — `EventError` hereda de `LINPROError`
- `test_log_error` — `LogError` hereda de `LINPROError`
- `test_settings_error` — `SettingsError` hereda de `LINPROError`
- `test_version_error` — `VersionError` hereda de `LINPROError`
- `test_workspace_error` — `WorkspaceError` hereda de `LINPROError`
- `test_catch_linpro_error` — `except LINPROError` captura todas
- `test_catch_project_error` — captura específica de `ProjectError`
- `test_catch_config_error` — captura específica de `ConfigError`
- `test_exception_message` — el mensaje se almacena correctamente
- `test_raise_and_catch_all` — todas las subclases se lanzan y capturan como `LINPROError`

### logging (13 tests)
- `test_singleton` — `get_instance()` es singleton
- `test_default_level` — el nivel por defecto es INFO
- `test_set_level` — `set_level()` cambia el nivel
- `test_info_log` — `info()` no lanza excepción
- `test_debug_log` — `debug()` no lanza excepción
- `test_warning_log` — `warning()` no lanza excepción
- `test_error_log` — `error()` no lanza excepción
- `test_critical_log` — `critical()` no lanza excepción
- `test_file_output` — `set_file_output()` escribe en archivo
- `test_file_output_encoding` — el archivo usa UTF-8
- `test_logger_name` — el nombre del logger es configurable
- `test_log_level_enum_values` — `LogLevel` tiene los valores correctos
- `test_logger_reuse` — cambiar nivel no rompe el logger existente

### plugins (10 tests)
- `test_singleton` — `PluginManager.get_instance()` es singleton
- `test_add_search_path` — `add_search_path()` con directorio válido
- `test_add_search_path_invalid` — ruta inexistente se ignora
- `test_load_not_found` — `load()` con nombre inexistente devuelve False
- `test_unload_not_loaded` — `unload()` con plugin no cargado no falla
- `test_list_plugins_empty` — `list_plugins()` vacío tras crear el gestor
- `test_run_all_empty` — `run_all()` sin plugins devuelve dict vacío
- `test_load_twice` — `load()` repetido devuelve True sin recargar
- `test_get_plugin_nonexistent` — `get_plugin()` devuelve None si no existe
- `test_plugin_info_dataclass` — `PluginInfo` se crea con valores por defecto

### project (25 tests)
- `test_create_project` — crear proyecto con nombre
- `test_default_name` — nombre por defecto "Sin título"
- `test_metadata_defaults` — valores por defecto de `ProjectMetadata`
- `test_set_data` — `set_data()` almacena y marca dirty
- `test_get_data` — `get_data()` recupera valores
- `test_get_data_default` — `get_data()` devuelve default si no existe
- `test_mark_loaded` — `mark_loaded()` limpia dirty
- `test_mark_saved` — `mark_saved()` limpia dirty
- `test_path_property` — getter/setter de `path`
- `test_to_dict` — `to_dict()` serializa metadatos y datos
- `test_from_dict` — `from_dict()` reconstruye desde diccionario
- `test_from_dict_roundtrip` — `to_dict()` + `from_dict()` es idempotente
- `test_project_state_defaults` — `ProjectState` con valores por defecto
- `test_project_repr` — `repr()` incluye nombre y dirty
- `test_workspace_singleton` — `Workspace.get_instance()` es singleton
- `test_workspace_current_project_none` — inicialmente sin proyecto
- `test_workspace_open_project` — `open_project()` establece proyecto activo
- `test_workspace_close_project` — `close_project()` limpia proyecto activo
- `test_workspace_list_projects` — `list_open_projects()` devuelve los abiertos
- `test_workspace_multiple_projects` — abrir dos proyectos, cerrar el activo
- `test_workspace_open_twice` — abrir mismo proyecto no duplica
- `test_metadata_created_modified` — fechas se establecen automáticamente
- `test_metadata_default_epsg` — EPSG por defecto 25830
- `test_project_set_data_updates_modified` — `set_data()` actualiza `modified`
- `test_project_from_dict_empty` — `from_dict({})` no lanza excepción

### settings (13 tests)
- `test_singleton` — `get_instance()` es singleton
- `test_default_values` — valores por defecto cargados
- `test_get_simple` — `get("ui.language")` devuelve "es"
- `test_get_default` — clave inexistente devuelve default
- `test_set_value` — `set()` actualiza y guarda
- `test_set_creates_nested` — `set("a.b.c", v)` crea estructura
- `test_load_nonexistent` — `load()` sin archivo crea defaults y guarda
- `test_load_invalid_json` — JSON inválido lanza `SettingsError`
- `test_save_and_reload` — guardar y recargar mantiene valores
- `test_add_recent_file` — `add_recent_file()` inserta al inicio
- `test_add_recent_file_max` — no supera 10 elementos
- `test_add_recent_file_no_duplicates` — evita duplicados moviendo al inicio
- `test_path_none_save_no_error` — `save()` sin path no falla

## Tests de integración (pendientes)

Los siguientes escenarios requieren pruebas de integración y están planificados para una versión futura:

- Ciclo completo `LINPROApp.start()` → `stop()` midiendo eventos emitidos
- Descubrimiento real de plugins desde directorio temporal
- Carga real de archivos YAML de configuración
- Persistencia completa de proyecto (serializar → archivo → deserializar)
- Interacción entre `Project`, `Workspace` y el bus de eventos

Ver `TODO.md` para más detalles.
