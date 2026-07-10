# Kernel — API Reference

## Constants

```python
from linpro.geometry.kernel import (
    VERSION,           # "0.3.0-dev"
    DEFAULT_CRS,       # "EPSG:25830"
    DEFAULT_PRECISION, # 9
    EPSILON_MATH,      # 1e-12
    EPSILON_GEOMETRY,  # 1e-9
    EPSILON_VISUAL,    # 1e-6
    ANGLE_EPSILON,     # 1e-10
    DISTANCE_EPSILON,  # 1e-8
    MAX_ITERATIONS,    # 1000
)
```

## Tolerance

```python
# Levels (ToleranceLevel instances)
Tolerance.math      # ε=1e-12
Tolerance.geometry  # ε=1e-9 (default)
Tolerance.visual    # ε=1e-6

# Methods on each level
Tolerance.geometry.equals(a, b)           # isclose with own ε
Tolerance.math.is_zero(v)                 # isclose(v, 0, ε=1e-12)
Tolerance.visual.distance_equals(d1, d2)  # isclose with own ε
Tolerance.geometry.angle_equals(a1, a2)   # isclose with angle_ε

# Convenience methods (delegate to .geometry)
Tolerance.equals(a, b)
Tolerance.is_zero(v)
Tolerance.distance_equals(d1, d2)
Tolerance.angle_equals(a1, a2)
```

## Validators

```python
NumericValidator.assert_finite(value, name="value")
NumericValidator.is_finite(value) → bool
NumericValidator.assert_positive(value, name="value")
NumericValidator.assert_range(value, low, high, name="value")

CoordinateValidator.assert_valid(x, y, z=None)
CoordinateValidator.assert_2d(x, y)
CoordinateValidator.assert_3d(x, y, z)

GeometryValidator.assert_type(value, type, name="value")
GeometryValidator.assert_not_none(value, name="value")
GeometryValidator.assert_valid_geometry(geometry)
```

## Geometry (ABC)

```python
class Geometry(ABC):
    _EPSILON: float = 1e-9

    # Abstract
    @property dimension → int
    @property is_empty → bool
    @property bbox → Geometry
    @property is_valid → bool
    def copy() → Geometry
    def to_dict() → dict
    @classmethod from_dict(data) → Geometry
    def to_wkt() → str
    def __eq__(other) → bool
    def __repr__() → str

    # Concrete
    def to_json(**kwargs) → str
    @classmethod from_json(data) → Geometry
    def __str__() → str
```
