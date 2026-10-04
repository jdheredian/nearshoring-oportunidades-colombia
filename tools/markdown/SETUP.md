# Setup y funcionamiento de la plantilla

Este archivo documenta la maquinaria del proyecto: como instalarlo, como funciona
`config.py` y por que las cosas estan donde estan. **Viaja intacto entre proyectos** —
no hay que reescribirlo al clonar la plantilla, a diferencia del `README.md`.

La plantilla vive en **https://github.com/jdheredian/project-template**.

---

## Estructura

```text
project-template/
├── pyproject.toml          # que paquetes necesita el proyecto
├── README.md               # descripcion del proyecto: se reescribe al clonar
├── SETUP.md                # este archivo: maquinaria, viaja intacto
├── data/
│   ├── raw/                # datos originales, nunca se modifican
│   ├── temp/               # intermedios de trabajo
│   └── processed/          # datos limpios, listos para analisis
├── output/
│   ├── figures/            # graficas
│   ├── tables/             # tablas exportadas
│   └── other/              # otras salidas
├── reports/
│   ├── literature/         # bibliografia y lecturas
│   ├── slide/              # presentaciones
│   └── document/           # documentos e informes
├── logs/                   # registro de auditoria (se versiona)
├── tools/
│   └── fonts/              # tipografias .ttf/.otf para las graficas
│       └── download.py     # las baja de Google Fonts (correr una vez)
├── notebooks/              # notebooks numerados: 00_, 01_, 02_...
└── src/
    ├── config.py           # rutas y configuracion, unica fuente de verdad
    └── template/           # plantilla de script .py
```

Estas carpetas **no hay que crearlas a mano**: `src/config.py` las crea al importarse. Aun asi
van al repositorio con un archivo `.gitkeep` adentro, porque git no versiona carpetas vacias y
la estructura debe verse completa apenas se clona.

---

## Que hay que tener instalado

Solo **Python 3.12 o superior** y **git**. Nada mas.

```bash
brew install python@3.12     # macOS; en otros sistemas, descargar de python.org
```

No hace falta Anaconda ni Miniconda. Todo lo que el proyecto necesita esta declarado en
`pyproject.toml`, asi que `pip` reconstruye el entorno completo desde cero en una maquina nueva.
Incluso `geopandas` instala por pip sin problema — historicamente era el unico que obligaba a
usar conda por las librerias de GDAL, y ya no.

Si de todos modos prefieres trabajar con conda, instala **Miniconda**, no Anaconda completo:
te da el manejo de entornos sin los ~9 GB de paquetes preinstalados, que son justamente lo que
este esquema reemplaza.

---

## Primeros pasos

Cada vez que arranques un proyecto nuevo a partir de esta plantilla:

**1. Clonar y renombrar la carpeta**

```bash
git clone https://github.com/jdheredian/project-template.git mi-proyecto
cd mi-proyecto
```

**2. Renombrar el proyecto en `pyproject.toml`**

```toml
name = "mi-proyecto"
```

De ahi sale el nombre con el que queda instalado el paquete.

**3. Crear el entorno**

```bash
python3.12 -m venv .venv --prompt "mi-proyecto"
source .venv/bin/activate
```

El `--prompt` hace que la terminal muestre `(mi-proyecto)` en vez de `(.venv)`, util cuando
tienes varios proyectos abiertos a la vez. La carpeta se sigue llamando `.venv`: ese nombre es
el que VSCode busca para detectar el entorno automaticamente, asi que conviene no cambiarlo.

Si prefieres conda: `conda create -n mi-proyecto python=3.12 -y && conda activate mi-proyecto`.

**4. Instalar**

```bash
pip install -e .
```

Trae el nucleo: pandas, numpy, pyarrow, openpyxl, matplotlib, seaborn, scipy, statsmodels,
linearmodels, ipykernel y python-dotenv. Si el proyecto necesita mas:

```bash
pip install -e ".[ml]"     # scikit-learn
pip install -e ".[geo]"    # geopandas
pip install -e ".[web]"    # requests, beautifulsoup4, lxml, selenium, sqlalchemy
pip install -e ".[viz]"    # plotly
pip install -e ".[full]"   # todos los anteriores
```

**5. Elegir el kernel**

En VSCode: abrir un notebook, hacer clic en el selector de kernel arriba a la derecha y elegir
el interprete de `.venv`. VSCode lo detecta solo cuando esta en la raiz del proyecto.

**6. Congelar versiones al cerrar el analisis**

```bash
pip freeze > requirements.lock.txt
```

Este archivo si se versiona: es el registro de con que versiones exactas se produjeron los
resultados.

---

## Conceptos

Vale la pena entender que esta pasando, porque este flujo es distinto al de un Anaconda con
un solo entorno para todo.

