"""GEOM-OPS-005: Distance.

distance(a, b) → minimum distance between two geometric entities.
Supports: Point-Point, Point-Segment, Segment-Segment, Point-BoundingBox.
"""

import math

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.operators.closest_point import closest_point
from linpro.geometry.primitives.bbox import BoundingBox
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.segment import Segment


def distance(a: Point | Segment | BoundingBox, b: Point | Segment | BoundingBox, tol: float = EPSILON_GEOMETRY) -> float:
    if isinstance(a, Point) and isinstance(b, Point):
        return _point_point(a, b)
    if isinstance(a, Point) and isinstance(b, Segment):
        return _point_segment(a, b)
    if isinstance(a, Segment) and isinstance(b, Point):
        return _point_segment(b, a)
    if isinstance(a, Segment) and isinstance(b, Segment):
        return _segment_segment(a, b)
    if isinstance(a, Point) and isinstance(b, BoundingBox):
        return _point_bbox(a, b)
    if isinstance(a, BoundingBox) and isinstance(b, Point):
        return _point_bbox(b, a)
    raise TypeError(f"distance() not supported for {type(a).__name__} and {type(b).__name__}")


def _point_point(a: Point, b: Point) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def _point_segment(p: Point, s: Segment) -> float:
    cp = closest_point(p, s)
    return _point_point(p, cp)


def _segment_segment(s1: Segment, s2: Segment) -> float:
    from linpro.geometry.operators.intersection import intersects
    if intersects(s1, s2):
        return 0.0
    d1 = _point_segment(s1.start, s2)
    d2 = _point_segment(s1.end, s2)
    d3 = _point_segment(s2.start, s1)
    d4 = _point_segment(s2.end, s1)
    return min(d1, d2, d3, d4)


def _point_bbox(p: Point, bb: BoundingBox) -> float:
    dx = max(bb.xmin - p.x, 0.0, p.x - bb.xmax)
    dy = max(bb.ymin - p.y, 0.0, p.y - bb.ymax)
    return math.sqrt(dx * dx + dy * dy)
