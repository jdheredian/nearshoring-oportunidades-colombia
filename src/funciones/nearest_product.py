import pandas as pd
from typing import List, Optional, Tuple, Union

def nearest_product(
    ps_df: pd.DataFrame,
    product: str,
    candidates: Optional[List[str]] = None,
    higher_is_closer: bool = True,
    threshold: Optional[Union[int, float]] = None,
) -> Tuple[Optional[str], Optional[float]]:
    """
    Devuelve el producto más cercano a `product` según el DataFrame `ps_df`.

    Parámetros
    ----------
    ps_df : pd.DataFrame
        Matriz K×K del product space (índices y columnas = códigos HS/PRODCOM…).
    product : str
        Código del producto cuyo vecino se busca.
    candidates : list[str] | None, opcional
        Lista de productos entre los que buscar. Si None, usa todos.
    higher_is_closer : bool, opcional (default=True)
        - True  → valores altos = más cerca.
        - False → valores bajos = más cerca.
    threshold : int | float | None, opcional (default=None)
        Umbral mínimo/máximo de cercanía:
          • Si `higher_is_closer` es True  → valor ≥ threshold.  
          • Si `higher_is_closer` es False → valor ≤ threshold.  
        Si None, no se aplica filtro.

    Retorna
    -------
    (str | None, float | None)
        Tupla (producto_más_cercano, valor). Devuelve (None, None) si
        ningún candidato cumple el umbral.
    """
    if product not in ps_df.index:
        raise KeyError(f"‘{product}’ no está en el índice del DataFrame.")
    
    # 1. Fila de interés
    row = ps_df.loc[product]

    # 2. Restringir búsqueda si se indica
    if candidates is not None:
        missing = set(candidates) - set(ps_df.columns)
        if missing:
            raise KeyError(f"Candidatos ausentes en DataFrame: {missing}")
        row = row[candidates]

    # 3. Quitar auto-comparación
    row = row.drop(labels=[product], errors='ignore')

    if row.empty:
        return None, None  # no hay candidatos

    # 4. Encontrar el mejor
    closest = row.idxmax() if higher_is_closer else row.idxmin()
    best_value = row[closest]

    # 5. Aplicar umbral si corresponde
    if threshold is not None:
        ok = best_value >= threshold if higher_is_closer else best_value <= threshold
        if not ok:
            return None, None  

    return closest, best_value