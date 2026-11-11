# Gràfiques de l'article de repair cafés

import altair as alt
import pandas as pd

BLAU = "#2a78d6"
BLAU_CLAR = "#a9c7ee"
TARONJA = "#eb6834"
VERD = "#1baf7a"
GRIS = "#b9b8b2"
TEXT = "#52514e"
AMPLADA = 640

LOCALE = {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["", " €"]}
MON = "https://cdn.jsdelivr.net/npm/vega-datasets@2.8.0/data/world-110m.json"


def titol(text):
    return alt.TitleParams(text, anchor="start", fontSize=15, offset=12)


def estil(grafica):
    # Fons blanc perquè es vegi bé també amb el mode fosc del blog
    return (grafica
            .configure_view(stroke=None)
            .configure_axis(labelColor=TEXT, titleColor=TEXT, gridColor="#e4e3df", domainColor="#d0cfca")
            .configure(font="Inter, system-ui, sans-serif", background="#ffffff", padding=12))


def creixement():
    dades = pd.DataFrame({
        "any": [2009, 2016, 2021, 2024, 2025],
        "n": [1, 1007, 2000, 3275, 3574],
        "etiqueta": ["1r Repair Café (Amsterdam)", "1.007 al web de RCI", "Més de 2.000",
                     "3.275 al mapa de RCI", "3.574 al mapa de RCI"],
    })
    base = alt.Chart(dades).encode(
        x=alt.X("any:Q", title=None, scale=alt.Scale(domain=[2008, 2026]), axis=alt.Axis(format="d", tickMinStep=2)),
        y=alt.Y("n:Q", title="Repair cafés al món", axis=alt.Axis(format=",.0f")),
    )
    linia = base.mark_line(strokeDash=[2, 3], color=BLAU)
    punts = base.mark_circle(size=140, color=BLAU, opacity=1)
    # L'etiqueta del 2009 va a la dreta del punt i la resta a l'esquerra
    etiquetes = base.mark_text(align="right", dx=-10, dy=-10, fontSize=11, color=TEXT).encode(text="etiqueta")
    etiquetes = etiquetes.transform_filter("datum.any > 2009")
    primera = base.mark_text(align="left", dx=8, dy=-30, fontSize=11, color=TEXT).encode(text="etiqueta")
    primera = primera.transform_filter("datum.any == 2009")

    grafica = linia + punts + etiquetes + primera
    return grafica.properties(width=AMPLADA, height=300, title=titol("Augment del nombre de repair cafés al món"))


def mapa(carpeta):
    paisos = pd.read_csv(carpeta / "repair_cafes_per_pais.csv")
    europa = paisos[paisos.continent == "Europe"].iso3
    cafes = pd.read_csv(carpeta / "repair_cafes_punts.csv")
    cafes = cafes[cafes.iso3.isin(europa)].copy()
    cafes["tipus"] = cafes.linux.map({True: "Ofereix Linux", False: "Només reparació"})
    cafes = cafes.sort_values("linux")  # els de Linux queden a sobre

    projeccio = dict(type="azimuthalEqualArea", rotate=[-10, -52, 0], scale=900, translate=[AMPLADA / 2, 260])
    fons = (alt.Chart(alt.topo_feature(MON, "countries"))
            .mark_geoshape(fill="#efeee9", stroke="white", strokeWidth=0.6)
            .project(**projeccio))

    clic = alt.selection_point(fields=["tipus"], bind="legend")
    punts = alt.Chart(cafes).mark_circle(size=16).encode(
        longitude="lon:Q",
        latitude="lat:Q",
        color=alt.Color("tipus:N",
                        scale=alt.Scale(domain=["Només reparació", "Ofereix Linux"], range=[BLAU, TARONJA]),
                        legend=alt.Legend(title="Clica per filtrar", orient="top-left", symbolOpacity=1)),
        opacity=alt.condition(clic, alt.value(0.35), alt.value(0.03)),
        tooltip=[alt.Tooltip("tipus:N", title="Tipus"),
                 alt.Tooltip("actualitzat:T", title="Fitxa actualitzada", format="%m/%Y")],
    ).add_params(clic).project(**projeccio)

    return (fons + punts).properties(width=AMPLADA, height=520, title=titol("Localització dels repair cafés a Europa"))


