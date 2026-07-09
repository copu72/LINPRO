# REQ-0003: Generar buffer

**Versión:** 0.0.1
**Fecha:** 2026-07-09
**Prioridad:** Alta
**Dependencias:** REQ-0001

## Descripción

El sistema debe generar un área de influencia (buffer) alrededor del alignment con una distancia configurable a izquierda y derecha.

## Criterios de aceptación

- CA-0003.1: Generar buffer simétrico (misma distancia a ambos lados).
- CA-0003.2: Generar buffer asimétrico (distancias diferentes izquierda/derecha).
- CA-0003.3: El buffer debe ser un polígono cerrado.
- CA-0003.4: Recalcular buffer automáticamente al modificar el alignment o las distancias.

## Referencias

- Especificación: 009_GEOMETRIA.md