# Oportunidades de inversión en Colombia

**Cuantificación del potencial del nearshoring.** Fedesarrollo para el Banco Interamericano de
Desarrollo, 2025–2026.

Cuantificación del tamaño de la oportunidad económica y social que representaría para Colombia
una estrategia de nearshoring: cuánto podrían crecer las exportaciones, qué industrias
concentrarían esa ganancia y qué efecto tendría sobre el producto interno bruto, el empleo, la
pobreza y el recaudo tributario.

**Autor:** Juan Diego Heredia Niño — jheredia@fedesarrollo.org.co
**Institución:** Fedesarrollo, para el Banco Interamericano de Desarrollo
**Período:** 2025 – 2026

Este repositorio es la migración del proyecto original, que vivía repartido en varias carpetas
de OneDrive. El detalle de qué se encontró, qué se cambió y qué se verificó está en
**[tools/markdown/AUDITORIA_MIGRACION.md](tools/markdown/AUDITORIA_MIGRACION.md)**; lo que queda
por hacer, en **[tools/markdown/pendientes.md](tools/markdown/pendientes.md)**.

---

## Datos

| Fuente | Contenido | Período | Ubicación |
|---|---|---|---|
| WITS, Banco Mundial | Comercio bilateral por producto HS6, un archivo por año | 1995–2023 | `data/raw/exportaciones/comercio/` |
| WITS, Banco Mundial | Comercio mundial y aranceles aplicados | | `data/raw/comercio/`, `data/raw/aranceles/` |
| ITC Export Potential Map | Potencial exportador de Colombia por producto y destino | descarga del 19-sep-2026 | `data/raw/itc/` |
| UNCTAD TRAINS | Medidas no arancelarias por país y producto | | `data/raw/aranceles/ntms/` |
| DIAN | Declaraciones de exportación, formulario 600 | 2023 | `data/raw/formulario600/` |
| Ministerio de Transporte | Registro Nacional de Despachos de Carga por Carretera | descarga del 30-may-2025 | `data/raw/logistica/` |
| Censo de Estados Unidos | Costos de transporte internacional | 2021 | `data/raw/logistica/` |
| DANE | Matriz insumo-producto 2019, cuentas nacionales anuales, estructura CIIU Rev. 4 A.C. | | `data/raw/pib/`, `data/raw/ciiu/` |
| CEPII | Distancias bilaterales y similitud cultural | | `data/raw/exportaciones/controles/` |
| FMI y FRED | Producto interno bruto per cápita y deflactor de Estados Unidos | descarga del 25-ago-2025 | `data/raw/exportaciones/gdp/`, `data/raw/descargas/` |
| BID, Araújo Ibarra, AmCham | Listas de productos priorizados | | `data/raw/insumos/`, `data/raw/amcham/` |

Los insumos que no se reconstruyen desde la cadena están archivados con su fecha de descarga en
`data/raw/descargas/` y `data/raw/modelo/`. El motivo de cada uno está en la auditoría.

`data/` no se versiona: `data/raw` pesa 9,5 GB y se repone con `tools/copiar_raw.sh` desde la
carpeta de OneDrive del proyecto original; `data/temp` y `data/processed` los regenera la cadena.
Sin esos insumos el repositorio no corre, de modo que la copia de referencia de `data/raw` hay que
conservarla por fuera.

---

## Notebooks

Se corren en orden numérico, primero por carpeta y luego por archivo.

### `00_download/` — insumos que se bajaban en tiempo de ejecución

| Notebook | Qué hace |
|---|---|
| `01_deflactor_fred` | Deflactor anual del producto interno bruto de Estados Unidos, base 2019 |
| `02_codigos_pais` | Correspondencia entre códigos ISO y la nomenclatura de países de WITS |
| `03_potencial_exportador_itc` | Potencial exportador de Colombia hacia 189 mercados, desde el Export Potential Map del ITC |

Los dos primeros leen por defecto la copia archivada; la bandera `reejecutar_descarga` vuelve a
consultar la fuente viva, con el riesgo de que el resultado ya no coincida. El tercero sí baja
del portal del ITC y deja la fecha de descarga en el nombre del archivo.

### `01_cleaning/` — limpieza y estructuración

| Notebook | Qué hace |
|---|---|
| `01_correlativas_hs` | Correspondencias HS 2017 y HS 2022 a HS 2012, clasificación de Leamer, categorías económicas, nombres de producto y correspondencia con la CIIU |
| `02_comercio` | Base de comercio bilateral y concentración de mercado |
| `03_product_space` | Red de proximidad entre productos |
| `04_calidad` | Calidad relativa por valores unitarios ajustados |
| `05_potencial_exportador` | Potencial exportador por producto y mercado |
| `06_aranceles_ntms` | Aranceles bilaterales y medidas no arancelarias |
| `07_formulario600` | Declaraciones de exportación por región y aduana |
| `08_logistica` | Costos de transporte interno y externo |
| `09_amcham` | Productos de AmCham y su margen de oportunidad |
| `10_exportaciones_impacto` | Panel de comercio de largo plazo y controles gravitacionales |
| `11_matriz_io` | Multiplicadores de Leontief y valor agregado sectorial |
| `12_indice_normalizado` | Índice del crecimiento exportador a veinte años, por ventanas móviles sobre cuatro países |

