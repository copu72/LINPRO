# Arquitectura de Plugins

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Estado:** Aprobado

---

## 1. Propósito

El sistema de plugins permite extender las capacidades de análisis de LINPRO sin modificar el código base. Cada plugin es un directorio independiente que se descubre y carga dinámicamente en tiempo de ejecución.

---

## 2. Estructura de un Plugin

Cada plugin reside en un subdirectorio independiente dentro de la carpeta `/plugins/`. La estructura mínima requerida es:

```
plugins/
└── mi_plugin/
    ├── __init__.py      # Contiene la clase del plugin (obligatorio)
    ├── plugin.yaml      # Metadatos del plugin (obligatorio)
    ├── ...              # Código adicional del plugin (opcional)
    └── resources/       # Recursos estáticos (opcional)
```

---

## 3. Metadatos (`plugin.yaml`)

Archivo YAML con la información descriptiva del plugin:

```yaml
name: mi_plugin
version: "1.0.0"
description: "Descripción breve del plugin"
author: "Autor o equipo"
license: "MIT"
tags: ["analisis", "hidrologia"]
dependencies:
  - geopandas>=0.12
  - numpy
entry_point: "MiPluginClass"
```

---

## 4. Interfaz `BasePlugin`

Todos los plugins deben implementar la interfaz `BasePlugin` definida en LINPRO Core:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class AnalysisResult:
    """Resultado estándar de un análisis."""
    plugin_name: str
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    messages: list[str] = field(default_factory=list)


class BasePlugin(ABC):
    """Clase base que todo plugin debe implementar."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre único del plugin."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Versión semántica del plugin."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Descripción del plugin."""
        ...

    @abstractmethod
    def analyze(self, project) -> AnalysisResult:
        """Ejecuta el análisis sobre el proyecto proporcionado.

        Args:
            project: Instancia de Project de LINPRO Core.

        Returns:
            AnalysisResult con los resultados del análisis.
        """
        ...
```

---

## 5. Ejemplo de Implementación Mínima

`plugins/ejemplo_analisis/__init__.py`:

```python
from linpro.core.plugin import BasePlugin, AnalysisResult

class EjemploAnalisisPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "ejemplo_analisis"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Plugin de ejemplo que procesa la alineación"

    def analyze(self, project) -> AnalysisResult:
        try:
            length = project.alignment.total_length()
            return AnalysisResult(
                plugin_name=self.name,
                success=True,
                data={"total_length": length},
                messages=[f"Longitud total: {length:.2f} m"]
            )
        except Exception as e:
            return AnalysisResult(
                plugin_name=self.name,
                success=False,
                error=str(e)
            )
```

---

## 6. `PluginLoader` — Descubrimiento y Carga

El `PluginLoader` se encarga de:

1. Escanear el directorio `/plugins/` en busca de subdirectorios.
2. Verificar que cada subdirectorio contenga `__init__.py` y `plugin.yaml`.
3. Parsear `plugin.yaml` para obtener los metadatos.
4. Importar dinámicamente el módulo `__init__.py` e instanciar la clase especificada en `entry_point`.
5. Verificar que la instancia implemente `BasePlugin`.
6. Registrar el plugin en `Project` para su uso.

```python
class PluginLoader:
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = Path(plugins_dir)
        self._plugins: dict[str, BasePlugin] = {}

    def discover(self) -> dict[str, BasePlugin]:
        """Descubre y carga todos los plugins válidos."""
        ...

    def load_plugin(self, plugin_dir: Path) -> Optional[BasePlugin]:
        """Carga un plugin desde un directorio específico."""
        ...

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Obtiene un plugin ya cargado por su nombre."""
        ...

    def unload_plugin(self, name: str) -> None:
        """Descarga un plugin."""
        ...
```

---

## 7. Registro en `Project`

El `Project` expone métodos para gestionar plugins:

```python
class Project:
    def register_plugin(self, plugin: BasePlugin) -> None:
        """Registra un plugin para su uso en análisis."""
        ...

    def unregister_plugin(self, name: str) -> None:
        """Elimina un plugin del registro."""
        ...

    def run_plugin(self, name: str) -> AnalysisResult:
        """Ejecuta un plugin registrado por su nombre."""
        ...

    def run_all_plugins(self) -> list[AnalysisResult]:
        """Ejecuta todos los plugins registrados secuencialmente."""
        ...
```

---

## 8. Ciclo de Vida de un Plugin

```
[Inicio de LINPRO]
       |
       v
PluginLoader.discover()
       |
       +-- Escanea /plugins/
       +-- Valida plugin.yaml
       +-- Importa __init__.py
       +-- Instancia la clase plugin
       |
       v
Project.register_plugin(plugin)
       |
       v
[Plugins disponibles en Project.plugins]
       |
       v
Usuario ejecuta análisis
       |
       v
Project.run_plugin("mi_plugin")
       |
       v
BasePlugin.analyze(project)
       |
       v
AnalysisResult
       |
       v
Resultados almacenados en Project.results
```

---

## 9. Buenas Prácticas

- Cada plugin debe ser autocontenido y declarar todas sus dependencias en `plugin.yaml`.
- Los plugins no deben modificar el estado interno de `Project` directamente; deben devolver resultados a través de `AnalysisResult`.
- Los plugins pueden leer cualquier atributo de `Project` (lectura), pero no deben escribir.
- Usar nombres únicos para evitar conflictos entre plugins.
- El `plugin.yaml` debe incluir la versión mínima de LINPRO Core con la que es compatible.

---

## 10. Histórico de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | 2026-07-09 | Documento inicial de arquitectura de plugins |
