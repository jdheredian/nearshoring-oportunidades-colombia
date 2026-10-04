# Pendientes

Lo que queda por hacer y las decisiones que siguen abiertas, al cierre de la migración de
septiembre de 2026.

---

## 1. Estado de la cadena

**No queda ningún bloqueo.** Los 9,5 GB de `data/raw` están copiados y verificados byte a byte,
y los treinta y tres notebooks corrieron de punta a punta desde los datos crudos.

| Carpeta | Notebooks | Corridos |
|---|---|---|
| `00_download/` | 3 | 3 |
| `01_cleaning/` | 12 | 12 |
| `02_stats/` | 8 | 8 |
| `03_models/` | 7 | 7 |
| `04_report/` | 3 | 3 |

El deck recompila en 62 páginas, sin errores de LaTeX, sin referencias sin resolver y sin citas
sin resolver. El archivo `.fls` confirma que el compilador abre las figuras regeneradas desde
`output/figures/deck/`.

Lo que sigue pendiente no es de ejecución sino de decisión, y está en las secciones 4 y 5.

---

## 2. Dónde se archivan los datos crudos

`data/raw` pesa 9,5 GB y el `.gitignore` ya no lo versiona (ver 5.7). Hace falta decidir dónde
queda la copia de referencia y dejarlo escrito en el `README.md`, porque sin ella la cadena no
arranca. Los insumos no reproducibles son los que más importan:

| Insumo | Tamaño | Por qué no se puede volver a bajar igual |
|---|---|---|
| 28 CSV de WITS, 1995-2023 | 7,4 GB | descarga por lote con identificador de trabajo, no una URL estable |
| `Registro_Nacional_de_Despachos_de_Carga_…_20250530.csv` | 252 MB | descarga manual del portal de datos abiertos, con corte del 30 de mayo de 2025 |
| `US_TransportCosts_20212021.csv` | | llega en `.7z` y se descomprime a mano |
| CSV de medidas no arancelarias de la UNCTAD | | descarga manual |
| `indices_normalizados_20anios.xlsx` | 9 KB | método documentado, base de origen no archivada (ver 4.1) |

---

## 3. Documentos de referencia archivados

Durante la migración aparecieron dos piezas que no estaban en las carpetas del alcance original y
que resultaron decisivas. Quedan archivadas en el repositorio:

| Archivo | Dónde está ahora | Qué resolvió |
|---|---|---|
| `Ajustes BID - V00.pdf`, 20-nov-2025 | `reports/slide/originales/` | el 15% del bootstrap, el origen del índice normalizado y la fuente de `expos.png` |
| `Nearshoring Resultados Númericos - V07 - 15%.xlsx`, 28-ene-2026 | `data/raw/impacto_excel/` | las cifras de empleo, pobreza y recaudo del deck y del capítulo |

Los dos venían de `Archivos de David Gelvez - 01. CPC - Nearshoring/04. Documentos Cliente/`,
una carpeta que no estaba en la lista inicial. **Conviene revisarla entera**: tiene diez versiones
del libro de resultados y material de los tres entregables al cliente, y es el sitio más probable
donde aparezca el código que falta de `Imagen 4.png`.

---

## 4. Assets del deck — todos con productor

Eran cuatro sin productor y **las cuatro quedaron resueltas**. `Imagen 1.png` e `Imagen 2.png` se
reproducen en matplotlib desde el libro de resultados; `expos.png` desde el extracto de WITS que ya
estaba archivado; `Imagen 4.png` desde la tabla de participaciones que apareció en
`Impacto/output/deck/tablas/`. El deck ya no compila con ningún PNG del proyecto original. El
detalle está en los hallazgos 2.7, 2.13 y 2.13.1 de la auditoría.

### 4.1 `expos.png` — resuelta

La fuente estaba en el repositorio desde el principio, en
`data/raw/comentarios/3004985_1C4043D0-F/DataJobID-3004985_3004985_howExportGrows.csv`: es el mismo
extracto de exportaciones totales que alimenta el índice normalizado.
`04_report/03_figuras_deck` la regenera y el resultado es indistinguible del PNG publicado. Ver el
hallazgo 2.13.1 de la auditoría.

### 4.2 `Imagen 4.png` — resuelta

Aparecieron las dos piezas que faltaban: el notebook que la produjo, archivado en
`reports/slide/originales/pipeline_proyecciones_industrias.ipynb`, y la tabla de participaciones por
industria, `resultados_ciiu_global.xlsx`, archivada en `data/raw/modelo/`.
`04_report/03_figuras_deck` la regenera con un error absoluto medio de 0,052 puntos porcentuales
contra el original. Ver el hallazgo 2.13 de la auditoría.

