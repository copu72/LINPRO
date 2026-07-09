# UC-003: Obtener Parcelas

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | UC-003                  |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Actor**       | Ingeniero               |

## Descripción

El ingeniero ejecuta el análisis catastral para identificar las parcelas afectadas por el buffer y puede filtrar los resultados por municipio para su revisión y exportación.

## Flujo Principal

1. El ingeniero selecciona la opción de análisis catastral desde el panel de herramientas.
2. El sistema ejecuta la consulta catastral cruzando el buffer con la capa de parcelas.
3. Para cada parcela, el sistema extrae la referencia catastral, área, geometría, uso y área de afección.
4. El sistema presenta los resultados agrupados por municipio.
5. El ingeniero aplica un filtro por municipio concreto para revisar únicamente las parcelas de ese término.
6. El sistema filtra la tabla mostrando solo las parcelas del municipio seleccionado.
7. El ingeniero exporta el listado filtrado al informe Excel (FR-0009) o al plano DXF (FR-0010).

## Flujos Alternativos

- **Filtro por clase de suelo** – El ingeniero puede filtrar también por clase de suelo (urbano, rústico, etc.).
- **Umbral de afección** – El ingeniero puede establecer un porcentaje mínimo de afección para excluir parcelas marginales.
- **Sin conexión catastral** – Si el servicio catastral no está disponible, el sistema informa y permite reintentar más tarde.

## Precondiciones

- El proyecto debe tener un _alignment_ definido (FR-0001).
- El buffer debe estar generado (FR-0003).
- La conexión con la fuente de datos catastrales debe estar operativa.

## Postcondiciones

- Las parcelas afectadas quedan registradas en el proyecto con sus datos asociados.
