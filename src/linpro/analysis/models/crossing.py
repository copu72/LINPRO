"""Crossing — cruce de una entidad geográfica con el Engineering Axis.

Jerarquía de tipos de cruce.
Todo cruce tiene PK de entrada, PK de salida, y puntos asociados.
"""

from __future__ import annotations

from dataclasses import dataclass

from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point


@dataclass(frozen=True)
class Crossing:
    """Cruce base entre una entidad geográfica y el Engineering Axis.

    Attributes:
        pk_start: PK de entrada al término/entidad.
        pk_end: PK de salida del término/entidad.
        point_start: Punto geográfico de entrada.
        point_end: Punto geográfico de salida.
    """

    pk_start: PK
    pk_end: PK
    point_start: Point
    point_end: Point

    @property
    def length(self) -> float:
        return float(self.pk_end - self.pk_start)


@dataclass(frozen=True)
class MunicipalityCrossing(Crossing):
    """Cruce de un municipio con el Engineering Axis.

    Attributes:
        municipality: Nombre del municipio.
        province: Provincia del municipio.
        code: Código INE del municipio (5 dígitos).
    """

    municipality: str
    province: str
    code: str


@dataclass(frozen=True)
class RoadCrossing(Crossing):
    """Cruce de una carretera con el Engineering Axis.

    Attributes:
        road_id: Identificador de la carretera.
        road_name: Nombre de la carretera.
        road_type: Tipo de carretera (autovía, nacional, ...).
    """

    road_id: str
    road_name: str
    road_type: str