**Queda una decisión menor:** la leyenda. El deck publicado rotula la quinta banda como «otros
productos químicos n.c.p.», que es el CIIU 2029 y tiene 0,95% de participación; la banda es en
realidad el CIIU 2429, «otros metales no ferrosos», con 4,02%. La versión regenerada usa el nombre
correcto y las descripciones oficiales completas de `CIIU_Clasificacion_Actualizada.xlsx`, algo más
largas que las abreviaciones del deck. Las bandas no cambian, solo el texto de la leyenda.

### 4.3 `Imagen 1.png` e `Imagen 2.png` — resueltas

Eran gráficos de Excel. La serie que las alimenta no está en la hoja `Series`, que sale vacía
del notebook, sino en la hoja `Hoja1` del mismo libro, en pesos constantes de 2015.
`04_report/03_figuras_deck` la convierte a dólares de 2024 y las reproduce en matplotlib. Los
valores extremos coinciden con el deck: 49,6 y 209,1 mil millones de dólares en exportaciones,
419,1 y 844,8 en producto interno bruto.

`Image1.png` e `Image2.png` sí quedaron resueltos: son las celdas 12 y 14 de
`1.1. Exploración de datos`, y ya están migrados en `03_models/03_exploracion_episodios` con su
`savefig`.

---

## 5. Decisiones abiertas

### 5.1 Logo del BID — resuelto

Los dos logos están visibles en las cabeceras de los treinta y un notebooks:

- Fedesarrollo: `https://fedesarrollo.org.co/logo-Fede.png`
- BID: `https://upload.wikimedia.org/wikipedia/commons/f/f9/Logo_BID_Espa%C3%B1ol.png`

Ambas URL responden. La del BID apunta a Wikimedia Commons, no a un servidor institucional del
banco: si se prefiere una fuente oficial o una copia local en `tools/logo/`, hay que
reemplazarla en las treinta y un cabeceras.

### 5.2 Determinismo de `nearest_product`

El hallazgo 2.2 de la auditoría: la función desempata con `idxmax()` sobre una lista de
candidatos construida con `set()`, cuyo orden depende de la aleatorización del hash del proceso.
Dos corridas del mismo notebook difieren en 59 de 728 filas de `Potencial Exportador Restante`.

La causa está medida: de las 5.199 filas de `df_product_space`, **1.649, el 31,7%, tienen el
máximo empatado** entre dos o más columnas una vez se descarta la diagonal. La mediana del empate
es de dos candidatos y el mayor llega a veinticuatro. Con esa densidad de empates, el orden de la
lista decide el resultado en una de cada tres consultas.

Se migró tal cual. Volverlo determinista es una línea, ordenar la lista de candidatos, pero eso
cambiaría esa columna a un tercer valor, distinto tanto del original como del que da hoy. No
alcanza a los entregables, porque la cadena de impacto no lee esa columna.

**Decisión pendiente:** ordenar la lista de candidatos y aceptar que `Output Final` cambie en
esa columna, o dejarlo como está y asumir que el repositorio no reproduce ese número dos veces
seguidas.

### 5.3 Cifras de priorización del deck — corregidas

Las dos tabulares de la lámina de priorización decían 22,34% / 16,20% / 12,38%. Se reemplazaron
por la salida vigente de `output/tables/participacion_industrias.tex`, que da 22,63% / 16,01% /
12,25%, regenerando las veinticuatro filas de las dos columnas con sus participaciones y su orden
actual. El deck vuelve a compilar en 62 páginas.

### 5.4 Las cifras macro publicadas — resuelta

El libro que reproduce las cifras publicadas no estaba en `Excel Impacto PIB/` sino en
`Archivos de David Gelvez - 01. CPC - Nearshoring/04. Documentos Cliente/02. Entregable 3 -
Recomendaciones/`, donde conviven diez versiones. La **V07 al 15%**, del 28 de enero de 2026,
reproduce el deck y el capítulo con diferencias menores a media persona. Que la V07 exista solo
al 15% confirma que ese es el escenario base. Ver el hallazgo 2.9 de la auditoría.

`04_report/02_macro_empleo_pobreza_recaudo` lee esa versión. No queda nada pendiente aquí.

### 5.5 Rótulo de los periodos — corregido en el deck, pendiente en el capítulo

El deck rotulaba los cinco tramos como periodos presidenciales, `C1: 2025--28` y siguientes, y el
capítulo como quinquenios. Ninguno de los dos corresponde a la partición real del libro V07, que es
2025-2029 seguido de cuatro tramos de cuatro años. En el deck se corrigieron los cinco rótulos a
`P1: 2025--2029` … `P5: 2042--2045` y se quitó «por periodo presidencial» del título de la lámina.

