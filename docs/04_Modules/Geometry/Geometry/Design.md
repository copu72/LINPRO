# Geometry — Design

## Decisión: ABC vs Protocol

Se usa `abc.ABC` y `@abstractmethod` (no `Protocol`) porque queremos herencia de implementación:
los métodos `to_dict`, `to_wkt`, `check_invariants` no tienen sentido sin una implementación concreta
y queremos que Python los exija en tiempo de instanciación.

## Jerarquía

```
Geometry (ABC)
├── Point             — no hereda de Geometry en sentido estricto (es primitiva),
│                        pero implementa todos sus contratos.
├── Vector            — implementa contratos Geometry.
├── Segment           — implementa contratos Geometry.
├── BoundingBox       — implementa contratos Geometry.
└── Curve (ABC)       — extiende Geometry con point_at, length, project.
    ├── Line
    ├── Polyline
    ├── Arc
    └── Circle
```

## Diagrama de flujo de contratos

```
Geometry.almost_equal(other, tol)
  └── cada subclase implementa coordinate-wise math.isclose

Geometry.to_dict()
  └── cada subclase devuelve dict plano de sus atributos

Geometry.from_dict(data)
  └── cada subclase reconstruye desde dict

Geometry.to_wkt()
  └── cada subclase devuelve WKT según su tipo

Geometry.check_invariants()
  └── cada subclase verifica sus invariantes
```