# Vector — Tests

## Cobertura objetivo

| Módulo | Cobertura mínima |
|---|---|
| `vector.py` | ≥95% |

## Casos de prueba

| # | Escenario | Verifica |
|---|---|---|
| 1 | Creación básica | dx, dy correctos |
| 2 | Creación con enteros | conversión a float |
| 3 | length | sqrt(dx²+dy²) |
| 4 | length vector nulo | 0.0 |
| 5 | angle | atan2(dy, dx) |
| 6 | angle vector nulo | 0.0 |
| 7 | normalized | longitud 1.0 |
| 8 | normalized vector nulo | Vector(0,0) |
| 9 | dot | ortogonales → 0 |
| 10 | cross | paralelos → 0 |
| 11 | angle_to | ángulo entre vectores |
| 12 | rotate | rotación correcta |
| 13 | perpendicular | (-dy, dx) |
| 14 | suma | (ax+bx, ay+by) |
| 15 | resta | (ax-bx, ay-by) |
| 16 | multiplicación escalar | (s*dx, s*dy) |
| 17 | to_tuple | (dx, dy) |
| 18 | to_dict | {"dx": ..., "dy": ...} |
| 19 | to_wkt | "POINT (dx dy)" |
| 20 | from_points | p2 - p1 |
| 21 | from_angle | dirección + longitud |
| 22 | igualdad exacta | == |
| 23 | igualdad tolerancia | dentro de EPSILON |
| 24 | desigualdad | != |
| 25 | hash | consistente |
| 26 | hash en set | sin duplicados |
| 27 | inmutable | AttributeError al asignar dx |
| 28 | error NaN | InvalidCoordinateError |
| 29 | error infinito | InvalidCoordinateError |
| 30 | error tipo string | InvalidCoordinateError |
| 31 | almost_equal | tolerancia explícita |
| 32 | check_invariants | pasa sin error |