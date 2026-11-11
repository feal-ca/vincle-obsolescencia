"""Escenaris de la població de mòbils del Regne Unit, 2013–2019.

Dos passos:
1. `entrades()` escriu escenaris_uk.csv: un valor per any, paràmetre i escenari, amb la regla
   o la font de cada valor. Les xifres i el perquè són a fonts_externes_uk.md i
   ordres_de_magnitud_uk.md.
2. `balanc()` llegeix el CSV i calcula el parc, les vendes, les sortides per via i per causa,
   i el calaix. Escriu balanc_escenaris_uk.csv i imprimeix les taules per al document.

Escenaris: pessimista, central i optimista sobre l'obsolescència (només mouen les palanques).
Banda d'ancoratge: baix i alt, amb les palanques centrals i el parc a les seves dues cotes.

Ús: python3 posts/avaries-mobil/_estimacio/escenaris_uk.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
ARREL_ANALISI = AQUI.parents[1] / "vida-material" / "_analisi"
sys.path.insert(0, str(ARREL_ANALISI))
from comu import GRUPS, RAW  # noqa: E402

ANYS = list(range(2013, 2020))
ESCENARIS = ["pessimista", "central", "optimista"]
BANDA = ["baix", "alt"]
VIES = ["calaix", "familia", "mercat", "reciclatge", "escombraries", "perdut"]

# --- Ancoratges tancats (fonts_externes_uk.md) -------------------------------------------
POBLACIO = dict(zip(ANYS, [64_105_700, 64_596_800, 65_110_000, 65_648_000,
                           66_040_229, 66_435_550, 66_796_807]))
PEN_MOBIL = dict(zip(ANYS, [.92, .93, .93, .93, .94, .94, .94]))       # Ofcom, adults 16+
PEN_SMART = dict(zip(ANYS, [.51, .61, .66, .71, .76, .78, .79]))       # Ofcom, adults 16+
SUBS_TERMINAL = dict(zip(ANYS, [78.2e6, 78.9e6, 79.7e6, 79.4e6, 79.1e6, 79.5e6, 81.0e6]))
SEGONA_MA = dict(zip(ANYS, [.08, .09, .10, .11, .13, .15, .15]))      # Deloitte 2015–2019
# Kantar, «temps de primer ús» (mesos), sèrie antiga. 2017–2019: sèrie nova − 1,8 mesos.
DURADA_GB = dict(zip(ANYS, [20.0, 22.0, 23.5, 23.4, 24.65, 25.9, 26.9]))
DURADA_EU5 = dict(zip(ANYS, [18.3, 19.5, 20.4, 21.6, 23.0, 24.4, 25.4]))
QUOTA_SMART_VENDES = dict(zip(ANYS, [.77, .82, .85, .87, .89, .90, .91]))

# --- Supòsits Fermi (ordres_de_magnitud_uk.md) -------------------------------------------
QUOTA_ADULTS = 0.81          # 16+ sobre la població
MOBILS_PER_USUARI = 1.05     # Ofcom 2019: 88 % un número, 6 % dos
MOBILS_MENORS = 0.06         # telèfons de menors de 16 anys per habitant

# Destí del telèfon anterior (Deloitte UK 2015, 2017, 2018; BidGrid 2013), en punts.
DESTI = {
    "BidGrid 2013":  dict(calaix=33, familia=15, mercat=27, reciclatge=4, escombraries=16, perdut=0),
    "Deloitte 2015": dict(calaix=43, familia=20, mercat=20, reciclatge=4, escombraries=7, perdut=1),
    "Deloitte 2017": dict(calaix=37, familia=24, mercat=20, reciclatge=4, escombraries=4, perdut=2),
    "Deloitte 2018": dict(calaix=41, familia=20, mercat=18, reciclatge=5, escombraries=5, perdut=3),
}
MERCAT_REVENUT = 0.97        # O2 Recycle 2015: 95–99 % en funcionament i revenuts
MERCAT_QUEDA_UK = 0.43       # O2 Recycle 2015: dels revenuts, 43 % al Regne Unit

# Eurobaròmetre 503 (des. 2019, Regne Unit): respostes sobre 119 punts de resposta
EB_TRENCAT, EB_RENDIMENT, EB_TOTAL = 41, 25, 119
AKWIEN_DEFECTE, DURADA_GB_2015 = 0.10, 23.5 / 12


def desti_central(a):
    """Punts de cada via per a l'any a: Deloitte interpolat; 2013 barreja BidGrid i Deloitte."""
    d = {k: pd.Series(v) for k, v in DESTI.items()}
    b13 = (d["BidGrid 2013"] + d["Deloitte 2015"]) / 2
    taula = {2013: b13, 2014: (b13 + d["Deloitte 2015"]) / 2, 2015: d["Deloitte 2015"],
             2016: (d["Deloitte 2015"] + d["Deloitte 2017"]) / 2, 2017: d["Deloitte 2017"],
             2018: d["Deloitte 2018"], 2019: d["Deloitte 2018"]}
    return taula[a]


