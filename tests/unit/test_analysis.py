"""Tests para el Spatial Analysis Framework (RFC-0006).

Cubre: modelos, detectores, servicios.
"""

from __future__ import annotations

import json
from datetime import datetime

import pytest

from linpro.analysis import (
    AnalysisMetadata,
    AnalysisResult,
    Crossing,
    Detector,
    Incident,
    IncidentSeverity,
    LinearCrossingDetector,
    MunicipalityCrossing,
    MunicipalityDetector,
    PolygonOverlayDetector,
    RoadCrossing,
    RoadDetector,
)
from linpro.analysis.services.gis_loader import GISLoader
from linpro.analysis.services.spatial_index import SpatialIndex
from linpro.geometry import PK, Point, Polyline
from linpro.geometry.exceptions import GeometryError

# ======================================================================
#  FIXTURES
# ======================================================================


@pytest.fixture
def square_polygon() -> Polyline:
    return Polyline([
        Point(0, 0),
        Point(100, 0),
        Point(100, 100),
        Point(0, 100),
        Point(0, 0),
    ])


@pytest.fixture
def triangle_polygon() -> Polyline:
    return Polyline([
        Point(50, 0),
        Point(100, 100),
        Point(0, 100),
        Point(50, 0),
    ])


@pytest.fixture
def horizontal_axis() -> Polyline:
    return Polyline([Point(-10, 50), Point(110, 50)])


@pytest.fixture
def vertical_axis() -> Polyline:
    return Polyline([Point(50, -10), Point(50, 110)])


@pytest.fixture
def crossing_road() -> Polyline:
    """Diagonal road that crosses vertical_axis at (50, 50)."""
    return Polyline([Point(0, 0), Point(100, 100)])


@pytest.fixture
def parallel_road() -> Polyline:
    """Road far to the right, doesn't cross vertical_axis (x=50)."""
    return Polyline([Point(200, 0), Point(200, 100)])


@pytest.fixture
def sample_roads(crossing_road, parallel_road) -> list[dict]:
    return [
        {"id": "A-4", "name": "Autovía del Sur", "type": "autovía", "polyline": crossing_road},
        {"id": "M-40", "name": "Calle 30", "type": "autovía", "polyline": parallel_road},
    ]


@pytest.fixture
def sample_municipalities(square_polygon, triangle_polygon) -> list[dict]:
    return [
        {
            "name": "Madrid",
            "province": "Madrid",
            "code": "28079",
            "polygon": square_polygon,
        },
        {
            "name": "Toledo",
            "province": "Toledo",
            "code": "45168",
            "polygon": triangle_polygon,
        },
    ]


# ======================================================================
#  MODELOS — AnalysisResult
# ======================================================================


class TestAnalysisResult:
    def test_create_empty(self):
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = AnalysisResult(axis=axis)
        assert result.axis is axis
        assert result.crossings == []
        assert result.incidents == []

    def test_create_with_crossings(self):
        axis = Polyline([Point(0, 0), Point(10, 0)])
        c = MunicipalityCrossing(
            pk_start=PK(0), pk_end=PK(10),
            point_start=Point(0, 0), point_end=Point(10, 0),
            municipality="Test", province="P", code="00000",
        )
        result = AnalysisResult(axis=axis, crossings=[c])
        assert len(result.crossings) == 1
        assert result.crossings[0].municipality == "Test"


class TestAnalysisMetadata:
    def test_defaults(self):
        m = AnalysisMetadata(detector_name="Test")
        assert m.detector_name == "Test"
        assert m.detector_version == "0.1.0"
        assert isinstance(m.timestamp, datetime)
        assert m.duration_ms == 0.0
        assert m.axis_length == 0.0

    def test_with_values(self):
        m = AnalysisMetadata(
            detector_name="X",
            duration_ms=100.5,
            axis_length=500.0,
            entity_count=10,
            crossing_count=3,
            incident_count=1,
        )
        assert m.duration_ms == 100.5


# ======================================================================
#  MODELOS — Crossing
# ======================================================================


