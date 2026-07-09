# LINPRO — Ingeniería Lineal Profesional

**LINPRO** es una librería Python para el análisis, diseño y gestión de infraestructuras lineales: líneas eléctricas, carreteras, tuberías, canales y cualquier obra cuya geometría se defina mediante un eje.

## Filosofía

- **Una carpeta = una responsabilidad.** Ningún módulo conoce el funcionamiento interno de otro.
- **Objeto central Project.** Todos los módulos leen y escriben sobre él. Ningún módulo habla directamente con otro.
- **Documentación primero.** Cada decisión técnica se registra en docs/adr/. Cada especificación vive en docs/specifications/.

## Uso

`python
from linpro import Project
from linpro.geometry import Alignment
from linpro.roads import RoadAnalyzer

proj = Project("Mi Proyecto")
alignment = Alignment.from_points([(0,0), (100, 50), (200, 200)])
proj.set_alignment(alignment)
`

## Licencia

Ver archivo LICENSE.

## Estado

En fase de definición y construcción del esqueleto.
