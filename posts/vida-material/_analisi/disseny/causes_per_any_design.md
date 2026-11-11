# Diseño: La pantalla explica entre el 29 % y el 37 % de las averías de móvil cada año (2014–2019)

| | |
|---|---|
| Registro de decisión | `p-part-to-whole-over-time--distribuci-anual-de-les-20261111` · sustituye a `-20261110` (cambio de paleta, 2026-11-11) · estado `candidate` (asumido, no confirmado) |
| Librería / host | matplotlib · script que guarda PNG |
| Datos | `posts/vida-material/_analisi/dades/raw/ora_mobifix.csv`, 1.916 filas (1.842 con resultado conocido), 2012–octubre 2020 |
| Salidas | `scripts/04_causes_per_any.py`, `posts/avaries-mobil/causes_per_any.png` (el Sankey `sankey_avaries.png` y su script se mantienen) |
| Idioma | diálogo es · texto del gráfico ca · código en |

## 1. Caracterización del problema

- **Lector**: público general (lectores del blog), sin tiempo para aprender un idioma gráfico nuevo. Modificador `cvd`.
- **Modo**: explicativo, estático, imagen dentro de un post de Quarto.
- **Pregunta**: ¿cuál es la causa de avería de los móviles en cada año y cómo cambia, año tras año, la distribución de causas?
- **Lecturas descartadas**: «salida» como final de vida (esa pregunta tiene su propio dato, 208 casos, demasiado disperso para una matriz año × causa; queda como gráfico aparte, ver §6).
- **Validación (amenaza: problema equivocado)**: asumida. Sale de la petición del usuario («por cada año cuál es el motivo» y «comparar año tras año la distribución de las causas») y de la crítica previa del Sankey. No se ha observado a lectores reales.

## 2. Abstracción de datos y tareas

| atributo | tipo | rol | niveles | notas |
|---|---|---|---|---|
| `event_date` → año | temporal | clave | 8 (2012–13 agrupados, 2013…2020) | 2012 tiene 1 caso y se cuenta con 2013, igual que el Sankey; 2020 llega hasta octubre |
| `fault_type` → causa | categórico | clave | 8 grupos (25 tipos originales) | mismos grupos que `03_sankey_mobifix.py` |
| cuota | cuantitativo (share) | valor derivado | 0–37 % | ver abajo |

- **Derivado**: `cuota = reparaciones(año, causa) / reparaciones(año) × 100`. Filtro: `repair_status` conocido (1.842 de 1.916), igual que el Sankey para que las cifras cuadren. n por año como serie aparte.
- **Tareas**: recuperar valor (cuánto pesa X en el año Y), encontrar extremo (la causa principal), comparar (año con año), caracterizar la distribución; temporales: patrón, ritmo de cambio.
- **Abstracciones descartadas**: recuentos absolutos (mezclan volumen con composición, el fallo principal del Sankey); mes como grano (n demasiado pequeño); incluir las 74 filas sin resultado (se mantiene el filtro del Sankey por consistencia con el post; ver §6).
- **Validación (amenaza: abstracción equivocada)**: cada término de la pregunta tiene atributo (año, causa) y valor (cuota). Asumida.

## 3. Codificación visual

- **Idioma**: mapa de calor (`heatmap`) con tira de barras de n encima.

| atributo | marca + canal | rango (Mackinlay) | comprobación de expresividad |
|---|---|---|---|
| año | posición x, ordinal cronológico | posición | orden temporal sobre canal ordenado |
| causa | posición y, nominal | posición | sin orden implícito: filas por frecuencia total, residuales al final |
| cuota | luminosidad secuencial + valor impreso en la celda | luminosidad (baja precisión) → compensada con el número | una sola escala 0–40 % en las 64 celdas |
| n por año | longitud, desde cero (tira aparte) | longitud | escala propia, no mezclada con la cuota |
| causa destacada | contención (recuadro) | – | un solo ressalt: la fila Pantalla, que es el título |

- **Orden, escalas**: columnas cronológicas, columna «Tot» tras un hueco; Altres y Desconegut al final, separadas (no nombran una causa).
- **Color** (revisado el 2026-11-11 para uniformarlo con `poblacio_mobils_uk.png`):
  - **Celdas.** Un solo propósito, codificar el valor. Rampa secuencial azul pastel, la familia del parque en el segundo gráfico (`#A9C1DD`, `#7FA7D1`), extendida por los dos extremos: `#EEF3F9 → #D3E0EF → #A9C1DD → #7FA7D1 → #5A86B8 → #3B6596`. L* baja de 96 a 42 en pasos de 10–12, así que se lee en gris y con daltonismo. El número de cada celda es el segundo indicio.
  - **Texto de las celdas.** Blanco o `#333333`, el que dé más contraste WCAG con el fondo de la celda.
  - **Barras de n.** Coral, el color de las averías en el segundo gráfico: `#DE9483`, y `#EDBBAE` rayado para los años con n < 80.
  - **Resto.** Recuadro de la fila Pantalla en gris pizarra `#5B6573` (las marcas de escenario del segundo gráfico); texto `#333333` y `#6b6b6b` sobre fondo hueso `#FBFAF7`.
  - **Paletas descartadas en la validación con el usuario:**
    - rampa coral de un solo tono: demasiado sosa;
    - degradado de dos tonos azul → coral: la interpolación RGB pasa por un tramo malva grisáceo, y acortarlo crea un corte de tono (en el 20 %) que se lee como un umbral que los datos no tienen (COL-02).
