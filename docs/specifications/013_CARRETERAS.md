# 013 — CARRETERAS

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Fuente de datos

- **MITMA** — Red de Carreteras del Estado (RCE).
- **OpenStreetMap** — Carreteras secundarias (fuente complementaria).
- **CCAA** — Carreteras autonómicas (descarga bajo demanda).

## Análisis

1. Identificar carreteras que intersectan el buffer.
2. Clasificar por tipo: autopista, autovía, nacional, autonómica, local.
3. Indicar PK de intersección.
4. Distancia perpendicular desde el eje al punto de cruce.
5. Ángulo de cruce.