# PROJECT_STATUS.md — Cuadro de Mando

**Fecha:** 2026-07-14
**Versión:** 0.4.0
**Lead Architect:** Carlos Olivera

---

## 1. Resumen ejecutivo

**Kernel version:** 0.4.0 (Geometry ABC → Point → BoundingBox → Vector)
**Project version:** 0.1.0-dev

Geometry Kernel v0.4.0 certificado y Computational Geometry Engine v0.1
operativo con 9 operadores (GEOM-OPS-001 a 009), 118 tests, 99% cobertura.
RFC-0005 certificado. Preparado para Segment.

---

## 2. RFCs

| ID | Título | Estado |
|---|---|---|
| RFC-0001 | Geometry Kernel | ✅ Aprobado |
| RFC-0002 | Point | ✅ Aprobado |
| RFC-0003 | BoundingBox | ✅ Aprobado |
| RFC-0004A | Álgebra Vectorial | ✅ Aprobado y congelado |
| RFC-0005 | Computational Geometry Operators | ✅ CERTIFICADO Y CONGELADO |

---

## 3. Architecture Layers

```
Computational Geometry Engine (v0.1)     ← NUEVO
│
├── Geometry Kernel (v0.4.0 CERTIFIED)
│   ├── Geometry ABC     ✅
│   ├── Point            ✅
│   ├── BoundingBox      ✅
│   └── Vector           ✅
│
├── Computational Geometry Operators (v0.1)
│   ├── orientation      ✅ GEOM-OPS-001
│   ├── is_collinear     ✅ GEOM-OPS-002
│   ├── is_parallel      ✅ GEOM-OPS-003
│   ├── is_perpendicular ✅ GEOM-OPS-004
│   ├── distance         ✅ GEOM-OPS-005
│   ├── project          ✅ GEOM-OPS-006
│   ├── closest_point    ✅ GEOM-OPS-007
│   ├── intersect        ✅ GEOM-OPS-008
│   └── bbox_ops         ✅ GEOM-OPS-009
│
└── Future Entities
    ├── Segment          ✅
    ├── Polyline         ⏳
    └── Line             ⏳
```

## 4. Geometry Kernel — Estado por entidad

```
Geometry ABC      ✅  (97% cov)
Point             ✅  (98% cov, 60 tests)
BoundingBox       ✅  (100% cov, 87 tests)
Vector            ✅  (100% cov, 133 tests, benchmark)
Segment           ✅  (100% cov, 142 tests, benchmark)  ← NUEVO
Polyline          ⏳  (pendiente)
```

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
| **Vector** | `primitives/vector.py` | 173 | 100% | ✅ **CERTIFICADO** |

### 3.2 Prototipos (pendientes de reescribir)

| Módulo | Archivo | Lines | Cobertura | Plan |
|---|---|---|---|---|
| **Segment** | `primitives/segment.py` | 117 | 100% | ✅ **CERTIFICADO** |
| Precision | `kernel/precision.py` | 17 | 0% | Revisar integración |

### 3.3 Tests

| Suite | Tests | Estado |
|---|---|---|
| Kernel (Tolerance + Validators + Geometry) | 62 | ✅ Todos pasando |
| Point (TASK-0003A) | 60 | ✅ Todos pasando |
| BoundingBox (TASK-0003B) | 87 | ✅ Todos pasando |
| Vector (TASK-0004B) | 133 | ✅ Todos pasando |
| Operators (TASK-0005A) | 118 | ✅ Todos pasando |
| Segment (TASK-0005B) | 142 | ✅ Todos pasando |
| **Total Geometry** | **602** | **✅ 0 fallos** |
| **Total proyecto** | **694** | **✅ 0 fallos** |

---

## 7. Cobertura global

| Alcance | Cobertura | Notas |
|---|---|---|
| Geometry Kernel testado (ABC + Point + BBox + Vector) | **99.5%** | 4 clases, 589 líneas |
| Geometry completo (con prototipos sin tests) | 89% | Segment, Precision pendientes |
| **Objetivo** | **≥95%** | Solo se mide sobre código completado |

---

## 5. Deuda técnica

| Ítem | Tipo | Impacto | Plan |
|---|---|---|---|---|
| `precision.py` (prototipo) | Código legacy sin tests | Bajo | Revisar integración |
| `precision.py` (prototipo, 17 lines) | Código legacy sin tests | Bajo (no usado) | Revisar si se integra o elimina |
| `__str__` no testeado en `Geometry` | 1 línea no cubierta | Muy bajo | Esperar a próxima entidad |
| Líneas 77-78 en `point.py` | 2 líneas inalcanzables | Muy bajo | Catch en `is_valid` |

**Deuda técnica total:** Muy baja. Vector certificado sin deuda. No hay bloqueadores.

---

## 6. Riesgos y reglas vigentes

