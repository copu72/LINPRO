"""GEOM-OPS-007: Closest Point.

closest_point(point, segment) → point on segment closest to the given point.
Clamps projection to [0, 1] range.
"""

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.vector import Vector


def closest_point(p: Point, s: Segment, tol: float = EPSILON_GEOMETRY) -> Point:
    vec_s = Vector.from_points(s.start, s.end)
    len2 = vec_s.length_squared
    if len2 <= tol * tol:
        return s.start
    t = Vector.from_points(s.start, p).dot(vec_s) / len2
    t = max(0.0, min(1.0, t))
    return Point(
        s.start.x + t * vec_s.dx,
        s.start.y + t * vec_s.dy,
        s.start.z + t * vec_s.dz,
    )
