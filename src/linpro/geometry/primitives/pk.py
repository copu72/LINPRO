"""PK — Progressiva Quilométrica (Station value object).

Value Object inmutable que representa un punto kilométrico
a lo largo de un eje lineal.

Prepara el terreno para Station, PK y Measure como VO.
Por ahora: wrapper de float con operaciones aritméticas y comparación.

Example:
    >>> pk = PK(1250.34)
    >>> float(pk)
    1250.34
    >>> PK(100.0) + PK(50.0)
    PK(150.0)
"""

from __future__ import annotations

from linpro.geometry.kernel.constants import EPSILON_GEOMETRY


class PK:
    """Progresiva Quilométrica (station value object).

    Inmutable, compatible con float, preparado para extensión
    futura a Station y Measure.
    """

    def __init__(self, value: int | float) -> None:
        self._value: float = float(value)

    @property
    def value(self) -> float:
        return self._value

    # -- Conversión --

    def __float__(self) -> float:
        return self._value

    def __int__(self) -> int:
        return int(self._value)

    # -- Comparación --

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PK):
            return abs(self._value - other._value) <= EPSILON_GEOMETRY
        if isinstance(other, (int, float)):
            return abs(self._value - float(other)) <= EPSILON_GEOMETRY
        return NotImplemented

    def __lt__(self, other: PK | int | float) -> bool:
        if isinstance(other, PK):
            return self._value < other._value
        if isinstance(other, (int, float)):
            return self._value < float(other)
        return NotImplemented

    def __le__(self, other: PK | int | float) -> bool:
        if isinstance(other, PK):
            return self._value <= other._value + EPSILON_GEOMETRY
        if isinstance(other, (int, float)):
            return self._value <= float(other) + EPSILON_GEOMETRY
        return NotImplemented

    def __gt__(self, other: PK | int | float) -> bool:
        if isinstance(other, PK):
            return self._value > other._value
        if isinstance(other, (int, float)):
            return self._value > float(other)
        return NotImplemented

    def __ge__(self, other: PK | int | float) -> bool:
        if isinstance(other, PK):
            return self._value >= other._value - EPSILON_GEOMETRY
        if isinstance(other, (int, float)):
            return self._value >= float(other) - EPSILON_GEOMETRY
        return NotImplemented

    def __hash__(self) -> int:
        return hash((round(self._value, 9),))

    # -- Aritmética --

    def __add__(self, other: PK | int | float) -> PK:
        if isinstance(other, PK):
            return PK(self._value + other._value)
        if isinstance(other, (int, float)):
            return PK(self._value + float(other))
        return NotImplemented

    def __radd__(self, other: PK | int | float) -> PK:
        return self.__add__(other)

    def __sub__(self, other: PK | int | float) -> PK:
        if isinstance(other, PK):
            return PK(self._value - other._value)
        if isinstance(other, (int, float)):
            return PK(self._value - float(other))
        return NotImplemented

    def __rsub__(self, other: PK | int | float) -> PK:
        if isinstance(other, (int, float)):
            return PK(float(other) - self._value)
        return NotImplemented

    def __mul__(self, other: int | float) -> PK:
        if isinstance(other, (int, float)):
            return PK(self._value * float(other))
        return NotImplemented

    def __rmul__(self, other: int | float) -> PK:
        return self.__mul__(other)

    def __truediv__(self, other: int | float) -> PK:
        if isinstance(other, (int, float)):
            return PK(self._value / float(other))
        return NotImplemented

    def __neg__(self) -> PK:
        return PK(-self._value)

    def __pos__(self) -> PK:
        return PK(self._value)

    def __abs__(self) -> float:
        return abs(self._value)

    # -- Representación --

    def __repr__(self) -> str:
        return f"PK({self._value})"

    def __str__(self) -> str:
        return f"PK({self._value:.3f})"
