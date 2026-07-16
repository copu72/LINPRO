"""TASK-0006: Tests Polyline — Engineering Axis.

Cobertura ≥99%, tests ≥200.
"""

from __future__ import annotations

import json
import math
import pickle

import pytest

from linpro.geometry import PK, EngineeringAxis, Point, Polyline
from linpro.geometry.exceptions import GeometryError
from linpro.geometry.primitives.bbox import BoundingBox
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.vector import Vector

# ======================================================================
#  HELPER FIXTURES
# ======================================================================


@pytest.fixture
def simple_poly() -> Polyline:
    return Polyline([Point(0, 0), Point(100, 0), Point(100, 100)])


@pytest.fixture
def zigzag() -> Polyline:
    return Polyline([
        Point(0, 0),
        Point(50, 50),
        Point(100, 0),
        Point(150, 50),
        Point(200, 0),
    ])


@pytest.fixture
def single_seg() -> Polyline:
    return Polyline([Point(10, 20), Point(30, 50)])


@pytest.fixture
def utm_poly() -> Polyline:
    return Polyline([
        Point(500000.0, 4600000.0),
        Point(510000.0, 4610000.0),
        Point(520000.0, 4610000.0),
        Point(530000.0, 4600000.0),
    ])


# ======================================================================
#  PK VALUE OBJECT
# ======================================================================


class TestPK:
    def test_create(self):
        pk = PK(1250.34)
        assert float(pk) == 1250.34

    def test_create_int(self):
        pk = PK(100)
        assert float(pk) == 100.0

    def test_create_zero(self):
        pk = PK(0)
        assert float(pk) == 0.0

    def test_create_negative(self):
        pk = PK(-50.0)
        assert float(pk) == -50.0

    def test_add_pk_pk(self):
        assert float(PK(100) + PK(50)) == 150.0

    def test_add_pk_float(self):
        assert float(PK(100) + 50.0) == 150.0

    def test_add_pk_int(self):
        assert float(PK(100) + 50) == 150.0

    def test_radd(self):
        assert float(50.0 + PK(100)) == 150.0

    def test_sub_pk_pk(self):
        assert float(PK(100) - PK(30)) == 70.0

    def test_sub_pk_float(self):
        assert float(PK(100) - 30.0) == 70.0

    def test_rsub(self):
        assert float(PK(100) - 150) == -50.0
        assert float(200 - PK(50)) == 150.0

    def test_mul(self):
        assert float(PK(100) * 2) == 200.0
        assert float(3 * PK(50)) == 150.0

    def test_truediv(self):
        assert float(PK(100) / 2) == 50.0

    def test_neg(self):
        assert float(-PK(50)) == -50.0

    def test_abs(self):
        assert abs(PK(-50)) == 50.0
        assert abs(PK(50)) == 50.0

    def test_eq(self):
        assert PK(100) == PK(100)
        assert PK(100) == 100.0
        assert PK(100) == 100

    def test_eq_tolerance(self):
        assert PK(100) == PK(100.0000000005)

    def test_ne(self):
        assert not (PK(100) != PK(100))

    def test_lt(self):
        assert PK(50) < PK(100)
        assert PK(50) < 100
        assert PK(50) < 100.0

    def test_le(self):
        assert PK(50) <= PK(100)
        assert PK(100) <= PK(100)
        assert PK(100) <= 100.0

    def test_gt(self):
        assert PK(100) > PK(50)
        assert PK(100) > 50

    def test_ge(self):
        assert PK(100) >= PK(50)
        assert PK(100) >= PK(100)
        assert PK(100) >= 50.0
        assert PK(100) >= 50

    def test_hash(self):
        assert hash(PK(100)) == hash(PK(100))
        s = {PK(100), PK(100), PK(200)}
        assert len(s) == 2

    def test_int_conversion(self):
        assert int(PK(1250.7)) == 1250

    def test_repr(self):
        assert repr(PK(1250.34)) == "PK(1250.34)"

    def test_str(self):
        assert "PK" in str(PK(1250.34))

    def test_not_implemented(self):
        with pytest.raises(TypeError):
            _ = PK(100) + "string"

    def test_le_not_implemented(self):
        with pytest.raises(TypeError):
            _ = PK(100) <= "string"

    def test_lt_not_implemented(self):
        with pytest.raises(TypeError):
            _ = PK(100) < "string"

    def test_gt_not_implemented(self):
        with pytest.raises(TypeError):
            _ = PK(100) > "string"

    def test_ge_not_implemented(self):
        with pytest.raises(TypeError):
            _ = PK(100) >= "string"

    def test_rsub_not_implemented(self):
        with pytest.raises(TypeError):
            _ = "string" - PK(100)

    def test_mul_not_implemented(self):
        with pytest.raises(TypeError):
            _ = PK(100) * "string"

    def test_truediv_not_implemented(self):
        with pytest.raises(TypeError):
            _ = PK(100) / "string"

    def test_pos(self):
        assert float(+PK(50)) == 50.0

    def test_value_property(self):
        pk = PK(42.5)
        assert pk.value == 42.5

    def test_eq_string_returns_false(self):
        assert (PK(100) == "string") is False

    def test_ge_string_raises(self):
        with pytest.raises(TypeError):
            _ = PK(100) >= "string"

    def test_sub_string_raises(self):
        with pytest.raises(TypeError):
            _ = PK(100) - "string"