**Queda pendiente el capítulo**, que es un `.docx` y no se recompila desde la cadena: hay que
corregir a mano el rótulo de quinquenios de sus Tablas 1 y 2.

### 5.6 El 15% del bootstrap — resuelta, y la lámina corregida

`Ajustes BID - V00.pdf` documenta el diseño y el propio deck lo dice con más precisión: «tres
escenarios conservadores de éxito: conservador (10%), **base (15%)** y optimista (20%)». El 15% es
una decisión del remuestreo, no la tasa de éxito exportador, y el 30% de la hoja `Léeme` es texto
desactualizado. Ver el hallazgo 2.12 de la auditoría.

La lámina prometía que «esta proporción se utiliza posteriormente para ponderar las proyecciones
del modelo», cosa que no ocurre. **Se corrigió el texto** para que diga lo que la cadena hace: la
proporción se estima como referencia empírica, el escenario base no la aplica como ponderador, y
los intervalos salen del remuestreo del 15%.

También se corrigieron las tres tasas de éxito por país de esa lámina, que decían «México 43.2%,
Costa Rica 35.7% y República Dominicana 33.8%» y que no son las que calcula la cadena. Ahora dicen
54.4% / 20.4% / 26.6%, con el promedio de 33.8% explícito. Ver el hallazgo 2.12.0 de la auditoría.

**Queda abierto** si conectar el 33,8% a una ponderación real, que sería un cambio de método, o
dejarlo como cifra de referencia. Hoy `05_proporciones` lo calcula, lo imprime y nadie lo consume.

### 5.6.1 La segmentación del bootstrap por tipo de oportunidad

`03_models/07_matriz_io` calcula un agregado único; el método documentado segmenta por tipo de
oportunidad y el PDF reporta las tablas desagregadas. Se implementó la segmentación y **el método
reproduce dos de las tres categorías**: «a la vista» con 1,6% de diferencia y un intervalo de
confianza casi idéntico al publicado, «a profundizar» con 2,8%. «De largo alcance» queda 41% por
debajo, con intervalos disjuntos. Ver el hallazgo 2.12.1 de la auditoría.

La causa está acotada: las tres cifras publicadas suman 18,7% más que el panel completo, de modo
que las categorías publicadas se solapan mucho más de lo que permite la clasificación archivada,
donde el solapamiento es de 16 productos de 809.

**Incorporada.** `03_models/07_matriz_io` produce
`output/tables/resultados_por_tipo_oportunidad.xlsx` con las tres categorías, sus exportaciones
totales y prioritarias, su efecto sobre el producto interno bruto y los intervalos al 95%, y
contrasta cada cifra contra la publicada. Las razones son 0,97 y 0,98 en las dos primeras
categorías y 0,59 en «largo alcance», que queda documentado con su brecha.

### 5.7 El `.gitignore` — resuelto

El `.gitignore` ya excluye `data/raw`, `data/temp`, `data/processed` y `output/model`,
conservando los `.gitkeep` de los cuatro. Se añadió `output/model/.gitkeep`, que no existía.

Con esas reglas el repositorio versionable queda en **9,0 MB y 146 archivos**, sin ningún archivo
por encima de dos megabytes. Sin ellas serían 10,8 GB, casi todo `data/raw` y los 283 MB de
`glm_model.pkl`.

No se hizo `git init` ni ningún commit, según lo acordado.

### 5.8 Tamaño del repositorio — resuelto por la regla anterior

La carpeta ocupa 11 GB en disco, repartidos así:

| Carpeta | Tamaño | ¿Se versiona? |
|---|---|---|
| `data/raw` | 9,5 GB | no, se archiva aparte |
| `.venv` | 767 MB | no |
| `data/temp` | 965 MB | no, la regenera la cadena |
| `output/model/glm_model.pkl` | 283 MB | no |
| `output` sin el modelo | 3 MB | sí |
| `reports` | 3,8 MB | sí |
| `notebooks` | 1,8 MB | sí |
| `src` + `tools` | 440 KB | sí |

Ya no hace falta archivar `df_comercio.parquet` consolidado para reducir el tamaño, que era la
alternativa que se planteaba antes: el peso está fuera del control de versiones y la cadena
conserva la verificación de ese artefacto, que sale idéntico al original.

Lo que sí queda pendiente es **dónde se archivan los 9,5 GB de `data/raw`**, porque el
repositorio ya no los lleva consigo y el `README.md` tiene que decir de dónde se reponen.

---

### 5.9 Versión del potencial exportador — resuelta

