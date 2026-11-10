# Anàlisi de la vida material dels mòbils

Codi i dades de treball de l'entrada `posts/vida-material/index.qmd`. Com que la carpeta comença amb guió baix, Quarto no la publica.

## Requisits

Python 3.10 o posterior amb `pandas`. Per als models caldran també `statsmodels` i `scikit-learn`.

## Com reproduir-ho

Des de l'arrel del repositori:

```bash
python3 posts/vida-material/_analisi/scripts/01_descarrega_ora.py
python3 posts/vida-material/_analisi/scripts/02_exploracio_ora.py
```

El primer script descarrega les dades d'Open Repair (uns 80 MB) a `dades/raw/`, que no es puja a git. El segon imprimeix les xifres de l'apartat 3 de l'entrada.

## Dades

| Fitxer | Origen | Llicència |
|---|---|---|
| `dades/raw/ora_aggregate.csv` | Open Repair Alliance, ORDS v0.3, versió 202607 | CC BY-SA 4.0 |
| `dades/raw/ora_mobifix.csv` | Open Repair Alliance, classificació MobiFix | CC BY-SA 4.0 |

Qualsevol conjunt derivat d'aquestes dades que es publiqui ha de tenir la mateixa llicència i citar-ne l'origen.