**Que es un entorno virtual.** Una carpeta (`.venv/`) con su propio Python y sus propios
paquetes. Cada proyecto tiene el suyo, asi que actualizar pandas en uno no rompe los demas.
Aisla *paquetes*, no el sistema operativo — eso ultimo es lo que hace Docker, que es otra cosa
y mucho mas pesada.

**Que es la instalacion editable.** `pip install -e .` registra el proyecto en el entorno
apuntando a los archivos fuente, sin copiarlos. Gracias a eso `from config import *` funciona
desde `notebooks/`, desde `src/template/` o desde donde sea, sin copiar `config.py` a cada
carpeta ni tocar `sys.path`. Y como es *editable*, al editar `config.py` el cambio se ve de
inmediato: no hay que reinstalar.

**Por que un entorno por proyecto es obligatorio.** El modulo se llama `config`, un nombre
generico. Si dos proyectos quedaran instalados en el mismo entorno, uno pisaria al otro y el
notebook del proyecto A leeria las rutas del proyecto B, en silencio y sin error. Por eso ya no
sirve el kernel `base` de Anaconda compartido entre todo: cada proyecto necesita su entorno.

**`pyproject.toml` vs `requirements.lock.txt`.** El primero declara *que* necesitas
(`pandas`, sin version) y es lo que se edita a mano. El segundo congela *con que exactamente
corriste* (`pandas==3.0.5`) y se genera con `pip freeze`. El primero deja instalar en cualquier
maquina; el segundo permite reproducir un resultado viejo tal cual.

**Anaconda sigue sirviendo.** Nada de esto obliga a desinstalarlo. Un entorno de conda funciona
igual con el mismo `pyproject.toml`; lo unico que cambia es crear un entorno por proyecto en vez
de trabajar siempre sobre `base`.

---

## Uso diario

Activar el entorno al empezar a trabajar:

```bash
source .venv/bin/activate
```

Y en el notebook o script, una sola linea:

```python
from config import *
```

Con eso quedan disponibles todas las rutas y constantes.

**Agregar una dependencia nueva:** se agrega a `dependencies` en `pyproject.toml` y se corre
`pip install -e .` otra vez. **Editar `config.py` no requiere reinstalar nada.**

---

## Credenciales

Si el proyecto usa contrasenas o tokens, van en un archivo `.env` en la raiz — nunca escritos
en el notebook:

```text
DB_PASSWORD=...
API_TOKEN=...
```

Luego se descomenta el bloque de `python-dotenv` al final de `src/config.py`. El `.gitignore`
ya impide que `.env` se suba al repositorio.

---

## Tipografia

Las graficas usan la fuente por defecto de matplotlib mientras no haya nada en `tools/fonts/`.
Para cambiarla basta con copiar los archivos ahi: `config.py` registra al importarse todo
`.ttf` y `.otf` que encuentre. No se edita codigo.

Conviene copiar todos los pesos, no solo el Regular:

```text
tools/fonts/
├── download.py
├── Lato-Regular.ttf
├── Lato-Bold.ttf
├── Lato-Italic.ttf
└── Lato-BoldItalic.ttf
```

`config.py` solo mira los `.ttf` y `.otf`, asi que `download.py` convive ahi sin estorbar.

matplotlib no fabrica la negrita a partir del Regular. Si falta `Bold`, los titulos en negrita
caen a la fuente por defecto y la grafica sale con dos tipografias mezcladas. Los cuatro
archivos comparten familia, asi que cuentan como una sola fuente. Si hay varias familias en la
carpeta se usa la primera en orden alfabetico: lo simple es dejar una sola.

Para bajarlas de Google Fonts, `tools/fonts/download.py` las deja en esa misma carpeta. Pide
las urls una por una y termina con un enter vacio:

```bash
python tools/fonts/download.py
```

Sirve tanto la url del archivo en bruto como la de la pagina de GitHub: la segunda devuelve
html y no la fuente, asi que el script la corrige antes de bajarla. Si aun asi lo que llega no
es una tipografia, avisa y no la guarda, porque un html con nombre `.ttf` rompe el import de
`config` en todos los notebooks.

**Ojo con las fuentes variables.** Google Fonts esta migrando a un solo archivo con ejes
(`Roboto[wdth,wght].ttf` en vez de un `.ttf` por peso). matplotlib lo registra pero no alcanza
el eje de peso: al pedir negrita la dibuja en redonda, sin error visible. Conviene bajar los
pesos estaticos, normalmente en la subcarpeta `static/` del repositorio.

**Licencias.** Muchas tipografias comerciales no se pueden redistribuir, y subirlas al
repositorio es justamente eso. Si la del proyecto tiene esa restriccion, se agrega al
`.gitignore` y se anota en el `README.md` de donde se saca:

