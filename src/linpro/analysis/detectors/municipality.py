"""MunicipalityDetector — detección de municipios sobre el Engineering Axis.

Analiza qué municipios cruza el eje y calcula los PK de
entrada y salida para cada uno.

Sigue el patrón Detector(ABC) definido en RFC-0006.
"""

from __future__ import annotations

import time
from typing import Any

from linpro.analysis.detectors.base import Detector
from linpro.analysis.models.analysis_result import AnalysisMetadata, AnalysisResult
from linpro.analysis.models.crossing import MunicipalityCrossing
from linpro.analysis.models.incident import Incident, IncidentSeverity
from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.polyline import Polyline
from linpro.geometry.primitives.segment import Segment


class MunicipalityDetector(Detector):
    """Detector de municipios que intersectan un Engineering Axis.

    Args:
        municipalities: Lista de municipios con su geometría.
            Cada elemento debe tener:
              - "name" (str): nombre del municipio
              - "province" (str): provincia
              - "code" (str): código INE
              - "polygon" (Polyline): perímetro del municipio (cerrado)
    """

    def __init__(
        self,
        municipalities: list[dict[str, Any]] | None = None,
    ) -> None:
        self._municipalities: list[dict[str, Any]] = municipalities or []

    def load_municipalities(self, municipalities: list[dict[str, Any]]) -> None:
        """Carga o reemplaza la lista de municipios a analizar."""
        self._municipalities = list(municipalities)

    def analyze(self, axis: Polyline) -> AnalysisResult:
        t0 = time.perf_counter()

        crossings: list[MunicipalityCrossing] = []
        incidents: list[Incident] = []

        if not self._municipalities:
            incidents.append(Incident(
                severity=IncidentSeverity.ERROR,
                code="MUN-001",
                message="No municipalities loaded. Call load_municipalities() first.",
            ))
            result = AnalysisResult(
                axis=axis,
                crossings=[],
                incidents=incidents,
                metadata=AnalysisMetadata(
                    detector_name="MunicipalityDetector",
                    axis_length=axis.length,
                    entity_count=0,
                ),
            )
            result.metadata.duration_ms = (time.perf_counter() - t0) * 1000
            return result

        axis_bbox = axis.bbox

        for mun in self._municipalities:
            try:
                name = mun.get("name", "Unknown")
                province = mun.get("province", "")
                code = mun.get("code", "")

                if "polygon" not in mun:
                    incidents.append(Incident(
                        severity=IncidentSeverity.WARNING,
                        code="MUN-002",
                        message=f"Municipality '{name}' has no polygon geometry",
                    ))
                    continue

                polygon: Polyline = mun["polygon"]

                if not polygon.bbox.intersects(axis_bbox):
                    continue

                crossings_for_mun = self._intersect_polygon_with_axis(
                    polygon, axis, name, province, code,
                )
                crossings.extend(crossings_for_mun)

                if not crossings_for_mun:
                    incidents.append(Incident(
                        severity=IncidentSeverity.INFO,
                        code="MUN-003",
                        message=f"Municipality '{name}' bbox overlaps but no crossing found",
                    ))

            except Exception as exc:
                incidents.append(Incident(
                    severity=IncidentSeverity.ERROR,
                    code="MUN-099",
                    message=f"Error processing municipality '{mun.get('name', '?')}': {exc}",
                ))

        t1 = time.perf_counter()
        metadata = AnalysisMetadata(
            detector_name="MunicipalityDetector",
            duration_ms=(t1 - t0) * 1000,
            axis_length=axis.length,
            entity_count=len(self._municipalities),
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
        name: str,
        province: str,
        code: str,
    ) -> list[MunicipalityCrossing]:
        """Intersecta un polígono municipal con el eje.

        Para cada segmento del eje, calcula si intersecta
        el polígono y resuelve los PK de entrada/salida.
        """
        polygon_segs = polygon.segments
        crossings: list[MunicipalityCrossing] = []

        for seg_idx, axis_seg in enumerate(axis.segments):
            axis_cum = axis.cumulative_lengths[seg_idx]

            for poly_seg in polygon_segs:
                pt = self._segment_intersection(axis_seg, poly_seg)
                if pt is not None:
                    local_pk = pt.distance_to(axis_seg.start)
                    pk_val = axis_cum + local_pk

                    crossings.append(MunicipalityCrossing(
                        pk_start=PK(pk_val),
                        pk_end=PK(pk_val),
                        point_start=pt,
                        point_end=pt,
                        municipality=name,
                        province=province,
                        code=code,
                    ))

        return self._merge_crossings(crossings)

    def _segment_intersection(
        self,
        seg1: Segment,
        seg2: Segment,
    ) -> Point | None:
        """Calcula el punto de intersección entre dos segmentos.

        Usa los operadores de LINPRO.
        """
        from linpro.geometry.operators.intersection import intersection_point, intersects

        if not intersects(seg1, seg2):
            return None
        return intersection_point(seg1, seg2)

    def _merge_crossings(
        self,
        crossings: list[MunicipalityCrossing],
    ) -> list[MunicipalityCrossing]:
        """Agrupa cruces consecutivos del mismo municipio.

        Si un municipio tiene múltiples puntos de intersección,
        se agrupan en pares entrada/salida.
        """
        if not crossings:
            return []

        grouped: dict[str, list[MunicipalityCrossing]] = {}
        for c in crossings:
            key = c.code
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(c)

        result: list[MunicipalityCrossing] = []
        for _code, muns in grouped.items():
            muns.sort(key=lambda x: float(x.pk_start))
            merged: list[MunicipalityCrossing] = []
            i = 0
            while i < len(muns):
                if i + 1 < len(muns):
                    first = muns[i]
                    second = muns[i + 1]
                    merged.append(MunicipalityCrossing(
                        pk_start=first.pk_start,
                        pk_end=second.pk_end,
                        point_start=first.point_start,
                        point_end=second.point_end,
                        municipality=first.municipality,
                        province=first.province,
                        code=first.code,
                    ))
                    i += 2
                else:
                    merged.append(muns[i])
                    i += 1
            result.extend(merged)

        return result
