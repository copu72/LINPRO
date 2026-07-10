"""Invalid coordinate exception."""

from linpro.geometry.exceptions.geometry_error import GeometryError


class InvalidCoordinateError(GeometryError, ValueError):
    """Raised when a coordinate is invalid.

    Reasons: NaN, infinity, wrong type, out of range.
    """
