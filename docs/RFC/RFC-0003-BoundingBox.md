# RFC-0003: BoundingBox

**Estado:** Pendiente de aprobación
**Autor:** Lead Developer
**Fecha:** 2026-07-10
**Requiere:** RFC-0001 (Geometry Kernel) — Aprobado

---

## 1. Definición

BoundingBox es una entidad geométrica **inmutable** que representa una caja
delimitadora alineada a los ejes (Axis-Aligned Bounding Box, AABB) en 2D.

Está definida por cuatro coordenadas:

- `xmin` — mínimo X (esquina inferior izquierda)
- `ymin` — mínimo Y
- `xmax` — máximo X (esquina superior derecha)
- `ymax` — máximo Y

BoundingBox es una entidad de **primer nivel** en el Geometry Engine, no un
simple contenedor de floats. Aparece en el contrato de `Geometry.bbox` y
será utilizada por absolutamente todas las entidades geométricas: Point,
Vector, Segment, Line, Polyline, Polygon, Arc, Circle, y por los futuros
algoritmos de intersección, índices espaciales (RTree) y operaciones GIS.

---

## 2. Responsabilidades

### Debe hacer (GEOM-BBOX-001 a GEOM-BBOX-020)

| ID | Responsabilidad |
|---|---|
| GEOM-BBOX-001 | Almacenar xmin, ymin, xmax, ymax como `float` |
| GEOM-BBOX-002 | Exponer xmin, ymin, xmax, ymax como propiedades de solo lectura |
| GEOM-BBOX-003 | Validar que xmin ≤ xmax e ymin ≤ ymax en construcción |
| GEOM-BBOX-004 | Rechazar coordenadas NaN, Inf o tipo incorrecto |
| GEOM-BBOX-005 | Calcular `width` → xmax - xmin |
| GEOM-BBOX-006 | Calcular `height` → ymax - ymin |
| GEOM-BBOX-007 | Calcular `area` → width * height |
| GEOM-BBOX-008 | Calcular `center` → Point en el centro geométrico |
| GEOM-BBOX-009 | Compararse con tolerancia vía `__eq__` |
| GEOM-BBOX-010 | Exponer `almost_equal(other, tol)` para tolerancia explícita |
| GEOM-BBOX-011 | Determinar si contiene un Point: `contains_point(point)` |
| GEOM-BBOX-012 | Determinar si contiene otro BoundingBox: `contains_bbox(other)` |
| GEOM-BBOX-013 | Determinar si interseca otro BoundingBox: `intersects(other)` |
| GEOM-BBOX-014 | Calcular la unión con otro BoundingBox: `union(other)` |
| GEOM-BBOX-015 | Calcular la intersección con otro BoundingBox: `intersection(other)` |
| GEOM-BBOX-016 | Expandir uniformemente por un margen: `expand(margin)` |
| GEOM-BBOX-017 | Construir desde una lista de puntos: `from_points(points)` |
| GEOM-BBOX-018 | Implementar `Geometry(ABC)` (heredar de la clase base) |
| GEOM-BBOX-019 | Serializar a dict/JSON/WKT y deserializar desde dict/JSON |
| GEOM-BBOX-020 | Exponer `is_empty` → True si width ≤ 0 o height ≤ 0 |

### Debe NO hacer (GEOM-BBOX-NO-001 a GEOM-BBOX-NO-005)

| ID | Exclusión |
|---|---|
| GEOM-BBOX-NO-001 | No debe rotar (es AABB, no OBB) |
| GEOM-BBOX-NO-002 | No debe conocer CRS / proyecciones |
| GEOM-BBOX-NO-003 | No debe hacer dibujo ni render |
| GEOM-BBOX-NO-004 | No debe leer/escribir archivos |
| GEOM-BBOX-NO-005 | No debe contener IDs de entidades ni referencias a objetos de dominio |

---

## 3. Invariantes (GEOM-BBOX-INV-001 a GEOM-BBOX-INV-006)

