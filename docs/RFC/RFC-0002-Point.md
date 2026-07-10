# RFC-0002: Point

**Estado:** Pendiente de aprobación
**Autor:** Software Architect
**Fecha:** 2026-07-09
**Requiere:** RFC-0001 (Geometry Kernel) — Aprobado

---

## 1. Definición

Point es una entidad geométrica **inmutable** que representa una posición
en un espacio cartesiano bidimensional o tridimensional.
Constituye la unidad básica del Geometry Engine de LINPRO.

Todo el resto de entidades geométricas (Vector, Segment, Polyline,
BoundingBox) se construyen a partir de Point.

---

## 2. Responsabilidades

### Debe hacer (GEOM-POINT-001 a GEOM-POINT-015)

| ID | Responsabilidad |
|---|---|
| GEOM-POINT-001 | Almacenar coordenadas (x, y, z) como `float` |
| GEOM-POINT-002 | Permitir z opcional (default 0.0) |
| GEOM-POINT-003 | Exponer x, y, z como propiedades de solo lectura |
| GEOM-POINT-004 | Calcular distancia euclidiana 2D/3D a otro Point |
| GEOM-POINT-005 | Compararse con tolerancia (≈) vía `__eq__` |
| GEOM-POINT-006 | Compararse con tolerancia explícita vía `almost_equal` |
| GEOM-POINT-007 | Ser hashable (poder usarse en sets y como clave dict) |
| GEOM-POINT-008 | Serializar a tupla: `to_tuple()` → (x, y, z) |
| GEOM-POINT-009 | Serializar a dict: `to_dict()` → {"x": ..., "y": ..., "z": ...} |
| GEOM-POINT-010 | Serializar a JSON: `to_json()` → str |
| GEOM-POINT-011 | Serializar a WKT: `to_wkt()` → "POINT (x y)" |
| GEOM-POINT-012 | Deserializar desde tupla: `from_tuple(data)` |
| GEOM-POINT-013 | Deserializar desde dict: `from_dict(data)` |
| GEOM-POINT-014 | Deserializar desde JSON: `from_json(data)` |
| GEOM-POINT-015 | Implementar `Geometry(ABC)` (heredar de la clase base) |

### Debe NO hacer (GEOM-POINT-NO-001 a GEOM-POINT-NO-008)

| ID | Exclusión |
|---|---|
| GEOM-POINT-NO-001 | No debe conocer AutoCAD / DXF |
| GEOM-POINT-NO-002 | No debe conocer Shapely |
| GEOM-POINT-NO-003 | No debe conocer EPSG / CRS |
| GEOM-POINT-NO-004 | No debe conocer GIS / GeoPandas |
| GEOM-POINT-NO-005 | No debe hacer transformaciones CRS |
| GEOM-POINT-NO-006 | No debe hacer dibujo ni render |
| GEOM-POINT-NO-007 | No debe leer/escribir archivos |
| GEOM-POINT-NO-008 | No debe calcular buffers ni offsets |

---

## 3. Invariantes (GEOM-POINT-INV-001 a GEOM-POINT-INV-008)

| ID | Invariante | Exigencia |
|---|---|---|
| GEOM-POINT-INV-001 | `x` es `float` (o convertible) | Error si no |
| GEOM-POINT-INV-002 | `y` es `float` (o convertible) | Error si no |
| GEOM-POINT-INV-003 | `z` es `float` (o convertible); si no se pasa, vale 0.0 | Error si no |
| GEOM-POINT-INV-004 | Ninguna coordenada es NaN | `InvalidCoordinateError` |
| GEOM-POINT-INV-005 | Ninguna coordenada es Infinity | `InvalidCoordinateError` |
| GEOM-POINT-INV-006 | El objeto es inmutable (sin setters) | `AttributeError` si se intenta asignar |
| GEOM-POINT-INV-007 | El hash es estable: `hash(p)` depende de (x, y, z) redondeados a 9 decimales | Mismo hash para puntos ≈ iguales |
| GEOM-POINT-INV-008 | `to_dict` y `from_dict` son inversos: `Point.from_dict(p.to_dict()) ≈ p` | Siempre verdadero dentro de tolerancia |

---

## 4. API pública completa

### 4.1 Constructor

```python
def __init__(self, x: int | float, y: int | float, z: int | float = 0.0) -> None
```

| Parámetro | Tipo | Default | GEOM-POINT |
|---|---|---|---|
| x | int \| float | obligatorio | 001 |
| y | int \| float | obligatorio | 001 |
| z | int \| float | 0.0 | 002 |

