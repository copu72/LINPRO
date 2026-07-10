# Performance Guidelines

## Principios

1. **Corrección primero.** Una función rápida pero incorrecta no sirve.
2. **Benchmarks desde el sprint 1.** Medir antes de optimizar.
3. **Perfilado obligatorio** antes de cualquier optimización significativa.
4. **Caching controlado** en Polyline (longitud, segmentos). Las entidades inmutables hacen seguro el caching.

## Operaciones críticas

| Operación | Frecuencia | Optimización esperada |
|---|---|---|
| `distance_to` | Muy alta | O(1), sin allocaciones innecesarias |
| `point_at_pk` | Alta | Búsqueda binaria O(log n) |
| `simplify` | Media | RDP O(n log n) |
| `offset` | Media | O(n) con generación de vértices |
| `buffer` | Media | O(n) |
| `intersections` | Baja | O(n × m) con early exit |

## Lo que no se hace

- ❌ Usar NumPy para acelerar operaciones simples (añade dependencia).
- ❌ Usar Cython/C extensions (a no ser que sea estrictamente necesario).
- ❌ Optimización prematura (perfilar primero).

## Benchmarks

Los benchmarks se almacenan en `benchmarks/` y se ejecutan con:

```bash
python scripts/quality/run_benchmarks.py
```

Cada benchmark mide: tiempo de ejecución, uso de memoria (tracemalloc), y escalabilidad con tamaño de entrada.