class TestConstruction:
    def test_create_points(self):
        pts = [Point(0, 0), Point(1, 1)]
        p = Polyline(pts)
        assert p.vertex_count == 2

    def test_create_min_vertices(self):
        with pytest.raises(GeometryError):
            Polyline([Point(0, 0)])

    def test_create_empty_list(self):
        with pytest.raises(GeometryError):
            Polyline([])

    def test_create_tuple(self):
        p = Polyline((Point(0, 0), Point(1, 1), Point(2, 2)))
        assert p.vertex_count == 3

    def test_create_invalid_point(self):
        with pytest.raises(Exception):
            Polyline([Point(0, 0), "not_a_point"])

    def test_from_segments(self):
        segs = [Segment(Point(0, 0), Point(10, 0)), Segment(Point(10, 0), Point(20, 0))]
        p = Polyline.from_segments(segs)
        assert p.vertex_count == 3
        assert p.length == 20.0

    def test_from_segments_disconnected(self):
        segs = [Segment(Point(0, 0), Point(10, 0)), Segment(Point(20, 0), Point(30, 0))]
        with pytest.raises(GeometryError):
            Polyline.from_segments(segs)

    def test_from_segments_empty(self):
        with pytest.raises(GeometryError):
            Polyline.from_segments([])

    def test_from_segments_single(self):
        segs = [Segment(Point(0, 0), Point(10, 0))]
        p = Polyline.from_segments(segs)
        assert p.vertex_count == 2

    def test_from_dict(self):
        data = {
            "vertices": [
                {"x": 0.0, "y": 0.0, "z": 0.0},
                {"x": 10.0, "y": 0.0, "z": 0.0},
            ],
        }
        p = Polyline.from_dict(data)
        assert p.vertex_count == 2
        assert p.length == 10.0

    def test_from_dict_with_closed(self):
        data = {
            "vertices": [
                {"x": 0.0, "y": 0.0, "z": 0.0},
                {"x": 10.0, "y": 0.0, "z": 0.0},
            ],
            "closed": True,
        }
        p = Polyline.from_dict(data)
        assert p.closed is True

    def test_from_json(self):
        data = json.dumps({
            "vertices": [
                {"x": 0.0, "y": 0.0, "z": 0.0},
                {"x": 10.0, "y": 0.0, "z": 0.0},
            ],
        })
        p = Polyline.from_json(data)
        assert p.vertex_count == 2
        assert p.length == 10.0

    def test_engineering_alias(self):
        pts = [Point(0, 0), Point(1, 1), Point(2, 2)]
        p = EngineeringAxis(pts)
        assert isinstance(p, Polyline)

    def test_closed_flag(self):
        p = Polyline([Point(0, 0), Point(10, 0), Point(10, 10)], closed=True)
        assert p.closed is True
        p2 = Polyline([Point(0, 0), Point(10, 0), Point(10, 10)])
        assert p2.closed is False

    def test_vertex_count_property(self):
        p = Polyline([Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)])
        assert p.vertex_count == 4
        assert p.segment_count == 3


# ======================================================================
#  DXF
# ======================================================================


class TestDxf:
    def test_from_dxf_lwpolyline(self):
        import os
        path = os.path.join(os.path.dirname(__file__), "..", "golden", "test_polyline.dxf")
        p = Polyline.from_dxf(path)
        assert p.vertex_count == 3
        assert p.start.almost_equal(Point(0, 0))
        assert p.end.almost_equal(Point(100, 100))
        assert abs(p.length - 200.0) < 1e-6

    def test_from_dxf_line(self):
        import os
        path = os.path.join(os.path.dirname(__file__), "..", "golden", "test_line.dxf")
        p = Polyline.from_dxf(path)
        assert p.vertex_count == 2
        assert p.start == Point(0, 0)
        assert p.end == Point(100, 0)

    def test_from_dxf_layer_filter(self):
        import os
        path = os.path.join(os.path.dirname(__file__), "..", "golden", "test_polyline.dxf")
        with pytest.raises(GeometryError):
            Polyline.from_dxf(path, layer="NONEXISTENT")

    def test_from_dxf_no_polyline(self):
        import os
        path = os.path.join(os.path.dirname(__file__), "..", "golden", "test_line.dxf")
        with pytest.raises(GeometryError):
            Polyline.from_dxf(path, layer="NONEXISTENT")

    def test_from_dxf_file_not_found(self):
        with pytest.raises(Exception):
            Polyline.from_dxf("nonexistent.dxf")

    def test_from_dxf_import_error(self, monkeypatch):
        import builtins as _b
        orig_import = _b.__import__

        def mock_import(name, *args, **kwargs):
            if name == 'ezdxf':
                raise ImportError("No module named ezdxf")
            return orig_import(name, *args, **kwargs)

        monkeypatch.setattr(_b, '__import__', mock_import)
        with pytest.raises(GeometryError, match="ezdxf is required"):
            Polyline.from_dxf("test.dxf")

    def test_from_dxf_legacy_polyline(self):
        import os
        path = os.path.join(os.path.dirname(__file__), "..", "golden", "test_polyline_legacy.dxf")
        p = Polyline.from_dxf(path)
        assert p.vertex_count == 3
        assert p.start.almost_equal(Point(0, 0))
        assert p.end.almost_equal(Point(100, 100))
        assert abs(p.length - 200.0) < 1e-6


# ======================================================================
#  PROPERTIES
# ======================================================================


