import pandas as pd
import numpy as np
import statsmodels.api as sm
from typing import Optional

def estimate_quality(
    df: pd.DataFrame,
    value_col: str = "Valor Comercio",
    quantity_col: str = "Cantidad",
    gdp_col: str = "GdpPerCapitaPPP",
    distance_col: str = "dist",
    product_col: str = "HS6",
    year_col: str = "Año",
    reporter_col: str = "ISO Importador",
    frontier_quantile: float = 0.9,
    n_deciles: int = 10
) -> pd.DataFrame:
    """
    Calcula una medida de calidad relativa (decomponiendo el precio unitario
    en ingreso del exportador y distancia) y la normaliza frente a la frontera
    mundial del percentil especificado.

    Parameters
    ----------
    df : pd.DataFrame
        Datos de comercio con al menos las columnas indicadas.
    value_col, quantity_col, gdp_col, distance_col, product_col, year_col,
    reporter_col : str
        Nombres de columnas a utilizar. Cambia si tus datos los nombran distinto.
    frontier_quantile : float, default 0.90
        Percentil que define la frontera mundial de calidad por producto-año.
    n_deciles : int, default 10
        Número de cortes (p. ej. 10 → deciles) para categorizar la calidad.

    Returns
    -------
    pd.DataFrame
        DataFrame con las columnas 'quality_estimate', 'frontera_XX',
        'quality_normalized' y la clasificación en cuantiles (Decile).
    """


    # 1. Variables básicas y logs
    df_work = df.copy()
    df_work["unit_value"] = (df_work[value_col] * 1_000) / df_work[quantity_col]
    df_work["ln_unit_value"]     = np.log(df_work["unit_value"])
    df_work["ln_income_exporter"] = np.log(df_work[gdp_col])
    df_work["ln_distance"]        = np.log(df_work[distance_col])

    # Quitar inf / -inf y filas incompletas 
    df_work.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_work.dropna(
        subset=["ln_unit_value", "ln_income_exporter", "ln_distance"],
        inplace=True
    )

    # 2. Regresión por producto-año y residuos ~ calidad
    quality_frames = []
    for (prod, yr), grp in df_work.groupby([product_col, year_col]):
        X = sm.add_constant(grp[["ln_income_exporter", "ln_distance"]])
        y = grp["ln_unit_value"]
        model = sm.OLS(y, X).fit()
        grp = grp.copy()
        grp["quality_estimate"] = model.resid.astype(float)
        quality_frames.append(grp)

    df_q = pd.concat(quality_frames, ignore_index=True)


    # 3. Normalización frente a la frontera (percentil 90 por defecto)
    frontier_label = f"frontera_{int(frontier_quantile*100)}"
    df_q[frontier_label] = (
        df_q
        .groupby([product_col, year_col])["quality_estimate"]
        .transform(lambda x: x.quantile(frontier_quantile))
    )

    df_q["quality_normalized"] = (
        df_q.apply(
            lambda r: r["quality_estimate"] / r[frontier_label]
            if r[frontier_label] != 0 else np.nan,
            axis=1
        )
    )


    # 4. Asignar deciles (o N-tiles) por producto-reporter-año
    df_q["Decile"] = (
        df_q
        .groupby([product_col, reporter_col, year_col])["quality_normalized"]
        .transform(
            lambda x: pd.qcut(
                x, n_deciles, labels=False, duplicates="drop"
            ) + 1
        )
    ).fillna(n_deciles).astype(int)

    # 5. Asignar Escaleras de Calidad
    df_q["quality_ladder"] = (
        df_q
        .groupby(['Año','HS6','ISO Importador'])['quality_normalized']
        .transform('max')
        - df_q
        .groupby(['Año','HS6','ISO Importador'])['quality_normalized']
        .transform('min')
    )

    # 6. Devolver
    return df_q