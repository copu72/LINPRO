# Project Roadmap

**Versión:** 1.0
**Fecha:** 2026-07-09

## Fase 0 — Arquitectura (Sprint 0)
**Duración:** 1-2 días
**Objetivo:** Fundación documental y estructural del proyecto.

- [x] Project Charter
- [x] Estructura de carpetas
- [x] Convenciones de código
- [x] Arquitectura general
- [x] ADRs (1-10)
- [ ] Diagramas de diseño
- [ ] CI/CD básico

## Fase 1 — Core (Sprint 1)
**Duración:** 2-3 sprints
**Objetivo:** LINPRO Core funcional.

- [ ] Sistema de configuración
- [ ] Objeto Project
- [ ] Sistema de logging
- [ ] Excepciones personalizadas
- [ ] Versión y actualizaciones
- [ ] Tests del Core

## Fase 2 — Geometry Engine (Sprint 2-3)
**Duración:** 3-4 sprints
**Objetivo:** Motor geométrico completo.

- [ ] Alignment (rectas, curvas, clotoides)
- [ ] Sistema de PK
- [ ] Buffer (simétrico y asimétrico)
- [ ] Intersecciones
- [ ] Topología
- [ ] Tests de geometry

## Fase 3 — GIS Engine (Sprint 4-5)
**Duración:** 3-4 sprints
**Objetivo:** Descarga y procesamiento de datos geográficos.

- [ ] Conexión WFS Catastro
- [ ] Descarga municipios (IGN)
- [ ] Descarga carreteras (MITMA)
- [ ] Descarga hidrografía (MITECO)
- [ ] Sistema de caché
- [ ] Tests de GIS

## Fase 4 — CAD Engine (Sprint 6-7)
**Duración:** 2 sprints
**Objetivo:** Exportación profesional a DXF/DWG.

- [ ] Capas y estilos
- [ ] Exportación de alignment
- [ ] Exportación de buffer
- [ ] Exportación de afecciones
- [ ] Tests de CAD

## Fase 5 — GUI (Sprint 8-9)
**Duración:** 3-4 sprints
**Objetivo:** Interfaz gráfica profesional.

- [ ] MainWindow
- [ ] Alignment editor
- [ ] Map viewer
- [ ] Results panel
- [ ] Export dialogs

## Fase 6 — Aplicación (Sprint 10+)
**Duración:** Continuo
**Objetivo:** Distribución, instaladores y documentación de usuario.

- [ ] Instalador Windows
- [ ] Versión portable
- [ ] Manual de usuario
- [ ] Manual de desarrollador
- [ ] Release v1.0