# Disseny: «La bateria acaba a final de vida més del doble de vegades que la pantalla, i només el 39 % es repara el mateix dia»

| | |
|---|---|
| Registre de decisió | `p-compare-two-keys--com-acaben-les-reparacions-de-20261111-3` · estat `declared`; substitueix la `-2` (paleta semàfor) i la versió sense sufix (dos panells), cap de les dues acceptades |
| Llibreria / host | Altair 6.3 + vl-convert 1.9 (`project.yaml`) · script que desa PNG i SVG a l'entrada, i HTML i Vega-Lite en aquesta carpeta; el quadern 05 l'importa |
| Dades | `../../dades/processades/mobils_classificats.csv`, 5.652 files; signatura `table\|k:categorical:few+k:categorical:few\|v:quantitative:share` |
| Sortides | `scripts/07_b3_resultat.py`, `posts/vida-material/b3_resultat.png` (i `.svg`) |
| Idioma | diàleg es · text del gràfic ca · codi en/ca |

## 1. Caracterització del problema

- **Lector:** públic general (lectors del blog): poca formació en gràfics, segons per mirar-lo, pantalla. Modificadors: daltonisme (`cvd`) i lectura en gris (`print-grayscale`).
- **Mode:** explicatiu, estàtic.
- **Pregunta:** «Per què les reparacions de bateria acaben sense arreglar més que les de pantalla?» La figura respon la part que les dades permeten (com acaben); el «per què» va al text, perquè el motiu gairebé mai no consta.
- **Lectures descartades:** el panell de motius de la versió anterior. L'usuari no la va acceptar perquè tenia massa barres.
- **Validació** (amenaça: problema equivocat): l'usuari va confirmar el resum de les etapes 1 i 2 i, a la iteració, va demanar mantenir només la representació de les proporcions. No s'ha observat cap lector real.

## 2. Abstracció de dades i tasques

| Atribut | Tipus | Rol | Nivells / rang | Notes |
|---|---|---|---|---|
| Component | categòric | clau | 2 (bateria, pantalla) | `grup_avaria` |
| Resultat | categòric ordenat | clau 2 | 3 (final de vida, pendent, reparat) | `repair_status` |
| Proporció | quantitatiu (*share*) | valor derivat | 0–100 % | recompte / total del component |

- **Filtres:** MobiFix amb resultat conegut: bateria n = 200, pantalla n = 584, 2013–2020.
- **Tasques:** presentar i comparar. A nivell baix: *gist*, comparar el final de vida i el reparat entre components, i recuperar valors.
- **Validació** (amenaça: abstracció equivocada): confirmada per l'usuari.

## 3. Codificació visual

**Idiom:** `stacked_bar_graph`, barres horitzontals al 100 %, reutilitzant l'estructura de la decisió de B1.

| Atribut | Marca + canal | Rang (Mackinlay) | Expressivitat |
|---|---|---|---|
| Component | posició vertical | 1r per a nominals | etiqueta en negre amb la n |
| Proporció | longitud des de la base comuna | 1r–3r | les parts sumen 100 % (EXP-05) |
| Resultat | to (pastels de la mateixa lluminositat) | adequat per a 3 nivells | dolent (corall), a mitges (lavanda) i bo (aigua) |

