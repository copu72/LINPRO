# Arquitectura de Base de Datos

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Estado:** Aprobado

---

## 1. Propósito

LINPRO no utiliza una base de datos relacional compleja como PostgreSQL, MySQL o SQL Server. Su modelo de persistencia se basa en archivos planos y caché local, priorizando la portabilidad, la simplicidad y la ausencia de dependencias externas de infraestructura.

---

## 2. Estrategia de Persistencia

| Tipo de Dato | Formato | Ubicación |
|-------------|---------|-----------|
| Proyecto completo | `.linpro` (JSON/YAML) | Ruta definida por el usuario |
| Geometrías pesadas | Shapefile / GeoJSON externos | Referenciados desde el `.linpro` |
| Configuración de usuario | `config.yaml` | `~/.linpro/config.yaml` |
| Caché de descargas | SQLite / archivos locales | `~/.linpro/cache/` |

---

## 3. Archivo de Proyecto (`.linpro`)

Formato principal de intercambio y almacenamiento de proyectos. Es un archivo JSON estructurado que contiene:

- Metadatos del proyecto (nombre, autor, fecha, versión).
- Configuración del proyecto (CRS, unidades, parámetros de análisis).
- Definición de la alineación (segmentos, PKs).
- Configuración de buffer y zonas de amortiguamiento.
- Resultados de análisis (almacenados como datos serializables).
- Lista de plugins habilitados.
- Referencias a archivos externos de geometría.

```json
{
  "version": "1.0",
  "metadata": { "name": "Proyecto Ejemplo", "author": "...", "created": "2026-07-09" },
  "settings": { "crs": "EPSG:25830", "units": "m" },
  "alignment": { "segments": [...] },
  "buffer": { "distance": 50.0, "side": "both" },
  "results": [...],
  "references": {
    "parcels": "./data/parcelas.shp",
    "roads": "./data/carreteras.geojson"
  }
}
```

---

## 4. Caché Local

### 4.1 Propósito

Almacenar temporalmente datos descargados desde servicios WFS u orígenes remotos para evitar descargas repetitivas y permitir el trabajo sin conexión.

### 4.2 Implementación

- **Motor:** SQLite (`sqlite3` módulo estándar de Python) o archivos serializados.
- **Ubicación:** `~/.linpro/cache/`
- **Estructura:**

```
~/.linpro/cache/
├── wfs/
│   ├── catastro_20260709.gpkg
│   └── ign_20260708.gpkg
├── tiles/
│   └── ... (teselas de mapa si aplica)
└── index.db   (SQLite con metadatos de caché)
```

### 4.3 Expiración

Cada entrada de caché tiene un tiempo de vida configurable:

| Origen | TTL por Defecto | Configurable |
|--------|-----------------|--------------|
| WFS Catastro | 7 días | Sí |
| WFS IGN | 30 días | Sí |
| Teselas de mapa | 90 días | Sí |

La tabla `index.db` contiene:

```sql
CREATE TABLE cache_entries (
    key TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    size_bytes INTEGER NOT NULL
);
```

### 4.4 Gestión de Caché

```python
class CacheManager:
    def __init__(self, cache_dir: Path, default_ttl: timedelta = timedelta(days=7))
    def get(self, key: str) -> Optional[Path]
    def set(self, key: str, data: Any, ttl: Optional[timedelta] = None) -> Path
    def invalidate(self, key: str) -> None
    def clear_expired(self) -> int
    def clear_all(self) -> None
```

---

## 5. Configuración de Usuario

Almacenada en `~/.linpro/config.yaml` con valores predeterminados:

```yaml
project:
  default_crs: EPSG:25830
  default_units: m

cache:
  enabled: true
  dir: ~/.linpro/cache
  default_ttl_days: 7

wfs:
  timeout_seconds: 30
  max_retries: 3

ui:
  language: es
  theme: system
```

---

## 6. Ausencia de Dependencias de Bases de Datos Relacionales

| Tecnología | ¿Se usa? | Motivo |
|------------|----------|--------|
| PostgreSQL | No | Complejidad innecesaria para proyectos monousuario. |
| MySQL | No | Misma razón; LINPRO no requiere concurrencia multiusuario. |
| SQL Server | No | Dependencia de plataforma Windows. |
| SQLite | Sí (caché) | Biblioteca estándar de Python, sin instalación adicional. |
| JSON/YAML | Sí | Formato universal, legible, versionable con git. |

---

## 7. Histórico de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | 2026-07-09 | Documento inicial de arquitectura de base de datos |
