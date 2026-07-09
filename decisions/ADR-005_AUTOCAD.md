# ADR-005: Estrategia de compatibilidad con AutoCAD

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO debe generar planos compatibles con AutoCAD, la plataforma CAD estándar en ingeniería civil en España.

## Decisión

Se usa **DXF como formato primario** mediante la librería `ezdxf`. No se depende de AutoCAD ni de su API COM/.NET.

Razones:

1. **DXF es un estándar abierto** documentado por Autodesk.
2. **ezdxf** es madura, puramente Python, sin dependencias externas.
3. **Independencia** de licencias de AutoCAD.

## Consecuencias

- **Positivo:** Los planos se abren directamente en AutoCAD, Civil 3D, QGIS, etc.
- **Positivo:** No requiere licencia de AutoCAD para generar planos.
- **Negativo:** No se puede leer DWG nativo (formato propietario cerrado). Se usa DXF como entrada/salida.
- **Negativo:** Algunas entidades complejas (sombras, renders) no son exportables a DXF.