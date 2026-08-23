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
(B) Al analizar los registros con los valores más altos de C6H6(GT), se observó que las mediciones de contaminación presentan una distribución desigual, con un grupo reducido de observaciones significativamente por encima del promedio.

## Decisiones de limpieza

### Pregunta de investigación 1 

 
¿Por qué uv sync puede reconstruir el entorno aunque .venv/ no esté versionado en el repositorio?

(B)El archivo `uv.lock` está versionado en el repositorio, por lo que todos los colaboradores lo reciben al clonar el proyecto. `uv sync` utiliza la información almacenada en ese archivo para reconstruir el entorno virtual con las mismas versiones de dependencias.

### Pregunta de investigación 2
¿qué diferencia hay entre correr pytest a secas y uv run pytest? 
(B)Copilot said:

La diferencia entre pytest y uv run pytest es que pytest ejecuta las pruebas con el intérprete de Python que esté activo en la terminal, que podría ser el Python global si no se ha activado el entorno virtual, mientras que uv run pytest garantiza que las pruebas se ejecuten usando la versión de Python y las dependencias definidas para el proyecto mediante uv; por ello, si alguien no activó el entorno virtual, pytest podría usar un entorno incorrecto y provocar errores o resultados inconsistentes, mientras que uv run pytest evita ese problema al utilizar automáticamente el entorno adecuado del proyecto.


