# RFC-0001: Geometry Kernel

**Estado:** Aprobado
**Autor:** Software Architect
**Fecha:** 2026-07-09

---

## Objetivo

Definir e implementar el núcleo matemático del Geometry Engine de LINPRO:
tolerancias, validaciones, constantes globales y el contrato abstracto
`Geometry` que toda entidad geométrica debe cumplir.

## Motivación

LINPRO necesita un sistema de coordenadas y tolerancias predecible desde
el primer día. Sin el Kernel, las primitivas (Point, Vector, Segment)
implementarían cada una su propia lógica de comparación y validación,
generando inconsistencias difíciles de corregir más adelante.

Tener una clase base `Geometry` con contratos obligatorios garantiza que
todas las entidades geométricas compartan la misma interfaz y el mismo
comportamiento fundamental.

## Diseño

### Componentes

```
kernel/
├── constants.py       — Constantes globales (EPSILONs, VERSION, DEFAULT_CRS, ...)
├── tolerance.py       — ToleranceLevel (ε) y Tolerance (3 niveles: math, geometry, visual)
├── validation.py      — NumericValidator, CoordinateValidator, GeometryValidator
├── geometry.py        — Geometry(ABC) — clase base abstracta
└── __init__.py        — Reexporta todo lo público
```

### Tolerancias

Tres niveles con epsilon por defecto para comparaciones floats:

| Nivel | ε | Ángulo ε | Contexto |
|---|---|---|---|
| math | 1e-12 | 1e-12 | Aritmética interna |
| geometry | 1e-9 | 1e-10 | Comparación de entidades (defecto) |
| visual | 1e-6 | 1e-8 | Display / CAD snap |

### Geometry (ABC)

```python
class Geometry(ABC):
    # Propiedades abstractas
    @property dimension -> int
    @property is_empty -> bool
    @property bbox -> Geometry
    @property is_valid -> bool

    # Métodos abstractos
    copy() -> Geometry
    to_dict() -> dict
    from_dict(data) -> Geometry (classmethod)
    to_wkt() -> str
    __eq__(other) -> bool
    __repr__() -> str

    # Métodos concretos
    to_json(**kwargs) -> str         # usa to_dict
    from_json(data) -> Geometry       # usa from_dict
```

### Validadores

Tres clases con métodos `assert_*` que lanzan `InvalidCoordinateError` o `ValidationError`:

- `NumericValidator`: assert_finite, is_finite, assert_positive, assert_range
- `CoordinateValidator`: assert_valid (2D/3D), assert_2d, assert_3d
- `GeometryValidator`: assert_type, assert_not_none, assert_valid_geometry

## API

Ver `docs/04_Modules/Geometry/Kernel/API.md`.

## Alternativas consideradas

| Alternativa | Decisión | Razón |
|---|---|---|
| Funciones sueltas vs clases | Clases (Tolerance, Validators) | Agrupación lógica, extensibilidad |
| EPSILON única vs tres niveles | Tres niveles | Matemática, geométrica y visual requieren distinta precisión |
| Protocol vs ABC | ABC | Queremos herencia de implementación, no solo estructural |
| Excepciones en un archivo vs uno por clase | Un archivo por excepción | Claridad, imports selectivos |
| Geometry con métodos concretos | to_json/from_json concretos | No tienen por qué reimplementarse en cada subclase |

## Decisiones

1. `Tolerance.math`, `.geometry`, `.visual` son instancias de `ToleranceLevel`.
2. Los métodos de clase `Tolerance.equals()`, etc. delegan a `Tolerance.geometry`.
3. Los validadores son clases con métodos `assert_*` (lanzan excepción) e `is_*` (devuelven bool).
4. `Geometry` usa `abc.ABC` y `@abstractmethod`.
5. `to_json/from_json` son concretos en `Geometry` y usan `to_dict/from_dict`.
6. Las excepciones heredan de `GeometryError` y residen en archivos individuales.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Epsilons mal elegidos obligan a recalibrar | Se definen en constants.py, un solo punto de cambio |
| Demasiadas clases abstractas complican | Solo Geometry es ABC; el resto son clases concretas |
| Validadores demasiado genéricos | Cada validador tiene responsabilidad específica y acotada |

## Pruebas

- `tests/unit/geometry/kernel/test_tolerance.py` — 26 tests (todos pasando)
- `tests/unit/geometry/kernel/test_validators.py` — 22 tests (todos pasando)
- `tests/unit/geometry/kernel/test_geometry.py` — 6 tests (todos pasando)

Cobertura: cobertura completa de los módulos `kernel/tolerance.py`,
`kernel/validation.py`, `kernel/geometry.py` y `kernel/constants.py`.

---

*Fin del RFC-0001*
