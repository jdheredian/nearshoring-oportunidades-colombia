"""
config.py
Configuracion del proyecto Nearshoring Colombia, unica fuente de verdad.
Vive en <PROJECT_ROOT>/src/config.py y se instala como paquete editable
(pyproject.toml, py-modules). Por eso cualquier notebook o script del
proyecto puede hacer `from config import ...` sin importar en que carpeta este,
sin necesidad de copiar este archivo ni de tocar sys.path.

Reemplaza los nueve paths.yml del proyecto original y las rutas absolutas
a OneDrive que tenian los notebooks.
"""

# lo unico que sale con "from config import *". Sin esta lista tambien se exportan
# los modulos que config importa (os, sys, datetime, pd, plt...), y entonces un
# notebook que haga "from datetime import datetime" antes de importar config se queda
# con el modulo en vez de la clase, y datetime.now() falla.
__all__ = [
    # rutas
    "raiz", "data", "raw", "temp", "processed",
    "output", "figures", "tables", "other", "model",
    "reports", "lit", "slide", "doc",
    "logs", "log_runs", "fuente_dir",
    # fechas y sesion
    "fecha_hoy", "fecha_hora", "notebook", "usuario",
    # graficas
    "paleta", "patron_lineas", "patron_puntos", "fuente_aptos", "random_state",
    "colores_industrias", "colores_macrosectores",
    "fig_slide_completa", "fig_slide_mitad",
    "fig_doc_fila", "fig_doc_media_fila", "fig_doc_pagina",
    # etiquetas y parametros del proyecto
    "mapeo_macrosector", "ciiu_otros_quimica", "macrosectores",
    "variables_modelo", "target_modelo",
    "porcentaje_min", "porcentaje_max", "num_iteraciones",
    "top_n_industrias", "valor_inicial", "valor_final",
]

import pathlib
import datetime
import getpass
import logging
import os
import sys
import subprocess
import atexit
import warnings

# --- raiz del proyecto ---
# este archivo vive en <PROJECT_ROOT>/src/config.py
# por eso subimos 1 nivel para llegar a la raiz
raiz = pathlib.Path(__file__).resolve().parents[1]

# --- carpetas de datos ---
data = raiz / "data"
raw = data / "raw"
temp = data / "temp"
processed = data / "processed"

# --- carpeta de outputs ---
output = raiz / "output"
other = output / "other"
figures = output / "figures"
tables = output / "tables"
# model no viene en la plantilla: aqui guarda el GLM serializado (glm_model.pkl),
# que tarda en re-estimarse y que consume la tabla de coeficientes del deck
model = output / "model"

# --- carpetas de reports ---
reports = raiz / "reports"
lit = reports / "literature"
slide = reports / "slide"
doc = reports / "document"

# --- carpeta de logs ---
# separada de output: es metadata operativa de las corridas, no un entregable del analisis
logs = raiz / "logs"

# --- asegurar que las carpetas existan ---
for _carpeta in (raw, temp, processed, other, figures, tables, model, lit, slide, doc, logs):
    _carpeta.mkdir(parents=True, exist_ok=True)

# --- fecha de la corrida actual ---
fecha_hoy = datetime.date.today().isoformat()
fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- registro de auditoria: una linea al inicio y otra al fin de cada corrida ---
# en Jupyter el nombre sale de JPY_SESSION_NAME; en scripts, del archivo que se ejecuto.
# con python -c o en la consola interactiva no hay archivo, y queda "interactivo"
script = pathlib.Path(sys.argv[0]).stem if sys.argv[0] not in ("-c", "") else ""
notebook = pathlib.Path(os.environ.get("JPY_SESSION_NAME", "")).stem or script or "interactivo"
usuario = getpass.getuser()

# commit actual: amarra cada corrida al codigo exacto que la produjo.
# el try es necesario porque el proyecto puede no ser un repo git o git puede no estar instalado
try:
    commit = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=raiz, capture_output=True, text=True,
    ).stdout.strip() or "sin-commit"
except OSError:
    commit = "sin-commit"

log_runs = logs / "log_runs.log"

logger_runs = logging.getLogger("log_runs")
logger_runs.setLevel(logging.INFO)
logger_runs.propagate = False  # evita que Jupyter tambien imprima el log duplicado

if not logger_runs.handlers:  # evita duplicar el handler si el modulo se vuelve a importar
    handler = logging.FileHandler(log_runs)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger_runs.addHandler(handler)

logger_runs.info(f"INICIO | notebook={notebook} | usuario={usuario} | commit={commit}")
atexit.register(lambda: logger_runs.info(f"FIN    | notebook={notebook} | usuario={usuario} | commit={commit}"))

# --- semilla ---
# el original corria la simulacion Monte Carlo de la priorizacion sin semilla, y por eso
# el deck y el capitulo reportan cifras distintas para la misma tabla. aqui se fija para
# que el resultado sea reproducible. ver tools/markdown/AUDITORIA_MIGRACION.md
random_state = 20010326

# --- parametros de la simulacion de priorizacion ---
porcentaje_min = 0.10    # proporcion minima de productos a muestrear por industria
porcentaje_max = 0.20    # proporcion maxima de productos a muestrear por industria
num_iteraciones = 1000   # numero de iteraciones de la simulacion
top_n_industrias = 10    # numero de industrias que entran a la proyeccion
valor_inicial = 0        # valor de exportaciones en el periodo inicial
valor_final = 100        # valor de exportaciones en el periodo final

