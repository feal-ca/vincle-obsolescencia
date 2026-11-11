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
