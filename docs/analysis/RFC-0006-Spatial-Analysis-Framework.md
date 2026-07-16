# RFC-0006: Spatial Analysis Framework

| Campo | Valor |
|---|---|
| **Estado** | BORRADOR |
| **Autor** | Chief Architect |
| **Fecha** | 2026-07-16 |
| **Dependencias** | RFC-0005 (Operators), TASK-0006 (Polyline/EngineeringAxis) |
| **Sustituye a** | — |
| **Nomenclatura** | `ANAL-` |

---

## 1. Problema

Hasta ahora LINPRO ha resuelto problemas matemáticos: puntos, vectores, segmentos, polilíneas, operadores de geometría computacional.

A partir de ahora debe resolver problemas de **ingeniería lineal**: detectar municipios, carreteras, ríos, parcelas e infraestructuras que intersectan un eje.

Cada uno de estos análisis comparte un patrón común:

1. Recibir un `EngineeringAxis` (Polyline con PK).
2. Consultar datos GIS externos (shapefile, geojson, wfs).
3. Calcular intersecciones geométricas.
4. Resolver los PK de entrada/salida.
5. Devolver un resultado estructurado.

Sin un marco común, cada detector implementaría su propia lógica de intersección, su propio manejo de PK, su propio formato de salida. Eso genera deuda técnica, duplicación y resultados inconsistentes.

---

## 2. Objetivo

Definir el **Spatial Analysis Framework**: la arquitectura, contratos y modelos que todos los detectores deben seguir.

**No objetivo:** Implementar ningún detector específico (eso será RFC-0007, RFC-0008, etc.).

---

## 3. Contrato base: `Detector(ABC)`

Todo detector debe heredar de `Detector(ABC)` e implementar:

```python
class Detector(ABC):
    @abstractmethod
    def analyze(
        self,
        axis: EngineeringAxis,
    ) -> AnalysisResult:
        ...
```

### 3.1. Entrada

| Parámetro | Tipo | Descripción |
|---|---|---|
| `axis` | `EngineeringAxis` (Polyline) | Eje de ingeniería con PK, topología y métodos de proyección |

### 3.2. Salida

`AnalysisResult` es un objeto que contiene:

```python
class AnalysisResult:
    axis: EngineeringAxis
    crossings: list[Crossing]
    incidents: list[Incident]
    metadata: AnalysisMetadata
```

Nunca un diccionario. Nunca `None`.

### 3.3. Responsabilidades del Detector

1. **Cargar** datos GIS (puede ser lazy, archivo local o WFS).
2. **Filtrar** entidades relevantes dentro del bbox del eje (optimización espacial).
3. **Intersectar** cada entidad con el eje usando operadores geométricos.
4. **Calcular PK** de entrada y salida usando `EngineeringAxis.pk_of()`.
5. **Construir** el `Crossing` correspondiente.
6. **Reportar** incidencias (errores, entidades sin intersección, etc.).
7. **Devolver** un `AnalysisResult` completo.

---

## 4. Modelo de cruces

### 4.1. `Crossing` (base)

```python
class Crossing(ABC):
    pk_start: PK
    pk_end: PK
    point_start: Point
    point_end: Point
    length: float          # = float(pk_end - pk_start)
```

### 4.2. `MunicipalityCrossing`

```python
class MunicipalityCrossing(Crossing):
    municipality: str       # Nombre del municipio
    province: str           # Provincia
    code: str               # INE code (5 dígitos)
```

### 4.3. `RoadCrossing` (futuro)

```python
class RoadCrossing(Crossing):
    road_id: str
    road_name: str
    road_type: str          # highway, national, regional, local
```

### 4.4. `RiverCrossing` (futuro)

```python
class RiverCrossing(Crossing):
    name: str
    river_type: str         # river, stream, creek
```

### 4.5. Principios del modelo

- Todo cruce específico hereda de `Crossing`.
- `Crossing` no almacena referencias al eje (se accede via `AnalysisResult.axis`).
- `Crossing` es inmutable (todos sus campos son `@property` o `__init__`-only).

---

## 5. Modelo de incidencias

No todo cruce es perfecto. El framework debe soportar reportar problemas:

```python
@dataclass
class Incident:
    severity: IncidentSeverity   # INFO, WARNING, ERROR
    code: str                    # Código máquina (ej. "MUN-001")
    message: str                 # Mensaje legible
    geometry: Geometry | None    # Geometría asociada (opcional)
    pk: PK | None                # PK asociado (opcional)


class IncidentSeverity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
```

Ejemplos de incidencias:
- `MUN-001` — Municipio sin geometría en la fuente de datos.
- `MUN-002` — Intersección degenerada (longitud cero).
- `GEN-001` — Error al cargar datos GIS.

---

## 6. Metadatos del análisis

```python
@dataclass
class AnalysisMetadata:
    detector_name: str
    detector_version: str
    timestamp: datetime
    duration_ms: float
    axis_length: float
    entity_count: int            # Entidades GIS evaluadas
    crossing_count: int
    incident_count: int
```

