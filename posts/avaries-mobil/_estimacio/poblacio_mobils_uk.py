"""Parc estimat de mòbils del Regne Unit i fluxos anuals (2013–2019)

Decision record: p-category-breakdown-over-time--parc-estimat-de-m-bils-del-20261111-2  ·  Design document: disseny/poblacio_mobils_uk_design.md
Library: matplotlib  ·  Generated: 2026-11-11
Question: ¿Cómo evoluciona cada año la población estimada de móviles en uso del Reino Unido,
cuántos entran y cuántos salen (por causa), con su incertidumbre?

Llegeix balanc_escenaris_uk.csv (sortida d'escenaris_uk.py) i escriu
posts/avaries-mobil/poblacio_mobils_uk.png.
"""
from __future__ import annotations

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
import pandas as pd  # noqa: E402

# ---------------------------------------------------------------- CONFIG
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "balanc_escenaris_uk.csv")   # script-relative, so inspectors can run it from anywhere
OUT_DIR = os.path.normpath(os.path.join(_HERE, ".."))
SLUG = "poblacio_mobils_uk"
LANG = "ca"
COLUMNS = {"time": "any", "category": "escenari"}
PARSE = {"sep": ",", "decimal": "."}

# ---------------------------------------------------------------- PALETTE
# Tres famílies pastel: blau (parc i entrades), corall (avaria), sàlvia (sense avaria).
# Dins de cada família, el to més fosc és la categoria més important.
PARC, ENTRADES = "#A9C1DD", "#7FA7D1"
CAUSES = [  # (columna derivada, etiqueta, color), del zero cap avall
    ("pantalla", "Avaria: pantalla", "#C96A55"),
    ("bateria", "Avaria: bateria", "#DE9483"),
    ("programari", "Avaria: programari", "#EDBBAE"),
    ("resta", "Avaria: altres i desconeguda", "#F7E1DA"),
    ("sense_avaria", "Altres sortides (calaix,\nexportació, reciclatge…)", "#8CC2AF"),
]
TEXT, MUTED, ESCENARI, FONS, GRID = "#333333", "#6b6b6b", "#5B6573", "#FBFAF7", "#e4e2dc"
AMPLE = 0.62


def load(path: str) -> pd.DataFrame:
    dtype = {c: str for c in PARSE.get("code_columns", [])}
    df = pd.read_csv(path, sep=PARSE.get("sep", ","), decimal=PARSE.get("decimal", "."),
                     dtype=dtype, encoding=PARSE.get("encoding", "utf-8"))
    for col, fmt in PARSE.get("dates", {}).items():
        df[col] = pd.to_datetime(df[col], format=fmt, errors="coerce")
    for col in PARSE.get("numeric", []):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if PARSE.get("sentinels"):
        df = df.replace(PARSE["sentinels"], pd.NA)
    needed = [c for c in COLUMNS.values() if c]
    missing = [c for c in needed if c not in df.columns]
    assert not missing, f"missing columns: {missing}"
    assert len(df) > 0, "empty dataset"
    print(f"loaded {len(df)} rows from {path}")
    return df


def derive(df: pd.DataFrame) -> pd.DataFrame:
    """Derived data exactly as in the design document, section 2.

    Una fila per any, en milions: el central; la banda del parc (baix, alt); i les baixes per
    avaria dels escenaris optimista i pessimista."""
    m = df.set_index(["escenari", "any"]).sort_index() / 1e6
    c = m.loc["central"].copy()
    c["pantalla"] = c["avaria_Pantalla"]
    c["bateria"] = c["avaria_Bateria i alimentació"]
    c["programari"] = c["avaria_Programari i configuració"]
    c["resta"] = c[["avaria_Altres", "avaria_Botons i connectors", "avaria_Port de càrrega",
                    "avaria_Danys interns i aigua", "avaria_Desconegut"]].sum(axis=1)
    c["sense_avaria"] = c.sortides_sense_avaria
    c["durada_implicita"] = c.parc / c.vendes   # anys; no és un recompte, no es divideix per 1e6
    c["parc_baix"], c["parc_alt"] = m.loc["baix"].parc, m.loc["alt"].parc
    c["avaria_optimista"] = m.loc["optimista"].sortides_avaria
    c["avaria_pessimista"] = m.loc["pessimista"].sortides_avaria
    # Les causes sumen les sortides (el CSV porta 6 xifres significatives)
    causes = c[[k for k, _, _ in CAUSES]].sum(axis=1)
    assert ((causes - c.sortides).abs() < 1e-3).all(), "les causes no sumen les sortides"
    return c


