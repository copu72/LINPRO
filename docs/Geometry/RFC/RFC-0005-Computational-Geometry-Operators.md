# RFC-0005: Computational Geometry Operators

**Estado:** ✅ CERTIFICADO Y CONGELADO
**Autor:** Lead Architect
**Fecha:** 2026-07-14
**Requiere:** RFC-0004A (Álgebra Vectorial) — Aprobado
**Requiere:** Kernel v0.4.0 (Geometry ABC + Point + BoundingBox + Vector) — Certificado

---

## 1. Objetivo

Definir el subsistema de **operadores geométricos reutilizables** que dará
servicio a Segment, Line, Polyline y futuros algoritmos del Geometry Engine.

A diferencia de los métodos de instancia de Vector (`.dot()`, `.cross()`, etc.),
estos operadores son **funciones independientes** que operan sobre múltiples
tipos del dominio (Point, Segment, BoundingBox). Su propósito es:

1. **Centralizar la lógica geométrica** para evitar duplicación entre entidades.
2. **Proporcionar contratos estables** que puedan ser consumidos por Segment,
   Line, Polyline y los algoritmos de negocio (PK Engine, cruces, etc.).
3. **Establecer tolerancias y reglas de precisión** uniformes en todo el Kernel.

Este RFC no especifica la implementación. Su único propósito es dejar cerrada
la especificación matemática y los contratos de cada operador.

---

## 2. Estructura del módulo

```
src/linpro/geometry/operators/
├── __init__.py               # Re-exporta todos los operadores públicos
├── orientation.py            # GEOM-OPS-001
├── collinearity.py           # GEOM-OPS-002
├── parallelism.py            # GEOM-OPS-003
├── perpendicularity.py       # GEOM-OPS-004
├── distance.py               # GEOM-OPS-005
├── projection.py             # GEOM-OPS-006
├── closest_point.py          # GEOM-OPS-007
├── intersection.py           # GEOM-OPS-008
└── bbox_ops.py               # GEOM-OPS-009
```

---

## 3. Principios de diseño

### 3.1 Funciones puras

Todos los operadores son funciones puras:
- Sin estado interno ni efectos secundarios.
- Dados los mismos argumentos, producen el mismo resultado.
- No modifican los argumentos (inmutabilidad del Kernel).

### 3.2 Tipos del dominio

Los operadores aceptan y retornan tipos del dominio (Point, Vector, Segment,
BoundingBox), nunca primitivas cuando existe una entidad del dominio.
(ADR-0007 — Strong Types)

### 3.3 Tolerancias

Cada operador acepta un parámetro `tol: float` que define la precisión:

| Nivel | Valor | Uso |
|---|---|---|
| `Tolerance.math` | 1e-12 | Comparaciones matemáticas estrictas |
| `Tolerance.geometry` *(default)* | 1e-9 | Operaciones geométricas generales |
| `Tolerance.visual` | 1e-6 | Tolerancia de visualización / snapping |

### 3.4 Manejo de errores

- `PrecisionError` si una operación es numéricamente inestable (división por cero, etc.).
- `TypeError` si los tipos de los argumentos no son válidos para la operación.
- No se lanzan errores para valores límite (punto coincidente, segmento degenerado)
  a menos que la operación sea imposible.

---

## 4. GEOM-OPS-001: Orientation

### 4.1 Objetivo

Determinar la **orientación** de tres puntos en el plano: si forman un giro
antihorario (CCW), horario (CW) o son colineales.

### 4.2 Definición matemática

```
orientation(A, B, C) = sign((B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x))
                      = cross(B - A, C - A)
```

Equivale al producto vectorial 2D de los vectores AB y AC.

### 4.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `a` | Point | Primer punto |
| `b` | Point | Segundo punto |
| `c` | Point | Tercer punto |
| `tol` | float | Tolerancia (opcional, default 1e-9) |
| **Retorno** | float | > 0 si CCW, < 0 si CW, ≈ 0 si colineal |

### 4.4 Complejidad

O(1) — 2 restas, 2 multiplicaciones, 1 resta.

### 4.5 Tolerancias

El resultado se compara con `tol` para determinar colinealidad:
- `|result| ≤ tol` → colineal (considerar 0.0)
- `result > tol` → CCW (positivo)
- `result < -tol` → CW (negativo)

