"""Kernel Mathematics of LINPRO.

Foundation layer of the Geometry Engine.
Defines global tolerances, precision, validation rules,
and base contracts for all geometric types.
"""

from linpro.geometry.kernel.constants import (
    ANGLE_EPSILON,
    DISTANCE_EPSILON,
    EPSILON,
    VISUAL_EPSILON,
)
from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.kernel.precision import Precision
from linpro.geometry.kernel.tolerance import Tolerance
from linpro.geometry.kernel.validation import Validation

__all__ = [
    "EPSILON",
    "ANGLE_EPSILON",
    "DISTANCE_EPSILON",
    "VISUAL_EPSILON",
    "Tolerance",
    "Precision",
    "Validation",
    "Geometry",
]
