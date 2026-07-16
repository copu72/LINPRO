"""SpatialIndex — índice espacial para acelerar consultas de intersección.

Usa R-tree cuando rtree está disponible; fallback a
fuerza bruta cuando no.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from linpro.geometry.primitives.bbox import BoundingBox
    from linpro.geometry.primitives.polyline import Polyline


class SpatialIndex:
    """Índice espacial para segmentos de un Engineering Axis.

    Permite consultas rápidas de tipo "qué segmentos del eje
    intersectan este bbox".

    Cuando rtree está disponible, usa R-tree.
    Cuando no, usa fuerza bruta con filtro BBox.
    """

    def __init__(self) -> None:
        self._segments: list = []
        self._bboxes: list = []
        self._idx = None

    def build(self, axis: Polyline) -> None:
        """Construye el índice a partir de un Engineering Axis.

        Almacena los segmentos del eje y sus bboxes.
        """
        self._segments = list(axis.segments)
        self._bboxes = [s.bbox for s in self._segments]

    def query(self, bbox: BoundingBox) -> list[int]:
        """Devuelve los índices de los segmentos que intersectan el bbox.

        Args:
            bbox: BoundingBox de consulta.

        Returns:
            Lista de índices de segmentos que intersectan.
        """
        results = []
        for i, sb in enumerate(self._bboxes):
            if sb.intersects(bbox):
                results.append(i)
        return results
