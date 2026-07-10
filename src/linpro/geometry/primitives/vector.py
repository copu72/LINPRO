"""GEOM-VEC: Vector — desplazamiento en el espacio 2D/3D.

Inmutable, serializable, con álgebra completa.
No tiene posición (a diferencia de Point).
"""

from __future__ import annotations

import math
from typing import Any

from linpro.geometry.exceptions import GeometryError, PrecisionError
from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.kernel.validation import NumericValidator

_Coord = int | float
_Tuple2 = tuple[float, float]
_Tuple3 = tuple[float, float, float]


class Vector(Geometry):
    """Vector de desplazamiento inmutable en 2D/3D.

    A diferencia de Point, Vector no tiene posición. Solo magnitud,
    dirección y sentido.

    Invariantes:
        - dx, dy, dz son float finitos
        - Igualdad usa EPSILON_GEOMETRY (1e-9)
        - Inmutable, hashable, serializable

    Example:
        >>> v = Vector(3.0, 4.0)
        >>> v.length
        5.0
    """

    _EPSILON: float = EPSILON_GEOMETRY

    def __init__(self, dx: _Coord, dy: _Coord, dz: _Coord = 0.0) -> None:
        NumericValidator.assert_finite(dx, "dx")
        NumericValidator.assert_finite(dy, "dy")
        NumericValidator.assert_finite(dz, "dz")
        self._dx: float = float(dx)
        self._dy: float = float(dy)
        self._dz: float = float(dz)

    # -- Propiedades --

    @property
    def dx(self) -> float:
        return self._dx

    @property
    def dy(self) -> float:
        return self._dy

    @property
    def dz(self) -> float:
        return self._dz

    @property
    def dimension(self) -> int:
        return 2 if self._dz == 0.0 else 3

    @property
    def is_empty(self) -> bool:
        return self.is_zero

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
        return BoundingBox(0.0, 0.0, self._dx, self._dy)

    @property
    def length(self) -> float:
        return math.hypot(self._dx, self._dy, self._dz)

    @property
    def length_squared(self) -> float:
        return self._dx * self._dx + self._dy * self._dy + self._dz * self._dz

    @property
    def angle(self) -> float:
        return math.atan2(self._dy, self._dx)

    @property
    def normalized(self) -> Vector:
        ln = self.length
        if ln <= self._EPSILON:
            raise PrecisionError("Cannot normalize a zero-length vector")
        return Vector(self._dx / ln, self._dy / ln, self._dz / ln)

    @property
    def is_zero(self) -> bool:
        return (
            abs(self._dx) <= self._EPSILON
            and abs(self._dy) <= self._EPSILON
            and abs(self._dz) <= self._EPSILON
        )

    @property
    def is_unit(self) -> bool:
        return abs(self.length - 1.0) <= self._EPSILON

    @property
    def perpendicular(self) -> Vector:
        return Vector(-self._dy, self._dx)

    # -- Métodos de álgebra --

    def dot(self, other: Vector) -> float:
        return (
            self._dx * other._dx
            + self._dy * other._dy
            + self._dz * other._dz
        )

    def cross(self, other: Vector) -> float | Vector:
        if self._dz == 0.0 and other._dz == 0.0:
            return self._dx * other._dy - self._dy * other._dx
        return Vector(
            self._dy * other._dz - self._dz * other._dy,
            self._dz * other._dx - self._dx * other._dz,
            self._dx * other._dy - self._dy * other._dx,
        )

    def angle_to(self, other: Vector) -> float:
        dot_val = self.dot(other)
        cos_angle = dot_val / (self.length * other.length)
        cos_angle = max(-1.0, min(1.0, cos_angle))
        return math.acos(cos_angle)

    def signed_angle_to(self, other: Vector) -> float:
        return math.atan2(self.cross(other), self.dot(other))

    def rotate(self, angle: float) -> Vector:
        NumericValidator.assert_finite(angle, "angle")
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector(
            self._dx * cos_a - self._dy * sin_a,
            self._dx * sin_a + self._dy * cos_a,
            self._dz,
        )

    def project_onto(self, other: Vector) -> Vector:
        denom = other.length_squared
        if denom <= self._EPSILON:
            return Vector(0.0, 0.0, 0.0)
        scalar = self.dot(other) / denom
        return other * scalar

    def reject_from(self, other: Vector) -> Vector:
        return self - self.project_onto(other)

    def lerp(self, other: Vector, t: float) -> Vector:
        NumericValidator.assert_finite(t, "t")
        return self + (other - self) * t

    def almost_equal(self, other: object, tol: float = EPSILON_GEOMETRY) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return (
            math.isclose(self._dx, other._dx, rel_tol=tol, abs_tol=tol)
            and math.isclose(self._dy, other._dy, rel_tol=tol, abs_tol=tol)
            and math.isclose(self._dz, other._dz, rel_tol=tol, abs_tol=tol)
        )

    def is_parallel(self, other: Vector, tol: float = EPSILON_GEOMETRY) -> bool:
        cross_val = self.cross(other)
        if isinstance(cross_val, Vector):
            return cross_val.length_squared <= tol * tol
        return abs(cross_val) <= tol

    def is_perpendicular(self, other: Vector, tol: float = EPSILON_GEOMETRY) -> bool:
        return abs(self.dot(other)) <= tol

    # -- Geometry contract --

    def copy(self) -> Vector:
        return Vector(self._dx, self._dy, self._dz)

    def check_invariants(self) -> None:
        NumericValidator.assert_finite(self._dx, "dx")
        NumericValidator.assert_finite(self._dy, "dy")
        NumericValidator.assert_finite(self._dz, "dz")

    # -- Serialización --

    def to_tuple(self) -> _Tuple3:
        return (self._dx, self._dy, self._dz)

    def to_dict(self) -> dict[str, Any]:
        return {"dx": self._dx, "dy": self._dy, "dz": self._dz}

    def to_wkt(self) -> str:
        raise GeometryError("Vector has no WKT representation")

    @classmethod
    def from_tuple(cls, data: tuple | list) -> Vector:
        if not isinstance(data, (tuple, list)):
            raise GeometryError(f"Expected tuple or list, got {type(data).__name__}")
        if len(data) == 2:
            return cls(data[0], data[1])
        if len(data) == 3:
            return cls(data[0], data[1], data[2])
        raise GeometryError(f"Expected 2 or 3 elements, got {len(data)}")

    @classmethod
    def from_dict(cls, data: dict) -> Vector:
        return cls(data["dx"], data["dy"], data.get("dz", 0.0))

    @classmethod
    def from_points(cls, p1: Geometry, p2: Geometry) -> Vector:
        return cls(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

    @classmethod
    def from_angle(cls, angle: float, length: float = 1.0) -> Vector:
        NumericValidator.assert_finite(angle, "angle")
        NumericValidator.assert_positive(length, "length")
        return cls(math.cos(angle) * length, math.sin(angle) * length)

    # -- Operadores --

    def __add__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self._dx + other._dx, self._dy + other._dy, self._dz + other._dz)

    def __sub__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self._dx - other._dx, self._dy - other._dy, self._dz - other._dz)

    def __mul__(self, scalar: _Coord) -> Vector:
        NumericValidator.assert_finite(scalar, "scalar")
        return Vector(self._dx * scalar, self._dy * scalar, self._dz * scalar)

    def __rmul__(self, scalar: _Coord) -> Vector:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: _Coord) -> Vector:
        NumericValidator.assert_finite(scalar, "scalar")
        if abs(scalar) <= self._EPSILON:
            raise PrecisionError("Division by zero in Vector")
        return Vector(self._dx / scalar, self._dy / scalar, self._dz / scalar)

    def __neg__(self) -> Vector:
        return Vector(-self._dx, -self._dy, -self._dz)

    def __pos__(self) -> Vector:
        return self.copy()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.almost_equal(other, self._EPSILON)

    def __hash__(self) -> int:
        return hash((
            round(self._dx, 9), round(self._dy, 9), round(self._dz, 9),
        ))

    def __repr__(self) -> str:
        return f"Vector({self._dx:.3f}, {self._dy:.3f}, {self._dz:.3f})"

    def __str__(self) -> str:
        return f"Vector({self._dx:.3f}, {self._dy:.3f}, {self._dz:.3f})"
