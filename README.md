# Lab Semana 1 - Air Quality (UCI)

- Persona A: LUIS TORRES
- Persona B: PATRICIO HEREDIA
- Dataset: https://archive.ics.uci.edu/static/public/360/data.csv
- Tarea: regresion   Variable objetivo: C6H6(GT)

Lo elegimos porque sus 16.701 faltantes no vienen como NaN sino codificados con
el centinela -200, asi que descubrir como estan codificados es parte del trabajo.

## Como correr

```bash
uv sync
uv run pytest -q
uv run python main.py
```

## Estructura

```
.
├── pyproject.toml   # dependencias del proyecto
├── uv.lock          # versiones exactas, permite reconstruir el entorno
├── src/
│   ├── carga.py     # Persona A: cargar, reporte_nulos, limpiar, guardar
│   └── analisis.py  # Persona B: filtrar, resumen_por_grupo, zscore, top_k, recta_minimos_cuadrados
├── tests/           # pruebas con pytest
├── data/            # datos generados localmente, NO se versionan
└── main.py          # integracion final
```

## Hallazgos

- (A) Los 16.701 faltantes del dataset son invisibles para `isna()`: vienen
  codificados con el centinela -200, asi que una lectura ingenua reporta **0
  nulos** y trata esos -200 como mediciones validas. El efecto es silencioso y
  grave: la media de `C6H6(GT)` cae a 1.87 en vez de 10.08, un factor de 5.4.
  El dato no se pierde, se corrompe, y nada en el CSV avisa de ello.

## Decisiones de limpieza

El dataset crudo tiene 9357 filas x 15 columnas y 16.701 faltantes. Ninguno
llega como NaN: todos vienen con el centinela -200, por eso se leen con
`na_values=[-200]`. Sin eso pandas los toma como mediciones validas y cualquier
promedio sale corrupto.

| Columna | % nulos | Decision | Justificacion |
|---|---|---|---|
| `NMHC(GT)` | 90.23% | Eliminar la **columna** | Imputar el 90% de los valores es inventar el dato. Borrar esas filas dejaria el dataset en 914 de 9357 |
| `C6H6(GT)` (objetivo) | 3.91% | Eliminar esas **filas** (366) | La variable objetivo nunca se imputa: rellenarla seria fabricar la respuesta que el modelo debe aprender |
| `CO(GT)`, `NO2(GT)`, `NOx(GT)` | ~17.5% | Imputar con **mediana** | La mediana no se desplaza con los valores extremos, la media si |
| `PT08.S1` a `PT08.S5`, `T`, `RH`, `AH` | 3.91% | Imputar con **mediana** | Porcentaje bajo, no justifica perder 366 filas de cada una |
| `Date`, `Time` | 0% | `strip()` + `lower()` | Normalizacion de texto |

Duplicados encontrados: 0. Infinitos: 0 (se unifican como NaN antes de tratarlos).

**Resultado:** 9357 x 15 -> 8991 x 14, sin ningun nulo restante.

El umbral para eliminar una columna esta en 80% de nulos. No se usa `dropna()`
sin criterio en ningun momento.

## Preguntas de investigacion

**1. Por que `uv sync` reconstruye el entorno si `.venv/` no esta versionado?**

Lo permite `uv.lock`. Ese archivo guarda el resultado exacto de la resolucion de
dependencias: la version fijada de cada paquete —tanto los que pedimos como sus
dependencias transitivas—, su hash de verificacion y las plataformas para las
que aplica. `.venv/` es solo la materializacion de esa receta, y por eso se
puede regenerar en cualquier maquina. Versionar `.venv/` seria subir cientos de
megas de binarios especificos de un sistema operativo; versionar `uv.lock` son
unos pocos KB que producen un entorno identico en todas partes.

**2. Que diferencia hay entre `pytest` y `uv run pytest`?**

`pytest` a secas ejecuta el primer `pytest` que aparezca en el `PATH`. Si nadie
activo el entorno virtual, eso es el Python del sistema u otro entorno
cualquiera: las pruebas corren con versiones distintas de pandas y numpy a las
del proyecto, o directamente fallan con `command not found`.

`uv run pytest` obliga a usar el entorno del proyecto: antes de ejecutar, uv
verifica que `.venv/` este sincronizado con `uv.lock` —y si falta, lo crea e
instala todo— y recien ahi lanza pytest desde ahi. No hace falta activar nada, y
el resultado es el mismo para los dos integrantes del equipo.
