"""La pantalla explica una part estable de les avaries cada any (mapa de calor causa × any)

Decision record: p-part-to-whole-over-time--distribuci-anual-de-les-20261111 (substitueix -20261110: paleta)  ·  Design document: posts/vida-material/_analisi/disseny/causes_per_any_design.md
Library: matplotlib  ·  Generated: 2026-11-10  ·  Paleta revisada: 2026-11-11
Question: Quina és la causa d'avaria dels mòbils en cada any i com canvia, any rere any, la
distribució de causes?

Escriu posts/avaries-mobil/causes_per_any.png a partir dels 1.842 registres de MobiFix amb
resultat conegut i imprimeix les xifres que en cita el text de l'entrada (avaries i resultats).

Ús, des de l'arrel del repositori:
    python3 posts/vida-material/_analisi/scripts/04_causes_per_any.py
"""
from __future__ import annotations

import argparse
import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, to_rgb  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

# ---------------------------------------------------------------- CONFIG
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "..", "dades", "raw", "ora_mobifix.csv")  # relatiu a l'script
OUT_DIR = os.path.join(_HERE, "..", "..", "..", "avaries-mobil")
SLUG = "causes_per_any"
LANG = "ca"
COLUMNS = {"time": "event_date", "category": "fault_type", "status": "repair_status"}
PARSE = {"sep": ",", "decimal": ".", "encoding": "utf-8"}

RESULTATS_CONEGUTS = ["Fixed", "Repairable", "End of life"]
MIN_N = 80  # per sota, un percentatge anual són uns pocs casos: es marca amb asterisc

# Mateixos grups que l'apartat 3 de posts/vida-material/index.qmd. La càmera, l'altaveu i el
# micròfon (86 casos) van a "Altres", igual que "Other".
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
# Per freqüència total; "Altres" i "Desconegut" al final, separades: no diuen cap causa.
ORDRE_CAUSES = [
    "Pantalla",
    "Bateria i alimentació",
    "Programari i configuració",
    "Botons i connectors",
    "Port de càrrega",
    "Danys interns i aigua",
    "Altres",
    "Desconegut",
]
N_INFORMADES = 6
TOT = "Tot"
MESOS = ["gener", "febrer", "març", "abril", "maig", "juny", "juliol", "agost", "setembre", "octubre",
         "novembre", "desembre"]

# ---------------------------------------------------------------- PALETTE
# Paleta de poblacio_mobils_uk.png. El mapa de calor fa servir la família blava (#A9C1DD, #7FA7D1)
# estesa als dos extrems: L* 96 → 42 en passos de 10–12, llegible en gris i amb daltonisme. Les
# barres del nombre de reparacions van en coral, el color de les avaries al segon gràfic.
VMAX = 40.0  # escala comuna a totes les cel·les (el màxim real és el 37 %)
SEQUENTIAL = ["#EEF3F9", "#D3E0EF", "#A9C1DD", "#7FA7D1", "#5A86B8", "#3B6596"]
INK, INK2, FONS = "#333333", "#6b6b6b", "#FBFAF7"
BARRA, BARRA_PETITA = "#DE9483", "#EDBBAE"
ACCENT = "#5B6573"  # gris pissarra de les marques d'escenari del segon gràfic


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=PARSE["sep"], decimal=PARSE["decimal"], encoding=PARSE["encoding"])
    missing = [c for c in COLUMNS.values() if c not in df.columns]
    assert not missing, f"missing columns: {missing}"
    assert len(df) > 0, "empty dataset"
    print(f"loaded {len(df)} rows from {path}")
    return df


def derive(df: pd.DataFrame) -> pd.DataFrame:
    """Reparacions per (causa, any) amb una columna 'Tot'. Es normalitza a build_chart()."""
    last = df["event_date"].max()
    k = df[df["repair_status"].isin(RESULTATS_CONEGUTS)].copy()  # només els que tenen resultat conegut
    k["any"] = k["event_date"].str[:4].astype(int).clip(lower=2013)  # 2012 només té 1 cas
    k["causa"] = k["fault_type"].map(GRUPS)
    assert k["causa"].notna().all(), "tipus d'avaria sense grup"
    anys = sorted(k["any"].unique())
    t = pd.crosstab(k["causa"], k["any"]).reindex(index=ORDRE_CAUSES, columns=anys, fill_value=0)
    t[TOT] = t.sum(axis=1)
    t.attrs["last_date"] = last
    t.attrs["dropped"] = len(df) - len(k)
    print(f"rows after derivation: {len(k)} (sense resultat conegut: {len(df) - len(k)})")
    return t


