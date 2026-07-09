# Project Objectives

**Versión:** 1.0
**Fecha:** 2026-07-09

## Objetivos generales

| ID | Objetivo | Prioridad | Fase |
|----|----------|-----------|------|
| OG-01 | Crear una librería Python robusta, tipada y documentada | Crítica | 0 |
| OG-02 | Automatizar análisis de afecciones para infraestructuras lineales | Crítica | 2-3 |
| OG-03 | Generar informes técnicos profesionales (Excel, DXF, PDF) | Alta | 4 |
| OG-04 | Mantener independencia total de software propietario | Crítica | 0 |
| OG-05 | Sistema de plugins para extensiones futuras | Alta | 0 |

## Objetivos específicos v0.1.0

| ID | Objetivo | Módulo |
|----|----------|--------|
| OE-01 | Alignment funcional con rectas, curvas circulares y clotoides | Geometry |
| OE-02 | Sistema de PK con recálculo automático | Geometry |
| OE-03 | Buffer configurable izquierda/derecha | Geometry |
| OE-04 | Descarga automática de catastro (WFS) | GIS |
| OE-05 | Análisis de afección catastral | Cadastre |
| OE-06 | Análisis de afección municipal | Municipalities |
| OE-07 | Exportación a Excel | Excel |
| OE-08 | Exportación a DXF | CAD |

## Objetivos de calidad

| ID | Objetivo | Métrica |
|----|----------|---------|
| OQ-01 | Cobertura de tests unitarios ≥ 90% | pytest-cov |
| OQ-02 | Cobertura de tests integración ≥ 70% | pytest-cov |
| OQ-03 | Código 100% tipado | mypy strict |
| OQ-04 | Sin errores de linting | ruff |
| OQ-05 | Documentación completa por módulo | README + API.md por módulo |