class TestProperties:
    def test_length_simple(self, simple_poly):
        assert simple_poly.length == 200.0

    def test_length_zigzag(self, zigzag):
        seg_len = math.sqrt(50**2 + 50**2)
        expected = seg_len * 4
        assert abs(zigzag.length - expected) < 1e-9

    def test_vertices(self, simple_poly):
        verts = simple_poly.vertices
        assert len(verts) == 3
        assert all(isinstance(v, Point) for v in verts)

    def test_segments(self, simple_poly):
        segs = simple_poly.segments
        assert len(segs) == 2
        assert all(isinstance(s, Segment) for s in segs)
        assert segs[0].start == Point(0, 0)
        assert segs[0].end == Point(100, 0)
        assert segs[1].start == Point(100, 0)
        assert segs[1].end == Point(100, 100)

    def test_bbox(self, simple_poly):
        bb = simple_poly.bbox
        assert isinstance(bb, BoundingBox)
        assert bb.xmin == 0.0
        assert bb.xmax == 100.0
        assert bb.ymin == 0.0
        assert bb.ymax == 100.0

    def test_start(self, simple_poly):
        assert simple_poly.start == Point(0, 0)

    def test_end(self, simple_poly):
        assert simple_poly.end == Point(100, 100)

    def test_center(self, simple_poly):
        c = simple_poly.center
        expected = Point(200 / 3, 100 / 3)
        assert c.almost_equal(expected)

    def test_dimension(self, simple_poly):
        assert simple_poly.dimension == 1

    def test_is_empty(self, simple_poly):
        assert simple_poly.is_empty is False

    def test_is_valid(self, simple_poly):
        assert simple_poly.is_valid is True

    def test_cumulative_lengths(self, simple_poly):
        cum = simple_poly.cumulative_lengths
        assert len(cum) == 3
        assert cum[0] == 0.0
        assert cum[1] == 100.0
        assert cum[2] == 200.0

    def test_cumulative_lengths_zigzag(self, zigzag):
        cum = zigzag.cumulative_lengths
        assert len(cum) == 5
        assert cum[0] == 0.0
        assert cum[-1] == zigzag.length

    def test_length_cached(self, simple_poly):
        assert simple_poly.length == simple_poly._total_length

    def test_repr(self, simple_poly):
        r = repr(simple_poly)
        assert "Polyline" in r
        assert "3 vertices" in r
        assert "200.000" in r

    def test_str(self, simple_poly):
        s = str(simple_poly)
        assert "Polyline" in s


# ======================================================================
#  TOPOLOGY
# ======================================================================


