# Módulo Reports — Generación de informes PDF

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Generación de informes técnicos en formato PDF con los resultados completos del análisis del proyecto.

## API pública

```python
class PDFReport:
    def __init__(self, project: Project)
```

**Métodos:**

```python
def generate(self, path: str, template: str = "default") -> str
```
Genera el informe PDF en la ruta especificada usando la plantilla indicada. Retorna la ruta absoluta del archivo generado.

### Estructura del informe

| Sección                | Contenido                             |
| ---------------------- | ------------------------------------- |
| Portada                | Título, proyecto, fecha, autor.       |
| Resumen ejecutivo      | Datos principales del proyecto.       |
| 1. Introducción        | Objeto del proyecto y metodología.    |
| 2. Trazado             | Tabla y perfil de puntos kilométricos. |
| 3. Afección municipal  | Análisis por municipio.               |
| 4. Afección catastral   | Parcelas afectadas con planos.        |
| 5. Cruces              | Carreteras, hidrografía e infraestructuras. |
| 6. Conclusiones        | Resumen de afecciones.                |
| Anexos                 | Planos y tablas complementarias.      |

## Dependencias

- `reportlab` o `weasyprint` para generación de PDF.
- `jinja2` para renderizado de plantillas HTML (si se usa weasyprint).
- `linpro.gis` y `linpro.excel` para obtener los datos.

## Uso básico

```python
from linpro.gis import Project
from linpro.reports import PDFReport

project = Project("C:/data/proyecto.linpro")
report = PDFReport(project)
report.generate("C:/data/informe_final.pdf")
```

## Plantillas

Las plantillas se almacenan en `linpro/reports/templates/`. Es posible crear plantillas personalizadas heredando de la plantilla base.