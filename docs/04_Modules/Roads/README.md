# Módulo Roads — Análisis de cruces con carreteras

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Identificación y análisis de cruces entre el trazado del proyecto y la red de carreteras.

## Requisitos funcionales

| ID      | Descripción                |
| ------- | -------------------------- |
| FR-0007 | Analizar Carreteras.       |

## API pública

```python
def get_road_crossings(project: Project) -> list[RoadCrossing]
```
Obtiene la lista de cruces del trazado con carreteras, incluyendo el punto de intersección, la carretera afectada y el ángulo de cruce.

### Tipo RoadCrossing

| Atributo         | Tipo    | Descripción                                  |
| ---------------- | ------- | -------------------------------------------- |
| `road_id`        | `str`   | Identificador de la carretera.              |
| `road_name`      | `str`   | Nombre o denominación de la carretera.      |
| `crossing_pk`    | `float` | PK del punto de cruce.                     |
| `crossing_point` | `Point` | Coordenadas del punto de cruce.            |
| `angle`          | `float` | Ángulo de intersección (grados).            |
| `road_category`  | `str`   | Categoría (autovía, nacional, autonómica…).|

## Dependencias

- Red de carreteras (formato Shapefile/GeoPackage del Mapa de Tráfico).
- `linpro.geometry.pk` para cálculo de PK en el cruce.

## Uso básico

```python
from linpro.gis import Project
from linpro.gis.roads import get_road_crossings

project = Project("C:/data/proyecto.linpro")
cruces = get_road_crossings(project)
for c in cruces:
    print(f"{c.road_name} en PK {c.crossing_pk:.3f} — {c.angle:.1f}°")
```