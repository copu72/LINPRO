"""Custom exceptions for the LINPRO Geometry Engine."""


class GeometryError(Exception):
    """Base exception for all geometry engine errors."""


class InvalidCoordinateError(GeometryError, ValueError):
    """Raised when a coordinate value is invalid (NaN, inf, wrong type)."""


class PrecisionError(GeometryError, ValueError):
    """Raised when a precision-related operation fails."""


class ValidationError(GeometryError, ValueError):
    """Raised when a geometric validation fails."""