La cadena lee la descarga automatizada del Export Potential Map, no los 190 archivos que se bajaron
a mano en 2025. El repositorio reproduce el portal, no lo publicado. Ver el hallazgo 2.14 de la
auditoría y la causa 2 de la sección 6.

Lo que eso mueve, medido sobre `Output Final 040725.xlsx`: los **mismos 662 productos**, con
`Margen`, `Industria`, `Industria 3digit`, `Leamer` y `Type` **idénticos en los 662**; el
`Potencial Exportador Restante` sube **7,28%** en total, con una mediana de cambio por fila del
22,6%; y cambian 12 y 48 marcas de `Tamaño de Mercado 90` y `80`, de 728. **Ninguna cifra de los
entregables se mueve**, porque la cadena de impacto solo lee `HS6`, `Margen` e `Industria 3digit`.

Para que la corrida limpia fuera comparable se le puso al descargador la bandera
`reejecutar_descarga = False`, como ya tenían los otros dos notebooks de `00_download`: sin ella,
cada corrida bajaría el portal del día y movería los resultados otra vez.

### 5.10 Cuatro de los cinco criterios de episodio no filtran nada

`03_models/02_episodios` implementa los cinco criterios de Freund y Pierola, pero los criterios 2,
3, 4 y 5 estan protegidos por `if 'anterior' in periodo`, y la asignacion de periodos solo produce
`previo`, `posterior` y `actual`. Los cuatro caen siempre por el `else`, que los marca `True`, de
modo que un episodio se conserva si y solo si cumple el criterio 1, el del 6% de crecimiento medio.
Ver el hallazgo 2.17 de la auditoria.

Queda sin aplicar, entre otros, el criterio que el paper incluye para asegurar que el auge sea
impulsado por la oferta y no por un aumento de demanda de los socios mayores.

**Decision pendiente, y es la mas de fondo que hay abierta.** Corregirlo cambiaria el conjunto de
episodios, y con el `df_para_estimacion`, el modelo lineal generalizado, las proyecciones y todas
las cifras macro de los dos entregables. Las opciones son tres:

1. Dejarlo como esta, documentado, y tratar lo que identifica la cadena como «tramos de crecimiento
   superior al 6%» en vez de auges exportadores en el sentido del paper.
2. Corregir la condicion y medir cuanto cambia: cuantos episodios sobreviven, como se mueve el
   modelo y en cuanto quedan las cifras publicadas. Con esos numeros en la mano decidir.
3. Corregirlo y rehacer los entregables.

La opcion 2 no compromete a nada y da la informacion para elegir entre la 1 y la 3. Cuesta unas dos
horas de computo, porque obliga a recorrer otra vez los 1.721.504 grupos.

---

## 6. Rediseño del scraping

La carpeta `Web Scrapping/` está vacía en disco. El material de scraping del proyecto vive en
`Archivos Extra/`:

| Archivo | Qué hace | Estado |
|---|---|---|
| `clean data transporte externo.ipynb` | Consulta con duckdb el CSV de costos de transporte de Estados Unidos y produce `df_costos_externos.parquet` | Migrado como `00_download/01_costos_transporte_eeuu`, pendiente de escribir |
| `costos_externos.sql` | Consulta SQL asociada | **Archivo vacío, cero bytes** |
| `Registro_Nacional_de_Despachos_de_Carga_por_Carretera_20250530.csv` | Descarga del portal de datos abiertos, 252 MB, del 30-may-2025 | Archivado en `data/raw/logistica/` |
| `scrapping (1).ipynb` | Raspa `isalopezgiraldo.com`, un blog de entrevistas | Ajeno al proyecto, fuera del repositorio |

Según lo acordado, esta parte hay que **volver a diseñarla**. Una parte ya se hizo:

`00_download/03_potencial_exportador_itc` sustituye los 190 archivos que se bajaban a mano del
Export Potential Map por una descarga automatizada contra la interfaz del portal, con la fecha de
descarga en el nombre del archivo. Está conectado a `01_cleaning/05_potencial_exportador`. Ver el
hallazgo 2.14 de la auditoría.

Lo que sigue pendiente de rediseño es la parte de transporte y carga.

Puntos a resolver en el rediseño:

1. El `.sql` está vacío, de modo que la consulta de duckdb que produjo los costos externos no
   se conserva en ninguna parte. Hay que reconstruirla a partir del notebook.
2. El CSV del registro de carga es una descarga manual del portal de datos abiertos. Convendría
   sustituirla por una llamada a la API con su fecha de corte explícita.
3. El CSV de costos de transporte de Estados Unidos llega comprimido en `.7z` y se descomprime a
   mano. Hay que decidir si se automatiza o se archiva.
4. Ninguno de los tres pasos deja registro de la fecha de descarga dentro del artefacto.
