# FR-0005: Analizar Municipios

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | FR-0005                 |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Prioridad**   | Alta                    |
| **Módulo**      | Municipalities          |
| **Dependencias**| FR-0003                 |

## Descripción

Identificar todos los municipios cuyo término municipal intersecta total o parcialmente con el buffer generado. Para cada municipio se debe cuantificar la longitud de _alignment_ afectada y los puntos kilométricos de entrada y salida.

## Criterios de Aceptación

1. **Listado de municipios** – Obtener una relación completa de municipios afectados por el buffer.
2. **PK de entrada y salida** – Para cada municipio, determinar el punto kilométrico de entrada y salida del _alignment_ dentro de su término.
3. **Longitud por municipio** – Calcular la longitud total del _alignment_ dentro de cada municipio.
4. **Código INE** – Incluir el código INE del municipio.
5. **Provincia** – Indicar la provincia a la que pertenece cada municipio.
6. **CCAA** – Indicar la comunidad autónoma correspondiente.
7. **Porcentaje de afección** – Calcular el porcentaje del término municipal afectado por el buffer (opcional).
8. **Solapamiento múltiple** – Si el _alignment_ atraviesa varias veces el mismo municipio, se debe acumular la longitud total y reportar todos los segmentos.

## Observaciones

- Los datos administrativos deben obtenerse de una fuente oficial actualizada (IGN, CNIG, CCAA correspondiente).
- Se debe tener en cuenta la posible discontinuidad de los términos municipales (enclaves y exclaves).