def xifres(df: pd.DataFrame) -> None:
    """Imprimeix les xifres que cita el text de posts/avaries-mobil."""
    resultats = {"Fixed": "Reparat", "Repairable": "Reparable", "End of life": "Final de vida"}
    k = df[df["repair_status"].isin(RESULTATS_CONEGUTS)].copy()
    k["causa"] = k["fault_type"].map(GRUPS)
    k["resultat"] = k["repair_status"].map(resultats)
    print(f"Reparacions de mòbil a MobiFix: {len(df):,}")
    print(f"  sense resultat conegut (fora del gràfic): {len(df) - len(k)}")
    print(f"  al gràfic: {len(k):,}")
    print(f"Proveïdor The Restart Project: {(df['data_provider'] == 'The Restart Project').mean():.1%}")
    print(f"Pantalla: {(k['causa'] == 'Pantalla').sum()} ({(k['causa'] == 'Pantalla').mean():.1%})")
    print(f"Desconegut: {(k['causa'] == 'Desconegut').sum()} ({(k['causa'] == 'Desconegut').mean():.1%})")
    print("Resultat:\n", k["resultat"].value_counts().to_string())
    print(k["resultat"].value_counts(normalize=True).round(3).to_string())
    t = pd.crosstab(k["causa"], k["resultat"])
    t["n"] = t.sum(axis=1)
    t["%final"] = (t["Final de vida"] / t["n"] * 100).round(1)
    print(t.loc[ORDRE_CAUSES].to_string())
    anys = df["event_date"].str[:4].astype(int).clip(lower=2013)  # 2012 només té 1 cas
    print("Registres per any:\n", anys.value_counts().sort_index().to_string())


def shares(t: pd.DataFrame) -> pd.DataFrame:
    return t / t.sum(axis=0) * 100  # cada columna suma 100 %


def milers(x) -> str:
    return f"{int(x):,}".replace(",", ".")


def etiq(a) -> str:
    return TOT if a == TOT else ("2012–13" if a == 2013 else str(a))


def fiables(t: pd.DataFrame) -> list:
    n = t.sum(axis=0)
    return [a for a in t.columns if a != TOT and n[a] >= MIN_N]


def takeaway(df: pd.DataFrame) -> str:
    """Títol calculat amb les dades (mai una xifra literal)."""
    p = shares(df).loc["Pantalla"]
    f = fiables(df)
    lo, hi = min(p[a] for a in f), max(p[a] for a in f)
    return (f"La pantalla explica entre el {lo:.0f} % i el {hi:.0f} % de les avaries de mòbil "
            f"cada any ({min(f)}–{max(f)})")


def nota_desconegut(df: pd.DataFrame) -> str:
    d = shares(df).loc["Desconegut"]
    f = fiables(df)
    a = max(f, key=lambda x: d[x])
    return (f"«Desconegut» són reparacions sense causa registrada: arriba al {d[a]:.0f} % el {a} "
            f"i en aquest any pot amagar altres causes.")


def _lum(rgb) -> float:
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb[:3]]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def text_sobre(fons) -> str:
    """Blanc o gris fosc segons el contrast (WCAG) amb el color de la cel·la. A la zona on tots dos
    queden prop de 3,5:1 es prefereix el blanc, perquè cel·les veïnes de valor semblant no canviïn."""
    lf = _lum(fons)
    blanc = 1.05 / (lf + 0.05)
    fosc = (lf + 0.05) / (_lum(to_rgb(INK)) + 0.05)
    return "white" if blanc >= 0.8 * fosc else INK


