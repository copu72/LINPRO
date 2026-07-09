"""GEOM-004: Validation — coordinate and geometry validation."""

from __future__ import annotations

import math
from typing import Any

from linpro.geometry.exceptions import InvalidCoordinateError


class Validation:
    @staticmethod
    def assert_finite(value: Any, name: str = "value") -> None:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise InvalidCoordinateError(f"{name} must be numeric, got {type(value).__name__}")
        if math.isnan(v):
            raise InvalidCoordinateError(f"{name} must not be NaN")
        if math.isinf(v):
            raise InvalidCoordinateError(f"{name} must not be infinite")

    @staticmethod
    def assert_finite_coordinate(x: Any, y: Any, z: Any | None = None) -> None:
        Validation.assert_finite(x, "x")
        Validation.assert_finite(y, "y")
        if z is not None:
            Validation.assert_finite(z, "z")

    @staticmethod
    def assert_type(value: Any, expected_type: type, name: str = "value") -> None:
        if not isinstance(value, expected_type):
            raise InvalidCoordinateError(
                f"{name} must be of type {expected_type.__name__}, got {type(value).__name__}"
            )
