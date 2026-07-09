# FR-0001: Definir eje (Alignment)

**Versión:** 1.0
**Fecha:** 2026-07-09
**Prioridad:** Crítica
**Dependencias:** Ninguna
**Módulo:** Geometry.Alignment

## Descripción

El usuario debe poder definir un eje como una secuencia ordenada de segmentos geométricos: rectas, curvas circulares y clotoides.

## Criterios de aceptación

- CA-0001.1: Crear alignment vacío.
- CA-0001.2: Añadir tramo recto (punto inicio, punto fin).
- CA-0001.3: Añadir curva circular (punto inicio, punto fin, radio, centro, dirección).
- CA-0001.4: Añadir clotoide (punto inicio, punto fin, parámetro A).
- CA-0001.5: Validar continuidad geométrica entre segmentos consecutivos.
- CA-0001.6: Rechazar segmentos que no conecten.
- CA-0001.7: Obtener la longitud total del alignment.

## Referencias

- UC-001: Analizar eje
- ADR-001: Arquitectura General