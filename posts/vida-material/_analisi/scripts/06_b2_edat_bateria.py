"""La bateria es porta a reparar més tard que la pantalla (distribució acumulada, franja de referència de 800 cicles)

Decision record: p-distribution-compare-groups--edat-a-la-reparaci-de-la-20261111-2  ·  Design document: posts/vida-material/_analisi/disseny/b2_edat_bateria/b2_edat_bateria_design.md
Library: Altair / Vega-Lite  ·  Generated: 2026-11-11
Question: A quina edat arriben a reparar les bateries, comparat amb les pantalles i amb el punt de
800 cicles que avui fixa el reglament?

Escriu posts/vida-material/b2_edat_bateria.png (i .svg); l'HTML i l'especificació Vega-Lite van a
disseny/b2_edat_bateria/. El quadern 04 importa aquest mòdul i en fa servir load(), derive() i
build_chart(), de manera que la figura del quadern i la del post són la mateixa.

Ús, des de l'arrel del repositori:
    posts/vida-material/_analisi/.venv/bin/python posts/vida-material/_analisi/scripts/06_b2_edat_bateria.py
"""
from __future__ import annotations

import argparse
import os
import sys

import altair as alt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- CONFIG
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "..", "dades", "processades", "mobils_classificats.csv")  # relatiu a l'script
OUT_DIR = os.path.join(_HERE, "..", "..")                                  # carpeta de l'entrada: PNG i SVG
SPEC_DIR = os.path.join(_HERE, "..", "disseny", "b2_edat_bateria")        # HTML i Vega-Lite, fora del web
SLUG = "b2_edat_bateria"
LANG = "ca"
COLUMNS = {"edat": "edat_neta", "grup": "grup_avaria", "font": "font_avaria", "cluster": "group_identifier"}
PARSE = {"sep": ",", "decimal": ".", "encoding": "utf-8"}

GRUPS = {"Bateria i alimentació": "Bateria", "Pantalla": "Pantalla"}
CLASSIFICAT = "Bateria, classificat"
ORDRE = ["Bateria", "Pantalla", CLASSIFICAT]
# 800 cicles convertits a anys amb 1 i 0,5 cicles complets al dia (supòsits, no mesures)
CICLES = 800
FRANJA = (CICLES / 365, CICLES / (0.5 * 365))
EDAT_MAX = 10       # eix x; les reparacions classificades de més edat queden fora i es diu al peu
AMPLE, ALT = 600, 320

# ---------------------------------------------------------------- PALETTE
# Bateria vermelló i pantalla blava (parella Okabe-Ito, segura per a daltònics); el classificat, en gris.
ACCENT = "#d55e00"
PALETTE = {"Bateria": ACCENT, "Pantalla": "#0072b2", CLASSIFICAT: "#b5b4af"}
TRAÇ = {"Bateria": 2.5, "Pantalla": 2.5, CLASSIFICAT: 1.5}
FRANJA_COLOR = "#ebeae6"
INK, INK2 = "#0b0b0b", "#52514e"


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=PARSE["sep"], decimal=PARSE["decimal"], encoding=PARSE["encoding"],
                     low_memory=False)
    missing = [c for c in COLUMNS.values() if c not in df.columns]
    assert not missing, f"missing columns: {missing}"
    assert len(df) > 0, "empty dataset"
    print(f"loaded {len(df)} rows from {path}")
    return df


def mediana_ic(df: pd.DataFrame, n_boot: int = 1000, seed: int = 42) -> pd.Series:
    """Mediana i IC 95 % per bootstrap agrupat per grup de reparació."""
    rng = np.random.default_rng(seed)
    valors = list(df.groupby(COLUMNS["cluster"])[COLUMNS["edat"]].apply(np.asarray).values)
    boots = [np.median(np.concatenate([valors[i] for i in rng.integers(0, len(valors), len(valors))]))
             for _ in range(n_boot)]
    return pd.Series({"n": len(df), "mediana": df[COLUMNS["edat"]].median(),
                      "ic_inf": np.percentile(boots, 2.5), "ic_sup": np.percentile(boots, 97.5)})


def acumulada(edats: pd.Series, grup: str) -> pd.DataFrame:
    """Esglaons de la distribució acumulada: un punt per edat diferent, més l'inici i el final."""
    pct = edats.value_counts().sort_index().cumsum() / len(edats) * 100
    e = pd.DataFrame({"edat": pct.index, "pct": pct.values})
    extrem = pd.DataFrame({"edat": [0.0, EDAT_MAX], "pct": [0.0, float(pct[pct.index <= EDAT_MAX].iloc[-1])]})
    e = pd.concat([extrem.iloc[:1], e[e["edat"] <= EDAT_MAX], extrem.iloc[1:]]).drop_duplicates("edat", keep="last")
    return e.assign(grup=grup)


