# ADR-001: Arquitectura General del Proyecto LINPRO

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO necesita una arquitectura que permita crecer durante años sin necesidad de reestructuraciones. Debe soportar múltiples módulos de análisis (catastro, carreteras, ríos, etc.) que comparten un eje común.

## Decisión

Se adopta una arquitectura de **Fachada + Mediador** centrada en el objeto `Project`:

- `Project` es el único objeto que conocen los módulos externos.
- Cada módulo de análisis (catastro, municipios, etc.) se comunica exclusivamente con `Project`.
- Ningún módulo de análisis conoce la existencia de otro.

## Consecuencias

- **Positivo:** Añadir un nuevo módulo (ej. Red Natura) no requiere modificar ningún módulo existente.
- **Positivo:** Los tests de cada módulo son independientes.
- **Negativo:** `Project` puede crecer mucho. Se mitigará dividiendo la lógica en servicios internos.
- **Negativo:** Puede haber ligeras duplicaciones de funcionalidad entre módulos similares.