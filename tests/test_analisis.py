import numpy as np
import pandas as pd
import pytest

from src.analisis import filtrar, recta_minimos_cuadrados, zscore


@pytest.fixture
def df_mini():
    """Datos de prueba reutilizables: 3 filas, dos columnas de escala distinta.

    Se define una sola vez y pytest lo inyecta en cada prueba que lo pida como
    parametro. Las dos columnas tienen rangos muy distintos a proposito
    (decenas contra miles), para que zscore tenga algo real que normalizar.
    """
    return pd.DataFrame(
        {
            "edad": [10.0, 25.0, 40.0],
            "ingreso": [1000.0, 2000.0, 3000.0],
        }
    )


def test_filtrar(df_mini):
    # De [10, 25, 40], mayores estrictos que 20 son dos: 25 y 40.
    resultado = filtrar(df_mini, "edad", 20)
    assert len(resultado) == 2
    assert resultado["edad"].min() > 20


def test_zscore_media_cero_y_desviacion_uno(df_mini):
    # Se pasan las DOS columnas: si zscore no usara axis=0 mezclaria las
    # escalas (edad ~decenas, ingreso ~miles) y ninguna quedaria centrada.
    z = zscore(df_mini.to_numpy())
    np.testing.assert_allclose(z.mean(axis=0), [0.0, 0.0], atol=1e-9)
    np.testing.assert_allclose(z.std(axis=0), [1.0, 1.0], atol=1e-9)


def test_recta_minimos_cuadrados():
    # y = 2x + 1 exacto: el ajuste debe recuperar a=2 y b=1.
    x = np.array([1, 2, 3, 4])
    y = 2 * x + 1
    a, b = recta_minimos_cuadrados(x, y)
    assert a == pytest.approx(2.0)
    assert b == pytest.approx(1.0)