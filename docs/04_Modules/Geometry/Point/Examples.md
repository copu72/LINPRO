# Point — Examples

```python
from linpro.geometry import Point

# Creación
p1 = Point(10.0, 20.0)
p2 = Point(10.0, 20.0, 5.0)

# Coordenadas
print(p1.x, p1.y, p1.z)   # 10.0 20.0 0.0
print(p2.z)                # 5.0

# Distancia
p3 = Point(13.0, 24.0)
dist = p1.distance_to(p3)
print(dist)                # 5.0

# Igualdad con tolerancia
print(Point(1.0, 2.0) == Point(1.000000001, 2.0))  # True (1e-9)

# Serialización
t = p1.to_tuple()          # (10.0, 20.0, 0.0)
d = p1.to_dict()           # {"x": 10.0, "y": 20.0, "z": 0.0}
s = p1.to_json()           # '{"x": 10.0, "y": 20.0, "z": 0.0}'
wkt = p1.to_wkt()          # "POINT (10 20)"

# Deserialización
p4 = Point.from_tuple((1.0, 2.0))
p5 = Point.from_dict({"x": 1.0, "y": 2.0})
p6 = Point.from_json('{"x": 1.0, "y": 2.0, "z": 3.0}')

# Hashable
s = {Point(0, 0), Point(1, 1), Point(0, 0)}
print(len(s))              # 2

# Inmutable
p = Point(1, 2)
# p.x = 3  # ❌ AttributeError
```