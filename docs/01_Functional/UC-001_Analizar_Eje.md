# UC-001: Analizar Eje

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | UC-001                  |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Actor**       | Ingeniero               |

## Descripción

Caso de uso principal del sistema. El ingeniero crea un nuevo proyecto, define el _alignment_ del trazado, calcula su replanteo (PK), genera el buffer de análisis y exporta los resultados.

## Flujo Principal

1. El ingeniero inicia la aplicación y crea un nuevo proyecto.
2. Define el _alignment_ (trazado en planta) mediante la introducción de vértices y curvas.
3. El sistema calcula el replanteo del _alignment_ (puntos kilométricos cada 20 m o según configuración).
4. El ingeniero configura las distancias del buffer (simétrico o asimétrico) y solicita su generación.
5. El sistema genera el polígono del buffer y lo superpone sobre el _alignment_.
6. El ingeniero ejecuta los análisis sectoriales disponibles (municipios, catastro, carreteras, hidrografía).
7. El sistema presenta los resultados en pantalla de forma estructurada.
8. El ingeniero exporta los informes (Excel) y planos (DXF) según las necesidades del proyecto.

## Flujos Alternativos

- **Error en la definición del _alignment_** – El sistema valida la geometría e informa de errores de topología o inconsistencia.
- **Buffer inválido** – Si las distancias configuradas producen un buffer no válido (autointersección), el sistema notifica al usuario.
- **Origen de datos no disponible** – Si alguna fuente de datos externa no está accesible, se informa al usuario y se omite el análisis correspondiente.

## Precondiciones

- El ingeniero dispone de credenciales de acceso a los servicios de datos geográficos necesarios (opcional).

## Postcondiciones

- Se genera un proyecto con todos los resultados de los análisis ejecutados.
- Los informes y planos quedan disponibles en el directorio de salida configurado.
