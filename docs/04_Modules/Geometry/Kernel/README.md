# Kernel — Geometry Kernel

## Descripción

Núcleo matemático del Geometry Engine. Define las reglas fundamentales:
tolerancias, validaciones, constantes globales y el contrato abstracto
que toda entidad geométrica debe cumplir.

## Componentes

| Módulo | Responsabilidad |
|---|---|
| `constants.py` | Constantes globales: epsilon, CRS por defecto, precisión, versión |
| `tolerance.py` | Clase `Tolerance` con tres niveles de precisión (math, geometry, visual) |
| `validation.py` | Validadores: `NumericValidator`, `CoordinateValidator`, `GeometryValidator` |
| `geometry.py` | `Geometry(ABC)` — clase base abstracta con contratos obligatorios |

## Dependencias

- Solo `math`, `json`, `abc` de la stdlib
- No depende de ninguna otra parte de LINPRO

## No depende de

- Shapely, AutoCAD, DXF, GIS, Excel, ningún adaptador
