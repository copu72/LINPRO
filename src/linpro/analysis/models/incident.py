"""Incident — incidencia o anomalía detectada durante el análisis.

Las incidencias no son excepciones: son parte del resultado.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.primitives.pk import PK


class IncidentSeverity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class Incident:
    """Incidencia detectada durante el análisis.

    Attributes:
        severity: Gravedad de la incidencia.
        code: Código máquina (ej. "MUN-001").
        message: Descripción legible.
        geometry: Geometría asociada (opcional).
        pk: PK asociado (opcional).
    """

    severity: IncidentSeverity
    code: str
    message: str
    geometry: Geometry | None = None
    pk: PK | None = None
