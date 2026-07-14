"""GEOM-OPS-003: Parallelism.

is_parallel(a, b) → True if two vectors or segments are parallel.
"""

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.precision import is_close
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.vector import Vector


def is_parallel(a: Vector | Segment, b: Vector | Segment, tol: float = EPSILON_GEOMETRY) -> bool:
    if isinstance(a, Segment):
        vec_a = _segment_direction(a)
    else:
        vec_a = a
    if isinstance(b, Segment):
        vec_b = _segment_direction(b)
    else:
        vec_b = b
    cross_val = vec_a.cross(vec_b)
    if isinstance(cross_val, Vector):
        return cross_val.length_squared <= tol * tol
    return is_close(cross_val, 0.0, tol)


def _segment_direction(s: Segment) -> Vector:
    return Vector.from_points(s.start, s.end)
