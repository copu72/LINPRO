"""Tests GEOM-OPS-003: Parallelism."""


from linpro.geometry import Point, Segment, Vector
from linpro.geometry.operators import is_parallel


class TestParallelism:
    def test_vectors_parallel_same_dir(self):
        assert is_parallel(Vector(2, 0), Vector(5, 0)) is True

    def test_vectors_parallel_opposite(self):
        assert is_parallel(Vector(2, 0), Vector(-3, 0)) is True

    def test_vectors_not_parallel(self):
        assert is_parallel(Vector(1, 0), Vector(0, 1)) is False

    def test_zero_vector(self):
        assert is_parallel(Vector(0, 0), Vector(1, 0)) is True

    def test_segments_parallel(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 5), Point(10, 5))
        assert is_parallel(s1, s2) is True

    def test_segments_not_parallel(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 0), Point(0, 10))
        assert is_parallel(s1, s2) is False

    def test_vector_3d_parallel(self):
        assert is_parallel(Vector(2, 4, 6), Vector(1, 2, 3)) is True

    def test_vector_3d_not_parallel(self):
        assert is_parallel(Vector(1, 0, 0), Vector(0, 1, 0)) is False

    def test_near_parallel_within_tol(self):
        assert is_parallel(Vector(1000, 0), Vector(1000, 1e-6), tol=1e-3) is True

    def test_near_parallel_outside_tol(self):
        assert is_parallel(Vector(1, 0), Vector(1, 0.1), tol=1e-9) is False
