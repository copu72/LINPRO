# Kernel — Design

## Tolerance

```
Tolerance (class registry)
├── .math      → ToleranceLevel(ε=1e-12)   — arithmetic
├── .geometry  → ToleranceLevel(ε=1e-9)    — comparisons (default)
└── .visual    → ToleranceLevel(ε=1e-6)    — display/CAD

Cada ToleranceLevel tiene:
  .equals(a, b)
  .is_zero(v)
  .distance_equals(d1, d2)
  .angle_equals(a1, a2)
  .less_or_equal(a, b)
  .greater_or_equal(a, b)
  .in_range(value, low, high)
```

Los métodos de clase en `Tolerance` delegan a `Tolerance.geometry`.

## Validators

Tres clases independientes, cada una con métodos `assert_*` y `is_*`:

```
NumericValidator     → finite, positive, range
CoordinateValidator  → 2D, 3D, assert_valid
GeometryValidator    → type, not none, valid geometry
```

## Geometry (ABC)

```
Geometry (ABC)
├── @property dimension      → int
├── @property is_empty       → bool
├── @property bbox           → Geometry
├── @property is_valid       → bool
├── copy()                   → Geometry
├── to_dict()                → dict
├── from_dict(data)          → Geometry (classmethod)
├── to_json(**kwargs)        → str (concrete)
├── from_json(data)          → Geometry (concrete)
├── to_wkt()                 → str
├── __eq__()                 → bool
└── __repr__()               → str
```
