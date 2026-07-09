# UC-004: Cruce de Carretera

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | UC-004                  |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Actor**       | Ingeniero               |

## Descripción

El ingeniero identifica los puntos de cruce entre el _alignment_ y las carreteras existentes, visualizando el PK y el ángulo de intersección para cada cruce detectado.

## Flujo Principal

1. El ingeniero selecciona la opción de análisis de carreteras desde el panel de herramientas.
2. El sistema cruza el buffer con la capa de carreteras.
3. El sistema calcula las intersecciones entre el _alignment_ y cada carretera (FR-0004).
4. Para cada intersección, el sistema calcula:
   - PK del cruce sobre el _alignment_.
   - Coordenada UTM del punto de cruce.
   - Ángulo de cruce (grados sexagesimales).
   - Distancia perpendicular entre ejes.
5. El sistema presenta los resultados en una tabla ordenada por PK.
6. El ingeniero puede seleccionar un cruce concreto para visualizar sus detalles en el mapa.
7. El ingeniero exporta el listado al informe Excel o al plano DXF.

## Flujos Alternativos

- **Cruce inexistente** – Si no se detectan cruces, el sistema muestra un mensaje informativo.
- **Múltiples cruces** – Si una misma carretera cruza el _alignment_ en varios puntos, todos se muestran de forma independiente.
- **Cruce a distinto nivel** – Si se dispone de datos de cota, el sistema indica si el cruce es en superficie, en viaducto o en túnel.

## Precondiciones

- El proyecto debe tener un _alignment_ definido (FR-0001).
- El buffer debe estar generado (FR-0003).
- La capa de carreteras debe estar cargada en el proyecto.

## Postcondiciones

- Los cruces detectados quedan registrados en el proyecto para su exportación y visualización.
