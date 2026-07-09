# Point — API Reference

## Constructor

```python
Point(x: float, y: float, z: float = 0.0)
```

### Parámetros

| Parámetro | Tipo | Default | Descripción |
|---|---|---|---|
| x | float | — | Coordenada X |
| y | float | — | Coordenada Y |
| z | float | 0.0 | Coordenada Z (opcional) |

### Lanza

- `InvalidCoordinateError` si x, y o z no son numéricos
- `InvalidCoordinateError` si x, y o z son NaN o infinito

## Propiedades

| Propiedad | Tipo | Descripción |
|---|---|---|
| `x` | float | Coordenada X (lectura) |
| `y` | float | Coordenada Y (lectura) |
| `z` | float | Coordenada Z (lectura) |

## Métodos de instancia

### `distance_to(other: Point) -> float`

Distancia euclidiana 3D entre dos puntos.

**Precondición:** `other` debe ser un `Point`.
**Postcondición:** resultado >= 0.0.

### `to_tuple() -> Tuple[float, float, float]`

Devuelve (x, y, z).

### `to_dict() -> Dict[str, float]`

Devuelve `{"x": x, "y": y, "z": z}`.

### `to_json() -> str`

Devuelve representación JSON del dict.

### `to_wkt() -> str`

Devuelve `"POINT (x y)"` (2D, sin z).

## Métodos de clase / estáticos

### `Point.from_tuple(data: Tuple[float, float] | Tuple[float, float, float]) -> Point`

Crea un Point desde una tupla de 2 o 3 elementos.

### `Point.from_dict(data: Dict[str, float]) -> Point`

Crea un Point desde un dict con claves "x", "y" y opcionalmente "z".

### `Point.from_json(data: str) -> Point`

Crea un Point desde un string JSON.

## Operadores

| Operador | Descripción |
|---|---|
| `p == q` | Igualdad con tolerancia EPSILON (1e-9) |
| `hash(p)` | Hash basado en coordenadas redondeadas |
| `repr(p)` | `"Point(x, y, z)"` |
| `str(p)` | `"Point(x, y, z)"` |