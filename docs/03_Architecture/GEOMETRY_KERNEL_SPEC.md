# GEOMETRY KERNEL SPEC

**Proyecto:** LINPRO
**Componente:** Geometry Engine (Kernel Matemático)
**Versión:** 1.0.0
**Estado:** ⚡ Aprobado
**Fecha:** 2026-07-09

---

## 1. Objetivo

Definir la arquitectura, contratos y reglas del Geometry Engine de LINPRO.
Este documento es la **Constitución** del núcleo matemático. Todo el código del motor
geométrico debe cumplir lo aquí establecido. Ninguna decisión de implementación
puede contradecir esta especificación sin una revisión de arquitectura.

El Geometry Engine es un **kernel matemático puro**, sin dependencias de GIS, CAD,
Excel, Shapely ni ningún módulo de negocio (catastro, municipios, carreteras, etc.).
Debe poder publicarse como librería independiente:

```bash
pip install linpro-geometry
```

---

## 2. Filosofía

| Principio | Descripción |
|---|---|
| **Matemáticas puras** | El kernel solo conoce coordenadas, vectores, curvas y transformaciones. Nada de parcelas, ejes de carretera o municipios. |
| **Cero dependencias externas** | Solo `math` y `json` de la stdlib. Sin Shapely, NumPy, GeoPandas, AutoCAD ni PySide. |
| **Inmutable por defecto** | Todas las entidades geométricas son inmutables. Esto elimina efectos secundarios y facilita el hash, la comparación y el uso en contenedores. |
| **Fail fast** | Las validaciones se ejecutan en el constructor. Coordenadas inválidas (NaN, inf, tipo incorrecto) lanzan excepción inmediatamente. |
| **Composición sobre herencia** | Las entidades complejas (Polyline) se componen de entidades simples (Point, Segment), no heredan de ellas. La herencia solo se usa para la jerarquía abstracta (Curve → Line, Polyline, Arc). |
| **Tipado fuerte** | Cobertura completa de tipos con type hints. `float` para coordenadas, nunca `int`. |
| **Sin estado compartido** | Ninguna clase usa estado global, variables de clase mutables o singletons. |
| **Sin deuda técnica** | Cada clase pasa por SPEC → DESIGN → IMPLEMENT → TEST → REVIEW → RELEASE. No se aceptan parches sin documentación y pruebas. |

---

## 3. Principios

1. **Principio de responsabilidad única** — cada clase hace una cosa y la hace bien.
2. **Principio de mínimo conocimiento** — una clase no conoce los detalles internos de otras.
3. **Principio de consistencia** — mismos patrones de nomenclatura, mismos tipos de retorno, mismo manejo de errores en toda la jerarquía.
4. **Principio de tolerancia** — todas las comparaciones usan tolerancia configurable; nunca `==` directo sobre `float`.
5. **Principio de publicabilidad** — el kernel debe poder empaquetarse y publicarse en PyPI sin modificaciones.
6. **Principio de preparación 3D** — aunque LINPRO es primariamente 2D, el kernel soporta coordenadas Z opcionales para evitar retrabajos futuros.

---

## 4. Convenciones

### Nombres

- **Clases**: PascalCase (`Point`, `BoundingBox`, `Polyline`)
- **Métodos**: snake_case (`distance_to`, `to_wkt`)
- **Propiedades**: snake_case (`p.x`, `seg.length`)
- **Constantes**: UPPER_SNAKE_CASE (`EPSILON`, `ANGLE_EPSILON`)
- **Atributos privados**: prefijo `_` (`_x`, `_points`)
- **Alias de tipos**: prefijo `_` (uso interno, no parte de la API pública): `_Coord`, `_Tuple3`

### Archivos

- Un archivo por clase, nombrado en snake_case: `point.py`, `bounding_box.py`
- Excepción: clases muy pequeñas y estrechamente acopladas pueden coexistir (ej. excepciones).

### Imports

- `from __future__ import annotations` siempre, para evaluación perezosa de tipos.
- Imports absolutos desde `linpro.geometry`.
- No se permite `from typing import ...` donde se pueda usar la sintaxis nativa (`list`, `dict`, `tuple`, `int | float`).

