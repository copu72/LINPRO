"""Precision error exception."""

from linpro.geometry.exceptions.geometry_error import GeometryError


class PrecisionError(GeometryError, ValueError):
    """Raised when a precision-related operation fails."""
