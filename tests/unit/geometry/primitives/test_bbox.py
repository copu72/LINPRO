"""Tests GEOM-BBOX: BoundingBox — caja delimitadora alineada a ejes.

Cubre GEOM-BBOX-TEST-001 a 086 (RFC-0003).
"""

import pytest

from linpro.geometry import BoundingBox, Point
from linpro.geometry.exceptions import GeometryError
from linpro.geometry.exceptions.invalid_coordinate import InvalidCoordinateError
from linpro.geometry.exceptions.validation_error import ValidationError
from linpro.geometry.kernel.geometry import Geometry


class TestCreacion:
    """GEOM-BBOX-TEST-001 a 010"""

    def test_creacion_basica(self):
        bb = BoundingBox(10.0, 20.0, 30.0, 40.0)
        assert bb.xmin == 10.0
        assert bb.ymin == 20.0
        assert bb.xmax == 30.0
        assert bb.ymax == 40.0

    def test_creacion_enteros(self):
        bb = BoundingBox(0, 0, 100, 100)
        assert all(isinstance(v, float) for v in (bb.xmin, bb.ymin, bb.xmax, bb.ymax))

    def test_creacion_floats(self):
        bb = BoundingBox(10.5, 20.5, 30.5, 40.5)
        assert bb.xmin == 10.5 and bb.ymin == 20.5
        assert bb.xmax == 30.5 and bb.ymax == 40.5

    def test_creacion_negativos(self):
        bb = BoundingBox(-100.0, -200.0, -10.0, -50.0)
        assert bb.xmin == -100 and bb.xmax == -10

    def test_creacion_cero(self):
        bb = BoundingBox(0.0, 0.0, 0.0, 0.0)
        assert bb.width == 0.0 and bb.height == 0.0

    def test_xmin_mayor_que_xmax_creado_pero_invalido(self):
        bb = BoundingBox(30, 20, 10, 40)
        assert bb.is_valid is False
        with pytest.raises(ValidationError):
            bb.check_invariants()

    def test_ymin_mayor_que_ymax_creado_pero_invalido(self):
        bb = BoundingBox(10, 40, 30, 20)
        assert bb.is_valid is False
        with pytest.raises(ValidationError):
            bb.check_invariants()

    def test_nan_raise(self):
        with pytest.raises(InvalidCoordinateError):
            BoundingBox(float("nan"), 0, 10, 10)

    def test_inf_raise(self):
        with pytest.raises(InvalidCoordinateError):
            BoundingBox(0, 0, 10, float("inf"))

    def test_string_raise(self):
        with pytest.raises(InvalidCoordinateError):
            BoundingBox("a", 0, 10, 10)


class TestPropiedades:
    """GEOM-BBOX-TEST-011 a 020"""

    def test_width(self):
        assert BoundingBox(10, 20, 30, 40).width == 20.0

    def test_height(self):
        assert BoundingBox(10, 20, 30, 40).height == 20.0

    def test_area(self):
        assert BoundingBox(10, 20, 30, 40).area == 400.0

    def test_center(self):
        c = BoundingBox(0, 0, 10, 10).center
        assert isinstance(c, Point)
        assert c == Point(5, 5)

    def test_width_cero(self):
        assert BoundingBox(10, 0, 10, 10).width == 0.0

    def test_height_cero(self):
        assert BoundingBox(0, 10, 10, 10).height == 0.0

    def test_area_cero(self):
        assert BoundingBox(0, 0, 0, 0).area == 0.0

    def test_center_negativos(self):
        c = BoundingBox(-10, -10, 10, 10).center
        assert c == Point(0, 0)

    def test_is_empty_width_cero(self):
        assert BoundingBox(5, 5, 5, 10).is_empty is True

    def test_is_empty_normal(self):
        assert BoundingBox(0, 0, 10, 10).is_empty is False