---

## 5. Sistema de coordenadas

### Espacio de trabajo

- Sistema cartesiano 2D/3D.
- No se asume ningún sistema de referencia geodésico (CRS). El kernel trabaja en coordenadas proyectadas (UTM, por ejemplo) pero no valida ni conoce el CRS.
- El eje X corresponde a la abscisa (Este en UTM).
- El eje Y corresponde a la ordenada (Norte en UTM).
- El eje Z es opcional y representa cota/elevación.

### Coordenadas

- **Todas las coordenadas son `float`**. Si se recibe `int`, se convierte a `float` en el constructor.
- **Z opcional**: `Point(x, y)` crea un punto 2D con `z=0.0`. `Point(x, y, z)` crea un punto 3D.
- **Rango**: no hay límite de rango (coordenadas UTM pueden ser grandes).
- **NaN e Inf**: prohibidos. El constructor los rechaza con `InvalidCoordinateError`.

### Convención de ángulos

- Ángulos en **radianes** en toda la API.
- Sentido positivo: antihorario (matemático).
- Rango normalizado: `[-π, π]` o `[0, 2π)` según convenga al método.

---

## 6. Precisión

Tres niveles de precisión definidos en `kernel/constants.py`:

| Nivel | Constante | Valor | Uso |
|---|---|---|---|
| Matemática | `MATHEMATICAL_EPSILON` | `1e-12` | Operaciones aritméticas internas (producto escalar, normalización, determinantes). |
| Geométrica | `EPSILON` | `1e-9` | Comparaciones entre entidades geométricas (punto igual a punto, punto sobre segmento, proyecciones). Es la tolerancia por defecto de todo el kernel. |
| Visual/CAD | `VISUAL_EPSILON` | `1e-6` | Operaciones de dibujo, snap, exportación CAD. Tolerancia más permisiva para display. |

| Helper | Constante | Valor | Uso específico |
|---|---|---|---|
| Angular | `ANGLE_EPSILON` | `1e-10` | Comparación de ángulos. Más restrictiva porque pequeñas diferencias angulares importan en ingeniería. |
| Distancia | `DISTANCE_EPSILON` | `1e-8` | Comparación de distancias. Un orden por debajo de la geométrica. |

---

## 7. Tolerancias

La clase `Tolerance` (`kernel/tolerance.py`) provee métodos estáticos para todas las comparaciones:

```python
Tolerance.almost_equal(a, b, tol=EPSILON)          # isclose con rel y abs
Tolerance.almost_zero(a, tol=EPSILON)               # isclose(a, 0)
Tolerance.angle_almost_equal(a, b)                  # con ANGLE_EPSILON
Tolerance.distance_almost_equal(a, b)               # con DISTANCE_EPSILON
Tolerance.less_or_equal(a, b, tol=EPSILON)          # a <= b + tol
Tolerance.greater_or_equal(a, b, tol=EPSILON)       # a >= b - tol
Tolerance.in_range(value, low, high, tol=EPSILON)   # low-tol <= value <= high+tol
```

### Reglas de tolerancia

1. Toda clase que implemente `__eq__` debe usar `math.isclose` con `EPSILON` (o su propia tolerancia).
2. Toda clase debe exponer un método `almost_equal(other, tol)` para comparación con tolerancia explícita.
3. Métodos geométricos (`contains_point`, `intersects`, `is_parallel`) deben aceptar un parámetro `tol` opcional.
4. La tolerancia por defecto para cualquier operación es `EPSILON` (1e-9).

---

## 8. Inmutabilidad

Todas las entidades geométricas son inmutables.

### Reglas

1. Los atributos se establecen en `__init__` y nunca cambian.
2. Las propiedades (`x`, `y`, `z`, `points`) son de solo lectura.
3. No hay setters públicos.
4. No hay métodos que muten el objeto (`translate`, `rotate`, `scale`) — devuelven una **nueva instancia**.
5. Las clases son hashables si tienen sentido semántico (Point sí, Polyline no, por su tamaño).

### Beneficios buscados

