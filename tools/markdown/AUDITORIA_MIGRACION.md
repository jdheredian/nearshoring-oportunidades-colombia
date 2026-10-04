# Auditoría de la migración

Migración del proyecto Nearshoring desde OneDrive a `nearshoring-oportunidades-colombia`, sobre
`project-template`. Regla de trabajo: **auditar, no arreglar**. Todo lo que se encontró se
migró tal cual y se anotó aquí. Las excepciones están marcadas como tales y justificadas.

Editor: Juan Diego Heredia Niño — jheredia@fedesarrollo.org.co
Fecha de la migración: septiembre de 2026

---

## 1. Alcance

### Entregables finales

| Entregable | Archivo de origen | Evidencia |
|---|---|---|
| Presentación | `Final/Presentacion_Unificada_Fedesarrollo.tex` | 62 páginas, `.tex` del 6-feb-2026, recompilado el 6-abr-2026. Idéntico al de `Documento/Final/`. |
| Documento | `Documento/Capitulo_Nearshoring_BID - DG & JD V05-20260319.docx` | 20-mar-2026, 2.871 palabras, cuatro tablas. |
| Documento de referencia | `Documento/Capitulo_Nearshoring_BID - DG V04-20260319.docx` | 19-mar-2026. Trae como figuras lo que V05 convirtió en las tablas 3 y 4. |

Criterio de alcance acordado: entra al repositorio todo lo necesario para reproducir cada
cifra, tabla y figura citada en esos dos documentos, aunque el `.tex` las tenga escritas a mano.

### Assets que consume la presentación

| Asset | Origen | Productor en el repositorio migrado |
|---|---|---|
| `Image1.png` | matplotlib, histograma de duración del episodio | `03_models/03_exploracion_episodios` |
| `Image2.png` | matplotlib | `03_models/03_exploracion_episodios` |
| `expos.png` | matplotlib, series de exportaciones de Colombia, Costa Rica, República Dominicana y México | `03_models/03_exploracion_episodios` |
| `Imagen 1.png` | **Excel**, exportaciones proyectadas 2025-2045 | `04_report/03_figuras_deck` (reproducida en matplotlib) |
| `Imagen 2.png` | **Excel**, producto interno bruto proyectado 2025-2045 | `04_report/03_figuras_deck` (reproducida en matplotlib) |
| `Imagen 4.png` | matplotlib, participación acumulada de la ganancia exportadora por industria | `03_models/06_proyeccion` |
| tabla de coeficientes (línea 273) | `coeficientes_regresion.tex` desde `glm_model.pkl` | `03_models/04_estimacion_glm` |
| tabla de empleo, pobreza y recaudo (línea 802) | `Excel Impacto PIB/Nearshoring Resultados Númericos - V05` | `04_report/02_macro_empleo_pobreza_recaudo` |
| tablas de priorización (líneas 909 y 930) | `participacion_industrias.tex` | `04_report/01_priorizacion` |

Verificado empíricamente con el `.fls` del compilador: `Imagen 3.png` está comentada en el
`.tex` e `Imagen 5.png` nunca se referencia. Ninguna de las dos entra al repositorio.

### Qué quedó fuera

| Carpeta | Motivo |
|---|---|
| `Extensión/analisis_transporte` | No alimenta ninguna cifra del deck ni del capítulo V05. Corresponde a la otra presentación (`Resumen Estudio Fedesarrollo BID.pptx`, 43 láminas). Decisión del usuario. |
| `Caracterización/Trabajo de Campo` | Igual que la anterior. Además lee rutas que ya no existen. |
| `Caracterización/Code + Data.zip` (1,45 GB) | Foto de junio de 2025 de la propia carpeta Caracterización. |
| `Caracterización/Nearshoring Code.zip` (875 KB) | Foto de abril de 2026 de los mismos notebooks. |
| `Archivos Extra/scrapping (1).ipynb` | Raspa `isalopezgiraldo.com`, un blog de entrevistas sin relación con el proyecto. |
| `Archivos Extra/jdheredian.github.io` | Sitio personal, ajeno al proyecto. |
| `Web Scrapping/` | Carpeta vacía en disco. Pendiente de rediseño; ver `pendientes.md`. |

---

## 2. Hallazgos que afectan resultados

### 2.1 La simulación de priorización no tiene semilla

`Impacto/Priorización/Priorización.ipynb` corre dos simulaciones Monte Carlo de mil iteraciones
que muestrean entre el 10% y el 20% de los productos de cada industria, con `np.random.uniform`
y `DataFrame.sample`, **sin fijar semilla**. Son las que producen las tablas 3 y 4 del capítulo.

Ocho corridas del mismo código dan un rango de 0,60 puntos porcentuales en la industria
principal (22,17% a 22,77%). Esto explica por qué el deck y el capítulo reportan cifras
distintas para la misma tabla:

| | Maquinaria y transporte | Equipos de potencia | Metales reciclados |
|---|---|---|---|
| Deck, compilado el 6-feb-2026 | 22,34% | 16,20% | 12,38% |
| Capítulo V05, 20-mar-2026 | 22,5% | 15,9% | 12,2% |
| Rango observado en ocho corridas | 22,17–22,77% | 15,83–16,39% | 12,00–12,23% |

Ambas cifras publicadas caen dentro del rango de la simulación. **No hubo actualización de
datos entre una y otra: es ruido de simulación.**

**Excepción aplicada:** por decisión del usuario se fijó `random_state = 20010326` en
`config.py`. El notebook queda reproducible de aquí en adelante, pero las tablas 3 y 4 del
capítulo ya no se reproducen exactamente. Con la semilla fijada:

| | Con semilla | Publicado en V05 |
|---|---|---|
| Maquinaria y transporte | 20,45 USD B · 22,63% | 20,25 · 22,5% |
| Equipos de potencia | 14,46 · 16,01% | 14,29 · 15,9% |
| Metales reciclados | 11,07 · 12,25% | 10,99 · 12,2% |
| Total macrosectores | 92,63 USD B | 93,44 |

### 2.2 `nearest_product` desempata según el orden de un conjunto

`funciones/nearest_product.py` resuelve el empate con `row.idxmax()`, que devuelve el primer
índice del máximo. La lista de candidatos que recibe se construye con `set(...) & set(...)`,
y el orden de iteración de un conjunto de cadenas depende de la aleatorización del hash del
proceso. El resultado es que **el notebook no es determinista contra sí mismo**.

Dos corridas consecutivas del mismo `02_stats/02_tamano_mercado` difieren en **59 de 728 filas**
de `Potencial Exportador Restante`, con una diferencia máxima de 55.987 miles de dólares.

Alcance verificado: el conjunto de 662 productos, y las columnas `Margen`, `Leamer` y `Type`,
son **estables entre corridas e idénticos al original**. La cadena de impacto consume de ese
archivo únicamente `HS6`, `Margen` e `Industria 3digit`, de modo que **la no determinación no
alcanza a los entregables**. Sí afecta, en cascada, a `Cutoff 90`, `Cutoff 80`,
`Tamaño de Mercado 90` (nueve productos cambian de marca) y `Tamaño de Mercado 80` (once).

