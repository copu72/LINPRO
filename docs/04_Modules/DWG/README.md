# Módulo DWG — Exportación a DXF/DWG

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Exportación del trazado, buffer y elementos del proyecto a formatos DXF y DWG para su integración con software CAD.

## Requisitos funcionales

| ID      | Descripción                |
| ------- | -------------------------- |
| FR-0010 | Exportar DXF.              |

## API pública

```python
class DXFExport:
    def __init__(self, project: Project)
```

**Métodos:**

```python
def generate(self, path: str) -> str
```
Exporta el proyecto a formato DXF en la ruta especificada. Retorna la ruta absoluta del archivo generado.

### Capas exportadas

| Capa CAD            | Contenido                            |
| ------------------- | ------------------------------------ |
| `EJE`               | Eje del trazado.                    |
| `PK`                | Puntos kilométricos y etiquetas.    |
| `BUFFER`            | Buffer de afección.                 |
| `MUNICIPIOS`        | Límites municipales afectados.      |
| `PARCELAS`          | Parcelas catastrales afectadas.     |
| `CARRETERAS`        | Cruces con carreteras.             |
| `HIDROGRAFIA`       | Cruces con red hidrográfica.        |
| `INFRAESTRUCTURAS`  | Cruces con infraestructuras.        |

## Dependencias

- `ezdxf` para generación de archivos DXF.
- Para DWG se requiere conversión adicional o uso de librería comercial.

## Uso básico

```python
from linpro.gis import Project
from linpro.cad import DXFExport

project = Project("C:/data/proyecto.linpro")
dxf = DXFExport(project)
dxf.generate("C:/data/exportacion_proyecto.dxf")
```