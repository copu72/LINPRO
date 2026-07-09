"""GEOM-001: Geometry — base class for all geometric types."""

from __future__ import annotations

from typing import ClassVar


class Geometry:
    """Base class for all geometric entities in LINPRO.

    Provides:
      - tolerance-aware equality
      - serialisation contracts
      - invariant checking
    """

    _EPSILON: ClassVar[float] = 1e-9

    def almost_equal(self, other: object, tol: float | None = None) -> bool:
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict) -> Geometry:
        raise NotImplementedError

    def to_wkt(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def check_invariants(self) -> None:
        raise NotImplementedError
