# API del Core de LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09

---

## LINPROApp (`linpro.app`)

```python
class LINPROApp:

    @classmethod
    def get_instance(cls) -> LINPROApp: ...

    def start(self) -> None: ...
    def stop(self) -> None: ...

    @property
    def is_running(self) -> bool: ...

    @property
    def logger(self) -> Optional[LINPROLogger]: ...
    @property
    def config(self) -> Configuration: ...
    @property
    def settings(self) -> UserSettings: ...
    @property
    def event_bus(self) -> EventBus: ...
    @property
    def plugin_manager(self) -> PluginManager: ...
    @property
    def workspace(self) -> Workspace: ...
```

---

## Configuration (`linpro.config`)

```python
class Configuration:

    @classmethod
    def get_instance(cls) -> Configuration: ...

    def load_file(self, path: Path) -> None:
        """Carga un archivo YAML y lo fusiona con la configuración actual.
        Raises: ConfigError si el archivo no existe o el formato es inválido."""

    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor por clave anidada (ej. 'project.default_epsg').
        Devuelve default si la clave no existe."""

    def set(self, key: str, value: Any) -> None:
        """Establece un valor por clave anidada. Crea diccionarios intermedios si es necesario."""

    def to_dict(self) -> Dict[str, Any]:
        """Devuelve una copia del diccionario interno de configuración."""

    def save(self, path: Path) -> None:
        """Guarda la configuración actual como YAML.
        Raises: ConfigError si no se dispone de PyYAML o hay error de escritura."""
```

---

## EventBus (`linpro.events`)

```python
class EventBus:

    @classmethod
    def get_instance(cls) -> EventBus: ...

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Suscribe un callable al evento especificado."""

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        """Elimina una suscripción específica."""

    def publish(self, event: Event) -> None:
        """Publica un evento, ejecutando todos los handlers suscritos.
        Raises: EventError si algún handler lanza una excepción."""

    def clear(self) -> None:
        """Elimina todas las suscripciones activas."""
```

---

## Event (`linpro.events`)

```python
@dataclass
class Event:
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
```

**Constantes de eventos estándar:**

```python
CORE_STARTING    = "core.starting"
CORE_STARTED     = "core.started"
CORE_STOPPING    = "core.stopping"
CORE_STOPPED     = "core.stopped"
PROJECT_OPENED   = "project.opened"
PROJECT_CLOSED   = "project.closed"
PROJECT_SAVED    = "project.saved"
PROJECT_MODIFIED = "project.modified"
PLUGIN_LOADED    = "plugin.loaded"
PLUGIN_UNLOADED  = "plugin.unloaded"
SETTINGS_CHANGED = "settings.changed"
CONFIG_CHANGED   = "config.changed"
```

---

## PluginManager (`linpro.plugins`)

```python
class PluginManager:

    @classmethod
    def get_instance(cls) -> PluginManager: ...

    def add_search_path(self, path: Path) -> None:
        """Agrega un directorio a la ruta de búsqueda de plugins."""

    def discover(self) -> List[PluginInfo]:
        """Escanea los directorios de búsqueda y carga todos los plugins encontrados.
        Devuelve una lista con la información de cada plugin descubierto."""

    def load(self, name: str) -> bool:
        """Carga un plugin por nombre. Devuelve True si se cargó correctamente."""

    def unload(self, name: str) -> None:
        """Descarga un plugin (llama a shutdown() y lo elimina del registro)."""

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Obtiene la instancia de un plugin cargado."""

    def run_all(self, project: Any, **kwargs: Any) -> Dict[str, Any]:
        """Ejecuta todos los plugins cargados sobre un proyecto.
        Devuelve un diccionario {nombre_plugin: resultado}."""

    def list_plugins(self) -> List[str]:
        """Devuelve los nombres de todos los plugins cargados."""
```

---

## BasePlugin (`linpro.plugins`)

```python
class BasePlugin(ABC):

    @abstractmethod
    def get_info(self) -> PluginInfo: ...

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def execute(self, project: Any, **kwargs: Any) -> Dict[str, Any]: ...

    def shutdown(self) -> None:
        """Libera recursos (opcional)."""
```

---

## PluginInfo (`linpro.plugins`)

```python
@dataclass
class PluginInfo:
    name: str
    version: str
    description: str = ""
    author: str = ""
    dependencies: List[str] = field(default_factory=list)
```