La causa está en la propia matriz: de las 5.199 filas de `df_product_space`, **1.649, el 31,7%,
tienen el máximo empatado** entre dos o más columnas una vez se descarta la diagonal. La mediana
del empate es de dos candidatos y el mayor llega a veinticuatro. Con tantos empates, el orden de
la lista decide el resultado en una de cada tres consultas.

Se migró tal cual. Queda como decisión abierta en `pendientes.md`.

### 2.3 El archivo que consume la cadena de impacto tiene ediciones manuales

`Impacto/data/raw/exportaciones/productos/2 - Output Final 040725 V02 - EXT.xlsx`, del
5-mar-2026, no es la salida del notebook `7. output.ipynb`, del 4-jul-2025. Tiene siete hojas
donde el notebook produce dos, y dos columnas añadidas a mano (`Comité`, `Arancel Trump Total 2`).

Comparando la hoja `Productos únicos`, con las mismas 662 filas, difieren ocho columnas:

| Columna | Filas que difieren de 662 |
|---|---|
| `Arancel Trump Total` | 495 |
| `Cutoff 90` | 253 |
| `Cutoff 80` | 253 |
| `Potencial Exportador Restante` | 47 |
| `Tamaño de Mercado 80` | 16 |
| `Tamaño de Mercado 90` | 10 |
| `Resiliencia ND` | 4 |
| `Leamer` | 2 |

**Ninguna** de esas columnas es de las tres que leen `0. clean_data` de Impacto y
`Priorización`. Parte de la diferencia se explica por el hallazgo 2.2. El archivo se archiva
en `data/raw/` como insumo no reproducible, y el notebook `02_stats/08_output_productos`
regenera su versión de notebook en `output/tables/Output Final 040725.xlsx` para comparación.

### 2.4 El estimador de calidad divide por un denominador casi nulo

`estimate_quality` calcula `quality_normalized = quality_estimate / frontera_90`, donde
`quality_estimate` es el residuo de una regresión y por construcción tiene media cercana a
cero. Hay 355 filas donde `|frontera_90| < 1e-6`, y el cociente amplifica ahí el ruido de
punto flotante.

Sobre 5.139.564 registros, `quality_estimate` coincide con el original hasta 1,5e-11 en todos.
Las filas con diferencia mayor a 1e-6 son 132 en `quality_normalized`, 47 en `quality_ladder`
y 19 en `Decile`. No es un defecto de la migración sino inestabilidad numérica del estimador.

### 2.5 Parquets que se leen y nadie escribe

| Archivo | Lo lee | Lo escribe |
|---|---|---|
| `df_trade_share.parquet` (370 MB) | `1.1. Exploración de datos`, `1.3. Proyección` | ningún notebook |
| `df_hat_basic.parquet` | `X. bootstrap` | ningún notebook |
| `indices_normalizados_20anios.xlsx` | `Priorización` | ningún notebook |
| `ciiu3.parquet` | `7. output` | ningún notebook |

Los cuatro se archivan en `data/raw/` como insumos no reproducibles.

`df_hat_complex.parquet`, que en principio parecía un quinto huérfano, **sí es reproducible**:
se verificó que su columna `Delta_x_hat` es exactamente igual a la columna `Prediction` de
`predicciones_proyeccion.parquet`, que produce `1.3. Proyección`. Los 36.851 registros
coinciden dígito a dígito.

### 2.6 Tres versiones distintas de los costos externos de transporte

| Ubicación | Tamaño | Columnas |
|---|---|---|
| `Caracterización/raw data/df_costos_externos.parquet` | 52.930.724 B | tiene `Valor por kg`: **es una salida, no un insumo** |
| `Caracterización/data/df_costos_externos.parquet` | 60.683.235 B | salida de la corrida del notebook |
| `Archivos Extra/df_costos_externos.parquet` | 62.677.935 B | tiene `Gasto` y `KG`: **este es el insumo real** |
| `Archivos Extra/US_TransportCosts_parquet/…` | 363.971.705 B | versión previa a la agregación |

El archivo colocado en la carpeta de datos crudos de Caracterización era en realidad una
salida, y con él la cadena no corre. Se identificó y archivó el insumo correcto, con el que
`df_costos_externos.parquet` se regenera **idéntico** al original (6.297.835 filas).
La copia mal ubicada se conserva como `df_costos_externos_SALIDA_previa.parquet`.

### 2.7 Tres assets del deck no tienen quien los produzca

| Asset | Qué es | Situación |
|---|---|---|
| `expos.png` | Cuatro paneles con la serie de exportaciones de Colombia, Costa Rica, República Dominicana y México, eje rotulado `Exportaciones (1000 USD)` | **Identificada:** es la figura de la página 5 de `Ajustes BID - V00.pdf`, con el mismo pie que el deck. Su fuente son las exportaciones **totales** por país y año, de 1990 a 2025, que no están archivadas. Los extractos que sí hay solo cubren las exportaciones a Estados Unidos |
| `Imagen 4.png` | Área apilada de la participación acumulada de la ganancia exportadora, con diez industrias rotuladas con nombres CIIU a cuatro dígitos | El único `stackplot` del proyecto está en `Priorización.ipynb` y agrupa por clase de negocio, no por industria CIIU. Los colores y la estructura coinciden; el nivel de agregación no. La versión que la produjo no se conserva |
| `Imagen 1.png` e `Imagen 2.png` | Exportaciones y producto interno bruto proyectados, 2025-2045 | Son gráficos de Excel. La serie anual que los alimenta se construyó dentro del libro `Nearshoring Resultados Númericos`, no en la cadena: el notebook `2.1 Matriz IO` escribe la hoja `Series` como un marco vacío, con el índice de años y ninguna columna. **Resueltas:** la serie vive en la hoja `Hoja1` del mismo libro, en pesos constantes de 2015; `04_report/03_figuras_deck` la convierte a dólares de 2024 y reproduce ambas figuras en matplotlib |

Las dos figuras de Excel quedaron verificadas contra el original en sus valores extremos:
exportaciones de 49,6 mil millones de dólares en 2025 y 209,1 en 2045; producto interno bruto de
419,1 en 2025 y 844,8 en 2045. El deck original muestra aproximadamente 50 y 207, y 420 y 845.

`Image1.png` e `Image2.png` sí quedaron identificados: son las celdas 12 y 14 de
`1.1. Exploración de datos`, el histograma de duración del episodio y el crecimiento promedio
por duración. En el original se guardaban a mano desde la salida de celda; en la migración se
les añadió el `savefig`.

### 2.8 La hoja `Series` del libro de resultados sale vacía del notebook

`2.1 Matriz IO` construye `df_anos = pd.DataFrame({'Año': list(range(2025, 2046))}).set_index('Año')`
y lo escribe como hoja `Series`. Es un índice de veintiún años sin ninguna columna. Las series
anuales que aparecen en el libro publicado, y que alimentan dos figuras del deck, se armaron
dentro de Excel.

### 2.9 Las cifras de empleo, pobreza y recaudo salen de un libro que estaba en otra carpeta — resuelto

La tabla 2 del capítulo y la tabla de periodos del deck reportan la reducción del desempleo como
549.710, 823.419, 708.188, 295.304 y 0, que suma 2.376.621 personas.

Ninguno de los tres libros de `Excel Impacto PIB/` reproduce esas cifras: dan 1.247.408,
1.602.186 y 1.925.280 personas. El del 15% además se modificó el 19 de mayo de 2026, dos meses
después del capítulo.