def derive(df: pd.DataFrame) -> dict:
    """Corbes acumulades, resums per grup i quantes bateries queden a cada costat de la franja."""
    amb_edat = df[df[COLUMNS["edat"]].notna()]
    mf = amb_edat[(amb_edat[COLUMNS["font"]] == "MobiFix") & amb_edat[COLUMNS["grup"]].isin(GRUPS)].copy()
    mf["grup"] = mf[COLUMNS["grup"]].map(GRUPS)
    cl = amb_edat[amb_edat[COLUMNS["grup"]] == "Bateria i alimentació"]
    conjunts = {"Bateria": mf[mf["grup"] == "Bateria"], "Pantalla": mf[mf["grup"] == "Pantalla"], CLASSIFICAT: cl}

    corbes = pd.concat([acumulada(conjunts[g][COLUMNS["edat"]], g) for g in ORDRE], ignore_index=True)
    resum = pd.DataFrame({g: mediana_ic(conjunts[g]) for g in ORDRE}).T
    bat = conjunts["Bateria"][COLUMNS["edat"]]
    franja = {"n": len(bat), "fins_inf": (bat <= FRANJA[0]).mean() * 100, "fins_sup": (bat <= FRANJA[1]).mean() * 100}
    fora = int((cl[COLUMNS["edat"]] > EDAT_MAX).sum())
    return {"corbes": corbes, "resum": resum, "franja": franja, "fora": fora}


def num(x: float, dec: int = 1) -> str:
    """Xifra en format català, sense decimals sobrers."""
    s = f"{x:.{dec}f}".rstrip("0").rstrip(".") if dec else f"{x:.0f}"
    return s.replace(".", ",")


def takeaway(d: dict) -> str:
    """Títol calculat a partir de les dades."""
    r = d["resum"]
    dif = r.loc["Bateria", "mediana"] - r.loc["Pantalla", "mediana"]
    return (f"La bateria es porta a reparar als {num(r.loc['Bateria', 'mediana'])} anys, "
            f"{num(dif)} anys més tard que la pantalla")


def text(df: pd.DataFrame, x, y, **kw) -> alt.Chart:
    return alt.Chart(df).mark_text(baseline="middle", fontSize=11, lineBreak="\n", **kw).encode(
        x=x, y=y, text="t:N")