Lanza:
- `InvalidCoordinateError` si x, y, z no son finitos (NaN, Inf, tipo incorrecto)

### 4.2 Propiedades

| Propiedad | Tipo | GEOM-POINT | Complejidad |
|---|---|---|---|
| `.x` | float | 003 | O(1) |
| `.y` | float | 003 | O(1) |
| `.z` | float | 003 | O(1) |
| `.dimension` | int | 015 (hereda de Geometry) | O(1) |
| `.is_empty` | bool | 015 | O(1) → siempre False |
| `.bbox` | BoundingBox | 015 | O(1) |
| `.is_valid` | bool | 015 | O(1) |
| `.xy` | tuple[float, float] | — | O(1) |

### 4.3 Métodos de instancia

| Método | Retorno | GEOM-POINT | Complejidad |
|---|---|---|---|
| `distance_to(other: Point)` | float | 004 | O(1) |
| `almost_equal(other, tol)` | bool | 006 | O(1) |
| `to_tuple()` | (float, float, float) | 008 | O(1) |
| `to_dict()` | dict | 009 | O(1) |
| `to_json(**kwargs)` | str | 010 | O(1) |
| `to_wkt()` | str | 011 | O(1) |
| `copy()` | Point | 015 | O(1) |
| `check_invariants()` | None | — | O(1) |

### 4.4 Métodos de clase

| Método | Retorno | GEOM-POINT | Complejidad |
|---|---|---|---|
| `from_tuple(data)` | Point | 012 | O(1) |
| `from_dict(data)` | Point | 013 | O(1) |
| `from_json(data)` | Point | 014 | O(1) |

### 4.5 Métodos especiales

| Método | GEOM-POINT | Complejidad |
|---|---|---|
| `__eq__(other)` | 005 | O(1) |
| `__hash__()` | 007 | O(1) |
| `__repr__()` | — | O(1) |
| `__str__()` | — | O(1) |

### 4.6 Operadores futuros (no implementar en TASK-0003)

| Operación | GEOM-POINT | Sprint previsto |
|---|---|---|
| `p + v` (Point + Vector) | FUT-001 | Sprint 3.3 |
| `p - v` (Point - Vector) | FUT-002 | Sprint 3.3 |
| `p - q` (Point - Point → Vector) | FUT-003 | Sprint 3.3 |
| `p * s` (Point × escalar → Point) | FUT-004 | Futuro |
| `midpoint(other)` | FUT-005 | Sprint 3.3 |
| `translate(dx, dy)` | FUT-006 | Sprint 3.3 |
| `rotate(angle, center)` | FUT-007 | Sprint 3.4 |
| `scale(factor, center)` | FUT-008 | Sprint 3.4 |

---

## 5. Complejidad temporal

| Operación | Coste | Explicación |
|---|---|---|
| `Point(x, y, z)` | O(1) | Asignación + validación de 3 floats |
| `.x`, `.y`, `.z` | O(1) | Retorno de atributo privado |
| `distance_to(other)` | O(1) | 3 restas, 3 productos, 1 suma, 1 sqrt |
| `almost_equal(other, tol)` | O(1) | 3 × `math.isclose` |
| `__eq__(other)` | O(1) | Delega en `almost_equal` |
| `__hash__()` | O(1) | 3 redondeos + hash de tupla |
| `to_tuple()` | O(1) | Construcción de tupla de 3 elementos |
| `to_dict()` | O(1) | Construcción de dict de 3 claves |
| `to_json()` | O(1) | `json.dumps` sobre dict de 3 claves |
| `to_wkt()` | O(1) | Formateo de string |
| `from_tuple(data)` | O(1) | Acceso a 2-3 elementos de tupla |
| `from_dict(data)` | O(1) | Acceso a 2-3 claves de dict |
| `from_json(data)` | O(1) | `json.loads` + `from_dict` |
| `copy()` | O(1) | `Point(self._x, self._y, self._z)` |
| `check_invariants()` | O(1) | 3 × `NumericValidator.assert_finite` |

Todas las operaciones son O(1). Point no itera sobre colecciones.

