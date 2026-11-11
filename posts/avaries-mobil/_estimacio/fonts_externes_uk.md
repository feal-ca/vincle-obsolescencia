# Dades tancades per al model de població de mòbils (Regne Unit, 2013–2019)

Revisat el 2026-11-11, després d'una segona cerca per any. Aquest document només recull dades **tancades**. Els valors per any i escenari que en surten, i els que són ordre de magnitud, són a [`ordres_de_magnitud_uk.md`](ordres_de_magnitud_uk.md) i a `escenaris_uk.csv`.

**Què vol dir «tancada».** La xifra l'he llegida en una pàgina o document amb el seu any, l'àmbit i la definició que dona la font, o bé surt directament de les dades del repositori. La columna *Lectura* diu si s'ha llegit en origen, en un mitjà que cita la font, o si és un càlcul meu a partir d'una xifra tancada (*derivat*). Les còpies de l'Ofcom i de Deloitte s'han llegit a la Wayback Machine perquè el web original rebutja les descàrregues automàtiques.

**Quan mesura cada font.** L'Ofcom fa el camp el gener i el febrer (és el parc a començament d'any); Deloitte, el maig i el juny; les subscripcions de l'Ofcom són a final d'any; l'ONS, a mitjan any; les vendes, l'any natural. El model ho tracta tot com a «any t», que és una aproximació Fermi.

## 1. Població humana (ONS, mitjans d'any)

| Any | Habitants del Regne Unit | Publicació | Lectura |
|---|---|---|---|
| 2013 | 64.105.700 | ONS, 26 juny 2014 | origen |
| 2014 | 64.596.800 | ONS, 25 juny 2015 | origen |
| 2015 | 65.110.000 | ONS, 23 juny 2016 | origen |
| 2016 | 65.648.000 | ONS, 22 juny 2017 | origen |
| 2017 | 66.040.229 | ONS, 28 juny 2018 | origen |
| 2018 | 66.435.550 | ONS, 26 juny 2019 | origen |
| 2019 | 66.796.807, **provisional** | ONS, 6 maig 2020 | origen |

Fonts: [2013](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/2014-06-26) · [2014](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/2015-06-25) · [2015](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2015) · [2016](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2016) · [2017](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2017) · [2018](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2018) · [2019](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2019).

Reserva: l'ONS va publicar sèries retrospectives corregides (març de 2018 per a 2012–2016) que no he llegit. Diu que els totals de 2013 i 2014 no s'han revisat.

## 2. Parc: qui fa servir un mòbil

### 2.1 Penetració entre adults (Ofcom)

Ofcom, adults de 16 anys o més, pregunta «Do you personally use a smartphone?» i «Do you personally use a mobile phone?», base: totes les persones entrevistades.

| Any (camp gen.–febr.) | Smartphone | Qualsevol mòbil | Document | Lectura |
|---|---|---|---|---|
| 2012 | 39 % | – | CMR 2017, fig. 5.1 | origen |
| 2013 | 51 % | 92 % | CMR 2013, dades clau i fig. 4.4 | origen |
| 2014 | 61 % | 93 % | CMR 2014, dades clau | origen |
| 2015 | 66 % | 93 % | CMR 2015, dades clau | origen |
| 2016 | 71 % | 93 % | CMR 2016, dades clau i fig. 5.1 | origen |
| 2017 | 76 % | 94 % | Technology Tracker H1 2017, QD4 i QD2 (n = 3.743) | origen |
| 2018 | 78 % | 94 % | Technology Tracker H1 2018, QD4 i QD2 (n = 3.730) | origen |
| 2019 | 79 % | 94 % | Technology Tracker 2019, QD4 i QD2 (n = 3.909) | origen |

