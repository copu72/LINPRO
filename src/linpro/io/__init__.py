"""Entrada y salida de LINPRO.

Gestiona la lectura y escritura de archivos: importación y
exportación de datos en múltiples formatos (CSV, GeoJSON,
Shapefile, DXF, Excel, etc.).
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from linpro.models import Project, Alignment, Municipality, Parcel, Road


class FileImporter:
    @staticmethod
    def read_csv(path: Path, delimiter: str = ",") -> List[Dict[str, Any]]:
        ...

    @staticmethod
    def read_geojson(path: Path) -> Dict[str, Any]:
        ...

    @staticmethod
    def read_shapefile(path: Path) -> Any:
        ...


class FileExporter:
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], path: Path) -> None:
        ...

    @staticmethod
    def to_geojson(data: Dict[str, Any], path: Path) -> None:
        ...

    @staticmethod
    def to_dxf(project: Project, path: Path) -> None:
        ...

    @staticmethod
    def to_excel(project: Project, path: Path) -> None:
        ...


def import_alignment(path: str) -> Alignment:
    ...


def export_results(project: Project, output_dir: str, formats: Optional[List[str]] = None) -> Dict[str, str]:
    ...


__all__ = ["FileImporter", "FileExporter", "import_alignment", "export_results"]