def ca(x: float, dec: int = 0) -> str:
    return f"{x:.{dec}f}".replace(".", ",")


def takeaway(df: pd.DataFrame) -> str:
    """Title computed from the data (never a literal number)."""
    baixa = (1 - df.vendes.iloc[-1] / df.vendes.iloc[0]) * 100
    return (f"S'estima que el {df.index[-1]} es van vendre un {ca(baixa)} % menys mòbils nous que el "
            f"{df.index[0]}, mentre el parc en ús passava de {ca(df.parc.iloc[0])} a {ca(df.parc.iloc[-1])} milions")


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10)


def row_axis(ax, labels):
    """Categorical rows: set ticks with the labels so the axis is recognised as categorical
    (and needs no axis title); use this for hlines/scatter-based row charts."""
    ax.set_yticks(range(len(labels)), labels=list(labels))
    ax.set_ylabel("")


def separa(posicions: list[float], minim: float) -> list[float]:
    """Desplaça les etiquetes (ordenades de dalt a baix) perquè no se solapin."""
    out = []
    for y in posicions:
        out.append(y if not out or out[-1] - y >= minim else out[-1] - minim)
    return out


def bigoti(ax, x, lo, hi, lw=1.3):
    ax.plot([x, x], [lo, hi], color=ESCENARI, lw=lw, solid_capstyle="butt")
    for y in (lo, hi):
        ax.plot([x - 0.06, x + 0.06], [y, y], color=ESCENARI, lw=lw + 0.5)


def franja_parc(ax, df):
    x = range(len(df))
    ax.bar(x, df.parc, AMPLE, color=PARC, edgecolor="white", linewidth=0.8)
    for i, a in enumerate(df.index):
        bigoti(ax, i + 0.17, df.loc[a, "parc_baix"], df.loc[a, "parc_alt"])
        ax.text(i - AMPLE / 2 + 0.03, df.loc[a, "parc"] - 2.5, ca(df.loc[a, "parc"], 1), ha="left", va="top",
                fontsize=10, color=TEXT, fontweight="bold")
    xl = len(df) - 1 + AMPLE / 2 + 0.25
    ax.text(xl, df.parc.iloc[-1] / 2, "Mòbils en ús\n(a començament\nde l'any)", fontsize=9.5, color=TEXT,
            va="center")
    ax.text(xl, df.parc_alt.iloc[-1], "┃ si es compten SIM", fontsize=8.5, color=ESCENARI, va="center")
    ax.text(xl, df.parc_baix.iloc[-1], "┃ si es compten persones", fontsize=8.5, color=ESCENARI, va="center")
    ax.set_title("Parc: quants mòbils hi ha en ús", loc="left", fontsize=12, color=TEXT,
                 fontweight="bold", pad=8)
    ax.set_ylabel("milions de mòbils", fontsize=10, color=TEXT)


def franja_fluxos(ax, df):
    anys = list(df.index)
    x = range(len(anys))
    ax.bar(x, df.vendes, AMPLE, color=ENTRADES, edgecolor="white", linewidth=0.8)
    for i, v in enumerate(df.vendes):
        ax.text(i, v + 0.8, ca(v, 1), ha="center", va="bottom", fontsize=10, color=TEXT)
    # Saldo de l'any: el que fa créixer el parc de l'any següent
    for i, a in enumerate(anys):
        saldo = df.loc[a, "vendes"] - df.loc[a, "sortides"]
        ax.text(i, -43.5, f"saldo {'+' if saldo >= 0 else '−'}{ca(abs(saldo), 1)}", ha="center",
                va="center", fontsize=9.5, color=ESCENARI, fontweight="bold")
    base = [0.0] * len(anys)
    etiq = []
    for col, nom, color in CAUSES:
        ax.bar(x, -df[col], AMPLE, bottom=base, color=color, edgecolor="white", linewidth=0.8)
        etiq.append((base[-1] - df[col].iloc[-1] / 2, nom))
        base = [b - v for b, v in zip(base, df[col])]
    for i, v in enumerate(df.sortides):
        ax.text(i, -v - 0.8, ca(v, 1), ha="center", va="top", fontsize=10, color=TEXT)
    # Incertesa de la frontera avaria / sense avaria: escenari optimista–pessimista
    for i, a in enumerate(anys):
        bigoti(ax, i + AMPLE / 2 + 0.09, -df.loc[a, "avaria_optimista"], -df.loc[a, "avaria_pessimista"], lw=1.6)
    xl = len(anys) - 1 + AMPLE / 2 + 0.3
    ys = separa([y for y, _ in etiq], 3.6)
    for (y0, nom), y in zip(etiq, ys):
        y -= 1.3 * nom.count("\n")  # una etiqueta de dues línies necessita més aire per dalt
        ax.annotate(nom, xy=(len(anys) - 1 + AMPLE / 2, y0), xytext=(xl, y), fontsize=9.5, color=TEXT,
                    va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6, shrinkA=0, shrinkB=0)
                    if abs(y - y0) > 0.3 else None)
    ax.text(xl, df.vendes.iloc[-1] / 2, "Entren: mòbils nous\nvenuts", fontsize=9.5, color=TEXT, va="center")
    a = anys[-1]
    ax.text(xl, -df.loc[a, "sortides"] - 2,
            f"┃ baixes per avaria segons l'escenari:\n  de {ca(df.loc[a, 'avaria_optimista'])} a "
            f"{ca(df.loc[a, 'avaria_pessimista'])} milions el {a}",
            fontsize=8.5, color=ESCENARI, va="top")
    ax.axhline(0, color=TEXT, lw=0.9)
    ax.set_title("Fluxos: quants entren i quants surten cada any", loc="left", fontsize=12, color=TEXT,
                 fontweight="bold", pad=8)
    ax.set_ylabel("milions de mòbils per any\n← surten   ·   entren →", fontsize=10, color=TEXT)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: ca(abs(v))))


