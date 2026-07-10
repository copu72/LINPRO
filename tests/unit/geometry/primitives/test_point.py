"""Tests GEOM-POINT: Point — primitiva fundamental del Kernel Geometry.

Cubre GEOM-POINT-TEST-001 a ~040 (TASK-0003A).
"""

import json
import math

import pytest

from linpro.geometry import BoundingBox, Point
from linpro.geometry.exceptions import GeometryError, InvalidCoordinateError
from linpro.geometry.kernel.geometry import Geometry


class TestPointCreation:
    """GEOM-POINT-TEST-001 a 008"""

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

    def test_z_default_cero(self):
        assert Point(5, 5).z == 0.0

    def test_coordenadas_utm_grandes(self):
        p = Point(500000.123, 4600000.456)
        assert p.x == 500000.123
        assert p.y == 4600000.456

    def test_creacion_origen(self):
        p = Point(0, 0, 0)
        assert p.x == 0.0 and p.y == 0.0 and p.z == 0.0

    def test_creacion_negativos(self):
        p = Point(-100.5, -200.3)
        assert p.x == -100.5
        assert p.y == -200.3


class TestPointValidacion:
    """GEOM-POINT-TEST-009 a 015"""

    def test_nan_x_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point(float("nan"), 0)

    def test_nan_y_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point(0, float("nan"))

    def test_nan_z_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point(0, 0, float("nan"))

    def test_inf_x_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point(float("inf"), 0)

    def test_string_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point("a", 0)

    def test_none_raise(self):
        with pytest.raises(InvalidCoordinateError):
            Point(None, 0)


class TestPointInmutabilidad:
    """GEOM-POINT-TEST-016 a 018"""

    def test_asignar_x_raise(self):
        p = Point(1, 2)
        with pytest.raises(AttributeError):
            p.x = 3

    def test_asignar_y_raise(self):
        p = Point(1, 2)
        with pytest.raises(AttributeError):
            p.y = 4

    def test_asignar_z_raise(self):
        p = Point(1, 2)
        with pytest.raises(AttributeError):
            p.z = 5


class TestPointDistancia:
    """GEOM-POINT-TEST-019 a 023"""

    def test_distancia_2d(self):
        d = Point(0, 0).distance_to(Point(3, 4))
        assert math.isclose(d, 5.0)

    def test_distancia_3d(self):
        d = Point(0, 0, 0).distance_to(Point(2, 3, 6))
        assert math.isclose(d, 7.0)

    def test_distancia_mismo_punto(self):
        assert Point(1, 2).distance_to(Point(1, 2)) == 0.0

    def test_distancia_negativos(self):
        d = Point(-1, -1).distance_to(Point(2, 3))
        assert math.isclose(d, 5.0)

    def test_distancia_simetrica(self):
        a = Point(10, 20)
        b = Point(30, 50)
        assert math.isclose(a.distance_to(b), b.distance_to(a))


class TestPointIgualdad:
    """GEOM-POINT-TEST-024 a 030"""

    def test_igualdad_exacta(self):
        assert Point(1.0, 2.0) == Point(1.0, 2.0)

    def test_igualdad_tolerancia(self):
        assert Point(1.0, 2.0) == Point(1.0000000005, 2.0)

    def test_desigualdad(self):
        assert Point(1, 2) != Point(3, 4)

    def test_no_igual_a_string(self):
        assert (Point(0, 0) == "POINT (0 0)") is False

    def test_almost_equal_explicito(self):
        assert Point(1, 2).almost_equal(Point(1.1, 2), tol=0.2) is True

    def test_almost_equal_fuera_tol(self):
        assert Point(1, 2).almost_equal(Point(1.1, 2), tol=0.05) is False

    def test_almost_equal_otro_tipo(self):
        assert Point(0, 0).almost_equal("not a point") is NotImplemented