def ratios_extrems():
    """Extrem pitjor i millor de cada via entre les quatre enquestes, sobre la mitjana."""
    t = pd.DataFrame(DESTI).T
    mitjana = t.mean()
    pitjor = {"calaix": t.calaix.max(), "familia": t.familia.min(), "mercat": t.mercat.min(),
              "reciclatge": t.reciclatge.min(), "escombraries": t.escombraries.max(),
              "perdut": t.perdut.max()}
    millor = {"calaix": t.calaix.min(), "familia": t.familia.max(), "mercat": t.mercat.max(),
              "reciclatge": t.reciclatge.max(), "escombraries": t.escombraries.min(),
              "perdut": t.perdut.min()}
    return ({k: pitjor[k] / mitjana[k] if mitjana[k] else 1 for k in VIES},
            {k: millor[k] / mitjana[k] if mitjana[k] else 1 for k in VIES})


def causes_finestra():
    """Quota de cada grup de causa a MobiFix (Regne Unit), finestra de tres anys centrada."""
    d = pd.read_csv(RAW / "ora_mobifix.csv")
    d = d[(d.country == "GBR") & d.repair_status.isin(["Fixed", "Repairable", "End of life"])]
    d["any"] = pd.to_numeric(d.event_date.str[:4], errors="coerce")
    d = d[d["any"].between(2013, 2019)]
    d["causa"] = d.fault_type.map(GRUPS).fillna("Altres")
    grups = sorted(set(GRUPS.values()))
    sortida = {}
    for a in ANYS:
        w = d[d["any"].between(a - 1, a + 1)]
        sortida[a] = (w.causa.value_counts(normalize=True).reindex(grups, fill_value=0), len(w))
    return sortida


def entrades():
    files = []

    def posa(a, param, esc, valor, unitat, regla):
        files.append(dict(any=a, parametre=param, escenari=esc, valor=valor,
                          unitat=unitat, regla_o_font=regla))

    pitjor, millor = ratios_extrems()
    h = {"pessimista": (EB_TRENCAT + EB_RENDIMENT) / EB_TOTAL / (DURADA_GB[2019] / 12),
         "central": EB_TRENCAT / EB_TOTAL / (DURADA_GB[2019] / 12),
         "optimista": AKWIEN_DEFECTE / DURADA_GB_2015}
    causes = causes_finestra()

    for a in ANYS:
        # Ancoratges
        posa(a, "poblacio", "central", POBLACIO[a], "persones", "ONS, mitjan any")
        posa(a, "penetracio_mobil", "central", PEN_MOBIL[a], "fracció adults 16+", "Ofcom Technology Tracker / CMR")
        posa(a, "penetracio_smartphone", "central", PEN_SMART[a], "fracció adults 16+", "Ofcom Technology Tracker / CMR")
        baix = POBLACIO[a] * (QUOTA_ADULTS * PEN_MOBIL[a] * MOBILS_PER_USUARI + MOBILS_MENORS)
        alt = SUBS_TERMINAL[a]
        posa(a, "parc", "baix", baix, "telèfons",
             "persones: població × (0,81 × penetració × 1,05 + 0,06) (Fermi)")
        posa(a, "parc", "alt", alt, "telèfons", "Ofcom: subscripcions de terminal (sense M2M ni dades)")
        posa(a, "parc", "central", (baix + alt) / 2, "telèfons", "mitjana de la cota per persones i per SIM")
        posa(a, "quota_segona_ma", "central", SEGONA_MA[a], "fracció del parc",
             "Deloitte UK 2015–2019 (2013–2014 extrapolat)")
        posa(a, "quota_smartphone_vendes", "central", QUOTA_SMART_VENDES[a], "fracció",
             "GfK via Ofcom: 74 % T1 2013, 89 % T4 2017 (contracte); interpolat, 2018–2019 Fermi")

        # Palanca: durada de primer ús
        posa(a, "durada_primer_us", "central", DURADA_GB[a] / 12, "anys",
             "Kantar GB, sèrie antiga (2017–2019: sèrie nova − 1,8 mesos)")
        posa(a, "durada_primer_us", "pessimista", DURADA_EU5[a] / 12, "anys",
             "Kantar EU5, sèrie antiga (més curta que GB)")
        posa(a, "durada_primer_us", "optimista", (DURADA_GB[a] + 1.8) / 12, "anys",
             "Kantar GB, sèrie nova (+1,8 mesos); Dixons 29 mesos el 2017")

        # Palanca: destí del telèfon que el titular deixa
        central = desti_central(a)
        for esc, r in [("central", None), ("pessimista", pitjor), ("optimista", millor)]:
            v = central if r is None else central * pd.Series(r)
            v = v / v.sum()
            for via in VIES:
                regla = ("Deloitte UK 2015/2017/2018, BidGrid 2013; interpolat" if r is None else
                         f"central × extrem {'pitjor' if esc == 'pessimista' else 'millor'} "
                         f"de les 4 enquestes ({r[via]:.2f})")
                posa(a, f"desti_{via}", esc, v[via], "fracció de les deixades", regla)

        # Palanca: part de les deixades per avaria = taxa × durada de primer ús (central)
        regles = {"pessimista": "Eurobaròmetre 503: trencat + rendiment, normalitzat; × durada",
                  "central": "Eurobaròmetre 503: trencat, normalitzat (0,345 el 2019); × durada",
                  "optimista": "AK Wien 2015: defecte tècnic estricte (10 %); × durada"}
        for esc in ESCENARIS:
            posa(a, "part_avaria", esc, min(h[esc] * DURADA_GB[a] / 12, 1), "fracció de les deixades",
                 regles[esc])

        # Palanca: calaix
        for esc, ini, estada, recic in [("pessimista", 9e7, 7, .45), ("central", 5e7, 4, .65),
                                        ("optimista", 3e7, 2.5, .80)]:
            if a == 2013:
                posa(a, "calaix_inicial", esc, ini, "telèfons",
                     {"pessimista": "Deloitte 2015 cita 85 M; Mobile News 2014 90 M",
                      "central": "Green Alliance 2015: 28–125 M (Fermi)",
                      "optimista": "Green Alliance 2015 (28 M); uSwitch 2021 (35 M)"}[esc])
            posa(a, "estada_calaix", esc, estada, "anys",
                 "Fermi: calaix / entrada anual (Material Focus 2017: entrada ≈ sortida)")
            posa(a, "calaix_a_reciclatge", esc, recic, "fracció de les sortides del calaix",
                 "Material Focus 2017: 65 % de les descartades no reutilitzades (central); ±Fermi")

        # Causes: iguals en tots els escenaris
        quotes, n = causes[a]
        for causa, q in quotes.items():
            posa(a, f"causa_{causa}", "central", q, "fracció de les baixes per avaria",
                 f"MobiFix Regne Unit, finestra {max(a - 1, 2013)}–{min(a + 1, 2019)}, n = {n}")

    df = pd.DataFrame(files)
    df.to_csv(AQUI / "escenaris_uk.csv", index=False, float_format="%.6g")
    return df


