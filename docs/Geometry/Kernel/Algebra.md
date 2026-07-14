# Álgebra Vectorial — Especificación Matemática

**Proyecto:** LINPRO
**Componente:** Geometry Engine
**Versión:** 1.0.0
**Estado:** ⚡ Aprobado (vía RFC-0004A)
**Fecha:** 2026-07-10

---

## 1. Espacio vectorial

LINPRO opera en un **espacio vectorial real** ℝ² (principalmente) y ℝ³
(preparado para futuro). Las coordenadas son números reales (`float` de
64 bits, precisión ~15 dígitos decimales).

### 1.1 Elementos del espacio

| Elemento | Símbolo | Representación | Pertenece a |
|---|---|---|---|
| Punto | p, q | `(x, y, z)` | ℝ³ |
| Vector | v, w | `(dx, dy, dz)` | ℝ³ (espacio vectorial) |
| Escalar | λ, μ | `float` | ℝ |

### 1.2 Axiomas del espacio vectorial

Para todo u, v, w ∈ V y λ, μ ∈ ℝ:

| Propiedad | Fórmula |
|---|---|
| Asociativa | `(u + v) + w = u + (v + w)` |
| Conmutativa | `u + v = v + u` |
| Elemento neutro | `v + 0 = v` |
| Elemento opuesto | `v + (-v) = 0` |
| Distributiva (escalar) | `λ·(u + v) = λ·u + λ·v` |
| Distributiva (vector) | `(λ + μ)·v = λ·v + μ·v` |
| Asociativa mixta | `λ·(μ·v) = (λμ)·v` |
| Identidad escalar | `1·v = v` |

---

## 2. Operaciones fundamentales

### 2.1 Suma de vectores

```
v + w = (dx₁ + dx₂, dy₁ + dy₂, dz₁ + dz₂)
```

### 2.2 Producto por escalar

```
λ · v = (λ·dx, λ·dy, λ·dz)
```

### 2.3 Producto escalar (dot product)

```
v · w = dx₁·dx₂ + dy₁·dy₂ + dz₁·dz₂
```

Propiedades:
- Conmutativo: `v · w = w · v`
- Distributivo: `u · (v + w) = u · v + u · w`
- `v · v = ‖v‖² ≥ 0`
- `v · v = 0` ⇔ `v = 0`

### 2.4 Producto vectorial (cross product) — 2D

En 2D, el producto vectorial es un **escalar** que representa la magnitud
del vector Z resultante:

```
v × w = dx₁·dy₂ - dy₁·dx₂
```

- `v × w = 0` ⇔ v y w son paralelos (colineales)
- `|v × w| = ‖v‖ · ‖w‖ · |sin(θ)|`
- Anticonmutativo: `v × w = -(w × v)`

### 2.5 Producto vectorial (cross product) — 3D

```
v × w = (dy₁·dz₂ - dz₁·dy₂, dz₁·dx₂ - dx₁·dz₂, dx₁·dy₂ - dy₁·dx₂)
```

---

## 3. Normas y métricas

### 3.1 Norma euclidiana (longitud, módulo)

```
‖v‖ = √(dx² + dy² + dz²)
```

Implementación: `math.hypot(dx, dy, dz)` para evitar overflow.

### 3.2 Distancia entre vectores

```
d(v, w) = ‖v - w‖
```

### 3.3 Vector unitario (versor)

```
û = v / ‖v‖      (si ‖v‖ ≠ 0)
```

Si `‖v‖ = 0`, la normalización no está definida.

---

## 4. Ángulos

### 4.1 Ángulo entre vectores

```
θ = arccos((v · w) / (‖v‖ · ‖w‖))     θ ∈ [0, π]
```

### 4.2 Ángulo con signo (2D)

```
θ_signed = atan2(v × w, v · w)         θ ∈ [-π, π]
```

Positivo = antihorario de v a w.

### 4.3 Ángulo absoluto de un vector

```
α = atan2(dy, dx)                      α ∈ [-π, π]
```

α = 0 → dirección del eje X positivo.

### 4.4 Correspondencia con azimut

| Convenio | Origen | Sentido positivo |
|---|---|---|
| LINPRO (matemático) | Eje X+ (Este) | Antihorario |
| Topográfico | Eje Y+ (Norte) | Horario |

**El Kernel usa exclusivamente el convenio matemático.**
La conversión a azimut topográfico es responsabilidad del módulo de dominio:

```
azimut_rad = π/2 - α      (con ajuste a [0, 2π))
```

---

## 5. Proyecciones

### 5.1 Proyección escalar de v sobre w

```
comp_w(v) = (v · w) / ‖w‖
```

### 5.2 Proyección vectorial de v sobre w

```
proj_w(v) = ((v · w) / (w · w)) · w
```

### 5.3 Rechazo (componente perpendicular)

```
rej_w(v) = v - proj_w(v)
```