class TestCrossing:
    def test_crossing_base_concrete(self):
        c = Crossing(pk_start=PK(0), pk_end=PK(10),
                     point_start=Point(0, 0), point_end=Point(10, 0))
        assert isinstance(c, Crossing)
        assert c.length == 10.0

    def test_municipality_crossing(self):
        c = MunicipalityCrossing(
            pk_start=PK(100),
            pk_end=PK(200),
            point_start=Point(100, 0),
            point_end=Point(200, 0),
            municipality="Madrid",
            province="Madrid",
            code="28079",
        )
        assert c.municipality == "Madrid"
        assert c.province == "Madrid"
        assert c.code == "28079"
        assert c.length == 100.0

    def test_crossing_immutable(self):
        c = MunicipalityCrossing(
            pk_start=PK(0), pk_end=PK(10),
            point_start=Point(0, 0), point_end=Point(10, 0),
            municipality="M", province="P", code="00000",
        )
        with pytest.raises(Exception):
            c.municipality = "Other"

    def test_crossing_length_zero(self):
        c = MunicipalityCrossing(
            pk_start=PK(50), pk_end=PK(50),
            point_start=Point(50, 0), point_end=Point(50, 0),
            municipality="M", province="P", code="00000",
        )
        assert c.length == 0.0

    def test_crossing_pk_types(self):
        c = MunicipalityCrossing(
            pk_start=PK(0), pk_end=PK(100),
            point_start=Point(0, 0), point_end=Point(100, 0),
            municipality="M", province="P", code="00000",
        )
        assert isinstance(c.pk_start, PK)
        assert isinstance(c.pk_end, PK)
        assert isinstance(c.length, float)


# ======================================================================
#  MODELOS — Incident
# ======================================================================


class TestIncident:
    def test_create_info(self):
        i = Incident(severity=IncidentSeverity.INFO, code="INF-001", message="Info")
        assert i.severity == IncidentSeverity.INFO
        assert i.code == "INF-001"

    def test_create_warning(self):
        i = Incident(severity=IncidentSeverity.WARNING, code="WARN-001", message="Warning")
        assert i.severity == IncidentSeverity.WARNING

    def test_create_error(self):
        i = Incident(severity=IncidentSeverity.ERROR, code="ERR-001", message="Error")
        assert i.severity == IncidentSeverity.ERROR

    def test_with_geometry(self):
        i = Incident(
            severity=IncidentSeverity.WARNING,
            code="GEO-001",
            message="Geometry issue",
            geometry=Point(10, 20),
            pk=PK(150),
        )
        assert i.geometry is not None
        assert i.pk == PK(150)

    def test_without_optional(self):
        i = Incident(severity=IncidentSeverity.INFO, code="INF-001", message="Info")
        assert i.geometry is None
        assert i.pk is None

    def test_severity_values(self):
        assert IncidentSeverity.INFO.value == "INFO"
        assert IncidentSeverity.WARNING.value == "WARNING"
        assert IncidentSeverity.ERROR.value == "ERROR"


# ======================================================================
#  DETECTOR — Base
# ======================================================================


class TestDetectorBase:
    def test_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            Detector()

    def test_municipality_is_detector(self):
        d = MunicipalityDetector()
        assert isinstance(d, Detector)

    def test_detector_has_analyze(self):
        d = MunicipalityDetector()
        assert hasattr(d, "analyze")
        assert callable(d.analyze)


# ======================================================================
#  DETECTOR — MunicipalityDetector
# ======================================================================


