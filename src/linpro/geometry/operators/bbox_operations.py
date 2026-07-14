"""GEOM-OPS-009: BoundingBox Operations.

Convenience functions that delegate to BoundingBox methods.
"""

from linpro.geometry.primitives.bbox import BoundingBox
from linpro.geometry.primitives.point import Point


def bbox_intersects(a: BoundingBox, b: BoundingBox) -> bool:
    return a.intersects(b)


def bbox_contains_point(bb: BoundingBox, point: Point) -> bool:
    return bb.contains_point(point)


def bbox_contains_bbox(outer: BoundingBox, inner: BoundingBox) -> bool:
    return outer.contains_bbox(inner)


def bbox_union(a: BoundingBox, b: BoundingBox) -> BoundingBox:
    return a.union(b)


def bbox_intersection(a: BoundingBox, b: BoundingBox) -> BoundingBox | None:
    return a.intersection(b)
