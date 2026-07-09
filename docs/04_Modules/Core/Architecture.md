# Arquitectura del Core de LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09

---

## 1. Principios de diseño

El Core de LINPRO se rige por los siguientes principios:

- **Singleton:** Los servicios fundamentales (app, config, logger, event bus, plugin manager, workspace) existen una única vez en todo el ciclo de vida.
- **Fachada (Facade):** `LINPROApp` es la fachada que orquesta todos los subsistemas internos. El resto del programa interactúa con el Core a través de ella.
- **Desacoplamiento:** Los módulos no se conocen entre sí. Se comunican exclusivamente a través del bus de eventos o leyendo/escribiendo sobre el objeto `Project`.
- **Inicialización perezosa (lazy):** Los singletons no se crean hasta que se invocan por primera vez.

## 2. Ciclo de vida de la aplicación

`LINPROApp.start()` orquesta el arranque en un orden estricto:

```
1. LINPROLogger       ← sistema de logging
2. Configuration      ← configuración global por defecto + YAML de usuario
3. UserSettings       ← preferencias de usuario desde JSON
4. EventBus           ← bus de eventos (aún sin subscriptores)
5. PluginManager      ← descubrimiento de plugins en directorios
6. Workspace          ← espacio de trabajo (sin proyecto abierto)
7. Publicación CORE_STARTED
```

`LINPROApp.stop()` invierte el orden:

```
1. Publicación CORE_STOPPING
2. Descarga de todos los plugins (shutdown)
3. Publicación CORE_STOPPED
4. Liberación de recursos
```

## 3. Patrón Singleton

Las siguientes clases implementan el patrón singleton mediante el método `get_instance()`:

| Clase            | Propósito |
|------------------|-----------|
| `LINPROApp`      | Punto de entrada único |
| `Configuration`  | Configuración global |
| `LINPROLogger`   | Logger único para toda la aplicación |
| `EventBus`       | Bus de eventos central |
| `PluginManager`  | Gestor único de plugins |
| `Workspace`      | Espacio de trabajo actual |

```python
# Todos los singletons se acceden igual:
obj = Clase.get_instance()
```

## 4. Patrón Fachada (Facade)

`LINPROApp` expone propiedades de solo lectura que delegan en los singletons subyacentes:

```
LINPROApp
├── .logger        → LINPROLogger.get_instance()
├── .config        → Configuration.get_instance()
├── .settings      → UserSettings.get_instance()
├── .event_bus     → EventBus.get_instance()
├── .plugin_manager → PluginManager.get_instance()
└── .workspace     → Workspace.get_instance()
```

El consumidor nunca llama a `get_instance()` de los subsistemas; accede a todo a través de `app.*`.

## 5. Bus de eventos

El `EventBus` implementa el patrón publicador-subscriptor (pub-sub). Los módulos se suscriben a eventos sin conocer al emisor:

```python
def on_project_opened(event: Event):
    print(f"Proyecto abierto: {event.data}")

bus = EventBus.get_instance()
bus.subscribe("project.opened", on_project_opened)
bus.publish(Event(name="project.opened", data={"name": "mi_proyecto"}))
```

**Eventos estándar del Core:**

| Constante             | Valor                  | Publicado por      |
|-----------------------|------------------------|--------------------|
| `CORE_STARTING`       | `core.starting`        | LINPROApp.start()  |
| `CORE_STARTED`        | `core.started`         | LINPROApp.start()  |
| `CORE_STOPPING`       | `core.stopping`        | LINPROApp.stop()   |
| `CORE_STOPPED`        | `core.stopped`         | LINPROApp.stop()   |
| `PROJECT_OPENED`      | `project.opened`       | Workspace          |
| `PROJECT_CLOSED`      | `project.closed`       | Workspace          |
| `PROJECT_SAVED`       | `project.saved`        | Project            |
| `PROJECT_MODIFIED`    | `project.modified`     | Project            |
| `PLUGIN_LOADED`       | `plugin.loaded`        | PluginManager      |
| `PLUGIN_UNLOADED`     | `plugin.unloaded`      | PluginManager      |
| `SETTINGS_CHANGED`    | `settings.changed`     | UserSettings       |
| `CONFIG_CHANGED`      | `config.changed`       | Configuration      |

## 6. Diagrama de relaciones

```
Usuario / UI / CLI
       │
       ▼
  LINPROApp  ◄── Fachada
       │
       ├── EventBus ◄── pub-sub entre módulos
       ├── Configuration
       ├── UserSettings
       ├── LINPROLogger
       ├── PluginManager ◄── BasePlugin, PluginInfo
       └── Workspace
               │
               └── Project ◄── ProjectMetadata, ProjectState
```

## 7. Gestión de proyectos

`Project` es el objeto central de datos. Todos los módulos leen y escriben sobre él. `Workspace` gestiona el conjunto de proyectos abiertos (actualmente uno solo, preparado para múltiples).

```
Workspace (singleton)
└── current_project: Optional[Project]
        ├── metadata: ProjectMetadata (nombre, autor, EPSG, fechas...)
        ├── state: ProjectState (dirty, loaded, has_alignment...)
        ├── data: Dict[str, Any] (almacenamiento genérico)
        └── path: Optional[Path]
```

## 8. Configuración y preferencias

- **Configuration:** Configuración técnica del proyecto (EPSG, análisis, exportación, GIS). Carga YAML opcional del usuario que se fusiona con los valores por defecto.
- **UserSettings:** Preferencias de la interfaz de usuario (idioma, tema, archivos recientes). Se persisten en JSON en el directorio de configuración del usuario.
