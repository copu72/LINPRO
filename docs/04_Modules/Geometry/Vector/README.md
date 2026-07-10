# Vector

## Descripción

Vector en el plano 2D. Representa un desplazamiento o dirección (dx, dy).
No tiene origen anclado: es solo magnitud y dirección.

## Responsabilidades

- Representar un desplazamiento (dx, dy).
- Calcular longitud, ángulo, normalizado, perpendicular.
- Operaciones vectoriales: suma, resta, producto escalar, producto vectorial.
- Rotación.
- Creación desde dos puntos o desde ángulo.
- Serialización (tupla, dict, JSON, WKT — como `POINT`).
- Comparación con tolerancia.

## Invariantes

| Invariante | Descripción |
|---|---|
| Coordenadas numéricas | dx, dy deben ser `int` o `float` |
| Sin NaN | Ninguna coordenada puede ser NaN |
| Sin infinito | Ninguna coordenada puede ser ±inf |
| Inmutabilidad | Una vez creado, no se puede modificar |
| Hashable | Debe poder usarse en sets |
| Igualdad con tolerancia | Usa EPSILON global |
| `length` es siempre ≥ 0 | Longitud nunca negativa |
| `normalized` tiene longitud 1 | Dentro de tolerancia |
| Vector(0,0).normalized es Vector(0,0) | Caso especial de vector nulo |

## API

```python
Vector(dx: float, dy: float)
```

| Propiedad | Tipo | Descripción |
|---|---|---|
| `.dx` | float | Componente X |
| `.dy` | float | Componente Y |
| `.length` | float | Magnitud euclidiana |
| `.angle` | float | Ángulo desde el eje X positivo (radianes) |
| `.normalized` | Vector | Vector unitario (misma dirección) |

| Método | Retorno | Descripción |
|---|---|---|
| `dot(other)` | float | Producto escalar |
| `cross(other)` | float | Producto vectorial (z) |
| `angle_to(other)` | float | Ángulo entre vectores (radianes) |
| `rotate(angle)` | Vector | Rotación (nueva instancia) |
| `perpendicular()` | Vector | Vector perpendicular (giro −90°) |
| `to_tuple()` | `(dx, dy)` | Desempaquetado rápido |
| `to_dict()` | dict | `{"dx": ..., "dy": ...}` |
| `to_wkt()` | str | `"POINT (dx dy)"` |
| `almost_equal(other, tol)` | bool | Comparación con tolerancia |
| `check_invariants()` | None | Verifica invariantes |
| `__eq__`, `__hash__`, `__repr__`, `__str__` | — | Estándar |
| `__add__`, `__sub__`, `__mul__` | Vector | Aritmética |
| `from_points(p1, p2)` | Vector | Diferencia p2 - p1 |
| `from_angle(angle, length=1.0)` | Vector | Desde ángulo |

## Dependencias

- `linpro.geometry.kernel.constants` (EPSILON)
- `linpro.geometry.kernel.validation`
- `linpro.geometry.exceptions`
- `math`

## No depende de

- Shapely, AutoCAD, DXF, GIS, ningún adaptador