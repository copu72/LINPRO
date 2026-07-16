"""Helper functions for detectors — Geometry Engine agnostic."""

from __future__ import annotations

from linpro.geometry.operators.intersection import intersection_point, intersects
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.segment import Segment


def segment_intersection(
    seg1: Segment,
    seg2: Segment,
) -> Point | None:
    """Calcula el punto de intersección entre dos segmentos (delegado a Geometry Engine)."""
    if not intersects(seg1, seg2):
        return None
    return intersection_point(seg1, seg2)
