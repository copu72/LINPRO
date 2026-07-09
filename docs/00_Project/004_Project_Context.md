# Project Context

**Versión:** 1.0
**Fecha:** 2026-07-09

## Contexto del proyecto

LINPRO nace de la necesidad de automatizar el trabajo repetitivo en la redacción de proyectos de infraestructuras lineales en España. Ingenieros civiles y topógrafos dedican horas a:

1. Dibujar ejes en AutoCAD
2. Cruzar datos catastrales manualmente
3. Contabilizar municipios afectados
4. Identificar cruces con carreteras y ríos
5. Generar informes en Excel
6. Generar planos en DWG

LINPRO automatiza todo ese flujo desde una librería Python.

## Arquitectura general

```
LINPRO Core (dependencia base)
    │
    ├── LINPRO GIS    (datos geográficos, descargas, proyecciones)
    ├── LINPRO CAD    (DXF/DWG, capas, estilos)
    ├── LINPRO GUI    (PySide6, ventanas, widgets)
    ├── LINPRO Reports (PDF)
    └── LINPRO Excel  (informes .xlsx)
```

Cada sublibrería depende exclusivamente de LINPRO Core. Ninguna depende de otra.

## Stack tecnológico

| Componente | Tecnología |
|------------|-----------|
| Lenguaje | Python 3.11+ |
| Geometría | Shapely |
| GIS | GeoPandas, Fiona, PyProj |
| CAD | ezdxf |
| GUI | PySide6 |
| Excel | openpyxl |
| Tests | pytest, pytest-cov, pytest-benchmark |
| Linting | ruff |
| Tipado | mypy (strict mode) |
| Build | setuptools, PyInstaller |

## Principios rectores

1. **Nada se programa sin estar especificado.**
2. **Ningún archivo Python existe sin su especificación.**
3. **Cada clase tiene un único propósito.**
4. **El repositorio es autoexplicativo.**