- **Ordenació:** final de vida, pendent i reparat; el final de vida parteix de la base comuna.
- **Color:**
  - finalitat: codificar el resultat amb la connotació que va demanar l'usuari (dolent, a mitges, bo), en pastels de la mateixa lluminositat (J' = 78 a CAM02-UCS);
  - colors: `#f99e7e` corall (final de vida), `#b4b4f8` lavanda (pendent), `#69cec4` aigua (reparat). El text dels segments és negre (contrast ≥ 9:1);
  - **comprovació de daltonisme:** amb colorspacious 1.1 (simulació de Machado et al. al 100 %) i distàncies ΔE a CAM02-UCS, entre unes 900 combinacions de to amb la mateixa lluminositat s'ha triat la que maximitza la distància mínima en visió normal, deuteranopia, protanopia i tritanopia;

    | Visió | ΔE mínima entre segments |
    |---|---|
    | Normal | 29,7 |
    | Deuteranopia | 15,2 |
    | Protanopia | 16,4 |
    | Tritanopia | 16,4 |

  - **limitació:** com que la lluminositat és la mateixa, en grisos els tres pastels són iguals. La segona pista és el nom de cada segment a sobre, en una versió fosca del mateix to (`#b5502f`, `#5a5ab0`, `#1f7a70`, contrast ≥ 5:1 sobre blanc), i els separadors blancs;
  - les etiquetes de fila van en negre (decisió de l'usuari), perquè el vermelló de la bateria de B2 no es confongui amb el final de vida.
- **Text:**
  - títol calculat: «La bateria acaba a final de vida més del doble de vegades que la pantalla, i només el 39 % es repara el mateix dia»;
  - subtítol amb el període;
  - percentatges als segments i «final de vida: 26 de 200» a la dreta;
  - peu amb la font i la definició de «Pendent».
- **Interacció:** cap.

**Idioms descartats:**

| Idiom | Motiu | Regla |
|---|---|---|
| Dos panells (resultat i motius) | no acceptada per l'usuari: massa barres al panell de motius i el resultat en grisos sense connotació | CLT-02 |
| Versió original d'un sol panell | «Reparable» es llegia al revés; sense títol ni font | TXT-07, TXT-01 |
| `multiset_barchart` (llavor `compare-two-keys--grouped-bars-few-few`) | separa les parts i amaga que sumen el total del component | EXP-05 |
| Paleta Okabe-Ito (vermelló, groc, verd blavós) | el vermelló i el verd tenen la mateixa lluminositat i el vermelló és la bateria a B2 | COL-08 |
| Paleta semàfor (`#b2182b`, `#f4c542`, `#1b9e77`) | l'usuari la va trobar massa semàfor; a més, vermell i verd quedaven a ΔE 20 en deuteranopia. La comprovació anterior amb CIE76 i el llindar de l'inspector no ho detectava bé | COL-05 |
| Granat, sorra i verd blavós (`#8e2a4a`, `#e4d9b8`, `#3f9f90`) | la més robusta (ΔE mínima 24 i distingible en grisos), però l'usuari la va trobar descolorida i grisosa | PUR-13 |

**Validació** (amenaça: idiom equivocat):

a. **Llista de regles:** EXP-05, EXP-08, TXT-01, TXT-04, TXT-07 («Pendent» definit), TXT-08, COL-05, COL-08 i DAT-03 (recomptes del final de vida).

b. **Temps per tasca:**
- *gist*: immediat;
- comparar el final de vida: immediat (base comuna);
- recuperar valors: immediat (etiquetes).

c. **Imatge inspeccionada:** a més de `inspect_image.py`, la imatge final s'ha simulat sencera amb colorspacious (deuteranopia, protanopia i tritanopia al 100 %, i lluminositat J'). Els tres segments es distingeixen a les tres simulacions i són iguals en grisos, com s'esperava.

d. **Crítica:** aplica les troballes de la crítica que afecten aquesta representació.

e. **Acceptació del lector:** després de dues iteracions de paleta (semàfor i granat), l'usuari va acceptar els pastels l'11/11/2026. Les etiquetes de fila van en negre.

## 4. Algorisme

- **Pipeline:** Altair 6.3, en un script amb `load → derive → build_chart → save`: un `layer` de barres i texts i un `vconcat` amb la línia del peu.
- **Validació** (amenaça: algorisme equivocat): l'script s'executa sense errors i el quadern 05 s'executa sencer amb `nbclient`.

## 5. Registre de decisió

Desat a `.claude/vis-decisions/p-compare-two-keys--com-acaben-les-reparacions-de-20261111-3.yaml` (estat `declared`), que substitueix la `-2`, que al seu torn substituïa la versió sense sufix. La còpia JSON és a `record.json`, en aquesta carpeta.

## 6. Supòsits i punts oberts

- **Motius dels finals de vida:** queden al text, amb els recomptes (57 de 89 sense motiu a la bateria i 56 de 87 a la pantalla).
- **Grup de la bateria:** «Bateria i alimentació» inclou 9 reparacions de carregador a MobiFix, cap amb final de vida.
- **Coherència entre figures:** a B2 el vermelló és la bateria; aquí el vermell és el final de vida. Les etiquetes en negre ho atenuen.
- **Impressió en blanc i negre:** amb pastels de la mateixa lluminositat, el resultat només es llegeix pels noms dels segments.
