"""Tests GEOM-OPS-007: Closest Point."""


from linpro.geometry import Point, Segment
from linpro.geometry.operators import closest_point


class TestClosestPoint:
    def test_inside_segment(self):
        s = Segment(Point(0, 0), Point(10, 0))
        cp = closest_point(Point(5, 5), s)
        assert cp == Point(5, 0)

    def test_before_start(self):
        s = Segment(Point(5, 0), Point(10, 0))
        cp = closest_point(Point(0, 0), s)
        assert cp == Point(5, 0)

    def test_after_end(self):
        s = Segment(Point(0, 0), Point(5, 0))
        cp = closest_point(Point(10, 0), s)
        assert cp == Point(5, 0)

    def test_on_segment(self):
        s = Segment(Point(0, 0), Point(10, 10))
        cp = closest_point(Point(3, 3), s)
        assert cp == Point(3, 3)

    def test_at_start(self):
        s = Segment(Point(5, 5), Point(10, 10))
        cp = closest_point(Point(0, 0), s)
        assert cp == Point(5, 5)

    def test_at_end(self):
        s = Segment(Point(0, 0), Point(10, 0))
        cp = closest_point(Point(15, 0), s)
        assert cp == Point(10, 0)

    def test_degenerate_segment(self):
        s = Segment(Point(3, 4), Point(3, 4))
        cp = closest_point(Point(0, 0), s)
        assert cp == Point(3, 4)

    def test_3d_projection(self):
        s = Segment(Point(0, 0, 0), Point(10, 0, 0))
        cp = closest_point(Point(5, 5, 5), s)
        assert cp == Point(5, 0, 0)

    def test_distance_zero(self):
        s = Segment(Point(0, 0), Point(10, 0))
        cp = closest_point(Point(3, 0), s)
        assert cp == Point(3, 0)

    def test_vertical_segment(self):
        s = Segment(Point(5, 0), Point(5, 10))
        cp = closest_point(Point(5, 15), s)
        assert cp == Point(5, 10)