class TestPointHash:
    """GEOM-POINT-TEST-031 a 034"""

    def test_hash_consistente(self):
        assert hash(Point(1, 2)) == hash(Point(1.0, 2.0))

    def test_hash_en_set(self):
        s = {Point(0, 0), Point(1, 1), Point(0, 0)}
        assert len(s) == 2

    def test_hash_como_clave_dict(self):
        d = {Point(0, 0): "origin"}
        assert d[Point(0, 0)] == "origin"


class TestPointSerializacion:
    """GEOM-POINT-TEST-035 a 045"""

    def test_to_tuple_3d(self):
        assert Point(1, 2, 3).to_tuple() == (1.0, 2.0, 3.0)

    def test_to_tuple_2d(self):
        assert Point(1, 2).to_tuple() == (1.0, 2.0, 0.0)

    def test_to_dict(self):
        assert Point(1, 2, 3).to_dict() == {"x": 1.0, "y": 2.0, "z": 3.0}

    def test_to_json(self):
        s = Point(1, 2, 3).to_json()
        assert json.loads(s) == {"x": 1.0, "y": 2.0, "z": 3.0}

    def test_to_wkt(self):
        assert Point(10.5, 20.5).to_wkt() == "POINT (10.5 20.5)"

    def test_from_tuple_2(self):
        p = Point.from_tuple((3.0, 4.0))
        assert p.xy == (3.0, 4.0) and p.z == 0.0

    def test_from_tuple_3(self):
        assert Point.from_tuple((1, 2, 3)).z == 3.0

    def test_from_dict(self):
        assert Point.from_dict({"x": 1.0, "y": 2.0}) == Point(1, 2)

    def test_from_dict_con_z(self):
        assert Point.from_dict({"x": 1, "y": 2, "z": 3}).z == 3.0

    def test_from_json(self):
        p = Point.from_json('{"x": 10, "y": 20}')
        assert p.x == 10.0 and p.y == 20.0


class TestPointErroresDeserializacion:
    """GEOM-POINT-TEST-046 a 049"""

    def test_from_tuple_un_elemento(self):
        with pytest.raises(GeometryError):
            Point.from_tuple((1,))

    def test_from_tuple_cuatro_elementos(self):
        with pytest.raises(GeometryError):
            Point.from_tuple((1, 2, 3, 4))

    def test_from_tuple_string(self):
        with pytest.raises(GeometryError):
            Point.from_tuple("not a tuple")

    def test_from_dict_falta_y(self):
        with pytest.raises(KeyError):
            Point.from_dict({"x": 1})


class TestPointGeometryContract:
    """GEOM-POINT-TEST-050 a 058"""

    def test_isinstance_geometry(self):
        assert isinstance(Point(1, 2), Geometry)

    def test_dimension_2d(self):
        assert Point(1, 2).dimension == 2

    def test_dimension_3d(self):
        assert Point(1, 2, 3).dimension == 3

    def test_bbox(self):
        bb = Point(10, 20).bbox
        assert isinstance(bb, BoundingBox)
        assert bb.xmin == 10.0 and bb.xmax == 10.0
        assert bb.ymin == 20.0 and bb.ymax == 20.0

    def test_is_valid(self):
        assert Point(1, 2).is_valid is True

    def test_is_empty(self):
        assert Point(1, 2).is_empty is False

    def test_copy_distinto_objeto(self):
        p = Point(1, 2, 3)
        c = p.copy()
        assert c == p
        assert c is not p

    def test_to_dict_from_dict_roundtrip(self):
        p = Point(1.5, 2.5, 3.5)
        assert Point.from_dict(p.to_dict()) == p

    def test_to_json_from_json_roundtrip(self):
        p = Point(10, 20, 30)
        assert Point.from_json(p.to_json()) == p

    def test_str_equals_repr(self):
        p = Point(1.5, 2.5)
        assert str(p) == repr(p)


class TestPointInvariantes:
    """GEOM-POINT-TEST-059 a 060"""

    def test_check_invariants_pasa(self):
        Point(1, 2, 3).check_invariants()

    def test_check_invariants_despues_roundtrip(self):
        p = Point.from_dict(Point(10, 20).to_dict())
        p.check_invariants()
