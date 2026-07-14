"""GEOM-003: Segment — Segmento recto entre dos puntos."""

from __future__ import annotations

from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.vector import Vector


class Segment:
    def __init__(self, start: Point, end: Point) -> None:
        self._start = start
        self._end = end

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end

    @property
    def length(self) -> float:
        return self._start.distance_to(self._end)

    @property
    def midpoint(self) -> Point:
        return self._start.midpoint(self._end)

    @property
    def direction(self) -> Vector:
        return Vector.from_points(self._start, self._end).normalized

    @property
    def angle(self) -> float:
        return self.direction.angle

    def point_at(self, distance: float) -> Point:
        ratio = distance / self.length if self.length > 0 else 0.0
        ratio = max(0.0, min(1.0, ratio))
        return Point(
            self._start.x + (self._end.x - self._start.x) * ratio,
            self._start.y + (self._end.y - self._start.y) * ratio,
        )

    def distance_to_point(self, point: Point) -> tuple[float, float, float]:
        dx = self._end.x - self._start.x
        dy = self._end.y - self._start.y
        length_sq = dx * dx + dy * dy
        if length_sq == 0:
            dist = self._start.distance_to(point)
            return (dist, 0.0, 0.0)
        t = ((point.x - self._start.x) * dx + (point.y - self._start.y) * dy) / length_sq
        t = max(0.0, min(1.0, t))
        proj_x = self._start.x + t * dx
        proj_y = self._start.y + t * dy
        proj = Point(proj_x, proj_y)
        dist = proj.distance_to(point)
        return (dist, t, dist)

    def contains_point(self, point: Point, tolerance: float = 1e-9) -> bool:
        dist, t, _ = self.distance_to_point(point)
        return dist <= tolerance and 0.0 <= t <= 1.0

    def intersects(self, other: Segment) -> bool:
        return self.intersection(other) is not None

    def intersection(self, other: Segment) -> Point | None:
        x1, y1 = self._start.x, self._start.y
        x2, y2 = self._end.x, self._end.y
        x3, y3 = other._start.x, other._start.y
        x4, y4 = other._end.x, other._end.y
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-12:
            return None
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
            return Point(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Segment):
            return NotImplemented
        return self._start == other._start and self._end == other._end

    def __repr__(self) -> str:
        return f"Segment({self._start} -> {self._end})"
