"""Tests GEOM-OPS-009: BoundingBox Operations."""


from linpro.geometry import BoundingBox, Point
from linpro.geometry.operators import (
    bbox_contains_bbox,
    bbox_contains_point,
    bbox_intersection,
    bbox_intersects,
    bbox_union,
)


class TestBBoxIntersects:
    def test_overlapping(self):
        a = BoundingBox(0, 0, 10, 10)
        b = BoundingBox(5, 5, 15, 15)
        assert bbox_intersects(a, b) is True

    def test_separated(self):
        a = BoundingBox(0, 0, 5, 5)
        b = BoundingBox(10, 10, 15, 15)
        assert bbox_intersects(a, b) is False

    def test_tangent(self):
        a = BoundingBox(0, 0, 10, 10)
        b = BoundingBox(10, 0, 20, 10)
        assert bbox_intersects(a, b) is True

    def test_identical(self):
        a = BoundingBox(0, 0, 10, 10)
        assert bbox_intersects(a, a) is True


class TestBBoxContainsPoint:
    def test_inside(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert bbox_contains_point(bb, Point(5, 5)) is True

    def test_outside(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert bbox_contains_point(bb, Point(15, 5)) is False

    def test_on_edge(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert bbox_contains_point(bb, Point(10, 5)) is True

    def test_on_corner(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert bbox_contains_point(bb, Point(0, 0)) is True


class TestBBoxContainsBBox:
    def test_contained(self):
        outer = BoundingBox(0, 0, 10, 10)
        inner = BoundingBox(2, 2, 8, 8)
        assert bbox_contains_bbox(outer, inner) is True

    def test_not_contained(self):
        outer = BoundingBox(0, 0, 10, 10)
        inner = BoundingBox(-1, -1, 11, 11)
        assert bbox_contains_bbox(outer, inner) is False

    def test_identical(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert bbox_contains_bbox(bb, bb) is True


class TestBBoxUnion:
    def test_separated(self):
        a = BoundingBox(0, 0, 5, 5)
        b = BoundingBox(10, 10, 15, 15)
        u = bbox_union(a, b)
        assert u == BoundingBox(0, 0, 15, 15)

    def test_overlapping(self):
        a = BoundingBox(0, 0, 10, 10)
        b = BoundingBox(5, 5, 15, 15)
        u = bbox_union(a, b)
        assert u == BoundingBox(0, 0, 15, 15)

    def test_identical(self):
        a = BoundingBox(0, 0, 10, 10)
        u = bbox_union(a, a)
        assert u == a


class TestBBoxIntersection:
    def test_overlapping(self):
        a = BoundingBox(0, 0, 10, 10)
        b = BoundingBox(5, 5, 15, 15)
        i = bbox_intersection(a, b)
        assert i == BoundingBox(5, 5, 10, 10)

    def test_separated(self):
        a = BoundingBox(0, 0, 5, 5)
        b = BoundingBox(10, 10, 15, 15)
        assert bbox_intersection(a, b) is None

    def test_identical(self):
        a = BoundingBox(0, 0, 10, 10)
        i = bbox_intersection(a, a)
        assert i == a

    def test_contained(self):
        outer = BoundingBox(0, 0, 10, 10)
        inner = BoundingBox(2, 2, 8, 8)
        i = bbox_intersection(outer, inner)
        assert i == inner
