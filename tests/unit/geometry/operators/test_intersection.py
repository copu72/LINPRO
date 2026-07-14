"""Tests GEOM-OPS-008: Intersection."""

import pytest

from linpro.geometry import Point, Segment
from linpro.geometry.operators import intersection_point, intersects


class TestIntersects:
    def test_cross_at_center(self):
        s1 = Segment(Point(0, 0), Point(10, 10))
        s2 = Segment(Point(0, 10), Point(10, 0))
        assert intersects(s1, s2) is True

    def test_cross_at_endpoint(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(10, 0), Point(10, 10))
        assert intersects(s1, s2) is True

    def test_parallel(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 5), Point(10, 5))
        assert intersects(s1, s2) is False

    def test_collinear_overlapping(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, 0), Point(15, 0))
        assert intersects(s1, s2) is True

    def test_collinear_separated(self):
        s1 = Segment(Point(0, 0), Point(5, 0))
        s2 = Segment(Point(10, 0), Point(15, 0))
        assert intersects(s1, s2) is False

    def test_t_shape(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, -5), Point(5, 0))
        assert intersects(s1, s2) is True

    def test_no_intersection(self):
        s1 = Segment(Point(0, 0), Point(5, 5))
        s2 = Segment(Point(6, 0), Point(10, 5))
        assert intersects(s1, s2) is False

    def test_returns_bool(self):
        s1 = Segment(Point(0, 0), Point(1, 1))
        s2 = Segment(Point(0, 1), Point(1, 0))
        assert isinstance(intersects(s1, s2), bool)


class TestIntersectionPoint:
    def test_cross_at_center(self):
        s1 = Segment(Point(0, 0), Point(10, 10))
        s2 = Segment(Point(0, 10), Point(10, 0))
        ip = intersection_point(s1, s2)
        assert ip == Point(5, 5)

    def test_cross_at_endpoint(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(10, 0), Point(10, 10))
        ip = intersection_point(s1, s2)
        assert ip == Point(10, 0)

    def test_no_intersection(self):
        s1 = Segment(Point(0, 0), Point(5, 5))
        s2 = Segment(Point(6, 0), Point(10, 5))
        assert intersection_point(s1, s2) is None

    def test_collinear_overlapping(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, 0), Point(15, 0))
        ip = intersection_point(s1, s2)
        assert ip is not None
        assert ip.x == pytest.approx(7.5)
        assert ip.y == pytest.approx(0.0)

    def test_t_shape(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, -5), Point(5, 0))
        ip = intersection_point(s1, s2)
        assert ip == Point(5, 0)

    def test_returns_none_type(self):
        s1 = Segment(Point(0, 0), Point(1, 0))
        s2 = Segment(Point(2, 0), Point(3, 0))
        assert intersection_point(s1, s2) is None

    def test_point_on_segment(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, -5), Point(5, 5))
        ip = intersection_point(s1, s2)
        assert ip == Point(5, 0)

    def test_end_on_other_segment(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(10, -5), Point(10, 5))
        assert intersects(s1, s2) is True
        assert intersection_point(s1, s2) == Point(10, 0)

    def test_collinear_overlap_center(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(4, 0), Point(6, 0))
        assert intersects(s1, s2) is True
        ip = intersection_point(s1, s2)
        assert ip is not None
        assert ip.y == pytest.approx(0.0)

    def test_no_collinear_intersection(self):
        s1 = Segment(Point(0, 0), Point(5, 0))
        s2 = Segment(Point(10, 0), Point(15, 0))
        ip = intersection_point(s1, s2)
        assert ip is None

    def test_start_on_other_segment(self):
        s1 = Segment(Point(5, 0), Point(15, 0))
        s2 = Segment(Point(0, 0), Point(10, 0))
        assert intersects(s1, s2) is True
        ip = intersection_point(s1, s2)
        assert ip is not None

    def test_collinear_touching_at_point(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(10, 0), Point(20, 0))
        assert intersects(s1, s2) is True
        ip = intersection_point(s1, s2)
        assert ip == Point(10, 0)

    def test_start_on_other_interior(self):
        s1 = Segment(Point(5, 0), Point(15, 5))
        s2 = Segment(Point(0, 0), Point(10, 0))
        assert intersects(s1, s2) is True
        ip = intersection_point(s1, s2)
        assert ip == Point(5, 0)
