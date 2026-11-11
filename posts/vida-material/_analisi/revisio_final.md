# Revisión final de `index.qmd` (vida material) · 2026-11-11

Cada cifra del texto se ha contrastado con la salida de los cuadernos 02–05 y con `dades/processades/mobils_classificats.csv`, y cada figura con el párrafo que la comenta.

## Cifras: todas cuadran

| Apartado | Afirmación | Comprobado |
|---|---|---|
| Tabla de datos | 1.664 / 114 / 42 y 42 / 200 / 52 | ✓ cuadernos 03, 04, 05 |
| B1 | No carga: batería 21 (50 %), puerto o cargador 16 (38 %) | ✓ |
| B1 | No se enciende: batería 24 (57 %), resto 17 + 1 | ✓ |
| B2 | Mediana batería 4 años (IC 3,5–5, n = 52); pantalla 2,5 (n = 160) | ✓ |
| B2 | 800 ciclos = 2,2–4,4 años; 1.000 ciclos = 2,7–5,5 | ✓ |
| B2 | 23 % antes de 2,2 años, 33 % después de 4,4 | ✓ (77 % y 33 % por encima) |
| B2 | 161 baterías del clasificador, mediana 5 años, casi todas de 2021–2026 | ✓ (145 de 161) |
| B2 | Hinchadas: mediana 6,5 años, n = 11 | ✓ |
| B3 | Fin de vida 13 % (26/200) frente a 5 % (29/584); reparado 39 % frente a 55 % | ✓ |
| B3 | Los 16 puntos se reparten a partes iguales (8 + 8) | ✓ |
| B3 | Solo clasificador: 21 % (63/302) frente a 15 % (58/381) | ✓ |
| B3 | Motivo vacío: 57 de 89 (batería), 56 de 87 (pantalla); «no se puede abrir» 6 frente a 3 | ✓ |
| B3 | Precodificación: 75 % sin motivo; 7 «no era la batería», 6 hinchada | ✓ |
| B3 | ≤ 3 años: 5 % y 5 % (1/20, 6/121); > 3 años: 16 % (5/32) frente a 3 % (1/39) | ✓ |

## Figuras frente al texto

- **Figura 1:** coherente con el texto (16/21/5 y 1/24/17).
- **Figura 2:** coherente (colores, medianas, 23 % y 33 % marcados en la curva, línea discontinua n = 213).
- **Figura 3:** coherente. El título dice «más del doble» y el texto «dos veces y media»: son compatibles.
- **Detalle menor, sin corregir:** el subtítulo de la figura 1 dice «MobiFix (2012–2020)» y el de la figura 3 «(2013–2020)». Las dos fechas son correctas porque B1 usa MobiFix entero (hay un registro de 2012) y B3 usa los registros cruzados. Para corregirlo habría que regenerar la figura 1.

**Bases distintas:** la figura 1 usa MobiFix tal como viene (1.664 con texto) porque necesita el tipo de avería detallado. Las figuras 2 y 3 usan las 1.407 reparaciones de MobiFix que se encuentran en el conjunto de smartphones, porque necesitan la edad, el resultado y el complemento del clasificador. Se ha corregido el pie de la tabla de datos, que decía que todo se contaba sobre las 1.664.

## Conclusiones

Ninguna conclusión va más allá de los datos. El texto ya dice que las muestras son pequeñas (B1), que la edad no es la duración y que no se puede comparar con el reglamento (B2), que la edad puede ser un factor de confusión y que el motivo casi nunca consta (B3). La conclusión final («acaba sin solución más a menudo que una pantalla») describe lo observado y no afirma ninguna causa.

**Hallazgo nuevo:** en B2 y B3, «avería de batería» es el grupo *Bateria i alimentació*, que incluye **7 cargadores de 200**. Puede parecer que contradice B1, que separa el cargador de la batería. Sin ellos, el fin de vida pasa del 13,0 % al 13,5 % y la mediana sigue en 4 años. Se añade una línea en «Com ho hem fet».

## Revisión manual: rebajada

Ningún resultado del artículo depende de la revisión manual, y esa revisión no se hará. Se ha cambiado el texto para que no aparezca como un paso pendiente:

- «Com ho hem fet», símptomes: se quita «aquesta comprovació també està pendent». Ahora dice que las palabras clave no se han revisado a mano y que la avería es la que anotaron los voluntarios.
- «Com ho hem fet», motius: se quita «Està pendent que una persona del grup revisi els 89 textos». Ahora queda claro que «el motivo no consta» sale del campo de los voluntarios y que la precodificación es orientativa.
- Apartado 3: «Hem llegit també les descripcions» pasa a «Hem passat també les descripcions per una classificació automàtica», porque nadie las ha leído.

No se ha encontrado en el proyecto ninguna comprobación manual de «1.200» registros. Lo que queda pendiente de validar son la muestra de 30 textos (B1) y los 89 fines de vida (B3). La cifra 1.200 solo aparece como los ciclos de la mejor tecnología disponible.

**Fuera del artículo (no publicado), sin tocar:** el cuaderno 05 sigue diciendo «una persona la revisa» y genera `revisio_bateria_fi_vida.csv`; el cuaderno 03 tiene la sección «Comprovació a mà».

---

# Segunda comprobación independiente · 2026-11-11

**Esta sección sustituye tres puntos de la primera revisión:** «7 no era la batería ✓», «Hinchadas n = 11 ✓» y «Ninguna conclusión va más allá de los datos». Ver abajo.

