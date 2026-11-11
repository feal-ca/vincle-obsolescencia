# Disseny: «Quan el mòbil no carrega, gairebé 4 de cada 10 vegades era el port o el carregador, no la bateria»

| | |
|---|---|
| Registre de decisió | `p-compare-two-keys--avaria-real-darrere-dels-s-20261111-2` · estat `declared`; substitueix `p-compare-two-keys--avaria-real-darrere-dels-s-20261111` (`candidate`) |
| Llibreria / host | matplotlib (`project.yaml`) · script que desa PNG i SVG; el quadern 03 l'importa |
| Dades | `../../dades/raw/ora_mobifix.csv`, 1.916 files (1.664 amb text), signatura `table\|k:categorical:few+k:categorical:few\|v:quantitative:share`, 2012–2020 |
| Sortides | `scripts/05_b1_simptomes.py`, `posts/vida-material/b1_simptomes.png` (i `.svg`) |
| Idioma | diàleg es · text del gràfic ca · codi en |

## 1. Caracterització del problema

- **Lector:** públic general (lectors del blog): poca formació en gràfics, segons per mirar-lo, pantalla. Modificadors: daltonisme (`cvd`) i lectura en gris (`print-grayscale`).
- **Mode:** explicatiu, un sol missatge, estàtic.
- **Pregunta:** «Quan un mòbil no carrega o no s'encén, quantes vegades és realment la bateria i quantes el port o el carregador?»
- **Lectures descartades:** la distribució completa de les set avaries per símptoma. Aquesta va ser la versió anterior, i la crítica la va descartar perquè dispersa el missatge.
- **Validació** (amenaça: problema equivocat): la pregunta surt de l'apartat B1 de l'entrada i de la crítica `vis-value-critique` de la figura anterior. L'usuari va fixar l'enunciat i el disseny al prompt («2 files, 3 categories, accent al port»). No s'ha observat cap lector real.

## 2. Abstracció de dades i tasques