### 4.6 Casos límite

| Escenario | Comportamiento |
|---|---|
| A, B, C colineales | Retorna valor ≈ 0.0 (dentro de tol) |
| A == B (puntos coincidentes) | Retorna 0.0 (degenerado) |
| A, B, C muy distantes (coordenadas UTM grandes) | Válido; usar math.hypot no aplica aquí |
| Puntos en 3D | Operación 2D sobre componentes X, Y (se ignora Z) |

### 4.7 Excepciones

- `TypeError` si algún argumento no es `Point`.

### 4.8 Tests previstos (GEOM-OPS-TEST-001 a 010)

| ID | Escenario | Entrada | Esperado |
|---|---|---|---|
| 001 | CCW (antihorario) | `A(0,0), B(1,0), C(0,1)` | > 0 |
| 002 | CW (horario) | `A(0,0), B(0,1), C(1,0)` | < 0 |
| 003 | Colineal horizontal | `A(0,0), B(1,0), C(2,0)` | ≈ 0.0 |
| 004 | Colineal vertical | `A(0,0), B(0,1), C(0,2)` | ≈ 0.0 |
| 005 | Colineal diagonal | `A(0,0), B(1,1), C(2,2)` | ≈ 0.0 |
| 006 | Puntos coincidentes | `A(1,1), B(1,1), C(2,3)` | 0.0 |
| 007 | A == B == C | `A(1,1), B(1,1), C(1,1)` | 0.0 |
| 008 | Puntos 3D | `A(0,0,5), B(1,0,5), C(0,1,5)` | > 0 (ignora Z) |
| 009 | Cerca de colineal (dentro de tol) | puntos casi alineados | ≈ 0 |
| 010 | TypeError con Vector | `orientation(Vector(1,0), ...)` | TypeError |

---

## 5. GEOM-OPS-002: Collinearity

### 5.1 Objetivo

Determinar si tres puntos son **colineales** (pertenecen a la misma línea recta).

### 5.2 Definición matemática

```
is_collinear(A, B, C, tol) = |orientation(A, B, C)| ≤ tol
```

Delega en `orientation()`.

### 5.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `a` | Point | Primer punto |
| `b` | Point | Segundo punto |
| `c` | Point | Tercer punto |
| `tol` | float | Tolerancia (opcional, default 1e-9) |
| **Retorno** | bool | `True` si los puntos son colineales |

### 5.4 Complejidad

O(1) — delega en orientation.

### 5.5 Tolerancias

Se heredan de `orientation()`.

### 5.6 Casos límite

| Escenario | Comportamiento |
|---|---|
| A y B coincidentes | `orientation` retorna 0 → colineal = True |
| Dos puntos coincidentes | Siempre colineal (tres puntos definen una línea si dos son iguales) |
| Puntos idénticos | True |

### 5.7 Excepciones

- `TypeError` si algún argumento no es `Point`.

### 5.8 Tests previstos (GEOM-OPS-TEST-011 a 020)

| ID | Escenario | Esperado |
|---|---|---|
| 011 | Colineal horizontal | True |
| 012 | Colineal vertical | True |
| 013 | Colineal diagonal | True |
| 014 | No colineal | False |
| 015 | A == B | True |
| 016 | Casi colineal (dentro de tol) | True |
| 017 | Casi colineal (fuera de tol) | False |
| 018 | Puntos coincidentes | True |
| 019 | 3D con misma Z | True |
| 020 | 3D con Z distinta | True (solo X,Y) |

---

## 6. GEOM-OPS-003: Parallelism

### 6.1 Objetivo

Determinar si dos vectores o dos segmentos son **paralelos**.

### 6.2 Definición matemática

```
is_parallel(u, v, tol) = |cross(u, v)| ≤ tol
```

Donde `cross` es el producto vectorial 2D (magnitud del cross 2D).

Para segmentos:
```
is_parallel(s1, s2, tol) = is_parallel(s1.direction, s2.direction, tol)
```

### 6.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `a` | Vector \| Segment | Primer vector o segmento |
| `b` | Vector \| Segment | Segundo vector o segmento |
| `tol` | float | Tolerancia (opcional, default 1e-9) |
| **Retorno** | bool | `True` si son paralelos |

