# Política de Releases — LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09  

## Versionado semántico

LINPRO sigue [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

| Componente | Cambio                                           | Ejemplo  |
|------------|--------------------------------------------------|----------|
| MAJOR      | Cambios incompatibles en API pública.           | `1.0.0` → `2.0.0` |
| MINOR      | Nueva funcionalidad compatible con versiones anteriores. | `1.0.0` → `1.1.0` |
| PATCH      | Corrección de errores compatible con versiones anteriores.| `1.0.0` → `1.0.1` |

Durante el desarrollo inicial (versión 0.x), los cambios MINOR pueden incluir breaking changes sin incrementar MAJOR.

## Frecuencia

- Releases cada 2–3 sprints (aprox. 4–6 semanas).
- Hotfixes se publican bajo demanda cuando se detectan errores críticos en producción.
- No hay fecha fija de release; se libera cuando el equipo lo considera estable.

## Changelog

Cada release debe incluir un archivo `CHANGELOG.md` actualizado con el siguiente formato:

```markdown
## [1.1.0] — 2026-07-09

### Añadido
- Nuevo módulo de análisis de infraestructuras.
- Soporte para exportación DXF con capas separadas.

### Cambiado
- Mejora de rendimiento en cálculo de PK (40% más rápido).

### Corregido
- Error al generar buffer asimétrico con left=0.
```

## Artefactos

Cada release publica los siguientes artefactos:

| Artefacto        | Formato          | Propósito                        |
|------------------|------------------|----------------------------------|
| pip package      | `.whl`, `.tar.gz`| Instalación como librería Python.|
| PyInstaller      | `.exe`           | Ejecutable portátil para Windows.|
| Documentación    | `.pdf`, HTML     | Documentación de la release.     |

## Estrategia de ramas

```
main ← ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ← hotfix/*
                                  ↑
                                merge
                                  ↑
develop ← ─ ─ ← feature/* ← ─ ─ ╯
```

- `main`: contiene solo el código de releases estables. Nunca se commitea directamente.
- `develop`: rama de integración donde se fusionan las `feature/*`.
- `feature/*`: ramas para desarrollo de nuevas funcionalidades.
- `release/*`: ramas de preparación de release (congelación de código, pruebas finales, ajuste de versión).
- `hotfix/*`: ramas para correcciones urgentes desde `main`.

## Proceso de release

1. Crear rama `release/vX.Y.Z` desde `develop`.
2. Actualizar versión en `linpro/__init__.py`.
3. Actualizar `CHANGELOG.md`.
4. Ejecutar suite completa de pruebas (unit + integration + regression).
5. Si hay errores, corregir en la rama de release.
6. Fusionar `release/vX.Y.Z` en `main` (--no-ff).
7. Fusionar `release/vX.Y.Z` en `develop` para mantener sincronización.
8. Etiquetar el commit en `main` como `vX.Y.Z`.
9. Publicar artefactos (pip package + PyInstaller).
10. Publicar release notes en GitHub.