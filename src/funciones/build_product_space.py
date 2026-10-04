import pandas as pd
import numpy as np
import networkx as nx
from itertools import combinations

def build_product_space(df,
                        country_col="country",
                        product_col="product",
                        value_col="value",
                        rca_threshold=1.0,
                        prox_threshold=0.55,
                        include_mst=True):
    """
    Construye el grafo del Product Space y la matriz de proximidades φ_ij.

    Parámetros
    ----------
    df : pandas.DataFrame
        Datos de comercio en formato largo: una fila por (país, producto) con su
        valor exportado.
    country_col, product_col, value_col : str
        Nombres de las columnas en `df`.
    rca_threshold : float, default 1.0
        Umbral para considerar que un país tiene ventaja comparativa revelada.
    prox_threshold : float, default 0.55
        Umbral mínimo de proximidad φ para dibujar una arista (además del MST).
    include_mst : bool, default True
        Asegura conectividad añadiendo el árbol generador mínimo (sobre distancias 1-φ).

    Devuelve
    --------
    G : networkx.Graph
        Grafo no dirigido con nodos = productos y aristas ponderadas por 'phi'.
    phi_df : pandas.DataFrame
        Matriz simétrica de proximidades (índice y columnas = productos).
    """
    # ---------- 1. Cálculo del RCA ----------
    df = df.copy()
    country_tot = df.groupby(country_col)[value_col].sum()
    product_tot = df.groupby(product_col)[value_col].sum()
    world_tot = product_tot.sum()

    df = df.merge(country_tot.rename("tot_country"), on=country_col)
    df = df.merge(product_tot.rename("tot_product"), on=product_col)

    df["rca"] = (df[value_col] / df["tot_country"]) / (df["tot_product"] / world_tot)

    # Matriz binaria M[c,i] = 1 si RCA >= umbral
    competitive = df[df["rca"] >= rca_threshold]
    prod_to_countries = competitive.groupby(product_col)[country_col].apply(set)

    products = prod_to_countries.index.tolist()
    n = len(products)
    phi_mat = np.eye(n)

    # ---------- 2. Product Space ----------
    for i, j in combinations(range(n), 2):
        A = prod_to_countries.get(products[i], set())
        B = prod_to_countries.get(products[j], set())
        if not A or not B:
            phi = 0.0
        else:
            pij = len(A & B) / len(A)   # P(RCA_i | RCA_j)
            pji = len(A & B) / len(B)   # P(RCA_j | RCA_i)
            phi = min(pij, pji)
        phi_mat[i, j] = phi_mat[j, i] = phi

    phi_df = pd.DataFrame(phi_mat, index=products, columns=products)

    # ---------- 3. Visualización ----------
    G = nx.Graph()
    G.add_nodes_from(products)

    # (a) Árbol generador mínimo para asegurar conectividad
    if include_mst:
        dist_mat = 1 - phi_mat                                   # distancia = 1-φ
        KG = nx.Graph()
        for i, j in combinations(range(n), 2):
            KG.add_edge(products[i], products[j], weight=dist_mat[i, j])
        mst = nx.minimum_spanning_tree(KG, weight="weight")
        for u, v, d in mst.edges(data=True):
            G.add_edge(u, v, phi=1 - d["weight"])

    # (b) Aristas con φ ≥ umbral
    for i, j in combinations(range(n), 2):
        if phi_mat[i, j] >= prox_threshold:
            G.add_edge(products[i], products[j], phi=phi_mat[i, j])

    return G, phi_df