def build_chart(df: pd.DataFrame):
    """Encodings as in the design document, section 3. Returns the Figure."""
    fig, (p, f) = plt.subplots(2, 1, figsize=(12, 11), sharex=True, facecolor=FONS,
                               gridspec_kw={"height_ratios": [1, 1]})
    fig.subplots_adjust(left=0.1, right=0.78, top=0.845, bottom=0.11, hspace=0.18)
    franja_parc(p, df)
    franja_fluxos(f, df)
    # La mateixa escala (milions per centímetre) a les dues franges: s'hi veu que el parc
    # equival a uns dos o tres anys de vendes.
    alcada = 85
    p.set_ylim(0, alcada)
    f.set_ylim(-(alcada - 40), 40)
    for ax in (p, f):
        ax.set_xticks(range(len(df)), labels=[str(a) for a in df.index])
        ax.set_xlim(-0.6, len(df) - 0.4)
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_facecolor(FONS)
        style(ax)
        ax.spines["left"].set_color(MUTED)
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="x", length=0, labelbottom=True)

    fig.text(0.1, 0.955, takeaway(df), fontsize=14.5, fontweight="bold", color=TEXT, wrap=True)
    fig.text(0.1, 0.902,
             "Regne Unit, estimació, escenari central. Les dues franges tenen la mateixa escala.\n"
             f"El saldo de cada any (entrades − sortides) s'afegeix al parc de l'any següent: "
             f"{ca(df.parc.iloc[0], 1)} + {ca(df.vendes.iloc[0], 1)} − {ca(df.sortides.iloc[0], 1)} = "
             f"{ca(df.parc.iloc[1], 1)} milions el {df.index[1]}.",
             fontsize=10.5, color=MUTED, va="center", linespacing=1.5)
    nota = "\n".join([
        "Fiable: l'ordre de magnitud (±20 %) i la tendència, que es repeteixen en tots els escenaris. "
        "Les baixes per avaria varien un factor 5 entre escenaris.",
        "Fonts: ONS, Ofcom, Kantar, Deloitte, Eurobaròmetre 503 i MobiFix (Regne Unit, n = 554). "
        "Càlcul i dades: posts/avaries-mobil/_estimacio/.",
    ])
    fig.text(0.1, 0.03, nota, fontsize=8.2, color=MUTED, va="bottom", linespacing=1.5)
    return fig


def save(fig, out_dir: str, slug: str) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, f"{slug}.png")
    fig.savefig(png, dpi=200, facecolor=fig.get_facecolor())
    return [png]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DATA_PATH)
    ap.add_argument("--out-dir", default=OUT_DIR)
    ap.add_argument("--no-show", action="store_true")
    args, _unknown = ap.parse_known_args(argv)  # tolerate a foreign argv (inspectors)
    df = derive(load(args.data))
    fig = build_chart(df)
    for f in save(fig, args.out_dir, SLUG):
        print("wrote", f)
    return fig


if __name__ == "__main__":
    fig = main()
