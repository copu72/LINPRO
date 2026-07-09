# Referencia de API — LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09  

Resumen de la API pública completa de LINPRO. Este documento describe únicamente las clases y métodos públicos. Para más detalle, consulte la documentación de cada módulo.

---

## Paquete `linpro`

### `linpro.Project`

Clase principal que representa un proyecto lineal.

```python
class Project:
    def __init__(self, path: str)
    def load(self) -> None
    def save(self) -> None
    def close(self) -> None
```

**Propiedades:**

| Propiedad      | Tipo    | Descripción                          |
| -------------- | ------- | ------------------------------------ |
| `path`         | `str`   | Ruta del archivo de proyecto.       |
| `name`         | `str`   | Nombre del proyecto.                |
| `alignment`    | `LineString` | Eje de referencia.          |
| `crs`          | `str`   | Sistema de referencia de coordenadas.|
| `metadata`     | `dict`  | Metadatos del proyecto.              |

---

### `linpro.geometry`

```python
# Módulo PK
def calc_pk(x: float, y: float) -> float
def calc_coords(pk: float) -> tuple[float, float]
def format_pk(pk: float) -> str

# Módulo Buffer
class Buffer:
    def __init__(self, alignment: LineString, left: float, right: float)
    def generate(self) -> Polygon
```

---

### `linpro.gis`

#### Proyecto GIS

```python
class GISProject(Project):
    def load_layers(self) -> None
    def get_layer(self, name: str) -> Layer
```

#### Municipalities

```python
def get_municipalities(project: Project) -> list[Municipality]
```

**`Municipality`:** `code`, `name`, `province`, `area_affected`, `length_affected`

#### Cadastre

```python
def get_parcels(project: Project) -> list[Parcel]
```

**`Parcel`:** `reference`, `municipality`, `area_affected`, `area_total`, `owner`, `use_type`

#### Roads

```python
def get_road_crossings(project: Project) -> list[RoadCrossing]
```

**`RoadCrossing`:** `road_id`, `road_name`, `crossing_pk`, `crossing_point`, `angle`, `road_category`

#### Hydrology

```python
def get_river_crossings(project: Project) -> list[RiverCrossing]
```

**`RiverCrossing`:** `water_name`, `water_type`, `crossing_pk`, `crossing_point`, `flow_regime`, `width`

#### Infrastructure

```python
def get_infrastructure_crossings(project: Project) -> list[InfraCrossing]
```

**`InfraCrossing`:** `infra_type`, `infra_id`, `infra_operator`, `crossing_pk`, `crossing_point`, `notes`

---

### `linpro.cad`

```python
class DXFExport:
    def __init__(self, project: Project)
    def generate(self, path: str) -> str
```

---

### `linpro.excel`

```python
class ExcelReport:
    def __init__(self, project: Project)
    def generate(self, path: str) -> str
```

---

### `linpro.reports`

```python
class PDFReport:
    def __init__(self, project: Project)
    def generate(self, path: str, template: str = "default") -> str
```

---

### `linpro.gui`

```python
class MainWindow(QMainWindow):
    def __init__(self, project: Project | None = None)
    def show(self) -> None
```