Documents (Wayback): [CMR 2013](https://stakeholders.ofcom.org.uk/binaries/research/cmr/cmr13/2013_UK_CMR.pdf) · [CMR 2014](https://stakeholders.ofcom.org.uk/binaries/research/cmr/cmr14/2014_UK_CMR.pdf) · [CMR 2015](https://stakeholders.ofcom.org.uk/binaries/research/cmr/cmr15/CMR_UK_2015.pdf) · [CMR 2016](https://www.ofcom.org.uk/__data/assets/pdf_file/0024/26826/cmr_uk_2016.pdf) · [CMR 2017, gràfics](https://www.ofcom.org.uk/__data/assets/pdf_file/0019/105418/cmr-2017-uk-charts.pdf) · [Tech Tracker H1 2017](https://www.ofcom.org.uk/__data/assets/pdf_file/0015/101292/technology-tracker-data-tables-h1-2017.pdf) · [Tech Tracker H1 2018](https://www.ofcom.org.uk/__data/assets/pdf_file/0021/113169/Technology-Tracker-H1-2018-data-tables.pdf) · [Tech Tracker 2019](https://www.ofcom.org.uk/__data/assets/pdf_file/0026/143981/technology-tracker-2019-uk-data-tables.pdf).

- **Correcció.** El 70 % del 2016 que havia vist en un resum de cercador és erroni: l'Ofcom diu 71 %.
- **Finder** (76, 78 i 79 % per al 2017–2019) repeteix l'Ofcom; no és una font independent.
- **Mòbils per usuari.** El 2019, el 88 % dels usuaris tenia un sol número i el 6 % en tenia dos (Technology Tracker 2019).

### 2.2 Altres mesures de penetració (no es barregen amb l'Ofcom)

| Any | Valor | Base | Font | Lectura |
|---|---|---|---|---|
| 2013–2018 | 62, 70, 76, 81, 85, 87 % | té o pot fer servir un smartphone, 18–75 anys, camp maig–juny | Deloitte, [*State of the smartphone market* 2018](https://www.deloitte.co.uk/mobileuk2018/themes/state-of-the-smartphone-market) (dades del gràfic) | origen |
| 2019 | 89 % | 16–75 anys, n = 4.150 | Deloitte, comunicat del 14 oct. 2019 | secundari |
| 2015 · 2016 | 73 % · 76 % | base no indicada | GfK, [Mobile News, 10 març 2016](https://mobilenewscwp.co.uk/features/article/gfk-uk-smartphone-market-is-bucking-the-trend/) | secundari |
| nov. 2017 | 83 % té smartphone; el 20 % encara té un mòbil bàsic | 2.000 usuaris d'internet de 16 anys o més | Mintel, [20 abril 2018](https://www.mintel.com/press-centre/smashing-times-24-of-uk-smartphone-owners-have-broken-their-screen-in-the-past-two-years) | origen |

Deloitte queda de 6 a 11 punts per sobre de l'Ofcom cada any: pregunta, edats i època del camp són diferents.

### 2.3 Subscripcions mòbils actives (Ofcom, milions, final d'any)

Compten SIM, no aparells. Les de terminal són la cota alta del parc.

| Any | Total amb M2M | M2M | Només dades | Sense M2M | **De terminal** | Lectura |
|---|---|---|---|---|---|---|
| 2013 | 88,8 | 5,7 | 4,9 | 83,1 | **78,2** | origen (CMR 2017, fig. 4.1, 4.23, 4.25) |
| 2014 | 90,3 | 6,3 | 5,2 | 84,0 | **78,9** | origen |
| 2015 | 91,9 | 6,7 | 5,5 | 85,2 | **79,7** | origen |
| 2016 | 92,0 | 7,6 | 5,0 | 84,4 | **79,4** | origen |
| 2017 | 92,0 | 7,9 | 5,0 | 84,1 | **79,1** | derivat (sense M2M − dades; CMR 2018, Telecoms Data Update T1 2019) |
| 2018 | – | – | 4,5 | 84,0 | **79,5** | derivat (Telecoms Data Update T1 i T4 2019) |
| 2019 | – | – | 4,5 | 85,5 | **81,0** | derivat ([Telecoms Data Update T4 2019](https://www.ofcom.org.uk/__data/assets/pdf_file/0039/196986/)) |

Les edicions anteriors donen valors una mica diferents (78,1 per al 2013 al CMR 2014). Alguns quadres del CMR 2015 i 2016 etiqueten «amb M2M» xifres que no l'inclouen.

## 3. Entrades: vendes de telèfons

| Període | Valor | Abast | Font | Lectura |
|---|---|---|---|---|
| 2013 · 2014 · 2015 · 2016 · 2017 | 30 · 31 · 32 · 28 · 27 milions | enviaments de smartphones | Canalys, al gràfic de Deloitte *State of the smartphone market* 2018 | origen (dades del gràfic) |
| 2015 | 23,7 milions (2,8 milions lliures de SIM) | smartphones venuts, panell de punt de venda | GfK, [Mobile News, 10 març 2016](https://mobilenewscwp.co.uk/features/article/gfk-uk-smartphone-market-is-bucking-the-trend/) | origen |
| 2016 · 2018 | 24 · 25 milions, **previsions** | smartphones | GfK, mateixa notícia | origen |
| 2015 | més de 32 milions de smartphones comprats i uns 6 milions passats a un altre usuari | estimació de Deloitte | Deloitte *Mobile Consumer 2015*, via legal500.com | secundari |
| 4T 2017 · 4T 2018 | 8,5 · 7,3 milions (−14 %) | smartphones, un sol trimestre | Strategy Analytics, [TelecomTV, 14 febr. 2019](https://www.telecomtv.com/content/devices/strategy-analytics-uk-smartphone-shipments-fell-14-percent-in-q4-2018-34041) | secundari |
| 1T 2018 | GfK −11 %; Canalys −29,6 % respecte del 1T 2017 | unitats de smartphone | Deloitte 2018 | origen |
| 2016 · 2017 | 36,6 · 37,6 milions; creixement anual 4 % (2012–16) i 3,4 % (2013–17) | «volum de consum» de tots els mòbils | MarketLine, fitxes públiques a ResearchPool ([2016](https://app.researchpool.com/provider/marketline/mobile-phones-in-the-united-kingdom), [2017](https://app.researchpool.com/provider/marketline/mobile-phones-in-the-united-kingdom-2)) | secundari (resum) |
| 3T 2010 → 1T 2013 | de 42 % a **74 %** | part de smartphones sobre les unitats de mòbil venudes | GfK, a l'Ofcom CMR 2013, fig. 4.4 | origen |
| 4T 2017 | 89 % | part de smartphones sobre els mòbils de contracte | GfK, a l'Ofcom CMR 2018, p. 52 | origen |

**Dues mesures que no coincideixen.** Per al 2015, Canalys dona 32 milions i GfK 23,7. Canalys compta enviaments al canal (inclou empresa i estoc); GfK, vendes en botiga a consumidors. MarketLine creix quan Canalys baixa. A `ordres_de_magnitud_uk.md` (§1–3) es mostra que la diferència és la mateixa que hi ha entre el parc per persones i el parc per SIM.

## 4. Renovació i durada de tinença

| Dada | Valor | Font | Lectura |
|---|---|---|---|
| Temps de primer ús d'un smartphone, **Gran Bretanya**, sèrie antiga de Kantar | 20,0 · 22,0 · 23,5 · 23,4 mesos (2013–2016). EU5: 18,3 · 19,5 · 20,4 · 21,6 | Kantar Worldpanel 2017, a [JRC (2020), fig. 21](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC116106/jrc116106_jrc_e4c_task2_smartphones_final_publ_id.pdf) | secundari (taula llegida) |
| Mateix indicador, **sèrie nova** de Kantar | EU5: 23,4 (2016) → 26,2 (2018); Gran Bretanya 2018: 27,7 mesos | Kantar, a [CNBC, 17 maig 2019](https://www.cnbc.com/2019/05/17/smartphone-users-are-waiting-longer-before-upgrading-heres-why.html) | secundari. **No s'ha d'enganxar a la sèrie antiga**: el mateix any, EU5 dona 21,6 i 23,4 |
| Cicle de renovació dels clients de Dixons Carphone | 29 mesos de mitjana, davant de 24 «abans» | Dixons Carphone, [Yahoo Finance UK, 24 agost 2017](https://uk.finance.yahoo.com/news/dixons-carphone-warns-profits-customers-064402807.html) | secundari |
| Smartphones adquirits els 18 mesos anteriors | 66 % (2016) · 62 % (2017) · 59 % (2018) | Deloitte, comunicat de setembre 2018, [cwconnected.com](https://www.cwconnected.com/resource/17-million-people-think-they-use-their-smartphones-news-article-2920.html); 18–75 anys | origen |
| Contracte només SIM | 19 % (2015) → 32 % (2018) | Deloitte, mateix comunicat | origen |
| Telèfons en ús de segona mà o renovats | 10 % (2015) · 11 % (2016) · 15 % (2018) · 15 % (2019) | Deloitte *Mobile Consumer* 2015 (fig. 8), 2016 (p. 30), 2018; *Digital Consumer Trends* 2022 (fig. 3) | origen |
| Telèfons renovats venuts | 2,2–2,4 milions el 2018, prop del 10 % del mercat | Counterpoint, [Mobile News, 13 març 2019](https://mobilenewscwp.co.uk/?p=160290) | secundari |
| Edat mitjana i cicle de renovació al Regne Unit (O2) | edat mitjana 1,8 anys; cicle d'uns 22 mesos; telèfons *SIM Only* d'O2, 2,55 anys (2012) → 2,93 (2015) | Green Alliance, [*The end of the upgrade?*](https://green-alliance.org.uk/wp-content/uploads/2021/11/The_end_of_the_upgrade.pdf) (2016) | origen |
| Cicle de renovació mitjà global, 2016 | 21 mesos | Counterpoint, al JRC (2020) | secundari |

## 5. Destí del telèfon anterior

### 5.1 Deloitte: «Què vas fer amb el teu telèfon anterior?» (resposta única)

| Opció | 2015 | 2017 | 2018 |
|---|---|---|---|
| El guarda de recanvi | 43 | 37 | 41 |
| El dona o el ven a un familiar o amic | 20 | 24 | 20 |
| El ven (en línia, a una botiga, a l'operadora o al fabricant) | 20 | 20 | 18 |
| El recicla gratis | – | 4 | 5 |
| El llença | 7 | 4 | 5 |
| Perdut o robat | 1 | 2 | 3 |
| Altres, no ho sap, no en tenia | 9 | 9 | 10 |

Base: propietaris de smartphone (3.039 el 2015; 3.525 el 2017; 3.637 el 2018). Fonts: [*Mobile Consumer 2015: The UK cut*, fig. 7](https://web.archive.org/web/20150927004024/http://www.deloitte.co.uk:80/mobileuk/assets/pdf/Deloitte-Mobile-Consumer-2015.pdf) i [gràfic 2017–2018](https://web.archive.org/web/20190911011718/http://www.deloitte.co.uk:80/mobileuk/charts/uk-outcome-for-previous-smartphone-subsequent-to-buying-or-receiving-current-one/). Lectura: origen. El «reciclat» del 2015 (20 %) de Deloitte és venda, no reciclatge de material.

### 5.2 Altres enquestes

| Any de camp | Valor | Base | Font | Lectura |
|---|---|---|---|---|
| 2013 | 33 % calaix, 27 % venda, 15 % regal, 16 % escombraries, 4 % reciclatge | propietaris del Regne Unit «quan el substitueixen»; sense mostra | BidGrid, a [PCR, 7 oct. 2013](https://pcr-online.biz/2013/10/07/16-per-cent-of-uk-consumers-throw-away-old-mobile-phones/) | secundari |
| 2017 | 39 % segona vida (18 % passat gratis, 21 % mercat); 32 % de recanvi; 45 % sense segona vida | propietaris de smartphone | Mintel, [26 maig 2017](https://www.mintel.com/press-centre/two-in-five-phones-have-a-second-life) | origen |
| nov. 2017 | 57 % guarda el vell de recanvi | 2.000 usuaris d'internet 16+ | Mintel, 20 abril 2018 | origen. **És del 2017**, com el 32 %: no és una sèrie 2017→2018 |
| 2019 | 23 % de les llars té un mòbil sense ús; el 82 % no pensa reciclar ni vendre | Ipsos MORI, 2.353 adults 16–75 | Royal Society of Chemistry, a [envirotec](https://envirotecmagazine.com/2019/08/28/uk-households-still-stockpiling-old-gadgets-says-royal-society-of-chemistry-survey/) | secundari |
| 2022 (**fora de la finestra**) | 38 % es queda el vell; uns 24 milions de recanvi en tres anys | Deloitte *Digital Consumer Trends* 2022 | Deloitte | origen. Abans l'havia datat malament: és del 2022 |
| 2024 (**fora de la finestra**) | guarda 52, regala 42, entrega en compra 24, ven 20, ven per reciclar 19, ONG 13, recicla d'una altra manera 10, llença 10; **resposta múltiple** | 3.119 propietaris | YouGov, [16 juliol 2024](https://yougov.com/en-gb/articles/50080-what-do-britons-do-with-their-old-phones-half-of-them-keep-it) | origen |

### 5.3 Telèfons sense ús a les llars

| Any | Valor | Font | Lectura |
|---|---|---|---|
| 2014 | «més de 90 milions» | Mobile News, 21 nov. 2014, sense font | secundari |
| 2015 | 28–125 milions, sense derivació | Green Alliance, [*A circular economy for smart devices*](https://green-alliance.org.uk/wp-content/uploads/2021/11/A-circular-economy-for-smart-devices.pdf), p. 5 | origen |
| 2015 | 85 milions | Deloitte 2015, nota 11, citant ThinkProgress | origen (com a cita) |
| 2017 | mediana de 3 telèfons guardats per llar (0–7) | Material Focus 2020, taula 1 | origen |
| 2021 | 35 milions, 22 d'ells smartphones | uSwitch, a londonlovesbusiness.com | secundari |

### 5.4 Recollida, revenda i exportació

| Dada | Valor | Font | Lectura |
|---|---|---|---|
| Dispositius rebuts per O2 Recycle | 285.552 (2012) · 356.856 (2013) · 420.008 (2014) · 417.669 (2015) | Green Alliance, *The end of the upgrade?*, p. 9 | origen |
| Estat dels rebuts per O2 Recycle, 2015 | 95–99 % funcionen i es revenen; la resta es recicla | mateix, p. 9 | origen |
| On van els revenuts per O2, 2015 | 43 % (173.000) es queden al Regne Unit, 30 % a la resta d'Europa | mateix, p. 10 | origen |
| Telèfons reciclats o entregats a canvi al Regne Unit | 5,4 milions (2013); previsions 6,7 (2014) i més de 16 (2018) | Technavio, a Mobile News, 21 nov. 2014 | secundari. És **revenda**, no reciclatge de material |
| Smartphones recollits per programes d'entrega als països rics, 2013 | 30 % es revenen en mercats rics i 70 % en emergents | Bernstein, a Green Alliance 2015, p. 11 | origen (com a cita) |

## 6. Avaria i motius de substitució

| Dada | Valor | Base | Font | Lectura |
|---|---|---|---|---|
| Motiu de substitució de l'últim **dispositiu digital** (mòbil, tauleta o portàtil), **fins a 3 respostes** | Regne Unit: «el vaig trencar» 41 %, rendiment empitjorat 25 %, programari 13 %, contracte 13 %, funcions noves 15 %, el més nou 5 %, aspecte 4 %, altres 3 % (sobre totes les persones; el 88 % havia substituït algun dispositiu) | n = 1.023, camp 6–19 des. 2019 | Eurobaròmetre especial 503, pregunta QC3, [taules a data.europa.eu](https://europa.eu/eurobarometer/surveys/detail/2228) | origen |
| Motius de substitució del telèfon anterior | «funcionament restringit» 31,4 % (respostes múltiples); només un terç eren defectes tècnics, **uns 10 % de tots els telèfons**; ús mitjà 2,7 anys | Àustria, n = 1.009, 2014–2015 | AK Wien, [Wieser i Tröger, *Working Paper 3*](https://www.arbeiterkammer.at/infopool/wien/Working_Paper_Nr.3_en.pdf) | origen |
| Propietaris de smartphone que han trencat la pantalla en dos anys | 24 % (48 % als 16–24 anys, 7 % als majors de 55) | 2.000 usuaris d'internet 16+, nov. 2017 | Mintel, 20 abril 2018 | origen |
| Pantalles trencades en un moment donat | 7,5 milions; la meitat ha trencat alguna vegada una pantalla | 1.729 adults, agost 2017 | O2, a [Mobile News](https://mobilenewscwp.co.uk/news/article/o2-cracked-screen-epidemic-exploded/) | origen |
| Incidents amb el smartphone en 12 mesos (**2020**) | 13 milions de persones; pantalla 36 %, cantonades 12 %, bateria 11 % | 1.012 adults | [SquareTrade, agost 2020](https://newsroom.squaretrade.com/press-release/13-million-brits-have-had-smartphone-damage-past-year/) | origen |
| Smartphones que funcionaven quan es van substituir (**2021–2025**) | 58 % (per tant, un 42 % no) | 1.104 membres del panell Which? | [Which?, 2026](https://www.which.co.uk/news/article/not-got-the-latest-phone-this-is-why-youre-an-inspiration-axNHy2J0IBA5) | origen; el 42 % és derivat |

## 7. Residus elèctrics (RAEE): categoria 3, equips informàtics i de telecomunicacions

Tones, any natural. Totes llegides en origen als fitxers ODS de l'Environment Agency (gov.uk; per al 2013–2017, les versions de juliol de 2019 a la Wayback Machine).

| Any | Recollit de llars | Recollit no domèstic | No obligat (AATF i exportadors) | Posat al mercat, llars | Posat al mercat, no domèstic |
|---|---|---|---|---|---|
| 2013 | 32.769 | 4.214 | 41.168 | 75.829 | 100.904 |
| 2014 | 35.988 | 3.055 | 38.595 | 78.542 | 96.780 |
| 2015 | 47.268 | 2.471 | 35.850 | 95.888 | 75.270 |
| 2016 | 52.008 | 1.153 | 30.694 | 87.877 | 75.519 |
| 2017 | 48.563 | 913 | 24.417 | 84.327 | 67.446 |
| 2018 | 45.013 | 918 | 23.144 | 82.369 | 71.224 |
| 2019 | 44.798 | 1.906 | 19.042 | 78.357 | 72.883 |

Fitxers: [recollit](https://assets.publishing.service.gov.uk/media/6a91511e9a177a1decf97b13/WEEE_Collected_in_the_UK.ods) · [posat al mercat](https://assets.publishing.service.gov.uk/media/6a915871df4246cf45e46661/Electrical_and_electronic_equipment_placed_on_the_UK_market.ods) · [no obligat](https://assets.publishing.service.gov.uk/media/6a9151aa9a177a1decf97b14/Non-obligated_WEEE_received_at_approved_authorised_treatment_facilities_and_approved_exporters.ods).

- El full AATF del 2016 porta la capçalera «2017»; les dades són del 2016. Per això faig servir el recollit de llars, no l'AATF.
- La categoria 3 no separa els mòbils.

**Mòbils (clau UNU 0306), 2017, modelitzat.** Material Focus, [*Electrical waste – challenges and opportunities*](https://eprints.lancs.ac.uk/145741/1/Material_Focus_Electrical_waste_challenges_and_opportunities.pdf) (2020), annex XIV, taules 6–8. Lectura: origen; són sortides d'un model, no mesures.

- **Posats al mercat:** 2,512 kt.
- **Descartats després de l'ús:** 2,472 kt.
- **Al calaix:** n'hi entren 0,871 kt i en surten 0,907 kt.
- **Destí dels descartats:**

  | Destí | kt |
  |---|---|
  | reciclatge | 1,035 |
  | donació o reutilització | 0,459 |
  | escombraries | 0,312 |
  | venda | 0,241 |
  | retorn al venedor | 0,149 |
  | altres | 0,131 |
  | desconegut | 0,182 |

- **Massa per unitat** de la clau 0306 a la UE: 0,09 kg el 2010–2016 (Forti, Baldé i Kuehr 2018, annex V; secundari).

## 8. Dades pròpies (Open Repair / MobiFix)

Totes surten de `posts/vida-material/_analisi/dades/raw/ora_mobifix.csv` i `posts/vida-material/_analisi/dades/processades/mobils_classificats.csv`, que són compartits amb l'entrada `vida-material` i no s'han mogut. Les calculo per a **Regne Unit, 2013–2019**, només amb estat de reparació conegut.

**Referència per a les causes: MobiFix cru (n = 554).** Té tots els registres, també els que no tenen descripció, i només etiquetes humanes. El fitxer processat (n = 624) perd els registres de MobiFix sense text (no es poden creuar) i hi afegeix prediccions del classificador, de manera que subestima «Desconegut».

| Causa (Regne Unit, 2013–2019, n = 554) | Registres | % | % entre els de final de vida (n = 87) |
|---|---|---|---|
| Pantalla | 154 | 27,8 | 12,6 |
| Bateria i alimentació | 100 | 18,1 | 17,2 |
| Altres | 78 | 14,1 | 21,8 |
| Desconegut | 75 | 13,5 | 25,3 |
| Programari i configuració | 70 | 12,6 | 11,5 |
| Botons i connectors | 44 | 7,9 | 9,2 |
| Port de càrrega | 31 | 5,6 | 1,1 |
| Danys interns i aigua | 2 | 0,4 | 1,1 |

| Registres per any (MobiFix, Regne Unit) | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 |
|---|---|---|---|---|---|---|---|
| n | 28 | 65 | 66 | 113 | 79 | 135 | 68 |
| % pantalla | 18 | 34 | 26 | 24 | 22 | 39 | 19 |

- **Estat**: reparat 220, reparable 247, final de vida 87 (15,7 %).
- **Proveïdor**: The Restart Project 538, Repair Café Internacional 16.
- **Edat a la reparació**: coneguda en 70 registres; mediana 3 anys, quartils 2 i 4. En el fitxer processat de 2013–2019 amb tots els països (n = 448): mediana 3, quartils 2 i 4.
- **Fitxer processat, Regne Unit 2013–2019 (n = 624)**: final de vida 18,6 %; edat coneguda en 75 registres (mediana 3, quartils 2 i 5), cap anterior al 2017. El motiu de final de vida consta només en 5 casos: no és utilitzable.

Reserves, de `posts/vida-material/index.qmd` §8: la mostra és de persones que van a un Repair Café; l'edat és la del dia de la reparació; els percentatges anuals tenen pocs casos (error estàndard d'un percentatge de 0,28: ±5 punts amb n≈80, ±9 amb n=28).

## 9. Què no queda tancat

- Vendes anuals totals (smartphones i bàsics) de cap any, amb font primària.
- Vendes de smartphones del 2018 i el 2019 per any sencer.
- Parc de telèfons en ús (aparells, no persones ni SIM).
- Durada de primer ús al Regne Unit per al 2017 i el 2019.
- Destí del telèfon anterior per al 2013 (amb un criteri comparable), el 2014, el 2016 i el 2019.
- Part de les substitucions per avaria entre el 2013 i el 2018.
- Telèfons reciclats per any.
- Exportacions de telèfons usats.
- Mòbils i telèfons per usuari dels menors.

Com es cobreixen és a [`ordres_de_magnitud_uk.md`](ordres_de_magnitud_uk.md).

**Xifres vistes només en resums de cercador, no usades:**
- Reportlinker: 34,8 milions el 2013.
- Kantar: penetració a la Gran Bretanya del 69–71 % (desembre 2013 – març 2014) i 85–88 % de smartphones entre els aparells venuts.
- Dixons Carphone: «uns 20 mesos el 2013» (The Guardian).
- Mazuma: «12 milions de telèfons reciclats l'any passat», sense data.
- musicMagpie 2018: «4 de cada 10» substitueixen el telèfon després de trencar la pantalla.
