# Vector — Examples

```python
from linpro.geometry import Vector, Point

# Creación
v = Vector(3.0, 4.0)
print(v.length)       # 5.0
print(v.angle)        # 0.9272952180016122 rad (~53.13°)

# Normalizado
u = v.normalized
print(u.length)       # 1.0
print(u.dx, u.dy)     # 0.6, 0.8

# Vector nulo
zero = Vector(0, 0)
print(zero.length)    # 0.0
print(zero.normalized)  # Vector(0.000, 0.000)

# Operaciones
a = Vector(1, 0)
b = Vector(0, 1)
print(a.dot(b))       # 0.0
print(a.cross(b))     # 1.0
print(a.angle_to(b))  # 1.5707963267948966 (π/2)

# Rotación
v = Vector(1, 0).rotate(1.5708)  # ~Vector(0, 1)

# Perpendicular
v = Vector(2, 3).perpendicular()  # Vector(-3, 2)

# Desde puntos
p1 = Point(10, 20)
p2 = Point(13, 24)
v = Vector.from_points(p1, p2)    # Vector(3, 4)

# Desde ángulo
v = Vector.from_angle(0.0, 5.0)                 # Vector(5, 0)
v = Vector.from_angle(3.14159 / 2, 10.0)        # ~Vector(0, 10)

# Aritmética
print(Vector(1, 2) + Vector(3, 4))  # Vector(4.000, 6.000)
print(Vector(5, 7) - Vector(2, 3))  # Vector(3.000, 4.000)
print(Vector(2, 3) * 2.5)           # Vector(5.000, 7.500)

# Tolerancia
print(Vector(1.0, 2.0) == Vector(1.000000001, 2.0))  # True

# Hashable
s = {Vector(1, 0), Vector(0, 1), Vector(1, 0)}
print(len(s))         # 2
```