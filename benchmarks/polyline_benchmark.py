"""Benchmark: Polyline / PK Engine.

Mide rendimiento de operaciones críticas del Engineering Axis.
"""

import math
import timeit

from linpro.geometry import PK, Point, Polyline


def _make_axis(n: int) -> Polyline:
    pts = [Point(i * 100.0, math.sin(i * 0.1) * 100.0) for i in range(n)]
    return Polyline(pts)


def bench_creation():
    _make_axis(100)


def bench_length():
    a = _make_axis(100)
    a.length


def bench_bbox():
    a = _make_axis(100)
    a.bbox


def bench_point_at_pk():
    a = _make_axis(100)
    pk = PK(a.length / 2)
    a.point_at_pk(pk)


def bench_pk_of():
    a = _make_axis(100)
    pt = a.point_at_pk(a.length / 2)
    a.pk_of(pt)


def bench_closest_point():
    a = _make_axis(100)
    p = Point(5000.0, 50.0)
    a.closest_point(p)


def bench_to_wkt():
    a = _make_axis(100)
    a.to_wkt()


def bench_to_dict():
    a = _make_axis(100)
    a.to_dict()


if __name__ == "__main__":
    n = 1000
    for name in [
        "creation",
        "length",
        "bbox",
        "point_at_pk",
        "pk_of",
        "closest_point",
        "to_wkt",
        "to_dict",
    ]:
        fn = globals()[f"bench_{name}"]
        t = timeit.timeit(fn, number=n)
        print(f"  {name:20s}  {t/n*1e6:8.2f} µs  ({n} runs)")