- **Texto**: título con mensaje calculado de los datos («La pantalla explica entre el 29 % y el 37 % de las averías de móvil cada año (2014–2019)»); subtítulo con la definición de la medida; asteriscos en 2012–13 y 2020 (n < 80, barra rayada); nota de «Desconegut» (32 % en 2017); fuente, n y exclusiones al pie.
- **Interacción**: ninguna; el estado por defecto responde a las dos preguntas.
- **Idiomas rechazados**:

| idioma | motivo | regla |
|---|---|---|
| área apilada al 100 % (default almacenado) | 8 categorías; solo la inferior tiene línea base | IDM-STACK |
| barras apiladas al 100 % | igual: solo Pantalla y el segmento superior se comparan | IDM-STACK |
| Sankey (versión previa) | ancho mezcla volumen y cuota, ~62 cintas cruzadas | EFF-16 |
| líneas | 8 líneas con valores solapados en 0–15 % | IDM-LINE |
| small multiples | 8 paneles; el mapa de calor muestra los 64 valores a la vez | CMP-05 |

- **Validación (amenaza: idioma equivocado)**
  a. Lista de reglas: COL-02 (paleta secuencial para valores) ✔ · IDM-HEATMAP (orden significativo, celdas legibles, escala común) ✔ · CMP-01 (filas por valor total) ✔ · TXT-01 (título) ✔ · TXT-08 (fuente, n) ✔.
  b. Tiempos: causa principal de un año → inmediato (columna, celda más oscura); cuota de una causa en un año → inmediato (número); comparar años → inmediato (fila); tendencia de una causa → inmediato; peso del volumen → inmediato (tira de n).
  c. Render: `posts/avaries-mobil/causes_per_any.png`; escala de grises inspeccionada (la fila Pantalla y los picos de Desconegut siguen destacando); simulación de deuteranopía: las celdas contiguas del degradado se parecen (ΔE 6,6), pero el número impreso lo cubre.
  d. Crítica opcional: no se ha pasado `vis-value-critique` sobre el resultado final. El inspector determinista no marca nada bloqueante.
  e. Aceptación del lector: **pendiente**, el usuario no ha visto aún el render.

## 4. Algoritmo

- matplotlib (instalado, exporta PNG). Pipeline `load → derive → build_chart → save`.
- Filas de entrada 1.916, tras derivar 1.842 (74 excluidas), 1,7 s de ejecución.
- **Rechazados**: Altair y Plotly (no instalado `vl_convert`/`kaleido`, no exportan PNG sin instalar nada; además el Sankey ya usa matplotlib).
- **Validación (amenaza: algoritmo equivocado)**: `run_check.py` → `ok: true`, sin hallazgos bloqueantes. Las cifras del PNG coinciden con las de `03_sankey_mobifix.py` (n por año 30, 82, 100, 209, 332, 482, 538, 69). Hallazgos deterministas descartados:
  - COL-04 (49 colores cromáticos): es una rampa secuencial.
  - COL-05 (celdas contiguas se funden en deuteranopía): el degradado es ordenado y cada celda lleva el número.
  - COL-06 (celdas claras con poco contraste frente al fondo): son las de valores bajos, siempre rotuladas.
  - SCL-06 (sin títulos de eje), SCL-07 (eje y invertido), TXT-01 (título no detectado): ejes categóricos/temporales autoexplicativos, matriz con filas de arriba abajo, título dibujado con `fig.text`.
  - SCL-08 (dos paneles con escala distinta): son volumen y cuota a propósito.

## 5. Registro de decisión

Guardado en `.claude/vis-decisions/p-part-to-whole-over-time--distribuci-anual-de-les-20261111.yaml` (estado `candidate`, confianza media, `--assumed`). Sustituye a `-20261110`: la solución es la misma salvo el plan de color.

## 6. Supuestos y puntos abiertos

| pregunta | respuesta asumida | motivo |
|---|---|---|
| S1.reader | público general | blog divulgativo |
| S1.mode / medium | explicativo, estático | imagen en un post |
| S1.question | causa por año + comparación año a año | petición del usuario |
| S2.data | año × causa, valor = cuota del año | crítica previa del Sankey |
| S2.derive | normalizar por año; filtrar a resultado conocido | consistencia con el Sankey (1.842) |
| S3.idiom | mapa de calor (default almacenado, área apilada, descartado) | 8 categorías exceden su escala |
| S3.color | secuencial azul de la paleta del segundo gráfico; barras de n en coral | valor, no categoría; uniformidad pedida por el usuario |
| S3.interaction | ninguna | medio estático |
| S4.library | matplotlib | instalado, exporta PNG, consistente con el Sankey |

Puntos abiertos:
- **Resultado conocido**: para este gráfico no hace falta el resultado de la reparación, así que las 74 filas excluidas podrían entrar (n = 1.916). Se mantienen fuera para que cuadre con los 619/34 % del texto del post.
- **Final de vida por año**: baja del 30 % (2012–13) al 6 % (2019). Es el hallazgo que ocultaba el Sankey. No cabe en esta matriz; merece un gráfico de barras aparte.
- **Aceptación del lector**: el usuario no ha validado el render.
