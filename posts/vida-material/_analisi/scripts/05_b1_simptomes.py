"""Quan el mòbil no carrega, sovint no és la bateria (barres 100 % de 3 parts, accent al port)

Decision record: p-compare-two-keys--avaria-real-darrere-dels-s-20261111-2  ·  Design document: posts/vida-material/_analisi/disseny/b1_simptomes/b1_simptomes_design.md
Library: matplotlib  ·  Generated: 2026-11-11
Question: Quan un mòbil no carrega o no s'encén, quantes vegades és realment la bateria i quantes
el port o el carregador?

Escriu posts/vida-material/b1_simptomes.png (i .svg). El quadern 03 importa aquest mòdul i en fa
servir load(), derive() i build_chart(), de manera que la figura del quadern i la del post són la
mateixa.

Ús, des de l'arrel del repositori:
    posts/vida-material/_analisi/.venv/bin/python posts/vida-material/_analisi/scripts/05_b1_simptomes.py
"""
from __future__ import annotations

import argparse
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

# ---------------------------------------------------------------- CONFIG
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, ".."))
import comu  # noqa: E402

DATA_PATH = os.path.join(_HERE, "..", "dades", "raw", "ora_mobifix.csv")   # relatiu a l'script
OUT_DIR = os.path.join(_HERE, "..", "..")                                   # carpeta de l'entrada
SLUG = "b1_simptomes"
LANG = "ca"
COLUMNS = {"text": "problem", "avaria": "fault_type"}
PARSE = {"sep": ",", "decimal": ".", "encoding": "utf-8"}

# Símptomes que es mostren (els altres no tenen casos sense la paraula «bateria»)
SIMPTOMES = {"no_carrega": "No carrega", "no_sencen": "No s'encén"}
# Tres grups d'avaria: el que defensa el text (port o carregador), la bateria i la resta
GRUP = {"USB/charging port": "Port o carregador", "Charger": "Port o carregador",
        "Power/battery": "Bateria"}
ORDRE = ["Port o carregador", "Bateria", "Altres o desconegut"]

# ---------------------------------------------------------------- PALETTE
# Neutre + un accent (el port), segur per a daltònics i llegible en grisos; text fosc sobre grisos.
ACCENT = "#0072b2"
PALETTE = {"Port o carregador": ACCENT, "Bateria": "#8f8e89", "Altres o desconegut": "#d9d8d4"}
TEXT_ON = {"Port o carregador": "white", "Bateria": "#0b0b0b", "Altres o desconegut": "#0b0b0b"}
INK, INK2 = "#0b0b0b", "#52514e"


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=PARSE["sep"], decimal=PARSE["decimal"], encoding=PARSE["encoding"])
    missing = [c for c in COLUMNS.values() if c not in df.columns]
    assert not missing, f"missing columns: {missing}"
    assert len(df) > 0, "empty dataset"
    print(f"loaded {len(df)} rows from {path}")
    return df


def derive(df: pd.DataFrame) -> pd.DataFrame:
    """Taula final: una fila per (símptoma, grup) amb el recompte, el total i la proporció.

    Només textos de MobiFix que no esmenten la bateria (per no comptar el diagnòstic del
    voluntari com a símptoma)."""
    df = df[df["problem"].notna()].copy()
    s = comu.simptomes(df["problem"])
    df = df[~s["mencio_bateria"]]
    s = s[~s["mencio_bateria"]]
    df["grup"] = df["fault_type"].map(GRUP).fillna("Altres o desconegut")
    files = []
    for clau, nom in SIMPTOMES.items():
        sub = df[s[clau]]
        compte = sub["grup"].value_counts().reindex(ORDRE, fill_value=0)
        for grup, n in compte.items():
            files.append({"simptoma": nom, "grup": grup, "n": int(n), "total": len(sub)})
    out = pd.DataFrame(files)
    out["pct"] = out["n"] / out["total"] * 100
    return out


def takeaway(df: pd.DataFrame) -> str:
    """Títol calculat a partir de les dades."""
    fila = df[(df["simptoma"] == "No carrega") & (df["grup"] == "Port o carregador")].iloc[0]
    de_cada_10 = round(fila["n"] / fila["total"] * 10)
    return (f"Quan el mòbil no carrega, gairebé {de_cada_10} de cada 10 vegades\n"
            f"era el port o el carregador, no la bateria")


def style(ax):
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0, labelsize=10)


def build_chart(df: pd.DataFrame):
    """Barres horitzontals al 100 %, el port primer des de la base comuna, etiquetes directes."""
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    simptomes = list(SIMPTOMES.values())
    etiquetes = [f"{s}\n(n = {df.loc[df['simptoma'] == s, 'total'].iloc[0]})" for s in simptomes]
    esquerra = [0.0] * len(simptomes)
    for grup in ORDRE:
        sub = df[df["grup"] == grup].set_index("simptoma").loc[simptomes]
        ax.barh(etiquetes, sub["pct"], left=esquerra, color=PALETTE[grup], height=0.62,
                edgecolor="white", linewidth=1.5)
        for y, (x0, (_, r)) in enumerate(zip(esquerra, sub.iterrows())):
            text = f"{grup}\n{r['n']} de {r['total']} · {r['pct']:.0f} %".replace(".", ",")
            if r["pct"] >= 22:
                ax.text(x0 + r["pct"] / 2, y, text, ha="center", va="center",
                        color=TEXT_ON[grup], fontsize=8.5, linespacing=1.25)
            elif r["n"] > 0:  # segment massa estret: l'etiqueta va a sota de la barra
                ax.text(x0, y + 0.44, f"{grup}: {r['n']} de {r['total']}",
                        ha="left", va="top", color=ACCENT if grup == ORDRE[0] else INK2, fontsize=8)
        esquerra = [a + b for a, b in zip(esquerra, sub["pct"])]
    ax.set_ylim(1.62, -0.42)  # files de dalt a baix, amb lloc per a les etiquetes de sota
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    style(ax)
    fig.suptitle(takeaway(df), x=0.01, y=0.99, ha="left", va="top", fontsize=11, color=INK, linespacing=1.3)
    fig.text(0.01, 0.77, "Reparacions de MobiFix (2012–2020) sense la paraula «bateria» · avaria trobada pels voluntaris",
             fontsize=8.5, color=INK2)
    fig.text(0.01, -0.04, "Font: elaboració pròpia a partir d'Open Repair Data (MobiFix), CC BY-SA 4.0.",
             fontsize=7.5, color=INK2)
    fig.subplots_adjust(left=0.15, right=0.86, top=0.70, bottom=0.06)
    return fig


def save(fig, out_dir: str, slug: str) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, f"{slug}.png")
    fig.savefig(png, dpi=200, bbox_inches="tight")
    svg = os.path.join(out_dir, f"{slug}.svg")
    fig.savefig(svg, bbox_inches="tight")
    return [png, svg]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DATA_PATH)
    ap.add_argument("--out-dir", default=OUT_DIR)
    ap.add_argument("--no-show", action="store_true")
    args, _unknown = ap.parse_known_args(argv)  # tolera un argv aliè (inspectors)
    df = derive(load(args.data))
    print(df.to_string(index=False))
    fig = build_chart(df)
    for f in save(fig, args.out_dir, SLUG):
        print("wrote", f)
    return fig


if __name__ == "__main__":
    fig = main()