Se han recalculado todas las cifras desde `dades/raw/ora_mobifix.csv` y `dades/processades/mobils_classificats.csv` con un script propio (no con los cuadernos), y se han contrastado las afirmaciones legales con el texto de EUR-Lex del Reglamento (UE) 2023/1670.

## Lo que se confirma

- Todas las cifras de la tabla de la primera revisión salen igual, salvo las bateries inflades (ver abajo).
- Las tres figuras dicen lo mismo que el texto: 16/21/5 y 1/24/17 (fig. 1); 23 % y 67 % en la curva, medianas 4 y 2,5, n = 213 en la discontinua (fig. 2); 13/48/39 y 5/40/55 (fig. 3).
- Los años cuadran: las 52 baterías con edad son de 2017–2019 (texto) y las pantallas llegan a 2020 (subtítulo de la fig. 2, 2017–2020).
- **La conclusión central de B3 es sólida:** 26/200 frente a 29/584, prueba exacta de Fisher p ≈ 0,0003 (OR ≈ 2,9).
- Reglamento: 800 ciclos al 80 % desde el 20/06/2025 ✓; excepción 83 %/500, 80 %/1.000 e IP67 ✓; 1.200 ciclos como mejor tecnología disponible (anexo V) ✓.

## Errores corregidos en `index.qmd`

1. **«l'única peça del mòbil amb un llindar legal de durabilitat» era falso.** El mismo reglamento exige a la pantalla dureza 4 en la escala de Mohs, 45 caídas sin funda y protección IP. Ahora dice «I té un llindar legal de durabilitat propi».
2. **«el problema no era la bateria (7 casos)» exageraba.** De los 7 textos, uno dice «Akku und Buchsen defekt» (batería *y* conector), tres dicen «battery or/and main board» (dos son el mismo texto) y solo unos tres dicen claramente que la batería nueva no lo arregló. Además, **los 7 son del clasificador**, ninguno de MobiFix: es un error del clasificador, no de las etiquetas humanas. Se ha reescrito la frase en ese sentido.
3. **Baterías hinchadas (11 casos, mediana 6,5).** No salen del clasificador sino de buscar palabras clave en todos los registros con edad, e incluyen uno que no está en el grupo de batería. Solo con el grupo de batería son 10 y la mediana es 6,25. Ahora el texto dice de dónde salen.
4. **«el motiu gairebé mai no consta»** exageraba: falta en 57 de 89 (64 %). Ahora dice «en dos de cada tres casos».

## Propuestas de redacción (no aplicadas, decisión del autor)

**A. Edad en el conjunto clasificado (apartado 2).** Las pantallas del clasificador también son más viejas (mediana 4 años frente a 2,5 en MobiFix). La batería sube 1 año y la pantalla 1,5, así que la distancia entre las dos se *reduce*. Propuesta, después de «un any més que les de MobiFix (2017–2019)»: «Però les pantalles que hi afegeix també són més velles (mediana de 4 anys), així que el que ha canviat és sobretot l'edat de tots els mòbils que arriben, no només la de les bateries.»

**B. Final de vida por edad (apartado 3).** Las pantallas no empeoran con la edad (5 % → 3 %); las baterías pasan del 5 % al 16 % solo en los móviles viejos. Si fuera solo la edad del móvil, subirían las dos. La lectura más precisa es que la diferencia se concentra en las baterías de móviles viejos (p. ej., recambios para modelos antiguos). Propuesta para sustituir «Com que les bateries es porten a reparar més tard, part de la diferència podria ser l'edat del mòbil i no la bateria»: «No és l'edat sola, perquè les pantalles dels mòbils vells gairebé mai no acaben a final de vida. El que acaba més sovint sense solució és la bateria d'un mòbil vell.» (Sin dar causa, para no contradecir la línea 80.)

**C. «Què diu la llei» y la conclusión.** El reglamento también obliga a ofrecer la batería como recambio a reparadores *y usuarios* durante 7 años después de dejar de vender el modelo, a entregarla en 5 días laborables (10 en los dos últimos años) y a publicar el precio orientativo sin impuestos (anexo II, punto 1.1, apartados 1, 3 y 4: «Information on the price of spare parts»). Esto ataca justo la barrera principal que sale en B3 (piezas caras o inexistentes). Sin mencionarlo, «exigeix durabilitat més que no pas facilitat per canviar-la» (conclusión) queda sesgado. Propuesta: añadir una frase en «Què diu la llei» y matizar la conclusión.

**D. Sesgo de selección en B1 (menor).** Al quitar los textos con la palabra «batería» se quitan sobre todo casos de batería. Con todos los «no carga» (52), el puerto o cargador es 18 de 52 (35 %) y la batería 29 (56 %). La conclusión cualitativa no cambia, pero el «gairebé 4 de cada 10» es el techo. Se podría añadir: «Si comptem també els textos que diuen “bateria”, el port o el carregador són 1 de cada 3.»

## Detalles menores, sin corregir

- Colores: la batería es gris en la fig. 1, naranja en la fig. 2 y no tiene color propio en la fig. 3 (que codifica el resultado). No confunde, pero no hay un color fijo para la batería en toda la entrada.
- Hay textos repetidos en el mismo evento con ids consecutivos (p. ej., Lambeth 2023, Portsmouth 2025, Weymouth 2025). Pueden ser dos móviles o una entrada doble; afectan como mucho a 4–5 de los 89 finales de vida.
- Edad declarada en años enteros: «23 % abans dels 2,2 anys» es en la práctica «2 años o menos». El pie de la fig. 2 ya lo dice.
- «Treure'ls no canvia les xifres» (carregadors): exactamente, el final de vida pasa del 13,0 % al 13,5 %. Sería más preciso «no canvia les conclusions».