### 6.4 Complejidad

O(1) — 1 producto vectorial.

### 6.5 Tolerancias

El valor absoluto del cross debe ser ≤ `tol`.

### 6.6 Casos límite

| Escenario | Comportamiento |
|---|---|
| Vector nulo vs cualquier vector | cross = 0 → True (por convención, el vector nulo es paralelo a todo) |
| Segmento degenerado (length=0) | dirección indefinida → True si ambos son degenerados |
| Vectores opuestos (v, -v) | cross = 0 → True |
| Segmentos en 3D | Se usa cross 3D → `|cross|` = longitud del vector resultante |

### 6.7 Excepciones

- `TypeError` si los tipos no son Vector ni Segment.
- `TypeError` si los dos argumentos son de distinto tipo.

### 6.8 Tests previstos (GEOM-OPS-TEST-021 a 030)

| ID | Escenario | Esperado |
|---|---|---|
| 021 | Vectores paralelos misma dirección | True |
| 022 | Vectores paralelos opuestos | True |
| 023 | Vectores no paralelos | False |
| 024 | Vector nulo vs vector cualquiera | True |
| 025 | Segmentos paralelos | True |
| 026 | Segmentos no paralelos | False |
| 027 | Segmento vs Vector (TypeError) | TypeError |
| 028 | Vector 3D paralelo | True |
| 029 | Casi paralelos (dentro de tol) | True |
| 030 | Casi paralelos (fuera de tol) | False |

---

## 7. GEOM-OPS-004: Perpendicularity

### 7.1 Objetivo

Determinar si dos vectores o dos segmentos son **perpendiculares**.

### 7.2 Definición matemática

```
is_perpendicular(u, v, tol) = |dot(u, v)| ≤ tol
```

Donde `dot` es el producto escalar.

### 7.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `a` | Vector \| Segment | Primer vector o segmento |
| `b` | Vector \| Segment | Segundo vector o segmento |
| `tol` | float | Tolerancia (opcional, default 1e-9) |
| **Retorno** | bool | `True` si son perpendiculares |

### 7.4 Complejidad

O(1) — 1 producto escalar.

### 7.5 Casos límite

| Escenario | Comportamiento |
|---|---|
| Vector nulo vs cualquier vector | dot = 0 → True (el vector nulo es perpendicular a todo por convención) |
| Segmento degenerado | dirección indefinida → True si ambos son degenerados |

### 7.6 Excepciones

- `TypeError` si los tipos no son Vector ni Segment.
- `TypeError` si los dos argumentos son de distinto tipo.

### 7.7 Tests previstos (GEOM-OPS-TEST-031 a 040)

| ID | Escenario | Esperado |
|---|---|---|
| 031 | Vectores perpendiculares (1,0)·(0,1) | True |
| 032 | Vectores no perpendiculares | False |
| 033 | Vector nulo vs cualquier vector | True |
| 034 | Segmentos perpendiculares | True |
| 035 | Segmentos no perpendiculares | False |
| 036 | Perpendiculares en 3D | True |
| 037 | Casi perpendiculares (dentro de tol) | True |
| 038 | Casi perpendiculares (fuera de tol) | False |
| 039 | Perpendicular consigo mismo (1,0)·(1,0)≠0 | False |
| 040 | TypeError tipos mixtos | TypeError |

---

## 8. GEOM-OPS-005: Distance

### 8.1 Objetivo

Calcular la **distancia mínima** entre dos entidades geométricas.

### 8.2 Definición matemática

Combinaciones soportadas:

| Firma | Descripción |
|---|---|
| `distance(p1: Point, p2: Point) -> float` | Distancia euclidiana entre dos puntos |
| `distance(p: Point, s: Segment) -> float` | Distancia de un punto a un segmento |
| `distance(s1: Segment, s2: Segment) -> float` | Distancia mínima entre dos segmentos |
| `distance(p: Point, bb: BoundingBox) -> float` | Distancia de un punto a un BoundingBox |

