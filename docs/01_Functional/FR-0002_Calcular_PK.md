# FR-0002: Calcular PK

**Versión:** 1.0
**Fecha:** 2026-07-09
**Prioridad:** Crítica
**Dependencias:** FR-0001
**Módulo:** Geometry.PK

## Descripción

El sistema debe calcular Puntos Kilométricos para cualquier punto del alignment.

## Criterios de aceptación

- CA-0002.1: Obtener PK dada una coordenada (x, y).
- CA-0002.2: Obtener coordenada (x, y) y acimut dado un PK.
- CA-0002.3: Recalcular PKs automáticamente al modificar el alignment.
- CA-0002.4: Precisión de 3 decimales (milímetros).
- CA-0002.5: Formatear PK como "PK 0+000.000".

## Referencias

- UC-001: Analizar eje