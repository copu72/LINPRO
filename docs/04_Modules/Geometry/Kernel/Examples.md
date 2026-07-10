# Kernel — Examples

```python
from linpro.geometry.kernel import (
    Tolerance,
    NumericValidator,
    CoordinateValidator,
    GeometryValidator,
)

# ---- Tolerance ----
a = 1.000000001
b = 1.0

# Different levels give different results
print(Tolerance.math.equals(a, b))       # False (ε=1e-12)
print(Tolerance.geometry.equals(a, b))   # True  (ε=1e-9)
print(Tolerance.visual.equals(a, b))     # True  (ε=1e-6)

# Zero check
print(Tolerance.math.is_zero(1e-13))     # True
print(Tolerance.geometry.is_zero(1e-8))  # False

# Distance
print(Tolerance.geometry.distance_equals(1000.0, 1000.000001))  # True

# Angle
print(Tolerance.geometry.angle_equals(1.57079633, 1.57079633))  # True

# Convenience (delegates to geometry)
print(Tolerance.equals(a, b))            # True

# ---- NumericValidator ----
NumericValidator.assert_finite(42.0)          # OK
NumericValidator.assert_finite("not a num")   # ❌ InvalidCoordinateError
NumericValidator.assert_positive(-1)          # ❌ InvalidCoordinateError
NumericValidator.assert_range(5, 0, 10)       # OK

# ---- CoordinateValidator ----
CoordinateValidator.assert_valid(100000.0, 500000.0)        # OK
CoordinateValidator.assert_valid(100000.0, 500000.0, 25.0)  # OK (with Z)
CoordinateValidator.assert_valid(float("nan"), 0.0)         # ❌

# ---- GeometryValidator ----
from linpro.geometry import Point
GeometryValidator.assert_type(Point(1,2), Point)  # OK
GeometryValidator.assert_not_none(Point(1,2))     # OK
```
