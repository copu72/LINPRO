# 012 — CATASTRO

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Fuente de datos

- **Sede Electrónica de Catastro** (SEC) — Servicios OGC WFS y descarga de parcelario.
- **Formato:** INSPIRE (CatastralZoning, CadastralParcel, CadastralBoundary).

## Análisis

1. Identificar parcelas catastrales dentro del buffer.
2. Para cada parcela: referencia catastral, área, geometría, uso, titularidad (cuando disponible).
3. Calcular el área de afección (intersección del buffer con la parcela).
4. Agregar por municipio y clase de suelo (rústico/urbano).

## Descarga

La descarga se realiza mediante WFS de la SEC. El usuario debe estar conectado a internet.