class TestInmutabilidad:
    """GEOM-BBOX-TEST-021 a 024"""

    def test_asignar_xmin_raise(self):
        bb = BoundingBox(0, 0, 10, 10)
        with pytest.raises(AttributeError):
            bb.xmin = 5

    def test_asignar_ymin_raise(self):
        bb = BoundingBox(0, 0, 10, 10)
        with pytest.raises(AttributeError):
            bb.ymin = 5

    def test_asignar_xmax_raise(self):
        bb = BoundingBox(0, 0, 10, 10)
        with pytest.raises(AttributeError):
            bb.xmax = 5

    def test_asignar_ymax_raise(self):
        bb = BoundingBox(0, 0, 10, 10)
        with pytest.raises(AttributeError):
            bb.ymax = 5


class TestContains:
    """GEOM-BBOX-TEST-025 a 032"""

    def test_punto_dentro(self):
        assert BoundingBox(0, 0, 10, 10).contains_point(Point(5, 5)) is True

    def test_punto_fuera_izquierda(self):
        assert BoundingBox(0, 0, 10, 10).contains_point(Point(-1, 5)) is False

    def test_punto_fuera_arriba(self):
        assert BoundingBox(0, 0, 10, 10).contains_point(Point(5, 15)) is False

    def test_punto_en_borde(self):
        assert BoundingBox(0, 0, 10, 10).contains_point(Point(10, 5)) is True

    def test_punto_en_esquina(self):
        assert BoundingBox(0, 0, 10, 10).contains_point(Point(0, 0)) is True

    def test_contains_bbox_identico(self):
        a = BoundingBox(0, 0, 10, 10)
        assert a.contains_bbox(a) is True

    def test_contains_bbox_interno(self):
        a = BoundingBox(0, 0, 10, 10)
        assert a.contains_bbox(BoundingBox(1, 1, 9, 9)) is True

    def test_contains_bbox_externo(self):
        a = BoundingBox(0, 0, 10, 10)
        assert a.contains_bbox(BoundingBox(-1, -1, 11, 11)) is False


class TestIntersects:
    """GEOM-BBOX-TEST-033 a 038"""

    def test_cajas_solapadas(self):
        assert BoundingBox(0, 0, 10, 10).intersects(BoundingBox(5, 5, 15, 15)) is True

    def test_cajas_separadas(self):
        assert BoundingBox(0, 0, 5, 5).intersects(BoundingBox(10, 10, 15, 15)) is False

    def test_cajas_tangentes(self):
        assert BoundingBox(0, 0, 10, 10).intersects(BoundingBox(10, 0, 20, 10)) is True

    def test_caja_contenida(self):
        assert BoundingBox(0, 0, 10, 10).intersects(BoundingBox(2, 2, 8, 8)) is True

    def test_caja_contenedora(self):
        assert BoundingBox(0, 0, 10, 10).intersects(BoundingBox(-5, -5, 15, 15)) is True

    def test_misma_caja(self):
        a = BoundingBox(0, 0, 10, 10)
        assert a.intersects(a) is True


class TestUnion:
    """GEOM-BBOX-TEST-039 a 043"""

    def test_union_separadas(self):
        u = BoundingBox(0, 0, 5, 5).union(BoundingBox(10, 10, 15, 15))
        assert u == BoundingBox(0, 0, 15, 15)

    def test_union_solapadas(self):
        u = BoundingBox(0, 0, 10, 10).union(BoundingBox(5, 5, 15, 15))
        assert u == BoundingBox(0, 0, 15, 15)

    def test_union_consigo_misma(self):
        a = BoundingBox(2, 3, 12, 13)
        assert a.union(a) == a

    def test_union_con_contenida(self):
        u = BoundingBox(0, 0, 10, 10).union(BoundingBox(2, 2, 8, 8))
        assert u == BoundingBox(0, 0, 10, 10)

    def test_union_con_contenedora(self):
        u = BoundingBox(2, 2, 8, 8).union(BoundingBox(0, 0, 10, 10))
        assert u == BoundingBox(0, 0, 10, 10)


