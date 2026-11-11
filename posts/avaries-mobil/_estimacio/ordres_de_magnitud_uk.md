# Paràmetres per any i escenaris del model de població de mòbils (Regne Unit, 2013–2019)

Revisat el 2026-11-11. Aquí hi ha, per a cada any, els valors que no surten directament d'una dada tancada: o bé es deriven d'una relació, o bé són un ordre de magnitud. Les dades tancades són a [`fonts_externes_uk.md`](fonts_externes_uk.md) i les cito per secció (p. ex. «F §2.1»). Tots els valors són a `escenaris_uk.csv` i el balanç el calcula `escenaris_uk.py` (sortida: `balanc_escenaris_uk.csv`).

## Com s'ha de llegir

**Model.** El parc de telèfons en ús de cada any és un ancoratge. Les vendes surten del parc i de la durada de primer ús. Les sortides tanquen el balanç:

- adquisicions = parc ÷ durada de primer ús;
- vendes de telèfons nous = adquisicions × (1 − part de segona mà);
- sortides de l'any = parc(t) + vendes(t) − parc(t+1).

Les sortides es reparteixen de dues maneres que no se sumen: **per via** (calaix, exportació, reciclatge, escombraries, perdut) i **per causa** (avaria repartida amb les causes de MobiFix, o sense avaria).

**Ancoratges, palanques i tancament.**

| Classe | Què hi entra | Com es mou |
|---|---|---|
| Ancoratges | població, penetració, parc, part de segona mà, part de smartphones en les vendes | igual en els tres escenaris; la seva incertesa és la **banda d'ancoratge** (baix i alt) |
| Palanques | durada de primer ús, destí del telèfon deixat, part per avaria, calaix | escenari pessimista, central o optimista |
| Tancament | vendes, sortides, durada implícita (parc ÷ vendes) | es calculen |

**Escenaris.**
- **Pessimista:** vida curta, menys segona vida, més escombraries i més baixes per avaria.
- **Optimista:** el contrari.
- **Coherència:** cada valor no central diu de quina font o extrem surt. Els escenaris són **cotes coherents, no intervals de confiança**: no combinen tots els extrems possibles, només els que empitjoren o milloren l'obsolescència alhora.

**Canvis respecte del pla aprovat.**
1. La durada de primer ús passa de variable de tancament a palanca, i les vendes passen a ser de tancament. El motiu és que les vendes mesurades no coincideixen entre elles (Canalys 32 milions, GfK 23,7 el 2015) i la durada sí que té sèrie anual (Kantar). Les vendes mesurades queden com a contrast (§3).
2. Les causes són iguals en els tres escenaris, en lloc de fer servir els extrems de l'interval binomial: els extrems de cada causa per separat no sumen 1. L'interval es dona a §8 com a banda.
3. El script es diu `escenaris_uk.py`, no `balanç_escenaris.py`, per evitar la «ç» al nom.

**Supòsit declarat.** Els percentatges de causes de MobiFix (Regne Unit, finestres de tres anys) representen les causes de totes les baixes per avaria del Regne Unit.

## 1. Parc de telèfons en ús (ancoratge)

