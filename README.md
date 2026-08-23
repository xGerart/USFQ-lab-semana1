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

## Decisiones de limpieza

### Pregunta de investigación 1

 
¿Por qué uv sync puede reconstruir el entorno aunque .venv/ no esté versionado en el repositorio?

El archivo `uv.lock` está versionado en el repositorio, por lo que todos los colaboradores lo reciben al clonar el proyecto. `uv sync` utiliza la información almacenada en ese archivo para reconstruir el entorno virtual con las mismas versiones de dependencias.
