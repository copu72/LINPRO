# FR-0010: Exportar Plano DXF

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | FR-0010                 |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Prioridad**   | Alta                    |
| **Módulo**      | DWG                     |
| **Dependencias**| FR-0001, FR-0003        |

## Descripción

Generar un plano en formato DXF con la información geométrica del proyecto organizada en capas temáticas. El archivo debe ser compatible con AutoCAD 2018 y versiones posteriores, permitiendo su integración en flujos de trabajo CAD existentes.

## Criterios de Aceptación

1. **Capa EJE** – Geometría del _alignment_ (línea continua, color asignado).
2. **Capa PK** – Puntos kilométricos etiquetados sobre el _alignment_ (bloques o texto).
3. **Capa BUFFER** – Polígono del buffer (simétrico o asimétrico) con relleno semitransparente o _hatch_.
4. **Capa MUNICIPIOS** – Límites municipales afectados, con etiqueta del nombre del municipio.
5. **Capa CATASTRO** – Parcelas catastrales afectadas, con etiqueta de referencia catastral.
6. **Capa CRUCES_VIARIO** – Puntos de cruce con carreteras, con símbolo y etiqueta del nombre de la vía.
7. **Capa CRUCES_HIDRO** – Puntos de cruce con cursos de agua, con símbolo y etiqueta del nombre del río/arroyo.
8. **Capa INFRA_EXISTENTE** – Infraestructuras existentes detectadas (opcional).
9. **Compatibilidad AutoCAD 2018+** – El DXF debe poder abrirse sin errores en AutoCAD 2018, 2019, 2020, 2021, 2022, 2023, 2024 y 2025.
10. **Sistema de coordenadas** – El DXF debe incluir la referencia al sistema de coordenadas utilizado (ETRS89 UTM huso correspondiente).

## Observaciones

- Se debe utilizar el formato DXF ASCII para máxima compatibilidad entre versiones.
- Las capas deben tener colores y tipos de línea predefinidos según una convención establecida.
- Los textos deben usar fuentes estándar de AutoCAD (SHX).
