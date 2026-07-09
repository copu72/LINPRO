# Arquitectura del Núcleo (LINPRO Core)

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Estado:** Aprobado

---

## 1. Propósito

LINPRO Core es la capa base de la plataforma y contiene el objeto central `Project`, que actúa como fachada y mediador para todos los módulos del sistema. Ningún módulo externo se comunica con los subsistemas sin pasar por `Project`.

---

## 2. Objeto `Project` — Fachada Principal

`Project` es el único punto de entrada para cualquier operación sobre un proyecto LINPRO. Encapsula el estado completo del proyecto y coordina los módulos de análisis.

### 2.1 Estructura Interna

```
Project
├── alignment        # Alineación horizontal (trazado en planta)
├── buffer           # Configuración de zonas de amortiguamiento
├── settings         # Configuración global del proyecto
├── municipalities   # Datos municipales (desde GIS)
├── parcels          # Datos parcelarios (desde GIS)
├── roads            # Red de carreteras (desde GIS)
├── rivers           # Red hidrográfica (desde GIS)
├── infrastructure   # Infraestructura existente (desde GIS)
├── results          # Resultados de análisis (AnalysisResult[])
├── history          # Historial de cambios (undo/redo)
└── plugins          # Plugins cargados y registrados
```

### 2.2 Responsabilidades

| Responsabilidad | Descripción |
|----------------|-------------|
| Fachada | Proporciona una API unificada para todas las operaciones del proyecto. |
| Mediador | Coordina la comunicación entre módulos de análisis y fuentes de datos. |
| Serialización | Lee y escribe proyectos en formato `.linpro` (JSON/YAML). |
| Undo/Redo | Mantiene un historial de cambios con capacidad de deshacer/rehacer. |
| Eventos | Emite eventos cuando el estado del proyecto cambia para que las vistas se actualicen. |
| Registro de plugins | Permite que los plugins se registren y extiendan las capacidades de análisis. |

---

## 3. Diagrama de Clases Conceptual (Textual)

```
+------------------+
|     Project      |
+------------------+
| + name: str      |
| + path: Path     |
| + version: str   |
+------------------+
| + load()         |
| + save()         |
| + undo()         |
| + redo()         |
| + analyze_all()  |
| + on_event()     |
+------------------+
        |
        | contiene
        v
+------------------+     +-------------------+
|   Alignment      |     |   AnalysisModule  |<-- (interfaz)
+------------------+     +-------------------+
| + segments: list |     | + name: str       |
| + total_length() |     | + analyze()       |
| + interpolate()  |     +-------------------+
+------------------+             ^
                                 |
                    +------------+------------+
                    |            |             |
            +-------+--+  +-----+------+  +--+--------+
            | GISModule |  | CADModule  |  | ReportsMod |
            +----------+  +------------+  +-----------+
            | + load_   |  | + export_  |  | + generate |
            |   layers()|  |   to_dxf() |  |   _report()|
            +-----------+  +------------+  +-----------+
```

---

## 4. Serialización

El proyecto se serializa en un único archivo con extensión `.linpro`. El formato interno es JSON compatible con esquemas de validación.

Estructura del archivo `.linpro`:

```json
{
  "version": "1.0",
  "metadata": { "name": "...", "author": "...", "date": "..." },
  "settings": { "crs": "EPSG:25830", "units": "m" },
  "alignment": { "segments": [...] },
  "buffer": { "distance": 50.0, "side": "both" },
  "results": [...],
  "plugins": { "enabled": ["plugin_a", "plugin_b"] }
}
```

Los datos geográficos pesados (geometrías) no se incrustan en el `.linpro`; se referencian mediante rutas relativas a archivos externos (shapefiles, GeoJSON) o se regeneran desde las fuentes WFS.

---

## 5. Sistema de Eventos

`Project` implementa un bus de eventos interno al que se suscriben los componentes de la GUI y otros módulos.

Eventos principales:

| Evento | Descripción |
|--------|-------------|
| `project.loaded` | Proyecto cargado correctamente. |
| `project.saved` | Proyecto guardado. |
| `project.modified` | Algún componente del proyecto cambió. |
| `project.analyzed` | Análisis completado. Nuevos resultados disponibles. |
| `project.undo` | Se ejecutó una operación de deshacer. |
| `project.redo` | Se ejecutó una operación de rehacer. |
| `project.error` | Ocurrió un error durante una operación. |

---

## 6. Dependencias Externas

- `pyyaml` — lectura/escritura de YAML.
- `json` (stdlib) — serialización principal.
- `pathlib` (stdlib) — manejo de rutas.
- `dataclasses` (stdlib) — modelos de datos.

No se permiten dependencias pesadas en el núcleo. Cualquier funcionalidad que requiera `geopandas`, `shapely`, `ezdxf`, etc. debe implementarse en una capa superior.

---

## 7. Histórico de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | 2026-07-09 | Documento inicial de arquitectura del núcleo |
