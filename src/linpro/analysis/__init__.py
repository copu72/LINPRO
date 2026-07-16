"""Spatial Analysis Framework — Engineering Platform de LINPRO.

Los detectores resuelven problemas de ingeniería:
municipios, carreteras, ríos, parcelas, infraestructuras.

Todo análisis sigue el patrón:
  Detector.analyze(axis) → AnalysisResult
"""

from linpro.analysis.detectors.base import Detector
from linpro.analysis.detectors.municipality import MunicipalityDetector
from linpro.analysis.models.analysis_result import AnalysisMetadata, AnalysisResult
from linpro.analysis.models.crossing import Crossing, MunicipalityCrossing
from linpro.analysis.models.incident import Incident, IncidentSeverity

__all__ = [
    "AnalysisMetadata",
    "AnalysisResult",
    "Crossing",
    "Detector",
    "Incident",
    "IncidentSeverity",
    "MunicipalityCrossing",
    "MunicipalityDetector",
]
