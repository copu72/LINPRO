"""Tests for Geometry abstract base class."""

import json
import pytest
from linpro.geometry.kernel.geometry import Geometry


class TestGeometryAbstract:
    def test_cannot_instantiate_geometry(self):
        with pytest.raises(TypeError):
            Geometry()  # type: ignore

    def test_geometry_is_abstract(self):
        import abc
        assert issubclass(Geometry, abc.ABC)

    def test_geometry_has_epsilon_classvar(self):
        assert Geometry._EPSILON == 1e-9

    def test_to_json_concrete_implementation(self):
        """Verify to_json/from_json logic via the abstract class contract."""
        from linpro.geometry import Point
        p = Point(10.0, 20.0)
        json_str = p.to_json()
        restored = Point.from_json(json_str)
        assert restored == p

    def test_from_json_parse(self):
        from linpro.geometry import Point
        data = '{"x": 1.0, "y": 2.0, "z": 3.0}'
        p = Point.from_json(data)
        assert isinstance(p, Point)
        assert p.x == 1.0 and p.y == 2.0 and p.z == 3.0

    def test_str_equals_repr_on_concrete(self):
        from linpro.geometry import Point
        p = Point(1.5, 2.5)
        assert str(p) == repr(p)