def exit_per_objecte(carpeta):
    dades = pd.read_csv(carpeta / "exit_per_objecte.csv")
    resultats = ["Reparat", "Mig reparat", "No reparat"]
    ordre = dades[dades.resultat == "Reparat"].sort_values("pct", ascending=False).objecte.tolist()
    clic = alt.selection_point(fields=["resultat"], bind="legend")
    opacitat = alt.condition(clic, alt.value(1), alt.value(0.2))

    base = alt.Chart(dades).encode(
        y=alt.Y("objecte:N", sort=ordre, title=None),
        yOffset=alt.YOffset("resultat:N", sort=resultats),
    )
    barres = base.mark_bar(height=8, cornerRadiusEnd=3).encode(
        x=alt.X("pct:Q", title="% d'intents de reparació", scale=alt.Scale(domain=[0, 70])),
        color=alt.Color("resultat:N", sort=resultats,
                        scale=alt.Scale(domain=resultats, range=[BLAU, BLAU_CLAR, TARONJA]),
                        legend=alt.Legend(title="Clica per ressaltar", orient="top", direction="horizontal")),
        opacity=opacitat,
        tooltip=[alt.Tooltip("objecte:N", title="Aparell"),
                 alt.Tooltip("resultat:N", title="Resultat"),
                 alt.Tooltip("pct:Q", title="%", format=".1f"),
                 alt.Tooltip("n:Q", title="Casos", format=",.0f"),
                 alt.Tooltip("total:Q", title="Intents en total", format=",.0f"),
                 alt.Tooltip("puntuacio:Q", title="Reparabilitat (1-10, segons voluntaris)", format=".1f")],
    ).add_params(clic)
    xifres = base.mark_text(align="left", dx=4, fontSize=9, color=TEXT).encode(
        x="pct:Q",
        text="text:N",
        opacity=opacitat,
    ).transform_calculate(text="format(datum.pct, '.0f') + ' %'")

    return (barres + xifres).properties(width=AMPLADA - 120, height=440,
                                        title=titol("Resultat de les reparacions per tipus d'aparell"))


def motius(carpeta):
    dades = pd.read_csv(carpeta / "motius_fracas.csv")
    grups = ["Tots els aparells elèctrics", "Ordinadors", "Mòbils i tauletes"]
    dades["llegenda"] = dades.grup + " (n = " + dades.total.map("{:,}".format).str.replace(",", ".") + ")"
    dades["ordre"] = dades.grup.map(grups.index)
    llegendes = [dades[dades.grup == g].llegenda.iloc[0] for g in grups]
    ordre = dades[dades.grup == grups[0]].sort_values("pct", ascending=False).motiu.tolist()
    clic = alt.selection_point(fields=["llegenda"], bind="legend")

    y = alt.Y("motiu:N", sort=ordre, title=None, axis=alt.Axis(labelLimit=300, labelFontSize=11))
    linia = alt.Chart(dades).mark_rule(color=GRIS, strokeWidth=3).encode(
        y=y,
        x=alt.X("min(pct):Q", title="% dels objectes no reparats", scale=alt.Scale(domain=[0, 45])),
        x2="max(pct):Q",
    )
    # Cada grup té un punt més petit que l'anterior, així si dos coincideixen es veuen tots dos
    punts = alt.Chart(dades).mark_circle(opacity=1, stroke="white", strokeWidth=1.5).encode(
        y=y,
        x="pct:Q",
        size=alt.Size("llegenda:N", sort=llegendes, scale=alt.Scale(domain=llegendes, range=[200, 110, 28]), legend=None),
        order="ordre:Q",
        color=alt.Color("llegenda:N", sort=llegendes,
                        scale=alt.Scale(domain=llegendes, range=[BLAU, VERD, TARONJA]),
                        legend=alt.Legend(title="Clica per ressaltar", orient="bottom", direction="vertical",
                                          labelLimit=400, symbolSize=90)),
        opacity=alt.condition(clic, alt.value(1), alt.value(0.15)),
        tooltip=[alt.Tooltip("grup:N", title="Grup"),
                 alt.Tooltip("motiu:N", title="Motiu"),
                 alt.Tooltip("pct:Q", title="% dels no reparats", format=".1f"),
                 alt.Tooltip("n:Q", title="Casos", format=",.0f")],
    ).add_params(clic)

    return (linia + punts).properties(width=AMPLADA - 280, height=300,
                                      title=titol("Motius pels quals no es va poder reparar"))
