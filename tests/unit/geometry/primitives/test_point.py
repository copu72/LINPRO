"""Tests GEOM-010: Point — primitiva fundamental del Kernel Geometry."""

import json
import math
import pytest
from linpro.geometry import Point
from linpro.geometry.exceptions import GeometryError, InvalidCoordinateError


class TestPointCreation:
    def test_creacion_2d(self):
        p = Point(10.0, 20.0)
        assert p.x == 10.0
        assert p.y == 20.0
        assert p.z == 0.0

    def test_creacion_3d(self):
        p = Point(1.0, 2.0, 3.0)
        assert p.z == 3.0

    def test_creacion_enteros(self):
        p = Point(1, 2)
        assert isinstance(p.x, float)
        assert isinstance(p.y, float)

    def test_creacion_z_default_cero(self):
        p = Point(5, 5)
        assert p.z == 0.0


class TestPointInmutabilidad:
    def test_propiedades_solo_lectura(self):
        p = Point(1, 2)
        with pytest.raises(AttributeError):
            p.x = 3  # type: ignore
        with pytest.raises(AttributeError):
            p.y = 4  # type: ignore
        with pytest.raises(AttributeError):
            p.z = 5  # type: ignore


class TestPointDistance:
    def test_distance_2d(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        assert math.isclose(p1.distance_to(p2), 5.0)

    def test_distance_3d(self):
        p1 = Point(0, 0, 0)
        p2 = Point(2, 3, 6)
        dist = p1.distance_to(p2)
        assert math.isclose(dist, 7.0), f"Expected 7.0, got {dist}"

    def test_distance_mismo_punto(self):
        p = Point(1.5, 2.5, 3.5)
        assert p.distance_to(Point(1.5, 2.5, 3.5)) == 0.0


class TestPointIgualdad:
    def test_igualdad_exacta(self):
        assert Point(1.0, 2.0) == Point(1.0, 2.0)

    def test_igualdad_tolerancia(self):
        assert Point(1.0, 2.0) == Point(1.0000000005, 2.0)

    def test_igualdad_tolerancia_límite(self):
        tol = 1e-9
        assert Point(0, 0) == Point(tol / 2, 0)

    def test_desigualdad(self):
        assert Point(1, 2) != Point(3, 4)

    def test_no_igual_a_otro_tipo(self):
        assert Point(0, 0) != "POINT (0 0)"


class TestPointHash:
    def test_hash_mismo_punto(self):
        assert hash(Point(1, 2)) == hash(Point(1.0, 2.0))

    def test_hash_en_set(self):
        s = {Point(0, 0), Point(1, 1), Point(0, 0)}
        assert len(s) == 2


class TestPointSerializacion:
    def test_to_tuple(self):
        assert Point(1, 2, 3).to_tuple() == (1.0, 2.0, 3.0)

    def test_to_dict(self):
        d = Point(1, 2, 3).to_dict()
        assert d == {"x": 1.0, "y": 2.0, "z": 3.0}

    def test_to_json(self):
        s = Point(1, 2, 3).to_json()
        assert json.loads(s) == {"x": 1.0, "y": 2.0, "z": 3.0}

    def test_to_wkt(self):
        assert Point(10.5, 20.5).to_wkt() == "POINT (10.5 20.5)"

    def test_from_tuple_2(self):
        p = Point.from_tuple((3.0, 4.0))
        assert p.x == 3.0 and p.y == 4.0 and p.z == 0.0

    def test_from_tuple_3(self):
        p = Point.from_tuple((1, 2, 3))
        assert p.z == 3.0

    def test_from_dict(self):
        p = Point.from_dict({"x": 1.0, "y": 2.0})
        assert p.x == 1.0 and p.y == 2.0

    def test_from_dict_with_z(self):
        p = Point.from_dict({"x": 1.0, "y": 2.0, "z": 3.0})
        assert p.z == 3.0

    def test_from_json(self):
        p = Point.from_json('{"x": 10, "y": 20}')
        assert p.x == 10.0 and p.y == 20.0

    def test_from_tuple_list(self):
        p = Point.from_tuple([1, 2, 3])
        assert p.z == 3.0


class TestPointValidacion:
    def test_nan_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point(float("nan"), 0)

    def test_inf_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point(0, float("inf"))

    def test_string_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point("a", 0)  # type: ignore

    def test_from_tuple_invalid_length(self):
        with pytest.raises(GeometryError):
            Point.from_tuple((1,))

    def test_from_tuple_invalid_type(self):
        with pytest.raises(GeometryError):
            Point.from_tuple("not a tuple")  # type: ignore


class TestPointRepresentacion:
    def test_repr(self):
        r = repr(Point(1.5, 2.5))
        assert "Point" in r
        assert "1.5" in r

    def test_str(self):
        s = str(Point(1.5, 2.5))
        assert "Point" in s
        assert "1.5" in s


class TestPointInvariantes:
    def test_check_invariants_pasa(self):
        p = Point(1, 2, 3)
        p.check_invariants()

    def test_coordenadas_son_float(self):
        p = Point(1, 2)
        assert isinstance(p.x, float)
        assert isinstance(p.y, float)


class TestPointAlmostEqual:
    def test_almost_equal_mismo(self):
        assert Point(1, 2).almost_equal(Point(1, 2)) is True

    def test_almost_equal_diferente_tol(self):
        assert Point(1, 2).almost_equal(Point(1.1, 2), tol=0.2) is True

    def test_almost_equal_fuera_tol(self):
        assert Point(1, 2).almost_equal(Point(1.1, 2), tol=0.05) is False

    def test_almost_equal_otro_tipo(self):
        assert Point(0, 0).almost_equal("not a point") is NotImplemented