class TestIntersection:
    """GEOM-BBOX-TEST-044 a 050"""

    def test_interseccion_solapadas(self):
        i = BoundingBox(0, 0, 10, 10).intersection(BoundingBox(5, 5, 15, 15))
        assert i == BoundingBox(5, 5, 10, 10)

    def test_interseccion_separadas(self):
        i = BoundingBox(0, 0, 5, 5).intersection(BoundingBox(10, 10, 15, 15))
        assert i is None

    def test_interseccion_consigo_misma(self):
        a = BoundingBox(1, 2, 11, 12)
        assert a.intersection(a) == a

    def test_interseccion_con_contenida(self):
        i = BoundingBox(0, 0, 10, 10).intersection(BoundingBox(2, 2, 8, 8))
        assert i == BoundingBox(2, 2, 8, 8)

    def test_interseccion_tangentes(self):
        i = BoundingBox(0, 0, 10, 10).intersection(BoundingBox(10, 0, 20, 10))
        assert i == BoundingBox(10, 0, 10, 10)

    def test_interseccion_tangentes_esquina_none(self):
        i = BoundingBox(0, 0, 5, 5).intersection(BoundingBox(5, 5, 10, 10))
        assert i is None

    def test_interseccion_devuelve_none_type(self):
        i = BoundingBox(0, 0, 5, 5).intersection(BoundingBox(10, 10, 15, 15))
        assert i is None


class TestExpand:
    """GEOM-BBOX-TEST-051 a 054"""

    def test_expand_positivo(self):
        e = BoundingBox(5, 5, 10, 10).expand(2)
        assert e == BoundingBox(3, 3, 12, 12)

    def test_expand_negativo(self):
        e = BoundingBox(0, 0, 10, 10).expand(-2)
        assert e == BoundingBox(2, 2, 8, 8)

    def test_expand_cero(self):
        a = BoundingBox(0, 0, 10, 10)
        assert a.expand(0) == a

    def test_expand_negativo_invierte_orden(self):
        e = BoundingBox(5, 5, 10, 10).expand(-10)
        assert e.is_empty is True
        assert e.is_valid is False


class TestFromPoints:
    """GEOM-BBOX-TEST-055 a 058"""

    def test_un_punto(self):
        bb = BoundingBox.from_points([Point(5, 10)])
        assert bb == BoundingBox(5, 10, 5, 10)

    def test_multiples_puntos(self):
        bb = BoundingBox.from_points([Point(0, 0), Point(10, 20), Point(5, 5)])
        assert bb == BoundingBox(0, 0, 10, 20)

    def test_puntos_linea_horizontal(self):
        bb = BoundingBox.from_points([Point(0, 5), Point(10, 5)])
        assert bb == BoundingBox(0, 5, 10, 5)
        assert bb.height == 0.0

    def test_lista_vacia_raise(self):
        with pytest.raises(ValidationError):
            BoundingBox.from_points([])


class TestIgualdadHash:
    """GEOM-BBOX-TEST-059 a 064"""

    def test_eq_mismo(self):
        assert BoundingBox(1, 2, 3, 4) == BoundingBox(1.0, 2.0, 3.0, 4.0)

    def test_eq_tolerancia(self):
        assert BoundingBox(1, 2, 3, 4) == BoundingBox(1.0000000005, 2, 3, 4)

    def test_neq(self):
        assert BoundingBox(1, 2, 3, 4) != BoundingBox(5, 6, 7, 8)

    def test_eq_otro_tipo(self):
        assert (BoundingBox(0, 0, 10, 10) == "POLYGON(...)") is False

    def test_hash_consistente(self):
        assert hash(BoundingBox(1, 2, 3, 4)) == hash(BoundingBox(1.0, 2.0, 3.0, 4.0))

    def test_hash_en_set(self):
        s = {BoundingBox(0, 0, 10, 10), BoundingBox(0, 0, 10, 10)}
        assert len(s) == 1

    def test_almost_equal_explicito(self):
        assert BoundingBox(1, 2, 3, 4).almost_equal(BoundingBox(1.1, 2, 3, 4), tol=0.2) is True

    def test_almost_equal_fuera_tol(self):
        assert BoundingBox(1, 2, 3, 4).almost_equal(BoundingBox(1.1, 2, 3, 4), tol=0.05) is False

    def test_almost_equal_otro_tipo(self):
        assert BoundingBox(0, 0, 10, 10).almost_equal("string") is NotImplemented


