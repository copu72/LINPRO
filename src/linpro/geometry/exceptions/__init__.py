"""Custom exceptions for the LINPRO Geometry Engine.

Each exception lives in its own module for clean imports.
"""

from linpro.geometry.exceptions.geometry_error import GeometryError
from linpro.geometry.exceptions.invalid_coordinate import InvalidCoordinateError
from linpro.geometry.exceptions.precision_error import PrecisionError
from linpro.geometry.exceptions.validation_error import ValidationError

__all__ = [
    "GeometryError",
    "InvalidCoordinateError",
    "PrecisionError",
    "ValidationError",
]
