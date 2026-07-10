# Architecture Principles

## SOLID en LINPRO

### S — Single Responsibility

Cada clase tiene una única responsabilidad. `Point` representa coordenadas. `Polyline` representa una secuencia de puntos. `Tolerance` gestiona comparaciones. Si una clase hace dos cosas, se divide.

**Ejemplo LINPRO:** `Point` no sabe exportar a Excel. `Point` no sabe calcular buffers. `Point` solo sabe ser un punto.

### O — Open/Closed

Las clases están abiertas a extensión pero cerradas a modificación. Se extienden por composición o herencia (Curve → Polyline), no modificando el código existente.

**Ejemplo LINPRO:** Si queremos un nuevo tipo de curva, heredamos de `Curve`. No tocamos `Polyline`.

### L — Liskov Substitution

Las subclases deben poder sustituir a sus clases base sin alterar el comportamiento del programa.

**Ejemplo LINPRO:** Donde se espera una `Curve`, debe poder usarse una `Line` o `Polyline` sin cambiar el código cliente.

### I — Interface Segregation

Interfaces pequeñas y específicas. `Geometry` define `to_dict`, `from_dict`, `to_wkt`, `check_invariants`. No métodos que solo aplican a curvas como `point_at`.

### D — Dependency Inversion

Los módulos de alto nivel no dependen de módulos de bajo nivel. Ambos dependen de abstracciones.

**Ejemplo LINPRO:** `domain` depende de `geometry.kernel` (abstracción), no de `geometry.primitives.point` (implementación concreta).

## DRY — Don't Repeat Yourself

La tolerancia se define en `kernel/constants.py`, no repetida en cada clase. La validación está en `kernel/validation.py`. Si un patrón aparece tres veces, se extrae a una función.

## KISS — Keep It Simple, Stupid

`Point(x, y, z=0.0)` es simple. `Point(x=0.0, y=0.0, z=0.0, crs="EPSG:25830", metadata={})` no lo es. La complejidad se añade cuando se necesita, no antes.

## YAGNI — You Aren't Gonna Need It

No implementar `Point.from_dxf()` antes de tener un adaptador DXF. No implementar `Arc` antes de que un caso de uso lo requiera. No implementar transformaciones CRS antes del módulo GIS.

## Composition over Inheritance

`Polyline` se compone de `Point` y produce `Segment`. No hereda de `list` ni de `Segment`. Hereda de `Curve` solo porque comparte el contrato de curva (point_at, length, project).

## Clean Architecture

```
┌─────────────────────────────────────────────┐
│                 domain/                     │  Entidades de negocio
│  alignment, municipality, parcel, crossing  │
├─────────────────────────────────────────────┤
│              services/, io/                 │  Casos de uso / adaptadores
│  catastro, excel, dxf, reports              │
├─────────────────────────────────────────────┤
│              engine/geometry/               │  Kernel matemático
│  point, vector, polyline, algorithms        │  ← núcleo puro
└─────────────────────────────────────────────┘
```

Las dependencias apuntan hacia adentro. El kernel no sabe nada del exterior.

## Design by Contract

Cada clase tiene:
- **Invariantes**: lo que siempre se cumple (ej. Point siempre tiene coordenadas finitas).
- **Precondiciones**: lo que el método exige (ej. `distance_to` exige un `Point`).
- **Postcondiciones**: lo que el método garantiza (ej. `distance_to` devuelve float ≥ 0).

## Regla de oro para LINPRO

> Ninguna clase del Geometry Engine debe saber que existe el catastro, los municipios, las carreteras, AutoCAD o Excel. Si una clase几何 necesita conocer el negocio, está en el lugar equivocado.
