"""Geometry Engine de LINPRO — Kernel Matemático.

Independiente del resto de módulos.
Publicable como librería separada.
"""

from linpro.geometry.primitives.bbox import BoundingBox
from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.polyline import Polyline
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.vector import Vector

# Engineering Axis alias
EngineeringAxis = Polyline

__all__ = [
    "BoundingBox",
    "EngineeringAxis",
    "PK",
    "Point",
    "Polyline",
    "Segment",
    "Vector",
]
