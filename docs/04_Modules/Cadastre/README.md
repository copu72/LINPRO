# Módulo Cadastre — Análisis de afección catastral

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Análisis de afección catastral del proyecto, identificando parcelas afectadas por el trazado y su zona de servidumbre.

## Requisitos funcionales

| ID      | Descripción                |
| ------- | -------------------------- |
| FR-0006 | Analizar Catastro.         |

## API pública

```python
def get_parcels(project: Project) -> list[Parcel]
```
Obtiene la lista de parcelas catastrales afectadas por el proyecto, con información de superficie, propietario y uso del suelo.

### Tipo Parcel

| Atributo         | Tipo    | Descripción                              |
| ---------------- | ------- | ---------------------------------------- |
| `reference`      | `str`   | Referencia catastral.                   |
| `municipality`   | `str`   | Municipio donde se ubica.               |
| `area_affected`  | `float` | Superficie de afección (m²).            |
| `area_total`     | `float` | Superficie total de la parcela (m²).    |
| `owner`          | `str`   | Titular catastral (anonimizado).        |
| `use_type`       | `str`   | Tipo de suelo (urbano, rústico, etc.).  |

## Dependencias

- Fichero catastral (formato Catastro INSPIRE o Shapefile).
- Servicio WFS de la Sede Electrónica del Catastro (opcional).
- `linpro.gis` para carga de capas.

## Uso básico

```python
from linpro.gis import Project
from linpro.gis.cadastre import get_parcels

project = Project("C:/data/proyecto.linpro")
parcelas = get_parcels(project)
for p in parcelas:
    print(f"{p.reference}: {p.area_affected:.2f} m² ({p.use_type})")
```