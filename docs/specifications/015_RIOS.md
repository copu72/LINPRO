# 015 — RÍOS

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Fuente de datos

- **MITECO** — Red hidrográfica nacional (Confederaciones Hidrográficas).
- **IGME** — Masas de agua superficial.
- **CH** — Datos específicos por Confederación Hidrográfica.

## Análisis

1. Identificar ríos, arroyos y masas de agua que intersectan el buffer.
2. Para cada curso: nombre, tipo (permanente/estacional), PK de cruce.
3. Identificar la Confederación Hidrográfica competente.
4. Calcular la distancia de cruce (ancho del río en la zona de afección).