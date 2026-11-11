"""Descarrega les dades d'Open Repair Alliance (ORDS v0.3) a dades/raw/.

Les dades són CC BY-SA 4.0: qualsevol conjunt derivat que publiquem
hereta la llicència. No es pugen al repositori (vegeu .gitignore).

Ús, des de l'arrel del repositori:
    python3 posts/vida-material/_analisi/scripts/01_descarrega_ora.py
"""

from pathlib import Path
from urllib.request import urlretrieve

# Versió fixada perquè l'anàlisi sigui reproduïble. Si se'n publica una de
# nova, canvieu-ho aquí i anoteu-ho al README de _analisi.
VERSIO = "202607"
BASE = "https://media.githubusercontent.com/media/openrepair/data/main"
FITXERS = {
    f"OpenRepairData_v0.3_aggregate_{VERSIO}_eee.csv": "ora_aggregate.csv",
    "quests/mobiles/mobifix.csv": "ora_mobifix.csv",
}

RAW = Path(__file__).resolve().parents[1] / "dades" / "raw"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for remot, local in FITXERS.items():
        desti = RAW / local
        if desti.exists():
            print(f"Ja existeix: {desti.name}")
            continue
        print(f"Descarregant {remot} ...")
        urlretrieve(f"{BASE}/{remot}", desti)
        print(f"  {desti.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
