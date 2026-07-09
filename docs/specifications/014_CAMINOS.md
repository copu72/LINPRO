# 014 — CAMINOS

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Fuente de datos

- **Catastro** — Caminos y viales en el parcelario catastral.
- **OpenStreetMap** — Viales secundarios y caminos rurales.

## Análisis

1. Identificar caminos que intersectan el buffer.
2. Clasificar por tipo: camino público, camino privado, servidumbre de paso.
3. Para cada camino: PK de cruce, ángulo, longitud dentro del buffer.