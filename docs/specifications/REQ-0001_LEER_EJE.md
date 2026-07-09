# REQ-0001: Leer eje (Alignment)

**Versión:** 0.0.1
**Fecha:** 2026-07-09
**Prioridad:** Alta
**Dependencias:** Ninguna

## Descripción

El sistema debe poder definir un eje (alignment) como una secuencia ordenada de segmentos geométricos. Los segmentos pueden ser tramos rectos (Straight), curvas circulares (CircularArc) y clotoides (Clothoid).

## Criterios de aceptación

- CA-0001.1: Crear un alignment vacío.
- CA-0001.2: Añadir un tramo recto al alignment.
- CA-0001.3: Añadir una curva circular con radio y centro.
- CA-0001.4: Añadir una clotoide con parámetro A.
- CA-0001.5: Validar que la secuencia de segmentos sea continua (fin de uno = inicio del siguiente).
- CA-0001.6: Rechazar segmentos que no conecten geométricamente.

## Referencias

- Especificación: 009_GEOMETRIA.md
- ADR: decisions/ADR-001_ARQUITECTURA_GENERAL.md