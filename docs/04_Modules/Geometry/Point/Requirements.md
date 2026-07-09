# Point — Requirements

| ID | Requisito | Prioridad | Estado |
|---|---|---|---|
| GEOM-004 | Crear Point con x, y | Alta | ✅ |
| GEOM-004b | Crear Point con x, y, z (z opcional, default 0) | Alta | ✅ |
| GEOM-005 | Igualdad con tolerancia (==) | Alta | ✅ |
| GEOM-006 | Distancia entre puntos (distance_to) | Alta | pescada |
| GEOM-007 | Conversión a tupla (to_tuple) | Media | ✅ |
| GEOM-008 | Conversión a WKT (to_wkt) | Media | ✅ |
| GEOM-009 | Serialización JSON (to_dict, to_json, from_dict, from_json, from_tuple) | Media | ✅ |
| GEOM-010 | Tests unitarios | Alta | ✅ |
| — | Representación (repr y str) | Media | ✅ |
| — | Hashable | Alta | ✅ |
| — | Inmutable | Alta | ✅ |
| — | Validación de coordenadas (NaN, inf, tipo) | Alta | ✅ |
| — | Distancia 2D | Alta | ✅ |
| — | Distancia 3D | Alta | ✅ |