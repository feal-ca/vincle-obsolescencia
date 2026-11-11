"""Diagrama de Sankey de les avaries de mòbil de MobiFix: any -> tipus d'avaria -> resultat.

Genera posts/avaries-mobil/sankey_avaries.png i imprimeix les xifres que
cita el text de l'entrada. Cal haver executat abans 01_descarrega_ora.py.

Ús, des de l'arrel del repositori:
    python3 posts/vida-material/_analisi/scripts/03_sankey_mobifix.py

Els amples de les cintes són reparacions *registrades* a Repair Cafés, no
mòbils espatllats en general. L'últim pas (resultat) agrupa tots els anys.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd

ARREL = Path(__file__).resolve().parents[4]
RAW = Path(__file__).resolve().parents[1] / "dades" / "raw"
SORTIDA = ARREL / "posts" / "avaries-mobil" / "sankey_avaries.png"

# Mateixos grups que l'apartat 3 de posts/vida-material/index.qmd. La càmera,
# l'altaveu i el micròfon (86 casos) van a "Altres", igual que "Other".
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
ORDRE_GRUPS = [
    "Pantalla",
    "Bateria i alimentació",
    "Port de càrrega",
    "Botons i connectors",
    "Danys interns i aigua",
    "Programari i configuració",
    "Altres",
    "Desconegut",
]
# Paleta categòrica validada (ordre fix); "Altres" i "Desconegut" en grisos.
COLORS = dict(
    zip(
        ORDRE_GRUPS,
        ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6", "#8f8e89", "#c9c8c2"],
    )
)
RESULTATS = {"Fixed": "Reparat", "Repairable": "Reparable", "End of life": "Final de vida"}
ORDRE_RES = ["Reparat", "Reparable", "Final de vida"]
COLOR_RES = {"Reparat": "#52514e", "Reparable": "#52514e", "Final de vida": "#e34948"}
INK, INK2 = "#0b0b0b", "#52514e"


def carrega():
    m = pd.read_csv(RAW / "ora_mobifix.csv")
    m["any"] = m["event_date"].str[:4].astype(int).clip(lower=2013)  # 2012 només té 1 cas
    m["grup"] = m["fault_type"].map(GRUPS)
    m["resultat"] = m["repair_status"].map(RESULTATS)
    assert m["grup"].notna().all()
    return m


def xifres(m, k):
    print(f"Reparacions de mòbil a MobiFix: {len(m):,}")
    print(f"  sense resultat conegut (fora del gràfic): {len(m) - len(k)}")
    print(f"  al gràfic: {len(k):,}")
    print(f"Proveïdor The Restart Project: {(m['data_provider'] == 'The Restart Project').mean():.1%}")
    print(f"Pantalla: {(k['grup'] == 'Pantalla').sum()} ({(k['grup'] == 'Pantalla').mean():.1%})")
    print(f"Desconegut: {(k['grup'] == 'Desconegut').sum()} ({(k['grup'] == 'Desconegut').mean():.1%})")
    print("Resultat:\n", k["resultat"].value_counts().to_string())
    print(k["resultat"].value_counts(normalize=True).round(3).to_string())
    t = pd.crosstab(k["grup"], k["resultat"])
    t["n"] = t.sum(axis=1)
    t["%final"] = (t["Final de vida"] / t["n"] * 100).round(1)
    print(t.loc[ORDRE_GRUPS].to_string())
    print("Registres per any:\n", m.groupby("any").size().to_string())
    print("Última data:", m["event_date"].max())


def cinta(ax, x0, x1, ya0, ya1, yb0, yb1, color, alpha):
    """Cinta amb entrada [ya0, ya1] a x0 i sortida [yb0, yb1] a x1 (eix y invertit)."""
    t = np.linspace(0, 1, 60)
    s = t * t * (3 - 2 * t)
    x = x0 + (x1 - x0) * t
    top = ya0 + (yb0 - ya0) * s
    bot = ya1 + (yb1 - ya1) * s
    ax.fill_between(x, top, bot, color=color, alpha=alpha, lw=0)


def dibuixa(k):
    anys = sorted(k["any"].unique())
    etiq_any = {a: ("2012–13" if a == 2013 else str(a)) for a in anys}
    capes = [anys, ORDRE_GRUPS, ORDRE_RES]
    cols = ["any", "grup", "resultat"]
    GAP = 22  # separació entre nodes, en unitats de reparacions

    # Posició (inici, final) de cada node, cada capa centrada verticalment.
    total = len(k)
    alt_max = total + GAP * (max(len(c) for c in capes) - 1)
    pos = []
    for cap, col in zip(capes, cols):
        n = k.groupby(col).size()
        alt = total + GAP * (len(cap) - 1)
        y = (alt_max - alt) / 2
        d = {}
        for nom in cap:
            d[nom] = (y, y + n.get(nom, 0))
            y += n.get(nom, 0) + GAP
        pos.append(d)

    fig, ax = plt.subplots(figsize=(11, 8.2), dpi=200)
    fig.patch.set_facecolor("white")
    X = [0.0, 5.5, 11.0]
    W = 0.28

    def flux(c, col_a, col_b, a_ordre, b_ordre):
        """Cintes entre capes c i c+1, apilades sense creuar-se dins de cada node."""
        t = k.groupby([col_a, col_b]).size()
        sortida = {a: pos[c][a][0] for a in a_ordre}
        entrada = {b: pos[c + 1][b][0] for b in b_ordre}
        # La sortida de cada node s'apila segons l'ordre de destí i l'entrada
        # segons l'ordre d'origen, i així no hi ha creus dins del node.
        for a in a_ordre:
            for b in b_ordre:
                v = t.get((a, b), 0)
                if not v:
                    continue
                yield a, b, sortida[a], entrada[b], v
                sortida[a] += v
                entrada[b] += v

    for a, g, ya, yb, v in flux(0, "any", "grup", anys, ORDRE_GRUPS):
        cinta(ax, X[0] + W, X[1], ya, ya + v, yb, yb + v, COLORS[g], 0.5)
    for g, r, ya, yb, v in flux(1, "grup", "resultat", ORDRE_GRUPS, ORDRE_RES):
        cinta(ax, X[1] + W, X[2], ya, ya + v, yb, yb + v, COLORS[g], 0.5)

    # Nodes i etiquetes.
    halo = [pe.withStroke(linewidth=3, foreground="white")]
    for c, (cap, x) in enumerate(zip(capes, X)):
        for nom in cap:
            y0, y1 = pos[c][nom]
            if y1 == y0:
                continue
            n = int(y1 - y0)
            if c == 0:
                color, txt = "#3a3935", f"{etiq_any[nom]}  ·  {n}"
                ax.add_patch(plt.Rectangle((x, y0), W, y1 - y0, color=color, lw=0))
                ax.text(x - 0.15, (y0 + y1) / 2, txt, ha="right", va="center", fontsize=10, color=INK)
            elif c == 1:
                ax.add_patch(plt.Rectangle((x, y0), W, y1 - y0, color=COLORS[nom], lw=0))
                ax.text(x + W + 0.12, (y0 + y1) / 2, f"{nom} · {n}", ha="left", va="center", fontsize=10,
                        color=INK, fontweight="bold", path_effects=halo)
            else:
                ax.add_patch(plt.Rectangle((x, y0), W, y1 - y0, color=COLOR_RES[nom], lw=0))
                pct = n / total * 100
                ax.text(x + W + 0.15, (y0 + y1) / 2, f"{nom}\n{n}  ({pct:.0f} %)".replace(".", ","),
                        ha="left", va="center", fontsize=10.5, color=INK, linespacing=1.3)

    ax.text(X[0] + W, -85, "Any de la reparació", ha="right", fontsize=10, color=INK2, fontweight="bold")
    ax.text(X[1] + W / 2, -85, "Tipus d'avaria", ha="center", fontsize=10, color=INK2, fontweight="bold")
    ax.text(X[2] + W / 2, -85, "Resultat (tots els anys)", ha="center", fontsize=10, color=INK2, fontweight="bold")

    ax.set_xlim(-2.2, 13.0)
    ax.set_ylim(alt_max + 20, -110)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
    SORTIDA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SORTIDA, facecolor="white")
    print("Escrit", SORTIDA)


def main():
    m = carrega()
    k = m[m["resultat"].notna()].copy()
    xifres(m, k)
    dibuixa(k)


if __name__ == "__main__":
    main()