```
distance(Point a, Point b) = sqrt((a.x - b.x)² + (a.y - b.y)²)

distance(Point p, Segment s)  → ver closest_point: |p - closest_point(p, s)|

distance(Seg s1, Seg s2) = min(
    distance(s1.start, s2),
    distance(s1.end, s2),
    distance(s2.start, s1),
    distance(s2.end, s1)
)  [si no se intersectan; 0 si se intersectan]

distance(Point p, BoundingBox bb):
    dx = max(bb.xmin - p.x, 0, p.x - bb.xmax)
    dy = max(bb.ymin - p.y, 0, p.y - bb.ymax)
    return sqrt(dx² + dy²)
```

### 8.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `a` | Point \| Segment \| BoundingBox | Primera entidad |
| `b` | Point \| Segment \| BoundingBox | Segunda entidad |
| **Retorno** | float | Distancia mínima (≥ 0) |

### 8.4 Complejidad

- Point-Point: O(1)
- Point-Segment: O(1) — delega en closest_point
- Segment-Segment: O(1) — 4 distancias punto-segmento
- Point-BoundingBox: O(1)

### 8.5 Tolerancias

Distancias menores o iguales a `tol` se consideran cero (entidades que se tocan).

### 8.6 Casos límite

| Escenario | Comportamiento |
|---|---|
| Puntos coincidentes | 0.0 |
| Punto sobre segmento | 0.0 |
| Segmentos que se intersectan | 0.0 |
| Punto dentro de BoundingBox | 0.0 |
| Segmento degenerado (punto) | Se comporta como Point-Point |

### 8.7 Excepciones

- `TypeError` si la combinación de tipos no está soportada.
- `PrecisionError` si el cálculo es inestable (coordenadas extremas).

### 8.8 Tests previstos (GEOM-OPS-TEST-041 a 055)

| ID | Escenario | Esperado |
|---|---|---|
| 041 | Point-Point separados | > 0 |
| 042 | Point-Point coincidentes | 0.0 |
| 043 | Point-Segment, punto sobre segmento | 0.0 |
| 044 | Point-Segment, punto fuera (perpendicular) | > 0 |
| 045 | Point-Segment, punto más allá del extremo | distancia al extremo |
| 046 | Segment-Segment que se cruzan | 0.0 |
| 047 | Segment-Segment paralelos separados | > 0 |
| 048 | Segment-Segment en línea pero separados | > 0 |
| 049 | Point-BoundingBox, punto dentro | 0.0 |
| 050 | Point-BoundingBox, punto fuera | > 0 |
| 051 | Point-BoundingBox, punto en borde | 0.0 |
| 052 | Segmento degenerado como punto | válido |
| 053 | TypeError con Vector | TypeError |
| 054 | Distancia 3D Point-Point | correcta |
| 055 | Punto muy lejano (coordenadas UTM) | correcta dentro de precisión |

---

## 9. GEOM-OPS-006: Projection

### 9.1 Objetivo

Calcular la **proyección ortogonal** de un punto sobre un segmento (línea infinita).

### 9.2 Definición matemática

```
project(p, s) = s.start + t * (s.end - s.start)

t = (p - s.start) · (s.end - s.start) / |s.end - s.start|²
```

Donde `t` NO está clampado al rango [0, 1] — esta es la proyección sobre la
**línea infinita** que contiene al segmento.

### 9.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `point` | Point | Punto a proyectar |
| `segment` | Segment | Segmento de referencia |
| **Retorno** | Point | Proyección sobre la línea del segmento |

### 9.4 Complejidad

O(1) — 2 restas, 1 producto escalar, 1 división.

### 9.5 Tolerancias

- Si `|s.end - s.start|² ≈ 0` (segmento degenerado), retorna `s.start`.
- La tolerancia determina cuándo un segmento se considera degenerado.

### 9.6 Casos límite

| Escenario | Comportamiento |
|---|---|
| Punto sobre la línea | Retorna el mismo punto |
| Punto más allá del extremo | Retorna punto más allá del extremo (sin clamp) |
| Segmento degenerado (punto) | Retorna el punto del segmento |
| Punto en el origen del segmento | Retorna el origen |

### 9.7 Excepciones

- `TypeError` si `point` no es Point o `segment` no es Segment.

### 9.8 Tests previstos (GEOM-OPS-TEST-056 a 065)

