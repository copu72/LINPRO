# FR-0009: Exportar Informe Excel

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | FR-0009                 |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Prioridad**   | Alta                    |
| **Módulo**      | Excel                   |
| **Dependencias**| FR-0005, FR-0006, FR-0007, FR-0008 |

## Descripción

Generar un informe en formato Microsoft Excel (`.xlsx`) que compile todos los resultados de los análisis sectoriales realizados sobre el buffer. El informe debe presentar la información de forma estructurada y profesional, con formato adecuado para su presentación a clientes o administraciones.

## Criterios de Aceptación

1. **Hoja Resumen** – Datos generales del proyecto, parámetros del _alignment_, fechas y estadísticas globales (longitud total, número de municipios, parcelas, carreteras, ríos).
2. **Hoja Municipios** – Listado de municipios con código INE, provincia, CCAA, PK entrada/salida, longitud afectada.
3. **Hoja Catastro** – Listado de parcelas con referencia catastral, área total, área de afección, porcentaje, uso, municipio y clase de suelo.
4. **Hoja Carreteras** – Listado de carreteras con nombre, tipo, PK de cruce, distancia perpendicular, ángulo de cruce.
5. **Hoja Ríos** – Listado de cursos de agua con nombre, tipo, PK de cruce, CH competente, distancia de cruce.
6. **Hoja Infraestructuras** – Otras infraestructuras detectadas (opcional, reservada para ampliaciones futuras).
7. **Hoja PK Singulares** – Puntos kilométricos singulares (inicio, fin, cambios de municipio, intersecciones relevantes).
8. **Formato profesional** – Encabezados con estilo, celdas con anchos adecuados, números formateados (decimales, separadores de miles), colores corporativos o de la administración.
9. **Coordenadas UTM** – Todas las coordenadas deben expresarse en UTM (huso 29, 30 o 31 según corresponda, datum ETRS89).
10. **Escalabilidad** – El libro debe poder contener miles de filas sin degradación del rendimiento.

## Observaciones

- No se requiere Microsoft Excel instalado; el archivo debe generarse mediante librerías nativas (ej. OpenXML, xlsxwriter o equivalente).
- El formato debe ser compatible con Excel 2016 y versiones posteriores.
