"""Spatial Analysis Framework — Engineering Platform de LINPRO.

Los detectores resuelven problemas de ingeniería:
municipios, carreteras, ríos, parcelas, infraestructuras.

Todo análisis sigue el patrón:
  Detector.analyze(axis) → AnalysisResult
"""

from linpro.analysis.detectors.base import Detector
from linpro.analysis.detectors.linear_crossing import LinearCrossingDetector
from linpro.analysis.detectors.municipality import MunicipalityDetector
from linpro.analysis.detectors.polygon_overlay import PolygonOverlayDetector
from linpro.analysis.detectors.road import RoadDetector
from linpro.analysis.models.analysis_result import AnalysisMetadata, AnalysisResult
from linpro.analysis.models.crossing import Crossing, MunicipalityCrossing, RoadCrossing
from linpro.analysis.models.incident import Incident, IncidentSeverity

__all__ = [
    "AnalysisMetadata",
    "AnalysisResult",
    "Crossing",
    "Detector",
    "Incident",
    "IncidentSeverity",
    "LinearCrossingDetector",
    "MunicipalityCrossing",
    "MunicipalityDetector",
    "PolygonOverlayDetector",
    "RoadCrossing",
    "RoadDetector",
]
