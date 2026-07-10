"""Tolerance — precision levels for the Geometry Kernel.

Three tolerance levels for different contexts:
  - Tolerance.math      (1e-12) — internal arithmetic
  - Tolerance.geometry  (1e-9)  — entity comparisons (default)
  - Tolerance.visual    (1e-6)  — display / CAD snapping

Usage:
    Tolerance.geometry.equals(a, b)
    Tolerance.math.is_zero(v)
    Tolerance.visual.distance_equals(d1, d2)
"""

from __future__ import annotations

import math
from typing import ClassVar


class ToleranceLevel:
    """A tolerance level with its own epsilon and comparison methods."""

    def __init__(self, epsilon: float, angle_epsilon: float = 1e-10) -> None:
        self._epsilon = float(epsilon)
        self._angle_epsilon = float(angle_epsilon)

    @property
    def epsilon(self) -> float:
        return self._epsilon

    @property
    def angle_epsilon(self) -> float:
        return self._angle_epsilon

    def equals(self, a: float, b: float) -> bool:
        return math.isclose(a, b, rel_tol=self._epsilon, abs_tol=self._epsilon)

    def is_zero(self, v: float) -> bool:
        return math.isclose(v, 0.0, rel_tol=self._epsilon, abs_tol=self._epsilon)

    def distance_equals(self, d1: float, d2: float) -> bool:
        return self.equals(d1, d2)

    def angle_equals(self, a1: float, a2: float) -> bool:
        return math.isclose(a1, a2, rel_tol=self._angle_epsilon, abs_tol=self._angle_epsilon)

    def less_or_equal(self, a: float, b: float) -> bool:
        return a <= b + self._epsilon

    def greater_or_equal(self, a: float, b: float) -> bool:
        return a >= b - self._epsilon

    def in_range(self, value: float, low: float, high: float) -> bool:
        return self.greater_or_equal(value, low) and self.less_or_equal(value, high)

    def __repr__(self) -> str:
        return f"ToleranceLevel(ε={self._epsilon})"


class Tolerance:
    """Global tolerance registry with three precision levels.

    Each level (math, geometry, visual) is a ToleranceLevel instance
    with its own epsilon and comparison methods.
    """

    math: ClassVar[ToleranceLevel] = ToleranceLevel(1e-12, angle_epsilon=1e-12)
    geometry: ClassVar[ToleranceLevel] = ToleranceLevel(1e-9, angle_epsilon=1e-10)
    visual: ClassVar[ToleranceLevel] = ToleranceLevel(1e-6, angle_epsilon=1e-8)

    @classmethod
    def equals(cls, a: float, b: float) -> bool:
        return cls.geometry.equals(a, b)

    @classmethod
    def is_zero(cls, v: float) -> bool:
        return cls.geometry.is_zero(v)

    @classmethod
    def distance_equals(cls, d1: float, d2: float) -> bool:
        return cls.geometry.distance_equals(d1, d2)

    @classmethod
    def angle_equals(cls, a1: float, a2: float) -> bool:
        return cls.geometry.angle_equals(a1, a2)

    @classmethod
    def less_or_equal(cls, a: float, b: float) -> bool:
        return cls.geometry.less_or_equal(a, b)

    @classmethod
    def greater_or_equal(cls, a: float, b: float) -> bool:
        return cls.geometry.greater_or_equal(a, b)

    @classmethod
    def in_range(cls, value: float, low: float, high: float) -> bool:
        return cls.geometry.in_range(value, low, high)