| Regla | Descripción | Origen |
|---|---|---|
| **Modelo antes que código** | Ninguna entidad se implementa hasta que su modelo matemático esté definido y aprobado | RFC-0004A |
| **Dominio sobre primitivas** | Ninguna clase devuelve tipos primitivos cuando existe una entidad del dominio | Lead Architect |
| **No Point + Point** | La suma de dos posiciones no tiene significado geométrico | RFC-0004A |

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| RFC-0005 sin abrir bloquea Segment/Polyline | Alta | Medio | Abrir RFC-0005 al certificar Vector |
| `geometry.py` crece con cada nueva entidad | Media | Bajo | Refactorizar si supera 400 líneas |
| Prototipos antiguos confunden al desarrollador | Baja | Bajo | Borrar o marcar como `@deprecated` |

---

## 8. Próximos objetivos — Hito A (Motor Geométrico Completo)

**🎯 Objetivo:** Polyline + PK Engine funcional, demo sobre línea real.

1. ✅ **TASK-0003A** — Point (APROBADO)
2. ✅ **TASK-0003B** — BoundingBox (APROBADO)
3. ✅ **RFC-0004A** — Álgebra Vectorial (modelo matemático, congelado)
4. ✅ **TASK-0004B** — Vector (CERTIFICADO, Kernel v0.4.0)
5. ✅ **RFC-0005** — Computational Geometry Operators (CERTIFICADO)
6. ✅ **TASK-0005A** — Operators Package (9 operadores, 118 tests)
7. ✅ **TASK-0005B** — Segment (CERTIFICADO, 142 tests, 100% cov)
8. ⏳ **TASK-0006** — Polyline
9. ⏳ **PK Engine** — `point_at_pk`, `pk_of_point`, `project`, `subline`

---

> **Flujo:** Operators → Segment → Polyline → PK Engine → Primera demo real.

---

## 8. Jerarquía y documentos del Geometry Engine

```
Geometry (ABC)        ✅ Kernel v0.4.0
│
├── Point             ✅ Certificado (98% cov, 60 tests)
├── BoundingBox       ✅ Certificado (100% cov, 87 tests)
├── Vector            ✅ Certificado (100% cov, 133 tests, benchmark)
├── Segment           ✅ Certificado (100% cov, 142 tests, benchmark)
│
├── Curve (ABC)       📅 Futuro
│   ├── Line
│   ├── Polyline      🎯 Siguiente hito
│   ├── Arc
│   └── Circle
│
└── Surface (ABC)     📅 Futuro
    └── Polygon
```

Documentos matemáticos permanentes:

| Documento | Ubicación | Descripción |
|---|---|---|
| Álgebra Vectorial | `docs/Geometry/Kernel/Algebra.md` | Especificación matemática del motor. 30 operaciones definidas |
| RFC-0004A | `docs/RFC/RFC-0004A-Algebra-Vectorial.md` | ✅ Aprobado y congelado. 30 responsabilidades, 4 ADRs |
| RFC-0005 | `docs/Geometry/RFC/RFC-0005-Computational-Geometry-Operators.md` | ✅ CERTIFICADO. 9 operadores, 5 ADRs |
| ADR-0007 | `GEOMETRY_KERNEL_SPEC.md §19` | Strong Types — no primitivas cuando existe entidad de dominio |
| ADR-0008 | `GEOMETRY_KERNEL_SPEC.md §19` | Inmutabilidad total del Kernel |
| ADR-0009 | `GEOMETRY_KERNEL_SPEC.md §19` | Versionado independiente del Kernel |

## 9. Álgebra de operadores — Reglas vigentes

Decisión arquitectónica clave (RFC-0004A, congelada):

| Operación | Resultado | Estado |
|---|---|---|
| Point - Point | Vector | ✅ Implementado |
| Point + Vector | Point | ✅ Implementado |
| Point - Vector | Point | ✅ Implementado |
| Vector + Vector | Vector | ✅ Implementado |
| Vector - Vector | Vector | ✅ Implementado |
| Vector * escalar | Vector | ✅ Implementado |
| escalar * Vector | Vector | ✅ Implementado |
| Vector / escalar | Vector | ✅ Implementado |
| -Vector | Vector | ✅ Implementado |
| Point + Point | ❌ Error | 🚫 Prohibido |
| Point * escalar | ❌ Error | 🚫 Prohibido |

> **Nuevo:** Vector + Point = Point (vía `__radd__`).

---

## 10. Líneas de código (LOC)

| Módulo | Líneas | % del total |
|---|---|---|---|
| Kernel (constants, geometry, tolerance, validation) | 247 | 27% |
| Point | 108 | 12% |
| BoundingBox | 134 | 14% |
| Vector | 173 | 19% |
| Operators (9 módulos) | 175 | 19% |
| Segment | 117 | 12% |
| **Total Geometry Engine** | **954** | 100% |

---

*Documento generado el 2026-07-14. Próxima actualización: al certificar Segment (TASK-0005B).*
