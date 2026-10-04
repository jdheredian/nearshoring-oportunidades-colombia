"""
Compara cada artefacto regenerado por la cadena contra el del proyecto original.

Uso:
    python tools/verificar_migracion.py [prefijo ...]

Para cada par informa forma, columnas, dtypes y diferencia maxima por columna numerica.
El manifiesto vive en MANIFIESTO: regenerado (relativo a la raiz) -> original (ruta absoluta).
"""
import sys
import pathlib

import pandas as pd
import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[1]
ORIG = pathlib.Path(
    "/Users/juandiegoheredianino/Library/CloudStorage/OneDrive-Fedesarrollo/"
    "David Gelvez & Rafael Puyana/Nearshoring"
)

# por debajo de estos umbrales la diferencia se atribuye al orden de acumulacion en
# punto flotante y no a un cambio de resultado
TOLERANCIA_MATERIAL = 1e-6

CAR = ORIG / "Caracterización"
IMP = ORIG / "Impacto"

MANIFIESTO = {
    # 01_cleaning / 01_correlativas_hs
    "data/temp/df_hs2012_2017.parquet": CAR / "data/df_hs2012_2017.parquet",
    "data/temp/df_hs2012_2022.parquet": CAR / "data/df_hs2012_2022.parquet",
    "data/temp/df_leamer.parquet":      CAR / "data/df_leamer.parquet",
    "data/temp/df_BEC.parquet":         CAR / "data/df_BEC.parquet",
    "data/temp/df_hs_names.parquet":    CAR / "data/df_hs_names.parquet",
    "data/temp/df_ciiu.parquet":        CAR / "data/df_ciiu.parquet",
    "data/temp/df_ciiu_1996.parquet":   IMP / "data/raw/exportaciones/df_ciiu.parquet",

    # 01_cleaning / 02_comercio
    "data/temp/df_comercio.parquet":         CAR / "data/df_comercio.parquet",
    "data/temp/df_comercio_mundial.parquet": CAR / "data/df_comercio_mundial.parquet",
    "data/temp/df_hhi.parquet":              CAR / "data/df_hhi.parquet",

    # 01_cleaning / 03..05
    "data/temp/df_product_space.parquet":     CAR / "data/df_product_space.parquet",
    "data/temp/df_info_calidad.parquet":      CAR / "data/df_info_calidad.parquet",
    "data/temp/df_calidad.parquet":           CAR / "data/df_calidad.parquet",
    "data/temp/df_calidad_13.parquet":        CAR / "data/df_calidad_13.parquet",
    "data/temp/potencial_exportador.parquet": CAR / "data/potencial_exportador.parquet",

    # 01_cleaning / 06..09
    "data/temp/df_aranceles.parquet": CAR / "data/df_aranceles.parquet",
    "data/temp/df_trump.parquet":     CAR / "data/df_trump.parquet",
    "data/temp/df_ntms.parquet":      CAR / "data/df_ntms.parquet",
    "data/temp/df_600.parquet":       CAR / "data/df_600.parquet",
    "data/temp/df_rndc.parquet":      CAR / "data/df_rndc.parquet",
    "data/temp/df_costos_externos.parquet": CAR / "data/df_costos_externos.parquet",
    "data/temp/df_amcham.parquet":    IMP / "data/raw/exportaciones/productos/df_amcham.parquet",

    # 02_stats
    "data/temp/df_products_caracterizado.parquet": CAR / "df_products/caracterizado/df_products.parquet",
    "data/temp/df_products_mercado.parquet": CAR / "df_products/con tamaño de mercado/df_products.parquet",
    "output/tables/df_potencial_exportador.xlsx": CAR / "outputs/df_potencial_exportador.xlsx",
    "output/tables/calidad/criterio1.xlsx": CAR / "outputs/calidad/criterio1.xlsx",
    "output/tables/calidad/criterio2.xlsx": CAR / "outputs/calidad/criterio2.xlsx",
    "output/tables/calidad/criterio3.xlsx": CAR / "outputs/calidad/criterio3.xlsx",
    "output/tables/calidad/criterio4.xlsx": CAR / "outputs/calidad/criterio4.xlsx",
    "output/tables/calidad/otros países/chl_criterio4.xlsx": CAR / "outputs/calidad/otros países/chl_criterio4.xlsx",
    "output/tables/calidad/otros países/mex_criterio4.xlsx": CAR / "outputs/calidad/otros países/mex_criterio4.xlsx",
    "output/tables/calidad/otros países/per_criterio4.xlsx": CAR / "outputs/calidad/otros países/per_criterio4.xlsx",
    "output/tables/resiliencia/df_resiliencia.xlsx": CAR / "outputs/resiliencia/df_resiliencia.xlsx",
    "output/tables/resiliencia/df_resiliencia_nec_declarada.xlsx": CAR / "outputs/resiliencia/df_resiliencia_nec_declarada.xlsx",
    "output/tables/AmChamOverLap.xlsx": ORIG / "AmCham/AmChamOverLap.xlsx",
    "output/tables/tariffs/df_tariffs.xlsx": CAR / "outputs/tariffs/df_tariffs.xlsx",
    "output/tables/tariffs/df_tariffs_trump.xlsx": CAR / "outputs/tariffs/df_tariffs_trump.xlsx",
    "output/tables/tariffs/df_ntms.xlsx": CAR / "outputs/tariffs/df_ntms.xlsx",
    "output/tables/localizacion/loc internos.xlsx": CAR / "outputs/localizacion/loc internos.xlsx",
    "output/tables/localizacion/loc externos.xlsx": CAR / "outputs/localizacion/loc externos.xlsx",
    "output/tables/Output Final 040725.xlsx": CAR / "outputs/Output Final 040725.xlsx",

    # 01_cleaning / 10 y 11: cadena de impacto
    "data/temp/exportaciones/deflactor.parquet":   IMP / "data/temp/exportaciones/deflactor.parquet",
    "data/temp/exportaciones/df_productos.parquet": IMP / "data/temp/exportaciones/df_productos.parquet",
    "data/temp/exportaciones/df_comercio.parquet": IMP / "data/temp/exportaciones/df_comercio.parquet",
    "data/temp/exportaciones/df_controles.parquet": IMP / "data/temp/exportaciones/df_controles.parquet",
    "data/temp/exportaciones/df_paises.parquet":   IMP / "data/temp/exportaciones/df_paises.parquet",
    "data/temp/pib/multiplicadores_leontief.parquet": IMP / "data/temp/pib/multiplicadores_leontief.parquet",
    "data/temp/pib/df_ciiu_mio.parquet":           IMP / "data/temp/pib/df_ciiu_mio.parquet",
    "data/temp/pib/df_va.parquet":                 IMP / "data/temp/pib/df_va.parquet",

    # 03_models
    "data/temp/exportaciones/df_surge_vars_6.parquet": IMP / "df_surge_vars_6.parquet",
    "data/temp/exportaciones/df_para_estimacion.parquet": IMP / "df_para_estimacion.parquet",
    "data/temp/exportaciones/df_regresion_glm.parquet": IMP / "df_regresion_glm.parquet",
    "data/temp/exportaciones/df_m_forecast_6_8_25.parquet": IMP / "data/temp/exportaciones/df_m_forecast_6_8_25.parquet",
    "data/temp/exportaciones/X_fuera_muestra.parquet": IMP / "X_fuera_muestra.parquet",
    "data/processed/predicciones_proyeccion.parquet": IMP / "data/processed/proyección/predicciones_proyeccion.parquet",
    "data/processed/df_hat_complex.parquet":       IMP / "data/processed/proyección/df_hat_complex.parquet",
}