class TestMunicipalityDetector:
    def test_no_municipalities(self, horizontal_axis):
        d = MunicipalityDetector()
        result = d.analyze(horizontal_axis)
        assert len(result.crossings) == 0
        assert len(result.incidents) == 1
        assert result.incidents[0].code == "MUN-001"

    def test_crosses_square(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        result = d.analyze(vertical_axis)
        # vertical axis at x=50 crosses the square at y=0..100
        assert len(result.crossings) >= 1

    def test_no_crossing_far_axis(self, sample_municipalities):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        far = Polyline([Point(500, 500), Point(600, 600)])
        result = d.analyze(far)
        assert len(result.crossings) == 0
        # Municipios that don't intersect the bbox are skipped silently

    def test_result_has_axis(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        result = d.analyze(vertical_axis)
        assert result.axis is vertical_axis

    def test_result_metadata(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        result = d.analyze(vertical_axis)
        assert result.metadata.detector_name == "MunicipalityDetector"
        assert result.metadata.entity_count == 2
        assert result.metadata.duration_ms > 0

    def test_load_municipalities(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector()
        d.load_municipalities(sample_municipalities)
        result = d.analyze(vertical_axis)
        assert len(result.crossings) >= 1
        assert result.metadata.entity_count == 2

    def test_reload_municipalities(self):
        d = MunicipalityDetector(municipalities=[])
        d.load_municipalities([])
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = d.analyze(axis)
        assert len(result.crossings) == 0

    def test_missing_polygon(self, horizontal_axis):
        muns = [{"name": "NoPoly", "province": "P", "code": "00000"}]
        d = MunicipalityDetector(municipalities=muns)
        result = d.analyze(horizontal_axis)
        assert len(result.crossings) == 0
        warnings = [i for i in result.incidents if i.code == "MUN-002"]
        assert len(warnings) == 1

    def test_bbox_filter(self, sample_municipalities):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        far = Polyline([Point(999, 999), Point(1000, 1000)])
        result = d.analyze(far)
        assert len(result.crossings) == 0
        # Both municipios are far, so no crossings and no MUN-003 incidents

    def test_crossing_has_correct_fields(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        result = d.analyze(vertical_axis)
        for c in result.crossings:
            assert isinstance(c, MunicipalityCrossing)
            assert isinstance(c.municipality, str)
            assert isinstance(c.province, str)
            assert isinstance(c.code, str)
            assert isinstance(c.pk_start, PK)
            assert isinstance(c.pk_end, PK)
            assert isinstance(c.point_start, Point)
            assert isinstance(c.point_end, Point)

    def test_detector_name_in_metadata(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        result = d.analyze(vertical_axis)
        assert result.metadata.detector_name == "MunicipalityDetector"


# ======================================================================
#  SERVICIOS — GISLoader
# ======================================================================


class TestGISLoader:
    def test_from_geojson_simple(self, tmp_path):
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Madrid",
                        "PROVINCIA": "Madrid",
                        "CODIGOINE": "28079",
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]],
                    },
                },
            ],
        }
        path = tmp_path / "test.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        features = GISLoader.from_geojson(str(path))
        assert len(features) == 1
        assert features[0]["name"] == "Madrid"
        assert features[0]["province"] == "Madrid"
        assert features[0]["code"] == "28079"
        assert "polygon" in features[0]
        assert features[0]["polygon"].vertex_count >= 3

    def test_from_geojson_single_feature(self, tmp_path):
        data = {
            "type": "Feature",
            "properties": {"name": "Toledo"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]],
            },
        }
        path = tmp_path / "single.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        features = GISLoader.from_geojson(str(path))
        assert len(features) == 1
        assert features[0]["name"] == "Toledo"

    def test_from_geojson_multipolygon(self, tmp_path):
        data = {
            "type": "Feature",
            "properties": {"name": "Multi"},
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]],
            },
        }
        path = tmp_path / "multi.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        features = GISLoader.from_geojson(str(path))
        assert len(features) == 1
        assert "polygon" in features[0]

    def test_from_geojson_unsupported_type(self, tmp_path):
        data = {
            "type": "Point",
            "coordinates": [0, 0],
        }
        path = tmp_path / "point.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        with pytest.raises(GeometryError):
            GISLoader.from_geojson(str(path))

    def test_from_geojson_empty_features(self, tmp_path):
        data = {"type": "FeatureCollection", "features": []}
        path = tmp_path / "empty.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        features = GISLoader.from_geojson(str(path))
        assert features == []

    def test_property_fallback(self, tmp_path):
        data = {
            "type": "Feature",
            "properties": {"NAME": "Barcelona", "CODIGO": "08019"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]],
            },
        }
        path = tmp_path / "fallback.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        features = GISLoader.from_geojson(str(path))
        assert features[0]["name"] == "Barcelona"
        assert features[0]["code"] == "08019"

    def test_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            GISLoader.from_geojson("nonexistent.geojson")

    def test_from_geojson_skips_non_polygon(self, tmp_path):
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Point"},
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Poly"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]],
                    },
                },
            ],
        }
        path = tmp_path / "mixed.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        features = GISLoader.from_geojson(str(path))
        assert len(features) == 1
        assert features[0]["name"] == "Poly"

    def test_from_geojson_skips_degenerate_polygon(self, tmp_path):
        data = {
            "type": "Feature",
            "properties": {"name": "Bad"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [10, 0]]],
            },
        }
        path = tmp_path / "degenerate.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        features = GISLoader.from_geojson(str(path))
        assert len(features) == 0


# ======================================================================
#  SERVICIOS — SpatialIndex
# ======================================================================


