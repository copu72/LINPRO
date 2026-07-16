"""LinearCrossingDetector — detector genérico de cruce lineal.

Todo detector que analice intersecciones de entidades lineales
(carreteras, ríos, ferrocarriles, tuberías) sobre el Engineering
Axis hereda de aquí. Sin lógica espacial duplicada.
"""

from __future__ import annotations

import time
from abc import abstractmethod
from typing import Any

from linpro.analysis.detectors._helpers import segment_intersection
from linpro.analysis.detectors.base import Detector
from linpro.analysis.models.analysis_result import AnalysisMetadata, AnalysisResult
from linpro.analysis.models.crossing import Crossing
from linpro.analysis.models.incident import Incident, IncidentSeverity
from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.polyline import Polyline


class LinearCrossingDetector(Detector):
    """Detector genérico de cruce lineal.

    Subclases solo implementan _create_crossing() para definir
    el modelo de salida.

    Args:
        features: Lista de features con clave "polyline" (Polyline).
    """

    INCIDENT_PREFIX: str = "LCD"

    def __init__(
        self,
        features: list[dict[str, Any]] | None = None,
    ) -> None:
        self._features: list[dict[str, Any]] = features or []

    def load_features(self, features: list[dict[str, Any]]) -> None:
        """Carga o reemplaza la lista de features a analizar."""
        self._features = list(features)

    @property
    def detector_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def _create_crossing(
        self,
        feature: dict[str, Any],
        pk: PK,
        point: Point,
    ) -> Crossing:
        """Crea el cruce tipado para la subclase concreta.

        Los cruces lineales son puntuales (pk_start == pk_end).
        """

    def analyze(self, axis: Polyline) -> AnalysisResult:
        t0 = time.perf_counter()

        crossings: list[Crossing] = []
        incidents: list[Incident] = []

        if not self._features:
            incidents.append(Incident(
                severity=IncidentSeverity.ERROR,
                code=f"{self.INCIDENT_PREFIX}-001",
                message="No features loaded. Call load_features() first.",
            ))
            result = AnalysisResult(
                axis=axis,
                crossings=[],
                incidents=incidents,
                metadata=AnalysisMetadata(
                    detector_name=self.detector_name,
                    axis_length=axis.length,
                    entity_count=0,
                ),
            )
            result.metadata.duration_ms = (time.perf_counter() - t0) * 1000
            return result

        axis_bbox = axis.bbox

        for feat in self._features:
            try:
                name = feat.get("name", "Unknown")

                if "polyline" not in feat:
                    incidents.append(Incident(
                        severity=IncidentSeverity.WARNING,
                        code=f"{self.INCIDENT_PREFIX}-002",
                        message=f"Feature '{name}' has no polyline geometry",
                    ))
                    continue

                line: Polyline = feat["polyline"]

                if not line.bbox.intersects(axis_bbox):
                    continue

                feat_crossings = self._intersect_line_with_axis(
                    line, axis, feat,
                )
                crossings.extend(feat_crossings)

                if not feat_crossings:
                    incidents.append(Incident(
                        severity=IncidentSeverity.INFO,
                        code=f"{self.INCIDENT_PREFIX}-003",
                        message=f"Feature '{name}' bbox overlaps but no crossing found",
                    ))

            except Exception as exc:
                incidents.append(Incident(
                    severity=IncidentSeverity.ERROR,
                    code=f"{self.INCIDENT_PREFIX}-099",
                    message=f"Error processing feature '{feat.get('name', '?')}': {exc}",
                ))

        t1 = time.perf_counter()
        metadata = AnalysisMetadata(
            detector_name=self.detector_name,
            duration_ms=(t1 - t0) * 1000,
            axis_length=axis.length,
            entity_count=len(self._features),
            crossing_count=len(crossings),
            incident_count=len(incidents),
        )

        return AnalysisResult(
            axis=axis,
            crossings=crossings,
            incidents=incidents,
            metadata=metadata,
        )

    def _intersect_line_with_axis(
        self,
        line: Polyline,
        axis: Polyline,
        feature: dict[str, Any],
    ) -> list[Crossing]:
        """Intersecta una entidad lineal con el eje."""
        raw_crossings: list[Crossing] = []

        for seg_idx, axis_seg in enumerate(axis.segments):
            axis_cum = axis.cumulative_lengths[seg_idx]

            for line_seg in line.segments:
                pt = segment_intersection(axis_seg, line_seg)
                if pt is not None:
                    local_pk = pt.distance_to(axis_seg.start)
                    pk_val = axis_cum + local_pk

                    raw_crossings.append(self._create_crossing(
                        feature=feature,
                        pk=PK(pk_val),
                        point=pt,
                    ))

        return raw_crossings
