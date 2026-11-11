# Anàlisi de la vida material dels mòbils

Codi i dades de treball de l'entrada `posts/vida-material/index.qmd`. Com que la carpeta comença amb guió baix, Quarto no la publica.

## Requisits

Python 3.10 o posterior amb `pandas` i `matplotlib`. Per als models caldran també `statsmodels` i `scikit-learn`.

## Com reproduir-ho

Des de l'arrel del repositori:

```bash
python3 posts/vida-material/_analisi/scripts/01_descarrega_ora.py
python3 posts/vida-material/_analisi/scripts/02_exploracio_ora.py
python3 posts/vida-material/_analisi/scripts/03_sankey_mobifix.py
python3 posts/vida-material/_analisi/scripts/04_causes_per_any.py
python3 posts/vida-material/_analisi/scripts/05_b1_simptomes.py
python3 posts/vida-material/_analisi/scripts/06_b2_edat_bateria.py
python3 posts/vida-material/_analisi/scripts/07_b3_resultat.py
```

El primer script descarrega les dades d'Open Repair (uns 80 MB) a `dades/raw/`, que no es puja a git. El segon fa l'exploració inicial dels mòbils. El tercer i el quart generen el gràfic de Sankey i el mapa de calor de causes per any de l'entrada `posts/avaries-mobil` i n'imprimeixen les xifres. Els tres últims generen les figures 1, 2 i 3 de l'entrada (`b1_simptomes`, `b2_edat_bateria` i `b3_resultat`, en PNG i SVG). Els de les figures 2 i 3 necessiten haver executat abans els quaderns 01 i 02, que creen `dades/processades/`.

## Dades

| Fitxer | Origen | Llicència |
|---|---|---|
| `dades/raw/ora_aggregate.csv` | Open Repair Alliance, ORDS v0.3, versió 202607 | CC BY-SA 4.0 |
| `dades/raw/ora_mobifix.csv` | Open Repair Alliance, classificació MobiFix | CC BY-SA 4.0 |

Qualsevol conjunt derivat d'aquestes dades que es publiqui ha de tenir la mateixa llicència i citar-ne l'origen.