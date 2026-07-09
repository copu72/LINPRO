# 011 — MUNICIPIOS

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Fuente de datos

- **INE** (Instituto Nacional de Estadística) — Líneas límite municipales.
- **IGN** — Límites municipales actualizados.

## Análisis

Dado un alignment con buffer, LINPRO debe:

1. Identificar todos los municipios que intersectan el buffer.
2. Para cada municipio, calcular la longitud de trazado dentro de su término.
3. Para cada municipio, indicar el PK de entrada y salida.
4. Agregar metadatos: código INE, provincia, comunidad autónoma.

## Descarga

Los datos municipales se descargan bajo demanda desde el IGN/CNIG. No se almacenan en el repositorio.