**Dues cotes d'una mateixa mesura.**
- **Cota per persones (baix).** Població × (0,81 adults × penetració de mòbil de l'Ofcom × 1,05 mòbils per usuari + 0,06 telèfons de menors per habitant).
- **Cota per SIM (alt).** Subscripcions de terminal de l'Ofcom (F §2.3).
- **Central.** La mitjana de les dues cotes.

| Milions | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| baix (persones) | 54,0 | 55,0 | 55,4 | 55,9 | 56,8 | 57,1 | 57,4 |
| **central** | **66,1** | **66,9** | **67,6** | **67,6** | **67,9** | **68,3** | **69,2** |
| alt (SIM de terminal) | 78,2 | 78,9 | 79,7 | 79,4 | 79,1 | 79,5 | 81,0 |
| part de smartphones (Ofcom smartphone ÷ mòbil) | 0,55 | 0,66 | 0,71 | 0,76 | 0,81 | 0,83 | 0,84 |

**Per què dues cotes.**
- La cota per persones no compta els telèfons d'empresa ni els segons telèfons.
- La de SIM compta SIM de doble línia i de prepagament que no són aparells diferents.

**Ordres de magnitud de la cota baixa.**
- **0,81 adults sobre la població.** Ordre de magnitud: a l'ONS els menors de 16 anys són prop d'una cinquena part.
- **1,05 mòbils per usuari.** L'Ofcom 2019 diu que el 6 % té dos números (F §2.1).
- **0,06 telèfons de menors per habitant.** Uns 4 milions de nens de 8 a 15 anys amb mòbil. És un ordre de magnitud: no l'he verificat en aquesta cerca.

**Parc del 2020.** Per calcular les sortides del 2019 cal el parc del 2020. S'extrapola amb la tendència del 2018 al 2019.

## 2. Durada de primer ús (palanca)

| Anys | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| pessimista | 1,53 | 1,63 | 1,70 | 1,80 | 1,92 | 2,03 | 2,12 |
| **central** | **1,67** | **1,83** | **1,96** | **1,95** | **2,05** | **2,16** | **2,24** |
| optimista | 1,82 | 1,98 | 2,11 | 2,10 | 2,20 | 2,31 | 2,39 |

**Per què.**
- **Central, 2013–2016.** Kantar, Gran Bretanya, sèrie antiga (F §4).
- **Central, 2018.** El valor de la sèrie nova (27,7 mesos) menys el desfasament entre sèries que Kantar dona per a EU5 el 2016 (23,4 − 21,6 = 1,8 mesos). Dona 25,9 mesos.
- **Central, 2017 i 2019.** El 2017 és la interpolació; el 2019 suma un mes, la meitat del ritme de Kantar EU5 entre el 2019 i el 2021 (+2,8 mesos en dos anys).
- **Pessimista.** La sèrie EU5 de Kantar, més curta que la de Gran Bretanya, amb la mateixa extensió per al 2017–2019.
- **Optimista.** La sèrie nova de Kantar (+1,8 mesos). És coherent amb els 29 mesos de Dixons el 2017.
- **Contrast.**
  - Deloitte: 66 %, 62 % i 59 % dels smartphones adquirits en els 18 mesos anteriors (2016–2018). Si les edats fossin exponencials, la durada seria de 1,4 a 1,7 anys; si es renovés a edat fixa, de 2,3 a 2,5. Els valors de Kantar queden entremig.
  - El sentit creixent coincideix amb totes les fonts.

**Si fos diferent.** Mou les vendes i les sortides en proporció inversa: amb un 10 % més de durada, un 10 % menys de vendes.

## 3. Vendes (tancament) i contrast amb les vendes mesurades

Vendes de telèfons nous = parc ÷ durada × (1 − part de segona mà). La part de segona mà és de Deloitte: 0,10, 0,11, 0,13, 0,15 i 0,15 per al 2015–2019 (el 2017 és derivat del «+2 punts» del 2018), i 0,08 i 0,09 extrapolats per al 2013 i el 2014. La part de smartphones sobre les vendes va de 0,77 el 2013 a 0,89 el 2017, interpolant el 74 % de GfK del 1T 2013 i el 89 % del 4T 2017 (F §3); 0,90 i 0,91 per al 2018–2019 són ordre de magnitud.

| Smartphones venuts (milions) | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| model, banda baixa | 23,0 | 22,4 | 21,6 | 22,2 | 21,4 | 20,2 | 19,8 |
| **model, central** | **28,1** | **27,2** | **26,4** | **26,9** | **25,6** | **24,2** | **23,9** |
| model, banda alta | 33,2 | 32,1 | 31,1 | 31,5 | 29,8 | 28,2 | 27,9 |
| Canalys (enviaments) | 30 | 31 | 32 | 28 | 27 | – | – |
| GfK (punt de venda) | – | – | 23,7 | – | – | – | – |

**Lectura.**
- La cota per persones dona vendes a prop de GfK; la cota per SIM, a prop de Canalys.
- Les dues discrepàncies (parc i vendes) són per tant una sola: telèfons d'empresa, segons telèfons i estoc del canal.
- Per això la banda d'ancoratge mou el parc i les vendes alhora.

**Discrepàncies que queden.**
- **Caiguda 2017–2018.** El model fa caure les vendes un 5 % entre el 2017 i el 2018. Strategy Analytics mesura un −14 % al 4T i Canalys un −30 % al 1T: el model suavitza la caiguda.
- **Tendència de MarketLine.** Creix (36,6 i 37,6 milions el 2016 i el 2017) i no coincideix amb cap de les altres fonts.

| Total de mòbils venuts (milions) | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| pessimista | 39,9 | 37,5 | 35,8 | 33,4 | 30,8 | 28,6 | 27,8 |
| **central** | **36,5** | **33,2** | **31,0** | **30,9** | **28,8** | **26,9** | **26,2** |
| optimista | 33,5 | 30,7 | 28,8 | 28,7 | 26,8 | 25,2 | 24,6 |

## 4. Destí del telèfon que el titular deixa (palanca)

**Fracció de les deixades, central.**

| Via | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| calaix | 0,40 | 0,43 | 0,45 | 0,43 | 0,41 | 0,45 | 0,45 |
| familiar o amic | 0,18 | 0,20 | 0,21 | 0,24 | 0,26 | 0,22 | 0,22 |
| venda al mercat | 0,25 | 0,23 | 0,21 | 0,22 | 0,22 | 0,20 | 0,20 |
| reciclatge gratuït | 0,04 | 0,04 | 0,04 | 0,04 | 0,04 | 0,05 | 0,05 |
| escombraries | 0,12 | 0,10 | 0,07 | 0,06 | 0,04 | 0,05 | 0,05 |
| perdut o robat | 0,01 | 0,01 | 0,01 | 0,02 | 0,02 | 0,03 | 0,03 |

**Com s'han construït les dades centrals.**
- **Fonts.** Deloitte 2015, 2017 i 2018 (F §5.1), sense «altres» ni «no ho sap», i normalitzat.
- **2013.** Mitjana de BidGrid 2013 i Deloitte 2015. BidGrid pesa poc: no diu la mostra.
- **2014 i 2016.** Interpolats.
- **2019.** Igual que el 2018.
- **Reciclatge del 2015.** Deloitte 2015 no tenia l'opció; es pren el 4 % del 2017.

**Escenaris.** Cada via es multiplica per l'extrem de les quatre enquestes dividit per la seva mitjana, i després es normalitza.

| Via | Multiplicador pessimista | Multiplicador optimista |
|---|---|---|
| escombraries | ×2,0 (BidGrid, 16 %) | ×0,5 (Deloitte 2017, 4 %) |
| familiar o amic | ×0,76 | ×1,22 |
| venda | ×0,85 | ×1,27 |
| calaix | ×1,12 | ×0,86 |
| reciclatge | ×0,92 | ×1,15 |

**De les deixades a les sortides del parc.**
- **Supòsit d'O2 Recycle 2015.** Dels venuts al mercat, el 97 % es revenen i el 3 % es reciclen. Dels revenuts, el 43 % es queda al Regne Unit (F §5.4).
- **Reutilització al Regne Unit.** Ho són els passats a un familiar més el 43 % dels revenuts. Continuen en ús i no són sortides.
- **Sortides.** La resta es reparteix entre les vies de sortida en proporció.
- **Exportació.** El 57 % dels revenuts.

**Una discrepància estructural que infla les vies.**
- **Dues mesures de reutilització.** Les enquestes de destí diuen que un 30 % de les deixades es reutilitza al Regne Unit (familiar més revenda interior). La part de segona mà dels telèfons en ús que fan servir les vendes (Deloitte) és només del 10–15 %.
- **Explicació probable.** Els telèfons passats als menors, que Deloitte no entrevista, i els «regalats» que acaben en un altre calaix.
- **Efecte en les vies.** El balanç fa sortir del parc més telèfons dels que les enquestes deixen sense reutilitzar. Repartir aquestes sortides en proporció infla totes les vies d'un factor 1,17–1,33 en el central (`inflacio_vies` a `balanc_escenaris_uk.csv`; 1,06–1,18 en el pessimista i 1,31–1,50 en l'optimista).
- **Conseqüència.** És la causa comuna de l'excés de calaix (§6) i d'exportació (§9) respecte de Material Focus i Technavio.
- **Escenaris.** La reutilització al Regne Unit sí que segueix l'ordre dels escenaris: el 2019 és de 7,3 milions al pessimista, 9,2 al central i 10,8 a l'optimista.
- **Perdut o robat.** A l'optimista és zero perquè BidGrid no té aquesta categoria i en dona el mínim.

