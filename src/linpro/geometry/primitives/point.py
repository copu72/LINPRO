"""GEOM-004: Point — punto en el espacio 2D/3D.

Inmutable, hashable, serializable.
Es la primitiva fundamental del Geometry Engine de LINPRO.
"""

from __future__ import annotations

import json
import math

from linpro.geometry.exceptions import GeometryError
from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.kernel.validation import NumericValidator

_Coord = int | float
_Tuple3 = tuple[float, float, float]


class Point(Geometry):
    """Punto cartesiano inmutable en 2D/3D.

    Invariantes:
        - x, y, z son float
        - Ninguna coordenada es NaN o infinito
        - Igualdad usa EPSILON_GEOMETRY (1e-9)
        - Inmutable, hashable, serializable

    Example:
        >>> p = Point(10.0, 20.0)
        >>> p.distance_to(Point(13.0, 24.0))
        5.0
    """

    _EPSILON: float = EPSILON_GEOMETRY

    def __init__(self, x: _Coord, y: _Coord, z: _Coord = 0.0) -> None:
        NumericValidator.assert_finite(x, "x")
        NumericValidator.assert_finite(y, "y")
        NumericValidator.assert_finite(z, "z")
        self._x: float = float(x)
        self._y: float = float(y)
        self._z: float = float(z)

    # -- Propiedades --

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def z(self) -> float:
        return self._z

    @property
    def xy(self) -> tuple[float, float]:
        return (self._x, self._y)

    @property
    def dimension(self) -> int:
        return 2 if self._z == 0.0 else 3

    @property
    def is_empty(self) -> bool:
        return False

    @property
    def is_valid(self) -> bool:
        try:
            self.check_invariants()
            return True
        except Exception:
            return False

    @property
    def bbox(self) -> Geometry:
        from linpro.geometry.primitives.bbox import BoundingBox
        return BoundingBox(self._x, self._y, self._x, self._y)

    # -- Métodos de instancia --

    def distance_to(self, other: Point) -> float:
        dx = self._x - other._x
        dy = self._y - other._y
        dz = self._z - other._z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def almost_equal(self, other: object, tol: float = EPSILON_GEOMETRY) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (
            math.isclose(self._x, other._x, rel_tol=tol, abs_tol=tol)
            and math.isclose(self._y, other._y, rel_tol=tol, abs_tol=tol)
            and math.isclose(self._z, other._z, rel_tol=tol, abs_tol=tol)
        )

    def copy(self) -> Point:
        return Point(self._x, self._y, self._z)

    def check_invariants(self) -> None:
        NumericValidator.assert_finite(self._x, "x")
        NumericValidator.assert_finite(self._y, "y")
        NumericValidator.assert_finite(self._z, "z")

    # -- Serialización --

    def to_tuple(self) -> _Tuple3:
        return (self._x, self._y, self._z)

    def to_dict(self) -> dict[str, float]:
        return {"x": self._x, "y": self._y, "z": self._z}

    def to_wkt(self) -> str:
        return f"POINT ({self._x} {self._y})"

    # -- Deserialización --

    @classmethod
    def from_tuple(cls, data: tuple | list) -> Point:
        if not isinstance(data, (tuple, list)):
            raise GeometryError(f"Expected tuple or list, got {type(data).__name__}")
        if len(data) == 2:
            return cls(data[0], data[1])
        if len(data) == 3:
            return cls(data[0], data[1], data[2])
        raise GeometryError(f"Expected 2 or 3 elements, got {len(data)}")

    @classmethod
    def from_dict(cls, data: dict) -> Point:
        return cls(data["x"], data["y"], data.get("z", 0.0))

    @classmethod
    def from_json(cls, data: str) -> Point:
        return cls.from_dict(json.loads(data))

    # -- Métodos especiales --

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.almost_equal(other, self._EPSILON)

    def __hash__(self) -> int:
        return hash((round(self._x, 9), round(self._y, 9), round(self._z, 9)))

    def __repr__(self) -> str:
        return f"Point({self._x}, {self._y}, {self._z})"

    def __str__(self) -> str:
        return f"Point({self._x}, {self._y}, {self._z})"
