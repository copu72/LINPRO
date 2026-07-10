"""Geometry Engine de LINPRO — Kernel Matemático.

Independiente del resto de módulos.
Publicable como librería separada.
"""

from linpro.geometry.primitives.bbox import BoundingBox
from linpro.geometry.primitives.point import Point

__all__ = [
    "BoundingBox",
    "Point",
]