def valor(df, a, param, esc):
    """Valor del paràmetre; si l'escenari no en té, el central."""
    s = df[(df["any"] == a) & (df.parametre == param)]
    v = s[s.escenari == esc]
    return float((v if len(v) else s[s.escenari == "central"]).valor.iloc[0])


def balanc(df):
    sortida = []
    for esc in ESCENARIS + BANDA:
        palanques = esc if esc in ESCENARIS else "central"
        parc = {a: valor(df, a, "parc", esc if esc in BANDA else "central") for a in ANYS}
        # Parc del 2020 extrapolat amb la tendència 2018–2019 (Fermi)
        parc[2020] = parc[2019] + (parc[2019] - parc[2018])
        calaix = valor(df, 2013, "calaix_inicial", palanques)
        for a in ANYS:
            durada = valor(df, a, "durada_primer_us", palanques)
            u = valor(df, a, "quota_segona_ma", palanques)
            adquisicions = parc[a] / durada
            vendes = adquisicions * (1 - u)
            sortides = parc[a] + vendes - parc[a + 1]
            d = {v: valor(df, a, f"desti_{v}", palanques) for v in VIES}
            revenut = d["mercat"] * MERCAT_REVENUT
            reus_uk = d["familia"] + revenut * MERCAT_QUEDA_UK
            no_reus = 1 - reus_uk
            via = {
                "calaix": d["calaix"] / no_reus,
                "exportacio": revenut * (1 - MERCAT_QUEDA_UK) / no_reus,
                "reciclatge": (d["reciclatge"] + d["mercat"] * (1 - MERCAT_REVENUT)) / no_reus,
                "escombraries": d["escombraries"] / no_reus,
                "perdut": d["perdut"] / no_reus,
            }
            avaria = min(valor(df, a, "part_avaria", palanques) * adquisicions, sortides)
            estada = valor(df, a, "estada_calaix", palanques)
            surt_calaix = calaix / estada
            recic_calaix = surt_calaix * valor(df, a, "calaix_a_reciclatge", palanques)
            fila = dict(escenari=esc, any=a, parc=parc[a], vendes=vendes,
                        vendes_smartphone=vendes * valor(df, a, "quota_smartphone_vendes", palanques),
                        adquisicions=adquisicions, reutilitzats_uk=adquisicions * reus_uk,
                        sortides=sortides, durada_implicita=parc[a] / vendes,
                        # Les vies es reparteixen sobre les sortides del balanç, que són més que
                        # les deixades no reutilitzades segons les enquestes: (1 − u) / (1 − reús)
                        inflacio_vies=sortides / (adquisicions * no_reus),
                        sortides_avaria=avaria, sortides_sense_avaria=sortides - avaria,
                        calaix=calaix, surt_calaix=surt_calaix,
                        reciclatge_total=sortides * via["reciclatge"] + recic_calaix)
            fila.update({f"via_{k}": sortides * v for k, v in via.items()})
            fila["suma_vies"] = sum(via.values())
            for p in df[(df["any"] == a) & df.parametre.str.startswith("causa_")].parametre:
                fila[p.replace("causa_", "avaria_")] = avaria * valor(df, a, p, "central")
            sortida.append(fila)
            calaix += sortides * via["calaix"] - surt_calaix
    b = pd.DataFrame(sortida)
    b.to_csv(AQUI / "balanc_escenaris_uk.csv", index=False, float_format="%.6g")
    return b


