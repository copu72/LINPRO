"""Tests para ClassName."""

import math
import pytest
from linpro.geometry import ClassName
from linpro.geometry.exceptions import GeometryError, InvalidCoordinateError


class TestClassNameCreation:
    def test_creacion_basica(self):
        obj = ClassName(1.0, 2.0)
        assert obj.param1 == 1.0


class TestClassNameMethods:
    def test_some_method(self):
        obj = ClassName(1.0, 2.0)
        assert obj.some_method(ClassName(3.0, 4.0)) >= 0.0


class TestClassNameSerializacion:
    def test_to_dict(self):
        d = ClassName(1.0, 2.0).to_dict()
        assert "param1" in d

    def test_from_dict(self):
        obj = ClassName.from_dict({"param1": 1.0, "param2": 2.0})
        assert obj.param1 == 1.0


class TestClassNameValidacion:
    def test_nan_raise(self):
        with pytest.raises(InvalidCoordinateError):
            ClassName(float("nan"), 2.0)


class TestClassNameIgualdad:
    def test_eq(self):
        assert ClassName(1.0, 2.0) == ClassName(1.0, 2.0)

    def test_almost_equal(self):
        assert ClassName(1.0, 2.0).almost_equal(ClassName(1.000000001, 2.0))


class TestClassNameInvariantes:
    def test_check_invariants(self):
        ClassName(1.0, 2.0).check_invariants()