| ID | Invariante | Exigencia |
|---|---|---|
| GEOM-BBOX-INV-001 | `xmin`, `ymin`, `xmax`, `ymax` son `float` (o convertibles) | Error si no |
| GEOM-BBOX-INV-002 | `xmin ≤ xmax` (dentro de tolerancia) | `ValidationError` |
| GEOM-BBOX-INV-003 | `ymin ≤ ymax` (dentro de tolerancia) | `ValidationError` |
| GEOM-BBOX-INV-004 | Ninguna coordenada es NaN o Infinity | `InvalidCoordinateError` |
| GEOM-BBOX-INV-005 | El objeto es inmutable (sin setters) | `AttributeError` si se intenta asignar |
| GEOM-BBOX-INV-006 | `to_dict` y `from_dict` son inversos | Siempre verdadero dentro de tolerancia |

---

## 4. API pública completa

### 4.1 Constructor

```python
def __init__(self, xmin: int | float, ymin: int | float,
             xmax: int | float, ymax: int | float) -> None
```

| Parámetro | Tipo | Default | GEOM-BBOX |
|---|---|---|---|
| xmin | int \| float | obligatorio | 001 |
| ymin | int \| float | obligatorio | 001 |
| xmax | int \| float | obligatorio | 001 |
| ymax | int \| float | obligatorio | 001 |

Lanza:
- `InvalidCoordinateError` si xmin, ymin, xmax, ymax no son finitos
- `ValidationError` si `xmin > xmax` o `ymin > ymax`

### 4.2 Propiedades

| Propiedad | Tipo | GEOM-BBOX | Complejidad |
|---|---|---|---|
| `.xmin` | float | 002 | O(1) |
| `.ymin` | float | 002 | O(1) |
| `.xmax` | float | 002 | O(1) |
| `.ymax` | float | 002 | O(1) |
| `.width` | float | 005 | O(1) |
| `.height` | float | 006 | O(1) |
| `.area` | float | 007 | O(1) |
| `.center` | Point | 008 | O(1) |
| `.dimension` | int | 018 (Geometry) | O(1) |
| `.is_empty` | bool | 020 | O(1) |
| `.bbox` | BoundingBox | 018 (Geometry) | O(1) → self |
| `.is_valid` | bool | 018 (Geometry) | O(1) |

### 4.3 Métodos de instancia

| Método | Retorno | GEOM-BBOX | Complejidad |
|---|---|---|---|
| `contains_point(point)` | bool | 011 | O(1) |
| `contains_bbox(other)` | bool | 012 | O(1) |
| `intersects(other)` | bool | 013 | O(1) |
| `union(other)` | BoundingBox | 014 | O(1) |
| `intersection(other)` | BoundingBox \| None | 015 | O(1) |
| `expand(margin)` | BoundingBox | 016 | O(1) |
| `copy()` | BoundingBox | 018 | O(1) |
| `to_tuple()` | (xmin, ymin, xmax, ymax) | 019 | O(1) |
| `to_dict()` | dict | 019 | O(1) |
| `to_json(**kwargs)` | str | 019 | O(1) |
| `to_wkt()` | str | 019 | O(1) — como POLYGON |
| `check_invariants()` | None | — | O(1) |

### 4.4 Métodos de clase

| Método | Retorno | GEOM-BBOX | Complejidad |
|---|---|---|---|
| `from_tuple(data)` | BoundingBox | 019 | O(1) |
| `from_dict(data)` | BoundingBox | 019 | O(1) |
| `from_json(data)` | BoundingBox | 019 | O(1) |
| `from_points(points)` | BoundingBox | 017 | O(n) |
| `empty()` | BoundingBox | — | O(1) → BoundingBox(0,0,0,0) |

### 4.5 Métodos especiales

| Método | GEOM-BBOX | Complejidad |
|---|---|---|
| `__eq__(other)` | 009 | O(1) |
| `__hash__()` | — | O(1) |
| `__repr__()` | — | O(1) |
| `__str__()` | — | O(1) |

### 4.6 Formato WKT