---

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Coordenadas UTM grandes** (x ~ 500.000, y ~ 4.600.000) | Pérdida de precisión sub-milimétrica en restas de puntos cercanos | Usar `math.isclose` con tolerancia; el Kernel define EPSILON_GEOMETRY = 1e-9 (equivalente a ~0.001 mm en UTM) |
| **Error de coma flotante en `__eq__`** | Dos puntos iguales matemáticamente reportados como diferentes | `__eq__` usa `math.isclose` con EPSILON_GEOMETRY, nunca `==` directo |
| **Hash inestable** | Puntos ≈ iguales tienen diferente hash, rompiendo uso en sets | Hash se calcula sobre valores redondeados a 9 decimales, no sobre los raw floats |
| **Serialización con pérdida** | `to_json` / `from_json` no es inverso exacto por límites de representación JSON | JSON puede transportar hasta 15-17 dígitos significativos, suficiente para precisión milimétrica en UTM |
| **Z olvidada** | Código cliente trata Point como 2D cuando debería ser 3D | Z tiene default 0.0, pero el constructor siempre espera 3 parámetros: `Point(x, y, z=0.0)` |
| **Uso de Point como clave dict inapropiado** | Dos puntos ≈ iguales se consideran claves diferentes | Documentar que `__eq__` usa tolerancia pero `__hash__` también, haciendo que sets de puntos cercanos funcionen correctamente |

---

## 7. Lista completa de casos de prueba (GEOM-POINT-TEST)

### 7.1 Creación (GEOM-POINT-TEST-001 a 008)

| ID | Escenario | Entrada | Esperado |
|---|---|---|---|
| 001 | Creación 2D básica | `Point(10.0, 20.0)` | x=10, y=20, z=0 |
| 002 | Creación 3D | `Point(1.0, 2.0, 3.0)` | z=3.0 |
| 003 | Creación con enteros | `Point(1, 2)` | x=1.0 (float), y=2.0 (float) |
| 004 | Z default | `Point(5, 5)` | z=0.0 |
| 005 | Creación con coordenadas UTM grandes | `Point(500000.123, 4600000.456)` | Sin error, precisión mantenida |
| 006 | Creación con x=0, y=0, z=0 | `Point(0, 0, 0)` | Válido |
| 007 | Creación con coordenadas negativas | `Point(-100.5, -200.3)` | Válido |
| 008 | Creación desde Geometry.from_dict | `Geometry.from_dict({"type": "Point", ...})` | Point válido |

### 7.2 Validación (GEOM-POINT-TEST-009 a 015)

| ID | Escenario | Entrada | Esperado |
|---|---|---|---|
| 009 | NaN en x | `Point(float("nan"), 0)` | `InvalidCoordinateError` |
| 010 | NaN en y | `Point(0, float("nan"))` | `InvalidCoordinateError` |
| 011 | NaN en z | `Point(0, 0, float("nan"))` | `InvalidCoordinateError` |
| 012 | Infinito en x | `Point(float("inf"), 0)` | `InvalidCoordinateError` |
| 013 | String en lugar de número | `Point("a", 0)` | `InvalidCoordinateError` |
| 014 | None en lugar de número | `Point(None, 0)` | `InvalidCoordinateError` |
| 015 | Lista en lugar de número | `Point([1, 2], 0)` | `InvalidCoordinateError` |

### 7.3 Inmutabilidad (GEOM-POINT-TEST-016 a 018)

| ID | Escenario | Esperado |
|---|---|---|
| 016 | Asignar a p.x | `AttributeError` |
| 017 | Asignar a p.y | `AttributeError` |
| 018 | Asignar a p.z | `AttributeError` |

### 7.4 Distancia (GEOM-POINT-TEST-019 a 023)

| ID | Escenario | Entrada | Esperado |
|---|---|---|---|
| 019 | Distancia 2D | `Point(0,0).distance_to(Point(3,4))` | 5.0 |
| 020 | Distancia 3D | `Point(0,0,0).distance_to(Point(2,3,6))` | 7.0 |
| 021 | Distancia mismo punto | `Point(1,2).distance_to(Point(1,2))` | 0.0 |
| 022 | Distancia con negativos | `Point(-1,-1).distance_to(Point(2,3))` | 5.0 |
| 023 | Distancia simétrica | `a.distance_to(b) == b.distance_to(a)` | True |

### 7.5 Igualdad y tolerancia (GEOM-POINT-TEST-024 a 030)

| ID | Escenario | Esperado |
|---|---|---|
| 024 | `Point(1,2) == Point(1.0, 2.0)` | True |
| 025 | `Point(1,2) == Point(1.0000000005, 2.0)` | True (dentro de EPSILON_GEOMETRY) |
| 026 | `Point(1,2) != Point(3,4)` | True |
| 027 | `Point(0,0) == "POINT (0 0)"` | False (no es Point) |
| 028 | `almost_equal(Point(1,2), Point(1.1,2), tol=0.2)` | True |
| 029 | `almost_equal(Point(1,2), Point(1.1,2), tol=0.05)` | False |
| 030 | `almost_equal("string", Point(0,0))` | `NotImplemented` |

