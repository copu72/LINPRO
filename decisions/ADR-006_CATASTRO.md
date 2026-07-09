# ADR-006: Obtención de datos catastrales

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO necesita acceder al parcelario catastral español. Existen varias vías: descarga masiva (SEC), WFS, archivos Shapefile.

## Decisión

Se usa el **servicio WFS de la Sede Electrónica de Catastro** siguiendo el modelo INSPIRE.

Razones:

1. **Datos oficiales y actualizados** directamente de la fuente.
2. **Formato INSPIRE** estandarizado a nivel europeo.
3. **Acceso gratuito** sin necesidad de convenios.
4. **Descarga bajo demanda** — no almacenamos datos en el repositorio.

## Consecuencias

- **Positivo:** Datos siempre actualizados.
- **Positivo:** Sin problemas de licencia de redistribución.
- **Negativo:** Requiere conexión a internet para la descarga.
- **Negativo:** Límite de peticiones por IP. Se implementará caché local con expiración.