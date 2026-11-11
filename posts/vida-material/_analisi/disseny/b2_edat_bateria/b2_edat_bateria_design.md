# Disseny: «La bateria es porta a reparar als 4 anys, 1,5 anys més tard que la pantalla»

| | |
|---|---|
| Registre de decisió | `p-distribution-compare-groups--edat-a-la-reparaci-de-la-20261111-2` · estat `declared`; substitueix `p-distribution-compare-groups--edat-a-la-reparaci-de-la-20261111` (`candidate`) |
| Llibreria / host | Altair 6.3 + vl-convert 1.9 (`project.yaml`) · script que desa PNG i SVG a l'entrada, i HTML i Vega-Lite en aquesta carpeta; el quadern 04 l'importa |
| Dades | `../../dades/processades/mobils_classificats.csv`, 5.652 files; signatura `table\|k:categorical:few\|v:quantitative:duration` |
| Sortides | `scripts/06_b2_edat_bateria.py`, `posts/vida-material/b2_edat_bateria.png` (i `.svg`) |
| Idioma | diàleg es · text del gràfic ca · codi en/ca |

## 1. Caracterització del problema

- **Lector:** públic general (lectors del blog): poca formació en gràfics, segons per mirar-lo, pantalla. Modificadors: daltonisme (`cvd`) i lectura en gris (`print-grayscale`).
- **Mode:** explicatiu, estàtic. També fa de miniatura del llistat del blog, on surt sense peu: necessita títol i font propis.
- **Pregunta:** «A quina edat arriben a reparar les bateries, comparat amb les pantalles i amb el punt de 800 cicles que avui fixa el reglament?»
- **Lectures descartades:**
  - «Comparat amb el que exigeix el reglament», la pregunta de la versió anterior. La crítica (`vis-value-critique`) va mostrar que no se sosté: les reparacions són del 2017–2019, el reglament s'aplica des del 2025, i 800 cicles al 80 % no és una avaria.
  - «Quina part arriba abans o després dels 800 cicles», perquè la resposta (33–77 %) depèn gairebé del tot del supòsit de cicles al dia.
- **Validació** (amenaça: problema equivocat): l'usuari va triar la pregunta reformulada, el lector i el mitjà, i va confirmar el resum de l'etapa 1. No s'ha observat cap lector real.

## 2. Abstracció de dades i tasques

| Atribut | Tipus | Rol | Nivells / rang | Notes |
|---|---|---|---|---|
| Grup | categòric | clau | 3: bateria MobiFix, pantalla MobiFix, bateria classificada | `grup_avaria` i `font_avaria` |
| Edat | quantitatiu (durada) | valor | 0–14 anys | `edat_neta`, declarada, gairebé sempre en anys sencers |
| % acumulat | quantitatiu | derivat | 0–100 % | reparacions amb aquesta edat o menys |

- **Dades derivades:**
  - corba acumulada per grup;
  - mediana i IC 95 % per *bootstrap* agrupat per `group_identifier` (1.000 rèpliques, llavor 42): bateria 4 (3,5–5), pantalla 2,5 (2–3), classificat 5 (4–5);
  - % de bateries MobiFix amb edat ≤ 2,2 anys (23 %) i ≤ 4,4 anys (67 %).
- **Filtres:** edat no buida i ≤ 15 anys. MobiFix per a bateria (n = 52) i pantalla (n = 160); bateria de tot el conjunt classificat (n = 213, no validat).
- **Tasques:** presentar i comparar. A nivell baix: *gist* (la bateria va més tard), caracteritzar la distribució, comparar els grups i recuperar valors (medianes i % a les vores de la franja).
- **Abstraccions descartades:**
  - només les medianes, perquè perden la forma de la distribució;
  - només el % de la franja, perquè perd la comparació amb la pantalla;
  - agrupar l'edat per anys sencers: l'usuari va preferir l'edat tal com es declara.
- **Validació** (amenaça: abstracció equivocada): confirmada per l'usuari, que va triar incloure el conjunt classificat en gris.

## 3. Codificació visual

**Idiom:** distribució acumulada (`line_graph` amb esglaons `step-after`).

| Atribut | Marca + canal | Rang (Mackinlay) | Expressivitat |
|---|---|---|---|
| Edat | posició x, 0–10 anys | 1r | escala comuna |
| % acumulat | posició y, 0–100 | 1r | des de zero |
| Grup | to (vermelló, blau, gris) i traç discontinu | adequat per a 3 nivells | sense ordre fals |
| Mediana i IC | punt sobre la línia del 50 % i barra translúcida | posició | definició al text |
| Referència | franja gris de 2,2 a 4,4 anys | posició | etiquetada com a referència, no com a llindar complert |

