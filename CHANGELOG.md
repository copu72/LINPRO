# Changelog

## [0.4.0-alpha.1] - 2026-07-14 — Geometry Kernel v0.4.0 CERTIFIED
### Added
- **Vector** (TASK-0004B) — certificado con 133 tests, 100% cobertura, benchmark
- `benchmarks/vector_benchmark.py` — línea base con 7 benchmarks (creación, dot, norm, rotate, JSON, length)
- `docs/Geometry/Kernel/` — documentación del Kernel reorganizada bajo `docs/Geometry/`
- `docs/Geometry/Algorithms/`, `docs/Geometry/ADR/`, `docs/Geometry/Examples/`, `docs/Geometry/Benchmarks/`

### Certified
- Geometry Kernel v0.4.0: Geometry(ABC) ✅, Point ✅, BoundingBox ✅, Vector ✅
- 342 tests Geometry, 434 tests total proyecto, 0 fallos

### Changed
- `docs/PROJECT_STATUS.md` — actualizado a Hito A, Kernel v0.4.0, tabla por entidad
- `.gitignore` — añadidos `.coverage` y `.pytest_cache/`

## [0.1.0] - 2026-07-09 — Sprint 1: LINPRO Core
### Added
- LINPRO Core completo con 11 módulos:
  - `app` — LINPROApp, ciclo de vida (start/stop)
  - `config` — Configuration, carga YAML, valores por defecto
  - `events` — EventBus, Event, eventos estándar del Core
  - `exceptions` — Jerarquía completa (LINPROError, ProjectError, ConfigError, etc.)
  - `logging` — LINPROLogger singleton, niveles, salida a consola/archivo
  - `plugins` — PluginManager, BasePlugin, PluginInfo, descubrimiento dinámico
  - `project` — Project, Workspace, ProjectMetadata, ProjectState
  - `settings` — UserSettings, persistencia JSON
  - `version` — VersionInfo, semver, comparación de versiones
- 109 tests unitarios (100% passing):
  - exceptions: 11 tests
  - logging: 13 tests
  - events: 12 tests
  - config: 13 tests
  - plugins: 9 tests
  - project: 21 tests
  - settings: 12 tests
  - app: 8 tests
- Documentación del Core: README, Architecture, Classes, API, Tests, TODO
- Release v0.1.0 con tag

### Changed
- Reestructuración completa de src/linpro/ para arquitectura limpia
- pyproject.toml actualizado a v0.1.0 con tooling configurado
- Sistema de plugins con BasePlugin abstracto

## [0.0.1] - 2026-07-09 — Sprint 0: Foundation
### Added
- Estructura completa del repositorio (~130 carpetas)
- 40+ documentos profesionales (00_Project a 08_Releases, ADRs, diagramas)
- README, LICENSE, CHANGELOG, CONTRIBUTING, ROADMAP, CODE_OF_CONDUCT
- CI workflows (lint, tests, build)