| ID | Escenario | Esperado |
|---|---|---|
| 056 | Proyección en punto medio | Punto medio |
| 057 | Proyección en el origen del segmento | s.start |
| 058 | Proyección más allá del extremo | Punto fuera del segmento |
| 059 | Punto ya sobre la línea | Mismo punto |
| 060 | Segmento horizontal, punto arriba | Proyección vertical correcta |
| 061 | Segmento vertical, punto a la derecha | Proyección horizontal correcta |
| 062 | Segmento diagonal | Proyección correcta |
| 063 | Segmento degenerado | s.start |
| 064 | Punto 3D sobre segmento 3D | Proyección 3D correcta |
| 065 | TypeError con Vector | TypeError |

---

## 10. GEOM-OPS-007: Closest Point

### 10.1 Objetivo

Encontrar el **punto más cercano** de un punto a un segmento (con clamp
al segmento, no a la línea infinita).

### 10.2 Definición matemática

```
closest_point(p, s) = s.start + clamp(t, 0, 1) * (s.end - s.start)

t = (p - s.start) · (s.end - s.start) / |s.end - s.start|²
```

A diferencia de `project()` (GEOM-OPS-006), `t` está clampado a [0, 1],
garantizando que el resultado siempre está **dentro del segmento**.

### 10.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `point` | Point | Punto a evaluar |
| `segment` | Segment | Segmento de referencia |
| **Retorno** | Point | Punto más cercano dentro del segmento |

### 10.4 Complejidad

O(1) — igual que project + 1 clamp.

### 10.5 Casos límite

| Escenario | Comportamiento |
|---|---|
| Punto más allá del inicio | Retorna s.start |
| Punto más allá del final | Retorna s.end |
| Punto sobre la línea dentro del segmento | Retorna la proyección exacta |
| Segmento degenerado | Retorna s.start (= s.end) |

### 10.6 Tests previstos (GEOM-OPS-TEST-066 a 075)

| ID | Escenario | Esperado |
|---|---|---|
| 066 | Punto dentro del segmento | Proyección exacta |
| 067 | Punto antes del inicio | s.start |
| 068 | Punto después del final | s.end |
| 069 | Punto perpendicular al segmento, dentro | Proyección correcta |
| 070 | Segmento degenerado | s.start |
| 071 | Punto sobre el segmento | El mismo punto |
| 072 | Punto en el extremo inicio | s.start |
| 073 | Punto en el extremo final | s.end |
| 074 | Segmento 3D | Proyección 3D clampada |
| 075 | Distancia = 0 | closest_point == punto original |

---

## 11. GEOM-OPS-008: Intersection

### 11.1 Objetivo

Determinar si dos segmentos se **intersectan** y, opcionalmente, calcular
el punto de intersección.

### 11.2 Definición matemática

```
intersects(seg1, seg2) → bool
```

Se usa el método de orientación:
```
o1 = orientation(seg1.start, seg1.end, seg2.start)
o2 = orientation(seg1.start, seg1.end, seg2.end)
o3 = orientation(seg2.start, seg2.end, seg1.start)
o4 = orientation(seg2.start, seg2.end, seg1.end)

// Caso general: los segmentos se cruzan
if o1 * o2 < 0 and o3 * o4 < 0 → True

// Caso colineal y solapado
if o1 == 0 and on_segment(seg1, seg2.start) → True
...
```

Además existe `intersection_point(seg1, seg2) → Point | None` que retorna
el punto de intersección cuando existe.

### 11.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `a` | Segment | Primer segmento |
| `b` | Segment | Segundo segmento |
| `tol` | float | Tolerancia (opcional) |
| **Retorno (intersects)** | bool | `True` si se intersectan |
| **Retorno (intersection_point)** | Point \| None | Punto de intersección o None |

### 11.4 Complejidad

O(1) — 4 orientaciones + comparaciones.

### 11.5 Tolerancias

La orientación se considera 0 si `|result| ≤ tol`. Esto afecta a la detección
de intersecciones colineales y casi-colineales.

### 11.6 Casos límite

