# RFC-0004A: Álgebra Vectorial

**Estado:** ✅ Aprobado y congelado
**Autor:** Lead Developer
**Fecha:** 2026-07-10
**Requiere:** RFC-0001 (Geometry Kernel) — Aprobado

---

## 1. Objetivo

Definir el modelo matemático del álgebra vectorial de LINPRO **antes** de
implementar la clase `Vector`. Establecer las reglas de operadores,
las conversiones entre tipos, y el contrato algebraico que gobernará
todas las operaciones vectoriales del Geometry Engine.

Este RFC no especifica la implementación de `Vector` (eso será RFC-0004B).
Su único propósito es dejar cerradas las reglas matemáticas.

---

## 2. Definición

### 2.1 ¿Qué es un Vector en LINPRO?

Un **Vector** es un objeto matemático que representa un **desplazamiento**
en el espacio cartesiano 2D/3D.

A diferencia de `Point`, un Vector **no tiene posición**. Tiene:

- **magnitud** (longitud, módulo)
- **dirección** (orientación en el espacio)
- **sentido** (hacia dónde apunta)

Un Vector se representa internamente como `(dx, dy[, dz])`.

### 2.2 Vector vs Point — Principio de distinción

| Concepto | Point | Vector |
|---|---|---|
| Representa | Una **posición** en el espacio | Un **desplazamiento** |
| Coordenadas | (x, y, z) — absolutas | (dx, dy) — relativas |
| Origen | El origen del sistema de coordenadas | No tiene origen |
| Depende del CRS | Sí (está anclado a un sistema de referencia) | No (es puramente matemático) |
| Transforma con CRS | Sí | No (es invariante) |
| `Point - Point` | ❌ Prohibido (¿qué posición sería?) | ✅ Devuelve `Vector` |
| `Point + Vector` | ✅ Devuelve `Point` | ❌ No tiene sentido |

### 2.3 Principio fundamental

> En LINPRO, Point está anclado al sistema de coordenadas. Vector no.
> Un Vector puede moverse libremente por el espacio sin cambiar su identidad.

Esto implica:

- `Vector(3, 4)` es el mismo objeto matemático desplace desde (0,0) o desde (500000, 4600000).
- `Point(3, 4)` en UTM es **distinto** de `Point(3, 4)` en otro CRS.
- Las operaciones que combinan Point y Vector **siempre** producen un Point.
- Las operaciones entre Vectores **siempre** producen un Vector (o escalar).

---

## 3. Álgebra de operadores

### 3.1 Tabla de operaciones permitidas y prohibidas

| Operación | Resultado | Ejemplo | GEOM-VEC |
|---|---|---|---|
| `Point - Point` | `Vector` | `p - q = Vector(dx, dy)` | VEC-001 |
| `Point + Vector` | `Point` | `p + v = Point(x+dx, y+dy)` | VEC-002 |
| `Point - Vector` | `Point` | `p - v = Point(x-dx, y-dy)` | VEC-003 |
| `Vector + Vector` | `Vector` | `v + w = Vector(dx1+dx2, dy1+dy2)` | VEC-004 |
| `Vector - Vector` | `Vector` | `v - w = Vector(dx1-dx2, dy1-dy2)` | VEC-005 |
| `Vector * escalar` | `Vector` | `v * 2 = Vector(2*dx, 2*dy)` | VEC-006 |
| `escalar * Vector` | `Vector` | `2 * v = Vector(2*dx, 2*dy)` | VEC-007 |
| `Vector / escalar` | `Vector` | `v / 2 = Vector(dx/2, dy/2)` | VEC-008 |
| `-Vector` (negación) | `Vector` | `-v = Vector(-dx, -dy)` | VEC-009 |
| `Vector + Point` | `Point` | `v + p = Point(x+dx, y+dy)` | VEC-010 |

### 3.2 Operaciones prohibidas

| Operación | Motivo |
|---|---|
| `Point + Point` | Dos posiciones no se suman. No tiene significado geométrico. |
| `Point * escalar` | ¿Qué sería un punto escalado? Solo tiene sentido desde un centro. |
| `Point / escalar` | Ídem. |
| `Point + Point → Point` | ❌ Error algebraico. Para promediar usar `midpoint`. |

### 3.3 Operaciones que devuelven escalar

| Operación | Resultado | Ejemplo |
|---|---|---|
| `v.dot(w)` | `float` | Producto escalar |
| `v.cross(w)` | `float` (2D) o `Vector` (3D) | Producto vectorial |
| `v.length` | `float` | Módulo (norma) |
| `v.angle_to(w)` | `float` (radianes) | Ángulo entre vectores |
| `v.distance_to(w)` | `float` | Distancia entre puntas |

