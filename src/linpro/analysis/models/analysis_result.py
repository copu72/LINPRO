"""AnalysisResult — resultado completo de un análisis de detección.

Contiene todos los cruces, incidencias y metadatos de la ejecución.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from linpro.analysis.models.crossing import Crossing
    from linpro.analysis.models.incident import Incident
    from linpro.geometry.primitives.polyline import Polyline as EngineeringAxis


@dataclass
class AnalysisMetadata:
    """Metadatos de la ejecución del detector."""

    detector_name: str = "Unknown"
    detector_version: str = "0.1.0"
    detector_version: str = "0.1.0"
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    axis_length: float = 0.0
    entity_count: int = 0
    crossing_count: int = 0
    incident_count: int = 0


@dataclass
class AnalysisResult:
    """Resultado completo de un análisis.

    Contiene el eje analizado, los cruces detectados,
    las incidencias encontradas y los metadatos.
    """

    axis: EngineeringAxis
    crossings: list[Crossing] = field(default_factory=list)
    incidents: list[Incident] = field(default_factory=list)
    metadata: AnalysisMetadata = field(default_factory=AnalysisMetadata)
