# Coding Standards

| Versión | Fecha       |
| ------- | ----------- |
| 1.0     | 2026-07-09 |

## Tipado

- Toda la base de código debe pasar `mypy --strict`.
- No se permite `Any`, `# type: ignore` ni omisiones de tipo en firmas de funciones.
- Usar `TypeVar`, `Generic`, `Callable`, `Literal`, `TypedDict` cuando corresponda.

## Ruff

- Longitud máxima de línea: 100 caracteres.
- Reglas activadas: `E` (pycodestyle), `F` (pyflakes), `I` (isort), `W` (warnings), `N` (naming), `UP` (pyupgrade).
- Configuración en `pyproject.toml`.

## Nombres

- Nombres descriptivos en español para variables, funciones, clases y módulos.
- Únicamente se usan palabras en inglés para palabras reservadas del lenguaje, bibliotecas estándar y terceras.
- Preferir nombres largos y explícitos sobre abreviaturas crípticas.

## Comentarios

- Prohibidos los comentarios superfluos o redundantes.
- El código debe ser autoexplicativo: nombres claros, tipos explícitos, funciones pequeñas.
- Los únicos comentarios permitidos son aquellos que documentan una decisión no obvia o una restricción externa.

## Tests

- Toda función nueva debe tener tests unitarios.
- Los tests deben cubrir casos normales, borde y error.
- Ejecutar `pytest` antes de cada commit.

## Docstrings

- Toda función o método público debe tener docstring.
- Formato: Google style (sección Args, Returns, Raises si aplica).
- Las funciones privadas pueden omitir docstring si el nombre es suficientemente descriptivo.
