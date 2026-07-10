"""Benchmark de ejemplo para el Geometry Engine.

Ejecutar con: python -m pytest benchmarks/ --benchmark-only -v
"""

import pytest
from linpro.geometry import Point


class BenchmarkPoint:
    def bench_distance_to(self, benchmark):
        p1 = Point(0, 0)
        p2 = Point(100000, 50000)
        result = benchmark(p1.distance_to, p2)
        assert result > 0

    def bench_creation(self, benchmark):
        result = benchmark(Point, 123456.789, 987654.321)
        assert result.x == 123456.789
