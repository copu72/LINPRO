# Kernel — Requirements

| ID | Requisito | Prioridad |
|---|---|---|
| KER-001 | Sistema de tolerancias con tres niveles (math, geometry, visual) | Alta |
| KER-002 | Comparaciones con tolerancia (equals, is_zero, distance_equals, angle_equals) | Alta |
| KER-003 | Validación numérica (finito, NaN, inf, tipo) | Alta |
| KER-004 | Validación de coordenadas (x, y, z) | Alta |
| KER-005 | Validación de geometrías (tipo, invariantes) | Alta |
| KER-006 | Clase base abstracta Geometry con contratos | Alta |
| KER-007 | Constantes globales (EPSILONs, VERSION, DEFAULT_CRS, MAX_ITERATIONS) | Alta |
| KER-008 | Excepciones propias (GeometryError, InvalidCoordinateError, PrecisionError, ValidationError) | Alta |
| KER-009 | Serialización base (to_dict, from_dict, to_json, from_json, to_wkt) | Alta |
| KER-010 | Tests unitarios con cobertura ≥95% | Alta |
