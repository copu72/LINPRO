# Estrategia de Testing — LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09  

## Pirámide de testing

La estrategia de pruebas sigue el modelo de pirámide de testing con tres niveles y una capa adicional de rendimiento:

```
        /\
       /  \        Pruebas de rendimiento (benchmarks)
      /    \
     /──────\
    /        \     Pruebas de regresión (100% funcionalidades publicadas)
   /──────────\
  /            \   Pruebas de integración (70% cobertura)
 /──────────────\
/                \ Pruebas unitarias (90% cobertura)
──────────────────
```

### Nivel 1 — Pruebas unitarias

| Aspecto         | Valor                        |
|-----------------|------------------------------|
| Cobertura mínima| 90%                          |
| Framework       | pytest                       |
| Ubicación       | `tests/unit/`               |

Cada módulo debe tener pruebas unitarias que cubran:

- Casos normales de uso.
- Casos límite (PK en origen/final, buffer de ancho cero, etc.).
- Manejo de errores (coordenadas fuera del eje, parámetros inválidos).

### Nivel 2 — Pruebas de integración

| Aspecto         | Valor                        |
|-----------------|------------------------------|
| Cobertura mínima| 70%                          |
| Framework       | pytest                       |
| Ubicación       | `tests/integration/`         |

Pruebas que verifican la interacción entre módulos:

- Carga de proyecto GIS + análisis completo.
- Exportación Excel + CAD con datos reales.
- Flujo completo de análisis (PK → municipios → catastro → informes).

### Nivel 3 — Pruebas de regresión

| Aspecto         | Valor                        |
|-----------------|------------------------------|
| Cobertura       | 100% de funcionalidades publicadas |
| Framework       | pytest + snapshots           |
| Ubicación       | `tests/regression/`          |

Se ejecutan antes de cada release para garantizar que no se han introducido regresiones en APIs ya publicadas.

### Rendimiento — Benchmarks

| Aspecto         | Valor                        |
|-----------------|------------------------------|
| Framework       | pytest-benchmark             |
| Ubicación       | `tests/benchmarks/`          |

Miden tiempos de ejecución de operaciones críticas:

- Cálculo de PK (1000 puntos).
- Generación de buffer (100 m de eje).
- Intersección con capas municipales y catastrales.
- Exportación Excel.

## CI (Integración Continua)

Los pipelines de CI se definen en `.github/workflows/`:

| Workflow      | Evento                     | Contenido                     |
|---------------|----------------------------|-------------------------------|
| `lint.yml`    | push, pull_request         | Ruff + mypy + pre-commit     |
| `tests.yml`   | push, pull_request         | pytest unit + integration    |
| `build.yml`   | push a main / release tag  | Build + package + PyInstaller|

## Ejecución local

```bash
# Pruebas unitarias
pytest tests/unit/ --cov=linpro --cov-fail-under=90

# Pruebas de integración
pytest tests/integration/ --cov=linpro --cov-fail-under=70

# Todas las pruebas
pytest tests/

# Benchmarks
pytest tests/benchmarks/ --benchmark-only --benchmark-warmup=on
```