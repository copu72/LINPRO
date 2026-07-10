# Testing Guidelines

## Herramientas

- **Pytest** como runner.
- **pytest-cov** para cobertura.
- **pytest-benchmark** para benchmarks (futuro).

## Estructura

```
tests/
├── unit/             # Tests unitarios (una clase, un módulo)
│   └── geometry/
│       └── primitives/
│           └── test_point.py
├── integration/      # Tests de integración (varios módulos)
├── performance/      # Tests de rendimiento
└── regression/       # Tests de regresión (bugs corregidos)
```

## Por archivo

- Un archivo `test_<modulo>.py` por archivo `<modulo>.py`.
- Tests agrupados en clases por funcionalidad:

```python
class TestPointCreation:
class TestPointDistance:
class TestPointSerialization:
```

## Nombres

```python
def test_distance_to_returns_zero_for_same_point(self):
def test_from_dict_restores_exact_values(self):
def test_raises_error_for_nan_coordinate(self):
```

## Cobertura

| Componente | Mínimo |
|---|---|
| Geometry Engine | 95 % |
| Módulos de dominio | 90 % |
| Adaptadores IO | 80 % |
| GUI | 60 % |

## Qué testear

- ✅ Casos normales (happy path)
- ✅ Casos borde (cero, vacío, límite de tolerancia)
- ✅ Casos de error (NaN, inf, tipo incorrecto)
- ✅ Invariantes (inmutabilidad, hash, serialización inversa)
- ✅ Tolerancia (comparaciones cerca del límite)

## Qué NO testear

- ❌ Código trivial (getters simples)
- ❌ Funciones privadas (testear a través de la pública)
- ❌ Implementación (testear comportamiento, no cómo se hace)
