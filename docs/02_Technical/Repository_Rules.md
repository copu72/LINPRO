# Repository Rules

| Versión | Fecha       |
| ------- | ----------- |
| 1.0     | 2026-07-09 |

## Regla 1: Nada se programa sin FR y UC especificados

No se escribe código sin un Functional Requirement (FR) y un Use Case (UC) aprobados. Cada tarea debe vincularse a un FR y UC en la documentación.

## Regla 2: Ningún archivo Python sin especificación

Todo archivo `.py` debe corresponder a una especificación documentada. No se permiten scripts exploratorios ni archivos huérfanos en la base de código principal.

## Regla 3: Cada carpeta una responsabilidad

Cada directorio debe tener una única responsabilidad bien definida. Si una carpeta acumula múltiples propósitos, debe dividirse.

## Regla 4: No subir datos oficiales al repo

Los archivos de datos oficiales (cartografía, shapefiles, DWG, PDFs, etc.) no se suben al repositorio. Usar `.gitignore` para excluirlos. Solo se permiten datos de prueba pequeños y anonimizados.

## Regla 5: Commits en inglés, descriptivos

Los mensajes de commit deben ser en inglés, en formato imperativo. Describir el qué y el por qué. Ejemplo: `Add parcel validation before export` en lugar de `fix`.

## Regla 6: Pull requests a develop, no directo a master

Toda rama de característica (feature) debe fusionarse mediante pull request a `develop`. La rama `master` solo recibe merges desde `develop` tras revisión y aprobación.

## Regla 7: Tests obligatorios en CI

Todo PR debe pasar la suite de tests en CI antes de ser fusionado. No se permite merge si algún test falla o la cobertura disminuye.

## Regla 8: Toda decisión importante requiere ADR

Las decisiones arquitectónicas significativas deben documentarse mediante un Architecture Decision Record (ADR) en `docs/adr/`. Incluir contexto, opciones consideradas, decisión tomada y consecuencias.
