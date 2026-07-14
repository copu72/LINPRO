"""Tests TASK-0005B: Segment — entidad de ingeniería.

≥140 tests, cobertura ≥99%, ruff clean.
"""

import math

import pytest

from linpro.geometry import BoundingBox, Point, Segment, Vector
from linpro.geometry.exceptions import GeometryError
from linpro.geometry.kernel.geometry import Geometry

# ============================================================
# Creación
# ============================================================

class TestCreacion:
    def test_creacion_basica(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.start == Point(0, 0)
        assert s.end == Point(10, 0)

    def test_creacion_3d(self):
        s = Segment(Point(0, 0, 0), Point(1, 2, 3))
        assert s.start.z == 0.0
        assert s.end.z == 3.0

    def test_creacion_punto_igual(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.is_zero_length is True

    def test_creacion_negativos(self):
        s = Segment(Point(-10, -20), Point(10, 20))
        assert s.start == Point(-10, -20)

    def test_creacion_floats(self):
        s = Segment(Point(1.5, 2.5), Point(3.5, 4.5))
        assert s.start.x == 1.5

    def test_creacion_desde_dict(self):
        d = {"start": {"x": 1, "y": 2}, "end": {"x": 3, "y": 4}}
        s = Segment.from_dict(d)
        assert s == Segment(Point(1, 2), Point(3, 4))

    def test_creacion_desde_tuple_4(self):
        s = Segment.from_tuple((0, 0, 10, 10))
        assert s == Segment(Point(0, 0), Point(10, 10))

    def test_creacion_desde_tuple_6(self):
        s = Segment.from_tuple((0, 0, 0, 1, 2, 3))
        assert s.end.z == 3.0

    def test_from_tuple_raise(self):
        with pytest.raises(GeometryError):
            Segment.from_tuple((1, 2, 3))

    def test_from_tuple_5_raise(self):
        with pytest.raises(GeometryError):
            Segment.from_tuple((1, 2, 3, 4, 5))

    def test_creacion_desde_json(self):
        s = Segment.from_json('{"start": {"x": 0, "y": 0}, "end": {"x": 1, "y": 1}}')
        assert s == Segment(Point(0, 0), Point(1, 1))


# ============================================================
# Propiedades
# ============================================================

class TestPropiedades:
    def test_start(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.start == Point(0, 0)

    def test_end(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.end == Point(10, 0)

    def test_vector(self):
        s = Segment(Point(0, 0), Point(3, 4))
        assert s.vector == Vector(3, 4)

    def test_vector_cache(self):
        s = Segment(Point(0, 0), Point(3, 4))
        assert s.vector is s.vector

    def test_length(self):
        s = Segment(Point(0, 0), Point(3, 4))
        assert s.length == 5.0

    def test_length_3d(self):
        s = Segment(Point(0, 0, 0), Point(2, 3, 6))
        assert s.length == 7.0

    def test_length_cero(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.length == 0.0

    def test_length_squared(self):
        s = Segment(Point(0, 0), Point(3, 4))
        assert s.length_squared == 25.0

    def test_bbox(self):
        s = Segment(Point(0, 0), Point(10, 20))
        bb = s.bbox
        assert isinstance(bb, BoundingBox)
        assert bb == BoundingBox(0, 0, 10, 20)

    def test_bbox_invertido(self):
        s = Segment(Point(10, 20), Point(0, 0))
        bb = s.bbox
        assert bb == BoundingBox(0, 0, 10, 20)

    def test_center(self):
        s = Segment(Point(0, 0), Point(10, 20))
        assert s.center == Point(5, 10)

    def test_center_3d(self):
        s = Segment(Point(0, 0, 0), Point(10, 20, 30))
        assert s.center == Point(5, 10, 15)

    def test_azimuth_east(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.azimuth == pytest.approx(0.0)

    def test_azimuth_north(self):
        s = Segment(Point(0, 0), Point(0, 10))
        assert s.azimuth == pytest.approx(90.0)

    def test_azimuth_45(self):
        s = Segment(Point(0, 0), Point(10, 10))
        assert s.azimuth == pytest.approx(45.0)

    def test_dimension(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.dimension == 1

    def test_is_zero_length_true(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.is_zero_length is True

    def test_is_zero_length_false(self):
        s = Segment(Point(0, 0), Point(1, 0))
        assert s.is_zero_length is False

    def test_is_empty_zero_length(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.is_empty is True

    def test_is_empty_normal(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.is_empty is False


# ============================================================
# Inmutabilidad
# ============================================================

class TestInmutabilidad:
    def test_asignar_start_raise(self):
        s = Segment(Point(0, 0), Point(10, 0))
        with pytest.raises(AttributeError):
            s.start = Point(1, 1)

    def test_asignar_end_raise(self):
        s = Segment(Point(0, 0), Point(10, 0))
        with pytest.raises(AttributeError):
            s.end = Point(1, 1)

    def test_reverse_nueva_instancia(self):
        s = Segment(Point(0, 0), Point(10, 0))
        r = s.reverse()
        assert r is not s
        assert r == Segment(Point(10, 0), Point(0, 0))

    def test_copy_independiente(self):
        s = Segment(Point(0, 0), Point(10, 0))
        c = s.copy()
        assert c == s
        assert c is not s


# ============================================================
# Geometry contract
# ============================================================

class TestGeometryContract:
    def test_isinstance_geometry(self):
        assert isinstance(Segment(Point(0, 0), Point(10, 0)), Geometry)

    def test_is_valid(self):
        assert Segment(Point(0, 0), Point(10, 0)).is_valid is True

    def test_is_valid_invalid(self):
        s = Segment(Point(0, 0), Point(10, 0))
        object.__setattr__(s, "_start", "not_a_point")
        assert s.is_valid is False

    def test_check_invariants(self):
        Segment(Point(0, 0), Point(10, 0)).check_invariants()

    def test_check_invariants_invalid_start(self):
        s = Segment(Point(0, 0), Point(10, 0))
        object.__setattr__(s, "_start", "bad")
        with pytest.raises(GeometryError):
            s.check_invariants()

    def test_check_invariants_invalid_end(self):
        s = Segment(Point(0, 0), Point(10, 0))
        object.__setattr__(s, "_end", "bad")
        with pytest.raises(GeometryError):
            s.check_invariants()

    def test_copy_equals(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.copy() == s

    def test_to_dict_from_dict_roundtrip(self):
        s = Segment(Point(1, 2, 3), Point(4, 5, 6))
        assert Segment.from_dict(s.to_dict()) == s

    def test_to_json_from_json_roundtrip(self):
        s = Segment(Point(0, 0), Point(10, 20))
        assert Segment.from_json(s.to_json()) == s

    def test_str_equals_repr(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert str(s) == repr(s)

    def test_bbox_type(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert isinstance(s.bbox, BoundingBox)

    def test_dimension_is_1(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.dimension == 1

    def test_equality_with_non_segment(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert (s == "string") is False


# ============================================================
# Serialización
# ============================================================

class TestSerializacion:
    def test_to_tuple_2d(self):
        s = Segment(Point(0, 0), Point(10, 20))
        t = s.to_tuple()
        assert len(t) == 6
        assert t == (0.0, 0.0, 0.0, 10.0, 20.0, 0.0)

    def test_to_tuple_3d(self):
        s = Segment(Point(0, 0, 5), Point(10, 20, 30))
        t = s.to_tuple()
        assert t == (0.0, 0.0, 5.0, 10.0, 20.0, 30.0)

    def test_to_dict(self):
        s = Segment(Point(0, 0), Point(10, 20))
        d = s.to_dict()
        assert d["start"] == {"x": 0.0, "y": 0.0, "z": 0.0}
        assert d["end"] == {"x": 10.0, "y": 20.0, "z": 0.0}

    def test_from_tuple_4(self):
        s = Segment.from_tuple((1, 2, 3, 4))
        assert s == Segment(Point(1, 2), Point(3, 4))

    def test_from_tuple_6(self):
        s = Segment.from_tuple((0, 0, 0, 1, 2, 3))
        assert s.end.z == 3.0

    def test_from_tuple_4_raises(self):
        with pytest.raises(GeometryError):
            Segment.from_tuple((1,))

    def test_from_dict(self):
        d = {"start": {"x": 1, "y": 2}, "end": {"x": 3, "y": 4}}
        s = Segment.from_dict(d)
        assert s == Segment(Point(1, 2), Point(3, 4))

    def test_from_dict_con_z(self):
        d = {"start": {"x": 0, "y": 0, "z": 5}, "end": {"x": 1, "y": 1, "z": 10}}
        s = Segment.from_dict(d)
        assert s.start.z == 5.0
        assert s.end.z == 10.0

    def test_to_json(self):
        import json
        s = Segment(Point(0, 0), Point(10, 0))
        d = json.loads(s.to_json())
        assert d["start"]["x"] == 0.0
        assert d["end"]["x"] == 10.0

    def test_from_json(self):
        s = Segment.from_json('{"start": {"x": 1, "y": 2}, "end": {"x": 3, "y": 4}}')
        assert s == Segment(Point(1, 2), Point(3, 4))

    def test_to_wkt(self):
        s = Segment(Point(0, 0), Point(10, 20))
        assert s.to_wkt() == "LINESTRING (0 0, 10 20)"

    def test_to_wkt_3d(self):
        s = Segment(Point(0, 0, 5), Point(10, 20, 30))
        assert s.to_wkt() == "LINESTRING (0 0, 10 20)"

    def test_roundtrip_tuple_2d(self):
        s = Segment(Point(1.5, 2.5), Point(3.5, 4.5))
        assert Segment.from_tuple(s.to_tuple()) == s

    def test_roundtrip_tuple_3d(self):
        s = Segment(Point(1, 2, 3), Point(4, 5, 6))
        assert Segment.from_tuple(s.to_tuple()) == s

    def test_roundtrip_dict(self):
        s = Segment(Point(10, 20), Point(30, 40))
        assert Segment.from_dict(s.to_dict()) == s

    def test_roundtrip_json(self):
        s = Segment(Point(10, 20), Point(30, 40))
        assert Segment.from_json(s.to_json()) == s


# ============================================================
# Igualdad y hash
# ============================================================

class TestIgualdadHash:
    def test_eq_mismo(self):
        assert Segment(Point(0, 0), Point(10, 0)) == Segment(Point(0, 0), Point(10, 0))

    def test_eq_tolerancia(self):
        a = Segment(Point(0, 0), Point(10, 0))
        b = Segment(Point(0, 0), Point(10.0000000005, 0))
        assert a == b

    def test_neq(self):
        assert Segment(Point(0, 0), Point(10, 0)) != Segment(Point(0, 0), Point(20, 0))

    def test_neq_start_diff(self):
        assert Segment(Point(0, 0), Point(10, 0)) != Segment(Point(1, 0), Point(10, 0))

    def test_eq_otro_tipo(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert (s == "segmento") is False

    def test_hash_consistente(self):
        a = Segment(Point(0, 0), Point(10, 0))
        b = Segment(Point(0, 0), Point(10, 0))
        assert hash(a) == hash(b)

    def test_hash_en_set(self):
        s = {
            Segment(Point(0, 0), Point(10, 0)),
            Segment(Point(0, 0), Point(10, 0)),
            Segment(Point(0, 0), Point(20, 0)),
        }
        assert len(s) == 2

    def test_eq_reverso_no_igual(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(10, 0), Point(0, 0))
        assert s1 != s2

    def test_eq_mismo_objeto(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s == s

    def test_neq_con_punto_distinto(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 1), Point(10, 0))
        assert s1 != s2


# ============================================================
# reverse y copy
# ============================================================

class TestReverseCopy:
    def test_reverse_true(self):
        s = Segment(Point(0, 0), Point(10, 20))
        r = s.reverse()
        assert r.start == s.end
        assert r.end == s.start

    def test_reverse_dos_veces_vuelta(self):
        s = Segment(Point(0, 0), Point(10, 20))
        assert s.reverse().reverse() == s

    def test_reverse_longitud(self):
        s = Segment(Point(0, 0), Point(3, 4))
        assert s.reverse().length == s.length

    def test_reverse_vector(self):
        s = Segment(Point(0, 0), Point(3, 4))
        assert s.reverse().vector == -s.vector

    def test_copy_independiente(self):
        s = Segment(Point(0, 0), Point(10, 0))
        c = s.copy()
        assert c == s
        assert c is not s

    def test_copy_no_alias(self):
        s = Segment(Point(0, 0), Point(10, 0))
        c = s.copy()
        assert c.start is not s.start
        assert c.end is not s.end


# ============================================================
# Operaciones delegadas: contains
# ============================================================

class TestContains:
    def test_contains_punto_sobre(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.contains(Point(5, 0)) is True

    def test_contains_punto_fuera(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.contains(Point(5, 5)) is False

    def test_contains_extremo_start(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.contains(Point(0, 0)) is True

    def test_contains_extremo_end(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.contains(Point(10, 0)) is True

    def test_contains_degenerado(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.contains(Point(5, 5)) is True

    def test_contains_degenerado_fuera(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.contains(Point(0, 0)) is False


# ============================================================
# Operaciones delegadas: distance_to
# ============================================================

class TestDistanceTo:
    def test_distance_point_sobre(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.distance_to(Point(5, 0)) == 0.0

    def test_distance_point_fuera(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.distance_to(Point(5, 3)) == pytest.approx(3.0)

    def test_distance_point_before(self):
        s = Segment(Point(5, 0), Point(10, 0))
        assert s.distance_to(Point(0, 0)) == pytest.approx(5.0)

    def test_distance_point_after(self):
        s = Segment(Point(0, 0), Point(5, 0))
        assert s.distance_to(Point(10, 0)) == pytest.approx(5.0)

    def test_distance_segment_intersect(self):
        s1 = Segment(Point(0, 0), Point(10, 10))
        s2 = Segment(Point(0, 10), Point(10, 0))
        assert s1.distance_to(s2) == 0.0

    def test_distance_segment_parallel(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 5), Point(10, 5))
        assert s1.distance_to(s2) == pytest.approx(5.0)

    def test_distance_segment_reverse(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        assert s1.distance_to(s1) == 0.0

    def test_distance_type_error(self):
        s = Segment(Point(0, 0), Point(10, 0))
        with pytest.raises(TypeError):
            s.distance_to(Vector(1, 0))

    def test_distance_segment_separated(self):
        s1 = Segment(Point(0, 0), Point(5, 0))
        s2 = Segment(Point(10, 0), Point(15, 0))
        assert s1.distance_to(s2) == pytest.approx(5.0)


# ============================================================
# Operaciones delegadas: project y closest_point
# ============================================================

class TestProjectClosest:
    def test_project_inside(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.project(Point(5, 5)) == Point(5, 0)

    def test_project_before(self):
        s = Segment(Point(5, 0), Point(10, 0))
        proj = s.project(Point(0, 0))
        assert proj.x < s.start.x

    def test_closest_inside(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.closest_point(Point(5, 5)) == Point(5, 0)

    def test_closest_before(self):
        s = Segment(Point(5, 0), Point(10, 0))
        assert s.closest_point(Point(0, 0)) == Point(5, 0)

    def test_closest_after(self):
        s = Segment(Point(0, 0), Point(5, 0))
        assert s.closest_point(Point(10, 0)) == Point(5, 0)

    def test_closest_on_point(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.closest_point(Point(3, 0)) == Point(3, 0)

    def test_closest_degenerate(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.closest_point(Point(0, 0)) == Point(5, 5)


# ============================================================
# Operaciones delegadas: intersects
# ============================================================

class TestIntersects:
    def test_intersects_cross(self):
        s1 = Segment(Point(0, 0), Point(10, 10))
        s2 = Segment(Point(0, 10), Point(10, 0))
        assert s1.intersects(s2) is True

    def test_intersects_parallel(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 5), Point(10, 5))
        assert s1.intersects(s2) is False

    def test_intersects_extremo(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(10, 0), Point(10, 10))
        assert s1.intersects(s2) is True

    def test_intersects_colinear(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, 0), Point(15, 0))
        assert s1.intersects(s2) is True

    def test_intersects_consigo_mismo(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.intersects(s) is True

    def test_intersects_con_tolerancia(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(10, 1e-8), Point(20, 1e-8))
        assert s1.intersects(s2, tol=1e-6) is True


# ============================================================
# Operaciones delegadas: orientation
# ============================================================

class TestOrientation:
    def test_orientation_ccw(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.orientation(Point(5, 5)) > 0

    def test_orientation_cw(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.orientation(Point(5, -5)) < 0

    def test_orientation_colinear(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.orientation(Point(5, 0)) == 0.0

    def test_is_collinear_true(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(5, 0), Point(15, 0))
        assert s1.is_collinear(s2) is True

    def test_is_collinear_false(self):
        s1 = Segment(Point(0, 0), Point(10, 0))
        s2 = Segment(Point(0, 5), Point(10, 5))
        assert s1.is_collinear(s2) is False


# ============================================================
# Casos límite
# ============================================================

class TestCasosLimite:
    def test_degenerado_length_cero(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.length == 0.0
        assert s.is_zero_length is True

    def test_degenerado_vector(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.vector == Vector(0, 0)

    def test_degenerado_bbox(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.bbox == BoundingBox(5, 5, 5, 5)

    def test_degenerado_center(self):
        s = Segment(Point(5, 5), Point(5, 5))
        assert s.center == Point(5, 5)

    def test_azimuth_cero(self):
        s = Segment(Point(0, 0), Point(0, 0))
        assert s.azimuth == pytest.approx(0.0)

    def test_azimuth_west(self):
        s = Segment(Point(10, 0), Point(0, 0))
        assert s.azimuth == pytest.approx(180.0)

    def test_azimuth_south(self):
        s = Segment(Point(0, 10), Point(0, 0))
        assert s.azimuth == pytest.approx(-90.0)

    def test_coordenadas_grandes_utm(self):
        s = Segment(Point(500000, 4600000), Point(600000, 4700000))
        assert s.length > 0
        assert isinstance(s.bbox, BoundingBox)

    def test_3d_vector(self):
        s = Segment(Point(0, 0, 0), Point(1, 2, 3))
        assert s.vector.dz == 3.0

    def test_3d_length(self):
        s = Segment(Point(0, 0, 0), Point(2, 3, 6))
        assert s.length == 7.0

    def test_3d_bbox_ignores_z(self):
        s = Segment(Point(0, 0, 100), Point(10, 20, 200))
        bb = s.bbox
        assert bb.xmin == 0
        assert bb.ymax == 20

    def test_3d_center(self):
        s = Segment(Point(0, 0, 0), Point(10, 20, 30))
        c = s.center
        assert c.x == 5.0
        assert c.z == 15.0

    def test_3d_to_wkt(self):
        s = Segment(Point(0, 0, 5), Point(10, 20, 30))
        assert s.to_wkt() == "LINESTRING (0 0, 10 20)"  # WKT 2D

    def test_recta_vertical(self):
        s = Segment(Point(5, 0), Point(5, 10))
        assert s.length == 10.0
        assert s.bbox == BoundingBox(5, 0, 5, 10)

    def test_recta_diagonal(self):
        s = Segment(Point(0, 0), Point(10, 10))
        assert s.length == pytest.approx(math.sqrt(200))

    def test_azimuth_135(self):
        s = Segment(Point(0, 0), Point(-10, 10))
        assert s.azimuth == pytest.approx(135.0)

    def test_azimuth_negativo_45(self):
        s = Segment(Point(0, 0), Point(10, -10))
        assert s.azimuth == pytest.approx(-45.0)


# ============================================================
# Errores
# ============================================================

class TestErrores:
    def test_from_tuple_tipo_raise(self):
        with pytest.raises(GeometryError):
            Segment.from_tuple("bad")

    def test_from_dict_tipo_raise(self):
        with pytest.raises((GeometryError, TypeError)):
            Segment.from_dict({"start": "bad", "end": "bad"})

    def test_distance_to_vector_raise(self):
        s = Segment(Point(0, 0), Point(10, 0))
        with pytest.raises(TypeError):
            s.distance_to(Vector(1, 2))

    def test_distance_to_bbox_raise(self):
        s = Segment(Point(0, 0), Point(10, 0))
        bb = BoundingBox(0, 0, 10, 10)
        with pytest.raises(TypeError):
            s.distance_to(bb)

    def test_orientation_degenerate(self):
        s = Segment(Point(5, 5), Point(5, 5))
        o = s.orientation(Point(0, 0))
        assert o == 0.0

    def test_contains_tolerance(self):
        s = Segment(Point(0, 0), Point(10, 0))
        assert s.contains(Point(5, 1e-8), tol=1e-6) is True


# ============================================================
# Benchmark suite (non-benchmark mode, just verify they run)
# ============================================================

class TestBenchmarkSanity:
    def test_bench_creation(self):
        for _ in range(1000):
            Segment(Point(0, 0), Point(1000, 500))

    def test_bench_length(self):
        s = Segment(Point(0, 0), Point(1000, 500))
        for _ in range(1000):
            _ = s.length

    def test_bench_azimuth(self):
        s = Segment(Point(0, 0), Point(1000, 500))
        for _ in range(1000):
            _ = s.azimuth

    def test_bench_reverse(self):
        s = Segment(Point(0, 0), Point(1000, 500))
        for _ in range(1000):
            s.reverse()

    def test_bench_vector(self):
        s = Segment(Point(0, 0), Point(1000, 500))
        for _ in range(1000):
            _ = s.vector

    def test_bench_distance(self):
        s = Segment(Point(0, 0), Point(1000, 0))
        p = Point(500, 300)
        for _ in range(1000):
            s.distance_to(p)
