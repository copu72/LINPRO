# Módulo Buffer — Generación de buffers simétricos y asimétricos

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Generación de buffers geométricos que representan la zona de afección de un eje lineal, permitiendo anchos diferenciados por lado.

## Requisitos funcionales

| ID      | Descripción               |
| ------- | ------------------------- |
| FR-0003 | Generar buffer.           |

## API pública

```python
class Buffer:
    def __init__(self, alignment: LineString, left: float, right: float)
```

**Parámetros:**

| Parámetro  | Tipo        | Descripción                                              |
| ---------- | ----------- | -------------------------------------------------------- |
| `alignment`| `LineString`| Eje de referencia sobre el que se genera el buffer.      |
| `left`     | `float`     | Ancho del buffer al lado izquierdo del eje (metros).     |
| `right`    | `float`     | Ancho del buffer al lado derecho del eje (metros).       |

**Métodos:**

```python
def generate(self) -> Polygon
```
Genera y retorna un polígono que representa la envolvente del buffer asimétrico alrededor del eje.

Si `left == right`, el resultado equivale a un buffer simétrico estándar.

## Dependencias

- `shapely.geometry.LineString` y `shapely.geometry.Polygon`.
- Algoritmo de offset lateral para buffers asimétricos.

## Uso básico

```python
from shapely.geometry import LineString
from linpro.geometry.buffer import Buffer

eje = LineString([(0, 0), (100, 0), (200, 50)])
buffer = Buffer(alignment=eje, left=50.0, right=30.0)
poligono = buffer.generate()
```