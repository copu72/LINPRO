"""GEOM-NNN: ClassName — breve descripción.

Descripción detallada de la clase.
Inmutable / mutable, hashable, serializable.
"""

from __future__ import annotations

import math
from typing import Any

from linpro.geometry.exceptions import GeometryError, ValidationError
from linpro.geometry.kernel.constants import EPSILON
from linpro.geometry.kernel.validation import Validation


class ClassName:
    """Breve descripción de la clase.

    Invariantes:
        - Invariante 1
        - Invariante 2

    Example:
        >>> obj = ClassName(...)
        >>> obj.some_method()
    """

    _EPSILON: float = EPSILON

    def __init__(self, param1: float, param2: float) -> None:
        Validation.assert_finite(param1, "param1")
        Validation.assert_finite(param2, "param2")
        self._param1: float = float(param1)
        self._param2: float = float(param2)

    @property
    def param1(self) -> float:
        return self._param1

    def some_method(self, other: Any) -> float:
        """Descripción breve.

        Args:
            other: Descripción.

        Returns:
            Descripción del retorno.

        Raises:
            GeometryError: Si ocurre algún error.
        """
        return 0.0

    def to_dict(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> ClassName:
        return cls(data["param1"], data["param2"])

    def to_wkt(self) -> str:
        return ""

    def almost_equal(self, other: object, tol: float = EPSILON) -> bool:
        if not isinstance(other, ClassName):
            return NotImplemented
        return False

    def check_invariants(self) -> None:
        Validation.assert_finite(self._param1, "param1")
        Validation.assert_finite(self._param2, "param2")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClassName):
            return NotImplemented
        return self.almost_equal(other, self._EPSILON)

    def __hash__(self) -> int:
        return hash(self._param1)

    def __repr__(self) -> str:
        return f"ClassName({self._param1})"

    def __str__(self) -> str:
        return f"ClassName({self._param1})"
