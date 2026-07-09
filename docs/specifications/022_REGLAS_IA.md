# 022 — REGLAS PARA ASISTENTES IA

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Reglas fundamentales

1. **Documentación primero:** No escribir una línea de código hasta que el documento de especificación correspondiente esté redactado.
2. **ADR antes que código:** Cualquier decisión técnica significativa debe documentarse en `docs/adr/` antes de implementarse.
3. **Tests antes que código:** Toda función nueva debe tener su test unitario definido conceptualmente antes de escribir la implementación.
4. **Un módulo = una responsabilidad.** Si un módulo hace dos cosas diferentes, dividirlo.
5. **Nunca depender de QGIS, AutoCAD u otro software propietario.** El código debe ejecutarse con `pip install linpro`.
6. **Type hints obligatorios.** Todo parámetro y retorno debe estar tipado.
7. **Sin comentarios superfluos.** El código debe ser autoexplicativo. No añadir comentarios salvo para documentar decisiones no obvias.
8. **Documentación en español.** Código, API, docstrings y documentación en español.
9. **No subir datos oficiales al repositorio.** Los datos se descargan bajo demanda.
10. **Seguir la estructura acordada.** No crear archivos ni carpetas fuera de la jerarquía establecida.