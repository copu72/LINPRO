# Project Charter — LINPRO

**Versión:** 1.0
**Fecha:** 2026-07-09
**Estado:** Aprobado

## Nombre del proyecto

LINPRO — Ingeniería Lineal Profesional

## Propósito

Desarrollar una plataforma Python modular, open-source, para el análisis, diseño y gestión de infraestructuras lineales: líneas eléctricas (MT, AT, 132kV, 220kV, 400kV), carreteras, gasoductos, tuberías y canales.

## Objetivos estratégicos

1. Automatizar el 80% del trabajo repetitivo en la redacción de proyectos de infraestructuras lineales.
2. Proporcionar una herramienta independiente de software propietario (QGIS, AutoCAD, etc.).
3. Garantizar trazabilidad total mediante identificadores únicos (FR-XXXX, UC-XXXX).
4. Mantener una arquitectura modular que permita añadir nuevos análisis sin modificar el Core.
5. Generar documentación profesional (informes Excel, planos DXF) sin intervención manual.

## Alcance

### Incluye
- Definición de ejes (Alignment) con rectas, curvas circulares y clotoides.
- Sistema de Puntos Kilométricos (PK).
- Análisis de afecciones: catastro, municipios, carreteras, ríos, infraestructuras.
- Descarga automática de datos oficiales (catastro, IGN, MITMA, MITECO).
- Exportación a Excel y DXF/DWG.
- Interfaz gráfica (PySide6).

### No incluye
- Edición CAD general (no es AutoCAD).
- SIG completo (no es QGIS).
- Gestión de proyectos empresariales (no es ERP).

## Stakeholders

- **Promotor:** copu72
- **Desarrolladores:** LINPRO Team
- **Usuarios:** Ingenieros civiles, topógrafos, proyectistas.
- **Beneficiarios:** Ingenierías que trabajan con infraestructuras lineales en España.

## Riesgos iniciales

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Dependencia de datos oficiales (cambios en APIs) | Alto | Abstraction layer en GIS downloader |
| Rendimiento en trazados largos (>100km) | Medio | Tests de performance desde Fase 1 |
| Complejidad de clotoides | Medio | Documentación exhaustiva y tests |
| Adopción por usuarios sin Python | Bajo | Instalador portátil (PyInstaller) |

## Aprobación

Este Project Charter establece la visión fundacional de LINPRO. Cualquier cambio sustancial requiere actualización de este documento y registro en ADR.