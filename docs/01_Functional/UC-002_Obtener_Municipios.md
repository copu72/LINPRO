# UC-002: Obtener Municipios

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | UC-002                  |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Actor**       | Ingeniero               |

## Descripción

El ingeniero ejecuta el análisis de municipios sobre el buffer previamente generado y obtiene el listado de términos municipales afectados.

## Flujo Principal

1. El ingeniero selecciona la opción de análisis de municipios desde el panel de herramientas.
2. El sistema ejecuta `project.run_analysis("municipalities")`.
3. El sistema cruza el buffer con la capa de límites municipales.
4. El sistema calcula los PK de entrada y salida para cada municipio.
5. El sistema presenta los resultados en una tabla con código INE, nombre, provincia, CCAA, PK entrada, PK salida y longitud afectada.
6. El ingeniero puede ordenar, filtrar y exportar el listado.

## Flujos Alternativos

- **Sin buffer previo** – Si no existe un buffer generado, el sistema solicita al ingeniero que lo cree antes de continuar.
- **Municipio sin datos** – Si un municipio no dispone de límites oficiales cargados, se omite y se registra una advertencia.

## Precondiciones

- El proyecto debe tener un _alignment_ definido (FR-0001).
- El buffer debe estar generado (FR-0003).

## Postcondiciones

- Los municipios afectados quedan registrados en el proyecto para su posterior exportación.
