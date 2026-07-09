# Módulo PK — Sistema de Puntos Kilométricos

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Sistema de Puntos Kilométricos para la localización y referencia de puntos sobre el eje de un proyecto lineal.

## Requisitos funcionales

| ID      | Descripción               |
| ------- | ------------------------- |
| FR-0002 | Calcular PK.              |

## API pública

```python
def calc_pk(x: float, y: float) -> float
```
Calcula el punto kilométrico (PK) correspondiente a las coordenadas (x, y) mediante proyección sobre el eje de referencia.

```python
def calc_coords(pk: float) -> tuple[float, float]
```
Devuelve las coordenadas (x, y) del punto kilométrico dado sobre el eje del proyecto.

```python
def format_pk(pk: float) -> str
```
Formatea un valor PK como cadena legible (ej. `1+234.567`).

## Dependencias

- `shapely` para operaciones geométricas sobre el eje de referencia.
- `linpro.geometry` para tipos base.

## Uso básico

```python
from linpro.geometry.pk import calc_pk, calc_coords, format_pk

pk = calc_pk(687432.10, 4178654.33)
x, y = calc_coords(pk)
print(format_pk(pk))  # "0+123.456"
```