---

## Project (`linpro.project`)

```python
class Project:

    def __init__(self, name: str = "Sin título") -> None: ...

    @property
    def metadata(self) -> ProjectMetadata: ...
    @property
    def state(self) -> ProjectState: ...
    @property
    def path(self) -> Optional[Path]: ...
    @path.setter
    def path(self, value: Optional[Path]) -> None: ...

    def set_data(self, key: str, value: Any) -> None:
        """Almacena un valor en el diccionario de datos del proyecto."""

    def get_data(self, key: str, default: Any = None) -> Any:
        """Recupera un valor del diccionario de datos."""

    def mark_loaded(self) -> None: ...
    def mark_saved(self) -> None: ...

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el proyecto a un diccionario serializable."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Project:
        """Crea un proyecto desde un diccionario."""
```

---

## Workspace (`linpro.project`)

```python
class Workspace:

    @classmethod
    def get_instance(cls) -> Workspace: ...

    @property
    def current_project(self) -> Optional[Project]: ...

    def open_project(self, project: Project) -> None: ...
    def close_project(self) -> None: ...
    def list_open_projects(self) -> List[Project]: ...
```

---

## ProjectMetadata (`linpro.project`)

```python
@dataclass
class ProjectMetadata:
    name: str
    description: str = ""
    author: str = ""
    company: str = ""
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    version: str = "0.1.0"
    epsg: int = 25830
```

---

## ProjectState (`linpro.project`)

```python
@dataclass
class ProjectState:
    is_dirty: bool = False
    is_loaded: bool = False
    has_alignment: bool = False
    has_analysis: bool = False
    has_results: bool = False
```

---

## UserSettings (`linpro.settings`)

```python
class UserSettings:

    @classmethod
    def get_instance(cls) -> UserSettings: ...

    def load(self, path: Path) -> None:
        """Carga preferencias desde un archivo JSON.
        Si el archivo no existe, crea uno con valores por defecto."""

    def save(self) -> None:
        """Guarda las preferencias actuales a JSON."""

    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor por clave anidada (ej. 'ui.language')."""

    def set(self, key: str, value: Any) -> None:
        """Establece un valor y persiste automáticamente."""

    def add_recent_file(self, path: str) -> None:
        """Agrega una ruta al inicio de la lista de archivos recientes (máx. 10)."""
```

---

## LINPROLogger (`linpro.logging`)

```python
class LINPROLogger:

    @classmethod
    def get_instance(cls) -> LINPROLogger: ...

    def set_file_output(self, path: Path) -> None: ...
    def set_level(self, level: LogLevel) -> None: ...

    def debug(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...
    def critical(self, message: str) -> None: ...

    @property
    def name(self) -> str: ...
```

---

## LogLevel (`linpro.logging`)

```python
class LogLevel(Enum):
    DEBUG    = 10
    INFO     = 20
    WARNING  = 30
    ERROR    = 40
    CRITICAL = 50
```

---

## VersionInfo (`linpro.version`)

```python
@dataclass
class VersionInfo:
    major: int
    minor: int
    patch: int
    suffix: str = ""
    string: str = ""
```

---

## Funciones auxiliares (`linpro.version`)

```python
def get_version() -> VersionInfo:
    """Devuelve la versión actual del programa como VersionInfo."""

def get_version_info() -> str:
    """Devuelve un string formateado: 'LINPRO Professional v0.1.0'."""

def compare_versions(v1: str, v2: str) -> int:
    """Compara dos versiones semver.
    Devuelve -1 si v1 < v2, 0 si son iguales, 1 si v1 > v2.
    Raises: VersionError si el formato es inválido."""
```

---

## Excepciones (`linpro.exceptions`)

```python
class LINPROError(Exception):     """Base de todas las excepciones."""
class ProjectError(LINPROError):   """Error en operaciones de proyecto."""
class ConfigError(LINPROError):    """Error en configuración."""
class PluginError(LINPROError):    """Error en sistema de plugins."""
class EventError(LINPROError):     """Error en bus de eventos."""
class LogError(LINPROError):       """Error en logging."""
class SettingsError(LINPROError):  """Error en preferencias."""
class VersionError(LINPROError):   """Error en versionado."""
class WorkspaceError(LINPROError): """Error en workspace."""
```
