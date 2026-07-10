# Coding Standards

**Aplica a:** Todo el código Python de LINPRO.
**Incumplir estas normas requiere revisión de arquitectura.**

## 1. Lenguaje

- Python 3.13+.
- Type hints obligatorios en toda la API pública.
- `from __future__ import annotations` en todos los archivos.

## 2. Estilo

- Seguir PEP 8 estrictamente.
- Ruff como linter con configuración en `pyproject.toml`.
- Máximo 100 caracteres por línea.
- 4 espacios por indentación. No tabs.

## 3. Imports

- Orden: stdlib → terceros → internos. Separados por línea en blanco.
- Absolutos siempre: `from linpro.geometry.kernel import ...`
- No se permite `import *`.
- No se permite imports circulares.

## 4. Nombres

| Elemento | Convención | Ejemplo |
|---|---|---|
| Clases | PascalCase | `BoundingBox`, `Polyline` |
| Funciones/métodos | snake_case | `distance_to`, `from_dict` |
| Variables | snake_case | `point_list`, `tolerance` |
| Constantes | UPPER_SNAKE_CASE | `EPSILON`, `MAX_ITERATIONS` |
| Privado | prefijo _ | `_x`, `_points` |
| Protected | prefijo _ (no usamos `__` name mangling) | `_internal` |

## 5. Documentación

- Google-style docstrings obligatorios en toda la API pública.
- Cada archivo .py comienza con docstring del módulo.
- Cada clase tiene docstring con: descripción, invariantes, ejemplo breve.
- Cada método público tiene Args/Returns/Raises.

## 6. Excepciones

- Usar excepciones propias del módulo (`GeometryError`, etc.).
- No lanzar `Exception` genérico.
- No lanzar `AssertionError` para control de flujo.
- Capturar excepciones específicas, no `except Exception`.

## 7. Tests

- Un archivo de test por clase: `test_point.py`.
- Usar pytest. No unittest.
- Nombres de test descriptivos: `test_distance_to_returns_zero_for_same_point`.
- Cobertura mínima: 95 % en Geometry Engine, 80 % en el resto.

## 8. Commits

- Prefijo semántico: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Máximo 72 caracteres en primera línea.
- Cuerpo opcional explicando el qué y el por qué.

## 9. Prohibiciones

- No se usa `# noqa` sin justificación en el mismo comentario.
- No se comentan tests para que pasen.
- No se deja código comentado.
- No se usa `print()` en código de producción (usar logging).
- No se importa `typing` donde se pueda usar sintaxis nativa (`list`, `dict`, `tuple`).