---

## 4. Propiedades de Vector

| Propiedad | Tipo | Fórmula | GEOM-VEC |
|---|---|---|---|
| `.dx` | float | — | VEC-011 |
| `.dy` | float | — | VEC-012 |
| `.dz` | float | 0.0 si 2D | VEC-013 |
| `.length` | float | `sqrt(dx² + dy² + dz²)` | VEC-014 |
| `.length_squared` | float | `dx² + dy² + dz²` | VEC-015 |
| `.angle` | float | `atan2(dy, dx)` en radianes | VEC-016 |
| `.normalized` | Vector | `v / v.length` (lanza si length=0) | VEC-017 |
| `.is_zero` | bool | `length ≈ 0` | VEC-018 |
| `.perpendicular` | Vector | `Vector(-dy, dx)` (sentido antihorario) | VEC-019 |
| `.dimension` | int | 2 o 3 | (Geometry) |

---

## 5. Métodos de Vector

| Método | Retorno | Descripción | GEOM-VEC |
|---|---|---|---|
| `dot(other)` | float | Producto escalar `dx1*dx2 + dy1*dy2` | VEC-020 |
| `cross(other)` | float \| Vector | Producto vectorial (2D: escalar; 3D: Vector) | VEC-021 |
| `angle_to(other)` | float | Ángulo entre vectores en radianes [0, π] | VEC-022 |
| `signed_angle_to(other)` | float | Ángulo con signo [-π, π] (antihorario positivo) | VEC-023 |
| `rotate(angle)` | Vector | Rotación antihoraria en radianes | VEC-024 |
| `project_onto(other)` | Vector | Proyección de `v` sobre `w` | VEC-025 |
| `reject_from(other)` | Vector | Componente perpendicular de `v` a `w` | VEC-026 |
| `lerp(other, t)` | Vector | Interpolación lineal: `v + t*(w - v)`, t ∈ [0,1] | VEC-027 |
| `almost_equal(other, tol)` | bool | Comparación con tolerancia | VEC-028 |
| `is_parallel(other)` | bool | `|cross| ≈ 0` | VEC-029 |
| `is_perpendicular(other)` | bool | `|dot| ≈ 0` | VEC-030 |
| `to_dict()` | dict | `{"dx": ..., "dy": ..., "dz": ...}` | (Geometry) |
| `from_dict(data)` | Vector | Desde dict | (Geometry) |
| `to_wkt()` | str | No aplica (Vector no tiene representación WKT) | — |

---

## 6. Inmutabilidad

Vector es **inmutable**, exactamente igual que Point y BoundingBox.

- `dx`, `dy`, `dz` son propiedades de solo lectura
- `rotate()` devuelve un **nuevo** Vector
- `normalized` es una propiedad calculada que devuelve un **nuevo** Vector
- No hay setters ni métodos que muten

---

## 7. Casos límite

### 7.1 Vector nulo

Un Vector con `dx=0, dy=0` (y `dz=0`) es el **vector nulo**:

- `length = 0`
- `normalized` → `PrecisionError` (no se puede normalizar el vector nulo)
- `angle` → indefinido (0.0 por convención)
- `is_zero = True`
- `dot(v, zero) = 0` para cualquier v
- `cross(zero, v) = 0` para cualquier v

### 7.2 Vector unitario

Un Vector con `length = 1` es un **vector unitario** (versor):

- `normalized` devuelve el mismo vector si ya es unitario
- `is_unit` (propiedad) → `True` si `|length - 1| < EPSILON`

### 7.3 Precisión

- `length` usa `math.hypot` para evitar overflow en coordenadas grandes
- `normalized` detecta length ≈ 0 con `EPSILON_GEOMETRY`
- `angle_to` usa `atan2` con protección contra dominio
- `is_parallel` y `is_perpendicular` usan `EPSILON_GEOMETRY`

---

## 8. Convenciones de ángulos

- Todos los ángulos en **radianes**
- Sentido **antihorario** (matemático) como positivo
- Ángulo 0 = dirección del eje X positivo (Este)
- `angle` = `atan2(dy, dx)` en rango `[-π, π]`
- `signed_angle_to(other)` en rango `[-π, π]`

### Correspondencia con azimut topográfico

| Dirección | Ángulo (rad) | Ángulo (grados) | Azimut topográfico |
|---|---|---|---|
| Este (X+) | 0 | 0° | 100g / 90° |
| Norte (Y+) | π/2 | 90° | 0g / 0° |
| Oeste (X-) | π | 180° | 300g / 270° |
| Sur (Y-) | -π/2 | -90° | 200g / 180° |

