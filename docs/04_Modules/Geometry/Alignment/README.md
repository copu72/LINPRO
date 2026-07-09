# Módulo: Geometry.Alignment

**Versión:** 1.0
**Fecha:** 2026-07-09

## Propósito

Definir y gestionar ejes geométricos (alignments) compuestos por una secuencia ordenada de segmentos: rectas, curvas circulares y clotoides.

## Dependencias

- LINPRO Core (Project, Settings)

## Archivos

- `alignment.py` — Clase Alignment y segmentos (Straight, CircularArc, Clothoid)
- `validation.py` — Validación de continuidad geométrica
- `import_export.py` — Importar/exportar alignment desde/hacia CSV, GeoJSON

## Requisitos implementados

- FR-0001: Definir eje

## API pública

```python
class Alignment:
    def add_straight(self, start: tuple, end: tuple) -> None
    def add_circular_arc(self, start: tuple, end: tuple, radius: float, center: tuple, direction: str) -> None
    def add_clothoid(self, start: tuple, end: tuple, A: float, start_radius: float, end_radius: float) -> None
    def validate(self) -> bool
    def total_length(self) -> float
    def get_segments(self) -> list[Segment]
```