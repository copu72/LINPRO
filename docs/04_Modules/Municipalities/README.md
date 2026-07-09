# Módulo Municipalities — Análisis de afección municipal

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Análisis de afección municipal del proyecto, identificando los municipios intersectados por el trazado y su buffer.

## Requisitos funcionales

| ID      | Descripción                |
| ------- | -------------------------- |
| FR-0005 | Analizar Municipios.       |

## API pública

```python
def get_municipalities(project: Project) -> list[Municipality]
```
Obtiene la lista de municipios afectados por el proyecto, incluyendo superficie de afección y longitud de trazado por municipio.

### Tipo Municipality

| Atributo        | Tipo    | Descripción                              |
| --------------- | ------- | ---------------------------------------- |
| `code`          | `str`   | Código INE del municipio.               |
| `name`          | `str`   | Nombre del municipio.                   |
| `province`      | `str`   | Provincia a la que pertenece.           |
| `area_affected` | `float` | Superficie afectada (m²).               |
| `length_affected` | `float` | Longitud de trazado dentro del municipio (m). |

## Dependencias

- Capa SIG de límites municipales (formato GeoPackage/GeoJSON).
- `linpro.gis` para carga de capas.
- `shapely` para operaciones de intersección.

## Uso básico

```python
from linpro.gis import Project
from linpro.gis.municipalities import get_municipalities

project = Project("C:/data/proyecto.linpro")
municipios = get_municipalities(project)
for m in municipios:
    print(f"{m.name}: {m.area_affected:.2f} m²")
```