> Nota: El azimut topográfico (0° = Norte, sentido horario) es una
> transformación de negocio, no del Kernel. El Kernel usa el convenio
> matemático (0° = Este, sentido antihorario). La conversión se hará
> en el módulo de dominio, no en el Geometry Engine.

---

## 9. Preparación 3D

LINPRO es principalmente 2D, pero el álgebra vectorial debe estar preparada
para 3D desde el diseño:

- `Vector(dx, dy, dz=0.0)` — constructor con z opcional
- `cross` en 2D devuelve escalar (la magnitud del vector resultante Z)
- `cross` en 3D devuelve Vector (producto vectorial completo)
- `length` siempre usa los 3 componentes
- `rotate` en 2D es rotación en el plano XY
- `rotate` en 3D requerirá eje de rotación (futuro)

---

## 10. Reglas de implementación (para RFC-0004B)

1. `Vector` hereda de `Geometry(ABC)`
2. `dimension = 2` si `dz == 0.0`, sino `3`
3. `is_empty = True` solo si `is_zero` (vector nulo)
4. `bbox` devuelve `BoundingBox(0, 0, dx, dy)` centrado en origen
5. `to_dict()` produce `{"dx": ..., "dy": ..., "dz": ...}`
6. `to_wkt()` no tiene representación WKT directa → lanza `GeometryError`
7. `__eq__` usa `math.isclose` con `EPSILON_GEOMETRY`
8. `__hash__` redondea a 9 decimales (como Point)
9. `from_tuple((dx, dy))` y `from_tuple((dx, dy, dz))`
10. `from_points(p, q)` → `Vector(q.x - p.x, q.y - p.y)`

---

## 11. ADRs

### ADR-001: Point - Point = Vector, no Point

**Contexto:** La diferencia entre dos posiciones es un desplazamiento,
no una posición. Es un error común en geometría computacional.

**Decisión:** `Point.__sub__(other)` devuelve `Vector`. `Point.__add__(other)`
con otro Point lanza `TypeError`.

**Consecuencias:**
+ Semántica matemática correcta
+ Consistencia con el álgebra lineal
- Código cliente debe ser explícito: `p + v` no `p + q`

### ADR-002: Vector no tiene posición

**Contexto:** Un Vector representa un desplazamiento, no una posición.
Operaciones como `bbox` deben reflejar esto.

**Decisión:** `Vector.bbox` devuelve un BoundingBox con origen en (0,0)
y extremo en (dx, dy). `Vector.center` no tiene significado y no se implementa.

**Consecuencias:**
+ Claridad semántica
+ `bbox` útil para representación visual
- `center` no está disponible (tampoco tiene sentido)

### ADR-003: Producto vectorial 2D devuelve escalar

**Contexto:** En 2D, el producto vectorial `cross(v, w)` produce un escalar
(la magnitud del vector Z resultante si v y w estuvieran en el plano XY).

**Decisión:** Si `Vector.dz == 0.0` para ambos operandos, `cross` devuelve
un `float`. Si alguno tiene dz ≠ 0, devuelve un `Vector` 3D.

**Consecuencias:**
+ API compacta para el caso 2D (el 99% de LINPRO)
+ Sin ruptura cuando se añada 3D
- El tipo de retorno cambia según los operandos (documentado)

### ADR-004: Rotación en radianes, sentido antihorario

**Contexto:** Consistencia con el resto del Geometry Engine.

**Decisión:** `rotate(angle)` rota en sentido antihorario, angle en radianes.

**Consecuencias:**
+ Consistente con `atan2`, `angle`, `signed_angle_to`
+ El usuario debe convertir grados a radianes si es necesario
+ `math.radians` y `math.degrees` son funciones estándar

---

## 12. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Vector nulo normalizado** | `PrecisionError` si no se protege | `normalized` lanza error; `is_zero` disponible para pre-chequeo |
| **Overflow en length con coordenadas grandes** | Pérdida de precisión | Usar `math.hypot` en lugar de `sqrt(dx² + dy²)` |
| **Confusión Point vs Vector** | Bugs sutiles en operaciones | Tipado fuerte, `__add__`/`__sub__` estrictos, documentación |
| **Producto cruz 2D vs 3D** | Código cliente espera tipo fijo | Documentar; el 99% de LINPRO usará cross 2D (float) |

---

## 13. Resumen de entidades

| Tipo | Rango ID | Cantidad |
|---|---|---|
| Responsabilidades | GEOM-VEC-001 a 030 | 30 |
| ADRs | ADR-001 a 004 | 4 |
| Operaciones prohibidas | — | 3 |
| Operaciones permitidas | — | 10 |

---

*Fin del RFC-0004A — Álgebra Vectorial*