class TestSpatialIndex:
    def test_build_and_query(self):
        axis = Polyline([Point(0, 0), Point(100, 0), Point(100, 100)])
        idx = SpatialIndex()
        idx.build(axis)
        assert len(idx._segments) == 2
        assert len(idx._bboxes) == 2

    def test_query_intersecting(self):
        axis = Polyline([Point(0, 0), Point(100, 0)])
        idx = SpatialIndex()
        idx.build(axis)
        from linpro.geometry import BoundingBox
        results = idx.query(BoundingBox(0, -10, 50, 10))
        assert len(results) >= 1

    def test_query_non_intersecting(self):
        axis = Polyline([Point(0, 0), Point(100, 0)])
        idx = SpatialIndex()
        idx.build(axis)
        from linpro.geometry import BoundingBox
        results = idx.query(BoundingBox(500, 500, 600, 600))
        assert len(results) == 0

    def test_empty_index(self):
        idx = SpatialIndex()
        from linpro.geometry import BoundingBox
        results = idx.query(BoundingBox(0, 0, 10, 10))
        assert results == []

    def test_rebuild(self):
        axis1 = Polyline([Point(0, 0), Point(10, 0)])
        axis2 = Polyline([Point(0, 0), Point(20, 0), Point(30, 0)])
        idx = SpatialIndex()
        idx.build(axis1)
        assert len(idx._segments) == 1
        idx.build(axis2)
        assert len(idx._segments) == 2


# ======================================================================
#  INTEGRACIÓN — Detector + Services
# ======================================================================


class TestIntegration:
    def test_detector_with_geojson(self, tmp_path, vertical_axis):
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Madrid", "PROVINCIA": "Madrid", "CODIGOINE": "28079"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]]],
                    },
                },
            ],
        }
        path = tmp_path / "madrid.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        municipalities = GISLoader.from_geojson(str(path))
        detector = MunicipalityDetector(municipalities=municipalities)
        result = detector.analyze(vertical_axis)
        assert len(result.crossings) >= 1
        assert result.crossings[0].municipality == "Madrid"

    def test_spatial_index_with_detector(self, sample_municipalities, vertical_axis):
        idx = SpatialIndex()
        idx.build(vertical_axis)
        # Use spatial index to test query works alongside detector
        from linpro.geometry import BoundingBox
        seg_indices = idx.query(BoundingBox(40, -10, 60, 110))
        assert len(seg_indices) >= 1

        detector = MunicipalityDetector(municipalities=sample_municipalities)
        result = detector.analyze(vertical_axis)
        assert len(result.crossings) >= 1

    def test_full_pipeline(self, tmp_path, vertical_axis):
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Madrid", "PROVINCIA": "Madrid", "CODIGOINE": "28079"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Toledo", "PROVINCIA": "Toledo", "CODIGOINE": "45168"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[50, 0], [150, 100], [-50, 100], [50, 0]]],
                    },
                },
            ],
        }
        path = tmp_path / "muns.geojson"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        municipalities = GISLoader.from_geojson(str(path))
        detector = MunicipalityDetector(municipalities=municipalities)
        result = detector.analyze(vertical_axis)

        assert isinstance(result, AnalysisResult)
        assert result.metadata.detector_name == "MunicipalityDetector"
        assert result.metadata.duration_ms > 0
        assert all(isinstance(c, MunicipalityCrossing) for c in result.crossings)
        assert all(isinstance(i, Incident) for i in result.incidents)


# ======================================================================
#  EDGE CASES
# ======================================================================