BoundingBox se serializa a WKT como POLYGON cerrado en sentido antihorario:

```
POLYGON ((xmin ymin, xmax ymin, xmax ymax, xmin ymax, xmin ymin))
```

### 4.7 Formato dict

```json
{
    "xmin": 10.0,
    "ymin": 20.0,
    "xmax": 30.0,
    "ymax": 50.0
}
```

---

## 5. Complejidad temporal

| Operación | Coste | Explicación |
|---|---|---|
| `BoundingBox(xmin, ymin, xmax, ymax)` | O(1) | 4 asignaciones + validación |
| `.xmin`, `.ymin`, `.xmax`, `.ymax` | O(1) | Retorno de atributo privado |
| `.width`, `.height` | O(1) | 1 resta |
| `.area` | O(1) | 1 multiplicación |
| `.center` | O(1) | 2 sumas, 2 divisiones, 1 Point |
| `.contains_point(p)` | O(1) | 4 comparaciones |
| `.contains_bbox(other)` | O(1) | 4 comparaciones |
| `.intersects(other)` | O(1) | 4 comparaciones |
| `.union(other)` | O(1) | 4 mins/max, 1 BoundingBox |
| `.intersection(other)` | O(1) | 4 mins/max, 1 BoundingBox o None |
| `.expand(margin)` | O(1) | 4 sumas/restas, 1 BoundingBox |
| `from_points(lista)` | O(n) | 2 scans de n puntos |
| `__eq__` | O(1) | 4 × `math.isclose` |
| `to_dict()` | O(1) | Construcción de dict de 4 claves |
| `from_dict(data)` | O(1) | Acceso a 4 claves |

Todas las operaciones son O(1) excepto `from_points` que es O(n).

---

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Caja degenerada** (xmin ≈ xmax) | Operaciones como `area` devuelven ~0 | `is_empty` lo detecta; no se lanza error |
| **BoundingBox gigantesco** (coordenadas UTM extremas) | `width * height` puede desbordar | `area` devuelve `float`; Python maneja big floats |
| **Confundir orden (ymin/ymax vs xmin/xmax)** | Caja incorrecta silenciosamente | Validación en constructor: `xmin ≤ xmax`, `ymin ≤ ymax` |
| **`intersects` con cajas tangentes** | Falso negativo si solo se tocan en un borde | Usar `≤`/`≥` en lugar de `<`/`>` |
| **`from_points` con lista vacía** | Error de índice | Documentar que requiere ≥ 1 punto; lanzar `ValidationError` |

---

## 7. Lista completa de casos de prueba (GEOM-BBOX-TEST)

### 7.1 Creación (GEOM-BBOX-TEST-001 a 010)

| ID | Escenario | Entrada | Esperado |
|---|---|---|---|
| 001 | Creación básica | `BoundingBox(10, 20, 30, 40)` | xmin=10, ymin=20, xmax=30, ymax=40 |
| 002 | Creación con enteros | `BoundingBox(0, 0, 100, 100)` | xmin=0.0 (float) |
| 003 | Creación con floats | `BoundingBox(10.5, 20.5, 30.5, 40.5)` | valores exactos |
| 004 | Creación con negativos | `BoundingBox(-100, -200, -10, -50)` | válido |
| 005 | Creación con cero | `BoundingBox(0, 0, 0, 0)` | válido (caja vacía) |
| 006 | Creación desde Geometry.from_dict | `Geometry.from_dict({"type": "BoundingBox", ...})` | BoundingBox válido |
| 007 | Creación sin orden xmin>xmax | `BoundingBox(30, 20, 10, 40)` | `ValidationError` |
| 008 | Creación sin orden ymin>ymax | `BoundingBox(10, 40, 30, 20)` | `ValidationError` |
| 009 | Creación con NaN en xmin | `BoundingBox(float("nan"), 0, 10, 10)` | `InvalidCoordinateError` |
| 010 | Creación con Inf en ymax | `BoundingBox(0, 0, 10, float("inf"))` | `InvalidCoordinateError` |

