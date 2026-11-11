# Diseño: el 2019 se vendieron y retiraron un 30 % menos de móviles que el 2013, y el parque en uso se mantuvo cerca de los 68 millones

| | |
|---|---|
| Registro de decisión | `p-category-breakdown-over-time--parc-estimat-de-m-bils-del-20261111-2` · sustituye a `-20261111` (textos revisados) · estado `declared` (aceptado por el usuario) |
| Librería / host | matplotlib 3.10 (`project.yaml`) · script que guarda PNG |
| Datos | `posts/avaries-mobil/_estimacio/balanc_escenaris_uk.csv`, 35 filas (5 escenarios × 7 años), salida de `escenaris_uk.py` |
| Salidas | `_estimacio/poblacio_mobils_uk.py`, `posts/avaries-mobil/poblacio_mobils_uk.png` |
| Idioma | diálogo y documento en castellano · texto del gráfico en catalán · código en catalán e inglés, como el resto del repositorio |

## 1. Caracterización del problema

- **Lector:** público general del blog, sin tiempo para aprender una forma de gráfico nueva. Modificador `cvd`.
- **Modo y medio:** explicativo; imagen estática dentro de un post de Quarto.
- **Pregunta del lector:** ¿cuántos móviles hay en uso en el Reino Unido cada año, cuántos entran, cuántos salen y por qué motivo?
- **Lectura descartada:** la de la v1, «por dónde y por qué salen», con dos paneles de salidas. Ver la validación.
- **Validación (amenaza: problema equivocado):** **la v1 falló.** El usuario dijo que la v1 repetía las entradas en los dos paneles, no mostraba el parque y fallaba en su tarea. La pregunta se reformuló con él: evolución del parque, entradas y salidas cada año. Las salidas se reparten por causa, que es lo que el usuario eligió.
- **Pregunta previa del usuario:** si las estimaciones eran suficientemente fiables para comparar cantidades.
  - **Respuesta:** sí para órdenes de magnitud (±20 %) y tendencias, que se mantienen en todas las filas de escenario y de banda; no para el reparto avería / sin avería (factor 5) ni para la diferencia de un año a otro.
  - **Consecuencia:** el usuario pidió dos franjas en lugar de la bañera cualitativa.
- **No hecho:** observar a lectores reales.

## 2. Abstracción de datos y tareas

| atributo | tipo | rol | niveles / rango | notas |
|---|---|---|---|---|
| `any` | temporal | clave | 2013–2019 (7) | |
| causa de salida | categórica | clave | 5: pantalla, batería, programario, resto, sin avería | «resto» = otras + botones + puerto + daños + desconocida |
| `parc` | cuantitativo (recuento) | medida | 66–69 M | banda de anclaje: 54–57 M (personas) a 78–81 M (SIM) |
| `vendes`, salidas por causa | cuantitativo (recuento por año) | medida 2 | 25–37 M al año | |
| baixes per avaria optimista / pessimista | cuantitativo | inferior / superior | 3–19 M | |

- **Datos derivados:**
  - `saldo = vendes − sortides`;
  - `durada implícita = parc ÷ vendes` (1,8–2,6 años);
  - «resto» como suma de cinco grupos de MobiFix.
- **Tareas:** presentar y comparar (entradas frente a salidas, años entre sí), ver la tendencia, captar la idea principal y conocer el rango del escenario. Tareas temporales: patrón y ritmo de cambio.
- **Abstracciones descartadas:**
  - **Salidas por vía en el gráfico principal.** Quedan en `ordres_de_magnitud_uk.md` §7, pendientes de un gráfico propio.
  - **Parque del cajón.** Su crecimiento es un artefacto de la estancia fija de cuatro años.
  - **Porcentajes en lugar de recuentos.** Ocultarían el tamaño del parque.
- **Validación (amenaza: abstracción equivocada):** cada término de la pregunta tiene su atributo (parque, entradas, salidas, causa, año). Confirmada por el usuario a través de la reformulación.

## 3. Codificación visual

**Forma:** dos franjas con el mismo eje x.
- **Arriba:** el parque, en barras desde cero, con un bigote para la banda de anclaje.
- **Abajo:** barras divergentes. Las entradas van encima del cero. Las salidas van debajo, apiladas por causa: las averías pegadas al cero y «sin avería» debajo. El bigote del escenario va sobre la frontera entre avería y sin avería.

| atributo | marca + canal | comprobación |
|---|---|---|
| año | posición x | orden cronológico |
| parque, entradas, salidas | longitud desde cero | **la misma escala en las dos franjas** (85 M de altura cada una), de manera que se ve que el parque equivale a unos dos años de ventas sin necesidad de un doble eje |
| causa | tono, en tres familias pastel, con orden de claridad dentro de cada familia | etiquetas directas en la barra del 2019 y bordes blancos entre segmentos |
| rango de escenario y banda | bigote gris pizarra | explicado al lado de la barra del 2019 y en el pie |
| saldo | texto bajo cada año | lo pidió el usuario |

- **Color.** Petición del usuario: pastel, atractivo, dos o tres colores complementarios con sus tonalidades.

  | Familia | Uso | Tonos |
  |---|---|---|
  | azul | parque | `#A9C1DD` |
  | azul | entradas | `#7FA7D1` |
  | coral | pantalla, batería, programario, resto | `#C96A55`, `#DE9483`, `#EDBBAE`, `#F7E1DA` |
  | salvia | sin avería | `#8CC2AF` |

  - **Pares contiguos.** `colorcheck.py` da una ΔE simulada de 13,3 o más entre todos los segmentos que se tocan, en deuteranopía, protanopía y tritanopía.
  - **Revisión de la deuteranopía.** El coral pasa a oliva y la salvia a gris, pero siguen separados por claridad.
