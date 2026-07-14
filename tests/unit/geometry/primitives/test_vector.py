"""Tests GEOM-VEC: Vector — desplazamiento en el espacio 2D/3D.

Cubre API completa del RFC-0004A (≥100 tests).
"""

import math

import pytest

from linpro.geometry import BoundingBox, Point, Vector
from linpro.geometry.exceptions import GeometryError, PrecisionError
from linpro.geometry.kernel.geometry import Geometry

# ============================================================
# Creación
# ============================================================

class TestCreacion:
    def test_creacion_2d(self):
        v = Vector(3.0, 4.0)
        assert v.dx == 3.0 and v.dy == 4.0 and v.dz == 0.0

    def test_creacion_3d(self):
        v = Vector(1.0, 2.0, 3.0)
        assert v.dz == 3.0

    def test_creacion_enteros(self):
        v = Vector(3, 4)
        assert isinstance(v.dx, float)

    def test_creacion_dz_default(self):
        v = Vector(1, 2)
        assert v.dz == 0.0

    def test_creacion_desde_point(self):
        p1, p2 = Point(0, 0), Point(3, 4)
        v = Vector.from_points(p1, p2)
        assert v == Vector(3, 4)

    def test_creacion_desde_angle(self):
        v = Vector.from_angle(0.0, 5.0)
        assert v == Vector(5, 0)

    def test_creacion_desde_angle_45(self):
        v = Vector.from_angle(math.pi / 4, 1.0)
        assert v.almost_equal(Vector(math.sqrt(2)/2, math.sqrt(2)/2))

    def test_creacion_nan_dx_raise(self):
        with pytest.raises(Exception):
            Vector(float("nan"), 0)

    def test_creacion_inf_raise(self):
        with pytest.raises(Exception):
            Vector(float("inf"), 0)

    def test_creacion_string_raise(self):
        with pytest.raises(Exception):
            Vector("a", 0)


# ============================================================
# Propiedades
# ============================================================

class TestPropiedades:
    def test_length_3_4_5(self):
        assert Vector(3, 4).length == 5.0

    def test_length_3d(self):
        assert Vector(2, 3, 6).length == 7.0

    def test_length_cero(self):
        assert Vector(0, 0).length == 0.0

    def test_length_squared(self):
        assert Vector(3, 4).length_squared == 25.0

    def test_angle_eje_x(self):
        assert Vector(1, 0).angle == 0.0

    def test_angle_eje_y(self):
        assert Vector(0, 1).angle == pytest.approx(math.pi / 2)

    def test_angle_negativo(self):
        assert Vector(-1, -1).angle == pytest.approx(-3 * math.pi / 4)

    def test_dimension_2d(self):
        assert Vector(1, 2).dimension == 2

    def test_dimension_3d(self):
        assert Vector(1, 2, 3).dimension == 3

    def test_is_zero_true(self):
        assert Vector(0, 0).is_zero is True

    def test_is_zero_false(self):
        assert Vector(1, 0).is_zero is False

    def test_is_unit_true(self):
        assert Vector(1, 0).is_unit is True

    def test_is_unit_false(self):
        assert Vector(2, 0).is_unit is False

    def test_perpendicular(self):
        v = Vector(3, 4)
        assert v.perpendicular == Vector(-4, 3)

    def test_normalized(self):
        v = Vector(3, 4).normalized
        assert v.almost_equal(Vector(0.6, 0.8))

    def test_normalized_es_unitario(self):
        assert Vector(5, 12).normalized.is_unit is True

    def test_normalized_zero_raise(self):
        with pytest.raises(PrecisionError):
            Vector(0, 0).normalized

    def test_bbox(self):
        bb = Vector(10, 20).bbox
        assert isinstance(bb, BoundingBox)
        assert bb == BoundingBox(0, 0, 10, 20)

    def test_is_empty_zero(self):
        assert Vector(0, 0).is_empty is True

    def test_is_empty_no(self):
        assert Vector(1, 1).is_empty is False


# ============================================================
# Inmutabilidad
# ============================================================

class TestInmutabilidad:
    def test_asignar_dx_raise(self):
        v = Vector(1, 2)
        with pytest.raises(AttributeError):
            v.dx = 5

    def test_asignar_dy_raise(self):
        v = Vector(1, 2)
        with pytest.raises(AttributeError):
            v.dy = 5


# ============================================================
# Álgebra: escalares
# ============================================================

