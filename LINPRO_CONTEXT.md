# LINPRO — Contexto del proyecto

**Versión:** 0.0.1
**Sprint:** 0
**Último commit:** 7ce59ec
**Fecha:** 2026-07-09

---

## Módulos / Hitos

| Estado | Módulo | Descripción |
|--------|--------|-------------|
| ☑ | Arquitectura | Sistema de plugins, objeto Project, ADRs |
| ☑ | Estructura | Carpetas, git, CI, pyproject.toml |
| ☑ | Documentación | Especificaciones REQ-XXXX, diagramas /design |
| ☐ | Geometría | Alignment, curvas, clotoides, topology |
| ☐ | PK | Sistema de puntos kilométricos |
| ☐ | Buffer | Área de influencia alrededor del eje |
| ☐ | Municipios | Análisis de afección municipal |
| ☐ | Catastro | Análisis de afección catastral |
| ☐ | Carreteras | Análisis de afección viaria |
| ☐ | Caminos | Análisis de caminos |
| ☐ | Ríos | Análisis hidrográfico |
| ☐ | Infraestructuras | Cruces con infraestructuras existentes |
| ☐ | GIS | Descarga y procesamiento de datos geográficos |
| ☐ | CAD | Exportación DWG/DXF |
| ☐ | Excel | Informes profesionales |
| ☐ | GUI | Interfaz gráfica PySide6 |

---

## Pendiente

- [ ] Crear motor geométrico (Sprint 1)

## Próximo objetivo

**Sprint 1 — Motor Geométrico:** Implementar Alignment con rectas, curvas circulares, clotoides, PK y buffer.

---

## Últimas especificaciones creadas

- REQ-0001: Leer eje
- REQ-0002: Calcular PK
- REQ-0003: Generar buffer
- REQ-0004: Intersecciones con geometrías externas

## Decisiones registradas

- ADR-001: Arquitectura General
- ADR-002: Python
- ADR-003: PySide6
- ADR-004: GeoPandas
- ADR-005: AutoCAD (DXF como formato primario)
- ADR-006: Catastro (WFS Sede Electrónica)
- ADR-007: Carreteras (MITMA + OSM)
- ADR-008: Ríos (MITECO + Confederaciones)
- ADR-009: Excel (openpyxl)
- ADR-010: Instalador (pip + PyInstaller)