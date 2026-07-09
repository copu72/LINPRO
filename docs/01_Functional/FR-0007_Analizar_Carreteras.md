# FR-0007: Analizar Carreteras

| Campo           | Valor                   |
| --------------- | ----------------------- |
| **ID**          | FR-0007                 |
| **Versión**     | 1.0                     |
| **Fecha**       | 2026-07-09              |
| **Prioridad**   | Alta                    |
| **Módulo**      | Roads                   |
| **Dependencias**| FR-0003                 |

## Descripción

Identificar todas las carreteras que intersectan el buffer, ya sea cruzando el _alignment_ o discurriendo dentro del área de influencia. Para cada intersección se deben calcular los parámetros geométricos del cruce.

## Criterios de Aceptación

1. **Nombre de la carretera** – Identificador/nombre oficial de la vía (ej. A-2, N-340, CM-101).
2. **Tipo de vía** – Clasificación según la red: autopista, autovía, carretera nacional, carretera autonómica, carretera provincial, camino municipal.
3. **PK de cruce** – Punto kilométrico del _alignment_ en el que se produce la intersección.
4. **Distancia perpendicular** – Distancia mínima entre el _alignment_ y la carretera en el punto de cruce (para el caso de pasos superiores o inferiores).
5. **Ángulo de cruce** – Ángulo formado entre el _alignment_ y la carretera en el punto de intersección (en grados sexagesimales).
6. **Longitud dentro del buffer** – Longitud de la carretera que discurre dentro del buffer (para vías paralelas o concurrentes).
7. **Jerarquía** – Las carreteras deben ordenarse por tipo y mostrar su dependencia administrativa (estatal, autonómica, provincial).

## Observaciones

- La fuente de datos de carreteras debe ser oficial (Mapa de Carreteras del Ministerio de Transportes o equivalente autonómico).
- Para intersecciones a distinto nivel (desmontes, viaductos), debe indicarse la diferencia de cota si el dato está disponible.
