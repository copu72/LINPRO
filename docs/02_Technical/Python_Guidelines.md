# Python Guidelines

| Versión | Fecha       |
| ------- | ----------- |
| 1.0     | 2026-07-09 |

## Versión

- Se requiere Python 3.11 o superior.
- Se permite usar `StrEnum`, `Self`, `TypeAlias` y demás características del lenguaje posteriores a 3.10.

## Dataclasses

- Usar `@dataclass(frozen=True)` para objetos de datos inmutables.
- Usar `@dataclass` sin `frozen` para objetos mutables con lógica simple.
- Para estructuras más complejas, considerar `TypedDict` o `NamedTuple`.

## Enumeraciones

- Usar `Enum` o `StrEnum` para constantes con nombre.
- No usar variables sueltas tipo `RED = "red"`.
- Ejemplo:
  ```python
  class Color(StrEnum):
      RED = "red"
      GREEN = "green"
  ```

## Interfaces

- Usar `Protocol` para definir interfaces implícitas.
- No crear clases base abstractas (ABC) a menos que se requiera comportamiento compartido.

## Herencia

- Evitar herencia múltiple.
- Preferir composición sobre herencia.
- Usar `Mixins` solo cuando sea estrictamente necesario y estén documentados.

## Rutas

- Usar `pathlib.Path` en toda la base de código.
- Prohibido usar `os.path.join`, `os.path.exists` ni similares.

## Logging

- Usar el módulo `logging` con niveles apropiados (debug, info, warning, error).
- Prohibido usar `print()` para salida del programa.
- Configurar el logger raíz una sola vez en el punto de entrada.

## Errores

- Definir excepciones personalizadas que hereden de `LINPROError` (base propia).
- Usar jerarquía plana: una excepción por módulo o funcionalidad.
- Capturar excepciones externas y re-lanzar como excepciones propias cuando tenga sentido.
