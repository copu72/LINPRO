"""Servicios de negocio de LINPRO.

Los servicios orquestan la lógica de análisis. Cada servicio
se encarga de un dominio específico: municipios, catastro,
carreteras, ríos, infraestructuras.

Los servicios dependen del Core (Configuration, EventBus, Logger)
y de los modelos de dominio. Nunca dependen de otros servicios.
"""

from typing import Any, Dict, List, Optional

from linpro.core import EventBus, LINPROLogger
from linpro.models import (
    AnalysisResult,
    Municipality,
    Parcel,
    Road,
    River,
    Infrastructure,
    Project,
)


class BaseService:
    def __init__(self) -> None:
        self.logger = LINPROLogger.get_instance()
        self.event_bus = EventBus.get_instance()

    def analyze(self, project: Project, **kwargs: Any) -> AnalysisResult:
        raise NotImplementedError


class MunicipalityService(BaseService):
    def analyze(self, project: Project, **kwargs: Any) -> AnalysisResult:
        ...


class CadastreService(BaseService):
    def analyze(self, project: Project, **kwargs: Any) -> AnalysisResult:
        ...


class RoadService(BaseService):
    def analyze(self, project: Project, **kwargs: Any) -> AnalysisResult:
        ...


class HydrologyService(BaseService):
    def analyze(self, project: Project, **kwargs: Any) -> AnalysisResult:
        ...


class InfrastructureService(BaseService):
    def analyze(self, project: Project, **kwargs: Any) -> AnalysisResult:
        ...


__all__ = [
    "BaseService",
    "MunicipalityService",
    "CadastreService",
    "RoadService",
    "HydrologyService",
    "InfrastructureService",
]