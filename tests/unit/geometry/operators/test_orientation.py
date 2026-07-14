"""Tests GEOM-OPS-001: Orientation."""


from linpro.geometry import Point
from linpro.geometry.operators import orientation


class TestOrientation:
    def test_ccw(self):
        assert orientation(Point(0, 0), Point(1, 0), Point(0, 1)) > 0

    def test_cw(self):
        assert orientation(Point(0, 0), Point(0, 1), Point(1, 0)) < 0

    def test_collinear_horizontal(self):
        assert orientation(Point(0, 0), Point(1, 0), Point(2, 0)) == 0.0

    def test_collinear_vertical(self):
        assert orientation(Point(0, 0), Point(0, 1), Point(0, 2)) == 0.0

    def test_collinear_diagonal(self):
        assert orientation(Point(0, 0), Point(1, 1), Point(2, 2)) == 0.0

    def test_coincident_a_b(self):
        assert orientation(Point(1, 1), Point(1, 1), Point(2, 3)) == 0.0

    def test_all_coincident(self):
        assert orientation(Point(1, 1), Point(1, 1), Point(1, 1)) == 0.0

    def test_3d_ignores_z(self):
        assert orientation(Point(0, 0, 5), Point(1, 0, 5), Point(0, 1, 5)) > 0

    def test_near_collinear_within_tol(self):
        a = Point(0, 0)
        b = Point(1000, 0)
        c = Point(2000, 1e-6)
        assert orientation(a, b, c, tol=1e-2) == 0.0

    def test_near_collinear_outside_tol(self):
        a = Point(0, 0)
        b = Point(1, 0)
        c = Point(2, 0.1)
        assert orientation(a, b, c, tol=1e-9) != 0.0
