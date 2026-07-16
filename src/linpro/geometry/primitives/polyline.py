"""TASK-0006: Polyline — Engineering Axis.

Entidad central de LINPRO.
No es una simple lista de segmentos: es un eje de ingeniería.

Conoce su geometría, topología, y responde preguntas de ingeniería:
PK, proyección, azimuth, normal, etc.

Delega en:
  Operators → Segment → Vector → Point

Internal structure:
  Polyline
  ├── vertices          (list[Point])
  ├── segments          (list[Segment]) — precomputado
  ├── cumulative_lengths (list[float]) — precomputado
  ├── bbox              (BoundingBox)  — precomputado
  └── total_length      (float)        — precomputado
"""

from __future__ import annotations

import bisect
from typing import Any

from linpro.geometry.exceptions import GeometryError
from linpro.geometry.kernel.constants import EPSILON_GEOMETRY
from linpro.geometry.kernel.geometry import Geometry
from linpro.geometry.kernel.validation import GeometryValidator
from linpro.geometry.primitives.bbox import BoundingBox
from linpro.geometry.primitives.pk import PK
from linpro.geometry.primitives.point import Point
from linpro.geometry.primitives.segment import Segment
from linpro.geometry.primitives.vector import Vector


class Polyline(Geometry):
    """Engineering Axis — entidad central de LINPRO.

    Representa un eje de ingeniería lineal compuesto por vértices
    y segmentos. No es una simple lista de segmentos: conoce su
    topología, responde preguntas de PK, proyección, azimuth y normal.

    Args:
        points: Lista de al menos 2 Point.
        closed: True si la polilínea es cerrada (no implementado aún).

    Example:
        >>> pts = [Point(0,0), Point(100,0), Point(100,100)]
        >>> axis = Polyline(pts)
        >>> axis.length
        200.0
        >>> axis.point_at_pk(PK(50))
        Point(50.0, 0.0, 0.0)
    """

    _EPSILON: float = EPSILON_GEOMETRY

    def __init__(
        self,
        points: list[Point] | tuple[Point, ...],
        closed: bool = False,
    ) -> None:
        if len(points) < 2:
            raise GeometryError(
                f"Polyline requires at least 2 points, got {len(points)}"
            )
        for i, p in enumerate(points):
            GeometryValidator.assert_type(p, Point, f"points[{i}]")

        self._vertices: list[Point] = list(points)
        self._closed: bool = closed
        self._compute_caches()

    # ==================================================================
    #  CACHES
    # ==================================================================

    def _compute_caches(self) -> None:
        vs = self._vertices
        n = len(vs)

        segs = [Segment(vs[i], vs[i + 1]) for i in range(n - 1)]
        self._segments: list[Segment] = segs

        cum = [0.0]
        for s in segs:
            cum.append(cum[-1] + s.length)
        self._cumulative_lengths: list[float] = cum

        self._total_length: float = cum[-1]

        xs = [p.x for p in vs]
        ys = [p.y for p in vs]
        self._bbox: BoundingBox = BoundingBox(
            min(xs), min(ys), max(xs), max(ys),
        )

    # ==================================================================
    #  CONSTRUCTORES ALTERNATIVOS
    # ==================================================================

    @classmethod
    def from_segments(cls, segments: list[Segment]) -> Polyline:
        if not segments:
            raise GeometryError("from_segments requires at least 1 segment")
        pts = [segments[0].start]
        for s in segments:
            if not s.start.almost_equal(pts[-1], cls._EPSILON):
                raise GeometryError(
                    f"Segments are not connected: {pts[-1]} != {s.start}"
                )
            pts.append(s.end)
        return cls(pts)

    @classmethod
    def from_dxf(cls, path: str, layer: str | None = None) -> Polyline:
        try:
            import ezdxf
        except ImportError:
            raise GeometryError(
                "ezdxf is required for DXF import. Install with: pip install ezdxf"
            )

        doc = ezdxf.readfile(path)
        msp = doc.modelspace()

        for entity in msp:
            if entity.dxftype() == "LWPOLYLINE":
                if layer is not None and entity.dxf.layer != layer:
                    continue
                pts_xy = entity.get_points("xy")
                points = [Point(x, y) for x, y in pts_xy]
                return cls(points)

            if entity.dxftype() == "POLYLINE":
                if layer is not None and entity.dxf.layer != layer:
                    continue
                try:
                    points = [
                        Point(float(v.dxf.x), float(v.dxf.y), float(v.dxf.z))
                        for v in entity.vertices
                    ]
                except Exception:
                    pts = [
                        Point(float(v.dxf.location.x),
                              float(v.dxf.location.y),
                              float(v.dxf.location.z))
                        for v in entity.vertices
                    ]
                    points = pts
                return cls(points)

            if entity.dxftype() == "LINE":
                if layer is not None and entity.dxf.layer != layer:
                    continue
                return cls([
                    Point(
                        entity.dxf.start.x,
                        entity.dxf.start.y,
                        entity.dxf.start.z,
                    ),
                    Point(
                        entity.dxf.end.x,
                        entity.dxf.end.y,
                        entity.dxf.end.z,
                    ),
                ])

        raise GeometryError(f"No polyline or line found in DXF: {path}")

    # ==================================================================
    #  PROPIEDADES — Geometría
    # ==================================================================

    @property
    def vertices(self) -> tuple[Point, ...]:
        return tuple(self._vertices)

    @property
    def segments(self) -> tuple[Segment, ...]:
        return tuple(self._segments)

    @property
    def length(self) -> float:
        return self._total_length

    @property
    def bbox(self) -> Geometry:
        return self._bbox

    @property
    def start(self) -> Point:
        return self._vertices[0]

    @property
    def end(self) -> Point:
        return self._vertices[-1]

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def segment_count(self) -> int:
        return len(self._segments)

    @property
    def center(self) -> Point:
        cx = sum(p.x for p in self._vertices) / self.vertex_count
        cy = sum(p.y for p in self._vertices) / self.vertex_count
        cz = sum(p.z for p in self._vertices) / self.vertex_count
        return Point(cx, cy, cz)

    @property
    def dimension(self) -> int:
        return 1

    @property
    def is_empty(self) -> bool:
        return False

    @property
    def is_valid(self) -> bool:
        try:
            self.check_invariants()
            return True
        except Exception:
            return False

    @property
    def cumulative_lengths(self) -> tuple[float, ...]:
        return tuple(self._cumulative_lengths)

    # ==================================================================
    #  TOPOLOGÍA
    # ==================================================================

    def segment_at(self, index: int) -> Segment:
        if index < 0 or index >= len(self._segments):
            raise GeometryError(
                f"Segment index {index} out of range [0, {len(self._segments)})"
            )
        return self._segments[index]

    def vertex_at(self, index: int) -> Point:
        if index < 0 or index >= len(self._vertices):
            raise GeometryError(
                f"Vertex index {index} out of range [0, {len(self._vertices)})"
            )
        return self._vertices[index]

    def pk_at_vertex(self, index: int) -> PK:
        if index < 0 or index > len(self._segments):
            raise GeometryError(
                f"Vertex index {index} out of range [0, {len(self._segments)}]"
            )
        return PK(self._cumulative_lengths[index])

    # ==================================================================
    #  INGENIERÍA — PK Engine
    # ==================================================================

    def _pk_val(self, pk: PK | int | float) -> float:
        return float(pk)

    def _check_pk_range(self, pk_val: float) -> None:
        if pk_val < -EPSILON_GEOMETRY or pk_val > self._total_length + EPSILON_GEOMETRY:
            raise GeometryError(
                f"PK {pk_val} out of range [0, {self._total_length}]"
            )

    def _segment_index_at_pk(self, pk_val: float) -> int:
        pk_val = max(0.0, min(pk_val, self._total_length))
        cum = self._cumulative_lengths
        idx = bisect.bisect_right(cum, pk_val) - 1
        return max(0, min(idx, len(self._segments) - 1))

    def point_at_pk(self, pk: PK | int | float) -> Point:
        pk_val = self._pk_val(pk)
        self._check_pk_range(pk_val)

        idx = self._segment_index_at_pk(pk_val)
        seg = self._segments[idx]
        local_pk = pk_val - self._cumulative_lengths[idx]
        t = local_pk / seg.length if seg.length > EPSILON_GEOMETRY else 0.0
        t = max(0.0, min(1.0, t))

        return Point(
            seg.start.x + t * seg.vector.dx,
            seg.start.y + t * seg.vector.dy,
            seg.start.z + t * seg.vector.dz,
        )

    def pk_of(self, point: Point) -> PK:
        from linpro.geometry.operators.closest_point import closest_point as _cp

        GeometryValidator.assert_type(point, Point, "point")

        min_dist = float("inf")
        best_pk = 0.0

        for i, seg in enumerate(self._segments):
            cp = _cp(point, seg)
            d = point.distance_to(cp)
            local_dist = cp.distance_to(seg.start)
            candidate_pk = self._cumulative_lengths[i] + local_dist

            if d < min_dist - EPSILON_GEOMETRY:
                min_dist = d
                best_pk = candidate_pk

        return PK(best_pk)

    def project(self, point: Point) -> Point:
        from linpro.geometry.operators.projection import project as _proj

        GeometryValidator.assert_type(point, Point, "point")

        min_dist = float("inf")
        best = point

        for seg in self._segments:
            proj = _proj(point, seg)
            d = point.distance_to(proj)
            if d < min_dist:
                min_dist = d
                best = proj

        return best

    def closest_point(self, point: Point) -> Point:
        from linpro.geometry.operators.closest_point import closest_point as _cp

        GeometryValidator.assert_type(point, Point, "point")

        min_dist = float("inf")
        best = point

        for seg in self._segments:
            cp = _cp(point, seg)
            d = point.distance_to(cp)
            if d < min_dist:
                min_dist = d
                best = cp

        return best

    def segment_at_pk(self, pk: PK | int | float) -> Segment:
        pk_val = self._pk_val(pk)
        self._check_pk_range(pk_val)
        idx = self._segment_index_at_pk(pk_val)
        return self._segments[idx]

    def azimuth_at_pk(self, pk: PK | int | float) -> float:
        seg = self.segment_at_pk(pk)
        return seg.azimuth

    def normal_at_pk(self, pk: PK | int | float) -> Vector:
        seg = self.segment_at_pk(pk)
        perp = seg.vector.perpendicular
        return perp.normalized if not perp.is_zero else perp

    # ==================================================================
    #  MUTACIÓN
    # ==================================================================

    def reverse(self) -> Polyline:
        return Polyline(list(reversed(self._vertices)), closed=self._closed)

    def copy(self) -> Polyline:
        return Polyline([v.copy() for v in self._vertices], closed=self._closed)

    def append(self, point: Point) -> None:
        GeometryValidator.assert_type(point, Point, "point")
        self._vertices.append(point)

        new_seg = Segment(self._vertices[-2], self._vertices[-1])
        self._segments.append(new_seg)
        self._cumulative_lengths.append(self._total_length + new_seg.length)
        self._total_length += new_seg.length

        self._bbox = self._bbox.union(
            BoundingBox(point.x, point.y, point.x, point.y)
        )

    def extend(self, points: list[Point]) -> None:
        for p in points:
            self.append(p)

    def simplify(self, tolerance: float = 1.0) -> Polyline:
        _ = tolerance
        return self.copy()

    def split(self, pk: PK | int | float) -> tuple[Polyline, Polyline]:
        pk_val = self._pk_val(pk)
        if pk_val <= EPSILON_GEOMETRY or pk_val >= self._total_length - EPSILON_GEOMETRY:
            raise GeometryError(
                f"Cannot split at PK {pk_val}: must be strictly internal (0, {self._total_length})"
            )

        idx = self._segment_index_at_pk(pk_val)
        seg = self._segments[idx]
        local_pk = pk_val - self._cumulative_lengths[idx]
        t = local_pk / seg.length if seg.length > EPSILON_GEOMETRY else 0.0

        split_pt = Point(
            seg.start.x + t * seg.vector.dx,
            seg.start.y + t * seg.vector.dy,
            seg.start.z + t * seg.vector.dz,
        )

        left_verts = list(self._vertices[: idx + 1]) + [split_pt]
        right_verts = [split_pt] + list(self._vertices[idx + 1 :])

        return Polyline(left_verts), Polyline(right_verts)

    def merge(self, other: Polyline) -> Polyline:
        joined = list(self._vertices) + list(other._vertices)
        return Polyline(joined)

    # ==================================================================
    #  SERIALIZACIÓN
    # ==================================================================

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "Polyline",
            "vertices": [v.to_dict() for v in self._vertices],
            "closed": self._closed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Polyline:
        verts = [Point.from_dict(v) for v in data["vertices"]]
        return cls(verts, closed=data.get("closed", False))

    def to_wkt(self) -> str:
        def _fmt(v: float) -> str:
            return str(v) if v != int(v) else str(int(v))

        coords = ", ".join(
            f"{_fmt(p.x)} {_fmt(p.y)}" for p in self._vertices
        )
        return f"LINESTRING ({coords})"

    # ==================================================================
    #  CONTRATO GEOMETRY
    # ==================================================================

    def check_invariants(self) -> None:
        if len(self._vertices) < 2:
            raise GeometryError(
                f"Polyline must have at least 2 vertices, got {len(self._vertices)}"
            )
        for i, p in enumerate(self._vertices):
            if not isinstance(p, Point):
                raise GeometryError(f"vertices[{i}] must be a Point")
        if len(self._segments) != len(self._vertices) - 1:
            raise GeometryError("segment count mismatch")
        if len(self._cumulative_lengths) != len(self._vertices):
            raise GeometryError("cumulative_lengths count mismatch")

    # ==================================================================
    #  ESPECIALES
    # ==================================================================

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polyline):
            return NotImplemented
        if self.vertex_count != other.vertex_count:
            return False
        if self._closed != other._closed:
            return False
        return all(
            a.almost_equal(b, self._EPSILON)
            for a, b in zip(self._vertices, other._vertices)
        )

    def __len__(self) -> int:
        return self.vertex_count

    def __iter__(self) -> Any:
        return iter(self._vertices)

    def __getitem__(self, index: int) -> Point:
        return self._vertices[index]

    def __repr__(self) -> str:
        return f"Polyline({self.vertex_count} vertices, {self._total_length:.3f} m)"

    def __str__(self) -> str:
        return f"Polyline({self.vertex_count} vertices, {self._total_length:.3f} m)"
