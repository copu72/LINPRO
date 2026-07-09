# ADR-010: Estrategia de instalación y distribución

**Fecha:** 2026-07-09
**Estado:** Aceptado

## Contexto

LINPRO debe distribuirse a usuarios que no tienen Python instalado. Se evaluaron PyInstaller, Nuitka, y distribución vía pip.

## Decisión

**Doble canal de distribución:**

1. **vía pip** (`pip install linpro`) — Para usuarios con Python.
2. **Ejecutable portátil** (PyInstaller) — Para usuarios sin Python.

Razones:

1. pip es el estándar de la comunidad Python.
2. PyInstaller empaqueta todo en un solo ejecutable sin requisitos de instalación.
3. El instalador MSI se reserva para versiones estables.

## Consecuencias

- **Positivo:** Usuarios técnicos y no técnicos pueden usar LINPRO.
- **Positivo:** El ejecutable portátil funciona en Windows sin instalación.
- **Negativo:** PyInstaller genera ejecutables grandes (~100MB). Se optimizará en releases.
- **Negativo:** Antivirus pueden marcar el ejecutable. Se firmará digitalmente.