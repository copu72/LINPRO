"""GEOM-001: Point.

Punto en el plano cartesiano 2D con coordenadas (x, y).
Es la primitiva fundamental de todo el Geometry Engine.
"""

from __future__ import annotations

import math
from typing import Tuple


class Point:
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

    def distance_to(self, other: Point) -> float:
        dx = self._x - other._x
        dy = self._y - other._y
        return math.sqrt(dx * dx + dy * dy)

    def midpoint(self, other: Point) -> Point:
        return Point((self._x + other._x) / 2.0, (self._y + other._y) / 2.0)

    def translate(self, dx: float, dy: float) -> Point:
        return Point(self._x + dx, self._y + dy)

    def rotate(self, angle: float, center: Point | None = None) -> Point:
        cx = center._x if center else 0.0
        cy = center._y if center else 0.0
        rx = self._x - cx
        ry = self._y - cy
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Point(cx + rx * cos_a - ry * sin_a, cy + rx * sin_a + ry * cos_a)

    def scale(self, factor: float, center: Point | None = None) -> Point:
        cx = center._x if center else 0.0
        cy = center._y if center else 0.0
        return Point(cx + (self._x - cx) * factor, cy + (self._y - cy) * factor)

    def normalize(self) -> Point:
        d = math.sqrt(self._x * self._x + self._y * self._y)
        if d == 0:
            return Point(0.0, 0.0)
        return Point(self._x / d, self._y / d)

    def dot(self, other: Point) -> float:
        return self._x * other._x + self._y * other._y

    def cross(self, other: Point) -> float:
        return self._x * other._y - self._y * other._x

    def __add__(self, other: Point) -> Point:
        return Point(self._x + other._x, self._y + other._y)

    def __sub__(self, other: Point) -> Point:
        return Point(self._x - other._x, self._y - other._y)

    def __mul__(self, scalar: float) -> Point:
        return Point(self._x * scalar, self._y * scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return math.isclose(self._x, other._x) and math.isclose(self._y, other._y)

    def __hash__(self) -> int:
        return hash((round(self._x, 9), round(self._y, 9)))

    def __repr__(self) -> str:
        return f"Point({self._x:.3f}, {self._y:.3f})"