def build_chart(df: pd.DataFrame):
    pct = shares(df)
    n = df.sum(axis=0)
    cols = list(df.columns)
    ncau = len(ORDRE_CAUSES)
    X = {a: i for i, a in enumerate(cols[:-1])}
    X[TOT] = len(cols) - 1 + 0.7  # buit abans de la columna de totals
    Y = {c: i + (0.4 if i >= N_INFORMADES else 0) for i, c in enumerate(ORDRE_CAUSES)}
    cmap = LinearSegmentedColormap.from_list("coral", SEQUENTIAL)

    fig = plt.figure(figsize=(11, 7.4), facecolor=FONS)
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 7.2], hspace=0.16, left=0.205, right=0.93, top=0.82, bottom=0.12)
    axb = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1], sharex=axb)
    xlim = (-0.55, X[TOT] + 0.55)
    ax.set_xlim(*xlim)
    for a_ in (ax, axb):
        a_.set_facecolor(FONS)

    # --- barres amb el nombre de reparacions de cada any (volum, en una escala pròpia des de zero)
    petit = {a: n[a] < MIN_N for a in cols}
    nmax = max(n[a] for a in cols if a != TOT)
    for a in cols:
        if a == TOT:
            axb.text(X[a], 0.05 * nmax, milers(n[a]), ha="center", va="bottom",
                     fontsize=10, color=INK2, fontweight="bold")
            continue
        axb.bar(X[a], n[a], width=0.84, color=BARRA_PETITA if petit[a] else BARRA,
                hatch="///" if petit[a] else None, edgecolor="white", linewidth=0)
        axb.text(X[a], n[a] + 0.04 * nmax, f"{int(n[a])}", ha="center", va="bottom", fontsize=10, color=INK2)
    axb.set_ylim(0, nmax * 1.35)
    axb.axis("off")
    axb.text(-0.7, 0, "Reparacions (n)", ha="right", va="bottom", fontsize=10.5, color=INK2)

    # --- mapa de calor: % de les reparacions de l'any per tipus d'avaria
    for c in ORDRE_CAUSES:
        for a in cols:
            v = pct.loc[c, a]
            fons = cmap(0.06 + 0.94 * min(v / VMAX, 1))
            ax.add_patch(Rectangle((X[a] - 0.47, Y[c] - 0.47), 0.94, 0.94, facecolor=fons, lw=0))
            ax.text(X[a], Y[c], f"{v:.0f}", ha="center", va="center", fontsize=11.5,
                    color=text_sobre(fons), fontweight="bold" if c == "Pantalla" else "normal")

    # un sol ressalt: la fila de la pantalla, que és el missatge del títol
    ax.add_patch(Rectangle((X[cols[0]] - 0.5, Y["Pantalla"] - 0.5), X[cols[-2]] - X[cols[0]] + 1.0, 1.0,
                           fill=False, edgecolor=ACCENT, lw=2.0, clip_on=False))

    ax.set_ylim(Y[ORDRE_CAUSES[-1]] + 0.6, -0.6)
    ax.set_yticks([Y[c] for c in ORDRE_CAUSES], labels=ORDRE_CAUSES)
    ax.get_yticklabels()[0].set_fontweight("bold")
    ax.set_xticks([X[a] for a in cols], labels=[etiq(a) + ("*" if petit[a] and a != TOT else "") for a in cols])
    ax.xaxis.tick_top()
    ax.tick_params(length=0, labelsize=11, labelcolor=INK)
    ax.tick_params(axis="y", pad=8)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(xlim[1] + 0.05, (Y["Altres"] + Y["Desconegut"]) / 2, "sense causa\nconcreta", ha="left",
            va="center", fontsize=9, color=INK2, linespacing=1.2, clip_on=False)

    # --- text: títol amb el missatge, subtítol, nota i font
    titol = textwrap.fill(takeaway(df), 80)
    fig.text(0.01, 0.975, titol, ha="left", va="top", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.01, 0.885, "Percentatge de les reparacions de mòbil de cada any segons el tipus d'avaria. "
             "Cada columna suma 100 %; com més fosc, més pes.", ha="left", va="top", fontsize=10.5, color=INK2)
    ult = df.attrs["last_date"]
    mes = f"{MESOS[int(ult[5:7]) - 1]} del {ult[:4]}"
    peu = (f"* Menys de {MIN_N} reparacions: els percentatges són pocs casos. Les dades arriben fins a {mes}.\n"
           f"{nota_desconegut(df)}\n"
           f"Font: elaboració pròpia a partir d'Open Repair Alliance (MobiFix), CC BY-SA 4.0. "
           f"n = {milers(n[TOT])} reparacions amb resultat conegut del {etiq(cols[0])[:4]} al {cols[-2]} "
           f"(se n'exclouen {df.attrs['dropped']}). «Tot» agrupa tots els anys.")
    fig.text(0.01, 0.015, peu, ha="left", va="bottom", fontsize=9, color=INK2, linespacing=1.5)
    return fig


def save(fig, out_dir: str, slug: str) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, f"{slug}.png")
    fig.savefig(png, dpi=200, bbox_inches="tight", facecolor=FONS)
    return [png]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DATA_PATH)
    ap.add_argument("--out-dir", default=OUT_DIR)
    ap.add_argument("--no-show", action="store_true")
    args, _unknown = ap.parse_known_args(argv)  # tolerate a foreign argv (inspectors)
    raw = load(args.data)
    xifres(raw)
    df = derive(raw)
    fig = build_chart(df)
    for f in save(fig, args.out_dir, SLUG):
        print("wrote", os.path.normpath(f))
    return fig


if __name__ == "__main__":
    fig = main()