class TestEdgeCases:
    def test_axis_single_point(self):
        mun = {
            "name": "Test",
            "province": "P",
            "code": "00000",
            "polygon": Polyline([
                Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10), Point(0, 0),
            ]),
        }
        d = MunicipalityDetector(municipalities=[mun])
        axis = Polyline([Point(5, 5), Point(5, 5)])  # zero-length axis
        result = d.analyze(axis)
        assert result.metadata.axis_length == 0.0

    def test_empty_polygon(self):
        with pytest.raises(Exception):
            Polyline([Point(0, 0)])

    def test_large_coordinates(self):
        mun = {
            "name": "Large",
            "province": "P",
            "code": "00000",
            "polygon": Polyline([
                Point(500000, 4600000),
                Point(510000, 4610000),
                Point(520000, 4600000),
                Point(500000, 4600000),
            ]),
        }
        d = MunicipalityDetector(municipalities=[mun])
        axis = Polyline([
            Point(505000, 4605000),
            Point(515000, 4605000),
        ])
        result = d.analyze(axis)
        assert isinstance(result, AnalysisResult)

    def test_detector_exception_handling(self):
        class BadMunicipality:
            pass

        mun = {
            "name": "Bad",
            "province": "P",
            "code": "00000",
            "polygon": "not_a_polyline",  # will cause error
        }
        d = MunicipalityDetector(municipalities=[mun])
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = d.analyze(axis)
        errors = [i for i in result.incidents if i.code == "MUN-099"]
        assert len(errors) >= 1

    def test_crossing_at_boundary(self):
        polygon = Polyline([
            Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10), Point(0, 0),
        ])
        mun = {
            "name": "Bdry",
            "province": "P",
            "code": "00000",
            "polygon": polygon,
        }
        d = MunicipalityDetector(municipalities=[mun])
        # Axis along the boundary of the polygon
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = d.analyze(axis)
        assert isinstance(result, AnalysisResult)

    def test_incident_code_format(self):
        i = Incident(severity=IncidentSeverity.ERROR, code="GEN-001", message="test")
        assert i.code.count("-") == 1

    def test_analysis_result_repr(self):
        axis = Polyline([Point(0, 0), Point(10, 0)])
        r = AnalysisResult(axis=axis)
        assert r.axis is not None

    def test_detector_with_3d_polygon(self):
        mun = {
            "name": "3D",
            "province": "P",
            "code": "00000",
            "polygon": Polyline([
                Point(0, 0, 100),
                Point(10, 0, 200),
                Point(10, 10, 300),
                Point(0, 10, 400),
                Point(0, 0, 500),
            ]),
        }
        d = MunicipalityDetector(municipalities=[mun])
        axis = Polyline([Point(5, -10), Point(5, 20)])
        result = d.analyze(axis)
        assert len(result.crossings) >= 1


# ======================================================================
#  HITO C — Generic Detectors
# ======================================================================


class TestPolygonOverlayDetector:
    def test_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            PolygonOverlayDetector()

    def test_is_detector(self):
        assert issubclass(PolygonOverlayDetector, Detector)

    def test_has_abstract_method(self):
        assert PolygonOverlayDetector._create_crossing.__isabstractmethod__

    def test_detector_name_default(self):
        class Concrete(PolygonOverlayDetector):
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        d = Concrete()
        assert d.detector_name == "Concrete"

    def test_no_features(self, vertical_axis):
        class Concrete(PolygonOverlayDetector):
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        d = Concrete()
        result = d.analyze(vertical_axis)
        assert len(result.crossings) == 0
        assert len(result.incidents) == 1
        assert result.incidents[0].code == "POD-001"

    def test_load_features(self, sample_municipalities, vertical_axis):
        class Concrete(PolygonOverlayDetector):
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        d = Concrete()
        d.load_features(sample_municipalities)
        result = d.analyze(vertical_axis)
        assert len(result.crossings) >= 1
        assert result.metadata.entity_count == 2

    def test_missing_polygon(self, horizontal_axis):
        class Concrete(PolygonOverlayDetector):
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        d = Concrete(features=[{"name": "NoPoly"}])
        result = d.analyze(horizontal_axis)
        warnings = [i for i in result.incidents if i.code == "POD-002"]
        assert len(warnings) == 1

    def test_bbox_filter(self, sample_municipalities):
        class Concrete(PolygonOverlayDetector):
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        d = Concrete(features=sample_municipalities)
        far = Polyline([Point(999, 999), Point(1000, 1000)])
        result = d.analyze(far)
        assert len(result.crossings) == 0

    def test_bbox_overlap_no_crossing(self):
        """Polygon bbox overlaps axis bbox but no segment intersection."""
        class Concrete(PolygonOverlayDetector):
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        # Axis is a rectangular perimeter; polygon sits inside the gap
        axis = Polyline([
            Point(0, 0), Point(100, 0), Point(100, 300), Point(0, 300), Point(0, 0),
        ])
        polygon = Polyline([
            Point(20, 100), Point(80, 100), Point(80, 200), Point(20, 200), Point(20, 100),
        ])
        d = Concrete(features=[{"name": "Inside", "polygon": polygon}])
        result = d.analyze(axis)
        infos = [i for i in result.incidents if i.code == "POD-003"]
        assert len(infos) == 1
        assert len(result.crossings) == 0

    def test_error_handling(self):
        class Concrete(PolygonOverlayDetector):
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        d = Concrete(features=[{"name": "Bad", "polygon": "not_a_polyline"}])
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = d.analyze(axis)
        errors = [i for i in result.incidents if i.code == "POD-099"]
        assert len(errors) >= 1

    def test_incident_prefix_override(self):
        class Custom(PolygonOverlayDetector):
            INCIDENT_PREFIX = "CUS"
            def _create_crossing(self, feature, pk_start, pk_end, point_start, point_end):
                return Crossing(pk_start=pk_start, pk_end=pk_end,
                                point_start=point_start, point_end=point_end)

        d = Custom()
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = d.analyze(axis)
        assert result.incidents[0].code == "CUS-001"