class TestAlgebraEscalar:
    def test_dot_producto(self):
        assert Vector(1, 0).dot(Vector(0, 1)) == 0.0

    def test_dot_paralelos(self):
        assert Vector(2, 0).dot(Vector(3, 0)) == 6.0

    def test_dot_3d(self):
        assert Vector(1, 2, 3).dot(Vector(4, 5, 6)) == 32.0

    def test_cross_2d(self):
        assert Vector(1, 0).cross(Vector(0, 1)) == 1.0

    def test_cross_2d_antiparalelo(self):
        assert Vector(2, 0).cross(Vector(0, -3)) == -6.0

    def test_cross_2d_paralelos(self):
        assert Vector(2, 0).cross(Vector(5, 0)) == 0.0

    def test_cross_3d_devuelve_vector(self):
        r = Vector(1, 0, 5).cross(Vector(0, 1, 0))
        assert isinstance(r, Vector)

    def test_cross_3d_magnitud(self):
        r = Vector(2, 0, 0).cross(Vector(0, 3, 1))
        assert isinstance(r, Vector)
        assert r == Vector(0, -2, 6)


# ============================================================
# Álgebra: ángulos
# ============================================================

class TestAlgebraAngulos:
    def test_angle_to_ortogonales(self):
        a = Vector(1, 0).angle_to(Vector(0, 1))
        assert a == pytest.approx(math.pi / 2)

    def test_angle_to_paralelos(self):
        a = Vector(2, 0).angle_to(Vector(3, 0))
        assert a == pytest.approx(0.0)

    def test_angle_to_opuestos(self):
        a = Vector(1, 0).angle_to(Vector(-1, 0))
        assert a == pytest.approx(math.pi)

    def test_signed_angle_to_positivo(self):
        a = Vector(1, 0).signed_angle_to(Vector(0, 1))
        assert a == pytest.approx(math.pi / 2)

    def test_signed_angle_to_negativo(self):
        a = Vector(0, 1).signed_angle_to(Vector(1, 0))
        assert a == pytest.approx(-math.pi / 2)


# ============================================================
# Álgebra: transformaciones
# ============================================================

class TestTransformaciones:
    def test_rotate_90(self):
        v = Vector(1, 0).rotate(math.pi / 2)
        assert v.almost_equal(Vector(0, 1))

    def test_rotate_180(self):
        v = Vector(1, 0).rotate(math.pi)
        assert v.almost_equal(Vector(-1, 0))

    def test_rotate_360_vuelta(self):
        v = Vector(3, 4).rotate(2 * math.pi)
        assert v.almost_equal(Vector(3, 4))

    def test_project_onto_eje_x(self):
        v = Vector(3, 4).project_onto(Vector(1, 0))
        assert v == Vector(3, 0)

    def test_project_onto_eje_y(self):
        v = Vector(3, 4).project_onto(Vector(0, 1))
        assert v == Vector(0, 4)

    def test_project_onto_zero(self):
        v = Vector(3, 4).project_onto(Vector(0, 0))
        assert v == Vector(0, 0)

    def test_reject_from(self):
        v = Vector(3, 4).reject_from(Vector(1, 0))
        assert v.almost_equal(Vector(0, 4))

    def test_lerp_mitad(self):
        v = Vector(0, 0).lerp(Vector(10, 20), 0.5)
        assert v == Vector(5, 10)

    def test_lerp_extremo(self):
        v = Vector(0, 0).lerp(Vector(10, 20), 1.0)
        assert v == Vector(10, 20)


# ============================================================
# Relaciones geométricas
# ============================================================

class TestRelaciones:
    def test_is_parallel_true(self):
        assert Vector(2, 0).is_parallel(Vector(5, 0)) is True

    def test_is_parallel_false(self):
        assert Vector(1, 0).is_parallel(Vector(0, 1)) is False

    def test_is_perpendicular_true(self):
        assert Vector(1, 0).is_perpendicular(Vector(0, 1)) is True

    def test_is_perpendicular_false(self):
        assert Vector(1, 0).is_perpendicular(Vector(1, 1)) is False

    def test_is_parallel_zero_vector(self):
        assert Vector(0, 0).is_parallel(Vector(1, 0)) is True

    def test_is_parallel_3d(self):
        assert Vector(2, 4, 6).is_parallel(Vector(1, 2, 3)) is True

    def test_is_parallel_3d_false(self):
        assert Vector(1, 0, 0).is_parallel(Vector(0, 1, 0)) is False


# ============================================================
# Igualdad y hash
# ============================================================

