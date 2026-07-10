# PROJECT_STATUS.md — Cuadro de Mando

**Fecha:** 2026-07-10
**Versión:** 0.1.0
**Lead Architect:** Carlos Olivera

---

## 1. Resumen ejecutivo

**Kernel version:** 0.3.0 (Geometry ABC → Point → BoundingBox)
**Project version:** 0.1.0-dev

Sprint 3.1 completado (Geometry Kernel). Sprint 3.2 en curso con TASK-0003A
(Point) aprobada ✅ y TASK-0003B (BoundingBox) implementada ✅.

El Geometry Engine está consolidando su base: tolerancias, validaciones,
contrato `Geometry(ABC)` y dos primitivas completas con cobertura ≥ 95%.

---

## 2. RFCs

| ID | Título | Estado |
|---|---|---|
| RFC-0001 | Geometry Kernel | ✅ Aprobado |
| RFC-0002 | Point | ✅ Aprobado |
| RFC-0003 | BoundingBox | ✅ Aprobado |
| RFC-0004A | Álgebra Vectorial | ✅ Aprobado y congelado |

---

## 3. Módulos del Geometry Engine

### 3.1 Completados (testeados, lint, docs)

| Módulo | Archivo | Lines | Cobertura | Estado |
|---|---|---|---|---|
| Geometry (ABC) | `kernel/geometry.py` | 88 | 97% | ✅ |
| Tolerance | `kernel/tolerance.py` | 69 | 98% | ✅ |
| Validators | `kernel/validation.py` | 75 | 94% | ✅ |
| Constants | `kernel/constants.py` | 15 | 100% | ✅ |
| Exceptions | `exceptions/*.py` | 5 archivos | 100% | ✅ |
| **Point** | `primitives/point.py` | 117 | 98% | ✅ **APROBADO** |
| **BoundingBox** | `primitives/bbox.py` | 211 | 100% | ✅ **IMPLEMENTADO** |

### 3.2 Prototipos (pendientes de reescribir)

| Módulo | Archivo | Lines | Cobertura | Sprint |
|---|---|---|---|---|
| Vector | `primitives/vector.py` | 63 | 0% | Sprint 3.3 |
| Segment | `primitives/segment.py` | 73 | 0% | Sprint 3.3 |
| Precision | `kernel/precision.py` | 17 | 0% | Sprint 3.3 |

### 3.3 Tests

| Suite | Tests | Estado |
|---|---|---|
| Kernel (Tolerance + Validators + Geometry) | 62 | ✅ Todos pasando |
| Point (TASK-0003A) | 60 | ✅ Todos pasando |
| BoundingBox (TASK-0003B) | 87 | ✅ Todos pasando |
| **Total** | **209** | **✅ 0 fallos** |

---

## 4. Cobertura global

| Alcance | Cobertura | Notas |
|---|---|---|
| Geometry completo (sin prototipos) | 99% | Solos modules testeados |
| Geometry completo (con prototipos) | 72% | Vector, Segment, Precision no tienen tests |
| **Objetivo** | **≥95%** | Solo se mide sobre código completado |

---

## 5. Deuda técnica

| Ítem | Tipo | Impacto | Plan |
|---|---|---|---|
| `segment.py` (prototipo, 73 lines) | Código legacy sin tests | Bajo (no importado) | Reescritura RFC-0004 |
| `vector.py` (prototipo, 63 lines) | Código legacy sin tests | Bajo (no importado) | Reescritura RFC-0005 |
| `precision.py` (prototipo, 17 lines) | Código legacy sin tests | Bajo (no usado) | Revisar si se integra o elimina |
| `__str__` no testeado en `Geometry` | 1 línea no cubierta | Muy bajo | Esperar a próxima entidad |
| Líneas 77-78 en `point.py` | 2 líneas inalcanzables | Muy bajo | Catch en `is_valid` |

**Deuda técnica total:** Muy baja. No hay bloqueadores.

---

## 6. Riesgos y reglas vigentes

