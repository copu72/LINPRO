# ADR-002: Elección de Python como lenguaje principal

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO debe ser multiplataforma, fácil de instalar y mantener, y permitir prototipado rápido. Se consideró C# (.NET) para integración con AutoCAD.

## Decisión

Se elige **Python 3.11+** por:

1. **Multiplataforma:** Windows, Linux y macOS.
2. **Ecosistema GIS:** GeoPandas, Shapely, Fiona, Rasterio, PyProj.
3. **Facilidad de instalación:** `pip install linpro`.
4. **Comunidad activa** en ingeniería civil y GIS.
5. **Type hints** maduros desde Python 3.11.

## Consecuencias

- **Positivo:** Instalación simple, sin compilación.
- **Positivo:** Acceso a todo el ecosistema científico y GIS de Python.
- **Negativo:** Rendimiento inferior a C# en cálculos intensivos. Se mitigará usando NumPy y Numba para cuellos de botella.
- **Negativo:** Sin integración directa con AutoCAD (.NET). Se usará DXF como puente.