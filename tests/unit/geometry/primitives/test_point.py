"""Tests GEOM-001: Point."""

import math
from linpro.geometry.primitives.point import Point


class TestPoint:
    def test_creacion(self):
        p = Point(3.0, 4.0)
        assert p.x == 3.0
        assert p.y == 4.0

    def test_xy(self):
        p = Point(1, 2)
        assert p.xy == (1.0, 2.0)

    def test_distance_to(self):
        a = Point(0, 0)
        b = Point(3, 4)
        assert math.isclose(a.distance_to(b), 5.0)

    def test_distance_to_cero(self):
        a = Point(1, 1)
        b = Point(1, 1)
        assert a.distance_to(b) == 0.0

    def test_midpoint(self):
        a = Point(0, 0)
        b = Point(4, 6)
        m = a.midpoint(b)
        assert m.x == 2.0
        assert m.y == 3.0

    def test_translate(self):
        p = Point(1, 2).translate(3, 4)
        assert p.x == 4.0
        assert p.y == 6.0

    def test_rotate_90(self):
        p = Point(1, 0).rotate(math.pi / 2)
        assert math.isclose(p.x, 0.0, abs_tol=1e-10)
        assert math.isclose(p.y, 1.0, abs_tol=1e-10)

    def test_rotate_alrededor_de_centro(self):
        p = Point(2, 0).rotate(math.pi / 2, Point(1, 0))
        assert math.isclose(p.x, 1.0, abs_tol=1e-10)
        assert math.isclose(p.y, 1.0, abs_tol=1e-10)

    def test_scale(self):
        p = Point(1, 2).scale(2.0)
        assert p.x == 2.0
        assert p.y == 4.0

    def test_scale_con_centro(self):
        p = Point(2, 2).scale(2.0, Point(1, 1))
        assert p.x == 3.0
        assert p.y == 3.0

    def test_normalize(self):
        p = Point(3, 0).normalize()
        assert math.isclose(p.x, 1.0)
        assert math.isclose(p.y, 0.0)

    def test_normalize_cero(self):
        p = Point(0, 0).normalize()
        assert p.x == 0.0
        assert p.y == 0.0

    def test_dot(self):
        a = Point(1, 0)
        b = Point(0, 1)
        assert a.dot(b) == 0.0

    def test_cross(self):
        a = Point(1, 0)
        b = Point(0, 1)
        assert a.cross(b) == 1.0

    def test_add(self):
        r = Point(1, 2) + Point(3, 4)
        assert r.x == 4.0
        assert r.y == 6.0

    def test_sub(self):
        r = Point(5, 7) - Point(2, 3)
        assert r.x == 3.0
        assert r.y == 4.0

    def test_mul(self):
        r = Point(2, 3) * 2.5
        assert r.x == 5.0
        assert r.y == 7.5

    def test_eq(self):
        assert Point(1, 2) == Point(1.0, 2.0)
        assert Point(1, 2) != Point(3, 4)

    def test_eq_close(self):
        assert Point(0.0, 0.0) == Point(0.0, 0.0)

    def test_repr(self):
        r = repr(Point(1.5, 2.5))
        assert "Point" in r
        assert "1.500" in r

    def test_hash(self):
        s = {Point(1, 2), Point(1, 2), Point(3, 4)}
        assert len(s) == 2