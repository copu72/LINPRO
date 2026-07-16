"""Detector — clase base abstracta para todos los detectores.

Define el contrato que toda detección debe cumplir.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from linpro.analysis.models.analysis_result import AnalysisResult
    from linpro.geometry.primitives.polyline import Polyline as EngineeringAxis


class Detector(ABC):
    """Clase base para todos los detectores de LINPRO.

    Cada detector analiza un EngineeringAxis y devuelve
    un AnalysisResult con los cruces detectados.

    Example:
        >>> detector = MunicipalityDetector(data_path="municipios.geojson")
        >>> result = detector.analyze(axis)
    """

    @abstractmethod
    def analyze(self, axis: EngineeringAxis) -> AnalysisResult:
        """Ejecuta el análisis sobre el eje dado.

        Args:
            axis: Engineering Axis a analizar.

        Returns:
            AnalysisResult con cruces, incidencias y metadatos.
        """