class TestTopology:
    def test_segment_at(self, simple_poly):
        s = simple_poly.segment_at(0)
        assert s.start == Point(0, 0)
        assert s.end == Point(100, 0)

    def test_segment_at_last(self, simple_poly):
        s = simple_poly.segment_at(1)
        assert s.start == Point(100, 0)

    def test_segment_at_oob(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.segment_at(999)

    def test_segment_at_negative(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.segment_at(-1)

    def test_vertex_at(self, simple_poly):
        assert simple_poly.vertex_at(0) == Point(0, 0)
        assert simple_poly.vertex_at(1) == Point(100, 0)
        assert simple_poly.vertex_at(2) == Point(100, 100)

    def test_vertex_at_oob(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.vertex_at(999)

    def test_pk_at_vertex(self, simple_poly):
        assert float(simple_poly.pk_at_vertex(0)) == 0.0
        assert float(simple_poly.pk_at_vertex(1)) == 100.0
        assert float(simple_poly.pk_at_vertex(2)) == 200.0

    def test_pk_at_vertex_oob(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.pk_at_vertex(999)

    def test_pk_at_vertex_negative(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.pk_at_vertex(-1)

    def test_pk_at_vertex_last(self, simple_poly):
        pk = simple_poly.pk_at_vertex(simple_poly.segment_count)
        assert float(pk) == simple_poly.length

    def test_len(self, simple_poly, zigzag):
        assert len(simple_poly) == 3
        assert len(zigzag) == 5

    def test_iter(self, simple_poly):
        verts = list(simple_poly)
        assert len(verts) == 3
        assert all(isinstance(v, Point) for v in verts)

    def test_getitem(self, simple_poly):
        assert simple_poly[0] == Point(0, 0)
        assert simple_poly[-1] == Point(100, 100)


# ======================================================================
#  INGENIERÍA — PK Engine
# ======================================================================


class TestPkEngine:
    def test_point_at_pk_0(self, simple_poly):
        pt = simple_poly.point_at_pk(PK(0))
        assert pt == Point(0, 0, 0)

    def test_point_at_pk_length(self, simple_poly):
        pt = simple_poly.point_at_pk(PK(200))
        assert pt == Point(100, 100, 0)

    def test_point_at_pk_mid_first_seg(self, simple_poly):
        pt = simple_poly.point_at_pk(PK(50))
        assert pt == Point(50, 0, 0)

    def test_point_at_pk_mid_second_seg(self, simple_poly):
        pt = simple_poly.point_at_pk(PK(150))
        assert pt == Point(100, 50, 0)

    def test_point_at_pk_float_arg(self, simple_poly):
        pt = simple_poly.point_at_pk(50.0)
        assert pt == Point(50, 0, 0)

    def test_point_at_pk_int_arg(self, simple_poly):
        pt = simple_poly.point_at_pk(100)
        assert pt == Point(100, 0, 0)

    def test_point_at_pk_negative(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.point_at_pk(-1)

    def test_point_at_pk_exceeds_length(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.point_at_pk(201)

    def test_point_at_pk_endpoint_tol(self, simple_poly):
        pt = simple_poly.point_at_pk(200.0 - 1e-10)
        assert pt.almost_equal(Point(100, 100, 0))

    def test_point_at_pk_start_tol(self, simple_poly):
        pt = simple_poly.point_at_pk(1e-10)
        assert pt.almost_equal(Point(0, 0, 0))

    def test_point_at_pk_zigzag_first(self, zigzag):
        seg_len = math.sqrt(50**2 + 50**2)
        pt = zigzag.point_at_pk(seg_len)
        assert pt == Point(50, 50)

    def test_point_at_pk_zigzag_mid(self, zigzag):
        pt = zigzag.point_at_pk(zigzag.length / 2)
        assert pt.almost_equal(Point(100, 0))

    def test_point_at_pk_utm(self, utm_poly):
        pt = utm_poly.point_at_pk(0)
        assert pt == utm_poly.start

    def test_point_at_pk_utm_end(self, utm_poly):
        pt = utm_poly.point_at_pk(utm_poly.length)
        assert pt == utm_poly.end

    def test_pk_of_vertex(self, simple_poly):
        assert float(simple_poly.pk_of(Point(0, 0))) == 0.0
        assert float(simple_poly.pk_of(Point(100, 0))) == 100.0
        assert float(simple_poly.pk_of(Point(100, 100))) == 200.0

    def test_pk_of_midpoint(self, simple_poly):
        pk = simple_poly.pk_of(Point(50, 0))
        assert abs(float(pk) - 50.0) < 1e-9

    def test_pk_of_off_axis(self, simple_poly):
        pk = simple_poly.pk_of(Point(50, -50))
        expected = 50.0
        assert abs(float(pk) - expected) < 1e-6

    def test_pk_of_far_point(self, simple_poly):
        pk = simple_poly.pk_of(Point(150, -50))
        expected = 100.0
        assert abs(float(pk) - expected) < 1e-6

    def test_pk_of_near_end(self, simple_poly):
        pk = simple_poly.pk_of(Point(100, 100))
        assert abs(float(pk) - 200.0) < 1e-9

    def test_pk_of_returns_pk_type(self, simple_poly):
        pk = simple_poly.pk_of(Point(50, 0))
        assert isinstance(pk, PK)

    def test_pk_of_invalid_type(self, simple_poly):
        with pytest.raises(Exception):
            simple_poly.pk_of("not_a_point")

    def test_project_onto_line(self, simple_poly):
        proj = simple_poly.project(Point(50, -50))
        assert proj == Point(50, 0)

    def test_project_off_axis(self, simple_poly):
        proj = simple_poly.project(Point(-10, 0))
        assert proj == Point(-10, 0)

    def test_project_returns_point(self, simple_poly):
        proj = simple_poly.project(Point(50, 50))
        assert isinstance(proj, Point)

    def test_closest_point_vertex(self, simple_poly):
        cp = simple_poly.closest_point(Point(0, 0))
        assert cp == Point(0, 0)

    def test_closest_point_mid(self, simple_poly):
        cp = simple_poly.closest_point(Point(50, -50))
        assert cp == Point(50, 0)

    def test_closest_point_near_segment(self, simple_poly):
        cp = simple_poly.closest_point(Point(50, 10))
        assert cp == Point(50, 0)

    def test_closest_point_far(self, simple_poly):
        cp = simple_poly.closest_point(Point(999, 999))
        assert cp == Point(100, 100)

    def test_segment_at_pk_first(self, simple_poly):
        s = simple_poly.segment_at_pk(0)
        assert s == Segment(Point(0, 0), Point(100, 0))

    def test_segment_at_pk_mid(self, simple_poly):
        s = simple_poly.segment_at_pk(150)
        assert s == Segment(Point(100, 0), Point(100, 100))

    def test_segment_at_pk_last(self, simple_poly):
        s = simple_poly.segment_at_pk(200)
        assert s == Segment(Point(100, 0), Point(100, 100))

    def test_segment_at_pk_float(self, simple_poly):
        s = simple_poly.segment_at_pk(50.0)
        assert s == Segment(Point(0, 0), Point(100, 0))

    def test_azimuth_at_pk_first(self, simple_poly):
        az = simple_poly.azimuth_at_pk(0)
        assert abs(az - 0.0) < 1e-9

    def test_azimuth_at_pk_second(self, simple_poly):
        az = simple_poly.azimuth_at_pk(150)
        assert abs(az - 90.0) < 1e-9

    def test_azimuth_at_pk_45(self, zigzag):
        seg_len = math.sqrt(50**2 + 50**2)
        az = zigzag.azimuth_at_pk(seg_len / 2)
        assert abs(az - 45.0) < 1e-9

    def test_azimuth_at_pk_negative(self, zigzag):
        seg_len = math.sqrt(50**2 + 50**2)
        az = zigzag.azimuth_at_pk(3 * seg_len)
        assert abs(az - (-45.0)) < 1e-9

    def test_normal_at_pk_first(self, simple_poly):
        n = simple_poly.normal_at_pk(50)
        assert n.almost_equal(Vector(0, 1))

    def test_normal_at_pk_second(self, simple_poly):
        n = simple_poly.normal_at_pk(150)
        assert n.almost_equal(Vector(-1, 0))

    def test_normal_at_pk_unit(self, simple_poly):
        n = simple_poly.normal_at_pk(50)
        assert abs(n.length - 1.0) < 1e-9

    def test_round_trip_pk_point_at_pk(self, simple_poly):
        for pk_val in [0.0, 50.0, 100.0, 150.0, 200.0]:
            pt = simple_poly.point_at_pk(pk_val)
            pk_back = simple_poly.pk_of(pt)
            assert abs(float(pk_back) - pk_val) < 1e-6

    def test_round_trip_closest_point_at_pk(self, simple_poly):
        for pk_val in [25.0, 75.0, 125.0, 175.0]:
            pt = simple_poly.point_at_pk(pk_val)
            cp = simple_poly.closest_point(pt)
            assert pt.almost_equal(cp)

    def test_project_on_axis_point(self, simple_poly):
        on_axis = Point(50, 0)
        proj = simple_poly.project(on_axis)
        assert proj.almost_equal(on_axis)

    def test_closest_point_on_axis(self, simple_poly):
        on_axis = Point(50, 0)
        cp = simple_poly.closest_point(on_axis)
        assert cp.almost_equal(on_axis)

    def test_pk_of_off_axis_by_50(self, simple_poly):
        pk = simple_poly.pk_of(Point(50, -50))
        assert abs(float(pk) - 50.0) < 1e-9

    def test_pk_of_prefers_smaller_pk_on_tie(self):
        p = Polyline([
            Point(0, 0),
            Point(10, 0),
            Point(10, 10),
        ])
        pk = p.pk_of(Point(5, 5))
        assert abs(float(pk) - 5.0) < 1e-6


# ======================================================================
#  MUTACIÓN
# ======================================================================


class TestMutation:
    def test_reverse(self, simple_poly):
        rev = simple_poly.reverse()
        assert rev.vertex_count == 3
        assert rev[0] == Point(100, 100)
        assert rev[-1] == Point(0, 0)
        assert rev.length == simple_poly.length

    def test_reverse_preserves_length(self, simple_poly):
        rev = simple_poly.reverse()
        assert abs(rev.length - simple_poly.length) < 1e-12

    def test_copy(self, simple_poly):
        c = simple_poly.copy()
        assert c == simple_poly
        assert c is not simple_poly

    def test_copy_independent(self, simple_poly):
        c = simple_poly.copy()
        c.append(Point(200, 200))
        assert c.vertex_count == 4
        assert simple_poly.vertex_count == 3

    def test_append(self, simple_poly):
        simple_poly.append(Point(200, 200))
        assert simple_poly.vertex_count == 4
        assert simple_poly.segment_count == 3
        assert abs(simple_poly.length - 341.421356237) < 1e-6

    def test_append_updates_bbox(self, simple_poly):
        simple_poly.append(Point(200, 200))
        bb = simple_poly.bbox
        assert bb.xmax == 200.0
        assert bb.ymax == 200.0

    def test_append_invalid(self, simple_poly):
        with pytest.raises(Exception):
            simple_poly.append("not_a_point")

    def test_extend(self, simple_poly):
        simple_poly.extend([Point(200, 200), Point(300, 200)])
        assert simple_poly.vertex_count == 5
        assert simple_poly.segment_count == 4

    def test_extend_empty(self, simple_poly):
        simple_poly.extend([])
        assert simple_poly.vertex_count == 3

    def test_simplify_returns_copy(self, simple_poly):
        s = simple_poly.simplify(1.0)
        assert s == simple_poly
        assert s is not simple_poly

    def test_split_at_mid(self, simple_poly):
        left, right = simple_poly.split(100)
        assert left.vertex_count >= 2
        assert right.vertex_count >= 2
        assert left[0] == Point(0, 0)
        assert right[0].almost_equal(Point(100, 0))
        assert right[-1] == Point(100, 100)

    def test_split_at_third(self, simple_poly):
        left, right = simple_poly.split(150)
        assert left.vertex_count == 3
        assert right.vertex_count == 2
        assert left[-1].almost_equal(Point(100, 50))
        assert right[0].almost_equal(Point(100, 50))

    def test_split_raises_at_zero(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.split(0)

    def test_split_raises_at_length(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.split(simple_poly.length)

    def test_split_raises_out_of_range(self, simple_poly):
        with pytest.raises(GeometryError):
            simple_poly.split(-1)

    def test_merge(self, simple_poly):
        other = Polyline([Point(100, 100), Point(200, 200)])
        merged = simple_poly.merge(other)
        assert merged.vertex_count == 5
        assert merged.length > simple_poly.length

    def test_merge_empty(self, simple_poly):
        merged = simple_poly.merge(Polyline([Point(0, 0), Point(1, 1)]))
        assert merged.vertex_count == 5

    def test_merge_preserves_start(self, simple_poly):
        other = Polyline([Point(200, 200), Point(300, 300)])
        merged = simple_poly.merge(other)
        assert merged[0] == Point(0, 0)

    def test_reverse_does_not_mutate(self, simple_poly):
        orig = simple_poly.copy()
        _ = simple_poly.reverse()
        assert simple_poly == orig

    def test_append_chain(self):
        p = Polyline([Point(0, 0), Point(10, 0)])
        p.append(Point(10, 10))
        p.append(Point(20, 10))
        p.append(Point(20, 0))
        assert p.vertex_count == 5
        assert p.segment_count == 4
        assert p.length == 40.0


# ======================================================================
#  SERIALIZACIÓN
# ======================================================================


class TestSerialization:
    def test_to_dict(self, simple_poly):
        d = simple_poly.to_dict()
        assert d["type"] == "Polyline"
        assert len(d["vertices"]) == 3
        assert d["closed"] is False

    def test_to_dict_and_back(self, simple_poly):
        d = simple_poly.to_dict()
        p = Polyline.from_dict(d)
        assert p == simple_poly

    def test_to_json(self, simple_poly):
        js = simple_poly.to_json()
        data = json.loads(js)
        assert data["type"] == "Polyline"

    def test_to_json_and_back(self, simple_poly):
        js = simple_poly.to_json()
        p = Polyline.from_json(js)
        assert p == simple_poly

    def test_to_json_indent(self, simple_poly):
        js = simple_poly.to_json(indent=2)
        assert "\n" in js

    def test_to_wkt(self, simple_poly):
        wkt = simple_poly.to_wkt()
        assert wkt.startswith("LINESTRING")
        assert "(0 0, 100 0, 100 100)" in wkt or "(0 0, 100 0, 100 100)" in wkt

    def test_to_wkt_3_vertices(self):
        p = Polyline([Point(0, 0), Point(10, 10), Point(20, 0)])
        wkt = p.to_wkt()
        assert "(0 0, 10 10, 20 0)" in wkt

    def test_to_wkt_floats(self):
        p = Polyline([Point(1.5, 2.5), Point(3.5, 4.5)])
        wkt = p.to_wkt()
        assert "1.5 2.5" in wkt

    def test_to_dict_utm(self, utm_poly):
        d = utm_poly.to_dict()
        assert len(d["vertices"]) == 4
        assert d["vertices"][0]["x"] == 500000.0

    def test_from_dict_json_roundtrip(self):
        pts = [Point(1, 2), Point(3, 4), Point(5, 6)]
        p = Polyline(pts)
        d = p.to_dict()
        p2 = Polyline.from_dict(d)
        assert p2 == p
        assert p2.vertex_count == 3
        assert p2.length == p.length

    def test_from_segments_to_dict_roundtrip(self):
        segs = [Segment(Point(0, 0), Point(10, 0)), Segment(Point(10, 0), Point(10, 10))]
        p = Polyline.from_segments(segs)
        d = p.to_dict()
        p2 = Polyline.from_dict(d)
        assert p2 == p

    def test_pickle(self, simple_poly):
        data = pickle.dumps(simple_poly)
        p = pickle.loads(data)
        assert p == simple_poly
        assert p.length == simple_poly.length

    def test_from_json_kwargs(self, simple_poly):
        js = simple_poly.to_json()
        p = Polyline.from_json(js)
        assert p == simple_poly


# ======================================================================
#  OPERADORES / COMPARACIÓN
# ======================================================================


class TestOperators:
    def test_eq_identical(self, simple_poly):
        p2 = Polyline([Point(0, 0), Point(100, 0), Point(100, 100)])
        assert simple_poly == p2

    def test_eq_same_points_different_instances(self, simple_poly):
        p2 = Polyline([Point(0, 0), Point(100, 0), Point(100, 100)])
        assert simple_poly == p2

    def test_eq_different_length(self):
        p1 = Polyline([Point(0, 0), Point(10, 0)])
        p2 = Polyline([Point(0, 0), Point(20, 0)])
        assert p1 != p2

    def test_eq_different_count(self):
        p1 = Polyline([Point(0, 0), Point(10, 0)])
        p2 = Polyline([Point(0, 0), Point(10, 0), Point(20, 0)])
        assert p1 != p2

    def test_eq_different_closed(self):
        p1 = Polyline([Point(0, 0), Point(10, 0)], closed=False)
        p2 = Polyline([Point(0, 0), Point(10, 0)], closed=True)
        assert p1 != p2

    def test_eq_not_polyline(self, simple_poly):
        assert simple_poly != "not a polyline"
        assert simple_poly != Point(0, 0)
        assert simple_poly != 42

    def test_eq_tolerance(self):
        pts1 = [Point(0, 0), Point(10, 0)]
        pts2 = [Point(0, 1e-10), Point(10, 1e-10)]
        p1 = Polyline(pts1)
        p2 = Polyline(pts2)
        assert p1 == p2

    def test_eq_near_tolerance(self):
        pts1 = [Point(0, 0), Point(10, 0)]
        pts2 = [Point(0, 1e-8), Point(10, 1e-8)]
        p1 = Polyline(pts1)
        p2 = Polyline(pts2)
        assert p1 != p2

    def test_check_invariants_valid(self, simple_poly):
        simple_poly.check_invariants()

    def test_check_invariants_raises(self):
        p = Polyline([Point(0, 0), Point(10, 0)])
        p._vertices.pop()
        with pytest.raises(GeometryError):
            p.check_invariants()

    def test_not_implemented_error_int(self, simple_poly):
        assert (simple_poly == 42) is False

    def test_reverse_equality_not_same(self, simple_poly):
        rev = simple_poly.reverse()
        assert rev != simple_poly

    def test_append_extend_equality(self):
        p1 = Polyline([Point(0, 0), Point(10, 0)])
        p1.append(Point(20, 0))
        p2 = Polyline([Point(0, 0), Point(10, 0), Point(20, 0)])
        assert p1 == p2

    def test_extend_equality(self):
        p1 = Polyline([Point(0, 0), Point(10, 0)])
        p1.extend([Point(20, 0), Point(30, 0)])
        p2 = Polyline([Point(0, 0), Point(10, 0), Point(20, 0), Point(30, 0)])
        assert p1 == p2

    def test_check_invariants_segment_count_mismatch(self):
        p = Polyline([Point(0, 0), Point(10, 0), Point(20, 0)])
        p._segments.pop()
        with pytest.raises(GeometryError):
            p.check_invariants()

    def test_check_invariants_cumulative_lengths_mismatch(self):
        p = Polyline([Point(0, 0), Point(10, 0), Point(20, 0)])
        p._cumulative_lengths.pop()
        with pytest.raises(GeometryError):
            p.check_invariants()

    def test_is_valid_returns_false_on_corruption(self):
        p = Polyline([Point(0, 0), Point(10, 0)])
        p._vertices.append("bad")
        assert p.is_valid is False

    def test_is_valid_returns_false_on_bad_segments(self):
        p = Polyline([Point(0, 0), Point(10, 0)])
        p._segments.append(None)
        assert p.is_valid is False


# ======================================================================
#  EDGE CASES
# ======================================================================


class TestEdgeCases:
    def test_zero_length_segments(self):
        p = Polyline([
            Point(0, 0),
            Point(0, 0),
            Point(10, 0),
        ])
        assert p.length == 10.0

    def test_point_at_pk_zero_segment(self):
        p = Polyline([Point(0, 0), Point(0, 0), Point(10, 0)])
        pt = p.point_at_pk(0)
        assert pt == Point(0, 0)

    def test_normal_at_zero_length_segment(self):
        p = Polyline([Point(0, 0), Point(1e-12, 0), Point(10, 0)])
        n = p.normal_at_pk(0)
        assert n.length < 1e-9

    def test_single_segment_length(self, single_seg):
        expected = math.sqrt(20**2 + 30**2)
        assert abs(single_seg.length - expected) < 1e-9

    def test_single_segment_point_at_pk(self, single_seg):
        pt = single_seg.point_at_pk(single_seg.length / 2)
        mid = Point(
            (10 + 30) / 2,
            (20 + 50) / 2,
        )
        assert pt.almost_equal(mid)

    def test_single_segment_closest_point(self, single_seg):
        cp = single_seg.closest_point(Point(10, 20))
        assert cp == Point(10, 20)

    def test_all_identical_points(self):
        p = Polyline([Point(5, 5), Point(5, 5), Point(5, 5)])
        assert p.length == 0.0
        assert p.bbox.xmin == p.bbox.xmax == 5.0

    def test_point_at_pk_on_zero_length(self):
        p = Polyline([Point(5, 5), Point(5, 5)])
        pt = p.point_at_pk(0)
        assert pt == Point(5, 5)

    def test_azimuth_on_zero_length(self):
        p = Polyline([Point(5, 5), Point(5, 5)])
        az = p.azimuth_at_pk(0)
        assert az == 0.0

    def test_normal_on_zero_length(self):
        p = Polyline([Point(5, 5), Point(5, 5)])
        n = p.normal_at_pk(0)
        assert n.almost_equal(Vector(0, 0))

    def test_negative_coordinates(self):
        p = Polyline([Point(-100, -100), Point(0, 0), Point(100, 100)])
        assert p.length > 0
        assert p.bbox.xmin == -100.0

    def test_3d_points(self):
        p = Polyline([Point(0, 0, 0), Point(10, 0, 5), Point(20, 0, 10)])
        assert p.vertex_count == 3
        assert p.dimension == 1
        assert abs(p.vertices[2].z - 10.0) < 1e-9

    def test_many_vertices(self):
        pts = [Point(i * 10, i * 10) for i in range(100)]
        p = Polyline(pts)
        assert p.vertex_count == 100
        assert p.segment_count == 99
        assert p.length > 0

    def test_many_vertices_point_at_pk(self):
        pts = [Point(i * 10, 0) for i in range(100)]
        p = Polyline(pts)
        pt = p.point_at_pk(495.0)
        assert pt.almost_equal(Point(495.0, 0, 0))

    def test_many_vertices_pk_of(self):
        pts = [Point(i * 10, 0) for i in range(100)]
        p = Polyline(pts)
        pk = p.pk_of(Point(505, 10))
        assert abs(float(pk) - 505.0) < 1e-6

    def test_large_coordinates(self):
        p = Polyline([
            Point(1000000, 2000000),
            Point(1000100, 2000100),
        ])
        assert p.length > 0

    def test_split_preserves_total_length(self, simple_poly):
        left, right = simple_poly.split(150)
        assert abs(left.length + right.length - simple_poly.length) < 1e-9

    def test_split_at_vertex(self, simple_poly):
        left, right = simple_poly.split(100)
        assert left.length == 100.0
        assert right.length == 100.0

    def test_from_dict_missing_closed(self):
        data = {
            "vertices": [
                {"x": 0.0, "y": 0.0, "z": 0.0},
                {"x": 10.0, "y": 0.0, "z": 0.0},
            ],
        }
        p = Polyline.from_dict(data)
        assert p.closed is False

    def test_from_dict_empty_vertices(self):
        with pytest.raises(GeometryError):
            Polyline.from_dict({"vertices": []})

    def test_from_segments_returns_correct_type(self):
        segs = [Segment(Point(0, 0), Point(10, 0))]
        p = Polyline.from_segments(segs)
        assert isinstance(p, Polyline)

    def test_split_point_coincident(self):
        p = Polyline([Point(0, 0), Point(100, 0)])
        with pytest.raises(GeometryError):
            p.split(p.length)

    def test_closest_point_far_away(self, simple_poly):
        cp = simple_poly.closest_point(Point(9999, 9999))
        assert cp == simple_poly.end

    def test_project_far_away(self, simple_poly):
        proj = simple_poly.project(Point(9999, 9999))
        assert isinstance(proj, Point)

    def test_append_updates_cumulative_lengths(self, simple_poly):
        old_cum = list(simple_poly.cumulative_lengths)
        simple_poly.append(Point(200, 200))
        new_cum = simple_poly.cumulative_lengths
        assert len(new_cum) == len(old_cum) + 1
        assert new_cum[-1] > old_cum[-1]

    def test_is_valid_after_append(self, simple_poly):
        simple_poly.append(Point(200, 200))
        assert simple_poly.is_valid is True

    def test_length_after_extend(self, simple_poly):
        old_len = simple_poly.length
        simple_poly.extend([Point(200, 200), Point(300, 200)])
        assert simple_poly.length > old_len

    def test_cached_property_independence(self):
        p1 = Polyline([Point(0, 0), Point(10, 0)])
        p2 = Polyline([Point(0, 0), Point(20, 0)])
        assert p1.length == 10.0
        assert p2.length == 20.0

    def test_multiple_extend(self):
        p = Polyline([Point(0, 0), Point(10, 0)])
        p.extend([Point(20, 0)])
        p.extend([Point(30, 0)])
        p.extend([Point(40, 0)])
        assert p.vertex_count == 5

    def test_pk_of_from_segments(self):
        segs = [Segment(Point(0, 0), Point(50, 0)), Segment(Point(50, 0), Point(50, 50))]
        p = Polyline.from_segments(segs)
        pk = p.pk_of(Point(50, 25))
        assert abs(float(pk) - 75.0) < 1e-9

    def test_point_at_pk_to_dict_roundtrip(self):
        pts = [Point(1, 2), Point(3, 4), Point(5, 6)]
        p1 = Polyline(pts)
        d = p1.to_dict()
        p2 = Polyline.from_dict(d)
        for pk_val in [0, p1.length / 2, p1.length]:
            pt1 = p1.point_at_pk(pk_val)
            pt2 = p2.point_at_pk(pk_val)
            assert pt1.almost_equal(pt2)

    def test_normal_at_pk_unit_length(self):
        p = Polyline([Point(0, 0), Point(10, 0)])
        for pk_val in [0, 5, 10]:
            n = p.normal_at_pk(pk_val)
            assert abs(n.length - 1.0) < 1e-9

    def test_azimuth_at_pk_diagonal(self):
        p = Polyline([Point(0, 0), Point(10, 10)])
        az = p.azimuth_at_pk(5)
        assert abs(az - 45.0) < 1e-9

    def test_azimuth_at_pk_horizontal(self):
        p = Polyline([Point(0, 0), Point(10, 0)])
        az = p.azimuth_at_pk(5)
        assert abs(az) < 1e-9

    def test_azimuth_at_pk_vertical(self):
        p = Polyline([Point(0, 0), Point(0, 10)])
        az = p.azimuth_at_pk(5)
        assert abs(az - 90.0) < 1e-9


# ======================================================================
#  GOLDEN TEST
# ======================================================================


class TestGolden:
    def test_golden_file(self, utm_poly):
        import json as _json
        import os

        golden_path = os.path.join(
            os.path.dirname(__file__), "..", "golden", "polyline_utm.json"
        )
        with open(golden_path) as f:
            golden = _json.load(f)

        p = utm_poly

        assert abs(p.length - golden["length"]) < 1e-6
        assert p.vertex_count == golden["vertex_count"]
        assert p.segment_count == golden["segment_count"]
        assert abs(p.bbox.xmin - golden["bb_xmin"]) < 1e-6
        assert abs(p.bbox.ymin - golden["bb_ymin"]) < 1e-6
        assert abs(p.bbox.xmax - golden["bb_xmax"]) < 1e-6
        assert abs(p.bbox.ymax - golden["bb_ymax"]) < 1e-6
        assert p.start == Point.from_dict(golden["start"])
        assert p.end == Point.from_dict(golden["end"])
        assert p.center.almost_equal(Point.from_dict(golden["center"]))
        assert p.dimension == golden["dimension"]
        assert p.is_empty == golden["is_empty"]
        assert p.is_valid == golden["is_valid"]

        d = p.to_dict()
        assert d == golden["to_dict"]

        wkt = p.to_wkt()
        assert wkt == golden["to_wkt"]

        pt0 = p.point_at_pk(0)
        assert pt0 == Point.from_dict(golden["point_at_pk_0"])

        pt_len = p.point_at_pk(p.length)
        assert pt_len == Point.from_dict(golden["point_at_pk_length"])

        mid_pk = golden["length"] / 2
        pt_mid = p.point_at_pk(mid_pk)
        golden_mid = Point.from_dict(golden["point_at_pk_mid"])
        assert pt_mid.almost_equal(golden_mid)

        az0 = p.azimuth_at_pk(0)
        assert abs(az0 - golden["azimuth_at_pk_0"]) < 1e-6

        mid_az_pk = (golden["length"] / 2) + 1
        az_mid = p.azimuth_at_pk(mid_az_pk)
        assert abs(az_mid - golden["azimuth_at_pk_mid"]) < 1e-6

        pk_mid = p.pk_of(Point.from_dict(golden["point_at_pk_mid"]))
        assert abs(float(pk_mid) - golden["pk_of_mid"]) < 1e-3

        assert repr(p) == golden["repr"]