**El libro correcto estaba en otra carpeta.** En
`Archivos de David Gelvez - 01. CPC - Nearshoring/04. Documentos Cliente/02. Entregable 3 - Recomendaciones/`
hay diez versiones del mismo libro, V04 a V07. La **V07 al 15%, del 28 de enero de 2026** —
anterior al deck y al capítulo— reproduce el total publicado **exactamente**: 2.376.621 personas.

Verificado columna por columna, con diferencias inferiores a media persona:

| Periodo | Desempleo | Publicado | Pobreza | Publicado | Pobreza extrema | Publicado |
|---|---|---|---|---|---|---|
| 2025-2029 | 549.710 | 549.710 | 1.134.721 | 1,1 M | 567.360 | 555 mil |
| 2030-2033 | 823.419 | 823.419 | 1.272.854 | 1,3 M | 636.427 | 636 mil |
| 2034-2037 | 708.188 | 708.188 | 894.555 | 895 mil | 447.277 | 447 mil |
| 2038-2041 | 295.304 | 295.304 | 122.518 | 123 mil | 61.259 | 61 mil |

Los acumulados del capítulo también: 2.376.621 frente a «2,4 millones», 3.424.647 frente a
«3,4 millones» y 1.712.324 frente a «1,7 millones». La única celda que no cuadra es la pobreza
extrema del primer periodo, 567.360 frente a los 555 mil publicados.

`04_report/02_macro_empleo_pobreza_recaudo` usa esa versión, archivada en
`data/raw/impacto_excel/`. La V07 solo existe al 15%, lo que confirma que ese es el escenario base.

### 2.10 Ninguno de los dos rótulos de periodo es correcto

La lámina 802 del deck rotula las filas como periodos presidenciales (`C1: 2025–28`,
`C2: 2029–32`, `C3: 2033–36`, `C4: 2037–40`, `C5: 2041–45`). La tabla 2 del capítulo rotula
exactamente los mismos valores como quinquenios (`2025-2029`, `2030-2034`, `2035-2039`,
`2040-2044`, `2045`).

Buscando la partición de la serie anual de la V07 que reproduce las cuatro cifras publicadas,
resulta que **no es ninguna de las dos**:

| Partición | Resultado |
|---|---|
| Quinquenios, como dice el capítulo | 549.710 · 1.022.122 · 735.198 · 69.591 · 0 |
| Periodos presidenciales, como dice el deck | 347.029 · 825.503 · 758.491 · 432.321 · 13.276 |
| **2025-2029 · 2030-2033 · 2034-2037 · 2038-2041 · 2042-2045** | **549.710 · 823.419 · 708.188 · 295.304 · 0** |
| Publicado en ambos entregables | 549.710 · 823.419 · 708.188 · 295.304 · 0 |

La partición real es de cinco años y luego cuatro, cuatro, cuatro y cuatro. **Los dos entregables
rotulan mal sus propios números.** La cadena migrada usa la partición que sí los reproduce y deja
la etiqueta como parámetro.

### 2.11 `CIIU-complementado.xlsx` está completado a mano

El notebook `0. clean_data` de Impacto construye la correspondencia entre la clasificación
industrial y las ramas de la matriz insumo-producto cruzando por la columna `Descripción` contra
el cuadro 8 de la matriz. Ese cruce solo resuelve **69 de las 715 filas**; las otras 646 están
completadas a mano en Excel, que es lo que significa el nombre del archivo.

La celda que lo escribe tiene `execution_count = None` en el notebook original: nunca llegó a
ejecutarse. La cadena siempre consumió el archivo completado a mano, no el regenerado.

Al migrar se redirigió la escritura a `data/temp` para no mutar el crudo, y eso rompió la cadena
hasta que se detectó: el paso siguiente leía el regenerado y producía 715 filas en vez de 499.
Verificado en ambos sentidos:

| Fuente del archivo | Filas de `df_ciiu_mio` | Idéntico al original |
|---|---|---|
| `data/raw/ciiu/CIIU-complementado.xlsx` (a mano) | 499 | **sí** |
| `data/temp/pib/CIIU-complementado.xlsx` (regenerado) | 715 | no |

En el repositorio migrado la celda que regenera se conserva, porque documenta cómo se sembró el
archivo, pero escribe a `data/temp` y está marcada como no consumida. El paso siguiente lee de
`data/raw`.

### 2.12 El 15% del bootstrap está documentado; el 33,8% que estima la cadena no se usa

**El propio deck ya lo dice**, en la lámina del bootstrap: «Se definen tres escenarios
conservadores de éxito: conservador (10%), **base (15%)** y optimista (20%), que representan la
fracción de productos que materializan un crecimiento sostenido». El 15% es el escenario base,
escrito con esa palabra, y eso confirma por una vía independiente la conclusión del hallazgo 2.9,
donde la V07 existe solo al 15%.

`Ajustes BID - V00.pdf`, del 20 de noviembre de 2025, lo repite en forma de algoritmo: «Para cada
iteración b = 1, …, 1000: **1. Se remuestrea el 15% de los datos originales.** 2. Se segmenta la
submuestra por tipo de oportunidad. 3. Se calculan métricas independientes para cada categoría».

Es decir, el 15% es una decisión de diseño del remuestreo y no la tasa de éxito exportador. Eso
deja tres cifras distintas circulando:

| Cifra | Dónde aparece | Uso |
|---|---|---|
| 15% | `Ajustes BID - V00.pdf` y el bootstrap de `07_matriz_io` | **es la que se usa** |
| 10% y 20% | nombres de archivo de los libros de resultados | escenarios alternativos |
| 30% | hoja `Léeme` de todos los libros, incluida la V07 | texto desactualizado, contradice el nombre del propio archivo |
| 33,8% | lo estima `05_proporciones` promediando Costa Rica, México y República Dominicana | **se calcula, se imprime y no se usa** |

La lámina del deck sobre el porcentaje de éxito exportador promete que «esta proporción se
utiliza posteriormente para ponderar las proyecciones del modelo». No ocurre: el bootstrap
remuestrea el 15% fijo.

### 2.12.0 Las tasas de éxito por país del deck no son las que calcula la cadena

La lámina del porcentaje de éxito exportador reporta «México 43.2%, Costa Rica 35.7% y República
Dominicana 33.8%». `03_models/05_proporciones` calcula otras tres:

| País | Deck | Cadena | Productos con episodio / productos |
|---|---|---|---|
| Costa Rica | 35,7% | **20,43%** | 697 de 3.411 |
| México | 43,2% | **54,44%** | 2.485 de 4.565 |
| República Dominicana | 33,8% | **26,56%** | 917 de 3.452 |
| Promedio | — | **33,81%** | |

Ninguna de las tres coincide, y el orden entre países tampoco: para el deck México supera a Costa
Rica por ocho puntos, para la cadena por treinta y cuatro.

Llama la atención que el 33,8% que el deck atribuye a República Dominicana sea exactamente el
**promedio de los tres** que produce la cadena. O el rótulo del deck está corrido, o las cifras
vienen de una corrida anterior y la coincidencia es casual. No hay forma de distinguirlo con el
material archivado.

Ninguna de estas cifras alimenta nada: el bootstrap remuestrea el 15% fijo.

