"""Benchmark GEOM-VEC: Vector — línea base de rendimiento.

Ejecutar con: pytest benchmarks/vector_benchmark.py --benchmark-only -v --benchmark-min-time=0.001
"""

import json
import math

from linpro.geometry import Vector

NUM_ITERATIONS = 1_000_000
SCALE = 1_000_000


class TestVectorBenchmark:
    def test_bench_creation_2d(self, benchmark):
        """Crear 1M vectores 2D."""
        def create():
            for i in range(NUM_ITERATIONS):
                Vector(i % SCALE, (i * 2) % SCALE)
        benchmark(create)

    def test_bench_creation_3d(self, benchmark):
        """Crear 1M vectores 3D."""
        def create():
            for i in range(NUM_ITERATIONS):
                Vector(i % SCALE, (i * 2) % SCALE, (i * 3) % SCALE)
        benchmark(create)

    def test_bench_dot_product(self, benchmark):
        """Producto escalar de 1M pares."""
        v1 = Vector(3.0, 4.0)
        v2 = Vector(5.0, 6.0)
        def dot():
            for _ in range(NUM_ITERATIONS):
                v1.dot(v2)
        benchmark(dot)

    def test_bench_normalized(self, benchmark):
        """Normalización de 1M vectores."""
        v = Vector(3.0, 4.0)
        def norm():
            for _ in range(NUM_ITERATIONS):
                v.normalized
        benchmark(norm)

    def test_bench_rotation(self, benchmark):
        """Rotación de 1M vectores."""
        v = Vector(3.0, 4.0)
        angle = math.pi / 4
        def rotate():
            for _ in range(NUM_ITERATIONS):
                v.rotate(angle)
        benchmark(rotate)

    def test_bench_json_serialization(self, benchmark):
        """Serialización JSON de 1M vectores."""
        v = Vector(123456.789, 987654.321)
        def serialize():
            for _ in range(NUM_ITERATIONS):
                json.dumps(v.to_dict())
        benchmark(serialize)

    def test_bench_length(self, benchmark):
        """Cálculo de magnitud de 1M vectores."""
        def lengths():
            for i in range(NUM_ITERATIONS):
                Vector(i % SCALE, (i * 3) % SCALE).length
        benchmark(lengths)