### 7.2 Propiedades (GEOM-BBOX-TEST-011 a 020)

| ID | Escenario | Entrada | Esperado |
|---|---|---|---|
| 011 | width positiva | `BoundingBox(10, 20, 30, 40)` | width=20 |
| 012 | height positiva | `BoundingBox(10, 20, 30, 40)` | height=20 |
| 013 | area positiva | `BoundingBox(10, 20, 30, 40)` | area=400 |
| 014 | center | `BoundingBox(0, 0, 10, 10).center` | Point(5, 5) |
| 015 | width cero | `BoundingBox(10, 0, 10, 10)` | width=0 |
| 016 | height cero | `BoundingBox(0, 10, 10, 10)` | height=0 |
| 017 | area cero | `BoundingBox(0, 0, 0, 0)` | area=0 |
| 018 | center con negativos | `BoundingBox(-10, -10, 10, 10).center` | Point(0, 0) |
| 019 | is_empty width=0 | `BoundingBox(5, 5, 5, 10)` | True |
| 020 | is_empty con valores normales | `BoundingBox(0,0,10,10)` | False |

### 7.3 Inmutabilidad (GEOM-BBOX-TEST-021 a 024)

| ID | Escenario | Esperado |
|---|---|---|
| 021 | Asignar a xmin | `AttributeError` |
| 022 | Asignar a ymin | `AttributeError` |
| 023 | Asignar a xmax | `AttributeError` |
| 024 | Asignar a ymax | `AttributeError` |

### 7.4 contains (GEOM-BBOX-TEST-025 a 032)

| ID | Escenario | Esperado |
|---|---|---|
| 025 | Point dentro | `BoundingBox(0,0,10,10).contains_point(Point(5,5))` → True |
| 026 | Point fuera (izquierda) | `BoundingBox(0,0,10,10).contains_point(Point(-1,5))` → False |
| 027 | Point fuera (arriba) | `BoundingBox(0,0,10,10).contains_point(Point(5,15))` → False |
| 028 | Point en borde | `BoundingBox(0,0,10,10).contains_point(Point(10,5))` → True |
| 029 | Point en esquina | `BoundingBox(0,0,10,10).contains_point(Point(0,0))` → True |
| 030 | contains_bbox idéntico | `a.contains_bbox(a)` → True |
| 031 | contains_bbox interno | `a.contains_bbox(BoundingBox(1,1,9,9))` → True |
| 032 | contains_bbox externo | `a.contains_bbox(BoundingBox(-1,-1,11,11))` → False |

### 7.5 intersects (GEOM-BBOX-TEST-033 a 038)

| ID | Escenario | Esperado |
|---|---|---|
| 033 | Cajas que se solapan | `BoundingBox(0,0,10,10).intersects(BoundingBox(5,5,15,15))` → True |
| 034 | Cajas separadas | `BoundingBox(0,0,5,5).intersects(BoundingBox(10,10,15,15))` → False |
| 035 | Cajas tangentes (borde común) | `BoundingBox(0,0,10,10).intersects(BoundingBox(10,0,20,10))` → True |
| 036 | Caja contenida | `BoundingBox(0,0,10,10).intersects(BoundingBox(2,2,8,8))` → True |
| 037 | Caja contenedora | `BoundingBox(0,0,10,10).intersects(BoundingBox(-5,-5,15,15))` → True |
| 038 | Misma caja | `a.intersects(a)` → True |

### 7.6 union (GEOM-BBOX-TEST-039 a 043)

| ID | Escenario | Esperado |
|---|---|---|
| 039 | Unión de cajas separadas | `BoundingBox(0,0,5,5).union(BoundingBox(10,10,15,15))` → BoundingBox(0,0,15,15) |
| 040 | Unión de cajas solapadas | `BoundingBox(0,0,10,10).union(BoundingBox(5,5,15,15))` → BoundingBox(0,0,15,15) |
| 041 | Unión consigo misma | `a.union(a)` → a |
| 042 | Unión con caja contenida | `BoundingBox(0,0,10,10).union(BoundingBox(2,2,8,8))` → BoundingBox(0,0,10,10) |
| 043 | Unión con caja contenedora | `BoundingBox(2,2,8,8).union(BoundingBox(0,0,10,10))` → BoundingBox(0,0,10,10) |

