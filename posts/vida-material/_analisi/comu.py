"""Càrrega i neteja compartides pels quaderns de l'anàlisi.

Implementa els passos 1 a 4 de l'apartat 4 de posts/vida-material/index.qmd.
Cal haver executat abans scripts/01_descarrega_ora.py.
"""

import re
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


def normalitza_text(text):
    """Text en minúscules i sense puntuació, per creuar MobiFix amb el conjunt agregat."""
    if pd.isna(text):
        return ""
    return re.sub(r"[^\w]+", " ", str(text).lower()).strip()


def agrupa_rars(serie, minim=30, nom="Altres"):
    """Posa a `nom` les categories amb menys de `minim` registres."""
    freq = serie.value_counts()
    return serie.where(~serie.isin(freq[freq < minim].index), nom)


def carrega_classificats():
    """Smartphones nets amb el tipus d'avaria (sortida del quadern 04)."""
    return pd.read_csv(PROCESSADES / "mobils_classificats.csv")


# Símptomes de bateria en el text lliure (anglès, alemany, neerlandès, francès,
# castellà i danès/noruec). Són paraules clau: el quadern 03 en comprova una
# mostra a mà. "mencio_bateria" no és un símptoma: serveix per separar els textos
# que ja porten el diagnòstic del voluntari.
SIMPTOMES = {
    "no_carrega": r"not charg|won.?t charge|doesn.?t charge|does not charge|no charg|not taking charge"
                  r"|not charging|charging (?:issue|problem|fault)|charge issue|lädt nicht|lädt schlecht|nicht laden"
                  r"|kann nicht geladen|wird nicht geladen|ladeproblem|laadt niet|laadt slecht|laadprobleem"
                  r"|ne charge|ne se charge|no carga|no carrega|lader ikke",
    "dura_poc": r"drain|doesn.?t hold|not hold|won.?t hold|loses charge|battery life|battery weak|weak battery"
                r"|hält nicht|hält kaum|akku schwach|akkulaufzeit|ontlaadt|snel leeg|tient pas|se décharge"
                r"|dura poco|holder ikke",
    "no_sencen": r"won.?t turn on|not turn on|doesn.?t turn on|no power|completely dead|dead phone"
                 r"|geht nicht an|startet nicht|nicht einschalten|gaat niet aan|ne s.?allume|no enciende"
                 r"|not switching on|not starting|won.?t start|keine funktion|doet het niet|ne démarre"
                 r"|tænder ikke|starter ikke",
    "inflada": r"swollen|swell|bulg|bloated|expanded|geschwollen|aufgebläht|opgezwollen|gonfl|hinchad|oppust|opsvulm",
}
MENCIO_BATERIA = r"batter|akku|\baccu|batería|bateria|batterij"


def simptomes(textos):
    """Taula booleana amb un símptoma de bateria per columna i la menció de bateria."""
    t = textos.fillna("").str.lower()
    taula = pd.DataFrame({nom: t.str.contains(patro, regex=True) for nom, patro in SIMPTOMES.items()})
    taula["algun_simptoma"] = taula.any(axis=1)
    taula["mencio_bateria"] = t.str.contains(MENCIO_BATERIA, regex=True)
    return taula
