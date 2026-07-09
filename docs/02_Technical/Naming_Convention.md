# Naming Convention

| Versión | Fecha       |
| ------- | ----------- |
| 1.0     | 2026-07-09 |

## Clases

- `PascalCase`. Sustantivos o frases nominales.
- Ejemplos: `Project`, `Alignment`, `RoadAnalyzer`, `ParcelCollection`, `CoordinateSystem`.

## Funciones y métodos

- `snake_case`. Verbos o frases verbales.
- Ejemplos: `calculate_pk`, `get_municipalities`, `validate_geometry`, `export_to_excel`.

## Variables

- `snake_case`. Sustantivos descriptivos.
- Ejemplos: `total_length`, `parcel_list`, `alignment_points`, `epsg_code`.

## Constantes

- `UPPER_SNAKE_CASE`.
- Definirse a nivel de módulo o en clases de constantes.
- Ejemplos: `DEFAULT_EPSG`, `MAX_ITERATIONS`, `PI`, `TOLERANCE_MM`.

## Archivos

- `snake_case`. Coincidir con el contenido principal.
- Ejemplos: `alignment.py`, `road_analyzer.py`, `excel_writer.py`, `cadastre_parser.py`.

## Directorios

- `snake_case` o una sola palabra en minúscula.
- Ejemplos: `geometry/`, `cadastre/`, `excel/`, `io_handlers/`, `tests/`.