**Per què no més precisió.**
- Les enquestes tenen bases diferents: propietaris de smartphone en el cas de Deloitte; persones que substitueixen el telèfon en el de BidGrid.
- La proporció del 43 % que es queda al Regne Unit és d'un sol operador i d'un sol any. Bernstein dona un 70 % d'exportació a països emergents (F §5.4): l'exportació podria ser un 20 % més gran.

## 5. Part de les deixades per avaria (palanca)

**Relació.** Si les avaries arriben a un ritme constant *h* i les renovacions per desig a un altre, la part de les deixades per avaria és *h* × durada de primer ús. Així, la part creix quan la renovació s'allarga. És coherent amb la direcció de totes les fonts: la gent espera més i canvia quan el telèfon falla.

| Fracció | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| pessimista | 0,41 | 0,45 | 0,49 | 0,48 | 0,51 | 0,53 | 0,56 |
| **central** | **0,26** | **0,28** | **0,30** | **0,30** | **0,32** | **0,33** | **0,35** |
| optimista | 0,09 | 0,09 | 0,10 | 0,10 | 0,11 | 0,11 | 0,11 |

**Per què.**
- **Central.**
  - Eurobaròmetre 503 (F §6), al Regne Unit, desembre 2019: «el vaig trencar» 41 de 119 punts de resposta, 0,345 un cop normalitzat. Les persones que van substituir algun dispositiu van donar 1,35 respostes de mitjana, de manera que el 47 % no és una part de les substitucions fins que es divideix.
  - Dona *h* = 0,154 l'any.
  - La pregunta és sobre qualsevol dispositiu digital, no només mòbils.
