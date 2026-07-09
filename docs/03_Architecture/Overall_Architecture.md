# Arquitectura General de LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Estado:** Aprobado

---

## 1. Introducción

LINPRO es una plataforma de ingeniería lineal y territorial estructurada en cinco capas independientes. Cada capa encapsula un dominio específico y se comunica con las demás exclusivamente a través de la capa **LINPRO Core**, lo que garantiza baja cohesión y alta capacidad de mantenimiento.

---

## 2. Diagrama Conceptual de Capas

```
+----------------------------------------------------------+
|                   LINPRO Reports/Excel                    |
|            Informes técnicos, tablas, exportación         |
+----------------------------------------------------------+
|                    LINPRO GUI (PySide6)                   |
|          MainWindow, MapView, ResultsPanel, Dialogs       |
+----------------------------------------------------------+
|                     LINPRO CAD (DXF/DWG)                  |
|         Capas CAD, estilos de línea, entidades gráficas  |
+----------------------------------------------------------+
|                      LINPRO GIS                           |
|     WFS, shapefiles, proyecciones, capas geográficas      |
+----------------------------------------------------------+
|                    LINPRO Core (Base)                     |
|   Project, Config, Logging, Exceptions, Version           |
+----------------------------------------------------------+
```

**Principio fundamental:** Cada capa solo depende de **LINPRO Core**. Ninguna capa superior depende directamente de otra capa superior o de una capa del mismo nivel.

---

## 3. Descripción de Capas

### 3.1 LINPRO Core

Es la dependencia base de todo el ecosistema. Contiene las abstracciones fundamentales:

- **Project**: fachada principal que orquesta todos los módulos.
- **Config**: configuración global del proyecto y del usuario.
- **Logging**: sistema de registro de eventos con niveles configurables.
- **Exceptions**: jerarquía de excepciones específicas del dominio.
- **Version**: control de versionado del proyecto y del formato de archivo.

*Dependencias externas:* ninguna (solo biblioteca estándar de Python y paquetes utilitarios mínimos como `pyyaml`).

### 3.2 LINPRO GIS

Gestiona toda la información geográfica y espacial:

- Descarga y transformación de datos WFS (Web Feature Service).
- Lectura/escritura de shapefiles y GeoJSON.
- Manejo de proyecciones (UTM, geodesicas) mediante `pyproj`.
- Generación de capas temáticas (municipios, parcelas, carreteras, ríos, infraestructura).
- Caché local de datos descargados con expiración configurable.

*Dependencias:* LINPRO Core, `geopandas`, `shapely`, `pyproj`, `requests`.

### 3.3 LINPRO CAD

Proporciona capacidades de exportación a formatos CAD:

- Exportación a DXF y DWG con `ezdxf`.
- Definición de capas CAD con nombres normalizados.
- Estilos de línea, colores y grosores según normativa local.
- Generación de entidades (líneas, polilíneas, textos, cotas, bloques).
- Transformación de coordenadas geográficas a coordenadas CAD.

*Dependencias:* LINPRO Core, `ezdxf`.

### 3.4 LINPRO GUI

Interfaz gráfica de usuario basada en PySide6 (Qt for Python):

- Arquitectura MVC estricta: las vistas nunca importan módulos de negocio directamente.
- Componentes principales: MainWindow, MapView, ResultsPanel.
- Soporte para visualización Matplotlib y OpenGL en el visor de mapa.
- Sistema de acciones deshacer/rehacer con retroalimentación visual.

*Dependencias:* LINPRO Core, `PySide6`, `matplotlib`, `PyOpenGL`.

### 3.5 LINPRO Reports / Excel

Generación de informes técnicos y exportación de datos:

- Reportes en formato Excel (`.xlsx`) con `openpyxl`.
- Plantillas de informes técnicos predefinidas.
- Tablas de resultados de análisis (PK, áreas, longitudes, intersecciones).
- Integración directa con `Project` para obtener datos sin acoplamiento.

*Dependencias:* LINPRO Core, `openpyxl`.

---

## 4. Principios Arquitectónicos

| Principio | Descripción |
|-----------|-------------|
| Dependencia unidireccional | Todas las capas apuntan a Core. No hay dependencias entre capas del mismo nivel. |
| Fachada (Facade) | `Project` expone una API unificada que oculta la complejidad interna. |
| Inversión de control (IoC) | Los plugins se registran en Core y son orquestados por `Project`. |
| Persistencia mínima | No hay base de datos relacional; se usan archivos `.linpro` (JSON/YAML). |
| Testeabilidad | Cada capa y submódulo es independiente y se puede probar de forma aislada. |

---

## 5. Flujo de Datos Típico

```
Usuario (GUI)
    |
    v
Controller (GUI)
    |
    v
Project (Core)
    |
    +--> GIS: carga datos geográficos
    +--> Geometry: cálculos de alineación, buffer, intersecciones
    +--> CAD: exporta resultados a DXF
    +--> Reports: genera informe Excel
    |
    v
Resultados almacenados en Project.results
    |
    v
Vistas actualizadas vía eventos
```

---

## 6. Histórico de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | 2026-07-09 | Documento inicial de arquitectura general |
