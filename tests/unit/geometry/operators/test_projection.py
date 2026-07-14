"""Tests GEOM-OPS-006: Projection."""


from linpro.geometry import Point, Segment
from linpro.geometry.operators import project


class TestProjection:
    def test_point_midpoint(self):
        s = Segment(Point(0, 0), Point(10, 0))
        proj = project(Point(5, 5), s)
        assert proj == Point(5, 0)

    def test_at_start(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert project(Point(0, 5), s) == Point(0, 0)

    def test_beyond_end(self):
        s = Segment(Point(0, 0), Point(10, 0))
        proj = project(Point(15, 3), s)
        assert proj == Point(15, 0)

    def test_already_on_line(self):
        s = Segment(Point(0, 0), Point(10, 10))
        assert project(Point(3, 3), s) == Point(3, 3)

    def test_horizontal_segment(self):
        s = Segment(Point(5, 5), Point(15, 5))
        assert project(Point(10, 10), s) == Point(10, 5)

    def test_vertical_segment(self):
        s = Segment(Point(5, 0), Point(5, 10))
        assert project(Point(10, 5), s) == Point(5, 5)

    def test_diagonal_segment(self):
        s = Segment(Point(0, 0), Point(10, 10))
        proj = project(Point(5, 0), s)
        assert proj.almost_equal(Point(2.5, 2.5))

    def test_degenerate_segment(self):
        s = Segment(Point(3, 4), Point(3, 4))
        assert project(Point(0, 0), s) == Point(3, 4)

    def test_3d_projection(self):
        s = Segment(Point(0, 0, 0), Point(10, 0, 0))
        proj = project(Point(5, 5, 5), s)
        assert proj == Point(5, 0, 0)

    def test_perpendicular_from_start(self):
        s = Segment(Point(0, 0), Point(0, 10))
        assert project(Point(5, 0), s) == Point(0, 0)