- Sin efectos secundarios al pasar objetos a funciones.
- Seguridad en contenedores (sets, dicts).
- Facilidad para caching (Polyline cachea su longitud, pero al ser la polyline inmutable, la caché es válida para siempre).
- Facilidad para paralelismo futuro.

---

## 9. Comparaciones

### Igualdad vs equivalencia geométrica

| Concepto | Método | Descripción |
|---|---|---|
| **Igualdad** | `__eq__` | Mismas coordenadas dentro de tolerancia. Propiedades y tipo deben coincidir. |
| **Equivalencia geométrica** | `almost_equal(other, tol)` | Mismas coordenadas con tolerancia explícita. Útil cuando se necesita comparar con diferente precisión. |

### Contratos de `__eq__`

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, type(self)):
        return NotImplemented
    # comparación coordinate a coordinate con math.isclose
```

- No se permite `self is other` como optimización (rompe la predicibilidad en entornos distribuitos).
- No se permite `return NotImplemented` para tipos incomparables (ya se hace por tipo).

---

## 10. Entidades geométricas

### Jerarquía de clases

```
Geometry (abstract)
│
├── Point              — Coordenada (x, y, z)
├── Vector             — Dirección (dx, dy)
├── Segment            — Recta entre dos puntos
├── BoundingBox        — Caja alineada a ejes (xmin, ymin, xmax, ymax)
│
├── Curve (abstract)
│   ├── Line           — Línea recta infinita
│   ├── Polyline       — Secuencia de Segmentos consecutivos
│   ├── Arc            — Arco circular (futuro)
│   └── Circle         — Círculo completo (futuro)
│
├── Surface (abstract)
│   └── Polygon        — Polígono cerrado (futuro)
│
└── Solid (futuro)
```

### Descripción de entidades

| Clase | Dimensión | Inmutable | Hashable | Descripción |
|---|---|---|---|---|
| `Geometry` | — | sí | no | Clase base abstracta. Define contratos `almost_equal`, `to_dict`, `from_dict`, `to_wkt`, `check_invariants`. |
| `Point` | 0D | sí | sí | Coordenada cartesiana (x, y, z). |
| `Vector` | 0D | sí | sí | Desplazamiento (dx, dy). Sin origen, solo magnitud y dirección. |
| `Segment` | 1D | sí | sí | Porción de recta entre dos puntos. |
| `BoundingBox` | 2D | sí | sí | Caja delimitadora alineada a ejes. |
| `Line` | 1D | sí | no | Recta infinita definida por dos puntos o punto+dirección. |
| `Polyline` | 1D | sí | no | Secuencia ordenada de puntos conectados por segmentos. Clase reina del motor. |
| `Arc` | 1D | sí | no | Arco circular (futuro). |
| `Circle` | 1D | sí | sí | Círculo definido por centro y radio (futuro). |
| `Polygon` | 2D | sí | no | Polígono cerrado (futuro). |

---

## 11. Relaciones entre clases

### Punto y Vector

```python
Vector.from_points(Point(0,0), Point(3,4))  # → Vector(3,4)
Point(1,2) + Vector(3,4)                    # → Point(4,6)
Point(1,2) - Point(3,4)                     # → Vector(-2,-2) Futuro
```

### Segmento

```python
Segment(start=Point(0,0), end=Point(10,0))
seg.point_at(5.0)      # → Point(5,0)
seg.distance_to_point(p)
seg.intersection(other)
```

### Polyline

```python
Polyline([Point(0,0), Point(5,0), Point(10,5)])
poly.length            # → float (calculado, cachead
poly.point_at_pk(5.0)  # → Point en el PK
poly.segments          # → list[Segment] (calculada, cachead
poly.simplify()        # → Polyline simplificada (nueva instancia)
poly.offset(d)         # → Polyline desplazada (nueva instancia)
poly.buffer(d)         # → list[Polyline] (norte y sur)
```

### BoundingBox

```python
bbox = BoundingBox.from_points([p1, p2, p3])
bbox.contains_point(p)          # bool
bbox.intersects(other_bbox)     # bool
bbox.union(other_bbox)          # BoundingBox
```

---

## 12. Convenciones de nombres

### Métodos estándar por clase

| Operación | Método | Retorno |
|---|---|---|
| Distancia a otro punto | `distance_to(other)` | `float ≥ 0` |
| Distancia perpendicular | `distance_to_point(point)` | `float` |
| Punto en parámetro | `point_at(t)` | `Point` |
| Punto en PK | `point_at_pk(pk)` | `Point` |
| Proyección de punto | `project(point)` | `(Point, float)` |
| Intersección | `intersection(other)` | `Point | None` |
| Intersección booleana | `intersects(other)` | `bool` |
| Contiene punto | `contains_point(point)` | `bool` |
| Traslación | `translate(dx, dy)` | `Self` (nueva instancia) |
| Rotación | `rotate(angle, center=None)` | `Self` (nueva instancia) |
| Escalado | `scale(factor, center=None)` | `Self` (nueva instancia) |
| Serialización | `to_dict()`, `to_json()`, `to_wkt()` | `dict`, `str`, `str` |
| Deserialización | `from_dict(data)`, `from_json(data)` | `Self` |
| Invariantes | `check_invariants()` | `None` (lanza si falla) |
| Representación | `__repr__`, `__str__` | `str` |

### Propiedades estándar

| Propiedad | Retorno | Descripción |
|---|---|---|
| `.x`, `.y`, `.z` | `float` | Coordenadas |
| `.length` | `float` | Longitud (Segment, Polyline) |
| `.midpoint` | `Point` | Punto medio (Segment) |
| `.direction` | `Vector` | Vector unitario (Segment, Line) |
| `.angle` | `float` | Ángulo en radianes (Vector, Segment) |
| `.start`, `.end` | `Point` | Extremos (Segment, Line) |
| `.points` | `tuple[Point, ...]` | Vértices (Polyline) |
| `.segments` | `tuple[Segment, ...]` | Segmentos (Polyline) |
| `.bbox` | `BoundingBox` | Caja delimitadora (cualquier entidad) |
| `.center` | `Point` | Centro geométrico |

---

## 13. Excepciones

Todas las excepciones del Geometry Engine heredan de `GeometryError`:

```
GeometryError (Exception)
├── InvalidCoordinateError   — coordenada NaN, inf, tipo incorrecto
├── PrecisionError           — error de precisión en operación
└── ValidationError          — error de validación geométrica
```

### Reglas

1. Ninguna clase del kernel lanza `ValueError` o `TypeError` directamente. Siempre se usan las excepciones propias.
2. Las excepciones llevan mensajes descriptivos en español o inglés (decidir por clase, consistencia intraclase).
3. Las excepciones de validación incluyen el nombre del parámetro y el valor recibido cuando es posible.
4. No se definen excepciones por entidad. Las cuatro excepciones del kernel cubren todos los casos.

---

## 14. Serialización

### Formatos soportados (núcleo)

| Formato | Método | Descripción |
|---|---|---|
| Tupla | `to_tuple()` | Para desempaquetado rápido. `(x, y, z)` para Point. |
| Diccionario | `to_dict()` | Para almacenamiento en bases de datos documento. |
| JSON | `to_json(**kwargs)` | Para APIs REST y archivos. |
| WKT | `to_wkt()` | Estándar OGC Well-Known Text. Sin Z, para compatibilidad GIS. |

### Formatos NO implementados en el Kernel

| Formato | Dónde se implementa | Razón |
|---|---|---|
| DXF | Adaptador CAD (`linpro.io`) | Depende de formato AutoCAD |
| SHP | Adaptador GIS | Depende de GeoPandas/Fiona |
| GPKG | Adaptador GIS | Depende de GeoPandas/Fiona |
| GeoJSON | Adaptador GIS | Requiere CRS, dominio de GIS |
| Excel | Adaptador Excel | Depende de openpyxl |

### Contrato de serialización

```python
def to_dict(self) -> dict:
    """Serializa a dict. Debe poder reconstruirse con from_dict."""
    raise NotImplementedError

