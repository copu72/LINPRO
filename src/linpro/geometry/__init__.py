"""Geometry Engine de LINPRO.

Motor matemático puro. No conoce nada de GIS, CAD, Excel ni
ningún módulo de negocio. Solo sabe hacer geometría.
"""

from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.vector import Vector
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.bbox import BoundingBox

__all__ = [
    "Point",
    "Vector",
    "Segment",
    "BoundingBox",
]