# Módulo Infrastructure — Análisis de infraestructuras existentes

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Identificación de cruces y afecciones del trazado con infraestructuras existentes (líneas eléctricas, tuberías, ferrocarriles, etc.).

## API pública

```python
def get_infrastructure_crossings(project: Project) -> list[InfraCrossing]
```
Obtiene la lista de cruces del trazado con infraestructuras existentes.

### Tipo InfraCrossing

| Atributo         | Tipo    | Descripción                                   |
| ---------------- | ------- | --------------------------------------------- |
| `infra_type`     | `str`   | Tipo (línea eléctrica, ferrocarril, tubería…).|
| `infra_id`       | `str`   | Identificador de la infraestructura.         |
| `infra_operator` | `str`   | Operador o compañía titular.                 |
| `crossing_pk`    | `float` | PK del punto de cruce.                      |
| `crossing_point` | `Point` | Coordenadas del punto de cruce.             |
| `notes`          | `str`   | Observaciones adicionales.                  |

## Dependencias

- Cartografía de infraestructuras (IGN, operadores).
- Capas opcionales según el tipo de proyecto (gas, electricidad, ferrocarril).

## Uso básico

```python
from linpro.gis import Project
from linpro.gis.infrastructure import get_infrastructure_crossings

project = Project("C:/data/proyecto.linpro")
cruces = get_infrastructure_crossings(project)
for c in cruces:
    print(f"[{c.infra_type}] {c.infra_name} en PK {c.crossing_pk:.3f}")
```