"""GEOM-OPS-006: Projection.

project(point, segment) → orthogonal projection of point onto the infinite line of segment.
Does NOT clamp to segment (use closest_point for that).
"""

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.vector import Vector


def project(p: Point, s: Segment, tol: float = EPSILON_GEOMETRY) -> Point:
    vec_s = Vector.from_points(s.start, s.end)
    len2 = vec_s.length_squared
    if len2 <= tol * tol:
        return s.start
    t = Vector.from_points(s.start, p).dot(vec_s) / len2
    return Point(
        s.start.x + t * vec_s.dx,
        s.start.y + t * vec_s.dy,
        s.start.z + t * vec_s.dz,
    )
