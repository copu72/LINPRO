# FR-0008: Analizar Hidrografía

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | FR-0008                 |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Prioridad**   | Alta                    |
| **Módulo**      | Hydrology               |
| **Dependencias**| FR-0003                 |

## Descripción

Identificar todos los cursos de agua (ríos, arroyos, ramblas) y masas de agua (embalses, lagos, humedales) que intersectan el buffer. Para cada elemento se deben calcular los parámetros del cruce y la información hidrológica relevante.

## Criterios de Aceptación

1. **Nombre** – Denominación del curso o masa de agua (si está disponible).
2. **Tipo** – Clasificación: permanente o estacional/temporal.
3. **PK de cruce** – Punto kilométrico del _alignment_ en el que se produce la intersección.
4. **Confederación Hidrográfica (CH) competente** – Identificar la CH correspondiente (CH Ebro, CH Guadalquivir, CH Duero, etc.).
5. **Distancia de cruce** – Longitud del tramo del curso de agua dentro del buffer en el punto de cruce.
6. **Caudal estimado** – Si está disponible, incluir información de caudal medio (opcional).
7. **Zona de policía** – Indicar si el cruce se encuentra dentro de zona de policía de aguas (100 m desde la ribera).
8. **Masas de agua superficial** – Para embalses y lagos, calcular el área de afección dentro del buffer y la capacidad si el dato está disponible.

## Observaciones

- Los datos hidrológicos deben obtenerse del MITECO (Ministerio para la Transición Ecológica) o de las Confederaciones Hidrográficas correspondientes.
- Para los cursos estacionales, debe indicarse el período aproximado de caudal (si la información está disponible).
