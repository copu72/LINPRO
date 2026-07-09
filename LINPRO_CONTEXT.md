# LINPRO — Contexto del proyecto

**Versión:** 0.1.0
**Sprint:** 1 (LINPRO Core)
**Fase:** 1 — Core
**Release:** v0.1.0
**Fecha:** 2026-07-09

---

## Módulos / Hitos

| Estado | Módulo | Docs | Código | Tests |
|--------|--------|------|--------|-------|
| ☑ | Fundación (Sprint 0) | ✅ | ✅ | - |
| ☑ | **Core (Sprint 1)** | ✅ 6 docs | ✅ 11 módulos | ✅ 109 tests |
| ☐ | Geometry Engine (Sprint 2) | ❌ | ❌ | ❌ |
| ☐ | GIS Engine (Sprint 3) | ❌ | ❌ | ❌ |
| ☐ | CAD Engine (Sprint 4) | ❌ | ❌ | ❌ |
| ☐ | Analysis Engine (Sprint 5) | ❌ | ❌ | ❌ |
| ☐ | Export Engine (Sprint 6) | ❌ | ❌ | ❌ |
| ☐ | GUI (Sprint 7) | ❌ | ❌ | ❌ |
| ☐ | Instalador (Sprint 8) | ❌ | ❌ | ❌ |
| ☐ | Beta (Sprint 9) | ❌ | ❌ | ❌ |
| ☐ | Release 1.0 (Sprint 10) | ❌ | ❌ | ❌ |

## Core — Módulos implementados

| Módulo | Clases principales | Propósito |
|--------|-------------------|-----------|
| `app` | LINPROApp | Ciclo de vida de la aplicación |
| `config` | Configuration | Configuración global (YAML) |
| `events` | EventBus, Event | Comunicación entre módulos |
| `exceptions` | LINPROError + 7 subclases | Jerarquía de errores |
| `logging` | LINPROLogger, LogLevel | Sistema de logging profesional |
| `plugins` | PluginManager, BasePlugin, PluginInfo | Sistema de plugins |
| `project` | Project, Workspace | Objeto central del proyecto |
| `settings` | UserSettings | Preferencias de usuario |
| `version` | VersionInfo | Versionado semver |

## Uso básico

```python
from linpro import Project, LINPROApp

app = LINPROApp.get_instance()
app.start()

project = Project("Mi Proyecto")
app.workspace.open_project(project)
```

## Próximo objetivo

**Sprint 2 — Geometry Engine:** Alignment, PK, Buffer, Intersections, Topology.