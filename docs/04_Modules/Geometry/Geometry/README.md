# Geometry — Base Abstract Class

## Descripción

Clase base abstracta para todas las entidades geométricas del Kernel Geometry.
Define los contratos que toda subclase debe cumplir.

## Responsabilidades

- Establecer la interfaz común (`almost_equal`, `to_dict`, `from_dict`, `to_wkt`, `check_invariants`)
- Definir la tolerancia por defecto de la clase (`_EPSILON`)
- Proporcionar la propiedad `bbox` para toda entidad
- Garantizar que todas las subclases implementen invariantes

## Invariantes

| Invariante | Descripción |
|---|---|
| Toda entidad tiene `_EPSILON` | Constante de clase para comparaciones |
| Toda entidad implementa `almost_equal` | Comparación con tolerancia explícita |
| `to_dict` / `from_dict` son inversos | `T.from_dict(obj.to_dict()) == obj` dentro de tolerancia |
| `check_invariants` no lanza | En estado válido pasa sin error |

## No depende de

- Shapely, AutoCAD, DXF, GIS, ningún adaptador

## Dependencias

- `linpro.geometry.kernel.tolerance`
- `abc` (ABC, abstractmethod)
