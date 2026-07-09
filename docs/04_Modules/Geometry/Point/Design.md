# Point — Design

## Diseño

Point se implementa como una clase inmutable que almacena coordenadas como float y expone propiedades de solo lectura.

## Decisiones técnicas

| Decisión | Opción elegida | Alternativa descartada |
|---|---|---|
| Inmutabilidad | Propiedades de solo lectura, sin setters | Dataclass frozen (evitamos dependencia) |
| Almacenamiento | Atributos privados `_x`, `_y`, `_z` | NamedTuple (no permite validación) |
| Comparación | `isclose` con EPSILON global | `==` directo (falla con floats) |
| Validación | En `__init__` usando Validation.assert_finite | En propiedades (validación tardía) |
| z opcional | Default 0.0 | Siempre obligatorio (menos flexible) |

### Invariantes

1. `x`, `y`, `z` son siempre `float`
2. Ninguna coordenada es NaN o infinito
3. El objeto es inmutable
4. `__hash__` usa valores redondeados a 9 decimales
5. `__eq__` usa `math.isclose` con `EPSILON`

### Diagrama de flujo

```
__init__(x, y, z=0.0)
    │
    ├─ Validation.assert_finite(x, y, z)
    │
    └─ self._x, self._y, self._z = float(x), float(y), float(z)
           │
           ▼
    Instancia inmutable
           │
           ├─ .x, .y, .z (propiedades)
           ├─ distance_to(other) → float
           ├─ to_tuple() → (x, y, z)
           ├─ to_dict() → {"x": ..., "y": ..., "z": ...}
           ├─ to_wkt() → "POINT (x y)"
           ├─ to_json() → str
           ├─ from_tuple(t) → Point
           ├─ from_dict(d) → Point
           ├─ from_json(s) → Point
           └─ __eq__, __hash__, __repr__
```