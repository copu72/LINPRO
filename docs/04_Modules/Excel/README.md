# Módulo Excel — Generación de informes Excel

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Generación de informes en formato Excel (.xlsx) con los resultados del análisis del proyecto.

## Requisitos funcionales

| ID      | Descripción                |
| ------- | -------------------------- |
| FR-0009 | Exportar Excel.            |

## API pública

```python
class ExcelReport:
    def __init__(self, project: Project)
```

**Métodos:**

```python
def generate(self, path: str) -> str
```
Genera el informe Excel en la ruta especificada. Retorna la ruta absoluta del archivo generado.

### Estructura del informe

| Hoja               | Contenido                              |
| ------------------ | -------------------------------------- |
| Resumen            | Datos generales del proyecto.         |
| PK                 | Tabla de puntos kilométricos.         |
| Municipios         | Afección municipal detallada.         |
| Catastro           | Parcelas catastrales afectadas.       |
| Carreteras         | Cruces con carreteras.               |
| Hidrografía        | Cruces con red hidrográfica.         |
| Infraestructuras   | Cruces con infraestructuras.         |

## Dependencias

- `openpyxl` para generación de archivos Excel.
- `linpro.geometry` y todos los módulos GIS para obtener los datos.

## Uso básico

```python
from linpro.gis import Project
from linpro.excel import ExcelReport

project = Project("C:/data/proyecto.linpro")
report = ExcelReport(project)
report.generate("C:/data/informe_proyecto.xlsx")
```