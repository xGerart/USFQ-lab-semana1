"""Analisis vectorizado del dataset Air Quality (UCI) - Persona B.

Ninguna funcion de este modulo abre archivos: todas reciben los datos ya
cargados como argumento. Eso es intencional y es lo que permite que Persona B
trabaje en paralelo con Persona A, sin esperar a que exista data/limpio.parquet.
"""

import numpy as np


def filtrar(df, columna, umbral):
    """Devuelve solo las filas donde df[columna] > umbral.

    df[columna] > umbral no devuelve True/False, devuelve una Series de
    booleanos del mismo largo que el DataFrame (una mascara). Al pasarla como
    indice, pandas conserva unicamente las filas cuya posicion vale True.
    """
    mascara = df[columna] > umbral
    return df[mascara]


def resumen_por_grupo(df, col_grupo, cols_num):
    """Media, desviacion y conteo de cols_num para cada categoria de col_grupo.

    El conteo importa tanto como la media: un promedio calculado sobre 3 filas
    no es comparable con uno calculado sobre 400.
    """
    return df.groupby(col_grupo)[cols_num].agg(["mean", "std", "count"])


def zscore(matriz):
    """Normaliza un ndarray 2D columna por columna: (x - media) / desviacion.

    axis=0 hace que mean y std se calculen POR COLUMNA. El resultado tiene
    forma (1, n_columnas) y numpy lo expande automaticamente a todas las filas
    por broadcasting, sin necesidad de un bucle for.
    """
    return (matriz - matriz.mean(axis=0)) / matriz.std(axis=0)


def top_k(df, columna, k):
    """Los k registros con mayor valor en esa columna, usando np.argsort.

    np.argsort no devuelve los valores ordenados sino las POSICIONES que los
    ordenarian, y siempre de menor a mayor. Por eso se invierte con [::-1]
    antes de cortar los primeros k.
    """
    valores = df[columna].to_numpy()
    posiciones = np.argsort(valores)[::-1][:k]
    return df.iloc[posiciones]


def recta_minimos_cuadrados(x, y):
    """Ajusta y = a*x + b y devuelve la tupla (a, b).

    lstsq resuelve A @ coeficientes = y. Para que el ajuste tenga intercepto
    hay que apilar junto a x una columna de unos: esa columna multiplica a b,
    de modo que b entra en la ecuacion como termino independiente.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    matriz_diseno = np.vstack([x, np.ones_like(x)]).T
    coeficientes, *_ = np.linalg.lstsq(matriz_diseno, y, rcond=None)
    a, b = coeficientes
    return a, b