- **Pessimista.**
  - «Trencat» més «rendiment empitjorat» (66 de 119, 0,555): inclou la degradació de bateria.
  - Dona *h* = 0,248.
- **Optimista.**
  - Defecte tècnic estricte, AK Wien (Àustria 2015, un 10 %), amb la durada de Gran Bretanya del 2015.
  - Dona *h* = 0,051.
- **Fonts compatibles amb el rang.**
  - Nordic 2017: un 40 % «no funcionava».
  - Which? 2021–2025: un 42 % no funcionava en substituir-lo.
  - Kantar 2021: 1 de cada 2, en plena COVID.

**Baixes per avaria resultants i contrast amb la incidència.**

| Milions | 2013 | 2015 | 2017 | 2019 | ÷ sortides el 2019 |
|---|---|---|---|---|---|
| pessimista | 17,9 | 19,3 | 18,0 | 18,1 | 0,67 |
| **central** | **10,2** | **10,4** | **10,4** | **10,6** | **0,42** |
| optimista | 3,1 | 3,2 | 3,2 | 3,3 | 0,14 |

**Comparació amb la incidència.**
- SquareTrade (2020) compta 13 milions de persones amb un incident en dotze mesos.
- **Central.** Queda per sota de la incidència.
- **Pessimista.** La supera: només és possible si s'hi compta la degradació de bateria i rendiment, que no és un «incident». Per això és la cota pessimista.