class TestSerializacion:
    """GEOM-BBOX-TEST-065 a 074"""

    def test_to_tuple(self):
        assert BoundingBox(1, 2, 3, 4).to_tuple() == (1.0, 2.0, 3.0, 4.0)

    def test_to_dict(self):
        assert BoundingBox(1, 2, 3, 4).to_dict() == {
            "xmin": 1.0, "ymin": 2.0, "xmax": 3.0, "ymax": 4.0,
        }

    def test_to_json(self):
        import json
        s = BoundingBox(1, 2, 3, 4).to_json()
        assert json.loads(s) == {"xmin": 1.0, "ymin": 2.0, "xmax": 3.0, "ymax": 4.0}

    def test_to_wkt(self):
        wkt = BoundingBox(1, 2, 3, 4).to_wkt()
        assert wkt == "POLYGON ((1.0 2.0, 3.0 2.0, 3.0 4.0, 1.0 4.0, 1.0 2.0))"

    def test_from_tuple_roundtrip(self):
        assert BoundingBox.from_tuple((1, 2, 3, 4)) == BoundingBox(1, 2, 3, 4)

    def test_from_dict_roundtrip(self):
        d = {"xmin": 1, "ymin": 2, "xmax": 3, "ymax": 4}
        assert BoundingBox.from_dict(d) == BoundingBox(1, 2, 3, 4)

    def test_from_json_roundtrip(self):
        bb = BoundingBox.from_json('{"xmin": 1, "ymin": 2, "xmax": 3, "ymax": 4}')
        assert bb == BoundingBox(1, 2, 3, 4)

    def test_from_tuple_3_elements_raise(self):
        with pytest.raises(GeometryError):
            BoundingBox.from_tuple((1, 2, 3))

    def test_from_tuple_5_elements_raise(self):
        with pytest.raises(GeometryError):
            BoundingBox.from_tuple((1, 2, 3, 4, 5))

    def test_from_dict_faltan_claves_raise(self):
        with pytest.raises(KeyError):
            BoundingBox.from_dict({"xmin": 1})

    def test_from_tuple_string_raise(self):
        with pytest.raises(GeometryError):
            BoundingBox.from_tuple("not a tuple")

    def test_empty_classmethod(self):
        bb = BoundingBox.empty()
        assert bb == BoundingBox(0, 0, 0, 0)
        assert bb.is_empty is True


class TestGeometryContract:
    """GEOM-BBOX-TEST-075 a 083"""

    def test_isinstance_geometry(self):
        assert isinstance(BoundingBox(0, 0, 10, 10), Geometry)

    def test_dimension(self):
        assert BoundingBox(0, 0, 10, 10).dimension == 2

    def test_bbox_self(self):
        bb = BoundingBox(0, 0, 10, 10)
        assert bb.bbox is bb

    def test_is_valid(self):
        assert BoundingBox(0, 0, 10, 10).is_valid is True

    def test_is_valid_false(self):
        assert BoundingBox(5, 5, 5, 10).is_empty is True

    def test_copy_distinto_objeto(self):
        bb = BoundingBox(1, 2, 3, 4)
        c = bb.copy()
        assert c == bb
        assert c is not bb

    def test_to_dict_from_dict_roundtrip(self):
        bb = BoundingBox(1.5, 2.5, 3.5, 4.5)
        assert BoundingBox.from_dict(bb.to_dict()) == bb

    def test_to_json_from_json_roundtrip(self):
        bb = BoundingBox(10, 20, 30, 40)
        assert BoundingBox.from_json(bb.to_json()) == bb

    def test_str_equals_repr(self):
        bb = BoundingBox(1.5, 2.5, 3.5, 4.5)
        assert str(bb) == repr(bb)


class TestInvariantes:
    """GEOM-BBOX-TEST-084 a 086"""

    def test_check_invariants_pasa(self):
        BoundingBox(1, 2, 3, 4).check_invariants()

    def test_check_invariants_despues_roundtrip(self):
        bb = BoundingBox.from_dict(BoundingBox(10, 20, 30, 40).to_dict())
        bb.check_invariants()

    def test_check_invariants_xmin_mayor_lanza(self):
        bb = BoundingBox(30, 20, 10, 40)
        with pytest.raises(ValidationError):
            bb.check_invariants()