```text
tools/fonts/*.ttf
tools/fonts/*.otf
```

Las de Google Fonts (licencia SIL OFL) si se pueden versionar, y es lo mas comodo.

**PDF.** `config.py` fija `pdf.fonttype = 42`, que embebe la fuente como TrueType. El default de
matplotlib es Type 3, que guarda cada letra como instrucciones de dibujo: varias revistas lo
rechazan en las figuras y se edita mal en Illustrator o Inkscape.

Si los documentos de `reports/` se compilan con XeLaTeX o LuaLaTeX, `fontspec` puede apuntar a
la misma carpeta para que figuras y texto queden en la misma tipografia:

```latex
\usepackage{fontspec}
\setmainfont{Lato}[Path=../../tools/fonts/, Extension=.ttf,
              UprightFont=*-Regular, BoldFont=*-Bold, ItalicFont=*-Italic]
```

---


## Registro de auditoria

Cada vez que se importa `config`, se escriben dos lineas en `logs/log_runs.log`: una al empezar
y otra al terminar.

```text
2026-08-30 10:15:22 | INICIO | notebook=01_limpieza | usuario=jdheredia | commit=a3f9c21
2026-08-30 10:18:44 | FIN    | notebook=01_limpieza | usuario=jdheredia | commit=a3f9c21
```

El `commit` es lo que hace util el registro: amarra cada corrida al codigo exacto que la
produjo, asi que meses despues se puede reconstruir el estado del proyecto en el momento en que
se genero un resultado. Si el proyecto todavia no es un repo de git, queda como `sin-commit`.

**Este archivo si se versiona**, a diferencia de los demas `.log`. Como es append-only, dos
personas corriendo notebooks generarian un conflicto en cada merge; para evitarlo,
`.gitattributes` lo marca con `merge=union`, que le indica a git que conserve las lineas de
ambos lados en vez de pedir resolucion manual. No hay que configurar nada: `.gitattributes`
viaja con el repositorio.

Al mezclar ramas las lineas pueden quedar fuera de orden cronologico, porque git las intercala
segun la rama. Como cada linea lleva su fecha, basta ordenarlas al revisarlas:

```bash
sort logs/log_runs.log
```

Los `.log` que genera LaTeX al compilar en `reports/` siguen ignorados: son basura de
compilacion, no auditoria.

---

## Referencia de `config.py`

**Rutas** (objetos `Path`, se combinan con `/`: `raw / 'archivo.parquet'`)

| Nombre | Carpeta |
|---|---|
| `raiz` | raiz del proyecto |
| `data`, `raw`, `temp`, `processed` | `data/` y sus subcarpetas |
| `output`, `figures`, `tables`, `other` | `output/` y sus subcarpetas |
| `reports`, `lit`, `slide`, `doc` | `reports/` y sus subcarpetas |
| `logs`, `log_runs` | carpeta de logs y archivo de registro |
| `fuente_dir` | `tools/fonts/`, para tipografias `.ttf` |

**Fechas y sesion**

| Nombre | Contenido |
|---|---|
| `fecha_hoy` | fecha de la corrida, `YYYY-MM-DD` |
| `fecha_hora` | fecha y hora, `YYYY-MM-DD HH:MM:SS` |
| `notebook`, `usuario` | nombre del notebook o script y usuario que lo corrio |

**Constantes de graficas**

| Nombre | Uso |
|---|---|
| `paleta` | 5 colores base |
| `fuente` | familia tipografica activa, o `None` si se usa la default |
| `patron_lineas`, `patron_puntos` | rellenos para cuando se acaba la paleta |
| `fig_slide_completa`, `fig_slide_mitad` | tamanos para presentaciones 16:9 |
| `fig_doc_fila`, `fig_doc_media_fila`, `fig_doc_pagina` | tamanos para documentos A4 |
| `random_state` | semilla fija para resultados reproducibles |

Ademas, `config.py` aplica al importarse: opciones de visualizacion de pandas, `rcParams` de
matplotlib y el registro de la corrida en `logs/log_runs.log` (una linea al iniciar y otra
al terminar).

`from config import *` trae **solo los nombres de estas tablas**, porque `config.py` los declara
en su `__all__`. Las librerias se importan en el notebook como siempre (`import pandas as pd`):
no llegan por `config`. Sin ese `__all__` tambien saldrian los modulos que `config` importa por
dentro, y un notebook que hiciera `from datetime import datetime` antes de importar `config`
se quedaria con el modulo en vez de la clase, rompiendo `datetime.now()`.

Para guardar una grafica en una carpeta con la fecha del dia:

```python
carpeta_hoy = figures / fecha_hoy
carpeta_hoy.mkdir(parents=True, exist_ok=True)
fig.savefig(carpeta_hoy / 'grafico.png', dpi=300, bbox_inches='tight')
```
