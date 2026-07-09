# FR-0004: Calcular Intersecciones

| Campo           | Valor                       |
| --------------- | --------------------------- |
| **ID**          | FR-0004                     |
| **Versión**     | 1.0                         |
| **Fecha**       | 2026-07-09                  |
| **Prioridad**   | Alta                        |
| **Módulo**      | Geometry.Intersections      |
| **Dependencias**| FR-0001                     |

## Descripción

Calcular las intersecciones entre el _alignment_ y geometrías externas (carreteras, ríos, infraestructuras, límites administrativos, etc.). Esta operación es fundamental para localizar los puntos de cruce y alimentar los análisis sectoriales.

## Criterios de Aceptación

1. **Intersección punto-línea** – Calcular el punto exacto donde una geometría lineal externa cruza el _alignment_.
2. **Intersección polígono-polígono** – Calcular el área de solapamiento entre el buffer y un polígono externo, así como los puntos de entrada y salida del _alignment_ sobre dicho polígono.
3. **Datos de salida** – Para cada intersección se debe devolver:
   - Punto kilométrico (PK) sobre el _alignment_.
   - Coordenada UTM (X, Y) del punto de cruce.
   - Ángulo de cruce con respecto al _alignment_.
4. **Ordenación** – Las intersecciones deben estar ordenadas ascendentemente por PK.
5. **Múltiples intersecciones** – Si una misma geometría externa cruza el _alignment_ en varios puntos, todos ellos deben ser identificados y registrados de forma independiente.
6. **Tolerancia** – Se debe admitir una tolerancia configurable para evitar intersecciones espurias por errores de precisión.

## Observaciones

- La operación debe ser eficiente al trabajar con múltiples geometrías externas simultáneamente.
- Las intersecciones calculadas sirven como _input_ para los análisis de carreteras, hidrografía y municipios.