- **Ordre de les capes:** classificat a sota, després la pantalla, i la bateria a sobre.
- **Color:**
  - finalitat: distingir la bateria i la pantalla;
  - `#d55e00` (bateria), `#0072b2` (pantalla), `#b5b4af` discontinu (classificat);
  - la pantalla era gris (`#a8a7a2`), però l'usuari la va canviar a blau perquè no es veia bé;
  - vermelló i blau són una parella Okabe-Ito segura per a daltònics;
  - a B1 el blau és el port: el color canvia de significat entre figures (punt obert).
- **Text:**
  - títol calculat: «La bateria es porta a reparar als 4 anys, 1,5 anys més tard que la pantalla»;
  - subtítol: període, què és la franja i que aquests mòbils són anteriors al reglament;
  - anotacions: medianes amb IC, «23 % abans» i «33 % després» a les vores de la franja;
  - etiquetes directes en lloc de llegenda;
  - peu: font, edat declarada i les 7 reparacions classificades de més de 10 anys que queden fora de l'eix.
- **Interacció:** cap.

**Idioms descartats:**

| Idiom | Motiu | Regla |
|---|---|---|
| `strip_plot` (adaptació de la llavor `distribution-compare-groups--strip-with-summary`): punts apilats per edat en dues files | generat i mostrat; l'usuari el va rebutjar a la validació de l'etapa 3 | PUR-13 |
| `histogram` (barres de % per any) | el % abans o després de la franja s'ha de sumar a mà | PUR-06 |
| `box_plot` | amaga la concentració en anys sencers i el públic general no el sap llegir | EXP-16 |
| distribució acumulada anterior | sense títol, franja etiquetada «del reglament», classificat amb el mateix to que la bateria, colors diferents de B1 | CMP-04, TXT-01, EFF-09, CLT-05 |

**Validació** (amenaça: idiom equivocat):

a. **Llista de regles:**
- TXT-01 i TXT-02: el títol diu la conclusió, calculada amb les dades.
- TXT-04: etiquetes directes, sense llegenda.
- TXT-05: cruces i medianes anotats.
- TXT-08: font, n i definició de l'edat.
- CMP-04: la franja es presenta com a referència i el subtítol diu que el reglament no aplicava.
- COL-05 i COL-08: segura per a daltònics; la bateria és la marca més fosca en grisos.
- DAT-03: IC de les medianes.
- EXP-09: les dades retallades per l'eix es declaren al peu.

b. **Temps per tasca:**
- *gist*: immediat;
- comparar els grups: immediat;
- recuperar les medianes i el % de les vores: immediat (anotats).

c. **Imatge inspeccionada:** `inspect_image.py` no dona cap troballa. Els grisos de la pantalla i del classificat es distingeixen pel traç.

d. **Crítica:** aplica totes les troballes crítiques i majors de la crítica anterior.

e. **Acceptació del lector:** la versió de punts es va rebutjar. Aquesta versió, amb la pantalla en blau a petició de l'usuari, la va acceptar l'usuari l'11/11/2026. El registre passa a `declared`.

## 4. Algorisme

- **Pipeline:** Altair 6.3, en un script amb `load → derive → build_chart → save`. Desa PNG (`scale_factor=2`) i SVG amb vl-convert a la carpeta de l'entrada, i HTML i `.vl.json` en aquesta carpeta (fora del web).
- **Files:** 5.652 a l'entrada; 425 reparacions amb edat als tres grups.
- **Validació** (amenaça: algorisme equivocat):
  - `run_check.py`: el codi s'executa sense errors i l'inspector Vega-Lite executa l'script; no hi ha troballes que bloquegin.
  - EFF-18 («panell molt petit») es descarta: és la línia de text del peu, de 24 px d'alçada.
  - El quadern 04 s'executa sencer amb `nbclient` sense errors.

## 5. Registre de decisió

Desat a `.claude/vis-decisions/p-distribution-compare-groups--edat-a-la-reparaci-de-la-20261111-2.yaml` (estat `declared`), que substitueix `p-distribution-compare-groups--edat-a-la-reparaci-de-la-20261111`. La còpia JSON és a `record.json`, en aquesta carpeta.

## 6. Supòsits i punts oberts

- **V3** (acceptació de la imatge): acceptada per l'usuari l'11/11/2026.
- **Grup de la bateria:** «Bateria i alimentació» inclou el tipus `Charger`. Entre les reparacions de MobiFix amb edat n'hi ha com a molt 3, de 52.
- **Coherència entre figures:** a B1 el blau és el port i aquí és la pantalla. A més, B3 encara fa servir vermell per al final de vida i gris fosc per al reparat. Si la bateria passa a ser vermelló a tot el post, caldrà revisar B3.