### 7.7 intersection (GEOM-BBOX-TEST-044 a 050)

| ID | Escenario | Esperado |
|---|---|---|
| 044 | Intersección de cajas solapadas | `BoundingBox(0,0,10,10).intersection(BoundingBox(5,5,15,15))` → BoundingBox(5,5,10,10) |
| 045 | Intersección de cajas separadas | `BoundingBox(0,0,5,5).intersection(BoundingBox(10,10,15,15))` → None |
| 046 | Intersección consigo misma | `a.intersection(a)` → a |
| 047 | Intersección con caja contenida | `BoundingBox(0,0,10,10).intersection(BoundingBox(2,2,8,8))` → BoundingBox(2,2,8,8) |
| 048 | Intersección de cajas tangentes | `BoundingBox(0,0,10,10).intersection(BoundingBox(10,0,20,10))` → BoundingBox(10,0,10,10) (área 0) |
| 049 | Intersección con None (justo uno toca) | `BoundingBox(0,0,5,5).intersection(BoundingBox(5,5,10,10))` → None |
| 050 | Intersección devuelve None correctamente | Verificar type es `NoneType` cuando no hay solapamiento |

### 7.8 expand (GEOM-BBOX-TEST-051 a 054)

| ID | Escenario | Entrada | Esperado |
|---|---|---|---|
| 051 | Expand positivo | `BoundingBox(5,5,10,10).expand(2)` | BoundingBox(3,3,12,12) |
| 052 | Expand negativo (contraer) | `BoundingBox(0,0,10,10).expand(-2)` | BoundingBox(2,2,8,8) |
| 053 | Expand cero | `BoundingBox(0,0,10,10).expand(0)` | mismo BoundingBox |
| 054 | Expand negativo que invierte orden | `BoundingBox(5,5,10,10).expand(-10)` | No válido (se permitiría, pero is_empty=True) |

### 7.9 from_points (GEOM-BBOX-TEST-055 a 058)

| ID | Escenario | Esperado |
|---|---|---|
| 055 | Un solo punto | `BoundingBox.from_points([Point(5,10)])` → BoundingBox(5,10,5,10) |
| 056 | Múltiples puntos | `BoundingBox.from_points([Point(0,0), Point(10,20), Point(5,5)])` → BoundingBox(0,0,10,20) |
| 057 | Puntos en línea recta horizontal | `BoundingBox.from_points([Point(0,5), Point(10,5)])` → BoundingBox(0,5,10,5) (height=0) |
| 058 | Lista vacía | `BoundingBox.from_points([])` → `ValidationError` |

### 7.10 Igualdad y hash (GEOM-BBOX-TEST-059 a 064)

| ID | Escenario | Esperado |
|---|---|---|
| 059 | `==` con mismo BoundingBox | `BoundingBox(1,2,3,4) == BoundingBox(1.0,2.0,3.0,4.0)` → True |
| 060 | `==` con tolerancia | `BoundingBox(1,2,3,4) == BoundingBox(1.0000000005,2,3,4)` → True |
| 061 | `!=` | `BoundingBox(1,2,3,4) != BoundingBox(5,6,7,8)` → True |
| 062 | `==` con otro tipo | `BoundingBox(0,0,10,10) == "POLYGON(...)"` → False (no TypeError) |
| 063 | hash consistente | `hash(BoundingBox(1,2,3,4)) == hash(BoundingBox(1.0,2.0,3.0,4.0))` → True |
| 064 | hash en set | `len({BoundingBox(0,0,10,10), BoundingBox(0,0,10,10)})` → 1 |

### 7.11 Serialización (GEOM-BBOX-TEST-065 a 074)

