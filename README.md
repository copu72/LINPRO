# LINPRO — Ingeniería Lineal Profesional

**LINPRO** es una plataforma Python para el análisis, diseño y gestión de infraestructuras lineales: líneas eléctricas (MT, AT, 132kV, 220kV, 400kV), carreteras, gasoductos, tuberías y canales.

## Filosofía

- **Plataforma, no programa.** Sistema de plugins modular donde cada análisis es independiente.
- **Objeto central `Project`.** Todos los módulos leen y escriben sobre él. Ninguno habla directamente con otro.
- **Identificador único.** Cada requisito tiene un ID (REQ-XXXX) para trazabilidad total.
- **Documentación primero.** Toda decisión queda registrada en `/decisions/`. Los diagramas viven en `/design/`.

## Estructura

```
LINPRO/
├── decisions/       # Architecture Decision Records (ADR-001...)
├── design/          # Diagramas .drawio (arquitectura, flujos, módulos)
├── docs/            # Especificaciones REQ-XXXX, manuales
├── src/linpro/      # Librería Python (core, geometry, gis, cad, gui...)
├── plugins/         # Módulos independientes (catastro, ríos, carreteras...)
├── tests/           # Unit, integration, regression, performance
├── examples/        # Proyectos reales de prueba
└── data/            # Oficial (vacío), samples, cache, output
```

## Uso

```python
from linpro import Project
from linpro.geometry import Alignment

proj = Project("Línea 132kV")
alignment = Alignment()
alignment.add_straight((0,0), (500,0))
alignment.add_curve((500,0), (600,50), radius=300)
proj.alignment = alignment
proj.run_analysis()
proj.export_excel("informe.xlsx")
```

## Licencia

MIT License.

## Estado

**Sprint 0 — Fundación.** Esqueleto del proyecto, documentación base, ADRs, diagramas.