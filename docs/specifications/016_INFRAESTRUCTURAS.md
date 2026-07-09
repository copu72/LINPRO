# 016 — INFRAESTRUCTURAS EXISTENTES

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Fuentes de datos

- **REE** (Red Eléctrica de España) — Líneas de transporte y subestaciones.
- **Distribuidoras** — Líneas de distribución de electricidad.
- **Mitma** — Otras infraestructuras (ferrocarril, tuberías).
- **Gasoductos** — Enagás y otras.

## Análisis

1. Identificar infraestructuras existentes que intersectan el buffer.
2. Clasificar por tipo: línea eléctrica, tubería, ferrocarril, etc.
3. Para cada intersección: PK, distancia, ángulo, titular.
4. Evaluar paralelismos (trazados que corren paralelos al eje a menos de una distancia crítica).