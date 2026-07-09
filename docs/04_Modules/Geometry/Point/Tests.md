# Point — Tests

## Cobertura objetivo

| Módulo | Cobertura mínima |
|---|---|
| `point.py` | ≥95% |

## Casos de prueba

| # | Escenario | Verifica |
|---|---|---|
| 1 | Creación 2D | coordenadas correctas |
| 2 | Creación 3D | z se almacena correctamente |
| 3 | Creación con enteros | conversión a float automática |
| 4 | Propiedades solo lectura | TypeError al asignar |
| 5 | distance_to 2D | (0,0)->(3,4) = 5 |
| 6 | distance_to 3D | (0,0,0)->(2,3,6) = 7 |
| 7 | distance_to mismo punto | 0 |
| 8 | Igualdad exacta | == |
| 9 | Igualdad con tolerancia | dentro de EPSILON |
| 10 | Desigualdad | != |
| 11 | Hash | mismo punto = mismo hash |
| 12 | Hash en set | sin duplicados |
| 13 | to_tuple | (x, y, z) |
| 14 | to_dict | claves correctas |
| 15 | to_json | JSON válido |
| 16 | to_wkt | formato POINT |
| 17 | from_tuple 2 elem | crea con z=0 |
| 18 | from_tuple 3 elem | crea con z dado |
| 19 | from_dict | crea correctamente |
| 20 | from_json | crea correctamente |
| 21 | Error: x NaN | InvalidCoordinateError |
| 22 | Error: y inf | InvalidCoordinateError |
| 23 | Error: tipo str | InvalidCoordinateError |
| 24 | repr | formato esperado |
| 25 | str | formato esperado |
| 26 | from_tuple tipo inválido | error |
| 27 | from_dict falta clave | KeyError |