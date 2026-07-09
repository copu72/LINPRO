"""Motor matemático de LINPRO.

Contiene los algoritmos de cálculo puro. No contiene objetos
de dominio, solo funciones y clases matemáticas.

Los algoritmos se organizan por tipo de cálculo, no por módulo
de negocio. Esto permite reutilizarlos desde cualquier servicio.
"""

from typing import List, Tuple

import numpy as np


def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    ...


def calculate_angle(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
    ...


def calculate_azimuth(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    ...


def interpolate_point(segment: Any, distance: float) -> Tuple[float, float]:
    ...


def project_point_to_line(point: Tuple[float, float], line_start: Tuple[float, float], line_end: Tuple[float, float]) -> Tuple[float, float, float]:
    ...


def offset_polygon(points: List[Tuple[float, float]], distance: float, side: str = "both") -> Any:
    ...


__all__ = [
    "calculate_distance",
    "calculate_angle",
    "calculate_azimuth",
    "interpolate_point",
    "project_point_to_line",
    "offset_polygon",
]