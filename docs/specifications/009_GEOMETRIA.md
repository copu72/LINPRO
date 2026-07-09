# 009 — GEOMETRÍA

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Submódulos

| Submódulo | Función |
|-----------|--------|
| `alignment` | Definición de ejes: tramos rectos, curvas circulares, clotoides |
| `pk` | Sistema de PK: interpolación, distancia acumulada |
| `buffer` | Generación de buffers con offset a izquierda/derecha |
| `intersections` | Cálculo de intersecciones entre el alignment y geometrías externas |
| `topology` | Validaciones topológicas: sentido, continuidad, solapamientos |
| `calculations` | Cálculos auxiliares: radios, ángulos, tangentes |

## Alignment

La clase `Alignment` se compone de una secuencia ordenada de segmentos:

```python
@dataclass
class Straight:
    start: Point
    end: Point

@dataclass
class CircularArc:
    start: Point
    end: Point
    radius: float
    center: Point
    direction: Literal["left", "right"]

@dataclass
class Clothoid:
    start: Point
    end: Point
    A: float
    start_radius: float
    end_radius: float
```