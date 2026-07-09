# 007 — MODELO DE DATOS

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Project
```python
class Project:
    name: str
    alignment: Alignment
    buffer: Buffer
    settings: ProjectSettings
    municipalities: list[Municipality]
    parcels: list[Parcel]
    roads: list[Road]
    rivers: list[River]
    infrastructure: list[Infrastructure]
    results: AnalysisResults
    history: ProjectHistory
```

## Alignment
```python
class Alignment:
    segments: list[Segment]
    # Segment es una unión de: Line, CircularArc, Clothoid
    total_length: float
    stations: list[Station]  # PKs
```

## Parcel (Catastro)
```python
class Parcel:
    reference: str
    area: float
    geometry: Polygon
    municipality: str
    province: str
    use: str
```

## Road
```python
class Road:
    name: str
    road_id: str
    geometry: LineString
    classification: str
```