# Python Style Guide

Basado en PEP 8, PEP 257 y PEP 484, adaptado para LINPRO.

## 1. Formateo

Ruff formatea automáticamente. Ejecutar `ruff format .` antes de cada commit.

## 2. Type Hints

- **Obligatorios** en: parámetros de funciones públicas, retornos de funciones públicas, atributos de clase.
- **Opcionales** en: variables locales (cuando el tipo es obvio).
- Usar tipos nativos de Python 3.9+: `list[str]` en lugar de `List[str]`.
- Usar `int | float` en lugar de `Union[int, float]`.
- Usar `X | None` en lugar de `Optional[X]`.

## 3. Naming detalhado

| Constructo | Convención |
|---|---|
| Clase abstracta | `Curve`, `Geometry` (no `AbstractCurve`) |
| Excepción | Sufijo `Error`: `GeometryError` |
| Enumeración | `class Color(Enum)` (no `ColorEnum`) |
| Función privada | `_validate_coordinate(...)` |
| Variable con tipo | `point: Point` (no `pt: Point`) |
| Booleano | `is_finite`, `has_intersection`, `can_merge` |

## 4. Longitud de línea

100 caracteres máximo. Excepciones:
- URLs en comentarios.
- Strings de test (pueden romperse visualmente).

## 5. Espaciado

- Dos líneas en blanco entre clases.
- Una línea en blanco entre métodos.
- Una línea en blanco entre secciones lógicas dentro de un método (solo si mejora legibilidad).
