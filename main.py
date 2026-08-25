"""Integracion final del laboratorio: usa los dos modulos del equipo.

Persona A aporta src/carga.py (cargar, reporte_nulos, limpiar, guardar) y
Persona B aporta src/analisis.py (resumen_por_grupo, top_k,
recta_minimos_cuadrados). Este archivo los junta y produce la salida que pide
la Etapa 6, en el orden que pide la Etapa 6.
"""

import matplotlib.pyplot as plt
import numpy as np

from src.analisis import recta_minimos_cuadrados, resumen_por_grupo, top_k
from src.carga import (
    CENTINELAS,
    OBJETIVO,
    RUTA_SALIDA,
    URL,
    cargar,
    guardar,
    limpiar,
    reporte_nulos,
)

# El sensor de oxido de estano que mejor sigue al benceno: correlacion 0.98.
# Es la pareja natural para la recta, y es el caso de uso real del dataset:
# predecir la medicion cara de referencia con un sensor barato.
PREDICTOR = "PT08.S2(NMHC)"


def separador(titulo):
    print(f"\n{'=' * 70}\n{titulo}\n{'=' * 70}")


def main():
    # ------------------------------------------------------------------
    # 1. Reporte de nulos del dataset CRUDO, antes de limpiar
    # ------------------------------------------------------------------
    separador("1. NULOS DEL DATASET CRUDO (antes de limpiar)")
    crudo = cargar(URL, na_values=CENTINELAS)
    print(f"Dimensiones: {crudo.shape[0]} filas x {crudo.shape[1]} columnas")
    print(f"Faltantes totales: {int(crudo.isna().sum().sum())}\n")
    print(reporte_nulos(crudo).to_string())

    limpio = limpiar(crudo)
    guardar(limpio, RUTA_SALIDA)
    print(f"\nLimpio: {limpio.shape[0]} x {limpio.shape[1]}, ", end="")
    print(f"nulos restantes: {int(limpio.isna().sum().sum())}")

    # ------------------------------------------------------------------
    # 2. resumen_por_grupo sobre el dataset YA LIMPIO
    # ------------------------------------------------------------------
    # La hora sale de 'Time' ("18:00:00" -> 18). Es la categoria natural del
    # dataset: la contaminacion tiene un ciclo diario marcado por el trafico.
    # Se parte por ":" y no con str[:2] porque las horas de un digito vienen
    # sin cero a la izquierda ("0:00:00"), y el corte fijo devolveria "0:".
    separador("2. RESUMEN POR HORA DEL DIA (dataset limpio)")
    limpio["hora"] = limpio["Time"].str.split(":").str[0].astype(int)
    resumen = resumen_por_grupo(limpio, "hora", [OBJETIVO, "NOx(GT)"])
    print(resumen.round(2).to_string())

    pico = resumen[(OBJETIVO, "mean")].idxmax()
    valle = resumen[(OBJETIVO, "mean")].idxmin()
    print(f"\nHora pico: {pico}:00  |  Hora valle: {valle}:00")

    # ------------------------------------------------------------------
    # 3. top_k con k=5
    # ------------------------------------------------------------------
    separador(f"3. TOP 5 REGISTROS CON MAYOR {OBJETIVO}")
    top = top_k(limpio, OBJETIVO, 5)
    print(top[["Date", "Time", OBJETIVO, PREDICTOR]].to_string(index=False))

    # ------------------------------------------------------------------
    # 4. Recta de minimos cuadrados entre dos variables numericas
    # ------------------------------------------------------------------
    separador(f"4. RECTA DE MINIMOS CUADRADOS: {OBJETIVO} ~ {PREDICTOR}")
    x = limpio[PREDICTOR].to_numpy()
    y = limpio[OBJETIVO].to_numpy()
    a, b = recta_minimos_cuadrados(x, y)
    print(f"Pendiente (a):  {a:.6f}")
    print(f"Intercepto (b): {b:.6f}")
    print(f"\nEcuacion: {OBJETIVO} = {a:.6f} * {PREDICTOR} + {b:.6f}")
    print(f"Correlacion: {np.corrcoef(x, y)[0, 1]:.4f}")

    # ------------------------------------------------------------------
    # 5. Grafico guardado en figura.png
    # ------------------------------------------------------------------
    separador("5. GRAFICO")
    fig, (izq, der) = plt.subplots(1, 2, figsize=(13, 5))

    izq.scatter(x, y, s=4, alpha=0.25, color="#4C72B0", label="Mediciones")
    recta_x = np.array([x.min(), x.max()])
    izq.plot(
        recta_x,
        a * recta_x + b,
        color="#C44E52",
        linewidth=2,
        label=f"y = {a:.4f}x + {b:.2f}",
    )
    izq.set_xlabel(PREDICTOR)
    izq.set_ylabel(OBJETIVO)
    izq.set_title("Ajuste por minimos cuadrados")
    izq.legend()
    izq.grid(alpha=0.3)

    medias = resumen[(OBJETIVO, "mean")]
    der.plot(medias.index, medias.to_numpy(), marker="o", color="#4C72B0")
    der.set_xlabel("Hora del dia")
    der.set_ylabel(f"{OBJETIVO} promedio")
    der.set_title("Ciclo diario de benceno")
    der.set_xticks(range(0, 24, 2))
    der.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("figura.png", dpi=120)
    print("Guardado en: figura.png")


if __name__ == "__main__":
    main()