| Escenario | Comportamiento |
|---|---|
| Segmentos que se cruzan en X | True, punto interior |
| Segmentos paralelos separados | False |
| Segmentos colineales solapados | True |
| Segmentos colineales separados | False |
| Segmentos que comparten un extremo | True (intersección en el extremo) |
| Segmentos en T (extremo sobre el otro) | True |
| Casi-intersección (dentro de tol) | True |
| Casi-intersección (fuera de tol) | False |

### 11.7 Excepciones

- `TypeError` si algún argumento no es Segment.

### 11.8 Tests previstos (GEOM-OPS-TEST-076 a 090)

| ID | Escenario | Esperado |
|---|---|---|
| 076 | Intersección en X (centro) | True, punto correcto |
| 077 | Intersección en extremo | True |
| 078 | Segmentos paralelos | False |
| 079 | Segmentos colineales solapados | True |
| 080 | Segmentos colineales separados | False |
| 081 | Segmentos en T | True |
| 082 | Sin intersección | False |
| 083 | Casi intersección (dentro de tol) | True |
| 084 | Casi intersección (fuera de tol) | False |
| 085 | Degenerado vs normal | False (o True si el punto está sobre) |
| 086 | Ambos degenerados | False (o True si coinciden) |
| 087 | intersection_point con intersección | Point válido |
| 088 | intersection_point sin intersección | None |
| 089 | intersects(seg, seg) devuelve bool | isinstance True |
| 090 | TypeError con Point | TypeError |

---

## 12. GEOM-OPS-009: BoundingBox Operations

### 12.1 Objetivo

Proporcionar operaciones rápidas de **BoundingBox** como funciones
independientes para test de intersección espacial previa (broad-phase).

### 12.2 Definiciones

```
bbox_intersects(bb1, bb2) → bool
```

Delega en `BoundingBox.intersects()` pero como función independiente
para mantener el patrón del módulo operators.

Además:

```
bbox_contains_point(bb, point) → bool
bbox_contains_bbox(outer, inner) → bool
bbox_union(bb1, bb2) → BoundingBox
bbox_intersection(bb1, bb2) → BoundingBox | None
```

### 12.3 Entradas y salidas

| Elemento | Tipo | Descripción |
|---|---|---|
| `a`, `b` | BoundingBox | BoundingBox a evaluar |
| `point` | Point | Punto a evaluar |
| `outer`, `inner` | BoundingBox | Contenedor y contenido |
| **Retorno** | bool \| BoundingBox \| None | Según operación |

### 12.4 Complejidad

Todas las operaciones: O(1) — entre 4 y 8 comparaciones.

### 12.5 Casos límite

| Escenario | Comportamiento |
|---|---|
| Cajas tangentes | intersects = True |
| Caja degenerada (width=0) | Válida; puede intersectar |
| Caja vacía | intersects = False con cualquier otra |

### 12.6 Tests previstos (GEOM-OPS-TEST-091 a 105)

| ID | Escenario | Esperado |
|---|---|---|
| 091 | bbox_intersects solapadas | True |
| 092 | bbox_intersects separadas | False |
| 093 | bbox_intersects tangentes | True |
| 094 | bbox_contains_point dentro | True |
| 095 | bbox_contains_point fuera | False |
| 096 | bbox_contains_bbox contenido | True |
| 097 | bbox_contains_bbox no contenido | False |
| 098 | bbox_union | BoundingBox expandido |
| 099 | bbox_intersection solapadas | BoundingBox válido |
| 100 | bbox_intersection separadas | None |
| 101 | Caja degenerada intersects | True si toca |
| 102 | Caja vacía intersects | False |
| 103 | bbox_contains_point en borde | True |
| 104 | from_points con lista de BoundingBox | BoundingBox envolvente |
| 105 | Encadenamiento: union → intersection | Consistente |

---

## 13. Tolerancias globales

Todos los operadores heredan la jerarquía de tolerancias del Kernel:

```python
# En cada operador que acepte tol:
def operator(..., tol: float | None = None) -> ...:
    if tol is None:
        tol = Tolerance.geometry  # 1e-9
    # ... lógica con tol
```

| Constante | Valor | Uso |
|---|---|---|
| `Tolerance.math` | 1e-12 | Comparaciones de igualdad exacta |
| `Tolerance.geometry` | 1e-9 | Operaciones geométricas (default) |
| `Tolerance.visual` | 1e-6 | Snapping y visualización |

