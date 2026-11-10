"""Exploració inicial dels mòbils d'Open Repair (fase 0 del disseny).

Reprodueix les xifres de l'apartat "Què hem comprovat" de l'entrada.
Cal haver executat abans 01_descarrega_ora.py.
"""

from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "dades" / "raw"


def main():
    d = pd.read_csv(RAW / "ora_aggregate.csv", low_memory=False)
    m = d[d["product_category"] == "Mobile"].copy()
    m["age"] = pd.to_numeric(m["product_age"], errors="coerce")
    m["any_event"] = m["event_date"].str[:4]

    print(f"Registres totals: {len(d):,}")
    print(f"Mòbils: {len(m):,}")
    print(f"Amb edat: {m['age'].notna().sum():,}")
    print(f"Marca desconeguda: {(m['brand'] == 'Unknown').sum():,}")
    print(f"Amb descripció del problema: {m['problem'].notna().sum():,}")

    print("\nEstat de la reparació:")
    print(m["repair_status"].value_counts())

    print("\nEdat (anys) segons l'estat de la reparació:")
    print(m.groupby("repair_status")["age"].describe()[["count", "50%", "25%", "75%"]])

    print("\nEdat mediana segons l'any de l'esdeveniment:")
    print(m.groupby("any_event")["age"].agg(["count", "median"]).dropna())

    print("\nRegistres amb edat segons el proveïdor (la manca d'edat no és aleatòria):")
    print(m.groupby("data_provider")["age"].agg(lambda s: f"{s.notna().sum()}/{len(s)}"))

    print("\nMotiu de fi de vida (només 'End of life'):")
    print(m["repair_barrier_if_end_of_life"].value_counts())


if __name__ == "__main__":
    main()
