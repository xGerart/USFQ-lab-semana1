from pathlib import Path

import numpy as np
import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/360/data.csv"
CENTINELAS = [-200]
OBJETIVO = "C6H6(GT)"

RAIZ = Path(__file__).resolve().parent.parent
RUTA_SALIDA = RAIZ / "data" / "limpio.parquet"

UMBRAL_COLUMNA = 80.0


def cargar(url, na_values=None):
    return pd.read_csv(url, na_values=na_values)


def reporte_nulos(df):
    nulos = df.isna().sum()
    reporte = pd.DataFrame(
        {
            "nulos": nulos,
            "porcentaje": (nulos / len(df) * 100).round(2),
        }
    )
    return reporte.sort_values("nulos", ascending=False)


def limpiar(df, umbral_columna=UMBRAL_COLUMNA, objetivo=OBJETIVO):
    df = df.copy()

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.drop_duplicates()

    columnas_texto = df.select_dtypes(include=["object", "string"]).columns
    for col in columnas_texto:
        df[col] = df[col].str.strip().str.lower()


    porcentaje = df.isna().sum() / len(df) * 100
    columnas_a_eliminar = porcentaje[porcentaje > umbral_columna].index
    df = df.drop(columns=columnas_a_eliminar)

    if objetivo is not None and objetivo in df.columns:
        df = df.dropna(subset=[objetivo])

    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    for col in columnas_numericas:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    return df.reset_index(drop=True)


def guardar(df, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta, index=False)
    return ruta


if __name__ == "__main__":
    crudo = cargar(URL, na_values=CENTINELAS)
    print(f"Dataset crudo: {crudo.shape[0]} filas x {crudo.shape[1]} columnas\n")

    print("Reporte de nulos ANTES de limpiar:")
    print(reporte_nulos(crudo).to_string(), "\n")

    limpio = limpiar(crudo)
    print(f"Dataset limpio: {limpio.shape[0]} filas x {limpio.shape[1]} columnas")
    print(f"Nulos restantes: {int(limpio.isna().sum().sum())}\n")

    print(f"Guardado en: {guardar(limpio, RUTA_SALIDA)}")
