# Guia d'estil del blog

Resum de l'estil que ja comparteixen les entrades del blog (obsolescència percebuda i programada, Samsung A40, fitxa de reparabilitat, repair cafés, suport de programari i HOP contra la impremta). El prefix `_` evita que Quarto renderitzi aquest fitxer.

## Estructura

- Front matter com a `posts/_plantilla/index.qmd`: `title`, `description` (una sola frase, surt a la targeta de la portada), `author`, `date` i `categories` en minúscula. Canvieu les categories de la plantilla (`categoria1`, `categoria2`).
- Trieu entre una i tres categories d'aquesta llista, sense inventar-ne de noves: `obsolescència`, `reparabilitat`, `normativa`, `programari`, `anàlisi de dades` i `experiència pròpia`.
- Introducció que situa el tema dins del fil del blog ("En articles anteriors…", "En aquest blog ens preguntem…") o amb una imatge quotidiana que porta a la pregunta de l'entrada.
- Seccions `##`. Funcionen bé els títols en forma de pregunta ("Funcionen?", "Com «mor» un telèfon?"). La numeració ("1.", "2.") és opcional, però no s'ha de barrejar dins d'una mateixa entrada.
- Conclusió explícita al final ("Conclusió", "Conclusions" o "I ara, què?") que recull la tesi i la baixa al cas concret (el mòbil, VINCLE DIGITAL).
- Enllaços entre entrades amb camins relatius, com `[Samsung Galaxy A40](../reparacio-samsung-a40/)`.

## Veu

- Català estàndard, to divulgatiu i seriós però proper, sense jerga.
- Primera persona del plural inclusiva per explicar i raonar ("hem vist", "ens porta a una pregunta").
- Primera persona del singular només quan hi ha experiència pròpia, amb narració cronològica en passat ("vaig obrir", "em vaig encallar").
- Tesi comuna del blog: un mòbil no deixa de servir només per motius tècnics. Hi influeixen la percepció, el programari, el disseny i la normativa.
- Sigueu prudents amb les dades: digueu la mida de la mostra i marqueu els límits ("la mostra és petita, cal llegir-ho com un indici", "crec que…"). Eviteu les afirmacions generals que la font no sosté.

## Fonts i dades

- Cada afirmació important porta una cita `[@clau]`; la clau ha d'existir a `references.bib`.
- Doneu xifres concretes amb la mida de la mostra ("N = 563 models", "617 persones").
- Prioritzeu estudis acadèmics, institucions europees i ONG. Citeu la normativa pel número (reglament (UE) 2023/1669 i 2023/1670, directiva (UE) 2024/1799).
- No copieu fragments llargs de les fonts: resumiu-los amb les vostres paraules.

## Figures i taules

- Peu de figura: "Font: elaboració pròpia a partir de …". Si les dades són d'una altra font i el gràfic és propi, digueu-ho.
- Peu de taula amb `: Font…` o `: Elaboració pròpia.` just després de la taula.
- Gràfics propis (Altair/Python), no imatges trobades. Si l'entrada en porta, guardeu les dades i el codi a la carpeta de l'entrada.
- Els `callout` de Quarto es poden fer servir per a resums, avisos i xifres clau.
- Imatges a la carpeta de l'entrada, amb `width` i `fig-align` quan calgui.

## Tipografia (unificar)

Les entrades actuals no coincideixen en aquests punts. Proposta:

| Element | Criteri |
|---|---|
| Milers i decimals | Format català: `1.000`, `55,3` |
| Percentatge | Amb espai: `60 %` |
| Cometes | Angulars `«…»` per a cites i termes; no barrejar amb `"…"` |
| Apòstrof | Sempre `'` (recte) |
| Anglicismes (*software*, *hardware*, *patch*) | En cursiva, sempre |
| Títols | Només la primera lletra en majúscula, sense punt final |

## Abans de publicar

- Canvieu categories, `description` i `author`, i descomenteu `image` si hi ha portada.
- Reviseu l'ortografia i els noms propis (HOP, Epson, Which?).
- Comproveu que totes les cites `[@clau]` surten a la pàgina de Referències.
