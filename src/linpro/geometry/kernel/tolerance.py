"""GEOM-002: Tolerance — tolerance-aware comparisons."""

from __future__ import annotations

import math

from linpro.geometry.kernel.constants import ANGLE_EPSILON, DISTANCE_EPSILON, EPSILON


class Tolerance:
    @staticmethod
    def almost_equal(a: float, b: float, tol: float = EPSILON) -> bool:
        return math.isclose(a, b, rel_tol=tol, abs_tol=tol)

    @staticmethod
    def almost_zero(a: float, tol: float = EPSILON) -> bool:
        return math.isclose(a, 0.0, rel_tol=tol, abs_tol=tol)

    @staticmethod
    def angle_almost_equal(a: float, b: float) -> bool:
        return Tolerance.almost_equal(a, b, ANGLE_EPSILON)

    @staticmethod
    def distance_almost_equal(a: float, b: float) -> bool:
        return Tolerance.almost_equal(a, b, DISTANCE_EPSILON)

    @staticmethod
    def less_or_equal(a: float, b: float, tol: float = EPSILON) -> bool:
        return a <= b + tol

    @staticmethod
    def greater_or_equal(a: float, b: float, tol: float = EPSILON) -> bool:
        return a >= b - tol

    @staticmethod
    def in_range(value: float, low: float, high: float, tol: float = EPSILON) -> bool:
        ge = Tolerance.greater_or_equal(value, low, tol)
        le = Tolerance.less_or_equal(value, high, tol)
        return ge and le
