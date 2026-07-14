"""GEOM-OPS-002: Collinearity.

is_collinear(a, b, c) → True if three points lie on the same line.
"""

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.operators.orientation import orientation
from linpro.geometry.primitives.point import Point


def is_collinear(a: Point, b: Point, c: Point, tol: float = EPSILON_GEOMETRY) -> bool:
    return orientation(a, b, c, tol) == 0.0
