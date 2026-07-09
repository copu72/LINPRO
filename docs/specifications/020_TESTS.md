# 020 — TESTS

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Pirámide de testing

LINPRO sigue el modelo de pirámide clásico:

1. **Unit tests** (`tests/unit/`) — Pruebas de funciones aisladas. Mock de dependencias externas.
2. **Integration tests** (`tests/integration/`) — Pruebas de flujos completos (Alignment + PK + Buffer).
3. **Regression tests** (`tests/regression/`) — Tests que verifican que cambios no rompen funcionalidades existentes.
4. **Performance tests** (`tests/performance/`) — Pruebas de rendimiento en trazados largos.
5. **Benchmarks** (`tests/benchmarks/`) — Comparativas de velocidad entre versiones.

## Framework

- **pytest** como framework principal.
- **pytest-cov** para cobertura.
- **pytest-benchmark** para benchmarks.

## Cobertura mínima

- Unit: 90%
- Integration: 70%
- Regression: 100% sobre funcionalidades publicadas.