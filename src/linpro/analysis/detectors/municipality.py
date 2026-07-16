"""MunicipalityDetector — detección de municipios sobre el Engineering Axis.

Configura PolygonOverlayDetector para producir MunicipalityCrossing.
Toda la lógica espacial está en la clase padre.
"""

from __future__ import annotations

from typing import Any

from linpro.analysis.detectors.polygon_overlay import PolygonOverlayDetector
from linpro.analysis.models.crossing import MunicipalityCrossing
from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point


class MunicipalityDetector(PolygonOverlayDetector):
    """Detector de municipios que intersectan un Engineering Axis.

    Args:
        municipalities: Lista de municipios con su geometría.
            Cada elemento debe tener: "name", "province", "code", "polygon".
    """

    INCIDENT_PREFIX: str = "MUN"

    def __init__(
        self,
        municipalities: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(municipalities)

    def load_municipalities(self, municipalities: list[dict[str, Any]]) -> None:
        """Carga o reemplaza la lista de municipios a analizar."""
        self.load_features(municipalities)

    def _create_crossing(
        self,
        feature: dict[str, Any],
        pk_start: PK,
        pk_end: PK,
        point_start: Point,
        point_end: Point,
    ) -> MunicipalityCrossing:
        return MunicipalityCrossing(
            pk_start=pk_start,
            pk_end=pk_end,
            point_start=point_start,
            point_end=point_end,
            municipality=feature.get("name", "Unknown"),
            province=feature.get("province", ""),
            code=feature.get("code", ""),
        )

    def _group_key(self, crossing: MunicipalityCrossing) -> int:
        return hash(crossing.code)