- **Texto.**
  - **Títol calculat:** «S'estima que el 2019 es van vendre un 28 % menys mòbils nous que el 2013, mentre el parc en ús passava de 66 a 69 milions».
  - **Subtítulo:** «Regne Unit, estimació, escenari central», la misma escala en las dos franjas y el ejemplo de balance 66,1 + 36,5 − 35,7 = 66,9.
  - **Pie (dos líneas):** qué es fiable (orden de magnitud ±20 %, tendencia; bajas por avería con factor 5 entre escenarios) y las fuentes con la ruta del cálculo.
  - **Revisión del 2026-11-11** tras las críticas de Slop Hunter y Popular Science sobre la entrada:
    - el título decía «un 30 %», mientras que el texto da un 28 %, y lo afirmaba como un hecho; ahora usa el valor calculado y «S'estima»;
    - «Sense avaria (el mòbil funcionava)» afirmaba algo que el modelo no sabe; ahora es «Altres sortides (calaix, exportació, reciclatge…)»;
    - el subtítulo de 1,8–2,6 años de ventas necesitaba una explicación aparte y se ha quitado;
    - el pie de cinco líneas repetía el texto y queda en dos (la sensibilidad de la pantalla está en el apartado 8 de la entrada).
- **Cifras con un decimal.** Lo pidió el usuario, para que el balance cuadre visiblemente. El pie dice que la precisión real es de ±20 %.
- **Interacción:** ninguna.

**Idiomas descartados:**

| idioma | motivo | regla |
|---|---|---|
| v1: dos paneles de salidas, lado a lado (por vía y por causa) | repetía las entradas y no mostraba el parque; el usuario la rechazó | CMP-05 |
| líneas (la decisión por defecto guardada, seed `category-breakdown-over-time--lines-few-categories`) | no muestra que las salidas suman un total ni el balance entre entradas y salidas | IDM-LINE |
| área apilada | cinco capas; solo la inferior tiene una línea base | IDM-STACK |
| bañera o flujo (Sankey) | la longitud de la flecha y la de la barra del parque tienen unidades distintas; solo sirve para una lectura cualitativa | EFF-16 |
| mapa de calor (la decisión guardada del proyecto) | responde a otra pregunta (cuota de causas) | IDM-HEATMAP |

**Validación (amenaza: idioma equivocado).**
1. **Comprobaciones.** Barras desde cero, sin doble eje, como mucho 7 tonos y una segunda pista: ✔.
2. **Tiempos de lectura:**
   - el parque de un año: inmediato;
   - entradas frente a salidas: inmediato, más el saldo;
   - la tendencia: inmediata;
   - la causa principal de salida: con las etiquetas;
   - el rango de las averías: con el bigote y la nota.
3. **Aceptación del lector.** La v1 fue rechazada. En la v2 el usuario pidió añadir decimales y se aplicó el cambio. El usuario aceptó la v2 y aprobó la revisión de textos del 2026-11-11.

## 4. Algoritmo

- **Plantilla.** `chart_matplotlib.py.tmpl`, con `derive → takeaway → build_chart → save`. `DATA_PATH` es relativo al script.
- **Salida.** Solo PNG; no se guarda SVG, para no añadir un archivo a la carpeta del post.
- **Comprobación interna.** `derive()` verifica que las causas suman las salidas, con una tolerancia de 10⁻³ millones porque el CSV tiene 6 cifras significativas.
- **Validación (amenaza: algoritmo equivocado).** `run_check.py` da `ok: true` e `inspector_ran_script: true`.
  - **Comprobación de las cifras.** Las del PNG coinciden con la fila central del CSV.
  - **Comprobación del saldo.** Cuadra con el parque del año siguiente, con un margen de ±0,1 por redondeo.

**Hallazgos descartados:**

| regla | motivo |
|---|---|
| COL-05 (rojo y verde, fusión en deuteranopía) | coral y salvia quedan separados por claridad, y hay etiquetas directas |
| COL-06 (poco contraste de los pastel) | se pidió paleta pastel; los bordes blancos y las etiquetas en gris oscuro lo compensan |
| SCL-06 (eje sin título) | los años se explican solos |
| SCL-08 (paneles con rangos de y distintos) | la altura es igual (85 M) a propósito, para que la escala coincida |
| TXT-01 (título no detectado) | el título se dibuja con `fig.text` |

## 5. Registro de decisión

Guardado en `.claude/vis-decisions/p-category-breakdown-over-time--parc-estimat-de-m-bils-del-20261111-2.yaml`, con estado `declared` y confianza media. Sustituye a la versión `candidate` `-20261111`: la forma y la paleta no cambian, solo los textos.

## 6. Supuestos y puntos abiertos

- **Librería.** No se volvió a preguntar: es la guardada en el proyecto (matplotlib).
- **Momento del parque.** Va etiquetado como «a comienzo de año» para que cuadre con la ecuación del balance. Las fuentes miden en momentos distintos (Ofcom en enero y febrero, ONS a mitad de año); es una aproximación Fermi.
- **Gráfico pendiente.** Las vías de salida (cajón, exportación, reciclaje, basura) siguen sin gráfico propio.
