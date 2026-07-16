"""GISLoader — carga de datos GIS desde múltiples fuentes.

Soporta GeoJSON, Shapefile (cuando geopandas esté disponible),
y WFS (cuando las dependencias estén instaladas).

Devuelve geometrías como objetos LINPRO (Point, Polyline),
no Shapely.
"""

from __future__ import annotations

import json
from typing import Any

from linpro.geometry.exceptions import GeometryError
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.polyline import Polyline


class GISLoader:
    """Carga datos GIS desde archivos y servicios web.

    Siempre devuelve geometrías LINPRO nativas.
    """

    @staticmethod
    def from_geojson(path: str) -> list[dict[str, Any]]:
        """Carga features desde un archivo GeoJSON.

        Cada feature se devuelve como un diccionario con:
          - "type": tipo de geometría ("Polygon", "MultiPolygon", etc.)
          - "polygon": Polyline LINPRO (perímetro exterior)
          - "properties": propiedades del feature
          - "name", "province", "code": campos extraídos de properties

        Args:
            path: Ruta al archivo GeoJSON.

        Returns:
            Lista de features con geometrías LINPRO.
        """
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if data.get("type") == "FeatureCollection":
            features = data.get("features", [])
        elif data.get("type") == "Feature":
            features = [data]
        else:
            raise GeometryError(f"Unsupported GeoJSON type: {data.get('type')}")

        result = []
        for feat in features:
            props = feat.get("properties", {})
            geom = feat.get("geometry", {})

            if geom.get("type") not in ("Polygon", "MultiPolygon"):
                continue

            coords = geom.get("coordinates", [])
            if geom["type"] == "Polygon":
                ring = coords[0] if coords else []
            else:
                ring = coords[0][0] if coords and coords[0] else []

            if len(ring) < 3:
                continue

            points = [Point(c[0], c[1], c[2] if len(c) > 2 else 0.0) for c in ring]
            polygon = Polyline(points)

            entry = {
                "type": geom["type"],
                "polygon": polygon,
                "properties": props,
                "name": props.get("name", props.get("NAME", props.get("NAMEUNIT", "Unknown"))),
                "province": props.get("province", props.get("PROVINCIA", "")),
                "code": props.get("code", props.get("CODIGO", props.get("CODIGOINE", ""))),
            }
            result.append(entry)

        return result
