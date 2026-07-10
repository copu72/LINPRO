"""Base exception for all Geometry Engine errors."""


class GeometryError(Exception):
    """Base exception for the LINPRO Geometry Engine.

    All geometry-specific exceptions should inherit from this class
    to allow unified error handling.
    """
