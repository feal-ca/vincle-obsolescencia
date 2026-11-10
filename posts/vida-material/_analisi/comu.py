"""Càrrega i neteja compartides pels quaderns de l'anàlisi.

Implementa els passos 1 a 4 de l'apartat 4 de posts/vida-material/index.qmd.
Cal haver executat abans scripts/01_descarrega_ora.py.
"""

from pathlib import Path

import pandas as pd

ARREL = Path(__file__).resolve().parent
RAW = ARREL / "dades" / "raw"
PROCESSADES = ARREL / "dades" / "processades"

# Còpia de GRUPS de scripts/03_sankey_mobifix.py: si en canvieu un, canvieu l'altre.
GRUPS = {
    "Screen": "Pantalla",
    "Power/battery": "Bateria i alimentació",
    "Charger": "Bateria i alimentació",
    "USB/charging port": "Port de càrrega",
    "Other buttons": "Botons i connectors",
    "On/Off button": "Botons i connectors",
    "Volume buttons": "Botons i connectors",
    "Headphone jack": "Botons i connectors",
    "Sim card slot": "Botons i connectors",
    "Memory card slot": "Botons i connectors",
    "Internal damage": "Danys interns i aigua",
    "External damage": "Danys interns i aigua",
    "Liquid damage": "Danys interns i aigua",
    "Help/configuration": "Programari i configuració",
    "Software update": "Programari i configuració",
    "Software issue": "Programari i configuració",
    "Storage problem": "Programari i configuració",
    "Stuck booting": "Programari i configuració",
    "Performance": "Programari i configuració",
    "Access issue": "Programari i configuració",
    "Camera": "Altres",
    "Speaker/amplifier": "Altres",
    "Microphone": "Altres",
    "Other": "Altres",
    "Unknown": "Desconegut",
}

# Sinònims de marca, en minúscules. La resta es posa amb majúscula inicial.
MARQUES = {
    "apple": "Apple",
    "iphone": "Apple",
    "i-phone": "Apple",
    "i phone": "Apple",
    "samsung": "Samsung",
    "huawei": "Huawei",
    "honor": "Huawei",
    "xiaomi": "Xiaomi",
    "redmi": "Xiaomi",
    "fairphone": "Fairphone",
    "lg": "LG",
    "htc": "HTC",
    "oneplus": "OnePlus",
    "sony": "Sony",
    "sony ericsson": "Sony",
    "google": "Google",
    "motorola": "Motorola",
    "nokia": "Nokia",
    "unknown": "Desconeguda",
}

# Filtre provisional de telèfons que no són smartphones: cal revisar-lo a mà
# amb el quadern 01 abans de fer servir els models. "Mobiltelefon" (danès i
# noruec) vol dir mòbil i es queda; "Telefon" sol a "Elektro divers" o
# "Andet" (altres) sol ser un telèfon fix.
NO_SMARTPHONE_CATEGORIA = r"not smartphone|(?:elektro divers|andet) ~ telefon$|festnetz|landline|dect"
NO_SMARTPHONE_MARCA = {"Doro", "Gigaset", "Siemens"}

EDAT_MAXIMA = 15
MIN_REGISTRES_MARCA = 50


def carrega_aggregate():
    """Mòbils del conjunt agregat d'Open Repair, amb edat i any numèrics."""
    d = pd.read_csv(RAW / "ora_aggregate.csv", low_memory=False)
    m = d[d["product_category"] == "Mobile"].copy()
    m["edat"] = pd.to_numeric(m["product_age"], errors="coerce")
    m["any_event"] = pd.to_numeric(m["event_date"].str[:4], errors="coerce")
    return m


def normalitza_marca(marca):
    if pd.isna(marca) or not str(marca).strip():
        return "Desconeguda"
    clau = str(marca).strip().lower()
    return MARQUES.get(clau, str(marca).strip().title())


def neteja(m):
    """Retorna (dades netes, recompte de registres a cada pas)."""
    passos = [("Mòbils", len(m))]

    m = m[m["repair_status"] != "Unknown"].copy()
    passos.append(("Amb estat de la reparació conegut", len(m)))

    m["marca"] = m["brand"].map(normalitza_marca)
    categoria = m["partner_product_category"].str.contains(
        NO_SMARTPHONE_CATEGORIA, case=False, na=False
    )
    m["es_smartphone"] = ~(categoria | m["marca"].isin(NO_SMARTPHONE_MARCA))
    m = m[m["es_smartphone"]].copy()
    passos.append(("Smartphones (filtre provisional)", len(m)))

    freq = m["marca"].value_counts()
    poc_freqüents = freq[freq < MIN_REGISTRES_MARCA].index
    m.loc[m["marca"].isin(poc_freqüents), "marca"] = "Altres"

    m["edat_neta"] = m["edat"].where(m["edat"] <= EDAT_MAXIMA)
    passos.append(("... dels quals amb edat", int(m["edat"].notna().sum())))
    passos.append(("... dels quals amb edat ≤ 15 anys", int(m["edat_neta"].notna().sum())))

    m["final_vida"] = (m["repair_status"] == "End of life").astype(int)
    passos.append(("... dels quals a final de vida", int(m["final_vida"].sum())))

    recompte = pd.DataFrame(passos, columns=["pas", "registres"])
    return m, recompte


def carrega_mobifix():
    """Classificació MobiFix, amb el grup d'avaria i l'edat numèrica."""
    f = pd.read_csv(RAW / "ora_mobifix.csv")
    f["grup_avaria"] = f["fault_type"].map(GRUPS).fillna("Altres")
    f["edat"] = pd.to_numeric(f["age"], errors="coerce")
    f["edat_neta"] = f["edat"].where(f["edat"] <= EDAT_MAXIMA)
    f["any_event"] = pd.to_numeric(f["event_date"].str[:4], errors="coerce")
    f["marca"] = f["brand"].map(normalitza_marca)
    return f
