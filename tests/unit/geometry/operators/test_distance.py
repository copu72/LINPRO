"""Tests GEOM-OPS-005: Distance."""

import math

import pytest

from linpro.geometry import BoundingBox, Point, Segment
from linpro.geometry.operators import distance


class TestDistancePointPoint:
    def test_separated(self):
        d = distance(Point(0, 0), Point(3, 4))
        assert d == pytest.approx(5.0)

    def test_coincident(self):
        assert distance(Point(1, 2), Point(1, 2)) == 0.0

    def test_3d(self):
        d = distance(Point(0, 0, 0), Point(2, 3, 6))
        assert d == pytest.approx(7.0)

    def test_negative_coords(self):
        d = distance(Point(-1, -1), Point(2, 3))
        assert d == pytest.approx(5.0)


class TestDistancePointSegment:
    def test_point_on_segment(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert distance(Point(5, 0), s) == 0.0

    def test_point_off_segment_perpendicular(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert distance(Point(5, 3), s) == pytest.approx(3.0)

    def test_point_beyond_start(self):
        s = Segment(Point(5, 0), Point(10, 0))
        d = distance(Point(0, 0), s)
        assert d == pytest.approx(5.0)

    def test_point_beyond_end(self):
        s = Segment(Point(0, 0), Point(5, 0))
        d = distance(Point(10, 0), s)
        assert d == pytest.approx(5.0)

    def test_degenerate_segment(self):
        s = Segment(Point(3, 4), Point(3, 4))
        assert distance(Point(0, 0), s) == pytest.approx(5.0)

    def test_reverse_order(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert distance(s, Point(5, 3)) == pytest.approx(3.0)


class TestDistanceSegmentSegment:
    def test_intersecting(self):
        s1 = Segment(Point(0, 0), Point(10, 10))
        s2 = Segment(Point(0, 10), Point(10, 0))
        assert distance(s1, s2) == 0.0

    def test_parallel_separated(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 5), Point(10, 5))
        assert distance(s1, s2) == pytest.approx(5.0)

    def test_collinear_separated(self):
        s1 = Segment(Point(0, 0), Point(5, 0))
        s2 = Segment(Point(10, 0), Point(15, 0))
        assert distance(s1, s2) == pytest.approx(5.0)

    def test_colinear_overlapping(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, 0), Point(15, 0))
        assert distance(s1, s2) == 0.0


class TestDistancePointBBox:
    def test_point_inside(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert distance(Point(5, 5), bb) == 0.0

    def test_point_outside(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert distance(Point(15, 5), bb) == pytest.approx(5.0)

    def test_point_on_edge(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert distance(Point(10, 5), bb) == 0.0

    def test_point_diagonal_outside(self):
        bb = BoundingBox(0, 0, 10, 10)
        d = distance(Point(15, 15), bb)
        assert d == pytest.approx(math.sqrt(50))

    def test_reverse_order(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert distance(bb, Point(15, 5)) == pytest.approx(5.0)


class TestDistanceErrors:
    def test_type_error_vector(self):
        from linpro.geometry import Vector
        with pytest.raises(TypeError):
            distance(Point(0, 0), Vector(1, 0))
