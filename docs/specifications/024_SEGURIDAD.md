# 024 — SEGURIDAD

**Versión:** 0.0.1
**Fecha:** 2026-07-09

## Principios

1. No se almacenan credenciales en el repositorio.
2. No se ejecutan scripts descargados automáticamente.
3. Las descargas de datos oficiales se realizan mediante APIs oficiales (WFS, REST).
4. Los archivos generados (Excel, DXF, PDF) no contienen macros ni código ejecutable.
5. Las rutas de archivos se sanitizan para evitar path traversal.
6. El instalador firmado digitalmente (cuando corresponda).