## 6. Calaix (palanca)

| | pessimista | central | optimista |
|---|---|---|---|
| telèfons al calaix el 2013 | 9×10⁷ | 5×10⁷ | 3×10⁷ |
| estada mitjana al calaix | 7 anys | 4 anys | 2,5 anys |
| part de les sortides del calaix que va a reciclatge | 0,45 | 0,65 | 0,80 |

**Per què.**
- **Valor inicial.** El calaix inicial va de 28 a 125 milions segons Green Alliance (2015).
  - Pessimista: 85–90 milions (Deloitte 2015, Mobile News 2014).
  - Optimista: 28–35 milions (Green Alliance, uSwitch 2021).
  - Central: una mitjana geomètrica arrodonida.
- **Estada.** 4 anys, ordre de magnitud. Material Focus 2017 dona una entrada al calaix d'uns 10 milions de telèfons l'any (0,871 kt amb 0,087 kg per telèfon); amb 5×10⁷ al calaix serien uns 5 anys d'estada.
- **El model no és estacionari.** Material Focus dona entrada i sortida iguals (0,871 i 0,907 kt). En el model central, en canvi, el calaix creix de 50 a 70 milions: l'entrada (16–20 milions l'any) supera la sortida.
- **Discrepància.** L'entrada al calaix del model central (18 milions el 2017) és 1,8 vegades la de Material Focus. Una part és la inflació de les vies (§4, factor 1,33 el 2017); la resta pot venir de les enquestes (un 37–43 % «el guarda de recanvi»), que compten telèfons que després es passen o es venen.
- **Part a reciclatge.** El 65 % central és la part de reciclatge i retorn sobre els descartats no reutilitzats de Material Focus 2017. Els extrems són un ordre de magnitud (±Fermi).

| Calaix (milions) | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| pessimista | 90,0 | 97,4 | 104,4 | 111,6 | 116,1 | 118,3 | 118,2 |
| **central** | **50,0** | **57,5** | **62,8** | **67,1** | **69,8** | **70,3** | **69,2** |
| optimista | 30,0 | 35,6 | 38,7 | 40,9 | 41,8 | 40,8 | 39,5 |

## 7. Balanç per escenari (milions de telèfons)

**Central**

| | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| parc | 66,1 | 66,9 | 67,6 | 67,6 | 67,9 | 68,3 | 69,2 |
| vendes | 36,5 | 33,2 | 31,0 | 30,9 | 28,8 | 26,9 | 26,2 |
| sortides | 35,7 | 32,6 | 31,0 | 30,6 | 28,4 | 26,0 | 25,3 |
| · per avaria | 10,2 | 10,3 | 10,4 | 10,4 | 10,4 | 10,5 | 10,6 |
| · al calaix | 20,0 | 19,7 | 20,0 | 19,5 | 17,9 | 16,5 | 16,1 |
| · exportació | 6,8 | 5,8 | 5,1 | 5,4 | 5,4 | 4,0 | 3,9 |
| · reciclatge directe | 2,5 | 2,3 | 2,1 | 2,2 | 2,2 | 2,2 | 2,2 |
| · escombraries | 6,1 | 4,5 | 3,3 | 2,7 | 1,9 | 2,0 | 2,0 |
| · perdut o robat | 0,3 | 0,4 | 0,5 | 0,7 | 1,0 | 1,2 | 1,2 |
| reciclatge total (directe + des del calaix) | 10,6 | 11,6 | 12,3 | 13,1 | 13,6 | 13,7 | 13,4 |
| reutilitzats al Regne Unit (flux intern, no surt) | 11,4 | 10,7 | 10,3 | 11,3 | 11,8 | 9,5 | 9,2 |
| durada implícita (anys, parc ÷ vendes) | 1,81 | 2,01 | 2,18 | 2,19 | 2,36 | 2,54 | 2,64 |

