"""Geometry — clase base abstracta del Kernel Geometry.

Define el contrato que toda entidad geométrica debe cumplir.
Todas las clases del motor (Point, Vector, Segment, Polyline, ...)
heredan de Geometry e implementan estos métodos.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any


class Geometry(ABC):
    """Clase base abstracta para todas las entidades geométricas.

    Invariantes:
        - Toda subclase implementa dimension, is_empty, bbox, is_valid
        - to_dict y from_dict son inversos
        - La igualdad usa tolerancia (cada subclase define su _EPSILON)
        - Son inmutables (ninguna subclase permite mutación)

    Example:
        >>> from linpro.geometry import Point
        >>> p = Point(1.0, 2.0)
        >>> p.dimension
        2
    """

    _EPSILON: float = 1e-9

    # ---- Propiedades abstractas ----

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Dimensión geométrica (0 para Point, 1 para Curve, 2 para Surface)."""
        ...

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """True si la geometría no contiene puntos."""
        ...

    @property
    @abstractmethod
    def bbox(self) -> Geometry:
        """BoundingBox que envuelve la geometría."""
        ...

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        """True si la geometría cumple todos los invariantes."""
        ...

    # ---- Métodos abstractos ----

    @abstractmethod
    def copy(self) -> Geometry:
        """Copia independiente de la geometría."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serializa la geometría a diccionario."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Geometry:
        """Reconstruye la geometría desde un diccionario."""
        ...

    @abstractmethod
    def to_wkt(self) -> str:
        """Well-Known Text (OGC). 2D, sin Z."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...

    # ---- Métodos concretos ----

    def to_json(self, **kwargs) -> str:
        """Serializa a JSON.

        Args:
            **kwargs: Argumentos para json.dumps (indent, sort_keys, etc.)

        Returns:
            String JSON con la geometría serializada.
        """
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, data: str) -> Geometry:
        """Reconstruye desde JSON.

        Args:
            data: String JSON con la geometría serializada.

        Returns:
            Instancia de la geometría.
        """
        return cls.from_dict(json.loads(data))

    def __str__(self) -> str:
        return self.__repr__()