---

## 6. Operadores entre tipos

### 6.1 Tabla completa

| Operación | Resultado | Implementación |
|---|---|---|
| `p - q` | `Vector` | `Vector(p.x - q.x, p.y - q.y)` |
| `p + v` | `Point` | `Point(p.x + v.dx, p.y + v.dy)` |
| `p - v` | `Point` | `Point(p.x - v.dx, p.y - v.dy)` |
| `v + w` | `Vector` | `Vector(v.dx + w.dx, v.dy + w.dy)` |
| `v - w` | `Vector` | `Vector(v.dx - w.dx, v.dy - w.dy)` |
| `v * λ` | `Vector` | `Vector(v.dx * λ, v.dy * λ)` |
| `λ * v` | `Vector` | `Vector(v.dx * λ, v.dy * λ)` |
| `v / λ` | `Vector` | `Vector(v.dx / λ, v.dy / λ)` |
| `-v` | `Vector` | `Vector(-v.dx, -v.dy)` |
| `v + p` | `Point` | `Point(p.x + v.dx, p.y + v.dy)` |

### 6.2 Operaciones prohibidas

| Operación | Razón |
|---|---|
| `p + q` | Dos posiciones no se suman |
| `λ * p` | Un punto escalado no tiene sentido sin centro |
| `p / λ` | Ídem |
| `v · p` | Producto escalar mixto no definido |

---

## 7. Rotaciones (2D)

Rotación antihoraria de un vector por un ángulo θ:

```
dx' = dx·cos(θ) - dy·sin(θ)
dy' = dx·sin(θ) + dy·cos(θ)
```

Forma matricial:

```
[dx']   [cos θ  -sin θ] [dx]
[dy'] = [sin θ   cos θ] [dy]
```

### 7.1 Vector perpendicular (2D)

El vector perpendicular antihorario a `(dx, dy)` es `(-dy, dx)`.

El vector perpendicular horario es `(dy, -dx)`.

LINPRO implementa `.perpendicular` como antihorario por defecto.

---

## 8. Relaciones geométricas

### 8.1 Paralelismo

Dos vectores son paralelos si:

```
v × w = 0      (dentro de tolerancia)
```

Equivalente: `|sin(θ)| < ε` o `|v · w| ≈ ‖v‖·‖w‖`.

### 8.2 Perpendicularidad

Dos vectores son perpendiculares si:

```
v · w = 0      (dentro de tolerancia)
```

Equivalente: `|cos(θ)| < ε`.

### 8.3 Colinealidad

Tres puntos p, q, r son colineales si:

```
(p - q) × (r - q) = 0      (dentro de tolerancia)
```

---

## 9. Tolerancias

Todas las comparaciones vectoriales usan `EPSILON_GEOMETRY` (1e-9) por defecto.
Ver `GEOMETRY_KERNEL_SPEC.md` sección 7 para la definición completa.

| Operación | Tolerancia por defecto |
|---|---|
| `almost_equal` | 1e-9 |
| `is_parallel` | 1e-9 |
| `is_perpendicular` | 1e-9 |
| `is_zero` | 1e-9 |
| `is_unit` | 1e-9 |

---

## 10. Convenciones de nomenclatura

| Concepto | Nombre en LINPRO | Unidades |
|---|---|---|
| Componente X | `.dx` | coordenada proyectada |
| Componente Y | `.dy` | coordenada proyectada |
| Componente Z | `.dz` | coordenada proyectada |
| Longitud | `.length` | coordenada proyectada |
| Longitud² | `.length_squared` | coordenada proyectada² |
| Ángulo absoluto | `.angle` | radianes |
| Vector unitario | `.normalized` | adimensional |
| Vector perpendicular | `.perpendicular` | coordenada proyectada |
| Producto escalar | `.dot(other)` | coordenada proyectada² |
| Producto vectorial 2D | `.cross(other) → float` | coordenada proyectada² |
| Producto vectorial 3D | `.cross(other) → Vector` | coordenada proyectada² |
| Ángulo entre vectores | `.angle_to(other)` | radianes |
| Ángulo con signo | `.signed_angle_to(other)` | radianes |

---

## 11. Referencias cruzadas

| Concepto | Documento |
|---|---|
| Tolerancias | `GEOMETRY_KERNEL_SPEC.md §7` |
| Geometry(ABC) | `GEOMETRY_KERNEL_SPEC.md §10` |
| Point | `RFC-0002-Point.md` |
| BoundingBox | `RFC-0003-BoundingBox.md` |
| Álgebra vectorial (este doc) | `RFC-0004A-Algebra-Vectorial.md` |
| Vector (implementación) | `RFC-0004B-Vector.md` (futuro) |

---

*Este documento es la referencia matemática permanente del Geometry Engine.*
*Cualquier cambio en el álgebra requiere revisión de arquitectura.*
