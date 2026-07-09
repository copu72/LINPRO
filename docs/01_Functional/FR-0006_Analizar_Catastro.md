# FR-0006: Analizar Catastro

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | FR-0006                 |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Prioridad**   | Alta                    |
| **Módulo**      | Cadastre                |
| **Dependencias**| FR-0003                 |

## Descripción

Identificar todas las parcelas catastrales que intersectan total o parcialmente con el buffer. Para cada parcela se debe extraer la información catastral disponible y cuantificar el área de afección.

## Criterios de Aceptación

1. **Referencia catastral** – Identificador único de cada parcela (14 o 20 dígitos según el formato oficial).
2. **Área total** – Superficie total de la parcela según el catastro.
3. **Geometría** – Incluir la geometría de la parcela (polígono).
4. **Uso** – Clasificación del suelo (urbano, rústico, industrial, etc.).
5. **Titularidad** – Datos del titular (si están disponibles y la normativa de protección de datos lo permite).
6. **Área de afección** – Superficie de la parcela que queda dentro del buffer, expresada en metros cuadrados y como porcentaje del total.
7. **Agrupación por municipio** – Las parcelas deben poder agruparse por municipio.
8. **Agrupación por clase de suelo** – Las parcelas deben poder agruparse por clase de suelo (urbano, urbanizable, no urbanizable, etc.).
9. **Filtro por afección mínima** – Opción para excluir parcelas cuya área de afección esté por debajo de un umbral configurable.

## Observaciones

- Los datos catastrales deben obtenerse de la Sede Electrónica del Catastro (SEC) o de una fuente autorizada equivalente.
- Se debe respetar la normativa de protección de datos (RGPD/LOPDGDD) en cuanto a la visualización de datos de titularidad.
