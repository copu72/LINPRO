"""Tests for NumericValidator, CoordinateValidator, GeometryValidator."""

import pytest
from linpro.geometry.kernel.validation import (
    NumericValidator,
    CoordinateValidator,
    GeometryValidator,
)
from linpro.geometry.exceptions import InvalidCoordinateError, ValidationError
from linpro.geometry import Point


class TestNumericValidator:
    def test_assert_finite_float(self):
        NumericValidator.assert_finite(42.0)

    def test_assert_finite_int(self):
        NumericValidator.assert_finite(42)

    def test_assert_finite_nan_raises(self):
        with pytest.raises(InvalidCoordinateError):
            NumericValidator.assert_finite(float("nan"))

    def test_assert_finite_inf_raises(self):
        with pytest.raises(InvalidCoordinateError):
            NumericValidator.assert_finite(float("inf"))

    def test_assert_finite_string_raises(self):
        with pytest.raises(InvalidCoordinateError):
            NumericValidator.assert_finite("not a number")

    def test_assert_finite_none_raises(self):
        with pytest.raises(InvalidCoordinateError):
            NumericValidator.assert_finite(None)

    def test_is_finite_float(self):
        assert NumericValidator.is_finite(42.0) is True

    def test_is_finite_nan(self):
        assert NumericValidator.is_finite(float("nan")) is False

    def test_is_finite_inf(self):
        assert NumericValidator.is_finite(float("inf")) is False

    def test_is_finite_string(self):
        assert NumericValidator.is_finite("abc") is False

    def test_assert_positive_ok(self):
        NumericValidator.assert_positive(5.0)

    def test_assert_positive_zero(self):
        NumericValidator.assert_positive(0.0)

    def test_assert_positive_negative_raises(self):
        with pytest.raises(InvalidCoordinateError):
            NumericValidator.assert_positive(-1.0)

    def test_assert_range_ok(self):
        NumericValidator.assert_range(5.0, 0.0, 10.0)

    def test_assert_range_below_raises(self):
        with pytest.raises(InvalidCoordinateError):
            NumericValidator.assert_range(-1.0, 0.0, 10.0)

    def test_assert_range_above_raises(self):
        with pytest.raises(InvalidCoordinateError):
            NumericValidator.assert_range(11.0, 0.0, 10.0)


class TestCoordinateValidator:
    def test_assert_valid_2d(self):
        CoordinateValidator.assert_valid(100.0, 200.0)

    def test_assert_valid_3d(self):
        CoordinateValidator.assert_valid(100.0, 200.0, 50.0)

    def test_assert_valid_nan_raises(self):
        with pytest.raises(InvalidCoordinateError):
            CoordinateValidator.assert_valid(float("nan"), 0.0)

    def test_assert_2d_ok(self):
        CoordinateValidator.assert_2d(10.0, 20.0)

    def test_assert_2d_nan_raises(self):
        with pytest.raises(InvalidCoordinateError):
            CoordinateValidator.assert_2d(10.0, float("nan"))

    def test_assert_3d_ok(self):
        CoordinateValidator.assert_3d(1.0, 2.0, 3.0)

    def test_assert_3d_inf_raises(self):
        with pytest.raises(InvalidCoordinateError):
            CoordinateValidator.assert_3d(1.0, 2.0, float("inf"))


class TestGeometryValidator:
    def test_assert_type_ok(self):
        GeometryValidator.assert_type(Point(1, 2), Point)

    def test_assert_type_wrong_raises(self):
        with pytest.raises(ValidationError):
            GeometryValidator.assert_type("not a point", Point)

    def test_assert_not_none_ok(self):
        GeometryValidator.assert_not_none(Point(1, 2))

    def test_assert_not_none_none_raises(self):
        with pytest.raises(ValidationError):
            GeometryValidator.assert_not_none(None)
