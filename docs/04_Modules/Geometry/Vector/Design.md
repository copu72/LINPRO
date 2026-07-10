# Vector — Design

## Decisión: propiedades vs getters

Se usan propiedades (`length`, `angle`, `normalized`) porque son valores derivados
que no requieren argumentos. La sintaxis `v.length` es más limpia que `v.length()`.

## Decisión: from_points

`Vector.from_points(p1, p2)` devuelve `Vector(p2.x - p1.x, p2.y - p1.y)`.
No se permite `Vector.from_points(p1, p2)` con un solo punto (no hay vector degenerado).

## Vector nulo

`Vector(0, 0)` es válido. Su `normalized` devuelve `Vector(0, 0)` para evitar división por cero.
Su `angle` devuelve `0.0`.

## Diagrama de flujo

```
Vector(dx, dy)
  ├─ Validation.assert_finite(dx, dy)
  └─ self._dx, self._dy = float(dx), float(dy)
        │
        ├─ .length  → sqrt(dx² + dy²)
        ├─ .angle   → atan2(dy, dx)
        ├─ .normalized → Vector(dx/length, dy/length) o (0,0)
        ├─ .dot(other) → dx*odx + dy*ody
        ├─ .cross(other) → dx*ody - dy*odx
        ├─ .rotate(α) → Vector(dx·cosα - dy·sinα, dx·sinα + dy·cosα)
        ├─ .perpendicular() → Vector(-dy, dx)
        └─ from_points(p1, p2) → Vector(p2.x-p1.x, p2.y-p1.y)
```