class TestLinearCrossingDetector:
    def test_abstract_cannot_instantiate(self):
        with pytest.raises(TypeError):
            LinearCrossingDetector()

    def test_is_detector(self):
        assert issubclass(LinearCrossingDetector, Detector)

    def test_has_abstract_method(self):
        assert LinearCrossingDetector._create_crossing.__isabstractmethod__

    def test_no_features(self, vertical_axis):
        class Concrete(LinearCrossingDetector):
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        d = Concrete()
        result = d.analyze(vertical_axis)
        assert len(result.crossings) == 0
        assert len(result.incidents) == 1
        assert result.incidents[0].code == "LCD-001"

    def test_detector_name_default(self):
        class Concrete(LinearCrossingDetector):
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        d = Concrete()
        assert d.detector_name == "Concrete"

    def test_load_features(self, sample_roads, vertical_axis):
        class Concrete(LinearCrossingDetector):
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        d = Concrete()
        d.load_features(sample_roads)
        result = d.analyze(vertical_axis)
        assert len(result.crossings) >= 1
        assert result.metadata.entity_count == 2

    def test_missing_polyline(self, vertical_axis):
        class Concrete(LinearCrossingDetector):
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        d = Concrete(features=[{"name": "NoLine"}])
        result = d.analyze(vertical_axis)
        warnings = [i for i in result.incidents if i.code == "LCD-002"]
        assert len(warnings) == 1

    def test_bbox_filter(self, sample_roads):
        class Concrete(LinearCrossingDetector):
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        d = Concrete(features=sample_roads)
        far = Polyline([Point(999, 999), Point(1000, 1000)])
        result = d.analyze(far)
        assert len(result.crossings) == 0

    def test_bbox_overlap_no_crossing(self):
        """Feature bbox overlaps axis bbox but no segment intersection."""
        class Concrete(LinearCrossingDetector):
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        # Axis is a rectangular perimeter; vertical road sits in the interior gap
        axis = Polyline([
            Point(0, 0), Point(100, 0), Point(100, 300), Point(0, 300), Point(0, 0),
        ])
        road = Polyline([Point(50, 100), Point(50, 200)])
        d = Concrete(features=[{"name": "Inside", "polyline": road}])
        result = d.analyze(axis)
        infos = [i for i in result.incidents if i.code == "LCD-003"]
        assert len(infos) == 1
        assert len(result.crossings) == 0

    def test_incident_prefix_override(self):
        class Custom(LinearCrossingDetector):
            INCIDENT_PREFIX = "CUS"
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        d = Custom()
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = d.analyze(axis)
        assert result.incidents[0].code == "CUS-001"

    def test_error_handling(self):
        class Concrete(LinearCrossingDetector):
            def _create_crossing(self, feature, pk, point):
                return Crossing(pk_start=pk, pk_end=pk,
                                point_start=point, point_end=point)

        d = Concrete(features=[{"name": "Bad", "polyline": "not_a_polyline"}])
        axis = Polyline([Point(0, 0), Point(10, 0)])
        result = d.analyze(axis)
        errors = [i for i in result.incidents if i.code == "LCD-099"]
        assert len(errors) >= 1


# ======================================================================
#  DETECTOR — RoadDetector
# ======================================================================