def build_chart(d: dict) -> alt.VConcatChart:
    """Corbes acumulades amb la franja de referència, la línia del 50 %, medianes amb IC i cruces anotats."""
    r, f = d["resum"], d["franja"]
    x = alt.X("edat:Q", scale=alt.Scale(domain=[0, EDAT_MAX], nice=False),
              axis=alt.Axis(title="Edat del mòbil el dia de la reparació (anys)", values=list(range(EDAT_MAX + 1)),
                            grid=False, labelColor=INK2, titleColor=INK2))
    y = alt.Y("pct:Q", scale=alt.Scale(domain=[0, 100]),
              axis=alt.Axis(title="% de reparacions amb aquesta edat o menys", values=[0, 25, 50, 75, 100],
                            grid=False, labelColor=INK2, titleColor=INK2))
    capes = []

    capes.append(alt.Chart(pd.DataFrame({"edat": [FRANJA[0]], "e2": [FRANJA[1]]})).mark_rect(
        color=FRANJA_COLOR).encode(x=x, x2="e2:Q"))
    capes.append(text(pd.DataFrame({"edat": [sum(FRANJA) / 2], "pct": [97], "t": ["800 cicles"]}), x, y,
                      color=INK2, fontWeight="bold"))
    capes.append(alt.Chart(pd.DataFrame({"pct": [50]})).mark_rule(
        color="#c9c8c4", strokeDash=[3, 3]).encode(y=y))

    # Corbes: la classificada primer (a sota), la bateria l'última (a sobre)
    for g in [CLASSIFICAT, "Pantalla", "Bateria"]:
        c = d["corbes"][d["corbes"]["grup"] == g]
        capes.append(alt.Chart(c).mark_line(interpolate="step-after", color=PALETTE[g], strokeWidth=TRAÇ[g],
                                            strokeDash=[4, 3] if g == CLASSIFICAT else [1, 0]).encode(x=x, y=y))

    # Medianes: IC sobre la línia del 50 % i punt a la mediana
    for g, dx, alinea, dy in [("Bateria", 0.15, "left", -5), ("Pantalla", -0.6, "right", 8)]:
        color = PALETTE[g]
        capes.append(alt.Chart(pd.DataFrame({"edat": [r.loc[g, "ic_inf"]], "e2": [r.loc[g, "ic_sup"]], "pct": [50]}))
                     .mark_rule(color=color, strokeWidth=5, opacity=0.35).encode(x=x, x2="e2:Q", y=y))
        capes.append(alt.Chart(pd.DataFrame({"edat": [r.loc[g, "mediana"]], "pct": [50]})).mark_point(
            filled=True, size=60, color=color, opacity=1).encode(x=x, y=y))
        vora = r.loc[g, "ic_sup"] if g == "Bateria" else r.loc[g, "ic_inf"]
        salt = " " if g == "Bateria" else "\n"  # la pantalla no hi cap en una línia
        t = f"mediana {num(r.loc[g, 'mediana'])} anys{salt}(IC 95 %: {num(r.loc[g, 'ic_inf'])}–{num(r.loc[g, 'ic_sup'])})"
        capes.append(text(pd.DataFrame({"edat": [vora + dx], "pct": [50 + dy], "t": [t]}), x, y,
                          align=alinea, color=color))

    # Cruces de la bateria amb les vores de la franja
    cruces = pd.DataFrame({"edat": list(FRANJA), "pct": [f["fins_inf"], f["fins_sup"]]})
    capes.append(alt.Chart(cruces).mark_point(shape="circle", size=50, filled=False, strokeWidth=2,
                                              color=ACCENT).encode(x=x, y=y))
    capes.append(text(pd.DataFrame({"edat": [FRANJA[0] - 0.25], "pct": [f["fins_inf"] + 8],
                                    "t": [f"{round(f['fins_inf'])} % abans"]}), x, y, align="right",
                      color=ACCENT, fontWeight="bold"))
    capes.append(text(pd.DataFrame({"edat": [FRANJA[1] + 0.12], "pct": [f["fins_sup"] - 5],
                                    "t": [f"{round(100 - f['fins_sup'])} % després"]}), x, y, align="left",
                      color=ACCENT, fontWeight="bold"))

    # Etiquetes directes en lloc de llegenda
    n = r["n"].astype(int)
    etiquetes = [("Bateria", 5.15, 80, f"Bateria (n = {n['Bateria']})", ACCENT, "bold"),
                 ("Pantalla", 2.0, 88, f"Pantalla (n = {n['Pantalla']})", PALETTE["Pantalla"], "bold"),
                 (CLASSIFICAT, 6.1, 66, f"bateria, classificat sense validar (n = {n[CLASSIFICAT]})", "#8f8e89", "normal")]
    for _, ex, ey, t, color, pes in etiquetes:
        capes.append(text(pd.DataFrame({"edat": [ex], "pct": [ey], "t": [t]}), x, y,
                          align="right" if ex < 3 else "left", color=color, fontWeight=pes))

    lo, hi = (num(v) for v in FRANJA)
    peu = ("Font: elaboració pròpia a partir d'Open Repair Data (MobiFix), CC BY-SA 4.0.\nL'edat es declara, "
           f"gairebé sempre en anys sencers. {d['fora']} reparacions classificades de més de {EDAT_MAX} anys queden fora.")
    linia = alt.Chart(pd.DataFrame({"t": [peu]})).mark_text(
        align="left", baseline="top", fontSize=10, color=INK2, lineBreak="\n").encode(
        x=alt.value(0), y=alt.value(0), text="t:N").properties(width=AMPLE, height=24)
    grafic = alt.layer(*capes).properties(width=AMPLE, height=ALT)
    return alt.vconcat(grafic, linia, spacing=14).properties(title=alt.TitleParams(
        takeaway(d),
        subtitle=["Edat del mòbil el dia de la reparació, MobiFix 2017–2020",
                  f"Franja grisa: 800 cicles, el que el reglament exigeix des del 2025, convertits a {lo}–{hi} anys",
                  "(0,5 a 1 cicle al dia). Aquests mòbils són anteriors al reglament."],
        anchor="start", fontSize=15, color=INK, subtitleColor=INK2, subtitleFontSize=11, offset=12)
    ).configure(font="Helvetica, Arial, sans-serif", background="white").configure_view(strokeWidth=0)


def save(chart, out_dir: str, slug: str) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(SPEC_DIR, exist_ok=True)
    written = []
    for path in (os.path.join(SPEC_DIR, f"{slug}.html"), os.path.join(SPEC_DIR, f"{slug}.vl.json")):
        chart.save(path)
        written.append(path)
    try:
        png = os.path.join(out_dir, f"{slug}.png")
        chart.save(png, scale_factor=2)
        written.append(png)
        svg = os.path.join(out_dir, f"{slug}.svg")
        chart.save(svg)
        written.append(svg)
    except Exception as e:  # vl_convert missing
        print(f"PNG not rendered ({e}); open the HTML in a browser", file=sys.stderr)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DATA_PATH)
    ap.add_argument("--out-dir", default=OUT_DIR)
    ap.add_argument("--no-show", action="store_true")
    args, _unknown = ap.parse_known_args(argv)  # tolera un argv aliè (inspectors)
    d = derive(load(args.data))
    print(d["resum"].round(2).to_string())
    print({k: round(v, 1) for k, v in d["franja"].items()}, "fora:", d["fora"])
    chart = build_chart(d)
    for f in save(chart, args.out_dir, SLUG):
        print("wrote", f)
    return chart


if __name__ == "__main__":
    chart = main()