### 7.6 Hash (GEOM-POINT-TEST-031 a 034)

| ID | Escenario | Esperado |
|---|---|---|
| 031 | `hash(Point(1,2)) == hash(Point(1.0, 2.0))` | True |
| 032 | `len({Point(0,0), Point(1,1), Point(0,0)})` | 2 |
| 033 | Point como clave de dict | Funciona |
| 034 | Puntos ≈ iguales pero no exactos ¿mismo hash? | Depende del redondeo a 9 decimales |

### 7.7 Serialización (GEOM-POINT-TEST-035 a 045)

| ID | Escenario | Esperado |
|---|---|---|
| 035 | `Point(1,2,3).to_tuple()` | `(1.0, 2.0, 3.0)` |
| 036 | `Point(1,2).to_tuple()` | `(1.0, 2.0, 0.0)` |
| 037 | `Point(1,2,3).to_dict()` | `{"x": 1.0, "y": 2.0, "z": 3.0}` |
| 038 | `Point(1,2,3).to_json()` | JSON con x, y, z |
| 039 | `Point(10.5, 20.5).to_wkt()` | `"POINT (10.5 20.5)"` |
| 040 | `Point.from_tuple((3.0, 4.0)).to_tuple()` | `(3.0, 4.0, 0.0)` |
| 041 | `Point.from_tuple((1,2,3)).z` | 3.0 |
| 042 | `Point.from_dict({"x":1,"y":2})` | Point(1,2) |
| 043 | `Point.from_dict({"x":1,"y":2,"z":3}).z` | 3.0 |
| 044 | `Point.from_json('{"x":1,"y":2}')` | Point(1,2) |
| 045 | `Point.from_json('{"x":1,"y":2,"z":3}').z` | 3.0 |

### 7.8 Errores de deserialización (GEOM-POINT-TEST-046 a 049)

| ID | Escenario | Esperado |
|---|---|---|
| 046 | `from_tuple((1,))` (1 elemento) | `GeometryError` |
| 047 | `from_tuple((1,2,3,4))` (4 elementos) | `GeometryError` |
| 048 | `from_tuple("not a tuple")` | `GeometryError` |
| 049 | `from_dict({"x":1})` (falta y) | `KeyError` |

### 7.9 Geometry (ABC) contract (GEOM-POINT-TEST-050 a 058)

| ID | Escenario | Esperado |
|---|---|---|
| 050 | `isinstance(Point(1,2), Geometry)` | True |
| 051 | `Point(1,2).dimension` | 2 |
| 052 | `Point(1,2).bbox` | `BoundingBox(1,2,1,2)` |
| 053 | `Point(1,2).is_valid` | True |
| 054 | `Point(1,2).is_empty` | False |
| 055 | `Point(1,2,3).copy()` | Point(1,2,3) distinto objeto, mismo valor |
| 056 | `Point(1,2).to_dict()`  →  `Point.from_dict(...)` | Roundtrip exacto |
| 057 | `Point(1,2).to_json()`  →  `Point.from_json(...)` | Roundtrip exacto |
| 058 | `str(Point(1,2)) == repr(Point(1,2))` | True |

### 7.10 Invariantes (GEOM-POINT-TEST-059 a 060)

| ID | Escenario | Esperado |
|---|---|---|
| 059 | `check_invariants()` en Point válido | No lanza |
| 060 | `check_invariants()` después de to_dict/from_dict | Sigue siendo válido |

---

## 8. ARDs (Architecture Decision Records)

### ADR-001: Inmutabilidad de Point

**Contexto:** Point debe usarse en sets, como clave de dict, y pasarse por miles de funciones sin riesgo de modificación accidental.

**Decisión:** Point es inmutable. Atributos `_x`, `_y`, `_z` son privados. Propiedades de solo lectura. No hay setters ni métodos que muten. `translate()`, `rotate()`, `scale()` devuelven nuevas instancias.

**Consecuencias:**
+ Seguridad en contenedores
+ Caching seguro (Polyline puede cachear sin invalidar)
+ Facilidad para paralelismo
- Más allocaciones (cada transformación crea un nuevo objeto)

### ADR-002: Z opcional con default 0.0

**Contexto:** LINPRO es principalmente 2D (infraestructuras lineales sobre el terreno), pero puede beneficiarse de 3D (catenarias, vanos, MDT).