**Corregido en el deck.** La lámina pasa a decir «México 54.4%, Costa Rica 20.4% y República
Dominicana 26.6%, con un promedio de 33.8%», que es lo que produce la cadena. Se añadió el promedio
de forma explícita para que el 33,8%, que es la cifra que `05_proporciones` calcula y que circulaba
atribuida a República Dominicana, quede identificado por lo que realmente es.

### 2.12.1 El bootstrap no segmenta por tipo de oportunidad; al implementarlo, dos de tres cuadran

El método documentado tiene tres pasos y `03_models/07_matriz_io`, que es el notebook que se
conserva del original, solo hace el primero y el tercero: calcula un agregado único y no segmenta.
El paso que falta es «2. Se segmenta la submuestra por tipo de oportunidad», y el documento reporta
los resultados desagregados que ningún notebook produce.

La segmentación **ya está implementada** en el notebook: la clasificación sale de
`df_productos.parquet`, que codifica las categorías múltiples como etiquetas compuestas unidas por
`" - "`; al expandirlas, las 809 filas se vuelven 829 asignaciones sobre 809 productos únicos, que
reparten 523 a profundizar, 205 de largo alcance y 101 a la vista. La salida es
`output/tables/resultados_por_tipo_oportunidad.xlsx`. Mil iteraciones, remuestreo del 15%, en miles
de millones de pesos de 2015:

| Categoría | Exportaciones | Publicado | IC 95% propio | IC 95% publicado |
|---|---|---|---|---|
| A profundizar | 225.963 | 232.474 | 208.720 – 243.291 | 215.038 – 249.419 |
| A la vista | 30.386 | 30.885 | 25.561 – 36.027 | 25.433 – 37.370 |
| De largo alcance | 57.215 | 97.053 | 50.580 – 65.049 | 72.198 – 140.789 |

| Categoría | Exp. prioritarias | Publicado | PIB | Publicado |
|---|---|---|---|---|
| A profundizar | 78.776 | 81.786 | 209.328 | 214.750 |
| A la vista | 13.797 | 14.049 | 28.191 | 28.655 |
| De largo alcance | 26.100 | 36.329 | 53.129 | 88.565 |

**El método es el correcto.** «A la vista» reproduce la media con 1,6% de diferencia y su intervalo
de confianza coincide casi punto por punto con el publicado. «A profundizar» queda 2,8% por debajo,
con intervalos que se solapan en casi toda su extensión.

**«De largo alcance» no es ruido de simulación:** los dos intervalos son disjuntos y el propio es
tres veces más estrecho, ±13% frente a ±35%. Esa categoría, en la versión publicada, es a la vez
más grande y mucho más dispersa.

La causa está en la pertenencia, no en el cálculo, y se puede acotar con una suma. Las tres cifras
publicadas suman 360.412, que es **18,7% más que el total del panel completo al 15%**, 303.671. Es
decir, las categorías publicadas se solapan: hay productos contados en más de una. En la
clasificación archivada el solapamiento es de apenas 16 productos de 809, y las tres categorías
suman 3,4% por encima del panel. Se probaron las cuatro fuentes de clasificación disponibles
—`Productos únicos`, `Productos completos`, `Prod. priorizados` y AmCham— y ninguna reparte de otro
modo: las tres primeras dan exactamente la misma pertenencia.

Para que «largo alcance» llegara a 97.053 tendría que abarcar el 32% del choque total del panel, en
vez del 19% que abarca hoy, sin que «a profundizar» se reduzca. Esa clasificación no está en el
material migrado.

### 2.12.2 El origen de `indices_normalizados_20anios.xlsx` ya estaba en el deck

Para Colombia, México, República Dominicana y Costa Rica se toman las exportaciones totales
anuales, se normalizan a base 1 dividiendo por el primer año de cada ventana móvil de veinte años,
y se promedian todas las ventanas de todos los países período a período.

Ese método **no es un hallazgo del PDF**: el deck final ya lo trae completo, con la transformación
a base 1, las ventanas móviles y la promediación, en las láminas de la senda de crecimiento. El
PDF es la versión previa de esas mismas láminas.

Lo que sigue faltando es el dato: la base de exportaciones totales por país y año, de 1990 a 2025,
**no está archivada en el material migrado**. El índice entra como insumo no reproducible.

### 2.13 `Imagen 4.png` queda reproducible, y el deck tiene un rótulo equivocado

La figura se reconstruyó por completo. Hicieron falta dos piezas que estaban en carpetas fuera del
alcance inicial.

**El código** está en `reports/slide/originales/pipeline_proyecciones_industrias.ipynb`. La
identificación es firme: la paleta de diez colores es píxel a píxel la del PNG, y coinciden
`figsize=(12,11)`, `xlim(0,19)`, los `xticks` de dos en dos, `alpha=0.9`, la leyenda a dos columnas
en `bbox_to_anchor=(0.5,-0.12)` y los dos rótulos de eje. Lo esencial de ese notebook es que **no
calcula las participaciones por industria: las lee**, y con ellas reparte la trayectoria del índice
normalizado.

**La tabla de participaciones** está en `Impacto/output/deck/tablas/resultados_ciiu_global.xlsx`,
hoja `Todos_CIIU`: 128 industrias CIIU con una columna `Share` que suma exactamente 1. Se archivó en
`data/raw/modelo/`. Es el único archivo de todo el proyecto con una columna `Share` junto a códigos
CIIU.

#### Verificación

La figura regenerada se contrastó contra `reports/slide/originales/Imagen 4.png` midiendo la altura
de cada banda por color y normalizando por el total, que es una comparación independiente de la
escala y del tamaño del PNG:

| Banda | Original | Regenerada | Tabla `Share` |
|---|---|---|---|
| 0311 Pesca marítima | 24,22% | 24,15% | 24,16% |
| 2910 Vehículos automotores | 12,78% | 12,71% | 12,64% |
| 2410 Hierro y acero | 10,63% | 10,60% | 10,66% |
| 2610 Componentes electrónicos | 9,47% | 9,51% | 9,44% |
| 2429 Otros metales no ferrosos | 8,58% | 8,50% | 8,63% |
| 3110 Muebles | 8,22% | 8,25% | 8,23% |
| 1921 Refinación del petróleo | 7,42% | 7,49% | 7,43% |
| 2011 Químicos básicos | 7,15% | 7,24% | 7,34% |
| 1012 Pescado y crustáceos | 7,15% | 7,15% | 7,12% |
| 0510 Hulla | 4,38% | 4,42% | 4,36% |

**Error absoluto medio 0,052 puntos porcentuales, máximo 0,087**, que es ruido de medición de
píxel. Las diez industrias y su orden coinciden.

#### El deck rotula mal la quinta banda

El deck publicado llama a la banda naranja «Fabricación de otros productos químicos n.c.p. (no
clasificados previamente)», que es el CIIU 2029. No puede serlo: en la tabla que alimenta la figura,
**2029 tiene una participación de 0,95%**, muy lejos del 4% que mide esa banda. La industria que
corresponde es **2429, «Industrias básicas de otros metales no ferrosos», con 4,02%**.

