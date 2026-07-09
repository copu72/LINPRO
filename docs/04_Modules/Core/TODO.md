# TODO — Core de LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09

---

## Pendientes para v1.1

### Tests de integración

- [ ] **Ciclo completo `app.start()` → `app.stop()`**
  - Verificar que todos los eventos `CORE_STARTING`, `CORE_STARTED`, `CORE_STOPPING`, `CORE_STOPPED` se emiten en el orden correcto.
  - Verificar que los 6 singletons están inicializados tras `start()`.
  - Verificar que `stop()` descarga todos los plugins y libera recursos.

- [ ] **Descubrimiento real de plugins**
  - Crear un directorio temporal con plugins mock que implementen `BasePlugin`.
  - Ejecutar `PluginManager.discover()` y verificar que los plugins se cargan correctamente.
  - Verificar que `PluginManager.run_all()` ejecuta todos los plugins sobre un proyecto.
  - Probar descarga con `unload()` y verificar limpieza.

- [ ] **Carga real de archivos YAML**
  - Escribir un archivo YAML de configuración en un directorio temporal.
  - Cargarlo con `Configuration.load_file()` y verificar fusión correcta con defaults.
  - Probar `Configuration.save()` y recarga para verificar consistencia.
  - Probar YAML con caracteres Unicode y UTF-8.

- [ ] **Persistencia de proyectos**
  - Serializar un `Project` completo con `to_dict()`.
  - Escribir a archivo JSON/YAML.
  - Recuperar con `from_dict()` y verificar que todos los campos se restauran.
  - Probar el flag `is_dirty` durante el ciclo guardar/cargar/modificar.

### Mejoras planificadas

- [ ] Añadir validación de esquema para Configuration (JSON Schema o similar).
- [ ] Implementar notificaciones de cambios (`CONFIG_CHANGED`) desde `Configuration.set()`.
- [ ] Separar `Project.serialize()` del actual `to_dict()` con formato de archivo versionado.
- [ ] Añadir logging de rendimiento (tiempo de inicio, carga de plugins, etc.).
- [ ] Soporte para plugins con dependencias entre sí (orden de carga).
- [ ] Hilos o procesos separados para ejecución de plugins (opcional).
- [ ] Gestión de proyectos múltiples simultáneos en `Workspace`.
- [ ] Documentación adicional: guía de creación de plugins.

### Bugs conocidos

- Ninguno reportado hasta la fecha.

---

## Historial de versiones

| Versión | Fecha       | Cambios |
|---------|-------------|---------|
| 1.0     | 2026-07-09 | Versión inicial del Core — funcionalidad base completa, 109 tests unitarios. |
