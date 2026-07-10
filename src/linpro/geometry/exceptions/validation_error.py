"""Validation error exception."""

from linpro.geometry.exceptions.geometry_error import GeometryError


class ValidationError(GeometryError, ValueError):
    """Raised when a geometric validation fails."""
