# LINPRO Philosophy

**Proyecto:** LINPRO — Linear Infrastructure Processor
**Versión:** 1.0.0
**Fecha:** 2026-07-09

---

## ¿Por qué existe LINPRO?

LINPRO existe porque el análisis de infraestructuras lineales (líneas eléctricas, gasoductos, carreteras, ferrocarriles, canales) sigue haciéndose con herramientas de propósito general: AutoCAD, Excel, QGIS. Cada proyecto requiere semanas de trabajo manual, copiar datos entre programas, y revisar decenas de planos para extraer información que debería estar a un clic.

LINPRO automatiza ese proceso. Un ingeniero carga un eje en DXF y obtiene, en minutos: parcelas afectadas, cruces con carreteras y ríos, municipios atravesados, informes y planos listos para la tramitación.

## ¿Qué problemas resuelve?

- **Cruce con catastro**: dada una polilínea, obtener todas las parcelas que intersecta, con superficies, titulares y referencias catastrales.
- **Cruce con municipios**: determinar qué municipios atraviesa una infraestructura y en qué porcentaje.
- **Cruce con carreteras y ríos**: detectar y clasificar todas las intersecciones con la red viaria e hidrográfica.
- **Cálculo de PK**: estacionar correctamente un eje, con precisión de centímetros en cientos de kilómetros.
- **Buffer y offset**: generar envolventes, zonas de servidumbre, y ejes desplazados.
- **Informes automáticos**: generar documentación técnica en Excel y PDF con todos los resultados del análisis.
- **Exportación CAD**: producir planos acotados y señalizados directamente desde los datos analizados.

## ¿Qué no pretende resolver?

LINPRO **no** es:
- Un sistema CAD. No dibuja planos desde cero, no edita geometría, no sustituye a AutoCAD o QGIS.
- Un sistema GIS. No gestiona capas, no edita shapefiles, no publica servicios WMS.
- Un sistema de gestión catastral. No almacena expedientes, no gestiona pagos, no interactúa con la Sede Electrónica del Catastro.
- Un ERP. No factura, no gestiona clientes, no tiene contabilidad.
- Una librería de geometría generalista. El Geometry Engine es matemático, pero LINPRO como aplicación está orientado a infraestructuras lineales.

## ¿Qué significa calidad para LINPRO?

Calidad en LINPRO significa:

1. **El código es correcto o no existe.** No hay "ya lo arreglaremos después". Cada clase se especifica, se diseña, se implementa, se prueba y se revisa antes de integrarse.
2. **Las pruebas no son opcionales.** Cobertura ≥ 95 % en el Geometry Engine. Sin tests, la funcionalidad no existe.
3. **La documentación está sincronizada con el código.** Si la documentación y el código discrepan, el error está en el código.
4. **El rendimiento se mide, no se supone.** Benchmarks desde el primer sprint.
5. **La arquitectura es explícita.** Cada decisión de diseño está documentada en un ADR (Architecture Decision Record).
6. **No hay deuda técnica consciente.** Preferimos diez clases impecables a cincuenta mediocres.

## ¿Por qué no dependemos del CAD?

El CAD (AutoCAD, BricsCAD, ZWCAD) es una herramienta de dibujo, no de análisis. LINPRO no depende de ninguna aplicación CAD porque:

- Queremos funcionar sin licencias de AutoCAD.
- Queremos ejecutarnos en servidores, en pipelines CI/CD, y en entornos sin interfaz gráfica.
- Queremos que los algoritmos geométricos sean independientes del formato de archivo.
- Queremos poder publicar el Geometry Engine como librería PyPI independiente.

Los adaptadores CAD (lectura/escritura de DXF, DWG) son plugins intercambiables, no parte del núcleo.

## ¿Por qué el Geometry Engine es independiente?

El Geometry Engine (Kernel Matemático) no conoce nada de catastro, municipios, carreteras, Excel o AutoCAD. Es un motor matemático puro, publicable como `pip install linpro-geometry`. Las razones:

- **Separación de responsabilidades**: la geometría es geometría, el negocio es negocio.
- **Testabilidad**: el kernel se prueba con operaciones matemáticas, no con datos de catastro.
- **Reutilización**: cualquier ingeniero puede usar `linpro-geometry` en sus propios proyectos, aunque nunca use LINPRO.
- **Evolución**: el kernel puede mejorar independientemente de los módulos de negocio.
- **Publicación**: el kernel puede tener su propio ciclo de versiones, su propia documentación y su propia comunidad.

## ¿Por qué los tests son obligatorios?

Porque en ingeniería, los errores cuestan dinero. Un error en el cálculo de PK puede significar una expropiación mal calculada. Un error en la intersección con catastro puede dejar una parcela fuera del informe. Un error en el buffer puede hacer que una carretera parezca dentro de una zona de protección cuando no lo está.

LINPRO se usa para tomar decisiones reales sobre infraestructuras reales. Cada función debe estar probada porque cada función tiene consecuencias.

## ¿Por qué documentamos antes de programar?

La documentación es el diseño. Si no puedes explicar qué hace una clase, cómo se usa y qué garantiza, no sabes lo suficiente para programarla.

El proceso es:

1. SPEC — ¿qué debe hacer?
2. DESIGN — ¿cómo lo hace?
3. CODE — la implementación.
4. TEST — ¿funciona?
5. REVIEW — ¿está bien hecha?
6. RELEASE — ya está lista.

Programar sin especificación es construir sin planos. En proyectos pequeños funciona. En LINPRO, con decenas de clases y módulos que se interrelacionan, es una receta para el desastre.

## ¿Qué esperamos de cada desarrollador?

- Que lea `GEOMETRY_KERNEL_SPEC.md` antes de escribir una línea de geometría.
- Que use las plantillas de `templates/` para cada nueva clase.
- Que siga `Coding_Standards.md` en cada commit.
- Que ejecute `scripts/quality/` antes de cada push.
- Que documente sus decisiones en ADRs.
- Que no acepte deuda técnica.
- Que pregunte antes de improvisar.

## El manifiesto en una frase

> LINPRO no es un programa que funciona. Es un programa que está bien construido y que seguirá funcionando dentro de diez años.

---

*Este documento es la identidad de LINPRO. No es técnico. Es filosófico. Cualquier decisión de desarrollo debe ser coherente con lo que aquí se dice.*