---

## 14. ADRs

### ADR-001: Operadores como funciones, no métodos

**Contexto:** Las operaciones como `orientation`, `distance`, `intersection`
podrían implementarse como métodos de `Segment` o `Point`. Sin embargo,
muchas operaciones involucran dos entidades del mismo tipo (dos segmentos)
o de tipos distintos (punto y segmento).

**Decisión:** Los operadores geométricos son **funciones independientes**
en el módulo `src/linpro/geometry/operators/`. Las entidades (Segment, Line,
Polyline) pueden llamarlos internamente, pero no duplican su lógica.

**Consecuencias:**
+ Un único punto de verdad para cada algoritmo
+ Se pueden probar de forma aislada
+ Se pueden usar sin instanciar entidades complejas
- Las entidades tienen que delegar explícitamente (una línea extra de código)
- Namespace adicional (importar desde `operators`)

### ADR-002: Orientation devuelve float, no enum

**Contexto:** La orientación puede ser CCW (+), CW (-) o colineal (0).
Podría modelarse como un enum (Orientation.CW, Orientation.CCW, Orientation.COLLINEAR).

**Decisión:** `orientation()` devuelve `float` (el valor exacto del cross 2D).
La interpretación como CCW/CW/colineal la hace el llamante comparando con `tol`.

**Consecuencias:**
+ El llamante puede usar el valor exacto (no solo el signo)
+ No se pierde información de magnitud
+ Compatible con algoritmos que necesitan el área orientada exacta
- El llamante debe comparar con tolerancia explícitamente

### ADR-003: Closest Point clampa, Projection no clampa

**Contexto:** Existen dos operaciones relacionadas pero distintas: proyectar
un punto sobre la línea infinita que contiene al segmento (project) y encontrar
el punto más cercano dentro del segmento (closest_point).

**Decisión:** Se implementan dos funciones separadas:
- `project()` → proyección sobre la línea (sin clamp)
- `closest_point()` → punto más cercano dentro del segmento (con clamp a [0,1])

**Consecuencias:**
+ Claridad semántica: cada función hace exactamente lo que su nombre indica
+ `project()` es útil para calcular distancias a líneas infinitas
+ `closest_point()` es útil para distancia mínima a segmentos
- El llamante debe elegir la función correcta (documentación clara)

### ADR-004: Intersection con tolerancia configurable

**Contexto:** En ingeniería real, dos segmentos pueden no intersectarse
matemáticamente pero sí en el mundo físico debido a la precisión de las
coordenadas de entrada (levantamientos topográficos, digitalizaciones).

**Decisión:** `intersects()` acepta un parámetro de tolerancia. Si dos
segmentos casi se intersectan (distancia mínima ≤ tol), se consideran
intersectantes.

**Consecuencias:**
+ Comportamiento robusto con datos del mundo real
+ El usuario puede ajustar la sensibilidad
- Posibles falsos positivos con tolerancias muy grandes

### ADR-006: Pure Functions — sin estado, sin caché, thread-safe

**Contexto:** Los operadores geométricos serán consumidos por múltiples
entidades y algoritmos simultáneamente, incluyendo posibles ejecuciones
paralelas en el PK Engine y algoritmos de cruces.

**Decisión:** Todos los operadores son **funciones puras**:
- Sin estado interno ni variables de clase mutables.
- Sin caché de resultados (el llamante puede cachear si lo necesita).
- Sin efectos secundarios (no modifican argumentos, no escriben en disco).
- Deterministas: mismos argumentos → mismo resultado siempre.
- Thread-safe por definición (no hay estado compartido).

**Consecuencias:**
+ Se pueden paralelizar sin locks ni sincronización
+ Fáciles de testear (no requieren setup/teardown)
+ Comportamiento predecible en pipelines
- No hay memoización automática (el llamante puede añadirla externamente si es necesario)

### ADR-005: BBox operations como funciones, no duplicación

**Contexto:** BoundingBox ya tiene métodos de instancia (`intersects`,
`contains_point`, `union`, `intersection`). Las funciones en `operators/`
delegarían en esos métodos.

