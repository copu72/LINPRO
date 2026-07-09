# 019 — CONFIGURACIÓN

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Sistema de configuración

LINPRO utiliza un sistema de configuración en tres niveles:

1. **Configuración por defecto** — `config/default/` (viene con el programa).
2. **Configuración de usuario** — `config/user/` (persiste entre sesiones).
3. **Configuración de proyecto** — Se almacena dentro del archivo `.linpro` del proyecto.

## Formato

```yaml
project:
  author: ""
  company: ""
  default_epsg: 25830

geometry:
  pk_precision: 3
  buffer_segments: 8
  min_tangent_length: 0.001

analysis:
  catastro: true
  municipalities: true
  roads: true
  rivers: true
  infrastructure: true

export:
  excel_template: "default.xlsx"
  dxf_version: "AC1027"
  pdf_orientation: "landscape"
```