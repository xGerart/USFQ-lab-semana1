import numpy as np
import pandas as pd
import pytest

from src.carga import limpiar, reporte_nulos


@pytest.fixture
def df_sucio():
    return pd.DataFrame(
        {
            "ciudad": ["  Quito  ", "GUAYAQUIL", "GUAYAQUIL", "Cuenca"],
            "medicion": [10.0, 20.0, 20.0, np.inf],
            "objetivo": [1.0, 2.0, 2.0, np.nan],
        }
    )


def test_limpiar_elimina_filas_duplicadas(df_sucio):
    resultado = limpiar(df_sucio, objetivo=None)
    assert resultado["ciudad"].tolist().count("guayaquil") == 1


def test_limpiar_no_deja_nulos_ni_infinitos(df_sucio):
    resultado = limpiar(df_sucio, objetivo=None)
    numericas = resultado.select_dtypes(include=[np.number])
    assert numericas.isna().sum().sum() == 0
    assert not np.isinf(numericas.to_numpy()).any()


def test_limpiar_normaliza_el_texto(df_sucio):
    resultado = limpiar(df_sucio, objetivo=None)
    assert "quito" in resultado["ciudad"].tolist()


def test_limpiar_elimina_columnas_con_demasiados_nulos():
    df = pd.DataFrame(
        {
            "buena": [1.0, 2.0, 3.0, 4.0],
            "casi_vacia": [1.0, np.nan, np.nan, np.nan],
        }
    )
    resultado = limpiar(df, umbral_columna=50, objetivo=None)
    assert "casi_vacia" not in resultado.columns
    assert len(resultado) == 4


def test_limpiar_no_imputa_la_variable_objetivo():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0], "objetivo": [10.0, np.nan, 30.0]})
    resultado = limpiar(df, objetivo="objetivo")
    assert len(resultado) == 2
    assert resultado["objetivo"].tolist() == [10.0, 30.0]


def test_reporte_nulos_cuenta_y_ordena():
    df = pd.DataFrame({"a": [1.0, np.nan, np.nan], "b": [1.0, 2.0, 3.0]})
    reporte = reporte_nulos(df)
    assert reporte.loc["a", "nulos"] == 2
    assert reporte.loc["a", "porcentaje"] == pytest.approx(66.67, abs=0.01)
    assert reporte.index[0] == "a"
