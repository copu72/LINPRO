# LINPRO — Ingeniería Lineal Profesional

**LINPRO** es una plataforma Python modular para el análisis, diseño y gestión de infraestructuras lineales: líneas eléctricas, carreteras, gasoductos, tuberías y canales.

## Arquitectura

```
LINPRO Core (dependencia base)
    ├── LINPRO GIS    (datos geográficos, descargas WFS, proyecciones)
    ├── LINPRO CAD    (DXF/DWG, capas, estilos, entidades)
    ├── LINPRO GUI    (PySide6, MVC)
    ├── LINPRO Reports (PDF)
    └── LINPRO Excel  (informes .xlsx)
```

Cada sublibrería depende exclusivamente de LINPRO Core.

## Estado del proyecto

**Fase:** 0 — Arquitectura (Sprint 0)
**Versión:** 0.0.1
**Documentación:** 40+ documentos profesionales completados.

| Documento | Estado |
|-----------|--------|
| Project Charter | ✅ |
| Objetivos y Roadmap | ✅ |
| Glosario | ✅ |
| Requisitos funcionales (FR-0001 a FR-0010) | ✅ |
| Casos de uso (UC-001 a UC-004) | ✅ |
| Convenciones de código | ✅ |
| Arquitectura (6 documentos) | ✅ |
| Módulos (11 READMEs) | ✅ |
| API Reference | ✅ |
| Testing Strategy | ✅ |
| Development Workflow | ✅ |
| ADRs (10 decisiones registradas) | ✅ |
| Diagramas de diseño (5 .drawio) | ✅ |

## Principios rectores

1. **Nada se programa sin estar especificado.**
2. **Ningún archivo Python existe sin su especificación.**
3. **Cada clase tiene un único propósito.**
4. **El repositorio es autoexplicativo.**

## Licencia

MIT License. Ver [LICENSE](LICENSE).