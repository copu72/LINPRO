# Flujo de Trabajo — LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09  

## Flujo general

```
Fork → Feature branch → Tests → PR a develop → Code review → Merge → Release → Merge a main
```

## Convención de ramas

| Rama              | Propósito                                           |
|-------------------|-----------------------------------------------------|
| `main`            | Código de producción estable. Solo merges desde `develop` o `hotfix/*`. |
| `develop`         | Rama de integración continua. Contiene la última versión en desarrollo. |
| `feature/*`       | Nuevas funcionalidades, ej. `feature/fr-0002-pk`.  |
| `release/*`       | Preparación de release, ej. `release/v1.1.0`.       |
| `hotfix/*`        | Correcciones urgentes sobre `main`, ej. `hotfix/crash-export`. |

## Commits

Se sigue la especificación de [Conventional Commits](https://www.conventionalcommits.org/):

| Tipo       | Uso                                        |
|------------|--------------------------------------------|
| `feat:`    | Nueva funcionalidad.                 |
| `fix:`     | Corrección de error.                      |
| `docs:`    | Cambios en documentación.                 |
| `test:`    | Adición o modificación de pruebas.        |
| `refactor:`| Refactorización sin cambio de funcionalidad. |
| `chore:`   | Tareas de mantenimiento (build, CI, etc.).|

Ejemplos:

```
feat: implementar cálculo de PK con proyección sobre el eje
fix: corregir desbordamiento en buffer asimétrico con left=0
docs: actualizar referencia de API para módulo Cadastre
test: añadir casos límite para calc_pk con coordenadas fuera del eje
```

## Code review

Toda integración a `main` requiere:

1. Pull request contra `develop` desde una rama `feature/*`.
2. Al menos un revisor aprueba los cambios.
3. Todas las pruebas CI (lint + tests) pasan.
4. Sin conflictos de merge.
5. Merge a `develop`.
6. En release, PR de `develop` a `main` con changelog actualizado.

## Política de merge

- `feature/*` → `develop`: merge normal o squash.
- `develop` → `main`: merge sin fast-forward (--no-ff) para mantener trazabilidad.
- `hotfix/*` → `main`: merge directo con backport posterior a `develop`.