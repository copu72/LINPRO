# REQ-0004: Intersecciones con geometrías externas

**Versión:** 0.0.1
**Fecha:** 2026-07-09
**Prioridad:** Alta
**Dependencias:** REQ-0001

## Descripción

El sistema debe calcular intersecciones entre el alignment y geometrías externas (carreteras, ríos, parcelas, etc.).

## Criterios de aceptación

- CA-0004.1: Intersección punto-línea entre el alignment y una línea externa.
- CA-0004.2: Intersección polígono-polígono entre el buffer y una geometría externa.
- CA-0004.3: Devolver PK, coordenada y ángulo de intersección.
- CA-0004.4: Múltiples intersecciones ordenadas por PK creciente.

## Referencias

- Especificación: 009_GEOMETRIA.md