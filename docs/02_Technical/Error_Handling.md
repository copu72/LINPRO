# Error Handling

## Principios

1. **Fail fast**: validar en el constructor, no esperar a que un valor inválido se propague.
2. **Excepciones propias**: cada módulo define su jerarquía de excepciones.
3. **Nunca silenciar errores**: no capturar `Exception` genérico, no pasar con `pass`.
4. **Mensajes descriptivos**: incluir nombre del parámetro y valor recibido.

## Jerarquía

```
GeometryError (Exception)
├── InvalidCoordinateError   — NaN, inf, tipo incorrecto
├── PrecisionError           — error de precisión
└── ValidationError          — fallo de validación
```

## Reglas por módulo

| Módulo | Excepción base |
|---|---|
| `geometry` | `GeometryError` |
| `core` | `CoreError` |
| `domain` | `DomainError` |
| `io` | `IOError` |

## Guía rápida

```python
# Correcto
if math.isnan(value):
    raise InvalidCoordinateError(f"x must not be NaN, got {value}")

# Incorrecto
if math.isnan(value):
    raise ValueError("x is NaN")

# Correcto
try:
    result = risky_operation()
except GeometryError:
    raise  # propagar

# Incorrecto
try:
    result = risky_operation()
except Exception:
    pass  # ❌ silenciar
```
