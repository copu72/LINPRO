# 005 — REQUISITOS NO FUNCIONALES

**Versión:** 0.0.1  
**Fecha:** 2026-07-09

1. **RNF-01 Rendimiento:** El cálculo de afecciones para un trazado de 50km debe completarse en menos de 5 minutos.
2. **RNF-02 Memoria:** El uso de RAM no debe superar los 2GB para trazados de hasta 100km.
3. **RNF-03 Portabilidad:** Debe ejecutarse en Windows 10/11, Linux y macOS sin dependencias de QGIS.
4. **RNF-04 Idioma:** El código, la API y la documentación interna serán en español.
5. **RNF-05 Tipado:** 100% del código con type hints.
6. **RNF-06 Cobertura de tests:** Mínimo 90% en unit, 70% en integración.
7. **RNF-07 Compatibilidad:** Los DWG generados serán compatibles con AutoCAD 2018+.
8. **RNF-08 Actualización:** Los datos oficiales se descargan bajo demanda, no se almacenan en el repositorio.
