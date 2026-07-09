# REQ-0002: Calcular PK

**Versión:** 0.0.1
**Fecha:** 2026-07-09
**Prioridad:** Alta
**Dependencias:** REQ-0001

## Descripción

El sistema debe calcular automáticamente los Puntos Kilométricos (PK) para cualquier punto del alignment. El PK es la distancia acumulada desde el origen del eje.

## Criterios de aceptación

- CA-0002.1: Dado un alignment, calcular PK en cualquier coordenada (x,y).
- CA-0002.2: Dado un PK, obtener coordenada (x,y) y acimut.
- CA-0002.3: Recalcular PK automáticamente al modificar el alignment.
- CA-0002.4: Precisión de 3 decimales (milímetros).
- CA-0002.5: Formato visual: PK 0+000.000, PK 1+234.567.

## Referencias

- Especificación: 010_PK.md