def informe(b):
    m = lambda x: f"{x / 1e6:.1f}"  # noqa: E731
    cols = ["parc", "vendes", "vendes_smartphone", "sortides", "durada_implicita", "sortides_avaria",
            "via_calaix", "via_exportacio", "via_reciclatge", "via_escombraries", "calaix",
            "reciclatge_total"]
    for esc in ESCENARIS + BANDA:
        t = b[b.escenari == esc].set_index("any")[cols]
        print(f"\n## {esc}")
        print(t.apply(lambda c: c.map(lambda x: f"{x:.2f}" if c.name == "durada_implicita" else m(x)))
              .T.to_string())
    print("\nComprovacions")
    print("suma de vies = 1:", np.allclose(b.suma_vies, 1))
    print("durada implícita 1,5–3:", b.durada_implicita.between(1.5, 3).all(),
          round(b.durada_implicita.min(), 2), round(b.durada_implicita.max(), 2))
    p = b.pivot(index="any", columns="escenari")
    print("ordre escombraries:",
          ((p.via_escombraries.pessimista > p.via_escombraries.central)
           & (p.via_escombraries.central > p.via_escombraries.optimista)).all())
    print("ordre avaria:",
          ((p.sortides_avaria.pessimista > p.sortides_avaria.central)
           & (p.sortides_avaria.central > p.sortides_avaria.optimista)).all())
    print("avaria ≤ sortides:", (b.sortides_avaria <= b.sortides + 1).all())
    print("ordre reutilització (optimista > central > pessimista):",
          ((p.reutilitzats_uk.optimista > p.reutilitzats_uk.central)
           & (p.reutilitzats_uk.central > p.reutilitzats_uk.pessimista)).all())
    print("inflació de les vies (sortides ÷ deixades no reutilitzades):",
          round(b.inflacio_vies.min(), 2), "–", round(b.inflacio_vies.max(), 2))

    # Contrast amb vendes mesurades: Canalys (enviaments) i GfK (punt de venda), smartphones
    canalys = {2013: 30, 2014: 31, 2015: 32, 2016: 28, 2017: 27}
    print("\nVendes de smartphones (M): model vs mesurades")
    print(pd.DataFrame({"baix": p.vendes_smartphone.baix / 1e6, "central": p.vendes_smartphone.central / 1e6,
                        "alt": p.vendes_smartphone.alt / 1e6, "Canalys": pd.Series(canalys),
                        "GfK": pd.Series({2015: 23.7})}).round(1).to_string())
    print("ràtio 2018/2017 central:", round(p.vendes_smartphone.central[2018] / p.vendes_smartphone.central[2017], 2),
          "(Strategy Analytics T4: 0,86)")

    # Contrast amb Material Focus 2017: massa per telèfon i telèfons reciclats
    massa = 2.512e6 / p.vendes.central[2017]
    print(f"\nMaterial Focus 2017: massa implícita {massa:.3f} kg; reciclats {1.035e6 / massa / 1e6:.1f} M;"
          f" model central {p.reciclatge_total.central[2017] / 1e6:.1f} M")
    print("Baixes per avaria 2019 (M):", (p.sortides_avaria.loc[2019] / 1e6).round(1).to_dict(),
          "· SquareTrade 2020: 13 M incidents l'any")


if __name__ == "__main__":
    informe(balanc(entrades()))