| Regla | Descripción | Origen |
|---|---|---|
| **Modelo antes que código** | Ninguna entidad se implementa hasta que su modelo matemático esté definido y aprobado | RFC-0004A |
| **Dominio sobre primitivas** | Ninguna clase devuelve tipos primitivos cuando existe una entidad del dominio | Lead Architect |
| **No Point + Point** | La suma de dos posiciones no tiene significado geométrico | RFC-0004A |

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Vector sin implementar bloquea Segment/Line | Alta | Medio | Priorizar RFC-0004 tras BoundingBox |
| `geometry.py` crece con cada nueva entidad | Media | Bajo | Refactorizar si supera 400 líneas |
| Prototipos antiguos confunden al desarrollador | Baja | Bajo | Borrar o marcar como `@deprecated` |

---

## 7. Próximos objetivos (Sprint 3.2)

1. ✅ **TASK-0003A** — Point (APROBADO)
2. ✅ **TASK-0003B** — BoundingBox (APROBADO)
3. 📝 **RFC-0004A** — Álgebra Vectorial (modelo matemático)
4. 📝 **RFC-0004B** — Vector (implementación)
5. 📝 **RFC-0005** — Segment

> **Regla:** Ninguna entidad se implementa hasta que su modelo matemático
> esté definido y aprobado (RFC-0004A antes que Vector).

---

## 8. Jerarquía y documentos del Geometry Engine

```
Geometry (ABC)
│
├── Point          ✅ Completado (98% cov)
├── BoundingBox    ✅ Completado (100% cov)
├── Vector         📝 Álgebra definida (RFC-0004A); impl. pendiente
├── Segment        📅 Prototipo (0% cov, pendiente)
│
├── Curve (ABC)    📅 Futuro Sprint 3.3
│   ├── Line
│   ├── Polyline
│   ├── Arc
│   └── Circle
│
└── Surface (ABC)  📅 Futuro
    └── Polygon
```

Documentos matemáticos permanentes:

| Documento | Ubicación | Descripción |
|---|---|---|
| Álgebra Vectorial | `docs/Geometry/Algebra.md` | Especificación matemática del motor. 30 operaciones definidas |
| RFC-0004A | `docs/RFC/RFC-0004A-Algebra-Vectorial.md` | ✅ Aprobado y congelado. 30 responsabilidades, 4 ADRs |
| ADR-0007 | `GEOMETRY_KERNEL_SPEC.md §19` | Strong Types — no primitivas cuando existe entidad de dominio |
| ADR-0008 | `GEOMETRY_KERNEL_SPEC.md §19` | Inmutabilidad total del Kernel |
| ADR-0009 | `GEOMETRY_KERNEL_SPEC.md §19` | Versionado independiente del Kernel |

## 9. Reglas de álgebra de operadores

Decisión arquitectónica clave (RFC-0004A):

| Operación | Resultado | Estado |
|---|---|---|
| Point - Point | Vector | ✅ Permitido |
| Point + Vector | Point | ✅ Permitido |
| Point - Vector | Point | ✅ Permitido |
| Vector + Vector | Vector | ✅ Permitido |
| Vector - Vector | Vector | ✅ Permitido |
| Vector * escalar | Vector | ✅ Permitido |
| escalar * Vector | Vector | ✅ Permitido |
| Vector / escalar | Vector | ✅ Permitido |
| -Vector | Vector | ✅ Permitido |
| Point + Point | ❌ Error | 🚫 Prohibido |
| Point * escalar | ❌ Error | 🚫 Prohibido |

---

## 10. Líneas de código (LOC)

| Módulo | Líneas | % del total |
|---|---|---|
| Kernel (constants, geometry, tolerance, validation) | 247 | 43% |
| Primitivas (point, bbox) | 328 | 57% |
| Prototipos (vector, segment, precision) | 153 | — (no cuentan) |
| **Total Geometry Engine** | **575** | 100% |

---

*Documento generado el 2026-07-10. Próxima actualización: al cierre del Sprint 3.2.*
