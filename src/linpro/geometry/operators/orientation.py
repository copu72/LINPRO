"""GEOM-OPS-001: Orientation.

orientation(a, b, c) → sign of cross(b-a, c-a).
Positive = CCW, Negative = CW, Zero = collinear.
"""

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.precision import is_close
from linpro.geometry.primitives.point import Point


def orientation(a: Point, b: Point, c: Point, tol: float = EPSILON_GEOMETRY) -> float:
    cross_val = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    if is_close(cross_val, 0.0, tol):
        return 0.0
    return cross_val
