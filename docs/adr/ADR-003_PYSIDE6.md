# ADR-003: PySide6 para la interfaz gráfica

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO necesita una interfaz gráfica para usuarios que no trabajan con Python directamente. Se evaluaron Tkinter, PyQt6 y PySide6.

## Decisión

Se elige **PySide6** (bindings oficiales de Qt6) por:

1. **Licencia LGPL** — Permite uso comercial sin restricciones.
2. **Bindings oficiales** de Qt Company.
3. **Moderno** — Qt6 es la versión actual.
4. **Documentación** oficial completa.

## Consecuencias

- **Positivo:** Interfaz profesional y multiplataforma.
- **Positivo:** Arquitectura MVC clara.
- **Negativo:** El instalador base pesa ~50MB. Se usará PyInstaller para empaquetar.
- **Negativo:** Curva de aprendizaje para desarrolladores no familiarizados con Qt.