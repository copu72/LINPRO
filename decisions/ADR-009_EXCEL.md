# ADR-009: Generación de informes Excel

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO debe generar informes profesionales en Excel. Se evaluaron openpyxl, xlsxwriter y pandas ExcelWriter.

## Decisión

Se usa **openpyxl** como motor principal de escritura Excel.

Razones:

1. **Formato .xlsx** nativo (no .xls legacy).
2. **Control total** sobre formato: bordes, colores, anchos de columna, imágenes.
3. **Compatible con** pandas ExcelWriter (útil para volcado rápido de DataFrames).
4. **Sin dependencias externas** a Office.

## Consecuencias

- **Positivo:** Informes profesionales con formato completo.
- **Positivo:** Se pueden leer y modificar informes existentes.
- **Negativo:** Mayor verbosidad que pandas solo. Se creará una capa de abstracción para simplificar la generación de informes.