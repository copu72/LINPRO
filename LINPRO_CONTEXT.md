# LINPRO — Contexto del proyecto

**Versión:** 0.0.1
**Sprint:** 0 (Fundación)
**Fase:** 0 — Arquitectura
**Fecha:** 2026-07-09

---

## Módulos / Hitos

| Estado | Módulo | Docs | Código |
|--------|--------|------|--------|
| ☑ | Arquitectura | ✅ 6 docs | ❌ |
| ☑ | Estructura del repo | ✅ | ✅ |
| ☑ | Project Charter | ✅ | ❌ |
| ☑ | Requisitos funcionales | ✅ FR-0001 a FR-0010 | ❌ |
| ☑ | Casos de uso | ✅ UC-001 a UC-004 | ❌ |
| ☑ | Convenciones técnicas | ✅ 5 docs | ❌ |
| ☑ | ADRs | ✅ 10 decisiones | ❌ |
| ☑ | Diagramas de diseño | ✅ 5 .drawio | ❌ |
| ☐ | Core (Project, config, logging) | Pendiente | ❌ |
| ☐ | Geometry (Alignment, PK, Buffer) | ✅ README | ❌ |
| ☐ | GIS (descargas, proyecciones) | Pendiente | ❌ |
| ☐ | CAD (DXF/DWG) | ✅ README | ❌ |
| ☐ | GUI (PySide6) | ✅ README | ❌ |
| ☐ | Excel / Reports | ✅ README | ❌ |

---

## Pendiente inmediato

- [ ] Iniciar Sprint 1: LINPRO Core

## Próximo objetivo

**Sprint 1 — Core:** Implementar objeto Project, configuración, logging, excepciones y sistema de versiones.

---

## Documentación generada (40+ archivos)

```
docs/
├── 00_Project/          5 documentos (Charter, Objectives, Roadmap, Glossary, Context)
├── 01_Functional/       14 documentos (FR-0001 a FR-0010, UC-001 a UC-004)
├── 02_Technical/        5 documentos (Coding Standards, Naming, Python Guidelines, Dependencies, Repository Rules)
├── 03_Architecture/     6 documentos (Overall, Core, Plugin, Geometry, GUI, Database)
├── 04_Modules/          11 READMEs (Alignment, PK, Buffer, Municipalities, Cadastre, Roads, Hydrology, Infrastructure, Excel, DWG, GUI, Reports)
├── 05_API/              1 documento (API Reference)
├── 06_Testing/          1 documento (Testing Strategy)
├── 07_Development/      2 documentos (Workflow, Environment Setup)
├── 08_Releases/         1 documento (Release Policy)
```

## Decisiones registradas

`decisions/` — ADR-001 a ADR-010

## Diagramas

`design/` — geometry_engine.drawio, gui.drawio, database.drawio, workflow.drawio, modules.drawio