**Pessimista**

| | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| vendes | 39,9 | 37,5 | 35,8 | 33,4 | 30,8 | 28,6 | 27,8 |
| sortides | 39,0 | 36,9 | 35,7 | 33,1 | 30,5 | 27,6 | 26,9 |
| · per avaria | 17,9 | 18,7 | 19,3 | 18,1 | 18,0 | 17,9 | 18,1 |
| · al calaix | 20,3 | 20,9 | 22,1 | 20,5 | 18,8 | 16,8 | 16,3 |
| · exportació | 5,3 | 4,7 | 4,3 | 4,3 | 4,3 | 3,1 | 3,0 |
| · reciclatge directe | 2,1 | 2,0 | 2,0 | 2,0 | 1,9 | 1,9 | 1,8 |
| · escombraries | 11,0 | 8,6 | 6,4 | 5,0 | 3,6 | 3,7 | 3,6 |
| reciclatge total | 7,9 | 8,3 | 8,7 | 9,1 | 9,4 | 9,5 | 9,4 |
| durada implícita | 1,66 | 1,79 | 1,89 | 2,02 | 2,20 | 2,39 | 2,49 |

**Optimista**

| | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| vendes | 33,5 | 30,7 | 28,8 | 28,7 | 26,8 | 25,2 | 24,6 |
| sortides | 32,6 | 30,1 | 28,8 | 28,4 | 26,4 | 24,2 | 23,7 |
| · per avaria | 3,1 | 3,2 | 3,2 | 3,2 | 3,2 | 3,3 | 3,3 |
| · al calaix | 17,6 | 17,4 | 17,7 | 17,2 | 15,8 | 15,0 | 14,6 |
| · exportació | 8,9 | 7,6 | 6,7 | 7,0 | 7,0 | 5,4 | 5,3 |
| · reciclatge directe | 3,0 | 2,8 | 2,6 | 2,7 | 2,7 | 2,8 | 2,7 |
| · escombraries | 3,1 | 2,3 | 1,7 | 1,4 | 1,0 | 1,1 | 1,0 |
| reciclatge total | 12,6 | 14,2 | 15,0 | 15,8 | 16,1 | 15,9 | 15,4 |
| durada implícita | 1,97 | 2,18 | 2,34 | 2,36 | 2,53 | 2,72 | 2,81 |

**Banda d'ancoratge** (palanques centrals): les sortides del 2013 van de 28,8 a 42,5 milions i les del 2019, de 21,5 a 29,2. Les formes són les mateixes que les del central, escalades per un factor de 0,8 a 1,2.

**Contrast amb Material Focus 2017.**
- **Massa per telèfon.** Les 2,512 kt de mòbils posats al mercat, dividides per les vendes centrals (28,8 milions), donen 0,087 kg per telèfon, en línia amb els 0,09 kg de la UNU.
- **Reciclatge.** Amb aquesta massa, els 1,035 kt reciclats són 11,9 milions de telèfons. El model central en dona 13,6 i el pessimista 9,4.
- **Coincidència no independent.** Les dues xifres s'assemblen, però no és una validació. Al model, la major part del reciclatge surt del calaix. Tant l'entrada com la sortida del calaix són unes 1,7–1,8 vegades les de Material Focus, i els dos errors es compensen.
- **Què es pot dir.** El reciclatge directe que declaren les enquestes (un 4–5 %) és petit. El reciclatge real només arriba a l'ordre de 10⁷ l'any si passa pel calaix.

**Sèrie de RAEE (contrast, no entrada).**
- **Proporció de mòbils en el recollit.** Els telèfons reciclats segons Material Focus 2017 són el 2,1 % de la massa de la categoria 3 recollida de llars aquell any (F §7).
- **Evolució.** Si la proporció fos constant, el reciclatge de mòbils hauria crescut un 59 % del 2013 al 2016 i baixat un 14 % fins al 2019. Coincideix amb la tendència de les tones.
- **Model central.** Creix un 24 % del 2013 al 2016 i es manté després.

