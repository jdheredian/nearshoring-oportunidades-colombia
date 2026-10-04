import pandas as pd

def find_distance(df: pd.DataFrame, producto1: str, producto2: str):
    """
    Devuelve el valor de la matriz de Product Space que relaciona `producto2`
    (fila) con `producto1` (columna), excluyendo la diagonal.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame cuadrado (K × K) con los códigos HS6 como índice y columnas.
    producto1 : str
        Código HS6 que se tomará como columna.
    producto2 : str
        Código HS6 que se tomará como fila.

    Retorna
    -------
    float
        Valor de proximidad (o la métrica que contenga la matriz) entre
        `producto1` y `producto2`.

    Ejemplo
    -------
    >>> obtener_relacion_productos(df_product_space_col, '621112', '611249')
    """
    # Comprobaciones básicas (opcional)
    if producto1 == producto2:
        raise ValueError("Los productos no deben ser iguales.")
    if producto1 not in df.columns:
        raise KeyError(f"{producto1} no aparece como columna en el DataFrame.")
    if producto2 not in df.index:
        raise KeyError(f"{producto2} no aparece como fila en el DataFrame.")

    # Seleccionar la columna, descartar la fila de sí mismo y extraer el valor
    return df[[producto1]].drop(index=producto1).loc[producto2, producto1]