| ID | Escenario | Esperado |
|---|---|---|
| 065 | `to_tuple()` | `(1.0, 2.0, 3.0, 4.0)` |
| 066 | `to_dict()` | `{"xmin": 1.0, "ymin": 2.0, "xmax": 3.0, "ymax": 4.0}` |
| 067 | `to_json()` | JSON con xmin, ymin, xmax, ymax |
| 068 | `to_wkt()` | `"POLYGON ((1 2, 3 2, 3 4, 1 4, 1 2))"` |
| 069 | `from_tuple((1,2,3,4))` → `to_tuple()` | Roundtrip exacto |
| 070 | `from_dict({"xmin":1,"ymin":2,"xmax":3,"ymax":4})` → `to_dict()` | Roundtrip exacto |
| 071 | `from_json(...)` → `to_json()` | Roundtrip exacto |
| 072 | `from_tuple((1,2,3))` (3 elementos) | `GeometryError` |
| 073 | `from_dict({"xmin":1})` (faltan claves) | `KeyError` |
| 074 | `from_dict({"xmin":1,"ymin":2,"xmax":"a","ymax":4})` | `InvalidCoordinateError` |

### 7.12 Geometry Contract (GEOM-BBOX-TEST-075 a 083)

| ID | Escenario | Esperado |
|---|---|---|
| 075 | `isinstance(bb, Geometry)` | True |
| 076 | `bb.dimension` | 2 |
| 077 | `bb.bbox is bb` | True (un BoundingBox de sí mismo es él mismo) |
| 078 | `bb.is_valid` | True |
| 079 | `bb.is_empty` (width=0) | True |
| 080 | `bb.copy()` | BoundingBox igual, objeto distinto |
| 081 | `to_dict()` → `from_dict()` roundtrip | True |
| 082 | `to_json()` → `from_json()` roundtrip | True |
| 083 | `str(bb) == repr(bb)` | True |

### 7.13 Invariantes (GEOM-BBOX-TEST-084 a 086)

| ID | Escenario | Esperado |
|---|---|---|
| 084 | `check_invariants()` en BoundingBox válido | No lanza |
| 085 | `check_invariants()` después de to_dict/from_dict | No lanza |
| 086 | `check_invariants()` si xmin > xmax | `ValidationError` |

---

## 8. ADRs (Architecture Decision Records)

### ADR-001: Inmutabilidad de BoundingBox

**Contexto:** BoundingBox es una entidad del Geometry Engine que debe poder
compartirse entre múltiples entidades (Polyline.bbox, Segment.bbox, etc.)
sin riesgo de modificación accidental.

**Decisión:** BoundingBox es inmutable. Atributos `_xmin`, `_ymin`, `_xmax`,
`_ymax` son privados. Propiedades de solo lectura. `expand()` y `union()`
devuelven nuevas instancias.

**Consecuencias:**
+ Seguridad en contenedores (sets, dicts)
+ Caching seguro en entidades compuestas
+ Sin efectos secundarios en operaciones encadenadas
- Más allocaciones (cada operación crea un nuevo objeto)

### ADR-002: Validación de orden en constructor

**Contexto:** Un BoundingBox con xmin > xmax o ymin > ymax es inválido.
El error debe detectarse temprano.

**Decisión:** El constructor valida xmin ≤ xmax e ymin ≤ ymax y lanza
`ValidationError` si no se cumple. Se usa tolerancia para permitir
casos límite por error de coma flotante.

**Consecuencias:**
+ Detección temprana de errores
+ Invariante garantizada para toda la vida del objeto
- Pequeño coste de validación en O(1)

### ADR-003: BoundingBox como Geometry de primer nivel

**Contexto:** BoundingBox aparece en el contrato `Geometry.bbox` y es
retornado por todas las entidades geométricas. Debe ser una entidad
de pleno derecho, no un tuple de 4 floats.

**Decisión:** BoundingBox hereda de `Geometry(ABC)` y tiene su propio
`to_dict()`, `from_dict()`, `to_wkt()`, `__eq__`, `__hash__`, etc.

