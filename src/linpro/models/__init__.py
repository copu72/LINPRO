"""Clases de dominio de LINPRO.

Aquí viven las entidades del negocio: Project, Alignment, Road,
Municipality, Parcel, River, Infrastructure, etc.

Cada clase es un objeto de datos inmutable (dataclass) que representa
una entidad del dominio. No contienen lógica de negocio.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional


class SoilClass(Enum):
    RUSTICO = auto()
    URBANO = auto()
    INDUSTRIAL = auto()


class RoadType(Enum):
    AUTOPISTA = auto()
    AUTOVIA = auto()
    NACIONAL = auto()
    AUTONOMICA = auto()
    LOCAL = auto()
    CAMINO = auto()


class RiverType(Enum):
    PERMANENTE = auto()
    ESTACIONAL = auto()


@dataclass
class Project:
    name: str
    description: str = ""
    author: str = ""
    company: str = ""
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    version: str = "0.1.0"
    epsg: int = 25830
    data: Dict[str, Any] = field(default_factory=dict)
    path: Optional[Path] = None


@dataclass
class Alignment:
    segments: List[Any] = field(default_factory=list)
    total_length: float = 0.0


@dataclass
class Municipality:
    code: str
    name: str
    province: str
    ccaa: str
    pk_start: float = 0.0
    pk_end: float = 0.0
    length: float = 0.0


@dataclass
class Parcel:
    reference: str
    area: float = 0.0
    soil_class: SoilClass = SoilClass.RUSTICO
    municipality: str = ""
    province: str = ""
    use: str = ""
    affected_area: float = 0.0


@dataclass
class Road:
    name: str
    road_id: str
    road_type: RoadType = RoadType.NACIONAL
    pk: float = 0.0
    angle: float = 0.0
    distance: float = 0.0


@dataclass
class River:
    name: str
    river_type: RiverType = RiverType.PERMANENTE
    confederation: str = ""
    pk: float = 0.0
    width: float = 0.0


@dataclass
class Infrastructure:
    name: str
    infra_type: str = ""
    owner: str = ""
    pk: float = 0.0
    distance: float = 0.0
    angle: float = 0.0


@dataclass
class AnalysisResult:
    module: str
    status: str = "pending"
    data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


__all__ = [
    "SoilClass", "RoadType", "RiverType",
    "Project", "Alignment", "Municipality", "Parcel",
    "Road", "River", "Infrastructure", "AnalysisResult",
]