**Decisión:** `Point(x, y, z=0.0)`. Internamente siempre es 3D. `z` es opcional. La API de WKT es 2D por compatibilidad OGC.

**Consecuencias:**
+ Migración a 3D sin cambiar la API
+ Código 2D existente no se rompe
- Todos los puntos ocupan el mismo espacio (3 floats) aunque sean 2D

### ADR-003: Igualdad con tolerancia

**Contexto:** Comparar floats con `==` es inseguro en geometría computacional. Dos coordenadas UTM pueden diferir en 1e-9 por error de representación.

**Decisión:** `__eq__` usa `math.isclose` con `EPSILON_GEOMETRY` (1e-9). `almost_equal(other, tol)` permite tolerancia explícita.

**Consecuencias:**
+ Comparaciones robustas
+ Rendimiento O(1) aceptable
- `is` (identidad de objeto) puede ser True aunque `==` sea False (no problemático)

### ADR-004: Point hereda de Geometry

**Contexto:** RFC-0001 define `Geometry(ABC)` como clase base de todas las entidades geométricas.

**Decisión:** `Point(Geometry)`. Implementa `dimension`, `is_empty`, `bbox`, `is_valid`, `copy()`, `to_dict()`, `from_dict()`, `to_json()`, `from_json()`, `to_wkt()`, `__eq__`, `__repr__`.

**Consecuencias:**
+ Polimorfismo: cualquier código que use `Geometry` acepta `Point`
+ Contratos garantizados
+ to_json/from_json heredados de Geometry

---

## 9. No objetivos (reiteración)

Point NO hará en ninguna versión:

| Funcionalidad | Motivo | Módulo destino |
|---|---|---|
| Transformaciones CRS | El Kernel no conoce proyecciones | `linpro.engine.gis` |
| Lectura/escritura DXF | El Kernel no conoce formatos CAD | `linpro.io.dxf` |
| Lectura/escritura SHP | El Kernel no conoce formatos GIS | `linpro.io.shp` |
| Buffers | Operación de nivel superior | `linpro.geometry.algorithms` |
| Offsets | Operación de nivel superior | `linpro.geometry.algorithms` |
| Dibujo / render | GUI | `linpro.app.gui` |
| Exportación a Excel | Formato de negocio | `linpro.io.excel` |
| from_dxf / from_shapely | Adaptadores | `linpro.io` |

---

## 10. Compatibilidad futura

Point garantiza compatibilidad con los siguientes escenarios a lo largo de
todas las versiones 0.x y 1.x:

| Aspecto | Compromiso |
|---|---|
| **2D** | `Point(x, y)` siempre será válido y producirá z=0.0 |
| **3D** | `Point(x, y, z)` siempre será válido. La Z nunca se ignora |
| **CRS abstracto** | Point no almacena CRS, pero tampoco impide que un wrapper lo añada en el futuro |
| **Serialización** | `to_dict()` / `from_dict()` serán inversos exactos dentro de tolerancia. El formato JSON no cambiará sin deprecación en una versión mayor |
| **Hash** | El algoritmo de hash (redondeo a 9 decimales) es estable entre versiones |
| **Igualdad** | `__eq__` siempre usará tolerancia. El valor de `EPSILON_GEOMETRY` puede ajustarse, pero el comportamiento de `math.isclose` se mantendrá |
| **Geometry(ABC)** | Point seguirá implementando `Geometry` mientras la clase base exista. Los contratos `dimension`, `bbox`, `is_valid`, `is_empty`, `copy()` son estables |

### Lo que NO garantiza compatibilidad

- El orden de los parámetros del constructor (`x, y, z`) es fijo.
- Los formatos de exportación a terceros (DXF, SHP, GeoJSON) no forman parte del contrato de Point.

---

## 11. Resumen de entidades Point

| Tipo | Rango ID | Cantidad |
|---|---|---|
| Responsabilidades (debe) | GEOM-POINT-001 a 015 | 15 |
| Responsabilidades (no debe) | GEOM-POINT-NO-001 a 008 | 8 |
| Invariantes | GEOM-POINT-INV-001 a 008 | 8 |
| Casos de prueba | GEOM-POINT-TEST-001 a 060 | 60 |
| ADRs | ADR-001 a 004 | 4 |
| Operaciones futuras | FUT-001 a 008 | 8 |

---

*Fin del RFC-0002 — Point*

*Estado actual: ✅ Aprobado por Lead Developer (2026-07-09).*
