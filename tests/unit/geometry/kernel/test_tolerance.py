"""Tests for Tolerance class — GEOM-002."""

import math
from linpro.geometry.kernel.tolerance import Tolerance, ToleranceLevel


class TestToleranceLevel:
    def test_math_epsilon(self):
        assert Tolerance.math.epsilon == 1e-12

    def test_geometry_epsilon(self):
        assert Tolerance.geometry.epsilon == 1e-9

    def test_visual_epsilon(self):
        assert Tolerance.visual.epsilon == 1e-6

    def test_math_equals_exact(self):
        assert Tolerance.math.equals(1.0, 1.0) is True

    def test_math_equals_within(self):
        assert Tolerance.math.equals(1.0, 1.0000000000001) is True

    def test_math_equals_beyond(self):
        assert Tolerance.math.equals(1.0, 1.0000001) is False

    def test_geometry_equals_within(self):
        assert Tolerance.geometry.equals(1.0, 1.0000000005) is True

    def test_geometry_equals_near_limit(self):
        assert Tolerance.geometry.equals(1.0, 1.0000000009) is True

    def test_geometry_equals_beyond(self):
        assert Tolerance.geometry.equals(1.0, 1.00001) is False

    def test_visual_equals_wide(self):
        assert Tolerance.visual.equals(1.0, 1.000001) is True

    def test_visual_equals_wide(self):
        assert Tolerance.visual.equals(1.0, 1.000001) is True

    def test_is_zero_true(self):
        assert Tolerance.math.is_zero(1e-13) is True
        assert Tolerance.geometry.is_zero(1e-10) is True

    def test_is_zero_false(self):
        assert Tolerance.geometry.is_zero(1e-8) is False

    def test_is_zero_exact(self):
        assert Tolerance.geometry.is_zero(0.0) is True

    def test_distance_equals(self):
        assert Tolerance.geometry.distance_equals(1000.0, 1000.000001) is True
        assert Tolerance.geometry.distance_equals(1000.0, 1000.1) is False

    def test_angle_equals(self):
        assert Tolerance.geometry.angle_equals(math.pi, math.pi) is True
        assert Tolerance.geometry.angle_equals(math.pi, math.pi + 1e-11) is True

    def test_less_or_equal(self):
        assert Tolerance.geometry.less_or_equal(5.0, 5.0) is True
        assert Tolerance.geometry.less_or_equal(5.0, 5.0 + 1e-10) is True
        assert Tolerance.geometry.less_or_equal(5.0, 4.0) is False

    def test_greater_or_equal(self):
        assert Tolerance.geometry.greater_or_equal(5.0, 5.0) is True
        assert Tolerance.geometry.greater_or_equal(5.0, 5.0 - 1e-10) is True
        assert Tolerance.geometry.greater_or_equal(5.0, 6.0) is False

    def test_in_range(self):
        assert Tolerance.geometry.in_range(5.0, 0.0, 10.0) is True
        assert Tolerance.geometry.in_range(5.0, 5.0, 5.0) is True
        assert Tolerance.geometry.in_range(11.0, 0.0, 10.0) is False

    def test_repr(self):
        r = repr(Tolerance.math)
        assert "ToleranceLevel" in r
        assert "1e-12" in r


class TestToleranceClassConvenience:
    def test_equals_delegates_to_geometry(self):
        assert Tolerance.equals(1.0, 1.0) is True
        assert Tolerance.equals(1.0, 1.0000000009) is True

    def test_is_zero_delegates(self):
        assert Tolerance.is_zero(0.0) is True
        assert Tolerance.is_zero(1e-10) is True

    def test_distance_equals_delegates(self):
        assert Tolerance.distance_equals(100.0, 100.0) is True

    def test_angle_equals_delegates(self):
        assert Tolerance.angle_equals(0.0, 0.0) is True

    def test_less_or_equal_delegates(self):
        assert Tolerance.less_or_equal(5.0, 5.0) is True

    def test_greater_or_equal_delegates(self):
        assert Tolerance.greater_or_equal(5.0, 5.0) is True

    def test_in_range_delegates(self):
        assert Tolerance.in_range(5.0, 0.0, 10.0) is True
