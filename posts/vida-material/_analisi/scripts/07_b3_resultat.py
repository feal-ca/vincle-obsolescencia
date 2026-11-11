"""La bateria acaba a final de vida més sovint que la pantalla (barres al 100 %, final de vida en corall)

Decision record: p-compare-two-keys--com-acaben-les-reparacions-de-20261111-3  ·  Design document: posts/vida-material/_analisi/disseny/b3_resultat/b3_resultat_design.md
Library: Altair / Vega-Lite  ·  Generated: 2026-11-11
Question: Per què les reparacions de bateria acaben sense arreglar més que les de pantalla?

Com acaben les reparacions de bateria i de pantalla a MobiFix. Els motius dels finals de vida
no hi surten (gairebé mai no consten) i es comenten al text de l'entrada.

Escriu posts/vida-material/b3_resultat.png (i .svg); l'HTML i l'especificació Vega-Lite van a
disseny/b3_resultat/. El quadern 05 importa aquest mòdul i en fa servir load(), derive() i
build_chart(), de manera que la figura del quadern i la del post són la mateixa.

Ús, des de l'arrel del repositori:
    posts/vida-material/_analisi/.venv/bin/python posts/vida-material/_analisi/scripts/07_b3_resultat.py
"""
from __future__ import annotations

import argparse
import os
import sys

import altair as alt
import pandas as pd

# ---------------------------------------------------------------- CONFIG
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "..", "dades", "processades", "mobils_classificats.csv")  # relatiu a l'script
OUT_DIR = os.path.join(_HERE, "..", "..")                                  # carpeta de l'entrada: PNG i SVG
SPEC_DIR = os.path.join(_HERE, "..", "disseny", "b3_resultat")            # HTML i Vega-Lite, fora del web
SLUG = "b3_resultat"
LANG = "ca"
COLUMNS = {"grup": "grup_avaria", "font": "font_avaria", "estat": "repair_status", "any": "any_event"}
PARSE = {"sep": ",", "decimal": ".", "encoding": "utf-8"}

GRUPS = {"Bateria i alimentació": "Bateria", "Pantalla": "Pantalla"}
ORDRE = ["Bateria", "Pantalla"]
ESTATS = {"End of life": "Final de vida", "Repairable": "Pendent", "Fixed": "Reparat"}
ORDRE_ESTAT = list(ESTATS.values())  # el final de vida primer, des de la base comuna
AMPLE = 460  # amplada de les barres; les etiquetes de la dreta queden fora

# ---------------------------------------------------------------- PALETTE
# Pastels de la mateixa lluminositat (J' = 78 a CAM02-UCS): corall (dolent), lavanda (a mitges),
# aigua (bo). Com que la lluminositat és igual, la distinció per a daltònics depèn del to: s'ha triat
# amb colorspacious (Machado et al. al 100 %) la combinació que maximitza la distància mínima, que
# queda a ΔE 15 en deuteranopia (30 en visió normal). En grisos no es distingeixen: la segona pista
# és el nom de cada segment a sobre, en una versió fosca del mateix to, i els separadors blancs.
ESTAT_COLOR = {"Final de vida": "#f99e7e", "Pendent": "#b4b4f8", "Reparat": "#69cec4"}
ESTAT_TEXT = {"Final de vida": "#0b0b0b", "Pendent": "#0b0b0b", "Reparat": "#0b0b0b"}   # contrast ≥ 9:1
ESTAT_ETIQUETA = {"Final de vida": "#b5502f", "Pendent": "#5a5ab0", "Reparat": "#1f7a70"}  # text sobre blanc ≥ 4,5:1
INK, INK2 = "#0b0b0b", "#52514e"


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=PARSE["sep"], decimal=PARSE["decimal"], encoding=PARSE["encoding"],
                     low_memory=False)
    missing = [c for c in COLUMNS.values() if c not in df.columns]
    assert not missing, f"missing columns: {missing}"
    assert len(df) > 0, "empty dataset"
    print(f"loaded {len(df)} rows from {path}")
    return df


def derive(df: pd.DataFrame) -> pd.DataFrame:
    """Resultat per component a MobiFix: recompte, total, % i posició d'inici de cada segment."""
    d = df[(df[COLUMNS["font"]] == "MobiFix") & df[COLUMNS["grup"]].isin(GRUPS) & df[COLUMNS["estat"]].isin(ESTATS)]
    d = d.assign(component=d[COLUMNS["grup"]].map(GRUPS), resultat=d[COLUMNS["estat"]].map(ESTATS))
    a = d.groupby(["component", "resultat"]).size().unstack(fill_value=0).reindex(index=ORDRE, columns=ORDRE_ESTAT)
    a = a.stack().rename("n").reset_index()
    a["total"] = a.groupby("component")["n"].transform("sum")
    a["pct"] = a["n"] / a["total"] * 100
    a["inici"] = a.groupby("component")["pct"].cumsum() - a["pct"]
    a["fila"] = a["component"] + " (n = " + a["total"].astype(str) + ")"
    a["periode"] = f"{int(d[COLUMNS['any']].min())}–{int(d[COLUMNS['any']].max())}"
    return a


