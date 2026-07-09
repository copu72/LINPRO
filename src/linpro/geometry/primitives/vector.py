"""GEOM-002: Vector — Vector en el plano 2D."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from linpro.geometry.primitives.point import Point


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def xy(self) -> Tuple[float, float]:
        return (self._x, self._y)

    @property
    def length(self) -> float:
        return math.sqrt(self._x * self._x + self._y * self._y)

    @property
    def angle(self) -> float:
        return math.atan2(self._y, self._x)

    @property
    def normalized(self) -> Vector:
        ln = self.length
        if ln == 0:
            return Vector(0.0, 0.0)
        return Vector(self._x / ln, self._y / ln)

    def dot(self, other: Vector) -> float:
        return self._x * other._x + self._y * other._y

    def cross(self, other: Vector) -> float:
        return self._x * other._y - self._y * other._x

    def angle_to(self, other: Vector) -> float:
        dot = self.dot(other)
        cross = self.cross(other)
        return math.atan2(cross, dot)

    def rotate(self, angle: float) -> Vector:
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector(self._x * cos_a - self._y * sin_a, self._x * sin_a + self._y * cos_a)

    def perpendicular(self) -> Vector:
        return Vector(-self._y, self._x)

    def __add__(self, other: Vector) -> Vector:
        return Vector(self._x + other._x, self._y + other._y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self._x - other._x, self._y - other._y)

    def __mul__(self, scalar: float) -> Vector:
        return Vector(self._x * scalar, self._y * scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self._x, other._x) and math.isclose(self._y, other._y)

    def __repr__(self) -> str:
        return f"Vector({self._x:.3f}, {self._y:.3f})"

    @staticmethod
    def from_points(p1: "Point", p2: "Point") -> "Vector":
        from linpro.geometry.primitives.point import Point
        return Vector(p2.x - p1.x, p2.y - p1.y)

    @staticmethod
    def from_angle(angle: float, length: float = 1.0) -> Vector:
        return Vector(math.cos(angle) * length, math.sin(angle) * length)