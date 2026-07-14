"""Tests GEOM-OPS-004: Perpendicularity."""


from linpro.geometry import Point, Segment, Vector
from linpro.geometry.operators import is_perpendicular


class TestPerpendicularity:
    def test_vectors_perpendicular(self):
        assert is_perpendicular(Vector(1, 0), Vector(0, 1)) is True

    def test_vectors_not_perpendicular(self):
        assert is_perpendicular(Vector(1, 0), Vector(1, 1)) is False

    def test_zero_vector(self):
        assert is_perpendicular(Vector(0, 0), Vector(1, 0)) is True

    def test_segments_perpendicular(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, -5), Point(5, 5))
        assert is_perpendicular(s1, s2) is True

    def test_segments_not_perpendicular(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 0), Point(10, 10))
        assert is_perpendicular(s1, s2) is False

    def test_3d_perpendicular(self):
        assert is_perpendicular(Vector(1, 0, 0), Vector(0, 1, 0)) is True

    def test_3d_not_perpendicular(self):
        assert is_perpendicular(Vector(1, 0, 0), Vector(1, 1, 0)) is False

    def test_self_not_perpendicular(self):
        assert is_perpendicular(Vector(1, 0), Vector(1, 0)) is False

    def test_near_perpendicular_within_tol(self):
        assert is_perpendicular(Vector(1000, 0), Vector(1e-6, 1000), tol=1e-3) is True