| Atribut | Tipus | Rol | Nivells / rang | Notes |
|---|---|---|---|---|
| Símptoma | categòric | clau | 2 (no carrega, no s'encén) | paraules clau sobre `problem` (`comu.SIMPTOMES`) |
| Grup d'avaria | categòric | clau 2 | 3 | `fault_type` agrupat |
| Proporció | quantitatiu (*share*) | valor derivat | 0–100 % | recompte / total del símptoma |

- **Dades derivades:**
  - grups: port o carregador = `USB/charging port` + `Charger`; bateria = `Power/battery`; la resta = altres avaries i desconegut;
  - proporció = n(símptoma, grup) / n(símptoma).
- **Filtres:** MobiFix amb text i textos que **no** contenen la paraula «bateria». «Dura poc» i «inflada» no hi surten perquè no tenen casos després del filtre.
- **Tasques:**
  - finalitat: presentar, consultar i comparar;
  - nivell baix: *gist* (sí o no és la bateria), comparar el port entre files i recuperar valors (recompte).
- **Abstraccions descartades:**
  - set categories, perquè no les demana la pregunta;
  - incloure els textos que diuen «bateria», perquè inflen la bateria amb el diagnòstic del voluntari.
- **Validació** (amenaça: abstracció equivocada): cada terme de la pregunta té un atribut (el símptoma, «realment» com a avaria trobada pels voluntaris, el port o el carregador com a grup). Confirmada per l'usuari al prompt.

## 3. Codificació visual

**Idiom:** `stacked_bar_graph`, barra horitzontal al 100 % amb 3 segments.

| Atribut | Marca + canal | Rang (Mackinlay) | Expressivitat |
|---|---|---|---|
| Símptoma | posició vertical (files) | 1r per a nominals | correcte: dues files i la n a l'etiqueta |
| Proporció | longitud des de la base comuna (només el primer segment) | 1r–3r | les parts sumen 100 % per fila (EXP-05 compleix) |
| Grup | lluminositat i to (accent més dos grisos) | adequat per a 3 nivells | sense ordre fals: l'accent marca el missatge, no un ordre |
| Recompte | text directe | — | «n de total · %» |

- **Ordenació i escales:**
  - el port va primer, perquè el segment del missatge parteixi de la base comuna i es pugui comparar entre files;
  - eix de 0 a 100, sense truncar (EXP-08);
  - sense eix visible perquè tots els valors porten etiqueta (excepció de TXT-04).
- **Color:**
  - finalitat: destacar;
  - paleta neutra amb un accent: `#0072b2` per al port, `#8f8e89` per a la bateria i `#d9d8d4` per a la resta;
  - `colorcheck`: segura per a daltònics, sense parelles confuses;
  - segona pista: etiquetes directes i separadors blancs;
  - text fosc sobre els grisos i blanc sobre el blau.
- **Text:**
  - títol calculat: «Quan el mòbil no carrega, gairebé 4 de cada 10 vegades era el port o el carregador, no la bateria»;
  - subtítol amb el filtre i el període;
  - n a cada fila;
  - font al peu.
- **Interacció:** cap. L'estat per defecte ja respon la pregunta.

**Idioms descartats:**

| Idiom | Motiu | Regla |
|---|---|---|
| `multiset_barchart` (decisió desada `compare-two-keys--grouped-bars-few-few`, *seed*) | separa les parts i amaga que sumen el total del símptoma | EXP-05 |
| `stacked_bar_graph` amb 7 avaries (versió anterior) | 7 colors i llegenda per a un argument de 3 parts; destacava l'element contrari al missatge | COL-04, EFF-09 |
| `error_bars` (punt amb interval del % que no és la bateria) | mostra la incertesa però perd la composició; amb n = 42, es dona la n a l'etiqueta | PUR-02 |

**Validació** (amenaça: idiom equivocat):

a. **Llista de regles:**
- EXP-05 i EXP-08: compleixen.
- COL-04: compleix (3 colors).
- COL-05: compleix (`colorcheck` i simulacions).
- TXT-01 i TXT-02: el títol diu la conclusió.
- TXT-04: etiquetes directes, sense llegenda.
- TXT-08: font i n.
- DAT-03: recomptes en lloc d'interval. És una decisió presa amb consciència, i l'entrada diu que la mostra és petita.

b. **Temps per tasca:**
- *gist*: immediat;
- comparar el port entre files: immediat (base comuna);
- recuperar valors: immediat (etiquetes).

c. **Imatge inspeccionada:** `inspect_image.py` no dona cap troballa. En escala de grisos els tres segments se separen per lluminositat, i amb deuteranopia el blau se separa dels grisos.

d. **Crítica:** aplica totes les troballes majors de la crítica anterior (`vis-value-critique`).

e. **Acceptació del lector:** acceptada per l'usuari l'11/11/2026, sense canvis. El registre passa a `declared`.

## 4. Algorisme

- **Pipeline:** matplotlib 3.10, en un script amb `load → derive → build_chart → save`, que el quadern 03 importa amb `importlib`.
- **Files:** 1.916 a l'entrada i 6 a la taula final (2 símptomes × 3 grups).
- **Llibreries descartades:** cap. Es manté matplotlib per coherència amb la resta de figures de l'entrada.
- **Validació** (amenaça: algorisme equivocat):
  - `run_check.py`: el codi s'executa sense errors, l'inspector executa l'script i no hi ha troballes que bloquegin.
  - SCL-06 («l'eix x no té títol») es descarta: és intencionat, perquè els valors van etiquetats (excepció de TXT-04).
  - TXT-01 va sortir en una primera versió amb el títol a `ax.set_title(loc="left")` i es va resoldre amb `fig.suptitle`.
  - La imatge coincideix amb l'etapa 3.

## 5. Registre de decisió

Desat a `.claude/vis-decisions/p-compare-two-keys--avaria-real-darrere-dels-s-20261111-2.yaml` (estat `declared`), que substitueix `p-compare-two-keys--avaria-real-darrere-dels-s-20261111`. La còpia JSON és a `record.json`, en aquesta carpeta.

## 6. Supòsits i punts oberts

- **S1 i S2** (lector, mode, pregunta, dades): són les que dona el prompt de l'usuari, que fixa el disseny. No s'han preguntat per separat.
- **S4** (llibreria): matplotlib, la que ja hi ha a `project.yaml` i la que indica el prompt.
- **V3** (acceptació de la imatge): acceptada per l'usuari l'11/11/2026.
- **Punt obert:** amb n = 42, el 38 % té un interval aproximat del 24 % al 54 %. L'entrada ho diu com a indici.
