"""Validation — numeric, coordinate, and geometry validators."""

from __future__ import annotations

import math
from typing import Any

from linpro.geometry.exceptions.invalid_coordinate import InvalidCoordinateError
from linpro.geometry.exceptions.validation_error import ValidationError


class NumericValidator:
    """Validates numeric values: type, finiteness, range."""

    @staticmethod
    def assert_finite(value: Any, name: str = "value") -> None:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise InvalidCoordinateError(
                f"{name} must be numeric, got {type(value).__name__}"
            )
        if math.isnan(v):
            raise InvalidCoordinateError(f"{name} must not be NaN")
        if math.isinf(v):
            raise InvalidCoordinateError(f"{name} must not be infinite")

    @staticmethod
    def is_finite(value: Any) -> bool:
        try:
            v = float(value)
            return not (math.isnan(v) or math.isinf(v))
        except (TypeError, ValueError):
            return False

    @staticmethod
    def assert_positive(value: float, name: str = "value") -> None:
        NumericValidator.assert_finite(value, name)
        if value < 0:
            raise InvalidCoordinateError(f"{name} must be >= 0, got {value}")

    @staticmethod
    def assert_range(value: float, low: float, high: float, name: str = "value") -> None:
        NumericValidator.assert_finite(value, name)
        if value < low or value > high:
            raise InvalidCoordinateError(
                f"{name} must be in [{low}, {high}], got {value}"
            )


class CoordinateValidator:
    """Validates coordinate values (x, y, z)."""

    @staticmethod
    def assert_valid(x: Any, y: Any, z: Any | None = None) -> None:
        NumericValidator.assert_finite(x, "x")
        NumericValidator.assert_finite(y, "y")
        if z is not None:
            NumericValidator.assert_finite(z, "z")

    @staticmethod
    def assert_2d(x: Any, y: Any) -> None:
        NumericValidator.assert_finite(x, "x")
        NumericValidator.assert_finite(y, "y")

    @staticmethod
    def assert_3d(x: Any, y: Any, z: Any) -> None:
        NumericValidator.assert_finite(x, "x")
        NumericValidator.assert_finite(y, "y")
        NumericValidator.assert_finite(z, "z")


class GeometryValidator:
    """Validates geometry objects and their invariants."""

    @staticmethod
    def assert_type(value: Any, expected_type: type, name: str = "value") -> None:
        if not isinstance(value, expected_type):
            raise ValidationError(
                f"{name} must be of type {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )

    @staticmethod
    def assert_not_none(value: Any, name: str = "value") -> None:
        if value is None:
            raise ValidationError(f"{name} must not be None")

    @staticmethod
    def assert_valid_geometry(geometry: Any) -> None:
        from linpro.geometry.kernel.geometry import Geometry
        GeometryValidator.assert_type(geometry, Geometry, "geometry")
        if not geometry.is_valid:
            raise ValidationError("Geometry is not valid")
