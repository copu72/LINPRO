# ADR-008: Obtención de datos hidrográficos

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO debe identificar ríos y masas de agua que intersectan el trazado. La información hidrográfica en España está distribuida por Confederaciones Hidrográficas.

## Decisión

Se usa **MITECO** como fuente principal (Red Hidrográfica Nacional) y datos específicos de cada **Confederación Hidrográfica** cuando se requiera detalle adicional.

Razones:

1. MITECO proporciona la capa nacional unificada de ríos y masas de agua.
2. Las CH tienen datos más detallados (caudales, DPH) que se consultan bajo demanda.
3. Formato INSPIRE compatible con GeoPandas.

## Consecuencias

- **Positivo:** Datos nacionales homogéneos.
- **Positivo:** Identificación automática de la CH competente a partir de la ubicación.
- **Negativo:** Las CH tienen distintas APIs y formatos. Se implementará un adaptador por CH si es necesario.