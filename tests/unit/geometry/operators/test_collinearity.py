"""Tests GEOM-OPS-002: Collinearity."""


from linpro.geometry import Point
from linpro.geometry.operators import is_collinear


class TestCollinearity:
    def test_collinear_horizontal(self):
        assert is_collinear(Point(0, 0), Point(1, 0), Point(2, 0)) is True

    def test_collinear_vertical(self):
        assert is_collinear(Point(0, 0), Point(0, 1), Point(0, 2)) is True

    def test_collinear_diagonal(self):
        assert is_collinear(Point(0, 0), Point(1, 1), Point(2, 2)) is True

    def test_not_collinear(self):
        assert is_collinear(Point(0, 0), Point(1, 0), Point(0, 1)) is False

    def test_coincident_a_b(self):
        assert is_collinear(Point(1, 1), Point(1, 1), Point(2, 3)) is True

    def test_all_coincident(self):
        assert is_collinear(Point(1, 1), Point(1, 1), Point(1, 1)) is True

    def test_near_collinear_within_tol(self):
        assert is_collinear(Point(0, 0), Point(1000, 0), Point(2000, 1e-6), tol=1e-2) is True

    def test_near_collinear_outside_tol(self):
        assert is_collinear(Point(0, 0), Point(1, 0), Point(2, 0.1), tol=1e-9) is False

    def test_3d_same_z(self):
        assert is_collinear(Point(0, 0, 5), Point(1, 1, 5), Point(2, 2, 5)) is True

    def test_3d_diff_z(self):
        assert is_collinear(Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 2)) is True