La versión regenerada usa el nombre correcto, tomado de `CIIU_Clasificacion_Actualizada.xlsx`, que
es la tabla de nomenclatura del propio proyecto. Los otros nueve rótulos también salen de ahí y son
las descripciones oficiales completas, algo más largas que las abreviaciones que usó el deck: dicen
«hierro y **de** acero» y «vehículos automotores **y sus motores**». La figura no cambia; cambia el
texto de la leyenda.

#### Una advertencia sobre la tabla de participaciones

`Todos_CIIU` no es una participación sobre el panel: es **la suma de las tres hojas segmentadas por
tipo de oportunidad** de `resultados_exportaciones_por_ciiu.xlsx`, y hay industrias que aparecen en
varias. El CIIU 0311 está en las tres, con 3.262 + 850 + 22.954 = 27.066, que es exactamente su
`Promedio` en la tabla global.

El efecto es grande: **sobre el panel completo, pesca marítima pesa 3,97%**, no 11,27%. Los veinte
productos de esa industria suman 28.865.366 de los 726.489.591 de `Delta_x_hat`. El 11,27% resulta
de contarla tres veces.

La industria no es ajena a la cadena: el CIIU 0311 está en `df_ciiu_mio`, mapeado al sector A03 de
la matriz insumo-producto, y sus veinte productos entran al panel de proyección por la vía de
AmCham. Lo que no ocurre es que esté entre los 662 productos priorizados de
`2 - Output Final 040725 V02 - EXT.xlsx`, que es el universo con el que trabaja la caracterización.
Por eso la priorización por clase de negocio, que se apoya en ese archivo, deja a «pesca y
acuicultura» en 0,65% con tres productos, mientras la figura la pone primera con 11,27%.

La figura se reproduce tal como se publicó, que es lo que se pidió. El sesgo queda anotado aquí
porque afecta a la lectura de esa lámina: la industria que domina el gráfico lo hace por un artefacto
del conteo, no por su peso en la proyección.

### 2.13.1 `expos.png` queda reproducible, y su fuente estaba en el repositorio

La figura son cuatro paneles con la serie anual de exportaciones totales de Colombia, Costa Rica,
República Dominicana y México. Ningún notebook del proyecto la producía, y los únicos extractos de
los tres países de comparación que se conocían estaban filtrados a `PartnerISO3 == 'USA'`, de modo
que cubrían entre el 42% y el 76% de los totales publicados.

La fuente real es **el mismo extracto de WITS que alimenta el índice normalizado**, que ya estaba
archivado en `data/raw/comentarios/3004985_1C4043D0-F/`: exportaciones totales hacia el agregado
mundial, con `ProductCode = Total`, `PartnerISO3 = WLD` y `TradeFlowName = Export`.

Tres señales confirman que es esa y no otra fuente:

- Los títulos de los paneles están en inglés, «Dominican Republic» y «Mexico», que es exactamente
  como viene el campo `ReporterName` del archivo.
- El eje vertical dice «Exportaciones (1000 USD)», que es la unidad del campo
  `TradeValue in 1000 USD`.
- El panel dominicano muestra el hueco de 1998 a 2000 con la línea saltando de 1997 a 2001, que es
  la misma discontinuidad que obliga a construir las ventanas del índice por posición y no por
  calendario.

La cobertura coincide país por país: Colombia 1991-2024, Costa Rica 1994-2024, República Dominicana
1996-2024 con 26 observaciones, México 1990-2024. La figura regenerada por
`04_report/03_figuras_deck` es indistinguible de la publicada.

### 2.14 El potencial exportador pasa de archivos descargados a mano a una descarga automatizada

Hasta esta versión, `01_cleaning/05_potencial_exportador` leía 190 archivos de valores separados
por comas que alguien bajó a mano del Export Potential Map del Centro de Comercio Internacional.
No traían fecha de descarga ni forma de reproducirlos.

El notebook `00_download/03_potencial_exportador_itc` los sustituye consultando la interfaz del
portal directamente. Las respuestas vienen cifradas con AES de 128 bits en modo CBC, con la clave
ofuscada en el JavaScript del sitio.

**Efecto sobre el insumo:**

| | Archivos a mano | Descarga automatizada |
|---|---|---|
| Filas | 171.024 | 176.557 |
| Mercados de destino | 189 | 188 |
| Productos HS6 | 1.224 | 1.268 |
| Potencial total, miles de dólares | 33.754.925 | 37.189.644 |

El aumento del 10,2% es una revisión de las estimaciones del portal, no un error de empalme: de
las 161.259 combinaciones comunes, la mediana de la diferencia es de 0,20 miles de dólares.

Dos ajustes de nomenclatura fueron necesarios. El portal escribe `Chinese Taipei` y
`Hong Kong, China` donde la tabla ISO dice `Taipei, Chinese` y `Hong Kong SAR`; sin equivalencia
esos dos mercados se perdían. Y añade dos mercados que los archivos anteriores no tenían, Bután y
San Pedro y Miquelón, que la tabla ISO tampoco lista.

**Efecto sobre la cadena**, medido sobre `Output Final`:

| Columna | Resultado |
|---|---|
| Conjunto de 662 productos | **idéntico** |
| `Margen`, `Leamer`, `Type`, `CIIU`, `Industria 3digit` | **idénticas** |
| `Calidad Total`, `Arancel Total`, `Transporte Total` | **idénticas** |
| `Potencial Exportador Restante` | cambia en las 662 filas, diferencia máxima 174.995 |
| `Tamaño de Mercado 90` | doce productos cambian de marca |
| `Tamaño de Mercado 80` | cuarenta y cuatro productos cambian de marca |

Las tres columnas que consumen `0. clean_data` de Impacto y la priorización —`HS6`, `Margen` e
`Industria 3digit`— son idénticas, de modo que **el cambio no alcanza a los entregables**.

Los 190 archivos originales se conservan en `data/raw/potencial_exportador/country_data/`, y la
versión del notebook que los leía quedó verificada como idéntica al artefacto original antes de
sustituirla.

---

### 2.15 La numeración de los notebooks invertía una dependencia real

La corrida limpia, con `data/temp` y `data/processed` vacías, se detuvo en
`02_stats/09_exploracion_episodios`: leía `df_surge_vars_6.parquet`, que produce
`03_models/02_episodios`, un notebook que corría **después**. Con las carpetas pobladas de corridas
anteriores el error no aparecía, porque el archivo ya estaba en disco.

El notebook además no es solo descriptivo: escribe `df_para_estimacion.parquet`, que es lo que
consume el modelo lineal generalizado. La cadena real es

> `02_episodios` → `exploracion_episodios` → `estimacion_glm`

y la numeración la tenía al revés.

**Excepción de migración, porque el código no corre de otro modo.** El notebook se movió de
`02_stats/09_exploracion_episodios` a `03_models/03_exploracion_episodios` y los cuatro siguientes
de esa carpeta se corrieron un número:

| Antes | Ahora |
|---|---|
| `02_stats/09_exploracion_episodios` | `03_models/03_exploracion_episodios` |
| `03_models/03_estimacion_glm` | `03_models/04_estimacion_glm` |
| `03_models/04_proporciones` | `03_models/05_proporciones` |
| `03_models/05_proyeccion` | `03_models/06_proyeccion` |
| `03_models/06_matriz_io` | `03_models/07_matriz_io` |

El contenido de los cinco no se tocó. `02_stats` queda con ocho notebooks y `03_models` con siete.

