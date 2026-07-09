# 000 — PROYECTO LINPRO

**Título:** LINPRO — Ingeniería Lineal Profesional  
**Versión:** 0.0.1  
**Fecha:** 2026-07-09  
**Estado:** En definición  
**Autor:** LINPRO Team

## 1. Propósito

LINPRO es una librería Python para el análisis, diseño y gestión de **infraestructuras lineales**: líneas eléctricas (MT, AT, 132kV, 220kV, 400kV), carreteras, gasoductos, tuberías, canales y cualquier obra cuya geometría se defina mediante un eje (alignment).

## 2. Alcance

- Cálculo geométrico de ejes con curvas circulares y clotoides.
- Sistema de Puntos Kilométricos (PK).
- Análisis de afecciones: catastro, municipios, carreteras, ríos, infraestructuras.
- Generación de planos (DWG/DXF).
- Generación de informes (Excel, PDF).
- Interfaz gráfica (PySide6).
- Descarga automática de datos oficiales (catastro, IGN, MITMA, etc.).

## 3. No alcance

- No es un CAD. No dibuja directamente.
- No es un SIG completo. No edita geometrías arbitrarias.
- No es un ERP. No gestiona proyectos más allá del ámbito técnico.

## 4. Principios rectores

1. **Una carpeta = una responsabilidad.** Cada módulo tiene una responsabilidad única y claramente delimitada.
2. **Objeto central Project.** Todas las operaciones giran alrededor de un único objeto Project que orquesta los módulos. Ningún módulo se comunica directamente con otro.
3. **Documentación primero.** Toda decisión técnica se registra en docs/adr/. Toda especificación se redacta en docs/specifications/ **antes** de escribir código.
4. **Pruebas en tres niveles:** unitarias, integración, regresión.
5. **Código tipado.** Uso estricto de type hints en Python.
6. **Sin dependencia de QGIS, AutoCAD ni software propietario.** LINPRO debe poder ejecutarse en cualquier máquina con Python.
