"""PolygonOverlayDetector — detector genérico de recubrimiento poligonal.

Todo detector que analice solapamiento de polígonos sobre el
Engineering Axis hereda de aquí. Sin lógica espacial duplicada.
"""

from __future__ import annotations

import time
from abc import abstractmethod
from dataclasses import replace
from typing import Any

from linpro.analysis.detectors._helpers import segment_intersection
from linpro.analysis.detectors.base import Detector
from linpro.analysis.models.analysis_result import AnalysisMetadata, AnalysisResult
from linpro.analysis.models.crossing import Crossing
from linpro.analysis.models.incident import Incident, IncidentSeverity
from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.polyline import Polyline
from linpro.geometry.primitives.segment import Segment


class PolygonOverlayDetector(Detector):
    """Detector genérico de recubrimiento poligonal.

    Subclases solo implementan _create_crossing() para definir
    el modelo de salida.

    Args:
        features: Lista de features con clave "polygon" (Polyline).
    """

    INCIDENT_PREFIX: str = "POD"

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
        pk_start: PK,
        pk_end: PK,
        point_start: Point,
        point_end: Point,
    ) -> Crossing:
        """Crea el cruce tipado para la subclase concreta."""

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

                if "polygon" not in feat:
                    incidents.append(Incident(
                        severity=IncidentSeverity.WARNING,
                        code=f"{self.INCIDENT_PREFIX}-002",
                        message=f"Feature '{name}' has no polygon geometry",
                    ))
                    continue

                polygon: Polyline = feat["polygon"]

                if not polygon.bbox.intersects(axis_bbox):
                    continue

                feat_crossings = self._intersect_polygon_with_axis(
                    polygon, axis, feat,
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

    def _intersect_polygon_with_axis(
        self,
        polygon: Polyline,
        axis: Polyline,
        feature: dict[str, Any],
    ) -> list[Crossing]:
        """Intersecta un polígono con el eje y devuelve cruces agrupados."""
        polygon_segs: list[Segment] = polygon.segments
        raw_crossings: list[Crossing] = []

        for seg_idx, axis_seg in enumerate(axis.segments):
            axis_cum = axis.cumulative_lengths[seg_idx]

            for poly_seg in polygon_segs:
                pt = segment_intersection(axis_seg, poly_seg)
                if pt is not None:
                    local_pk = pt.distance_to(axis_seg.start)
                    pk_val = axis_cum + local_pk

                    raw_crossings.append(self._create_crossing(
                        feature=feature,
                        pk_start=PK(pk_val),
                        pk_end=PK(pk_val),
                        point_start=pt,
                        point_end=pt,
                    ))

        return self._merge_crossings(raw_crossings)

    def _group_key(self, crossing: Crossing) -> int:
        """Clave de agrupación para el merge. Override para personalizar."""
        return hash(crossing.pk_start)

    def _merge_crossings(
        self,
        crossings: list[Crossing],
    ) -> list[Crossing]:
        """Agrupa cruces consecutivos de la misma entidad (entrada/salida)."""
        if not crossings:
            return []

        grouped: dict[int, list[Crossing]] = {}
        for c in crossings:
            k = self._group_key(c)
            if k not in grouped:
                grouped[k] = []
            grouped[k].append(c)

        result: list[Crossing] = []
        for _key, group in grouped.items():
            group.sort(key=lambda x: float(x.pk_start))
            i = 0
            while i < len(group):
                if i + 1 < len(group):
                    first = group[i]
                    second = group[i + 1]
                    merged = replace(
                        first,
                        pk_end=second.pk_end,
                        point_end=second.point_end,
                    )
                    result.append(merged)
                    i += 2
                else:
                    result.append(group[i])
                    i += 1

        return result