# --- etiquetas: clase de negocio a macrosector ---
macrosectores = [
    "Agroindustria y Alimentos",
    "Industria Química, Farmacéutica y Bioproductos",
    "Manufacturas Avanzadas y Bienes Industriales",
    "Industrias Extractivas",
]

mapeo_macrosector = {
    "Frutas frescas y frutas procesadas":                     "Agroindustria y Alimentos",
    "Cafés y cafes especiales":                               "Agroindustria y Alimentos",
    "Carne bovina":                                           "Agroindustria y Alimentos",
    "Pesca y acuicultura":                                    "Agroindustria y Alimentos",
    "Azúcar y derivados primarios":                           "Agroindustria y Alimentos",
    "Confitería":                                             "Agroindustria y Alimentos",
    "Otros productos alimenticios":                           "Agroindustria y Alimentos",

    "Cosméticos y productos de aseo personal":                "Industria Química, Farmacéutica y Bioproductos",
    "Agroquímicos y biológicos":                              "Industria Química, Farmacéutica y Bioproductos",
    "Sector farmacéutico":                                    "Industria Química, Farmacéutica y Bioproductos",
    "Plásticos y caucho":                                     "Industria Química, Farmacéutica y Bioproductos",
    "Química básica":                                         "Industria Química, Farmacéutica y Bioproductos",

    "Industria de maquinaria y transporte":                   "Manufacturas Avanzadas y Bienes Industriales",
    "Productos equipos de potencia y distribución eléctrica":  "Manufacturas Avanzadas y Bienes Industriales",
    "Metales derivados de materiales reciclados":             "Manufacturas Avanzadas y Bienes Industriales",
    "Metales a partir de material recuperado":                "Manufacturas Avanzadas y Bienes Industriales",
    "Productos metálicos":                                    "Manufacturas Avanzadas y Bienes Industriales",
    "Papel y productos de papel":                             "Manufacturas Avanzadas y Bienes Industriales",
    "Madera":                                                 "Manufacturas Avanzadas y Bienes Industriales",
    "Textiles y confección":                                  "Manufacturas Avanzadas y Bienes Industriales",
    "Minerales no metálicos":                                 "Manufacturas Avanzadas y Bienes Industriales",

    "Minería":                                                "Industrias Extractivas",
    "Derivados petróleo básicos":                             "Industrias Extractivas",
}

# la clase "Otros" no tiene macrosector propio: se desagrega por codigo CIIU.
# 3250 (instrumentos medicos y odontologicos) va a Quimica; el resto a Manufacturas
ciiu_otros_quimica = {"3250"}

# --- variables del modelo de auge exportador ---
target_modelo = "Delta_x"

variables_modelo = [
    "const", "log_Delta_m", "share_start", "log_duracion", "log_duracion2",
    "log_gdp_o", "log_gdp_o2", "log_gdp_d", "log_gdp_d2",
    "cultura_similaridad", "log_distancia",
]

# --- configuracion de librerias ---
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 100)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 100
paleta = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]

# paletas del proyecto original. se conservan tal cual porque son las que producen
# las figuras que consume el deck; cambiarlas cambiaria su aspecto
colores_industrias = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
]
colores_macrosectores = ["#e6194b", "#3cb44b", "#4363d8", "#f58231"]

# si se necesitan mas de 5 categorias y se acaba la paleta de colores solidos,
# usar fondo blanco con lineas del color (facecolor="white", edgecolor=color, hatch=patron_lineas)
# si tambien se acaban esas, usar fondo blanco con puntos del color (hatch=patron_puntos)
patron_lineas = "//"
patron_puntos = ".."

# --- Tipografia ---
# Aptos vive en tools/fonts/ y se registra al importar config, pero NO se fija como
# familia global: las figuras del deck (Image1, Image2, expos, Imagen 4) se produjeron
# con la tipografia por defecto de matplotlib, y fijar Aptos aqui las cambiaria de aspecto.
# Para usarla explicitamente en una figura: fontproperties=fuente_aptos
import matplotlib.font_manager as fm

fuente_dir = raiz / "tools" / "fonts"
fuente_dir.mkdir(parents=True, exist_ok=True)

fuentes = [a for a in sorted(fuente_dir.iterdir()) if a.suffix.lower() in (".ttf", ".otf")]
for archivo in fuentes:
    fm.fontManager.addfont(archivo)

_aptos = fuente_dir / "Aptos.ttf"
fuente_aptos = fm.FontProperties(fname=_aptos) if _aptos.exists() else None

# embebe la fuente como truetype al exportar. el default de matplotlib es type 3,
# que varias revistas rechazan en las figuras y que se edita mal en illustrator
plt.rcParams["pdf.fonttype"] = 42


# --- Tamanos estandar de graficas en pulgadas (ancho, alto) ---
# powerpoint / beamer 16:9
fig_slide_completa = (12, 6.5)  # slide completa con una sola imagen
fig_slide_mitad = (5.8, 6.5)    # cada imagen cuando van dos lado a lado en la misma slide

# word / latex en hoja A4 con margenes estandar
fig_doc_fila = (6.3, 4)        # una imagen a todo el ancho (una por fila)
fig_doc_media_fila = (3.0, 4)  # cada imagen cuando van dos lado a lado (dos por fila)
fig_doc_pagina = (6.3, 9)      # imagen de pagina completa