Este hallazgo es el argumento a favor de correr la cadena en limpio: `tools/correr_cadena.sh` borra
`data/temp` y `data/processed` antes de empezar, precisamente para que una dependencia así no pueda
esconderse detrás de un artefacto viejo.

### 2.16 Una guarda de existencia de archivo impedia que el notebook se ejecutara

`03_models/02_episodios` envolvia todo su calculo en

```python
archivo = temp / 'exportaciones' / temp / 'exportaciones' / 'df_surge_vars_6.parquet'
if not os.path.exists(archivo):
    ...  108 lineas: la identificacion de episodios ...
else:
    print(f"El archivo {archivo} ya existe. No se ejecuta el procedimiento.")
    df_surge_vars = pd.read_parquet(archivo)
```

Mientras `data/temp` conservara el parquet de una corrida anterior, el notebook imprimia «ya
existe» y seguia de largo. **Es el mecanismo que mantuvo escondida la inversion de dependencias
del hallazgo 2.15 durante toda la migracion**: el notebook nunca se ejecutaba de verdad, asi que
nunca se descubria que su insumo lo produce un notebook posterior.

La primera ejecucion genuina, en la corrida limpia, tardo **115 minutos**, el 85% de los 136
minutos de la cadena completa. El bucle recorre **1.721.504 grupos** de origen, destino y producto,
y por cada uno hace un `sort_values`, un `set_index`, dos busquedas de extremo, un `reset_index` y
varios `query`.

En la misma linea habia un segundo defecto: **la ruta aparecia duplicada**,
`temp / 'exportaciones' / temp / 'exportaciones' / ...`, en el `archivo` y en el `to_parquet`.
Funcionaba por accidente, porque en `pathlib` dividir por una ruta absoluta descarta lo anterior.

**Se quito la guarda**, se corrigio la ruta duplicada dejando una sola definicion, `archivo_salida`,
y se borro el `import os`, que era su unico uso en el notebook.

El cambio es demostrablemente inerte: al desindentar el cuerpo del `if` y compararlo contra el
original de OneDrive, **las 108 lineas coinciden una a una** y la unica diferencia es el destino
del `to_parquet`, que pasa de un nombre relativo en el directorio de trabajo a la ruta del
proyecto. No hay forma de que cambie un solo numero.

Se reviso el resto del repositorio en busca de guardas equivalentes y no hay mas. Los dos
`glob.glob` de `01_cleaning/06_aranceles_ntms` y `01_cleaning/10_exportaciones_impacto` listan
archivos de entrada, no saltan trabajo, y el `_aptos.exists()` de `config.py` es la tipografia
opcional.

### 2.17 Cuatro de los cinco criterios de episodio no filtran nada

Los criterios que implementa `03_models/02_episodios` son los cinco de Freund y Pierola, pero
**solo el primero discrimina**. Los otros cuatro estan protegidos por una condicion que nunca se
cumple:

```python
df_prueba['periodo'] = np.where(df_prueba['anio'] < min_year, 'previo',
                        np.where(df_prueba['anio'] > max_year, 'posterior', 'actual'))
...
if 'anterior' in df_prueba['periodo'].unique().tolist():   # nunca es cierto
    ...  evaluar el criterio ...
else:
    df_prueba['criterioN'] = True                          # siempre se toma esta rama
```

La asignacion solo produce `previo`, `posterior` y `actual`; la palabra `anterior` no se genera
jamas. La consulta aparece cuatro veces, una por cada uno de los criterios 2, 3, 4 y 5, y las
cuatro caen por el `else`, que los marca `True`. Como el filtro final exige
`[['criterio1', ..., 'criterio5']].sum(axis=1) == 5`, un episodio se conserva si y solo si cumple
el criterio 1.

Traducido a lo que dice el paper, cuyo detalle esta en `reports/literature/referencias.ris`, el
unico criterio vivo es el (a), crecimiento real medio superior al 6%. Quedan sin aplicar:

| Criterio | Que deberia exigir | Que hace el codigo |
|---|---|---|
| (b) aceleracion | que el crecimiento suba un tercio y al menos 3 puntos porcentuales | siempre `True` |
| (c) origen de oferta | que suba la participacion en los cinco mercados mayores | siempre `True` |
| (d) persistencia | que el minimo posterior supere el maximo previo | siempre `True` |
| (e) sin un solo anio fuerte | que el crecimiento sin el mejor anio siga siendo superior | siempre `True` |

El criterio (c) es justamente el que Freund y Pierola incluyen para asegurar que el episodio sea
**impulsado por la oferta y no por un aumento de demanda de los socios mayores**, que es el
proposito declarado del filtro. Sin el, lo que identifica la cadena no son auges exportadores en
el sentido del paper, sino tramos de crecimiento superior al 6%.

Se migro tal cual, sin tocarlo. Queda como decision abierta en `pendientes.md`.

## 3. Reproducibilidad

### 3.1 Rutas absolutas a carpetas que ya no existen

| Ruta referenciada | Estado |
|---|---|
| `OneDrive-Fedesarrollo/Nearshoring/…` | no existe |
| `OneDrive-Fedesarrollo/Notebooks Nearshoting/…` | no existe (hay una copia en `Archivos Extra/`) |
| `OneDrive-Fedesarrollo/Notebooks Impacto/…` | no existe |
| `OneDrive-Fedesarrollo/Archivos de David Gelvez - 01. CPC - Nearshoring/04. Documentos Cliente/…` | no existe en esa ruta |
| `/Users/juandiegoheredianino/Documents/df_costos_externos.parquet` | no existe |

El `.fls` de la presentación muestra además que se compiló desde
`OneDrive-Fedesarrollo/Nearshoring/Deck/Final/`, ruta que tampoco existe.

Todas se reemplazaron por `from config import ...`.

### 3.2 Celdas que nunca se ejecutaron en el estado guardado

`Caracterización/0. clean_data.ipynb` tiene once de veinticinco celdas de código con
`execution_count = None`, entre ellas la del potencial exportador. `Impacto/0. clean_data.ipynb`
tiene la mayoría. El notebook, tal como quedó guardado, **no corre de principio a fin**.

### 3.3 Convenciones de ruta mezcladas dentro del mismo notebook

`Impacto/0. clean_data.ipynb` usa tres formas distintas en el mismo archivo: `raw / 'pib' / …`,
`"raw data/pib/…"` y `"data/…"`. Nueve copias idénticas de `paths.yml` repartidas por el
proyecto original.

### 3.4 Escrituras a carpetas que el notebook nunca crea

`análisis excel/`, `outputs/calidad/otros países/`, `df_products/caracterizado/`. Funcionaban
solo porque las carpetas ya existían. Se añadió `mkdir(parents=True, exist_ok=True)` antes de
cada exportación.

### 3.5 Insumos vivos que se descargaban en tiempo de ejecución

| Insumo | Fuente | Tratamiento |
|---|---|---|
| Deflactor del PIB de Estados Unidos | serie `GDPDEF` de FRED, vía `pandas_datareader` | Archivado con su fecha de descarga (25-ago-2025). El proveedor revisa el histórico hacia atrás. |
| Códigos ISO de país | `iban.com/country-codes`, raspado con `read_html` | Archivado (30-jul-2025). |
| Correspondencia ISO con WITS | `wits.worldbank.org`, raspado con `read_html` | Archivado (30-jul-2025). |

