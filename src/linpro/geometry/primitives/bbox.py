"""GEOM-BBOX: BoundingBox — caja delimitadora alineada a ejes (AABB).

Inmutable, hashable, serializable.
Entidad de primer nivel del Geometry Engine.
"""

from __future__ import annotations

import math
from typing import Any

from linpro.geometry.exceptions import GeometryError
from linpro.geometry.exceptions.validation_error import ValidationError
from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.kernel.validation import NumericValidator

_Coord = int | float
_Tuple4 = tuple[float, float, float, float]


class BoundingBox(Geometry):
    """Caja delimitadora alineada a ejes (AABB) en 2D.

    Invariantes:
        - xmin, ymin, xmax, ymax son float finitos
        - xmin <= xmax, ymin <= ymax
        - Igualdad usa EPSILON_GEOMETRY (1e-9)
        - Inmutable, hashable, serializable

    Example:
        >>> from linpro.geometry import BoundingBox
        >>> bb = BoundingBox(10.0, 20.0, 30.0, 40.0)
        >>> bb.width
        20.0
    """

    _EPSILON: float = EPSILON_GEOMETRY

    def __init__(self, xmin: _Coord, ymin: _Coord, xmax: _Coord, ymax: _Coord) -> None:
        NumericValidator.assert_finite(xmin, "xmin")
        NumericValidator.assert_finite(ymin, "ymin")
        NumericValidator.assert_finite(xmax, "xmax")
        NumericValidator.assert_finite(ymax, "ymax")
        self._xmin: float = float(xmin)
        self._ymin: float = float(ymin)
        self._xmax: float = float(xmax)
        self._ymax: float = float(ymax)

    # -- Propiedades --

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
    def area(self) -> float:
        return self.width * self.height

    @property
    def dimension(self) -> int:
        return 2

    @property
    def is_empty(self) -> bool:
        return self.width <= 0.0 or self.height <= 0.0

    @property
    def is_valid(self) -> bool:
        try:
            self.check_invariants()
            return True
        except Exception:
            return False

    @property
    def bbox(self) -> Geometry:
        return self

    # -- Operaciones geométricas --

    @property
    def center(self) -> Geometry:
        from linpro.geometry.primitives.point import Point
        return Point(
            (self._xmin + self._xmax) / 2.0,
            (self._ymin + self._ymax) / 2.0,
        )

    def contains_point(self, point: Geometry) -> bool:
        return (
            self._xmin <= point.x <= self._xmax
            and self._ymin <= point.y <= self._ymax
        )

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

    def intersection(self, other: BoundingBox) -> BoundingBox | None:
        if not self.intersects(other):
            return None
        xmin = max(self._xmin, other._xmin)
        ymin = max(self._ymin, other._ymin)
        xmax = min(self._xmax, other._xmax)
        ymax = min(self._ymax, other._ymax)
        if xmin >= xmax and ymin >= ymax:
            return None
        return BoundingBox(xmin, ymin, xmax, ymax)

    def expand(self, margin: float) -> BoundingBox:
        NumericValidator.assert_finite(margin, "margin")
        return BoundingBox(
            self._xmin - margin,
            self._ymin - margin,
            self._xmax + margin,
            self._ymax + margin,
        )

    # -- Geometry contract --

    def almost_equal(self, other: object, tol: float = EPSILON_GEOMETRY) -> bool:
        if not isinstance(other, BoundingBox):
            return NotImplemented
        return (
            math.isclose(self._xmin, other._xmin, rel_tol=tol, abs_tol=tol)
            and math.isclose(self._ymin, other._ymin, rel_tol=tol, abs_tol=tol)
            and math.isclose(self._xmax, other._xmax, rel_tol=tol, abs_tol=tol)
            and math.isclose(self._ymax, other._ymax, rel_tol=tol, abs_tol=tol)
        )

    def copy(self) -> BoundingBox:
        return BoundingBox(self._xmin, self._ymin, self._xmax, self._ymax)

    def check_invariants(self) -> None:
        NumericValidator.assert_finite(self._xmin, "xmin")
        NumericValidator.assert_finite(self._ymin, "ymin")
        NumericValidator.assert_finite(self._xmax, "xmax")
        NumericValidator.assert_finite(self._ymax, "ymax")
        if self._xmin > self._xmax:
            raise ValidationError(
                f"xmin ({self._xmin}) must be <= xmax ({self._xmax})"
            )
        if self._ymin > self._ymax:
            raise ValidationError(
                f"ymin ({self._ymin}) must be <= ymax ({self._ymax})"
            )

    # -- Serialización --

    def to_tuple(self) -> _Tuple4:
        return (self._xmin, self._ymin, self._xmax, self._ymax)

    def to_dict(self) -> dict[str, Any]:
        return {
            "xmin": self._xmin,
            "ymin": self._ymin,
            "xmax": self._xmax,
            "ymax": self._ymax,
        }

    def to_wkt(self) -> str:
        return (
            f"POLYGON (({self._xmin} {self._ymin}, "
            f"{self._xmax} {self._ymin}, "
            f"{self._xmax} {self._ymax}, "
            f"{self._xmin} {self._ymax}, "
            f"{self._xmin} {self._ymin}))"
        )

    # -- Deserialización --

    @classmethod
    def from_tuple(cls, data: tuple | list) -> BoundingBox:
        if not isinstance(data, (tuple, list)):
            raise GeometryError(f"Expected tuple or list, got {type(data).__name__}")
        if len(data) != 4:
            raise GeometryError(f"Expected 4 elements, got {len(data)}")
        return cls(data[0], data[1], data[2], data[3])

    @classmethod
    def from_dict(cls, data: dict) -> BoundingBox:
        return cls(data["xmin"], data["ymin"], data["xmax"], data["ymax"])

    # -- Constructores adicionales --

    @classmethod
    def from_points(cls, points: list) -> BoundingBox:
        if not points:
            raise ValidationError("Cannot create BoundingBox from empty list")
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        return cls(min(xs), min(ys), max(xs), max(ys))

    @classmethod
    def empty(cls) -> BoundingBox:
        return cls(0.0, 0.0, 0.0, 0.0)

    # -- Métodos especiales --

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoundingBox):
            return NotImplemented
        return self.almost_equal(other, self._EPSILON)

    def __hash__(self) -> int:
        return hash((
            round(self._xmin, 9),
            round(self._ymin, 9),
            round(self._xmax, 9),
            round(self._ymax, 9),
        ))

    def __repr__(self) -> str:
        return (
            f"BoundingBox({self._xmin:.3f}, {self._ymin:.3f}, "
            f"{self._xmax:.3f}, {self._ymax:.3f})"
        )

    def __str__(self) -> str:
        return self.__repr__()
