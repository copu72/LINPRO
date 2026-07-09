# ADR-007: Obtención de datos de carreteras

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO necesita identificar carreteras que intersectan el buffer del trazado. Existen varias fuentes: MITMA (RCE), OpenStreetMap y datos autonómicos.

## Decisión

Se usa **MITMA Red de Carreteras del Estado** como fuente principal y **OpenStreetMap** como complementaria para carreteras secundarias y caminos.

Razones:

1. **MITMA** proporciona datos oficiales de la RCE con clasificación (autopista, autovía, nacional).
2. **OSM** cubre carreteras autonómicas y locales no incluidas en RCE.
3. Ambas son accesibles mediante WFS/descarga directa sin autenticación.

## Consecuencias

- **Positivo:** Datos fiables y actualizados para la RCE.
- **Positivo:** Cobertura completa con OSM como complemento.
- **Negativo:** OSM puede tener imprecisiones. Se priorizarán siempre los datos de MITMA cuando existan ambas fuentes.