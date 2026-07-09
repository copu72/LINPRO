# 017 — EXCEL

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Biblioteca

- **openpyxl** — Lectura/escritura de archivos Excel (.xlsx).

## Hojas del informe

| Hoja | Contenido |
|------|-----------|
| **Resumen** | Datos generales del proyecto: nombre, fecha, longitud, municipios afectados |
| **Municipios** | Listado detallado con PK entrada/salida, longitud, provincia |
| **Catastro** | Parcelas catastrales con referencia, área, PK, tipo de suelo |
| **Carreteras** | Cruces con carreteras: nombre, PK, ángulo, distancia |
| **Caminos** | Cruces con caminos |
| **Ríos** | Cruces con cursos de agua |
| **Infraestructuras** | Cruces y paralelismos con otras infraestructuras |
| **PK singulares** | PK de apoyos, vértices, puntos de inflexión |

## Formato

- Celdas con formato profesional: bordes, colores de cabecera, anchos automáticos.
- Columna de coordenadas UTM (huso, X, Y).