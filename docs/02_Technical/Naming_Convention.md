# Naming Convention

## Archivos

| Tipo | Convención | Ejemplo |
|---|---|---|
| Módulo | snake_case | `bounding_box.py`, `point.py` |
| Test | `test_` + nombre módulo | `test_bounding_box.py` |
| Directorio | snake_case | `geometry/primitives/` |
| Documentación | PascalCase con guiones | `API-Reference.md` |

## Identificadores

| Elemento | Convención | Correcto | Incorrecto |
|---|---|---|---|
| Clase | PascalCase | `BoundingBox` | `bounding_box`, `boundingbox` |
| Método | snake_case | `distance_to` | `distanceTo`, `DistanceTo` |
| Propiedad | snake_case | `p.x`, `seg.length` | `p.X`, `seg.Length` |
| Parámetro | snake_case | `other`, `tolerance` | `otherPoint`, `tolValue` |
| Variable local | snake_case | `temp_point` | `tempPoint`, `tp` |
| Constante | UPPER_SNAKE | `EPSILON` | `epsilon`, `Epsilon` |
| Privado | prefijo _ | `_x`, `_points` | `x_`, `__x` (name mangling) |

## Verbos para métodos

| Operación | Verbo | Ejemplo |
|---|---|---|
| Consulta | sin verbo (propiedad) | `p.x`, `seg.length` |
| Cálculo | `compute_` (caro) | `poly.compute_length()` |
| Validación | `validate_`, `assert_` | `validate_coordinate` |
| Conversión | `to_` | `p.to_dict()`, `p.to_wkt()` |
| Construcción | `from_` | `Point.from_dict(data)` |
| Transformación | verbo + nueva instancia | `vec.rotate(angle)` |
| Verificación | `is_`, `has_`, `contains_` | `bbox.contains_point(p)` |