Los tres viven en `data/raw/descargas/`. Los notebooks `00_download/01` y `00_download/02`
conservan el código de descarga tras una bandera `reejecutar_descarga`, que queda en falso.

---

## 4. Código muerto y duplicado

| Hallazgo | Detalle |
|---|---|
| `list_distancias` | `1. caracterizacion.ipynb` recorre todos los pares producto-vecino llamando a `find_distance`, guarda el resultado en una lista y **nunca la usa**. Se eliminó; con ello `funciones/find_distance.py` queda sin consumidores. |
| `df_comercio` en AmCham | `Productos AmCham.ipynb` carga la base de comercio completa y no la usa. Se eliminó la lectura. |
| `1.2.2. Proporciones` | Lee un parquet y no escribe ningún archivo; solo imprime tres proporciones. |
| Notebooks duplicados | `analysis.ipynb` frente a `analysis-MacBook Air de Juan Diego.ipynb`; `3. largo_alcance.ipynb` frente a `3. largo_alcance 055.ipynb`. |
| `funciones/` triplicada | En `Caracterización/`, en `Caracterización/funciones/` y en `Archivos Extra/Notebooks Nearshoting/funciones/`, con contenidos distintos entre sí. |
| Módulos sin consumidor | `distancia_ciudades.py` y `leiden_communities.py` solo existen como `.pyc` o en la copia de `Notebooks Nearshoting`; ningún notebook en alcance los importa. |
| `costos_externos.sql` | Archivo de cero bytes. |
| `CIIU 3 control` | En `1.1. Exploración de datos` la variable se asigna tres veces seguidas; las dos primeras quedan sobrescritas sin haberse usado. Se migraron tal cual. |
| Figuras sin consumidor | `1. caracterizacion` produce cinco figuras, `2. tamano_mercado` una, `3. calidad` tres, `5.1` una y `6. localizacion` dos. Ninguna aparece en el deck ni en el capítulo. Se eliminaron en el recorte. |
| Bloques repetidos | La concatenación del potencial exportador aparece cuatro veces en `2. tamano_mercado`; el bloque de ventaja arancelaria dos veces en `5.1`; el del criterio 4 de calidad cuatro veces en `3. calidad`; el de la CIIU dos veces entre `0. clean_data` y `ciiu1996`. Todos se convirtieron en funciones con tabla de parámetros. |

### Defectos lógicos que se migraron tal cual

| Defecto | Dónde | Efecto |
|---|---|---|
| `arr_can` se asigna dos veces seguidas, con `Table 2` y luego con `Table 3` | `Productos AmCham.ipynb` | Las partidas de `Table 2` nunca entran al conjunto. |
| `tuple_margen` conserva el valor de la iteración anterior cuando un producto no cae en ninguna de las dos condiciones | `1. caracterizacion`, `Productos AmCham` | Puede duplicar la clasificación de otro producto. |
| Comentario contradictorio | `ciiu1996.ipynb` filtra `Año <= 1996` y el comentario dice "Filtra hasta 2012 inclusive" | Ninguno sobre el resultado. |

---

## 5. Cambios que introduce la migración

Cada uno está comentado en el punto del notebook donde aparece.

| Cambio | Motivo | Efecto sobre los números |
|---|---|---|
| **Excepción.** `pd.to_numeric(df_totpart['Año'], errors='coerce')` en `01_cleaning/01_correlativas_hs` | El archivo DIRPEN se actualizó el 4-ago-2025, un día después de la última corrida, y dejó un valor `'z'` en la subpartida 0102100000. Sin la coerción la comparación `str <= int` aborta y el código no corre. | Ninguno: los dos `df_ciiu` salen **idénticos** a los originales. |
| **Excepción por rendimiento.** En `03_models/01_demanda` el bucle de proyección agrupa una vez por destino y producto en vez de filtrar el panel completo en cada vuelta | El original ejecutaba `df_trade.loc[(df_trade["d_iso3"] == dest) & (df_trade["hs6_1996"] == prod)]` dentro del bucle, sobre 15.575.422 filas. Medido: 801 ms por vuelta × 52.585 vueltas = **11,7 horas solo en filtrar**. Una primera corrida se agotó a las 8 horas sin terminar. Agrupar por esas dos columnas produce exactamente los mismos subconjuntos. | Ninguno: `df_m_forecast_6_8_25.parquet` sale **idéntico**, 718.888 filas, y el notebook pasa de más de 8 horas a **25 segundos**. |
| **Excepción.** Los 28 archivos de WITS se filtran uno por uno en vez de concatenarse | Son 7,4 GB de texto y la máquina tiene 16 GB de memoria: concatenarlos no cabe. Cada archivo contiene exactamente un año, y tanto el `groupby` de `TotalTradeValuePerPartner` como el `drop_duplicates` agrupan por `Year`, de modo que ninguno cruza archivos. | Ninguno: `df_comercio.parquet` sale **idéntico**, 15.575.422 filas. |
| **Excepción.** `df_potencial['HS6'].fillna(df_potencial['Code'])` en `01_cleaning/05_potencial_exportador` | La celda original nunca se ejecutó en su estado guardado y aborta: los códigos de cuatro dígitos y los terminados en `XX` no tienen correspondencia en HS 2017 y quedan nulos. | Ninguno: `potencial_exportador.parquet` sale **idéntico**, 171.024 filas. |
| `CIIU-complementado.xlsx` pasa a escribirse en `data/temp/` | El original escribía dentro de `data/raw`, mutando el archivo crudo en cada corrida. | Ninguno: misma computación, otra ubicación. |
| `Imagen 1.png` e `Imagen 2.png` pasan de Excel a matplotlib | Decisión del usuario. | **Dos láminas del deck cambian de aspecto.** Los datos que las alimentan son los mismos. |
| `random_state = 20010326` en la simulación de priorización | Decisión del usuario. Ver hallazgo 2.1. | **Las tablas 3 y 4 del capítulo cambian** en 0,1 a 0,8 puntos. |
| `savefig` explícito en las figuras del deck | En el original se guardaban a mano desde la salida de celda. | Ninguno. |
| `mkdir(parents=True, exist_ok=True)` antes de cada exportación | Ver 3.4. | Ninguno. |
| `paths.yml` y rutas absolutas reemplazadas por `from config import …` | Ver 3.1 y 3.3. | Ninguno. |
| Salidas de texto desmedidas recortadas con `tools/recortar_salidas.py` | `03_models/02_episodios` imprime una línea por cada combinación de producto, origen y destino: 23.313 bloques y 23 MB dentro del `.ipynb`. Se conservan las primeras y últimas veinte líneas y se marca cuántas se omitieron. El código no se toca. | Ninguno: el notebook pasa de 26,1 MB a 0,1 MB. |
| Tipografía Aptos registrada pero **no** fijada como familia global | Las figuras del deck se produjeron con la tipografía por defecto de matplotlib; fijar Aptos las cambiaría de aspecto. | Ninguno. |
| Entorno fijado a Python 3.10 con numpy 1.26.4, pandas 2.2.3, matplotlib 3.8.4 | Decisión del usuario: reproducir el entorno de la época. | Ninguno observado. |

---

## 6. Verificación

