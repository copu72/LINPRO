# 006 — ARQUITECTURA

**Versión:** 0.0.1  
**Fecha:** 2026-07-09

## Patrón general: Fachada + Mediador

LINPRO se organiza en torno al objeto Project, que actúa como **fachada** y **mediador**. Ningún módulo interno conoce la existencia de otro.

## Diagrama conceptual

`
Proyecto LINPRO
      │
      ├── Configuración
      ├── Eje (Alignment)
      ├── PK
      ├── Buffer
      ├── Municipios
      ├── Catastro
      ├── Carreteras
      ├── Caminos
      ├── Ríos
      ├── Infraestructuras
      ├── Resultados
      ├── Exportaciones
      └── Historial
`

## Flujo de trabajo típico

1. El usuario crea un Project.
2. Define un Alignment (eje) y lo asigna al proyecto.
3. El proyecto calcula PK y buffer automáticamente.
4. El usuario solicita análisis de afecciones.
5. El proyecto orquesta los módulos correspondientes.
6. Los resultados se almacenan en el proyecto.
7. El proyecto exporta (Excel, DWG).

## Módulos principales

| Módulo | Responsabilidad |
|--------|----------------|
| core.Project | Orquestación, estado global, historial |
| geometry.Alignment | Definición y cálculo del eje |
| geometry.PK | Sistema de puntos kilométricos |
| geometry.Buffer | Generación de áreas de influencia |
| municipalities | Análisis de afección municipal |
| cadastre | Análisis de afección catastral |
| oads | Análisis de carreteras |
| ivers | Análisis hidrográfico |
| infrastructure | Análisis de infraestructuras existentes |
| cad | Lectura/escritura DWG/DXF |
| excel | Generación de informes Excel |
| eports | Generación de informes PDF |
| gui | Interfaz gráfica PySide6 |
| gis | Descarga y procesamiento de datos geográficos |
| database | Almacenamiento local de datos |

## Dependencias entre módulos

Ningún módulo de negocio (municipalities, cadastre, etc.) importa directamente a otro. Todos dependen únicamente de core.Project y geometry.
