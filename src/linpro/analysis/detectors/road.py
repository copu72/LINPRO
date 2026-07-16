"""RoadDetector — detección de carreteras sobre el Engineering Axis.

Configura LinearCrossingDetector para producir RoadCrossing.
Toda la lógica espacial está en la clase padre.
"""

from __future__ import annotations

from typing import Any

from linpro.analysis.detectors.linear_crossing import LinearCrossingDetector
from linpro.analysis.models.crossing import RoadCrossing
from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point


class RoadDetector(LinearCrossingDetector):
    """Detector de carreteras que intersectan un Engineering Axis.

    Args:
        roads: Lista de carreteras con su geometría.
            Cada elemento debe tener: "id", "name", "type", "polyline".
    """

    INCIDENT_PREFIX: str = "ROD"

    def __init__(
        self,
        roads: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(roads)

    def load_roads(self, roads: list[dict[str, Any]]) -> None:
        """Carga o reemplaza la lista de carreteras a analizar."""
        self.load_features(roads)

    def _create_crossing(
        self,
        feature: dict[str, Any],
        pk: PK,
        point: Point,
    ) -> RoadCrossing:
        return RoadCrossing(
            pk_start=pk,
            pk_end=pk,
            point_start=point,
            point_end=point,
            road_id=feature.get("id", ""),
            road_name=feature.get("name", "Unknown"),
            road_type=feature.get("type", ""),
        )
