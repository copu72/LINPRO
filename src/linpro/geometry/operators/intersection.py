"""GEOM-OPS-008: Intersection.

intersects(seg1, seg2) → bool
intersection_point(seg1, seg2) → Point | None
"""


from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.operators.orientation import orientation
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.segment import Segment


def intersects(s1: Segment, s2: Segment, tol: float = EPSILON_GEOMETRY) -> bool:
    o1 = orientation(s1.start, s1.end, s2.start, tol)
    o2 = orientation(s1.start, s1.end, s2.end, tol)
    o3 = orientation(s2.start, s2.end, s1.start, tol)
    o4 = orientation(s2.start, s2.end, s1.end, tol)

    if o1 * o2 < 0 and o3 * o4 < 0:
        return True

    if o1 == 0 and _on_segment(s1, s2.start, tol):
        return True
    if o2 == 0 and _on_segment(s1, s2.end, tol):
        return True
    if o3 == 0 and _on_segment(s2, s1.start, tol):
        return True
    if o4 == 0 and _on_segment(s2, s1.end, tol):
        return True

    return False


def intersection_point(s1: Segment, s2: Segment, tol: float = EPSILON_GEOMETRY) -> Point | None:
    if not intersects(s1, s2, tol):
        return None

    x1, y1 = s1.start.x, s1.start.y
    x2, y2 = s1.end.x, s1.end.y
    x3, y3 = s2.start.x, s2.start.y
    x4, y4 = s2.end.x, s2.end.y

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) <= tol:
        return _collinear_intersection(s1, s2, tol)

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    px = x1 + t * (x2 - x1)
    py = y1 + t * (y2 - y1)
    return Point(px, py)


def _on_segment(s: Segment, p: Point, tol: float = EPSILON_GEOMETRY) -> bool:
    if min(s.start.x, s.end.x) - tol <= p.x <= max(s.start.x, s.end.x) + tol:
        if min(s.start.y, s.end.y) - tol <= p.y <= max(s.start.y, s.end.y) + tol:
            return True
    return False


def _collinear_intersection(s1: Segment, s2: Segment, tol: float = EPSILON_GEOMETRY) -> Point | None:
    pts = []
    for p in (s1.start, s1.end, s2.start, s2.end):
        if _on_segment(s1, p, tol) and _on_segment(s2, p, tol):
            pts.append(p)
    if not pts:
        return None
    cx = sum(p.x for p in pts) / len(pts)
    cy = sum(p.y for p in pts) / len(pts)
    return Point(cx, cy)