class TestRoadDetector:
    def test_no_roads(self, vertical_axis):
        d = RoadDetector()
        result = d.analyze(vertical_axis)
        assert len(result.crossings) == 0
        assert len(result.incidents) == 1
        assert result.incidents[0].code == "ROD-001"

    def test_is_detector(self):
        assert issubclass(RoadDetector, Detector)

    def test_is_linear_crossing_detector(self):
        assert isinstance(RoadDetector(), LinearCrossingDetector)

    def test_crosses_single_road(self, crossing_road, vertical_axis):
        roads = [
            {"id": "A-4", "name": "Autovía del Sur", "type": "autovía", "polyline": crossing_road},
        ]
        d = RoadDetector(roads=roads)
        result = d.analyze(vertical_axis)
        assert len(result.crossings) >= 1
        c = result.crossings[0]
        assert isinstance(c, RoadCrossing)
        assert c.road_id == "A-4"
        assert c.road_name == "Autovía del Sur"
        assert c.road_type == "autovía"

    def test_parallel_road_no_crossing(self, parallel_road, vertical_axis):
        roads = [{"id": "M-40", "name": "Calle 30", "type": "autovía", "polyline": parallel_road}]
        d = RoadDetector(roads=roads)
        result = d.analyze(vertical_axis)
        assert len(result.crossings) == 0

    def test_load_roads(self, sample_roads, vertical_axis):
        d = RoadDetector()
        d.load_roads(sample_roads)
        result = d.analyze(vertical_axis)
        assert len(result.crossings) >= 1
        assert result.metadata.entity_count == 2

    def test_crossing_has_correct_fields(self, sample_roads, vertical_axis):
        d = RoadDetector(roads=sample_roads)
        result = d.analyze(vertical_axis)
        for c in result.crossings:
            assert isinstance(c, RoadCrossing)
            assert isinstance(c.road_id, str)
            assert isinstance(c.road_name, str)
            assert isinstance(c.road_type, str)
            assert isinstance(c.pk_start, PK)
            assert isinstance(c.pk_end, PK)
            assert isinstance(c.point_start, Point)
            assert isinstance(c.point_end, Point)

    def test_crossing_pk_equal(self, sample_roads, vertical_axis):
        d = RoadDetector(roads=sample_roads)
        result = d.analyze(vertical_axis)
        for c in result.crossings:
            assert c.pk_start == c.pk_end

    def test_metadata(self, sample_roads, vertical_axis):
        d = RoadDetector(roads=sample_roads)
        result = d.analyze(vertical_axis)
        assert result.metadata.detector_name == "RoadDetector"
        assert result.metadata.entity_count == 2
        assert result.metadata.duration_ms > 0


# ======================================================================
#  MODELOS — RoadCrossing
# ======================================================================


class TestRoadCrossingModel:
    def test_create(self):
        c = RoadCrossing(
            pk_start=PK(100),
            pk_end=PK(100),
            point_start=Point(100, 0),
            point_end=Point(100, 0),
            road_id="A-4",
            road_name="Autovía del Sur",
            road_type="autovía",
        )
        assert c.road_id == "A-4"
        assert c.road_name == "Autovía del Sur"
        assert c.road_type == "autovía"
        assert c.length == 0.0

    def test_is_crossing(self):
        c = RoadCrossing(
            pk_start=PK(0), pk_end=PK(0),
            point_start=Point(0, 0), point_end=Point(0, 0),
            road_id="1", road_name="R1", road_type="nacional",
        )
        assert isinstance(c, Crossing)

    def test_immutable(self):
        c = RoadCrossing(
            pk_start=PK(0), pk_end=PK(0),
            point_start=Point(0, 0), point_end=Point(0, 0),
            road_id="1", road_name="R1", road_type="nacional",
        )
        with pytest.raises(Exception):
            c.road_id = "2"


# ======================================================================
#  HITO C — MunDetector sigue funcionando tras refactor
# ======================================================================


class TestRefactoredMunicipalityDetector:
    def test_is_polygon_overlay_detector(self, sample_municipalities):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        assert isinstance(d, PolygonOverlayDetector)

    def test_municipality_detector_name(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector(municipalities=sample_municipalities)
        result = d.analyze(vertical_axis)
        assert result.metadata.detector_name == "MunicipalityDetector"

    def test_incident_prefix_unchanged(self):
        assert MunicipalityDetector.INCIDENT_PREFIX == "MUN"

    def test_load_municipalities_api(self, sample_municipalities, vertical_axis):
        d = MunicipalityDetector()
        d.load_municipalities(sample_municipalities)
        result = d.analyze(vertical_axis)
        assert len(result.crossings) >= 1
