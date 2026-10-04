import pandas as pd


def hhi(
    df: pd.DataFrame,
    grupo_entidad: str,
    valor: str,
    otras_dimensiones: list,
    renombrar_columna: str = "HHI"
) -> pd.DataFrame:
    """
    Calcula el Índice Herfindahl-Hirschman (HHI) para cada combinación de las dimensiones especificadas.

    Este índice se calcula a partir de la participación de cada entidad (definida en 'grupo_entidad') en el valor total correspondiente 
    a cada combinación de las columnas especificadas en 'otras_dimensiones'. El HHI se escala a la métrica 0–10 000, tal como es 
    utilizada por la DOJ.

    Parámetros:
        df (pd.DataFrame): DataFrame que contiene los datos originales.
        grupo_entidad (str): Nombre de la columna que identifica la entidad sobre la que se calcula la participación.
        valor (str): Nombre de la columna cuyos valores se suman para obtener la participación de cada entidad.
        otras_dimensiones (list): Lista de nombres de columnas que definen las diferentes dimensiones o mercados en los que se agrupa el cálculo.
        renombrar_columna (str, opcional): Nombre asignado a la columna que contiene el HHI resultante. Por defecto es "HHI".

    Retorna:
        pd.DataFrame: DataFrame que contiene, para cada combinación de las columnas definidas en 'otras_dimensiones',
        el índice HHI calculado y escalado a la métrica de 0 a 10 000.
    """
    # Paso 1: suma por entidad + dimensiones
    agrup_cols = otras_dimensiones + [grupo_entidad]
    tmp = (df.groupby(agrup_cols, as_index=False)[valor]
             .sum()
             )

    # Paso 2: total de cada mercado (sin la entidad)
    total_cols = otras_dimensiones
    totales = (tmp.groupby(total_cols, as_index=False)[valor]
                   .sum()
                   .rename(columns={valor: "total_mercado"}))

    # Paso 3: fusiona, calcula participación y su cuadrado
    tmp = tmp.merge(totales, on=total_cols, how="left")
    tmp["participacion"] = tmp[valor] / tmp["total_mercado"]
    tmp["participacion_cuad"] = tmp["participacion"] ** 2

    # Paso 4: suma de cuadrados → HHI
    hhi = (tmp.groupby(total_cols, as_index=False)["participacion_cuad"]
              .sum()
              .rename(columns={"participacion_cuad": renombrar_columna}))

    # Escala a la métrica 0–10 000 usada por la DOJ:
    hhi[renombrar_columna] *= 10_000

    return hhi