class TestIgualdadHash:
    def test_eq_mismo(self):
        assert Vector(1, 2) == Vector(1.0, 2.0)

    def test_eq_tolerancia(self):
        assert Vector(1, 2) == Vector(1.0000000005, 2.0)

    def test_neq(self):
        assert Vector(1, 2) != Vector(3, 4)

    def test_eq_otro_tipo(self):
        assert (Vector(1, 2) == "vector") is False

    def test_hash_consistente(self):
        assert hash(Vector(1, 2)) == hash(Vector(1.0, 2.0))

    def test_hash_en_set(self):
        s = {Vector(1, 2), Vector(1, 2), Vector(3, 4)}
        assert len(s) == 2

    def test_almost_equal_explicito(self):
        assert Vector(1, 2).almost_equal(Vector(1.1, 2), tol=0.2) is True

    def test_almost_equal_fuera(self):
        assert Vector(1, 2).almost_equal(Vector(1.1, 2), tol=0.05) is False

    def test_almost_equal_otro_tipo(self):
        assert Vector(0, 0).almost_equal("string") is NotImplemented


# ============================================================
# Operadores
# ============================================================

class TestOperadores:
    def test_add(self):
        assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)

    def test_sub(self):
        assert Vector(5, 7) - Vector(3, 4) == Vector(2, 3)

    def test_mul_escalar(self):
        assert Vector(2, 3) * 2 == Vector(4, 6)

    def test_rmul_escalar(self):
        assert 2 * Vector(2, 3) == Vector(4, 6)

    def test_truediv(self):
        assert Vector(4, 6) / 2 == Vector(2, 3)

    def test_truediv_zero_raise(self):
        with pytest.raises(PrecisionError):
            Vector(1, 2) / 0.0

    def test_neg(self):
        assert -Vector(3, -4) == Vector(-3, 4)

    def test_pos(self):
        v = Vector(3, 4)
        assert +v == v
        assert (+v) is not v

    def test_add_3d(self):
        assert Vector(1, 2, 3) + Vector(4, 5, 6) == Vector(5, 7, 9)

    def test_sub_3d(self):
        assert Vector(5, 7, 9) - Vector(1, 2, 3) == Vector(4, 5, 6)


# ============================================================
# Operadores Point-Vector
# ============================================================

class TestOperadoresPointVector:
    def test_point_minus_point_es_vector(self):
        r = Point(10, 20) - Point(3, 4)
        assert isinstance(r, Vector)
        assert r == Vector(7, 16)

    def test_point_plus_vector_es_point(self):
        r = Point(10, 20) + Vector(3, 4)
        assert isinstance(r, Point)
        assert r == Point(13, 24)

    def test_point_minus_vector_es_point(self):
        r = Point(10, 20) - Vector(3, 4)
        assert isinstance(r, Point)
        assert r == Point(7, 16)

    def test_vector_plus_point_es_point(self):
        r = Vector(3, 4) + Point(10, 20)
        assert isinstance(r, Point)
        assert r == Point(13, 24)

    def test_point_plus_point_typeerror(self):
        with pytest.raises(TypeError):
            Point(1, 2) + Point(3, 4)

    def test_point_3d_minus_point_3d(self):
        r = Point(1, 2, 3) - Point(4, 5, 6)
        assert r == Vector(-3, -3, -3)


# ============================================================
# Serialización
# ============================================================

class TestSerializacion:
    def test_to_tuple_2d(self):
        assert Vector(1, 2).to_tuple() == (1.0, 2.0, 0.0)

    def test_to_tuple_3d(self):
        assert Vector(1, 2, 3).to_tuple() == (1.0, 2.0, 3.0)

    def test_to_dict(self):
        assert Vector(1, 2, 3).to_dict() == {"dx": 1.0, "dy": 2.0, "dz": 3.0}

    def test_from_tuple_2(self):
        assert Vector.from_tuple((3, 4)) == Vector(3, 4)

    def test_from_tuple_3(self):
        assert Vector.from_tuple((1, 2, 3)).dz == 3.0

    def test_from_tuple_2_raise(self):
        with pytest.raises(GeometryError):
            Vector.from_tuple((1,))

    def test_from_tuple_4_raise(self):
        with pytest.raises(GeometryError):
            Vector.from_tuple((1, 2, 3, 4))

    def test_from_tuple_string_raise(self):
        with pytest.raises(GeometryError):
            Vector.from_tuple("bad")

    def test_from_dict(self):
        assert Vector.from_dict({"dx": 1, "dy": 2}) == Vector(1, 2)

    def test_from_dict_con_dz(self):
        assert Vector.from_dict({"dx": 1, "dy": 2, "dz": 3}).dz == 3.0

    def test_from_dict_falta_dx_raise(self):
        with pytest.raises(KeyError):
            Vector.from_dict({"dy": 2})

    def test_to_json(self):
        import json
        s = Vector(1, 2).to_json()
        d = json.loads(s)
        assert d == {"dx": 1.0, "dy": 2.0, "dz": 0.0}

    def test_from_json(self):
        v = Vector.from_json('{"dx": 3, "dy": 4}')
        assert v == Vector(3, 4)

    def test_to_wkt_raise(self):
        with pytest.raises(GeometryError):
            Vector(1, 2).to_wkt()

    def test_roundtrip_dict(self):
        v = Vector(1.5, 2.5, 3.5)
        assert Vector.from_dict(v.to_dict()) == v

    def test_roundtrip_json(self):
        v = Vector(10, 20)
        assert Vector.from_json(v.to_json()) == v


