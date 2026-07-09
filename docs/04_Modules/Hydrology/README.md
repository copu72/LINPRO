# Módulo Hydrology — Análisis hidrográfico

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Identificación y análisis de cruces del trazado con la red hidrográfica, incluyendo ríos, arroyos y masas de agua.

## Requisitos funcionales

| ID      | Descripción                |
| ------- | -------------------------- |
| FR-0008 | Analizar Hidrografía.      |

## API pública

```python
def get_river_crossings(project: Project) -> list[RiverCrossing]
```
Obtiene la lista de cruces del trazado con la red hidrográfica.

### Tipo RiverCrossing

| Atributo         | Tipo    | Descripción                                   |
| ---------------- | ------- | --------------------------------------------- |
| `water_name`     | `str`   | Nombre del río, arroyo o masa de agua.       |
| `water_type`     | `str`   | Tipo (río, arroyo, lago, embalse).           |
| `crossing_pk`    | `float` | PK del punto de cruce.                      |
| `crossing_point` | `Point` | Coordenadas del punto de cruce.             |
| `flow_regime`    | `str`   | Régimen (permanente, estacional, efímero).   |
| `width`          | `float` | Ancho estimado en el cruce (m).             |

## Dependencias

- Red hidrográfica (MAS) del Ministerio o Confederación Hidrográfica.
- Capa de Dominio Público Hidráulico (DPH) si está disponible.

## Uso básico

```python
from linpro.gis import Project
from linpro.gis.hydrology import get_river_crossings

project = Project("C:/data/proyecto.linpro")
cruces = get_river_crossings(project)
for c in cruces:
    print(f"{c.water_name} — PK {c.crossing_pk:.3f} ({c.flow_regime})")
```