## 8. Causes de les baixes per avaria

**Com es calculen.**
- **Base.** MobiFix, Regne Unit, tots els estats coneguts, finestra de tres anys centrada en cada any (F §8).
- **Anys extrems.** Les finestres del 2013 i el 2019 només cobreixen dos anys: 2013–2014 (n = 93) i 2018–2019 (n = 203).
- **Desconegut.** «Desconegut» es manté com a categoria i no es redistribueix: es concentra en els finals de vida i repartir-lo no seria neutre.

| % de les baixes per avaria | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| n de la finestra | 93 | 159 | 244 | 258 | 327 | 282 | 203 |
| Pantalla (interval del 90 %) | 29 (22–37) | 28 (22–34) | 27 (23–32) | 24 (20–28) | 30 (26–34) | 29 (25–34) | 33 (27–38) |
| Bateria i alimentació | 12 | 14 | 17 | 19 | 19 | 19 | 20 |
| Programari i configuració | 18 | 13 | 13 | 11 | 12 | 11 | 12 |
| Altres | 14 | 15 | 13 | 15 | 13 | 15 | 13 |
| Botons i connectors | 13 | 11 | 8 | 8 | 7 | 7 | 6 |
| Port de càrrega | 7 | 6 | 7 | 5 | 6 | 5 | 6 |
| Danys interns i aigua | 0 | 0 | 0,4 | 0,4 | 0,3 | 0,4 | 0,5 |
| Desconegut | 8 | 14 | 14 | 19 | 14 | 13 | 10 |

**Tendències.**
- **Bateria.** Puja del 12 % al 20 %. **Botons**: baixen del 13 % al 6 %. Encaixa amb la substitució dels telèfons de tecles per smartphones.
- **Pantalla.** Es mou dins de l'interval i no té tendència.

**Sensibilitat que s'ha de decidir.**
- **Diferència entre estats.** Entre els 87 registres de final de vida, la pantalla és només el 12,6 % (davant del 27–34 % entre els reparats o reparables) i «Desconegut» el 25 % (F §8).
- **Quina composició és més propera.** Les baixes per avaria s'assemblen més al final de vida que al conjunt de reparacions. Amb aquesta composició, l'àrea de pantalla del gràfic es reduiria a la meitat.
- **Què fa el central.** Fa servir tots els estats, que és el supòsit declarat. Amb 87 casos en set anys no es pot fer una finestra per any de final de vida.

## 9. Exportació de telèfons usats

Ara és una sortida del model (§4): de 3,9 a 6,8 milions l'any en el central, que és més que el «10⁶ per any» de la versió anterior.

**Contrast.**
- **Technavio.** 5,4 milions de telèfons revenuts o entregats el 2013 i uns 6,7 milions el 2014 (F §5.4). Amb el 57 % d'O2 que surt del país, serien uns 3 milions exportats el 2013.
- **Model central.** Dona 6,8 milions el 2013, el doble. La banda baixa en dona 5,5.
- **Per què el model en dona més.** No és pels telèfons d'empresa: la banda per persones, que no els compta, també en dona 5,5.
  - Una part és la inflació de les vies (§4). Sense ella, el central seria d'uns 5,4 milions.
  - La resta pot venir del 43 % d'O2: és un sol operador i un sol any.
  - Mantinc el factor 2 com a incertesa declarada d'aquesta via.
- **Què no hi ha.** No hi ha cap sèrie de dades de duanes que separi els telèfons usats.

## 10. Escala dels registres de MobiFix

**Mida de la mostra respecte de la població.**
- **MobiFix.** 554 registres en set anys, uns 80 l'any.
- **Població.** Uns 10⁷ baixes per avaria l'any en el central.
- **Fracció.** Uns 10⁻⁵.
- **Ús en el model.** No s'utilitza per escalar res: el model només n'agafa proporcions. Però mostra que no es poden treure xifres absolutes de la mostra, que a més és autoseleccionada.
