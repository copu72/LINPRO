"""TASK-0005B: Segment — entidad de ingeniería entre dos puntos.

Inmutable, cachea vector (inmutable → seguro), delega algoritmos
en geometry/operators.
"""

from __future__ import annotations

import math
from functools import cached_property
from typing import Any

from linpro.geometry.exceptions import GeometryError
from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.primitives.bbox import BoundingBox
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.vector import Vector


class Segment(Geometry):
    _EPSILON: float = EPSILON_GEOMETRY

    def __init__(self, start: Point, end: Point) -> None:
        self._start: Point = start
        self._end: Point = end

    # -- Propiedades --

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end

    @cached_property
    def vector(self) -> Vector:
        return Vector.from_points(self._start, self._end)

    @property
    def length(self) -> float:
        return self.vector.length

    @property
    def length_squared(self) -> float:
        return self.vector.length_squared

    @property
    def bbox(self) -> Geometry:
        return BoundingBox(
            min(self._start.x, self._end.x),
            min(self._start.y, self._end.y),
            max(self._start.x, self._end.x),
            max(self._start.y, self._end.y),
        )

    @property
    def center(self) -> Point:
        return Point(
            (self._start.x + self._end.x) / 2.0,
            (self._start.y + self._end.y) / 2.0,
            (self._start.z + self._end.z) / 2.0,
        )

    @property
    def azimuth(self) -> float:
        return math.degrees(math.atan2(self.vector.dy, self.vector.dx))

    @property
    def dimension(self) -> int:
        return 1

    @property
    def is_zero_length(self) -> bool:
        return self.vector.is_zero

    @property
    def is_empty(self) -> bool:
        return self.is_zero_length

    @property
    def is_valid(self) -> bool:
        try:
            self.check_invariants()
            return True
        except Exception:
            return False

    # -- Métodos de instancia (delegan en operators) --

    def reverse(self) -> Segment:
        return Segment(self._end, self._start)

    def copy(self) -> Segment:
        return Segment(self._start.copy(), self._end.copy())

    def contains(self, point: Point, tol: float = EPSILON_GEOMETRY) -> bool:
        from linpro.geometry.operators.distance import distance
        return distance(point, self) <= tol

    def distance_to(self, other: object) -> float:
        from linpro.geometry.operators.distance import distance
        if isinstance(other, Point):
            return distance(self, other)
        if isinstance(other, Segment):
            return distance(self, other)
        raise TypeError(f"distance_to not supported for {type(other).__name__}")

    def project(self, point: Point) -> Point:
        from linpro.geometry.operators.projection import project
        return project(point, self)

    def closest_point(self, point: Point) -> Point:
        from linpro.geometry.operators.closest_point import closest_point
        return closest_point(point, self)

    def intersects(self, other: Segment, tol: float = EPSILON_GEOMETRY) -> bool:
        from linpro.geometry.operators.intersection import intersects
        return intersects(self, other, tol)

    def orientation(self, point: Point, tol: float = EPSILON_GEOMETRY) -> float:
        from linpro.geometry.operators.orientation import orientation
        return orientation(self._start, self._end, point, tol)

    def is_collinear(self, other: Segment, tol: float = EPSILON_GEOMETRY) -> bool:
        from linpro.geometry.operators.collinearity import is_collinear
        return is_collinear(self._start, self._end, other._start, tol)

    def check_invariants(self) -> None:
        if not isinstance(self._start, Point):
            raise GeometryError("start must be a Point")
        if not isinstance(self._end, Point):
            raise GeometryError("end must be a Point")

    # -- Serialización --

    def to_tuple(self) -> tuple[float, float, float, float, float, float]:
        return (
            self._start.x, self._start.y, self._start.z,
            self._end.x, self._end.y, self._end.z,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "start": self._start.to_dict(),
            "end": self._end.to_dict(),
        }

    def to_wkt(self) -> str:
        def _fmt(v: float) -> str:
            return str(v) if v != int(v) else str(int(v))
        return f"LINESTRING ({_fmt(self._start.x)} {_fmt(self._start.y)}, {_fmt(self._end.x)} {_fmt(self._end.y)})"

    @classmethod
    def from_tuple(cls, data: tuple | list) -> Segment:
        if len(data) == 6:
            return cls(Point(data[0], data[1], data[2]), Point(data[3], data[4], data[5]))
        if len(data) == 4:
            return cls(Point(data[0], data[1]), Point(data[2], data[3]))
        raise GeometryError(f"Expected 4 or 6 elements, got {len(data)}")

    @classmethod
    def from_dict(cls, data: dict) -> Segment:
        return cls(Point.from_dict(data["start"]), Point.from_dict(data["end"]))

    # -- Especiales --

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Segment):
            return NotImplemented
        return self._start == other._start and self._end == other._end

    def __hash__(self) -> int:
        return hash((self._start, self._end))

    def __repr__(self) -> str:
        return f"Segment({self._start} → {self._end})"

    def __str__(self) -> str:
        return self.__repr__()