El comparador es `tools/verificar_migracion.py`. Para cada artefacto regenerado contrasta forma,
columnas, tipos y diferencia máxima por columna numérica contra el original en OneDrive. El
manifiesto cubre **56 artefactos**, entre parquets y libros de Excel.

### La corrida en limpio

Los resultados de abajo no vienen de una cadena que se fue acumulando, sino de una **corrida desde
cero**: `tools/correr_cadena.sh` vacía `data/temp` y `data/processed`, conservando solo los
`.gitkeep`, y corre los treinta y tres notebooks en orden desde `data/raw`. Es la prueba de que no
queda ninguna dependencia escondida detrás de un artefacto viejo.

**Los treinta y tres corrieron sin un solo fallo, en 136 minutos.** El reparto del tiempo es muy
desigual: `03_models/02_episodios` se lleva **115 minutos, el 85% del total**, por los 1.721.504
grupos que recorre; `01_cleaning/04_calidad` ocho minutos; `02_stats/03_calidad` y
`01_cleaning/08_logistica` unos dos cada uno; los veintinueve restantes por debajo de noventa
segundos.

El resultado más importante de esa corrida es que **`df_surge_vars_6.parquet` sale IDÉNTICO**,
548.103 filas por 10 columnas, la primera vez que se calcula de verdad desde que empezó la
migración: hasta ahora la guarda del hallazgo 2.16 lo leía de disco sin recalcularlo. Y con él sale
idéntica toda la cadena de modelos aguas abajo.

| Resultado | Artefactos | Lectura |
|---|---|---|
| **Idénticos** | 31 | byte a byte en contenido |
| **Iguales salvo punto flotante** | 3 | diferencia máxima 2,7e-12 en `df_hhi`; 1,7e-07 en `predicciones_proyeccion` y `df_hat_complex`, con cero filas por encima de 1e-06 en 36.851 |
| **Iguales salvo el orden de filas** | 1 | `df_products_caracterizado`, 728 filas, por el `set()` del hallazgo 2.2 |
| **Iguales con una columna de más en el original** | 1 | `df_rndc`, 137.527 filas; el original trae una columna `sd` que ningún notebook consume |
| **Difieren** | 20 | los veinte se explican por dos causas, abajo |

### Los 31 idénticos

De la cadena de limpieza: `df_hs2012_2017`, `df_hs2012_2022`, `df_leamer`, `df_BEC`,
`df_hs_names`, `df_ciiu`, `df_ciiu_1996`, `df_comercio` de caracterización (6.984.528 filas),
`df_comercio_mundial` (27.498.389), `df_product_space` (5.199 × 5.199), `df_info_calidad`,
`df_aranceles` (3.891.573), `df_trump`, `df_ntms` (1.235.128), `df_600`, `df_costos_externos`
(6.297.835), `df_amcham`, `deflactor`, `df_productos`, `df_comercio` de impacto (15.575.422),
`df_controles`, `df_paises`, `df_ciiu_mio` (499), `df_va`, `multiplicadores_leontief` (68 × 68).

De la cadena de modelos: `df_surge_vars_6` (548.103), `df_para_estimacion` (359.402),
`df_regresion_glm` (353.741 × 48), `df_m_forecast_6_8_25` (718.888) y `X_fuera_muestra`
(36.851 × 50). De las salidas: `AmChamOverLap.xlsx`.

### Causa 1 de las diferencias: el estimador de calidad

`df_calidad` y `df_calidad_13`, por el hallazgo 2.4. En 5.139.564 filas, `quality_estimate` y
`frontera_90` coinciden hasta 1,5e-11; `quality_normalized` se separa en **132 filas** y
`quality_ladder` en 47, con un máximo de 109. El efecto llega a `Decile` en 19 filas, y de ahí a
`criterio4` en la columna `Decile Promedio`, donde cambian 4 de 253 filas.

### Causa 2 de las diferencias: el potencial exportador se descarga de nuevo

Las otras dieciocho diferencias salen todas de una sola columna, `Potencial Exportador Restante`,
y su origen es el cambio de fuente del hallazgo 2.14: `potencial_exportador.parquet` pasa de
171.024 a **176.557 filas** porque la descarga automatizada del Export Potential Map trae la
versión de 2026 del portal, mientras que el original leía los 190 archivos bajados a mano en 2025.

Comparando `Output Final 040725.xlsx` contra el original, producto a producto:

| Qué se compara | Resultado |
|---|---|
| Productos priorizados | **los mismos 662**, ninguno entra ni sale |
| `Margen`, `Industria`, `Industria 3digit`, `Leamer`, `Type` | **idénticos en los 662** |
| `Potencial Exportador Restante`, total | 17.096.074 → 18.341.046 miles de dólares, **+7,28%** |
| `Potencial Exportador Restante`, por fila | mediana de cambio 22,6%; percentil 90, 86,9% |
| `Tamaño de Mercado 90` / `Tamaño de Mercado 80` | cambian 12 y 48 marcas de 728 |

De esa columna se derivan las dieciocho salidas que difieren: los cuatro criterios de calidad, los
tres de países de comparación, los dos de resiliencia, los tres de aranceles y medidas no
arancelarias, los dos de localización, `df_products_mercado`, `df_potencial_exportador.xlsx` y el
propio `Output Final`.

**Lo que no cambia es lo que consume la cadena de impacto**, que de ese archivo lee `HS6`,
`Margen` e `Industria 3digit`, las tres idénticas. Por eso los artefactos de modelos aguas abajo
salen idénticos o iguales hasta el punto flotante, y las cifras de los dos entregables no se
mueven. Queda como decisión abierta en `pendientes.md`.

### Presentación

Compilada desde `reports/slide/` con las rutas reapuntadas a `output/figures/deck/`:
**62 páginas, cero errores de LaTeX, cero referencias sin resolver y cero citas sin resolver**,
el mismo número de páginas que el original.

Sobre esa versión se aplicaron las tres correcciones de contenido que se habían dejado anotadas:
las cifras de priorización pasan a las que produce la cadena, los cinco rótulos de periodo pasan a
la partición real, el texto de la lámina del porcentaje de éxito deja de prometer una ponderación
que no existe, y las tres tasas de éxito por país de esa misma lámina pasan a las que calcula
`05_proporciones`. Se comprobó sobre el PDF compilado que las cifras nuevas están y las viejas no.

El PDF pesa 946.679 bytes frente a los 818.380 del original de febrero de 2026, y **no es byte a
byte idéntico**, cosa que no podría ser: las seis figuras se regeneran y comprimen distinto. El
`.fls` es la comprobación empírica de qué abrió el compilador, y confirma que **las seis salen de
`output/figures/deck/` y ninguna de `reports/slide/originales/`**:

| Figura | Productor en la versión migrada |
|---|---|
| `Image1.png`, `Image2.png` | `02_stats/09_exploracion_episodios` |
| `Imagen 1.png`, `Imagen 2.png` | `04_report/03_figuras_deck`, en matplotlib en vez de Excel |
| `Imagen 4.png` | `04_report/03_figuras_deck`, desde la tabla de participaciones archivada |
| `expos.png` | `04_report/03_figuras_deck`, desde el extracto de WITS archivado |

**Ninguna lámina del deck depende ya de un PNG del proyecto original.**

El capítulo es un `.docx` y no se recompila: se verifica que sus tablas coincidan con la salida
de los notebooks.
