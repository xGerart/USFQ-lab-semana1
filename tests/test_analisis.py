import pandas as pd

from src.analisis import filtrar


def test_filtrar():
    df = pd.DataFrame({"edad": [10, 25, 40]})
    resultado = filtrar(df, "edad", 20)
    assert len(resultado) == 2
    assert resultado["edad"].min() > 20

import numpy as np
import pytest

from src.analisis import zscore


def test_zscore_media_cero():
    m = np.array([[1], [2], [3], [4]])
    z = zscore(m)
    assert z.mean() == pytest.approx(0.0)


from src.analisis import recta_minimos_cuadrados


def test_recta_minimos_cuadrados():
    x = np.array([1, 2, 3, 4])
    y = 2 * x + 1
    a, b = recta_minimos_cuadrados(x, y)
    assert a == pytest.approx(2.0)
    assert b == pytest.approx(1.0)