def takeaway(a: pd.DataFrame) -> list[str]:
    """Títol calculat a partir de les dades."""
    t = a.set_index(["component", "resultat"])["pct"]
    ratio = t[("Bateria", "Final de vida")] / t[("Pantalla", "Final de vida")]
    quant = "més del doble de vegades que" if ratio >= 2 else "més sovint que"
    return [f"La bateria acaba a final de vida {quant} la pantalla,",
            f"i només el {t[('Bateria', 'Reparat')]:.0f} % es repara el mateix dia"]


def build_chart(a: pd.DataFrame) -> alt.LayerChart:
    """Barres al 100 %, el final de vida primer des de la base comuna, etiquetes directes."""
    files = a.drop_duplicates("component")["fila"].tolist()
    x = alt.X("inici:Q", scale=alt.Scale(domain=[0, 100]), axis=None)
    y = alt.Y("fila:N", sort=files, title=None,
              axis=alt.Axis(labelColor=INK, labelFontSize=12, labelFontWeight="bold",
                            ticks=False, domain=False, labelPadding=8))
    barres = alt.Chart(a).mark_bar(height=30, stroke="white", strokeWidth=1.5).encode(
        x=x, x2="fi:Q", y=y,
        color=alt.Color("resultat:N", scale=alt.Scale(domain=ORDRE_ESTAT, range=[ESTAT_COLOR[e] for e in ORDRE_ESTAT]),
                        legend=None)).transform_calculate(fi="datum.inici + datum.pct")
    capes = [barres]
    for e in ORDRE_ESTAT:
        sub = a[a["resultat"] == e].assign(mig=lambda t: t["inici"] + t["pct"] / 2,
                                           t=lambda t: t["pct"].map(lambda v: f"{v:.0f} %"))
        capes.append(alt.Chart(sub).mark_text(fontSize=11, color=ESTAT_TEXT[e], fontWeight="bold").encode(
            x="mig:Q", y=y, text="t:N"))
    # Recompte del final de vida a la dreta de cada barra
    fv = a[a["resultat"] == "Final de vida"].assign(
        x=102, t=lambda t: "final de vida: " + t["n"].astype(str) + " de " + t["total"].astype(str))
    capes.append(alt.Chart(fv).mark_text(align="left", fontSize=11, color=ESTAT_ETIQUETA["Final de vida"]).encode(
        x="x:Q", y=y, text="t:N"))
    # Nom dels segments sobre la primera barra, del mateix color que el segment (en lloc de llegenda)
    bat = a[a["component"] == "Bateria"].reset_index(drop=True)
    for i, r in bat.iterrows():
        xs, al = (0, "left") if i == 0 else (r["inici"] + r["pct"] / 2, "center")
        color = ESTAT_ETIQUETA[r["resultat"]]
        capes.append(alt.Chart(pd.DataFrame({"x": [xs], "fila": [files[0]], "t": [r["resultat"]]})).mark_text(
            align=al, baseline="bottom", dy=-18, fontSize=11, fontWeight="bold", color=color).encode(
            x="x:Q", y=alt.Y("fila:N", sort=files), text="t:N"))
    grafic = alt.layer(*capes).properties(width=AMPLE, height=110)

    peu = alt.Chart(pd.DataFrame({"t": [
        f"Font: elaboració pròpia a partir d'Open Repair Data (MobiFix, {a['periode'].iloc[0]}), CC BY-SA 4.0.\n"
        "«Pendent»: es podia arreglar però no es va acabar aquell dia, per exemple perquè calia una peça."]})).mark_text(
        align="left", baseline="top", fontSize=10, color=INK2, lineBreak="\n").encode(
        x=alt.value(0), y=alt.value(0), text="t:N").properties(width=AMPLE, height=24)
    return alt.vconcat(grafic, peu, spacing=14).properties(title=alt.TitleParams(
        takeaway(a), subtitle=[f"Com acaben les reparacions de mòbils a MobiFix ({a['periode'].iloc[0]})"],
        anchor="start", fontSize=15, color=INK, subtitleColor=INK2, subtitleFontSize=11, offset=16)
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
    a = derive(load(args.data))
    print(a[["component", "resultat", "n", "total", "pct"]].round(1).to_string(index=False))
    chart = build_chart(a)
    for f in save(chart, args.out_dir, SLUG):
        print("wrote", f)
    return chart


if __name__ == "__main__":
    chart = main()