**Decisión:** Las funciones `bbox_intersects`, `bbox_contains_point`, etc.
en `operators/bbox_ops.py` delegan en los métodos de `BoundingBox`. No
duplican la lógica. Sirven como fachada uniforme del subsistema operators.

**Consecuencias:**
+ API consistente: todos los operadores se importan de `operators`
+ Sin duplicación de lógica
+ BoundingBox conserva sus métodos (interfaz rica)
- Una capa adicional de indirección

---

## 15. Plan de tests

### 15.1 Resumen

| Operador | ID prefix | Tests previstos |
|---|---|---|
| Orientation | GEOM-OPS-TEST-001 a 010 | 10 |
| Collinearity | GEOM-OPS-TEST-011 a 020 | 10 |
| Parallelism | GEOM-OPS-TEST-021 a 030 | 10 |
| Perpendicularity | GEOM-OPS-TEST-031 a 040 | 10 |
| Distance | GEOM-OPS-TEST-041 a 055 | 15 |
| Projection | GEOM-OPS-TEST-056 a 065 | 10 |
| Closest Point | GEOM-OPS-TEST-066 a 075 | 10 |
| Intersection | GEOM-OPS-TEST-076 a 090 | 15 |
| BoundingBox | GEOM-OPS-TEST-091 a 105 | 15 |
| **Total** | | **105** |

### 15.2 Cobertura objetivo

- ≥ 98% en todas las líneas del módulo `operators/`.
- Casos límite incluidos (no solo camino feliz).
- Tests de error (TypeError, PrecisionError).

### 15.3 Benchmark objetivo

Un benchmark por operador para establecer línea base de rendimiento.

---

## 16. Dependencias del módulo operators

```
operators/
├── orientation.py     → Point (Geometry)
├── collinearity.py    → orientation
├── parallelism.py     → Vector (cross/dot), Segment
├── perpendicularity.py → Vector (dot), Segment
├── distance.py        → Point, Segment, BoundingBox, closest_point
├── projection.py      → Point, Segment, Vector
├── closest_point.py   → projection (con clamp)
├── intersection.py    → orientation, Segment
└── bbox_ops.py        → BoundingBox (delega en métodos de instancia)
```

No hay dependencias circulares. Ningún operador depende de otro operador
que a su vez dependa de él.

---

## 17. No objetivos

| Funcionalidad | Motivo | Módulo destino |
|---|---|---|
| Offset de polilíneas | Algoritmo de nivel superior | `linpro.engine.algorithms` (futuro) |
| Simplificación (Douglas-Peucker) | Algoritmo de nivel superior | `linpro.engine.algorithms` (futuro) |
| Buffer / zona de influencia | Algoritmo de nivel superior | `linpro.engine.algorithms` (futuro) |
| Intersección Polilínea-Polilínea | Algoritmo compuesto | `linpro.engine.algorithms` (futuro) |
| Clipping (Cohen-Sutherland) | Algoritmo de render/GIS | `linpro.engine.algorithms` (futuro) |
| Conversión CRS | No es geometría pura | `linpro.engine.gis` |

---

## 18. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Duplicación entre operadores y métodos de instancia** | Dos implementaciones del mismo algoritmo | Los operadores son el único origen; los métodos de entidad (si existen) delegan |
| **Tolerancia inconsistente entre operadores** | Resultados contradictorios según qué operador se use | Todos los operadores usan `Tolerance.geometry` por defecto |
| **Segmento degenerado no detectado** | División por cero en proyección | Detectar `|s.end - s.start|² ≈ 0` antes de calcular t |
| **Rendimiento en closest_point para grandes volúmenes** | Cuello de botella si se usa en bucles | Benchmark como línea base; optimizar solo si es necesario |

---

## 19. Resumen de entidades

| Tipo | Rango ID | Cantidad |
|---|---|---|
| Operadores | GEOM-OPS-001 a 009 | 9 |
| Tests previstos | GEOM-OPS-TEST-001 a 105 | 105 |
| ADRs | ADR-001 a 005 | 5 |
| Dependencias entre módulos | — | 0 cíclicas |

---

*Fin del RFC-0005 — Computational Geometry Operators*

---

> *"En LINPRO, las entidades representan la geometría; los operadores representan el conocimiento matemático."*
> — Chief Software Architect, 2026-07-14
