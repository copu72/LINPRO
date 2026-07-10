# Docstring Convention

LINPRO usa **Google-style docstrings** con adaptaciones propias.

## Formato general

```python
def distance_to(self, other: Point) -> float:
    """Distancia euclidiana 3D hasta otro punto.

    Args:
        other: Punto destino.

    Returns:
        Distancia siempre >= 0.

    Raises:
        TypeError: Si other no es Point.
    """
```

## Reglas

1. **Primera línea:** breve descripción en tercera persona del singular. Termina en punto.
2. **Línea en blanco** después de la primera línea si hay más secciones.
3. **Args:** un parámetro por línea. Tipo documentado en type hint, no en texto.
4. **Returns:** siempre documentar el tipo y semántica. Si es `None`, puede omitirse.
5. **Raises:** solo documentar excepciones que el usuario debe manejar.
6. **Módulos:** todo archivo .py lleva docstring describiendo su propósito.

## Clases

```python
class Point:
    """Punto en el espacio cartesiano 2D/3D.

    Inmutable, hashable, serializable.
    Es la primitiva fundamental del Geometry Engine.

    Invariantes:
        - x, y, z son float
        - Ninguna coordenada es NaN o infinito
        - La igualdad usa EPSILON (1e-9)
        - Es inmutable

    Example:
        >>> p = Point(10.0, 20.0)
        >>> p.distance_to(Point(13.0, 24.0))
        5.0
    """
```

## Excepciones

```python
class InvalidCoordinateError(GeometryError):
    """Coordenada inválida: NaN, infinito o tipo incorrecto."""
```

## Archivos

```python
"""GEOM-004: Point — punto en el espacio 2D/3D.

Inmutable, hashable, serializable.
Es la primitiva fundamental del Geometry Engine de LINPRO.
"""
```
