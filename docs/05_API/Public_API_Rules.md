# Public API Rules

## 1. ¿Qué es público?

Es público todo lo que aparece en `__all__` de un módulo y todo lo que no empieza por `_`.

```python
class Point:          # pública
    _EPSILON = 1e-9   # privada (constante interna)
    _x: float         # privada (atributo interno)

    @property
    def x(self): ...  # pública (propiedad de solo lectura)

    def distance_to(self, other): ...  # pública
```

## 2. ¿Qué debe ser privado?

- Atributos internos (`_x`, `_points`, `_length`)
- Constantes de clase (`_EPSILON`)
- Métodos de ayuda interna (`_validate`, `_compute`)
- Implementaciones que pueden cambiar

## 3. ¿Qué debe ser público?

- Constructor (`__init__`)
- Propiedades de solo lectura
- Métodos de la interfaz (`distance_to`, `to_dict`, `to_wkt`)
- Métodos de clase (`from_dict`, `from_json`)

## 4. Reglas de `@property`

Usar `@property` cuando:
- El acceso es semánticamente un atributo (`.x`, `.length`, `.angle`).
- No requiere argumentos.
- Es barato de calcular (o está cachead).

NO usar `@property` cuando:
- El método tiene efectos secundarios.
- El método requiere argumentos.
- La operación es muy cara y no está cachead (usar método explícito `compute_`).

## 5. Reglas de métodos estáticos

Usar `@staticmethod` cuando:
- La función está relacionada con la clase pero no necesita acceso a `self` ni `cls`.
- Ejemplo: `Vector.from_angle`, `BoundingBox.from_points`.

## 6. Reglas de clases abstractas

Usar `abc.ABC` + `@abc.abstractmethod` cuando:
- Varias clases comparten un contrato pero no una implementación.
- Queremos que Python obligue a implementar ciertos métodos.
- Ejemplo: `Geometry` → `almost_equal`, `to_dict`, `from_dict`, `to_wkt`, `check_invariants`.

## 7. Estabilidad de la API

| Nivel | Significado | Fase |
|---|---|---|
| `internal` | Puede cambiar sin aviso. Prefijo `_`. | Siempre |
| `experimental` | Puede cambiar, pero se anuncia. | Sprint activo |
| `stable` | No cambia sin deprecación. | Release ≥ 0.3.0 |

## 8. Prohibiciones

- ❌ No exponer atributos privados como públicos para "ahorrar código".
- ❌ No añadir métodos públicos "por si acaso" (YAGNI).
- ❌ No cambiar la firma de un método público sin deprecación.
- ❌ No usar `_` como prefijo en métodos que son parte del contrato público.