---

## 7. Estrategia de intersección

El framework define dos niveles:

### 7.1. Intersección nativa (siempre disponible)

Usa los operadores geométricos de LINPRO (`geometry/operators/`):

1. **Filtro BBox**: Comparar el BoundingBox del eje con el BBox de cada entidad GIS (`bbox_intersects`).
2. **Intersección segmento-a-segmento**: Para cada segmento del eje, intersectar con los segmentos del polígono de la entidad (`intersects` + `intersection_point`).
3. **Resolución PK**: Usar `axis.segment_at_pk()`, `axis.point_at_pk()`, y `axis.pk_of()` para calcular PK de entrada/salida.

### 7.2. Intersección acelerada (con R-tree)

Cuando `rtree` esté disponible, el `SpatialIndex` (servicio) permite:

1. Indexar los segmentos del eje en un R-tree.
2. Indexar los polígonos de las entidades GIS.
3. Consultas rápidas de solapamiento.

---

## 8. Servicios del framework

### 8.1. `SpatialIndex`

Responsabilidad: construir y consultar un índice espacial para acelerar intersecciones.

```python
class SpatialIndex:
    def build(self, axis: EngineeringAxis) -> None: ...
    def query(self, bbox: BoundingBox) -> list[int]: ...
```

### 8.2. `GISLoader`

Responsabilidad: cargar datos GIS desde múltiples fuentes.

```python
class GISLoader:
    @staticmethod
    def from_shapefile(path: str, epsg: int = 25830) -> list[dict]: ...
    @staticmethod
    def from_geojson(path: str) -> list[dict]: ...
    @staticmethod
    def from_wfs(url: str, layer: str, bbox: BoundingBox) -> list[dict]: ...
```

El GISLoader devuelve geometrías como listas de `Point` de LINPRO (no Shapely).

---

## 9. Combinación de detectores

El `UnifiedAnalysisEngine` (futuro) orquestará múltiples detectores:

```python
class UnifiedAnalysisEngine:
    def __init__(self):
        self._detectors: list[Detector] = []

    def register(self, detector: Detector) -> None: ...

    def run_all(self, axis: EngineeringAxis) -> dict[str, AnalysisResult]:
        return {
            d.name: d.analyze(axis)
            for d in self._detectors
        }
```

---

## 10. Convenciones de PK

- Todo PK se expresa como `PK` (value object), nunca `float`.
- `pk_start` siempre ≤ `pk_end`.
- `length` = `float(pk_end - pk_start)`.
- Para cruces puntuales (una carretera que cruza el eje en un solo punto), `pk_start == pk_end` y `length == 0.0`.

---

## 11. Reglas de implementación

| Regla | Descripción |
|---|---|
| **ANAL-001** | Ningún detector devuelve `None` o lanza excepción no controlada. |
| **ANAL-002** | Todo detector se construye con `dataclass` o `__init__` simple, sin efectos secundarios. |
| **ANAL-003** | La carga de datos GIS debe ser explícita (parámetro en constructor o método `load_data`). |
| **ANAL-004** | Los detectores no modifican el eje de entrada. |
| **ANAL-005** | Todo resultado incluye metadatos de la ejecución. |
| **ANAL-006** | Si un detector no puede cargar sus datos, devuelve un `AnalysisResult` con una incidencia `ERROR` y cruces vacíos. |

---

## 12. ADRs asociados

| ID | Título |
|---|---|
| ADR-010 | Detector como ABC — todos los detectores heredan del mismo contrato |
| ADR-011 | AnalysisResult como objeto único — nunca diccionarios |
| ADR-012 | Crossing como jerarquía inmutable |
| ADR-013 | Incidencias como parte del resultado, no como excepciones |
| ADR-014 | GISLoader como servicio separado del detector |
| ADR-015 | SpatialIndex como optimización opcional |

---

## 13. Roadmap del framework

1. ✅ RFC-0006 — este documento.
2. ⏳ `analysis/__init__.py`, `detectors/base.py`, `models/`.
3. ⏳ `MunicipalityDetector` + `MunicipalityCrossing`.
4. ⏳ `GISLoader` (shapefile + geojson + wfs).
5. ⏳ `SpatialIndex` (con y sin rtree).
6. ⏳ `RoadDetector`, `RiverDetector`, `CadastreDetector`.
7. ⏳ `UnifiedAnalysisEngine`.
8. ⏳ `ExcelExporter` (resultados a Excel).

---

## 14. Criterios de certificación

1. `Detector(ABC)` definido, testado y documentado.
2. Al menos un detector concreto (`MunicipalityDetector`) implementado y testado.
3. Modelos `Crossing`, `AnalysisResult`, `Incident` implementados.
4. `GISLoader.from_geojson()` funcional con geometrías LINPRO.
5. 200+ tests, cobertura ≥95%.
6. Demo funcional: `axis = Polyline.from_dxf(...) → MunicipalityDetector.detect(axis) → resultado`.