### `02_stats/` — caracterización de los productos

| Notebook | Qué hace |
|---|---|
| `01_caracterizacion` | Consolida la cartera de productos con oportunidad y les asigna su margen |
| `02_tamano_mercado` | Potencial exportador restante, descontando el comercio ya observado |
| `03_calidad` | Cuatro criterios de calidad, con Chile, México y Perú como comparación |
| `04_resiliencia` | Concentración de mercado y estrategias de resiliencia declaradas |
| `05_medidas_arancelarias` | Ventaja arancelaria frente a otros proveedores, con y sin los aranceles anunciados |
| `06_ntms` | Ventaja en medidas no arancelarias |
| `07_localizacion` | Costos de transporte interno y posición frente a competidores |
| `08_output_productos` | Consolida los criterios en el archivo final de productos |

### `03_models/` — estimación y proyección

| Notebook | Qué hace |
|---|---|
| `01_demanda` | Proyecta la demanda externa por producto y destino |
| `02_episodios` | Identifica los episodios de auge exportador según los criterios de Freund y Pierola |
| `03_exploracion_episodios` | Descriptivos de los episodios y construcción del marco de estimación |
| `04_estimacion_glm` | Estima el modelo de crecimiento exportador y guarda los coeficientes |
| `05_proporciones` | Proporción de productos que consolidan un auge en países comparables |
| `06_proyeccion` | Aplica los coeficientes al caso colombiano |
| `07_matriz_io` | Traduce la ganancia exportadora a producto interno bruto por rama, en agregado y por tipo de oportunidad |

### `04_report/` — cifras de los entregables

| Notebook | Qué hace |
|---|---|
| `01_priorizacion` | Ranking de industrias y macrosectores; tablas 3 y 4 del capítulo |
| `02_macro_empleo_pobreza_recaudo` | Tablas 1 y 2 del capítulo y la tabla de periodos del deck |
| `03_figuras_deck` | Las cuatro figuras de la presentación que el proyecto original no producía |

---

## Resultados

- `output/figures/deck/` — las seis figuras que consume la presentación.
- `output/tables/` — el archivo final de productos, los criterios de calidad, resiliencia,
  aranceles y localización, y las tablas de priorización en LaTeX.
- `output/model/` — el modelo lineal generalizado estimado.
- `reports/slide/` — proyecto LaTeX de la presentación, 62 páginas.
- `reports/document/` — capítulo para el BID, versiones V05 y V04.
- `reports/slide/originales/` — el material original de la presentación, fuera de la ruta de
  compilación, para contrastar contra lo que regenera la cadena: las figuras, el PDF compilado,
  el notebook que produjo `Imagen 4.png` y el borrador previo `Ajustes BID - V00.pdf`.

---

## Cómo correrlo

El proyecto está fijado a **Python 3.10** con las versiones de la época: numpy 1.26.4,
pandas 2.2.3, matplotlib 3.8.4, statsmodels 0.14.4. Un entorno nuevo con las versiones más
recientes rompe la cadena.

```bash
python3.10 -m venv .venv --prompt "nearshoring-oportunidades-colombia"
source .venv/bin/activate
pip install -e ".[dev]"
```

Antes de la primera corrida hay que traer los insumos crudos desde OneDrive:

```bash
./tools/copiar_raw.sh
```

Conviene marcar antes la carpeta de origen como *Mantener siempre en este dispositivo* en
Finder: son unos 9,5 GB y la materialización archivo por archivo es lenta.

Luego se selecciona el intérprete de `.venv` como kernel y se corren los notebooks en orden.
Para correrlos por línea de comandos:

```bash
python -m jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.kernel_name=python3 \
  notebooks/01_cleaning/01_correlativas_hs.ipynb
```

Para contrastar lo regenerado contra los artefactos del proyecto original:

```bash
python tools/verificar_migracion.py            # todos
python tools/verificar_migracion.py df_comercio  # solo los que coincidan con el filtro
```

Para recompilar la presentación:

```bash
cd reports/slide && pdflatex -interaction=nonstopmode -recorder Presentacion_Unificada_Fedesarrollo.tex
```

Los detalles de instalación, la explicación de `config.py` y las convenciones del proyecto
están en **[SETUP.md](SETUP.md)**.
