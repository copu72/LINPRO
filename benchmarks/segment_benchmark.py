"""Benchmark TASK-0005B: Segment — línea base de rendimiento.

Ejecutar con: pytest benchmarks/segment_benchmark.py --benchmark-only -v
"""

from linpro.geometry import Point, Segment

NUM = 100_000


class TestSegmentBenchmark:
    def test_bench_creation(self, benchmark):
        def create():
            for i in range(NUM):
                Segment(Point(i, 0), Point(i + 1000, 500))
        benchmark(create)

    def test_bench_length(self, benchmark):
        s = Segment(Point(0, 0), Point(1000, 500))
        def run():
            for _ in range(NUM):
                _ = s.length
        benchmark(run)

    def test_bench_azimuth(self, benchmark):
        s = Segment(Point(0, 0), Point(1000, 500))
        def run():
            for _ in range(NUM):
                _ = s.azimuth
        benchmark(run)

    def test_bench_reverse(self, benchmark):
        s = Segment(Point(0, 0), Point(1000, 500))
        def run():
            for _ in range(NUM):
                s.reverse()
        benchmark(run)

    def test_bench_project(self, benchmark):
        s = Segment(Point(0, 0), Point(1000, 0))
        p = Point(500, 300)
        def run():
            for _ in range(NUM):
                s.project(p)
        benchmark(run)

    def test_bench_distance(self, benchmark):
        s = Segment(Point(0, 0), Point(1000, 0))
        p = Point(500, 300)
        def run():
            for _ in range(NUM):
                s.distance_to(p)
        benchmark(run)

    def test_bench_vector(self, benchmark):
        s = Segment(Point(0, 0), Point(1000, 500))
        def run():
            for _ in range(NUM):
                _ = s.vector
        benchmark(run)
