# Point

## Descripción

Punto en el plano cartesiano 2D/3D. Es la primitiva fundamental de todo el Geometry Engine.

## Responsabilidades

- Representar una posición en el espacio con coordenadas (x, y, z).
- Calcular distancia euclidiana a otro punto.
- Serializar y deserializar (tupla, dict, JSON, WKT).
- Compararse con tolerancia global.

## Invariantes

| Invariante | Descripción |
|---|---|
| Coordenadas numéricas | x, y, z deben ser `int` o `float` |
| Sin NaN | Ninguna coordenada puede ser NaN |
| Sin infinito | Ninguna coordenada puede ser ±inf |
| Inmutabilidad | Una vez creado, no se puede modificar |
| Hashable | Debe poder usarse en sets y como clave de dict |
| Igualdad con tolerancia | La igualdad usa EPSILON global |
| Serialización sin pérdida | to_json / from_json preservan precisión |

## Dependencias

- `linpro.geometry.kernel.constants` (EPSILON)
- `linpro.geometry.kernel.validation` (assert_finite)
- `linpro.geometry.exceptions` (InvalidCoordinateError)
- `math` (sqrt, isclose)

## No depende de

- Shapely, AutoCAD, DXF, GeoPandas, ningún adaptador.