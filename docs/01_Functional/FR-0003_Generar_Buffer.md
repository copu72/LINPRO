# FR-0003: Generar Buffer

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | FR-0003                 |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Prioridad**   | Alta                    |
| **Módulo**      | Geometry.Buffer         |
| **Dependencias**| FR-0001                 |

## Descripción

Generar un buffer simétrico o asimétrico alrededor del _alignment_ definido en el proyecto. El buffer constituye la zona de influencia o área de estudio sobre la que se ejecutarán los análisis posteriores (municipios, catastro, carreteras, hidrografía, etc.).

## Criterios de Aceptación

1. **Buffer simétrico** – El usuario puede especificar una distancia única que se aplica a ambos lados del _alignment_ (izquierda y derecha).
2. **Buffer asimétrico** – El usuario puede especificar distancias diferentes para el lado izquierdo y el lado derecho del _alignment_.
3. **Polígono cerrado** – El resultado del buffer debe ser un polígono cerrado y válido, sin autointersecciones.
4. **Recálculo automático** – El buffer se debe recalcular automáticamente cuando se modifique el _alignment_ o cualquiera de las distancias configuradas.
5. **Unidades configurables** – Las distancias deben poder expresarse en metros (u otra unidad definida en el proyecto).
6. **Geometría editable** – La geometría generada debe poder ser almacenada y reutilizada en análisis posteriores.

## Observaciones

- La operación de buffer debe estar optimizada para _alignments_ de gran longitud (decenas de kilómetros).
- Debe preservarse la topología del _alignment_ original, incluyendo curvas y transiciones.
