from fuzzywuzzy import fuzz, process

def fuzzy_match(value, choices, scorer=fuzz.token_sort_ratio, threshold=80):
    """
    Función para obtener la mejor coincidencia difusa de un valor dado dentro de una lista de opciones.

    Parameters
    ----------
        value (str): El valor de entrada que se desea comparar.
        choices (iterable of str): Lista de opciones en las cuales se busca la coincidencia.
        scorer (callable, opcional): Función que determina la similitud entre el valor y las opciones. 
                                     Por defecto se utiliza fuzz.token_sort_ratio.
        threshold (int, opcional): Puntuación mínima requerida para aceptar una coincidencia. 
                                   Por defecto es 80.

    Returns
    -------
        str o None: Retorna la opción que presenta la mayor similitud (y que cumple con el umbral establecido)
                    o None si ninguna coincidencia cumple el umbral.
    """
    # Obtiene el mejor match de las opciones usando el scorer dado
    match, score = process.extractOne(value, choices, scorer=scorer)
    return match if score >= threshold else None



