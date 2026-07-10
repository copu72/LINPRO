# Vector — API Reference

## Constructor

```python
Vector(dx: float, dy: float)
```

| Parámetro | Tipo | Default | Descripción |
|---|---|---|---|
| dx | float | — | Componente X del vector |
| dy | float | — | Componente Y del vector |

### Lanza

- `InvalidCoordinateError` si dx o dy no son numéricos, son NaN o infinito

## Propiedades

| Propiedad | Tipo | Descripción |
|---|---|---|
| `.dx` | float | Componente X |
| `.dy` | float | Componente Y |
| `.length` | float | Magnitud euclidiana (≥ 0) |
| `.angle` | float | Ángulo desde el eje X positivo (radianes, `[-π, π]`) |
| `.normalized` | Vector | Vector unitario (misma dirección); `Vector(0,0)` si el vector es nulo |

## Métodos de instancia

### `dot(other: Vector) -> float`

Producto escalar.

### `cross(other: Vector) -> float`

Producto vectorial (componente Z del producto 3D).

### `angle_to(other: Vector) -> float`

Ángulo entre vectores en radianes. Usa `atan2(cross, dot)` para cubrir todo el rango `[-π, π]`.

### `rotate(angle: float) -> Vector`

Rota el vector `angle` radianes. Devuelve nueva instancia.

### `perpendicular() -> Vector`

Devuelve `Vector(-dy, dx)` (giro −90°, sentido antihorario).

### `to_tuple() -> Tuple[float, float]`

Devuelve `(dx, dy)`.

### `to_dict() -> dict`

Devuelve `{"dx": dx, "dy": dy}`.

### `to_wkt() -> str`

Devuelve `"POINT (dx dy)"`.

### `almost_equal(other: object, tol: float) -> bool`

Comparación con tolerancia explícita.

### `check_invariants() -> None`

## Métodos de clase

### `Vector.from_points(p1: Point, p2: Point) -> Vector`

Vector desde p1 a p2: `p2 - p1`.

### `Vector.from_angle(angle: float, length: float = 1.0) -> Vector`

Vector con dirección y magnitud dadas.

## Operadores

| Operador | Descripción |
|---|---|
| `v + w` | Suma vectorial |
| `v - w` | Resta vectorial |
| `v * s` | Multiplicación escalar |
| `v == w` | Igualdad con EPSILON |
| `hash(v)` | Hash basado en (dx, dy) redondeados |
| `repr(v)` | `"Vector(dx, dy)"` |
| `str(v)` | `"Vector(dx, dy)"` |