**Consecuencias:**
+ Polimorfismo: `Geometry.bbox` devuelve `Geometry`
+ Serialización coherente con el resto del kernel
+ Operaciones ricas (union, intersection, expand) en lugar de funciones sueltas
- Pequeña sobrecarga de herencia (insignificante)

### ADR-004: is_empty para cajas degeneradas

**Contexto:** Un BoundingBox con width=0 o height=0 es una caja degenerada
(línea, punto o vacía). Algunas operaciones (intersección, contains)
siguen siendo válidas; otras (área) devuelven cero.

**Decisión:** `is_empty` devuelve True si width ≤ 0 o height ≤ 0.
No se lanza error. Las cajas degeneradas son válidas pero marcadas como vacías.

**Consecuencias:**
+ Semántica clara: una caja con área cero existe pero está vacía
+ `from_points` con todos los puntos iguales produce una caja vacía válida
+ Los algoritmos pueden consultar `is_empty` antes de operar

### ADR-005: to_wkt como POLYGON

**Contexto:** WKT no tiene un tipo nativo para AABB. La representación
más natural es un POLYGON cerrado.

**Decisión:** `to_wkt()` serializa como `POLYGON ((xmin ymin, xmax ymin, xmax ymax, xmin ymax, xmin ymin))`.

**Consecuencias:**
+ Compatible con sistemas GIS que entienden WKT
+ Redundancia del punto de cierre (OGC exige cerrar polígonos)
+ Un BoundingBox siempre produce un POLYGON válido (no degenerado en área)

---

## 9. No objetivos (reiteración)

BoundingBox NO hará en ninguna versión:

| Funcionalidad | Motivo | Módulo destino |
|---|---|---|
| Rotación (OBB) | El kernel solo maneja AABB | `linpro.geometry.algorithms` (futuro) |
| Transformaciones CRS | El Kernel no conoce proyecciones | `linpro.engine.gis` |
| Lectura/escritura DXF | El Kernel no conoce formatos CAD | `linpro.io.dxf` |
| Lectura/escritura SHP | El Kernel no conoce formatos GIS | `linpro.io.shp` |
| Dibujo / render | GUI | `linpro.app.gui` |
| Índices espaciales (RTree) | Operación de nivel superior | `linpro.geometry.algorithms` |

---

## 10. Compatibilidad futura

BoundingBox garantiza compatibilidad con los siguientes escenarios a lo largo de
todas las versiones 0.x y 1.x:

| Aspecto | Compromiso |
|---|---|
| **Constructor** | `BoundingBox(xmin, ymin, xmax, ymax)` siempre será válido |
| **Propiedades** | `.xmin`, `.ymin`, `.xmax`, `.ymax`, `.width`, `.height`, `.center`, `.area` son estables |
| **Operaciones** | `contains_point`, `contains_bbox`, `intersects`, `union`, `intersection`, `expand` son estables |
| **Serialización** | `to_dict()` / `from_dict()` serán inversos exactos dentro de tolerancia |
| **WKT** | El formato POLYGON de `to_wkt()` es estable |
| **Geometry(ABC)** | BoundingBox seguirá implementando `Geometry` mientras la clase base exista |

### Lo que NO garantiza compatibilidad

- El orden de los parámetros del constructor (`xmin, ymin, xmax, ymax`) es fijo.
- Los formatos de exportación a terceros (DXF, SHP, GeoJSON) no forman parte del contrato.

---

## 11. Resumen de entidades BoundingBox

| Tipo | Rango ID | Cantidad |
|---|---|---|
| Responsabilidades (debe) | GEOM-BBOX-001 a 020 | 20 |
| Responsabilidades (no debe) | GEOM-BBOX-NO-001 a 005 | 5 |
| Invariantes | GEOM-BBOX-INV-001 a 006 | 6 |
| Casos de prueba | GEOM-BBOX-TEST-001 a 086 | 86 |
| ADRs | ADR-001 a 005 | 5 |

---

*Fin del RFC-0003 — BoundingBox*
