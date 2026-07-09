# ADR-004: GeoPandas para procesamiento espacial

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO debe procesar grandes volúmenes de datos espaciales (parcelas catastrales, municipios, carreteras, ríos). Se evaluaron PostGIS, SQLite Spatialite y GeoPandas.

## Decisión

Se elige **GeoPandas** por:

1. **Integración natural** con el ecosistema Python.
2. **Rendimiento** basado en Shapely y Fiona en C.
3. **Facilidad de uso** con sintaxis tipo pandas.
4. **Sin servidor** requerido (a diferencia de PostGIS).

## Consecuencias

- **Positivo:** Consultas espaciales eficientes.
- **Positivo:** Exportación directa a GeoJSON, Shapefile, GPKG.
- **Negativo:** Dependencia de GDAL (Fiona). Se incluirá en el instalador.
- **Negativo:** Dataset grande puede consumir mucha RAM. Se usará chunking si es necesario.