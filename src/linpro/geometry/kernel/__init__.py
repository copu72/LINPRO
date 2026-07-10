"""Kernel Mathematics of LINPRO.

Foundation layer of the Geometry Engine.
Defines global tolerances, precision, validation rules,
and base contracts for all geometric types.
"""

from linpro.geometry.kernel.constants import (
    ANGLE_EPSILON,
    DEFAULT_CRS,
    DEFAULT_PRECISION,
    DISTANCE_EPSILON,
    EPSILON_GEOMETRY,
    EPSILON_MATH,
    EPSILON_VISUAL,
    MAX_ITERATIONS,
    VERSION,
)
from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.kernel.tolerance import Tolerance, ToleranceLevel
from linpro.geometry.kernel.validation import (
    CoordinateValidator,
    GeometryValidator,
    NumericValidator,
)

__all__ = [
    "ANGLE_EPSILON",
    "DEFAULT_CRS",
    "DEFAULT_PRECISION",
    "DISTANCE_EPSILON",
    "EPSILON_GEOMETRY",
    "EPSILON_MATH",
    "EPSILON_VISUAL",
    "MAX_ITERATIONS",
    "VERSION",
    "Geometry",
    "Tolerance",
    "ToleranceLevel",
    "CoordinateValidator",
    "GeometryValidator",
    "NumericValidator",
]
