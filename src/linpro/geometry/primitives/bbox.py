"""GEOM-005: BoundingBox — Caja delimitadora alineada a ejes."""

from __future__ import annotations

import math
from typing import List, Optional, Tuple


class BoundingBox:
    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float) -> None:
        self._xmin = float(xmin)
        self._ymin = float(ymin)
        self._xmax = float(xmax)
        self._ymax = float(ymax)

    @property
    def xmin(self) -> float:
        return self._xmin

    @property
    def ymin(self) -> float:
        return self._ymin

    @property
    def xmax(self) -> float:
        return self._xmax

    @property
    def ymax(self) -> float:
        return self._ymax

    @property
    def width(self) -> float:
        return self._xmax - self._xmin

    @property
    def height(self) -> float:
        return self._ymax - self._ymin

    @property
    def center(self) -> "Point":
        from linpro.geometry.primitives.point import Point
        return Point((self._xmin + self._xmax) / 2.0, (self._ymin + self._ymax) / 2.0)

    @property
    def area(self) -> float:
        return self.width * self.height

    def contains_point(self, point: "Point") -> bool:
        return self._xmin <= point.x <= self._xmax and self._ymin <= point.y <= self._ymax

    def contains_bbox(self, other: BoundingBox) -> bool:
        return (
            self._xmin <= other._xmin
            and self._xmax >= other._xmax
            and self._ymin <= other._ymin
            and self._ymax >= other._ymax
        )

    def intersects(self, other: BoundingBox) -> bool:
        return not (
            self._xmax < other._xmin
            or self._xmin > other._xmax
            or self._ymax < other._ymin
            or self._ymin > other._ymax
        )

    def union(self, other: BoundingBox) -> BoundingBox:
        return BoundingBox(
            min(self._xmin, other._xmin),
            min(self._ymin, other._ymin),
            max(self._xmax, other._xmax),
            max(self._ymax, other._ymax),
        )

    def intersection(self, other: BoundingBox) -> Optional[BoundingBox]:
        if not self.intersects(other):
            return None
        return BoundingBox(
            max(self._xmin, other._xmin),
            max(self._ymin, other._ymin),
            min(self._xmax, other._xmax),
            min(self._ymax, other._ymax),
        )

    def expanded(self, margin: float) -> BoundingBox:
        return BoundingBox(
            self._xmin - margin,
            self._ymin - margin,
            self._xmax + margin,
            self._ymax + margin,
        )

    @staticmethod
    def from_points(points: List["Point"]) -> BoundingBox:
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        return BoundingBox(min(xs), min(ys), max(xs), max(ys))

    @staticmethod
    def from_segments(segments: List["Segment"]) -> BoundingBox:
        from linpro.geometry.primitives.segment import Segment
        points: List = []
        for seg in segments:
            points.append(seg.start)
            points.append(seg.end)
        return BoundingBox.from_points(points)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoundingBox):
            return NotImplemented
        return (
            math.isclose(self._xmin, other._xmin)
            and math.isclose(self._ymin, other._ymin)
            and math.isclose(self._xmax, other._xmax)
            and math.isclose(self._ymax, other._ymax)
        )

    def __repr__(self) -> str:
        return f"BoundingBox({self._xmin:.3f}, {self._ymin:.3f}, {self._xmax:.3f}, {self._ymax:.3f})"