# ============================================================
# Geometry contract
# ============================================================

class TestGeometryContract:
    def test_isinstance_geometry(self):
        assert isinstance(Vector(1, 2), Geometry)

    def test_copy(self):
        v = Vector(1, 2, 3)
        c = v.copy()
        assert c == v
        assert c is not v

    def test_is_valid(self):
        assert Vector(1, 2).is_valid is True

    def test_check_invariants(self):
        Vector(1, 2).check_invariants()

    def test_str_equals_repr(self):
        v = Vector(1.5, 2.5)
        assert str(v) == repr(v)

    def test_from_dict_to_dict_roundtrip(self):
        v = Vector.from_dict(Vector(10, 20).to_dict())
        assert v == Vector(10, 20)

    def test_from_points_3d(self):
        v = Vector.from_points(Point(0, 0, 0), Point(1, 2, 3))
        assert v.dz == 3.0

    def test_is_valid_invalid_vector(self):
        v = Vector(1, 2)
        object.__setattr__(v, "_dx", float("nan"))
        assert v.is_valid is False


# ============================================================
# Casos límite
# ============================================================

class TestCasosLimite:
    def test_add_zero_vector(self):
        assert Vector(3, 4) + Vector(0, 0) == Vector(3, 4)

    def test_sub_self(self):
        v = Vector(3, 4)
        assert v - v == Vector(0, 0)

    def test_mul_by_zero(self):
        assert Vector(3, 4) * 0 == Vector(0, 0)

    def test_mul_by_one(self):
        assert Vector(3, 4) * 1 == Vector(3, 4)

    def test_neg_zero(self):
        assert -Vector(0, 0) == Vector(0, 0)

    def test_angle_zero_vector(self):
        assert Vector(0, 0).angle == 0.0

    def test_dot_with_zero(self):
        assert Vector(3, 4).dot(Vector(0, 0)) == 0.0

    def test_cross_with_zero(self):
        assert Vector(3, 4).cross(Vector(0, 0)) == 0.0

    def test_angle_to_mismo_vector(self):
        assert Vector(5, 12).angle_to(Vector(5, 12)) == pytest.approx(0.0)

    def test_rotate_por_cero(self):
        v = Vector(3, 4).rotate(0.0)
        assert v == Vector(3, 4)

    def test_lerp_t_cero(self):
        assert Vector(1, 2).lerp(Vector(10, 20), 0.0) == Vector(1, 2)

    def test_lerp_t_uno(self):
        assert Vector(1, 2).lerp(Vector(10, 20), 1.0) == Vector(10, 20)

    def test_signed_angle_to_self(self):
        assert Vector(3, 4).signed_angle_to(Vector(3, 4)) == pytest.approx(0.0)


# ============================================================
# from_angle
# ============================================================

class TestFromAngle:
    def test_from_angle_0(self):
        assert Vector.from_angle(0.0) == Vector(1, 0)

    def test_from_angle_90(self):
        v = Vector.from_angle(math.pi / 2, 5.0)
        assert v.almost_equal(Vector(0, 5))

    def test_from_angle_180(self):
        v = Vector.from_angle(math.pi, 2.0)
        assert v.almost_equal(Vector(-2, 0))

    def test_from_angle_length_cero(self):
        v = Vector.from_angle(0.0, 0.0)
        assert v == Vector(0, 0)

    def test_from_angle_negative_length_raise(self):
        with pytest.raises(Exception):
            Vector.from_angle(0.0, -1.0)


# ============================================================
# Error handling
# ============================================================

class TestErrores:
    def test_add_point_returns_point(self):
        r = Vector(1, 2) + Point(10, 20)
        assert isinstance(r, Point)
        assert r == Point(11, 22)

    def test_sub_typeerror(self):
        with pytest.raises(TypeError):
            Vector(1, 2) - Point(0, 0)

    def test_mul_typeerror(self):
        with pytest.raises(Exception):
            Vector(1, 2) * "a"

    def test_truediv_nan_raise(self):
        with pytest.raises(Exception):
            Vector(1, 2) / float("nan")

    def test_rotate_nan_raise(self):
        with pytest.raises(Exception):
            Vector(1, 0).rotate(float("nan"))
