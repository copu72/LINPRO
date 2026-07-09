# Arquitectura del Motor Geométrico

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Estado:** Aprobado

---

## 1. Propósito

El motor geométrico de LINPRO proporciona las capacidades fundamentales de cálculo sobre trazados lineales: definición de alineaciones, cálculo de distancias, generación de zonas de amortiguamiento, detección de intersecciones y validación topológica.

Cada submódulo es independiente, testeable por separado y depende únicamente de `shapely` para las operaciones geométricas de bajo nivel.

---

## 2. Estructura del Módulo

```
linpro/geometry/
├── __init__.py          # Exporta la API pública
├── alignment.py         # Alignment y tipos de segmento
├── buffer.py            # Generación de zonas de amortiguamiento
├── intersections.py     # Cálculo de intersecciones
├── pk.py                # Sistema de puntos kilométricos
└── topology.py          # Validaciones topológicas
```

---

## 3. Alignment

La clase `Alignment` representa un trazado horizontal compuesto por una secuencia de segmentos.

### 3.1 Tipos de Segmento

| Tipo | Clase | Descripción |
|------|-------|-------------|
| Recta | `Straight` | Segmento recto entre dos puntos. |
| Curva circular | `CircularArc` | Arco de circunferencia con radio constante. |
| Clotoide | `Clothoid` | Curva de transición con curvatura variable linealmente. |

### 3.2 Clase `Alignment`

```python
class Alignment:
    segments: list[Segment]  # Secuencia ordenada de segmentos

    def add_segment(self, segment: Segment) -> None
    def remove_segment(self, index: int) -> None
    def total_length(self) -> float
    def interpolate(self, pk: float) -> Point
    def point_at_distance(self, distance: float) -> Point
    def tangent_at(self, pk: float) -> float
    def get_segment_at(self, pk: float) -> tuple[int, Segment]
```

### 3.3 Interpolación

Dado un valor de PK (punto kilométrico), la interpolación recorre los segmentos acumulando distancias hasta localizar el segmento que contiene el PK solicitado, y luego calcula la posición exacta sobre ese segmento:

```
PK=0.0     PK=150.0       PK=450.0        PK=750.0
  +------------+--------------+--------------+
  |   Recta    |  Clotoide    | Curva Circ.  |
  | 150.0 m    |  300.0 m     |  300.0 m     |
  +------------+--------------+--------------+

Ej: PK=200.0  ->  Clotoide, a 50.0 m del inicio del segmento
```

---

## 4. PK (Punto Kilométrico)

El submódulo `pk.py` implementa el sistema de abscisas o puntos kilométricos:

```python
class PKSystem:
    """Sistema de puntos kilométricos asociado a una alineación."""

    origin: float          # PK de origen (normalmente 0.0)
    alignment: Alignment   # Alineación de referencia

    def to_distance(self, pk: float) -> float
    def from_distance(self, distance: float) -> float
    def interpolate(self, pk: float) -> Point
    def interpolate_bulk(self, pks: list[float]) -> list[Point]
```

- `to_distance`: convierte PK a distancia absoluta sobre la alineación.
- `from_distance`: convierte distancia absoluta a PK.
- `interpolate`: devuelve el punto `(x, y)` correspondiente a un PK.
- `interpolate_bulk`: versión optimizada para múltiples PKs.

---

## 5. Buffer

Genera zonas de amortiguamiento lateral a partir de la alineación, utilizando `shapely.buffer`.

### 5.1 Características

| Aspecto | Descripción |
|---------|-------------|
| Motor base | `shapely.buffer` con parámetros de calidad. |
| Distancia | Configurable por el usuario (valor único o variable por PK). |
| Lateral | Izquierda, derecha o ambos lados. |
| Precisión | Número de segmentos de aproximación para curvas. |

### 5.2 Clase `Buffer`

```python
@dataclass
class BufferConfig:
    distance: float = 50.0              # Distancia de buffer en metros
    side: Literal["left", "right", "both"] = "both"
    resolution: int = 16                # Segmentos por cuarto de círculo
    dynamic_distance: Optional[list[tuple[float, float]]] = None  # [(pk, dist), ...]

class BufferGenerator:
    config: BufferConfig
    alignment: Alignment

    def generate(self) -> Polygon
    def generate_side(self, side: str) -> Polygon
    def contains(self, geometry: Geometry) -> bool
```

---

## 6. Intersections

Detecta y caracteriza intersecciones entre la alineación y geometrías externas.

### 6.1 Clase `IntersectionFinder`

```python
class IntersectionFinder:
    alignment: Alignment

    def find_crossings(self, geometry: Geometry) -> list[Intersection]
    def find_crossings_multi(self, geometries: list[Geometry]) -> list[Intersection]
```

### 6.2 Intersección devuelta

```python
@dataclass
class Intersection:
    pk: float                  # PK donde ocurre la intersección
    point: Point               # Coordenadas del punto de cruce
    geometry_type: str         # Tipo de geometría intersectada
    geometry_id: Optional[str] # Identificador de la geometría (opcional)
    angle: float               # Ángulo de cruce en grados
```

---

## 7. Topology

Valida la consistencia topológica de la alineación y las geometrías asociadas.

### 7.1 Validaciones

| Validación | Descripción |
|------------|-------------|
| `check_continuity` | Verifica que no haya discontinuidades entre segmentos consecutivos. |
| `check_direction` | Verifica que el sentido de la alineación sea consistente. |
| `check_overlaps` | Detecta solapamientos entre segmentos. |
| `check_self_intersections` | Detecta auto-intersecciones en la alineación. |
| `check_min_radius` | Verifica que las curvas cumplan el radio mínimo normativo. |

### 7.2 Clase `TopologyValidator`

```python
class TopologyValidator:
    alignment: Alignment

    def validate_all(self) -> list[TopologyError]
    def check_continuity(self, tolerance: float = 1e-6) -> list[TopologyError]
    def check_direction(self) -> list[TopologyError]
    def check_overlaps(self) -> list[TopologyError]
    def check_self_intersections(self) -> list[TopologyError]
    def check_min_radius(self, min_radius: float) -> list[TopologyError]


@dataclass
class TopologyError:
    code: str                  # Código del error (ej: "DISCONTINUITY")
    severity: str              # "error" o "warning"
    message: str               # Descripción del problema
    segment_index: int         # Índice del segmento implicado
    pk: Optional[float]        # PK donde ocurre (si aplica)
```

---

## 8. Dependencias Externas

| Librería | Uso |
|----------|-----|
| `shapely` | Operaciones geométricas: buffer, intersecciones, validaciones. |
| `math` (stdlib) | Cálculos trigonométricos para clotoides y arcos. |
| `dataclasses` (stdlib) | Modelos de datos. |

---

## 9. Histórico de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | 2026-07-09 | Documento inicial de arquitectura del motor geométrico |