def _leer(ruta):
    """Lee parquet o excel segun la extension."""
    if ruta.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(ruta)
    return pd.read_parquet(ruta)


def comparar(nuevo, viejo):
    """Devuelve (veredicto, lineas de detalle)."""
    det = []
    if not nuevo.exists():
        return "SIN GENERAR", ["el artefacto regenerado no existe"]
    if not viejo.exists():
        return "SIN ORIGINAL", ["no hay original contra el cual comparar"]

    a = _leer(nuevo)
    b = _leer(viejo)

    if a.equals(b):
        return "IDENTICO", [f"{a.shape[0]:,} filas x {a.shape[1]} columnas"]

    if a.shape != b.shape:
        det.append(f"forma: regenerado {a.shape} vs original {b.shape}")
    solo_n = [c for c in a.columns if c not in b.columns]
    solo_o = [c for c in b.columns if c not in a.columns]
    if solo_n:
        det.append(f"columnas solo en el regenerado: {solo_n}")
    if solo_o:
        det.append(f"columnas solo en el original: {solo_o}")

    comunes = [c for c in a.columns if c in b.columns]

    # mismo contenido en las columnas comunes y en el mismo orden de filas:
    # la unica diferencia son columnas que el original traia de mas o de menos
    if (a.shape[0] == b.shape[0] and comunes
            and a[comunes].reset_index(drop=True).equals(b[comunes].reset_index(drop=True))):
        return "IGUAL, COLS EXTRA", det + [f"{a.shape[0]:,} filas; las columnas comunes coinciden exactamente"]

    dtypes = [(c, str(a[c].dtype), str(b[c].dtype)) for c in comunes if a[c].dtype != b[c].dtype]
    if dtypes:
        det.append("dtypes distintos: " + ", ".join(f"{c} {x} vs {y}" for c, x, y in dtypes))

    # ordena por las columnas comunes para descartar diferencias de orden de filas
    if a.shape[0] == b.shape[0] and comunes:
        clave = comunes[: min(3, len(comunes))]
        try:
            a_o = a[comunes].sort_values(clave).reset_index(drop=True)
            b_o = b[comunes].sort_values(clave).reset_index(drop=True)
        except TypeError:
            a_o, b_o = a[comunes], b[comunes]
        if a_o.equals(b_o):
            return "IGUAL SALVO ORDEN", det + [f"{a.shape[0]:,} filas; difiere solo el orden"]
        difiere = []
        solo_flotante = True
        for c in comunes:
            s1, s2 = a_o[c], b_o[c]
            if s1.equals(s2):
                continue
            if pd.api.types.is_numeric_dtype(s1) and pd.api.types.is_numeric_dtype(s2):
                d = (s1 - s2).abs()
                materiales = int((d > TOLERANCIA_MATERIAL).sum())
                if materiales:
                    solo_flotante = False
                difiere.append(
                    f"{c}: maxdif={d.max():.6g}, mediana={d.median():.3g}, "
                    f"filas>{TOLERANCIA_MATERIAL:g}={materiales:,} de {len(s1):,}")
            else:
                solo_flotante = False
                difiere.append(f"{c}: filas_dif={int((s1.astype(str) != s2.astype(str)).sum()):,}")
        det += ["columnas que difieren:"] + ["   " + x for x in difiere]
        if solo_flotante and not solo_n and not solo_o:
            return "IGUAL (flotante)", det

    return "DIFIERE", det


def main(prefijos):
    items = [(k, v) for k, v in MANIFIESTO.items()
             if not prefijos or any(k.startswith(p) or p in k for p in prefijos)]
    resumen = {}
    for rel, orig in items:
        veredicto, det = comparar(RAIZ / rel, orig)
        resumen[veredicto] = resumen.get(veredicto, 0) + 1
        print(f"[{veredicto:>17}] {rel}")
        for linea in det:
            print(f"                    {linea}")
    print("\n" + "-" * 60)
    total = len(items)
    for k, v in sorted(resumen.items()):
        print(f"{k:>17}: {v} de {total}")


if __name__ == "__main__":
    main(sys.argv[1:])
