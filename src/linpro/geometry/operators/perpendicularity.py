"""GEOM-OPS-004: Perpendicularity.

is_perpendicular(a, b) → True if two vectors or segments are perpendicular.
"""

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.precision import is_close
from linpro.geometry.operators.parallelism import _segment_direction
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.vector import Vector


def is_perpendicular(a: Vector | Segment, b: Vector | Segment, tol: float = EPSILON_GEOMETRY) -> bool:
    if isinstance(a, Segment):
        vec_a = _segment_direction(a)
    else:
        vec_a = a
    if isinstance(b, Segment):
        vec_b = _segment_direction(b)
    else:
        vec_b = b
    return is_close(vec_a.dot(vec_b), 0.0, tol)
