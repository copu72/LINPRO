# Review Checklist

**Estado:** ⬜ Pendiente / 🟡 En revisión / ✅ Aprobado / ❌ Rechazado

## 1. Código

- [ ] ¿Sigue PEP 8 y pasa Ruff sin errores?
- [ ] ¿Los type hints son correctos y completos?
- [ ] ¿No hay imports circulares?
- [ ] ¿No hay código comentado?
- [ ] ¿No hay `print()` en código de producción?
- [ ] ¿Las excepciones son propias del módulo?
- [ ] ¿La clase es inmutable (si aplica)?
- [ ] ¿No hay dependencias del módulo hacia capas superiores?

## 2. Tests

- [ ] ¿Cobertura ≥ 95 % (Geometry Engine)?
- [ ] ¿Cubren casos normales, borde y error?
- [ ] ¿Usan pytest (no unittest)?
- [ ] ¿Los nombres son descriptivos?
- [ ] ¿Pasan todos en local?

## 3. Documentación

- [ ] ¿El módulo tiene docstring?
- [ ] ¿La clase tiene docstring con invariantes?
- [ ] ¿Los métodos públicos tienen Args/Returns/Raises?
- [ ] ¿Existe SPEC (Requirements.md, Design.md, API.md)?
- [ ] ¿Existen Examples.md y Tests.md?
- [ ] ¿La documentación está sincronizada con el código?

## 4. Arquitectura

- [ ] ¿Cumple la especificación del módulo?
- [ ] ¿No rompe la compatibilidad con otras clases?
- [ ] ¿No introduce deuda técnica?
- [ ] ¿Los nombres siguen la Naming Convention?
- [ ] ¿Las responsabilidades están bien separadas?

## 5. Rendimiento

- [ ] ¿Las operaciones críticas tienen el coste esperado?
- [ ] ¿Hay benchmarks para operaciones nuevas?

## Veredicto

- [ ] **Aprobado** — merge autorizado.
- [ ] **Aprobado con observaciones** — merge autorizado, corregir observaciones en siguiente sprint.
- [ ] **Rechazado** — no merge, requiere cambios.
