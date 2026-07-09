# Arquitectura de la Interfaz Gráfica (GUI)

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Estado:** Aprobado

---

## 1. Propósito

La interfaz gráfica de LINPRO está construida con **PySide6** (Qt for Python) siguiendo el patrón **Modelo-Vista-Controlador (MVC)**. Este patrón garantiza la separación total entre la lógica de negocio y la presentación, facilitando el mantenimiento, las pruebas y la evolución independiente de cada componente.

**Regla fundamental:** Las vistas NUNCA importan módulos de negocio directamente. Toda comunicación con el modelo debe realizarse a través del controlador.

---

## 2. Diagrama MVC

```
+-------------------+       +--------------------+       +-------------------+
|      Model        |<----->|    Controller      |<----->|       View        |
| (linpro.core)     |       | (linpro.gui.ctrl)  |       | (linpro.gui.view) |
|                   |       |                    |       |                   |
| - Project         |       | - MainController  |       | - MainWindow      |
| - Alignment       |       | - MapController   |       | - MapView         |
| - Buffer          |       | - AnalysisCtrl    |       | - ResultsPanel    |
| - GIS layers      |       | - ExportCtrl      |       | - PropertyEditor  |
| - Results         |       |                    |       | - Dialogs         |
+-------------------+       +--------------------+       +-------------------+
        ^                          ^                           ^
        |                          |                           |
        |        Eventos / Señales PySide                     |
        +--------------------------+---------------------------+
```

---

## 3. Modelo (`linpro.core`)

El modelo consiste en los módulos de negocio de LINPRO Core y las capas superiores (GIS, CAD, Reports). El controlador es el único responsable de interactuar con estas capas.

El modelo expone:

- **Estado del proyecto** a través de `Project`.
- **Eventos** a través del bus de eventos interno de `Project`.
- **Resultados de análisis** a través de `Project.results`.

El modelo no tiene conocimiento de la existencia de la GUI.

---

## 4. Vista (`linpro.gui.view`)

Componentes visuales basados en PySide6. Ninguno de ellos importa directamente módulos como `Alignment`, `Buffer` o `GISLayer`.

### 4.1 MainWindow

Ventana principal de la aplicación:

```
+--------------------------------------------------------------+
| [Toolbar] [File] [Edit] [View] [Analysis] [Plugins] [Help]   |
+--------------------------------------------------------------+
|                                                               |
|  +----------------------------------+  +-------------------+ |
|  |                                  |  |   ResultsPanel    | |
|  |          MapView                 |  |                   | |
|  |    (Matplotlib / OpenGL)          |  | - Intersecciones | |
|  |                                  |  | - Longitudes     | |
|  |                                  |  | - Áreas          | |
|  |                                  |  | - Errores        | |
|  +----------------------------------+  +-------------------+ |
|                                                               |
+--------------------------------------------------------------+
| [Status Bar]  |  PK: 1+250.00  |  EPSG:25830  |  Zoom: 1:5000 |
+--------------------------------------------------------------+
```

### 4.2 Componentes de Vista

| Componente | Descripción |
|------------|-------------|
| `MainWindow` | Contenedor principal con menús, toolbar y layout. |
| `MapView` | Visor geográfico con soporte Matplotlib y OpenGL. |
| `ResultsPanel` | Panel lateral que muestra resultados de análisis. |
| `PropertyEditor` | Editor de propiedades del proyecto y sus elementos. |
| `StatusBar` | Barra de estado con PK, proyección y escala. |
| `Dialogs` | Cuadros de diálogo (configuración, exportación, ayuda). |

### 4.3 MapView — Visor de Mapa

El `MapView` soporta dos motores de renderizado intercambiables:

- **Matplotlib**: para visualización 2D con soporte de zoom, pan y selección.
- **OpenGL** (PyOpenGL): para visualización acelerada 3D cuando se requiera.

Ambos motores implementan una interfaz común:

```python
class MapRenderer(ABC):
    def render(self, data: MapData) -> None
    def zoom_to(self, extent: BoundingBox) -> None
    def select_at(self, x: int, y: int) -> list[str]
```

---

## 5. Controlador (`linpro.gui.controller`)

El controlador orquesta las interacciones entre el modelo y las vistas.

### 5.1 Controladores

| Controlador | Responsabilidad |
|-------------|-----------------|
| `MainController` | Coordina la aplicación completa. Gestiona el ciclo de vida del proyecto. |
| `MapController` | Gestiona la interacción con el mapa: zoom, selección, capas visibles. |
| `AnalysisController` | Lanza análisis (plugins, buffer, intersecciones) y actualiza resultados. |
| `ExportController` | Gestiona exportaciones a CAD y Excel. |
| `UndoController` | Gestiona las operaciones de deshacer/rehacer. |

### 5.2 Ejemplo de Flujo

```
Usuario hace clic en "Analizar intersecciones"
        |
        v
MainWindow emite señal: analysis_requested("intersections")
        |
        v
AnalysisController.handle_analysis("intersections")
        |
        v
AnalysisController llama a Project.analyze(...)  [MODELO]
        |
        v
Project devuelve AnalysisResult
        |
        v
AnalysisController procesa el resultado y emite:
  - results_updated(analysis_result)   [señal hacia ResultsPanel]
  - map_overlay_added(layer_data)      [señal hacia MapView]
        |
        v
ResultsPanel y MapView se actualizan automáticamente
```

---

## 6. Comunicación Vista-Controlador

La comunicación se realiza mediante **señales y slots de Qt**:

- Las vistas emiten señales cuando el usuario interactúa (clic, cambio de valor, etc.).
- Los controladores escuchan esas señales y actúan sobre el modelo.
- Cuando el modelo cambia, los controladores emiten señales que actualizan las vistas.

```python
# Ejemplo: Vista emite señal
class MapView(QWidget):
    zoom_changed = Signal(float)
    selection_changed = Signal(list)

# Ejemplo: Controlador conecta la señal
class MapController:
    def __init__(self, view: MapView, model: Project):
        view.zoom_changed.connect(self.on_zoom_changed)

    def on_zoom_changed(self, scale: float):
        # Actualiza el modelo o la vista según corresponda
        self.view.update_scale_display(scale)
```

---

## 7. Dependencias Externas

| Librería | Uso |
|----------|-----|
| `PySide6` | Framework Qt para la interfaz gráfica. |
| `matplotlib` | Renderizado 2D del mapa. |
| `PyOpenGL` | Renderizado 3D del mapa (opcional). |
| `numpy` | Operaciones numéricas para visualización. |

---

## 8. Buenas Prácticas

- Las vistas solo contienen lógica de presentación (layout, estilos, colores, traducciones).
- Los controladores no deben contener lógica de negocio; solo orquestación.
- El modelo no debe importar nada de `linpro.gui`.
- Los nombres de señales deben seguir la convención `{sujeto}_{acción}` (ej: `zoom_changed`, `file_loaded`).
- Los controladores se inyectan en las vistas mediante el constructor (dependency injection).

---

## 9. Histórico de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | 2026-07-09 | Documento inicial de arquitectura de la GUI |