@classmethod
def from_dict(cls, data: dict) -> Self:
    """Reconstruye desde dict. Los datos deben venir de to_dict."""
    raise NotImplementedError

def to_wkt(self) -> str:
    """Well-Known Text (2D, sin Z)."""
    raise NotImplementedError
```

- `to_dict()` y `from_dict()` deben ser inversos: `T.from_dict(obj.to_dict()) == obj` dentro de tolerancia.
- `to_json()` envuelve `to_dict()` con `json.dumps`.
- `from_json()` envuelve `json.loads` + `from_dict`.

---

## 15. Rendimiento

### Principios

1. **Corrección primero, optimización después.** No se acepta optimización prematura que complique el código.
2. **Caching controlado.** Polyline cachea `length` y `segments` porque son caros de calcular. Al ser inmutable, la caché es segura.
3. **Cálculos perezosos.** Las propiedades calculadas se evalúan la primera vez que se accede y se cachean (por inmutabilidad).
4. **No se usan arrays NumPy.** El kernel debe funcionar sin dependencias externas.
5. **Límite de precisión.** No se realizan operaciones con más de 15 dígitos significativos (precisión nativa de `float`).

### Operaciones etiquetadas por coste

| Operación | Coste | Clase |
|---|---|---|
| `distance_to` | O(1) | Point |
| `length` | O(n) → O(1) cachead | Polyline |
| `segments` | O(n) → O(1) cachead | Polyline |
| `simplify` | O(n log n) | Polyline |
| `offset` | O(n) | Polyline |
| `buffer` | O(n) | Polyline |
| `point_at_pk` | O(log n) con búsqueda binaria | Polyline |

---

## 16. Compatibilidad

### Dentro de LINPRO

- El Geometry Engine no importa nada de `linpro.domain`, `linpro.core` ni ningún otro módulo.
- Los módulos de negocio importan del Geometry Engine, nunca al revés.
- Las dependencias apuntan hacia el centro:

```
domain → geometry (kernel)
io → geometry (kernel)
core → geometry (kernel)
```

### Fuera de LINPRO (PyPI)

- `pip install linpro-geometry` debe funcionar sin instalar LINPRO completo.
- El paquete `linpro_geometry` contendría solo `geometry/` y sus dependencias internas.
- No debe depender de `pyproject.toml` de LINPRO root — tendría su propio `pyproject.toml`.

### Shapely

- No se usa Shapely dentro del Kernel.
- Sí puede usarse en adaptadores GIS para conversión de formatos.
- Si una operación existe tanto en el Kernel como en Shapely, la del Kernel tiene prioridad.

---

## 17. API pública

### Módulo raíz (`linpro.geometry`)

```python
from linpro.geometry import (
    Geometry,
    Point,
    Vector,
    Segment,
    BoundingBox,
    Curve,
    Line,
    Polyline,
)
```

### `__all__` por subpaquete

| Subpaquete | `__all__` |
|---|---|
| `kernel` | `EPSILON`, `ANGLE_EPSILON`, `DISTANCE_EPSILON`, `VISUAL_EPSILON`, `MATHEMATICAL_EPSILON`, `Tolerance`, `Precision`, `Validation`, `Geometry` |
| `exceptions` | `GeometryError`, `InvalidCoordinateError`, `PrecisionError`, `ValidationError` |
| `primitives` | `Point`, `Vector`, `Segment`, `BoundingBox` |
| `curves` | `Curve`, `Line`, `Polyline` |
| `algorithms` | Por definir en sprints posteriores |

### Estabilidad de la API

- La API raíz (`linpro.geometry`) es **estable** una vez publicada la versión 0.3.0.
- Los subpaquetes (`kernel`, `primitives`, `curves`) pueden tener cambios menores hasta 1.0.0.
- Las clases y métodos marcados con guion bajo (`_`) son privados y no forman parte de la API pública.
- El acceso a atributos privados (`_x`) desde fuera de la clase está prohibido.

---

## 18. Reglas para desarrolladores

### Proceso de incorporación de nuevas clases

1. **SPEC** — Documento de requisitos (Requirements.md)
2. **DESIGN** — Documento de diseño (Design.md)
3. **IMPLEMENT** — Código (`clase.py`)
4. **TEST** — Tests unitarios (`test_clase.py`) con cobertura ≥95%
5. **REVIEW** — Revisión: Ruff 0 errores, tipado correcto, cobertura, docs sincronizadas
6. **RELEASE** — Merge a main solo si pasa REVIEW

### CheckList de calidad

- [ ] ¿La clase es inmutable?
- [ ] ¿Tiene `__eq__` con tolerancia?
- [ ] ¿Tiene `almost_equal(other, tol)`?
- [ ] ¿Tiene `to_dict()` y `from_dict()`?
- [ ] ¿Tiene `to_wkt()`?
- [ ] ¿Tiene `check_invariants()`?
- [ ] ¿Tiene `__repr__` y `__str__`?
- [ ] ¿Tiene type hints completos?
- [ ] ¿Usa excepciones propias (`GeometryError` y subclases)?
- [ ] ¿No importa nada de `linpro.domain` ni `linpro.core`?
- [ ] ¿Tiene tests con cobertura ≥95%?
- [ ] ¿Ruff da 0 errores?
- [ ] ¿La documentación está sincronizada?

### Lo que NO debe hacer una clase del Kernel

- No debe leer/escribir archivos
- No debe conectarse a bases de datos
- No debe conocer AutoCAD, DXF, SHP, GPKG, Excel
- No debe importar módulos de negocio (domain, core)
- No debe usar GUI (PySide)
- No debe usar NumPy, Pandas, Shapely, GeoPandas
- No debe tener estado global mutable

---

## 19. Casos prohibidos

| Caso | Prohibido | Alternativa |
|---|---|---|
| `Point.from_dxf(...)` | ❌ | Adaptador CAD en `linpro.io` |
| `Point.to_shapely()` | ❌ | Adaptador GIS |
| `polyline.export_to_excel()` | ❌ | Módulo Excel en `linpro.io` |
| `Polyline.__eq__` comparando arrays | ❌ | `almost_equal` con tolerancia |
| `Point` modificable | ❌ | Inmutable con propiedades |
| `Vector` con origen anclado | ❌ | Vector es solo desplazamiento |
| `float` como PK | ❌ | Tipo `PK` propio en `domain` |
| imports circulares | ❌ | Las primitivas no importan curvas |
| `__slots__` en clases base | ⚠️ | Solo en clases hoja si es necesario |

---

## 20. Roadmap

### Sprint 3.1 — Geometry Kernel ✅

| Entregable | Estado |
|---|---|
| GEOMETRY_KERNEL_SPEC.md | ✅ Completado |
| kernel/ (constants, tolerance, precision, validation, geometry) | ✅ |
| Excepciones propias | ✅ |
| Point (especificación + implementación + tests) | ✅ |

### Sprint 3.2 — Primitivas

| Entregable | Prioridad |
|---|---|
| Vector | Alta |
| Segment | Alta |
| BoundingBox | Alta |

### Sprint 3.3 — Curvas

| Entregable | Prioridad |
|---|---|
| Curve (abstracta) | Alta |
| Line | Alta |
| Polyline | **Crítica** |
| Arc | Baja |

### Sprint 3.4 — Algoritmos I

| Entregable | Prioridad |
|---|---|
| Distancias (punto-punto, punto-segmento, punto-polyline) | Alta |
| Intersecciones (segmento-segmento, segmento-polyline) | Alta |
| Proyección de punto sobre curva | Alta |
| PK Engine (cálculo de estaciones) | **Crítica** |

### Sprint 3.5 — Algoritmos II

| Entregable | Prioridad |
|---|---|
| Offset de Polyline | Alta |
| Buffer de Polyline | Alta |
| Simplificación (Ramer-Douglas-Peucker) | Alta |
| Cálculo de ángulos internos | Media |

### Sprint 3.6 — Publicación PyPI

| Entregable | Prioridad |
|---|---|
| Empaquetado `linpro-geometry` | Alta |
| CI/CD para PyPI | Alta |
| Documentación de usuario | Alta |

---

*Este documento es la Constitución del Geometry Engine de LINPRO. Cualquier cambio requiere revisión de arquitectura.*
