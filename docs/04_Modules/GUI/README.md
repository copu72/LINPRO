# Módulo GUI — Interfaz gráfica PySide6

**Versión:** 1.0  
**Fecha:** 2026-07-09  
**Propósito:** Interfaz de usuario gráfica basada en PySide6 para la carga, visualización y análisis de proyectos lineales.

## API pública

```python
class MainWindow(QMainWindow):
    def __init__(self, project: Project | None = None)
```

**Métodos:**

```python
def show(self) -> None
```
Muestra la ventana principal de la aplicación.

### Componentes principales

| Componente       | Descripción                                    |
| ---------------- | ---------------------------------------------- |
| Mapa             | Visor cartográfico basado en QGraphicsView.   |
| Panel de capas   | Control de visibilidad de capas SIG.          |
| Barra de herramientas | Acciones rápidas (abrir, exportar, zoom). |
| Panel de resultados | Tabla de resultados del análisis.          |
| Barra de estado  | Información de PK, coordenadas y progreso.    |

## Dependencias

- `PySide6` para la interfaz gráfica.
- `matplotlib` / `cartopy` para visualización cartográfica opcional.
- `linpro` como motor de análisis.

## Uso básico

```python
import sys
from linpro.gis import Project
from linpro.gui import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
project = Project("C:/data/proyecto.linpro")
window = MainWindow(project)
window.show()
sys.exit(app.exec())
```