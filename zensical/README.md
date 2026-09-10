# Zensical-koeputki

Kokeilu siitä, voisiko Ohj2-materiaalin siirtää mdBookista **Zensicaliin**
(Material for MkDocsin tekijöiden uusi generaattori). Ei koske `../src`:ään
eikä `../book.toml`:iin — `bash ../start.sh` toimii koko ajan entiseen tapaan.

## Käynnistys

```bash
./zensical/run.sh
```

Ensimmäisellä kerralla se asentaa itse tarvitsemansa (`python3-venv`, `pip`,
`zensical`) ja kysyy sudo-salasanaa apt:ta varten. Sen jälkeen sivusto on
osoitteessa <http://localhost:8001>. Portti 8001 on välitetty
devcontainerista; jos se ei aukea, avaa VS Coden **PORTS**-välilehti.

```bash
./zensical/run.sh 8003     # eri portti
./zensical/run.sh build    # pelkkä rakennus site/-hakemistoon
```

`zensical serve` seuraa muutoksia `docs/`:ssä. Kun muokkaat `../src`:ää,
aja `python3 convert.py` uudelleen. **Huom:** se ei huomaa muutoksia
`assets/`-tiedostoihin, joten CSS:ää muokatessa palvelin on käynnistettävä
uudelleen.

## Testit

```bash
./zensical/run.sh test                        # kaikki, 154 testiä
./zensical/run.sh test tests/test_convert.py  # pelkät muunnokset, 0,2 s
./zensical/run.sh test --nobuild              # käytä olemassa olevaa site/:ä
```

Ensimmäisellä kerralla asentuvat `pytest`, `playwright`, sen chromium ja
selaimen systeemikirjastot (`playwright install-deps`, vaatii sudon); sivuston
rakentamiseen riittää yhä pelkkä `zensical`.

Kolme neljästä on `.venv`:ssä, mutta **selain ja sen kirjastot ovat sen
ulkopuolella** — selain kotihakemistossa (`~/.cache/ms-playwright`) ja
kirjastot kontissa — joten paketit voivat olla paikallaan vaikka testit eivät
käynnisty. Niin kävi, kun koeputki kloonattiin ensimmäisen kerran puhtaaseen
devcontaineriin: `import playwright` toimi, mutta selain kaatui käynnistyessään
(`libcups.so.2` puuttui) eikä `run.sh` yrittänyt asentaa mitään, koska sen ehto
katsoi vain paketteja. Vanhassa kontissa sama testijoukko meni läpi, koska
kirjastot olivat kertyneet sinne ajan mittaan käsin — eikä se tieto ollut
missään tiedostossa. Nyt `run.sh` tarkistaa selaimen `ldd`:llä ja asentaa
puuttuvan itse.

Kerroksia on kolme, koska rikkoutumisia on kolmea lajia:

| Tiedosto                | Mitä                                                          | Kesto      |
| ----------------------- | ------------------------------------------------------------- | ---------- |
| `tests/test_convert.py` | `convert.py`:n muunnokset yksin: ei käännöstä eikä selainta   | 0,2 s      |
| `tests/test_print.py`   | tulostussivun kokoaminen selaimessa, koekirjalla              | 6 s        |
| `tests/test_playground.py` | ajonapit koekirjalla, suorituspalvelin korvattuna          | 16 s       |
| `tests/test_hidelines.py` | piilorivit ja silmänappi koekirjalla                       | 2 s        |
| `tests/test_highlights.py` | korostetut rivit koekirjalla                              | 2 s        |
| `tests/test_change.py`  | koekirjan materiaalia muutetaan: näkyykö muutos tulosteessa   | 25 s       |
| `tests/test_book.py`    | sama oikealla materiaalilla, 72 lukua                          | 10 s       |

Mitään ei jäljitellä: testit ajavat `convert.py`:n ja `zensical build`in
oikeasti ja avaavat sivun oikeassa selaimessa. Tulostussivu on koeputken
ainoa kohta, jossa lopputulos syntyy vasta selaimessa — `print.js` hakee
jokaisen luvun oman sivun ja liittää siitä artikkelin — joten käännöksen
tuloksesta sitä ei voi lukea.

**Koekirja (`tests/book/src`) on neljätoista tiedostoa.** Se on olemassa kahdesta
syystä. Ensinnäkin materiaalin muuttamista pitää päästä *kokeilemaan*, eikä
sitä voi tehdä `../src`:ään; koekirjasta jokainen testi saa oman kopionsa,
jota se saa rikkoa. Toiseksi se on nopea: koko kirjan kääntäminen kestää
50 s, koekirjan 3 s. Siinä on yksi esimerkki jokaisesta asiasta, joka
kokoamisessa voi mennä rikki — sama otsikko kahdessa luvussa, kuva
alihakemistosta, sivun sisäinen ankkuri, lukujen välinen linkki, neljä
välilehtijoukkoa, `NEST_UNDER`-siirto, ulkoinen linkki, huomiolaatikot ja
sisällytykset kaikissa kolmessa muodossaan (koko tiedosto, yksi rivi
taulukon soluun ja koodiaidan sisällä `// FILE:` -merkinnän jäljessä).
Sisällytysten kohteet (`osa2/ohje.md` ja `osa2/Esimerkki.java`) eivät ole
`SUMMARY.md`:ssä, kuten eivät tehtävänannot oikeassa materiaalissakaan.

**`window.print` korvataan laskurilla.** Headless-selaimessa ei ole
tulostusikkunaa, mutta kutsu on samalla juuri se mitä halutaan mitata.
Talteen otetaan tilarivin teksti kutsun hetkellä, jolloin testi näkee myös
sen, ettei tulostusta pyydetä kesken kokoamisen: `"Koottu 72 lukua."`

**Käännös ohitetaan, jos site/ on ajan tasalla.** `convert.py` kopioi
`../src`:n kokonaan (116 MB, 32 s) ja `zensical build` kestää 16 s, joten
50 s menisi joka ajolla hukkaan, jos mikään ei ole muuttunut. Ajantasaisuus
kysytään tiedostoilta eikä käyttäjältä: jos `../src`, `assets/`,
`overrides/`, `convert.py` tai `mkdocs.yml` on `site/`:ä uudempi, käännetään.
Testien ajaminen kirjoittaa siis `docs/`:n ja `site/`:n uusiksi, kuten
`run.sh`kin.

Yksi tunnettu poikkeus on kirjattu testiin: tulostussivulla on **yksi kuollut
ankkuri** (`#comparable-rajapinta-ja-luonnollinen-järjestys`), koska Zensical
riisuu otsikoiden tunnisteista ääkköset mutta sivun oma linkki ei tiedä siitä.
Se on tarkistuslistan kohta 13 eikä tulostuksen vika, ja se on ainoa
käännöksen 16 varoituksesta joka on myös sivun sisäinen linkki. Testi sallii
tasan tämän yhden ja kaatuu, jos niitä tulee lisää.

Toinen tunnettu poikkeus on **yksi puuttuva kuva**
(`osa4/images/adventure.png`): `exercises/4-3-seikkailupeli/handout.md`
viittaa `images/adventure.png`:hen, mutta kuva on `osa3/images/`:ssä ja
tehtävänanto sisällytetään osa4:n kahdelle sivulle. Sama on mdBookin omassa
käännöksessä, eli aineiston virhe eikä sisällytyksen. Testi sallii tasan tämän
yhden kuvan ja sen 404:n konsolissa.

## Periaate

Lähtötilanne on **Zensicalin oletusteema sellaisenaan**. Ei omaa CSS:ää, ei
omaa JavaScriptiä, ei template-ylikirjoituksia, ei Markdown-laajennuksia,
ei sisältömuunnoksia.

`convert.py` teki alun perin tasan kaksi asiaa: kopioi `../src` → `docs/` ja
käänsi `SUMMARY.md`:n navigaatioksi. Kaikki mdBookin oma syntaksi jäi siis
sivuille raakana näkyviin — se on tarkoitus. Näin listasta ei tule arvauksia
vaan havaintoja. Sisältöä muunnetaan toistaiseksi yhdessätoista kohdassa
(sisällytykset, piilorivit, korostukset, välilehdet, alertit, avattavat osiot,
tehtäväkortit, vaatimuslohkot ja kaaviot, ks. kohdat 1, 2, 4, 5, 6, 7, 8, 9, 15,
23 ja 25);
jokainen uusi muunnos kuuluu perustella samalla tavalla kuin muutkin rivit.

Aiempi, täysin viritetty versio on tallessa branchissa `spike/mkdocs`
(siellä hakemisto on nimeltään `mkdocs-spike/`):
sieltä saa jokaisen palasen takaisin, kun se on ensin todettu tarpeelliseksi.

## Tarkistuslista

Käydään läpi yksi kerrallaan. Jokaiselle kolme kysymystä: mitä mdBook teki,
näyttääkö Zensical sen jo itse, ja tarvitaanko sitä oikeasti.

| #  | mdBookin ominaisuus                          | Esiintymiä                | Tila nyt                                                                                                           |
| -- | -------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1  | `{{#include tiedosto}}`                      | 194                       | **tehty** — `convert_includes`; 4 makroa jää näkyviin, kohde puuttuu aineistosta                                   |
| 2  | `//-` piilorivit                             | 1103                      | **tehty** — `hide_lines` + `assets/js/hidelines.js`; rivit piiloon ja silmänappi, ajoon ne menevät yhä               |
| 3  | ` ```java ` ajonappi (playground)            | 231                       | **tehty** — `assets/js/playground.js`; sama palvelin ja sama pyyntö kuin mdBookissa, monitiedostolohkot mukaan lukien |
| 4  | ` ```java,ignore` / `,noplayground`          | 289                       | **tehty** — attribuutit luokiksi (`{ .java .ignore }`), korostus palasi                                            |
| 5  | `// FILE:` monitiedostolohkot                | 73 lohkoa / 194 tiedostoa | **tehty** — `pymdownx.tabbed`, tiedosto per välilehti                                                              |
| 6  | `<task>` / `<points>` / `<handout>`          | 507                       | **tehty** — `convert_tasks` + `assets/css/tasks.css`; riippuva numerointi laatikon sijaan                          |
| 7  | `> [!VINKKI]`-tyyliset alertit               | 75                        | **tehty** — `convert_alerts`; `admonition` on jo Zensicalin oletuslistalla, `mkdocs.yml` ennallaan                 |
| 8  | `<details>`-lohkot                           | 88 + 6 `<summary>`        | **tehty** — `convert_details`; `markdown="1"` avaustagiin ja `markdown="block"` monirivisiin yhteenvetoihin       |
| 9  | `HIGHLIGHT_*_BEGIN/END`                      | 120                       | **tehty** — `mark_highlights` + `assets/js/highlights.js`; värit kirkkautta muuttamatta, ks. kohta 9              |
| 10 | Lukujen numerointi navigaatiossa             | koko nav                  | **tehty** — `convert.py`, 12 riviä                                                                                 |
| 11 | Osan etusivu = osan oma linkki navissa       | 13 osaa                   | **tehty** — `navigation.indexes`                                                                                   |
| 12 | Otsikoiden numerointi sivun sisällä          | —                         | ei ollut mdBookissakaan                                                                                            |
| 13 | Ääkköset ankkureissa (`#käyttö`)             | —                         | riisutaan (`#kaytto`)                                                                                              |
| 14 | `.html`-päätteiset osoitteet (TIM)           | —                         | puuttuu — nyt hakemistopolut                                                                                       |
| 15 | plantuml / bob / mermaid                     | 17 / 11 / 2               | **tehty** — `convert_plantuml` (kuviksi), `convert_svgbob` (upotetuksi SVG:ksi); mermaid toimi jo itsestään        |
| 16 | `<asciinema>`-upotukset                      | 13                        | rikki                                                                                                              |
| 17 | Bootstrap-ikonit `<i class="bi ...">`        | 136                       | puuttuu — ei fonttia; tehtävien 36 bonustähteä piirtää CSS, ks. kohta 6                                            |
| 18 | JYU-paletti, kultainen korostus              | 30                        | puuttuu                                                                                                            |
| 19 | Lisenssi + "Ehdota muutosta" alatunnisteessa | —                         | **tehty** — tekijät, lisenssi ja muokkauslinkki; "Ilmoita ongelmasta" puuttuu                                      |
| 20 | ACE-editori (`editable`-lohkot)              | 2                         | puuttuu — `.editable` säilyy nyt luokkana; ajonappi ajaa lohkon sellaisenaan, ks. kohdat 3 ja 4                     |
| 21 | KaTeX                                        | 0                         | voi jättää pois                                                                                                    |
| 22 | Edellinen/seuraava sivun alareunassa         | joka sivu                 | **tehty** — `navigation.footer`                                                                                    |
| 23 | `### [Windows](#tab/win)`-välilehdet         | 33 lohkoa / 9 joukkoa     | **tehty** — `pymdownx.tabbed` + `content.tabs.link`                                                                |
| 24 | Tulostuspainike: koko kirja yhdeksi PDF:ksi  | joka sivu                 | **tehty** — `assets/js/print.js`, `print.css`, runko `convert.py`:stä, yläpalkin malli                             |
| 25 | `<div class="ht-reqs">` vaatimuslohkot       | 9                         | **tehty** — `convert_divs` + `assets/css/requirements.css`; numerointi 1.1, 1.2, ... CSS-laskurista               |

Zensical antaa itse ilman mitään lisäystä: oikean reunan sisällysluettelon,
haun ja responsiivisen navigaation. Edellinen/seuraava -linkit ja alatunnisteen
se osaa myös, mutta ne ovat oletuksena pois päältä; ks. kohdat 19 ja 22. Samaan
joukkoon kuuluu **kopioi koodi -nappi**, joka mdBookissa on jokaisessa
koodilohkossa: teemalla on siihen valmis ominaisuus (`content.code.copy`), mutta
se on oletuksena pois päältä eikä sitä ole otettu käyttöön, joten sivustolla ei
tällä hetkellä ole kopiointinappia lainkaan. Yksi rivi `mkdocs.yml`:ään riittää,
jos se halutaan.

## Tehdyt kohdat

### Teemanvaihto (14 riviä `mkdocs.yml`:ään)

`book.toml`:ssa on `default-theme = "jyu-light"` ja
`preferred-dark-theme = "jyu-dark"` — kaksi teemaa, ei viittä. Sama tehdään
Materialin `palette`-lohkolla `media`-ehdolla, jolloin teema seuraa
käyttöjärjestelmää ja vaihdin ohittaa sen. Todennettu selaimella: kun
järjestelmä on vaalea, sivu avautuu `default`-teemalla ja vaihdin vie
`slate`en; kun järjestelmä on tumma, päinvastoin.

Havainto samalla: Materialin oletusväreillä koodilohkon ja sivun taustan
kontrasti on **1,09:1 molemmissa teemoissa** (vaalea 255,255,255 vs
245,245,245; tumma 11,12,15 vs 20,23,31). Sama ongelma josta aiemmin
huomautit — se on siis Materialin oletus, ei koeputken tekemä. Kuuluu
kohtaan 18.

### Osan etusivu navigaatiossa (1 rivi + 1 rivi)

Barebones-konversio toisti osan otsikon vielä ensimmäisenä lapsena
("Perintä, polymorfismi" kahdesti). mdBookissa osan otsikko *on* linkki
`index.md`:hen ja nuoli avaa alikohdat erikseen. Sama saadaan
`navigation.indexes`-ominaisuudella, kun `convert.py` kirjoittaa osan
etusivun paljaana polkuna listan ensimmäiseksi.

Todennettu selaimella: otsikko linkittää `osa3/`:een, nuoli avaa neljä
alikohtaa, aktiivinen sivu saa pillerikorostuksen.

### Lukujen numerointi (12 riviä `convert.py`:hyn)

mdBook numeroi vain `SUMMARY.md`:n listakohdat (`- [Luku](...)`), juoksevasti
myös `---`-erottimien yli. Etu- ja jälkilinkit (Aloitus, Työkalut, Luennot)
jäävät numeroimatta, jolloin ne erottuvat osista ilman erillisiä erottimia —
tämä korvaa `---`-viivat, joille Materialissa ei ole vastinetta.

Todennettu vertaamalla generoitu `nav.yml` mdBookin omaan `book/toc.html`:ään
ohjelmallisesti: **72 riviä, ei yhtään eroa** otsikoissa, numeroinnin
juoksutuksessa eikä poluissa.

Kaksi tietoista eroa mdBookiin:

- Numeron perässä ei ole pistettä (`1 Java-kielen perusteet`, `1.1 Hei, Java!`),
  kun mdBookissa on (`1.`, `1.1.`).
- mdBookissa numero on omassa `<strong>`-elementissään ja himmennetty; tässä se
  on osa linkkitekstiä. Vaatisi oman CSS/JS-palan, joten jätetty pois.

### Työpöytäasettelu: valikko kiinteänä kiskona (`assets/css/layout.css`)

**Tämä on branchin ensimmäinen oma CSS.** Zensicalin oletuksessa valikko on
osa keskitettyä ruudukkoa ja `position: sticky`, jolloin kaksi asiaa häiritsi:

1. Valikko liikkui sisällön mukana ensimmäiset 30 px vieritystä ja pysähtyi
   sitten nytkähtäen, koska yhteinen säiliö on
   `.md-main__inner { display: flex; height: 100%; margin-top: 1.5rem }`.
   Sama on Zensicalin omalla sivustolla, jossa matka on 127 px.
2. Yläpalkki on läpikuultava ja sumennettu, joten sisältö liukui sen alle
   mutta valikko katkesi siihen terävästi (`top: 48px`).

Ratkaisu on sama kuin mdBookissa: **valikko ei ole yläpalkin alla lainkaan**
vaan omana kiskonaan ruudun vasemmassa reunassa, koko korkeudeltaan ja
kiinteänä, ja kurssin nimi on kiskon yläosassa. Silloin ei ole mitään mikä
liikkuisi tai katkeaisi — ja Zensicalin sumennettu yläpalkki voi jäädä, koska
se sumentaa vain kiskon oikealla puolella olevan sisällön.

Kiskon leveys on vähintään 15rem (300 px, sama kuin mdBookissa; Zensicalin
oletus on 12,1rem) ja enintään 16rem: `clamp(15rem, 100vw - 62rem, 16rem)`.
Sisältöruudukon maksimi on 61rem, joten sitä leveämmällä näytöllä ruudun
ylimääräinen tila on pelkkää tyhjää kourua sisällön molemmin puolin — kisko voi
ottaa siitä osansa ilman että tekstipalstasta lähtee pikseliäkään. Vain
työpöydällä (`min-width: 76.25em`); kapeilla näytöillä Zensicalin oma
laatikkovalikko jää koskematta.

Kolme asiaa jotka kaivautuivat esiin matkalla:

* Zensicalin JavaScript kirjoittaa sivupalkille inline-tyylit (`top: 48px`,
  vieritysalueen `height`) olettaen sen olevan yläpalkin alla. Kiskona ne
  ovat väärin, joten ne on kumottava `!important`illa. **Jos Zensical muuttaa
  kirjoittamiaan tyylejä, tämä on ensimmäinen paikka jota katsoa.**
* Yläpalkissa on repo-linkin paikka, joka varaa 11,5rem oikeasta reunasta.
  Kapeassa palkissa se ei haitannut; reunasta reunaan ulottuvassa se jätti
  haun roikkumaan keskelle. Paikka on tyhjä, koska linkki on tyhjennetty
  mallista (ks. *Repo-linkki pois* alempana), ja se piilotetaan
  `:not(:has(*))`-ehdolla eikä suoralla `display: none`llä, jotta sääntö
  purkautuu itsestään jos ylikirjoitus poistetaan.
* Zensical vaihtaa yläpalkin otsikon kurssin nimestä sivun otsikoksi
  vieritettäessä. Kiskon päällä se olisi hämmentävää, joten nimi jätetään
  paikalleen.

Mitattu leveyksillä 1280, 1440 ja 1920: kisko on `0/0/300/900` (1920:llä
330 px, koska teeman juurikoko kasvaa), vieritysalue on vakiokorkuinen
kaikilla vieritysarvoilla, ja mobiilissa (390 px) valikko on yhä
laatikkona ruudun ulkopuolella `-242`:ssa.

Listan päihin lisätty ilma (`.md-nav__list`, 8 px ylös ja 20 px alas): ilman
sitä ensimmäinen kohta oli 2 px kurssin nimen alapuolella ja viimeinen 2 px
ruudun alareunasta, koska kisko täyttää koko korkeuden eikä sillä ole
Zensicalin oletusasettelun marginaaleja. Padding on listalla eikä
vieritysalueella, jotta se kasvattaa vieritettävää korkeutta. Mitattu 1440 ×
900: ensimmäisen kohdan yläreuna 50 px → 58 px, viimeisen alareuna pohjaan
asti vieritettynä 898 px → 878 px (myös pitkällä, 1246 px:n listalla).

Avatun luvun alalukujen vasemmalla puolella kulkee yhdistävä viiva
(`border-left` sisäkkäisellä `.md-nav__list`illa). Pelkkä 0,6rem sisennys ei
kertonut, mihin lukuun alaluvut kuuluvat: ne näyttivät yhtä itsenäisiltä
kohdilta kuin numeroimattomat linkit listan yläosassa. Viiva on listalla eikä
yksittäisillä kohdilla, jolloin se jatkuu yhtenäisenä kohtien välisten rakojen
yli.

Viivan paikka on `margin-left: 1rem` = yläluvun linkin marginaali 0,2rem +
täyte 0,8rem, eli tasan yläluvun tekstin alku. Se ei siis ala mistään välistä
vaan tekstin kohdalta, ja koska molemmat ovat rem-yksiköitä, kohdistus pitää
myös 1920:llä, jossa teeman juurikoko kasvaa. Materialin oletus on 0,6rem,
joten alaluvut siirtyvät 8 px oikealle; hinta on yksi rivinvaihto lisää koko
navigaatiossa (8 → 9, kun kaikki 81 linkkiä on avattu).

Väri on `--md-default-fg-color--lighter` eikä `--lightest`, jota kiskon oma
reunaviiva käyttää: lightest on tummassa teemassa 0,12 ja vaaleassa 0,07,
mikä katosi käytännössä näkyvistä.

Mitattu: 1440 ja 1280 viiva x = 20 = yläluvun tekstin alku, alaluvun pilleri
25:stä ja teksti 41:stä; 1920:llä 22,0 vs. 21,99. Leveyksillä 900 ja 390
sääntö ei ole voimassa (`border-left: 0px`), joten laatikkovalikko pysyy
ennallaan.

Valikko täyttää kiskon leveyden (`.md-sidebar__inner`, `padding-right: 0.6rem`).
Zensical pitää sivupalkin sisällön 11,5rem levyisenä riippumatta sivupalkin
leveydestä (`[dir=ltr] .md-sidebar__inner { padding-right: calc(100% - 11.5rem) }`).
Sen omalla 12,1rem sivupalkilla se on 0,6rem kouru vierityspalkille, mutta
15rem kiskossa 3,5rem eli 70 px tyhjää valikon ja vierityspalkin väliin: koko
kiskon leventäminen meni kouruun eikä otsikoihin. Mitattu 1440 × 900 kaikki
osat avattuina: tyhjä 70 px → 13 px ja kahdelle riville taittuvia
valikkokohtia 30 → 19 (98:sta). Leveydestä 1700 px ylöspäin kisko kasvaa
16rem:iin ja taittuvia on 14; tekstipalsta ei kapene millään leveydellä
(675/835/1023/1116 px leveyksillä 1280/1440/1920/2560, sama sekä ennen että
jälkeen). 17rem ei enää vähentäisi taittuvia yhtään (14), joten siihen yläraja.

Kisko ei kärsi kohdan 1 nytkähdyksestä, koska se on `position: fixed`, mutta
oikean reunan sisällysluettelo on yhä `position: sticky` — ja se nytkähti
edelleen. Väljyys siirretään siksi yhteiseltä säiliöltä pelkälle sisällölle:

```css
.md-main__inner { margin-top: 0; }      /* pois yhteiseltä säiliöltä */
.md-content     { margin-top: 1.5rem; } /* sama arvo, vain sisällölle */
```

Ei negatiivista marginaalia sivupalkeille: se toistaisi 30 px:n taikanumerona,
ja jos Zensical joskus muuttaa `1.5rem`:ää, nytkähdys palaisi hiljaisesti.
Säännöt ovat media-kyselyn ulkopuolella, koska niitä tarvitaan myös
tableteilla (60–76,25em), joilla sisällysluettelo on vielä sticky.

Mitattu selaimella leveyksillä 1920, 1440, 1100, 900, 768, 390 ja 320:

* Sisällysluettelon `top` on **48 px kaikilla vieritysarvoilla** (0/15/30/60/200).
  Vanhalla säännöllä sama sarja oli 78 → 63 → 48 → 48 → 48, eli juuri se 30 px:n
  nytkähdys. 1920:llä vastaava vakioarvo on 53 px, koska teeman juurikoko kasvaa.
* Sisällön paikka säilyy pikselilleen: `h1` on 100 px riippumatta siitä, onko
  `layout.css` päällä vai pois (1920:llä 110 px). Ainoa muutos on se, kummassa
  elementissä 30 px:n marginaali istuu.
* Mobiilissa asettelu on **tasan ennallaan**: siellä molemmat sivupalkit ovat
  `position: fixed` (laatikko `-242` → `8` avattaessa, sisällysluettelo
  kelluvana nappina), joten säiliön marginaali ei koskenut niihin muutenkaan.
  Ei vaakavieritystä millään mitatulla leveydellä.

### Valikon vieritys lukua avattaessa (`assets/js/nav-scroll.js`)

**Tämä on branchin ensimmäinen oma JavaScript.** Alalukujen avaaminen on
Zensicalissa pelkkää CSS:ää: nuoli on `<label>`, joka rastittaa piilotetun
valintaruudun, ja rastitettu ruutu näyttää sisarenaan olevan alaluettelon.
Mikään ei siis vieritä kiskoa. Listan alapäässä se tarkoitti, että alaluvut
avautuivat kokonaan näkyvän alueen alapuolelle: nuoli kääntyi, mutta ruudulla
ei tapahtunut mitään.

Mitattu 1440 × 900: kun viimeinen luku ("13 JavaFX-ohjeita") avattiin lista
pohjaan asti vieritettynä, sen kuusi alalukua asettuivat 882–1114 px:ään eli
kokonaan kiskon alareunan (900 px) alapuolelle. Vieritysasema jäi paikalleen
(27), vaikka vieritysvara kasvoi 27 → 267.

Zensical vierittää kyllä itse aktiivisen kohdan näkyviin, mutta vain **sivun
latautuessa** (sidebar-komponentti keskittää `.md-nav__link--active`
vieritysalueeseen — siksi linkin klikkaaminen toimii jo nyt oikein).
Avaamiseen se ei reagoi mitenkään: nuolen `<label>`-käsittelijä päivittää vain
`aria-expanded`in. CSS:llä tätä ei voi tehdä, koska vieritys on tapahtuma eikä
tyyli.

Sääntö on: vieritä sen verran, että avatun luvun alalaita tulee näkyviin —
mutta enintään sen verran, että luvun oma rivi jää kiskon yläreunaan.
Alalukuja voi olla enemmän kuin kiskoon mahtuu, ja silloin on tärkeämpää
nähdä mikä luku avattiin kuin nähdä kaikki sen alaluvut. Alalaidan alle
jätetään sama ilma kuin listan alareunaan, jottei viimeinen alaluku jää kiinni
ruudun reunaan; arvo luetaan listan omasta `padding-bottom`ista eikä toisteta
lukuna.

Yksi ansa matkalla: **selain rajaa vierityksen siihen vieritysvaraan, joka on
olemassa käskyn hetkellä**, ja aukeaminen on animoitu
(`grid-template-rows: 0fr → 1fr`, 0,25 s). Heti muutostapahtumassa annettu
`scrollBy` jäi siis kokonaan tekemättä — vieritysasema pysyi 27:ssä koko
sekunnin ajan, vaikka vara kasvoi 267:ään. Vieritys tehdään siksi vasta
alaluettelon `transitionend`istä (nimenomaan `grid-template-rows`: samalla
elementillä on myös 0 s `visibility`-siirtymä, joka päättyisi heti).

Poikkeus tehdään lukemalla teemasta eikä käyttäjän asetuksesta: kun käyttäjä
on pyytänyt vähemmän liikettä, Material katkaisee kaikki siirtymät
(`* { transition: none }`), jolloin `transitionend`iä ei tule lainkaan. Jos
siirtymän kesto on 0 s, luku on jo auki ja myös vieritys tehdään kerralla.

Mitattu 1440 × 900 (vieritysasema ennen → jälkeen):

| Tilanne                            | Ennen                           | Nyt                             |
| ---------------------------------- | ------------------------------- | ------------------------------- |
| Viimeinen luku, lista pohjassa     | 27 → 27, 0/6 alalukua näkyvissä | 27 → 265, **6/6**               |
| Viimeinen luku, lista yläasennossa | 0 → 0, 0/6                      | 0 → 265, **6/6**                |
| Luku 8, alalaita jäi rajan alle    | 0 → 0, 5/7                      | 0 → 120, **7/7**                |
| Luku 1, mahtuu jo kokonaan         | 0 → 0, 5/5                      | 0 → 0, 5/5 (ei vieritä turhaan) |
| Luvun sulkeminen                   | 0 → 0                           | 0 → 0 (ei vieritä)              |

Reunatapaukset: 1440 × 300, jossa avattu luku on kiskoa korkeampi, vierittää
luvun oman rivin tasan kiskon yläreunaan (48 px = kiskon yläreuna) ja näyttää
kuudesta alaluvusta viisi; loput saa esiin vierittämällä. Mobiilissa
(390 × 844) sama toimii laatikkovalikossa: 164 → 414, 6/6. Vähennetyllä
liikkeellä vieritys on valmis 50 ms:ssä klikkauksesta. Nopea auki–kiinni–auki
päätyy oikeaan lopputilaan, eikä konsoliin tule virheitä.

Kytkentä on kaksi riviä `mkdocs.yml`:ään (`extra_javascript`); `convert.py`
kopioi `assets/`-hakemiston jo valmiiksi `docs/`:iin, joten uutta ei tarvittu.

### Tenttiohjeet Tentti-sivun alasivuksi (43 riviä `convert.py`:hyn)

Tämä on ensimmäinen kohta, jossa Zensical osaa enemmän kuin mdBook.
`SUMMARY.md`:n etulinkit (prefix chapters) ovat mdBookissa aina samalla
tasolla: kokeiltu mdBook 0.4.52:lla, sisennetty `[Tenttiohjeet](...)` päätyy
silti omaksi juuritason kohdakseen — ja jättää `toc.js`:ään vielä yhden
tyhjän `<li>`:n. Alasivuksi se kelpaisi vasta numeroituna lukuna, jolloin se
saisi järjestysnumeron osien 1–13 joukosta.

Zensicalissa se vaatii kaksi asiaa. `nav`-lohkon sisäkkäisyys on helppo osa:
`NEST_UNDER`-taulukko siirtää alasivun vanhempansa perään ja tason
syvemmälle. Pelkkä sisäkkäisyys ei kuitenkaan riitä, vaan otsikosta tulee
silloin pelkkä nuoli ja yläsivu toistuu ensimmäisenä lapsena — sama vika joka
osilla korjattiin `navigation.indexes`-ominaisuudella. Se nimittäin tunnistaa
osion etusivun **vain tiedostonimestä**: `zensical/config.py`:n `_is_index`
hyväksyy `index.md`:n ja `README.md`:n, ei mitään muuta.

Yläsivun on siis oltava oman hakemistonsa `index.md`. Siksi `convert.py`
siirtää kopioinnin yhteydessä molemmat sivut samaan hakemistoon:

```
docs/tentti.md        -> docs/tentti/index.md
docs/tenttiohjeet.md  -> docs/tentti/tenttiohjeet.md
```

Molemmat, koska sivut jäävät silloin toistensa viereen ja `tentti.md`:n kaksi
linkkiä (`./tenttiohjeet.md#jy-tenttiohjeet`, `#ohj2-tenttiohjeet`) osoittavat
yhä oikein. Sisältöä ei siis tarvitse muuntaa — pelkän yläsivun siirtäminen
vaatisi linkkien uudelleenkirjoitusta, mikä olisi vastoin koeputken
periaatetta.

Yläsivun osoite `/tentti/` säilyy ennallaan (hakemisto-osoitteilla `tentti.md`
kääntyi jo valmiiksi muotoon `site/tentti/index.html`). Alasivun osoite sen
sijaan muuttuu: `/tenttiohjeet/` -> `/tentti/tenttiohjeet/` (mdBookissa
`/tenttiohjeet.html`). Se on hierarkian hinta; jos osoite halutaan pitää,
sisäkkäisyydestä on luovuttava.

Todennettu käännetystä sivustosta: valikossa otsikko on linkki
(`<a href="../tentti/">Tentti</a>`) ja sen vieressä erillinen nuoli, jonka
alla on yksi kohta `../tentti/tenttiohjeet/`. Sivun sisäiset linkit kääntyvät
muotoon `./tenttiohjeet/#jy-tenttiohjeet` ja molemmat ankkurit löytyvät.
Varoitusten määrä on ennallaan 53, eli yhtään linkkiä ei katkennut. Lukujen
numerointi on koskematon, koska numeron saavat vain listakohdat.

### Alatunniste: edellinen/seuraava, tekijät ja lisenssi

Sivun alareunassa oli mdBookissa kaksi asiaa, ja kumpikaan ei tullut
Zensicalilta itsestään:

1. `<nav class="chapter-navigation">` — Edellinen/Seuraava luvun otsikoineen.
2. `<footer>` — CC-lisenssimerkki sekä linkit "Ehdota muutosta" ja
   "Ilmoita ongelmasta".

Ensimmäinen on Zensicalissa valmiina, mutta oletuksena pois päältä: yksi rivi
`navigation.footer` teeman `features`-listaan. Suomennokset ("Edellinen",
"Seuraava") tulevat kielipaketista, joka on jo käytössä. Todennettu selaimella
sekä vaaleassa että tummassa teemassa, ja ensimmäisellä sivulla on vain
Seuraava, viimeisellä vain Edellinen.

Toiseen ei ole omaa asetusta, mutta `copyright` menee malliin sellaisenaan
ilman escapetusta, joten siihen mahtuu myös linkki. Tekstin lähde on repon
`README.md`:n License-osio, sanasta sanaan: tekijät, vuosi ja CC BY-SA 4.0.
Zensical lisää perään oman "Made with Zensical" -rivinsä; `extra.generator:
false` poistaisi sen, mutta koeputkessa se saa näkyä.

Muokkauslinkit ("Ehdota muutosta", "Ilmoita ongelmasta") eivät kuulu tähän
kohtaan, koska ne eivät ole Materialissa alatunnisteessa lainkaan vaan sivun
oikeassa yläkulmassa kynäkuvakkeena (`content.action.edit`). Ne ovat siis oma
ratkaisunsa, ks. "Muokkauslinkki alatunnisteeseen"; "Ilmoita ongelmasta"
on yhä auki.

**Alatunniste tarvitsi yhden rivin `layout.css`:ään.** `.md-footer` ei ole
`.md-mainin` sisällä vaan sen sisarena `.md-containerissa`, joten kiskon
`padding-left` ei koskenut siihen: alatunnisteen oma ruudukko keskittyi koko
ruudun leveyteen ja jäi osittain kiskon alle. Mitattu 1440 × 900:
"Edellinen"-linkki alkoi x = 103, kisko peittää 0–300. Sama padding
`.md-footerille` siirtää sen kohdalleen (linkki 304, tekijätiedot 316, sisältö
324). Tausta ja yläreunan viiva saavat jäädä koko leveydelle, koska kisko on
läpinäkymätön ja piirtyy niiden päälle.

Mitattu leveyksillä 1220, 1280, 1440, 1920 ja 2560: alatunnisteen ruudukko on
pikselilleen sama kuin `.md-main__inner` (300/1125 leveydellä 1440, 458/1342
leveydellä 1920), eli se on täsmälleen sisällön ja oikean sivupalkin yhteinen
leveys — tämä on Materialin oma valinta, ei tässä muutettu. Leveyksillä 1100,
900 ja 390 sääntö ei ole voimassa, ja alatunniste on siellä ennallaan; 390:llä
teema piilottaa Edellinen-linkin otsikon ja jättää pelkän nuolen.

### Osien numerot myös alareunan linkkeihin (1 rivi `convert.py`:hyn)

Numerointi tuli aiemmin vain valikkoon, koska numero kirjoitetaan
`nav.yml`:n otsikkoon. Osan etusivu (`osaN/index.md`) kirjoitettiin kuitenkin
paljaana polkuna, jolloin sen oma otsikko tuli sivun H1:stä ilman numeroa.
Valikossa se ei näkynyt — siellä otsikko luetaan osiolta, ei tältä lapselta —
mutta alareunan linkeissä näkyi: "1.5 Osan kaikki tehtävät" → "Seuraava:
Olio-ohjelmoinnin perusteet", eli osat olivat ainoat numeroimattomat.

Korjaus on kirjoittaa lapselle sama numeroitu otsikko kuin osiolle
(`- "2 Olio-ohjelmoinnin perusteet": osa2/index.md` paljaan polun sijaan).
`navigation.indexes` toimii yhä, koska Zensical päättelee etusivun pelkästä
tiedostonimestä (`index.md` / `README.md`), ei siitä onko otsikko annettu.

Sama numero menee samalla `<title>`-tagiin. Se ei ole uusi poikkeama vaan
päinvastoin: numeroidut luvut ovat olleet siellä numeroituja siitä asti kun
numerointi tehtiin (mdBookissa `<title>Hei, Java! - Ohjelmointi 2`,
Zensicalissa `1.1 Hei, Java! - Ohjelmointi 2`), joten osat olivat ainoa
poikkeus. Nyt ne ovat samanlaisia kuin kaikki muut.

Todennettu vertaamalla koko edellinen/seuraava-ketju mdBookin omaan
`book/`-tulosteeseen ohjelmallisesti (numerot riisuttuna): mdBookin 72
luvusta 71 on myös Zensicalissa, ja niissä on **seitsemän eroa**, kaikki
selitettyjä:

* Neljä johtuu Tenttiohjeiden siirtämisestä Tentin alle (`NEST_UNDER`), eli
  ne ovat tarkoitettuja.
* Yksi on vertailun oma artefakti (juurisivun polku `""` vs `"."`).
* Kaksi on aito ero: SUMMARY.md:n ulkoinen linkki (Eteneminen, TIM) on
  Zensicalilla osa ketjua, mdBookilla ei. Käytännössä Luennot-sivun
  "Seuraava" vie TIMiin ja osan 1 "Edellinen" tulee sieltä. Linkki menee
  oikeaan osoitteeseen, ja koska se on navigaatiossa näkyvissä siinä
  välissä, järjestys on itse asiassa se mitä valikko lupaa. Korjaaminen
  vaatisi template-ylikirjoituksen, joten jätetty näin.

### Muokkauslinkki alatunnisteeseen (3 riviä `mkdocs.yml`:ään + `overrides/partials/copyright.html`)

mdBookin alatunnisteessa on lisenssimerkin vieressä "Ehdota muutosta": linkki
GitHubin editoriin juuri sen sivun lähdetiedostoon, ja tallennuksesta syntyy
pull request. Osoitteen antaa `book.toml`:n `edit-url-template`. Zensicalilla
vastaavaa asetusta ei ole, vaan osoite kootaan kahdesta osasta ja sivun
polusta:

```yaml
repo_url: https://github.com/ohj-perus-jy/ohj2
edit_uri: edit/main/src/
```

`edit_uri` osoittaa mdBookin lähdepuuhun `src/`, ei tämän koeputken
`docs/`:iin: `docs/` on `convert.py`:n kertakäyttöinen kopio eikä sitä ole
versionhallinnassa. Muuten polut ovat samat, joten sama `edit_uri` kelpaa
kaikille sivuille.

**Paikka vaatii mallin.** Materialissa muokkauslinkille on tasan yksi paikka,
sivun oikea yläkulma (`content.action.edit`), eikä alatunnisteeseen ole
laajennuspistettä — `base.html` tarjoaa vain koko `footer`-lohkon, joten
`main.html`-tyylinen lohkon täydennys ei riitä.
`overrides/partials/copyright.html` on siksi kopio teeman omasta, ja siihen
on lisätty linkki `.md-copyright`-lohkon **sisareksi**, ei sisälle: teema
levittää `.md-footer-meta__innerin` lapset rivin päihin
(`justify-content: space-between`), joten linkki asettuu oikeaan reunaan
itsestään. Kopio vanhenee, jos Zensical muuttaa alatunnistettaan — sama
koskee `overrides/partials/header.html`:ää, ja siksi lisäys on rajattu
yhteen lohkoon ja merkitty tiedostoon.

Ulkoasu tulee muuten teemalta. Linkki lainaa `.md-copyright`-luokkaa, josta
se saa saman koon, värin ja pystykeskityksen kuin lisenssiteksti; oma
`.md-copyright--edit` (13 riviä `layout.css`:ään) hoitaa vain kuvakkeen ja
sen, ettei `.md-copyrightin` `width: 100%` venytä linkkiä omalle riville.
Teksti tulee kielipaketista (`action.edit` = "Muokkaa tätä sivua"), kuten
Edellinen/Seuraavakin. Kuvake on teeman oma GitHub-merkki inline-SVG:nä: se
ei tuo takaisin `api.github.com`-kutsua, ks. *Repo-linkki pois*.

Mitattu 1440 × 900: linkin oikea reuna on x = 1409 ja Seuraava-linkin nuolen
1409, eli linkki tasautuu nuolen kanssa ilman omaa sääntöä — molemmat
päättyvät samaan ruudukkoon. Leveydellä 1100, jossa kiskoa ei ole, molemmat
ovat 1069. Kapealla näytöllä (390) alatunnisteen rivi taittuu ja linkki menee
lisenssitekstin alle vasempaan reunaan, kuten teeman omat some-linkit.

Kolme sivua tarvitsi poikkeuksen, koska Zensical laskee osoitteen sivun
polusta `docs/`:ssä eivätkä kaikki sivut ole siellä samalla nimellä kuin
`src`:ssä:

* `NEST_UNDER` siirtää `tentti.md` → `tentti/index.md` ja `tenttiohjeet.md` →
  `tentti/tenttiohjeet.md`. Ne käännetään takaisin.
* `PRINT_PAGE` (`tulosta.md`) syntyy vasta `convert.py`:ssä eikä sitä ole
  `src`:ssä lainkaan. Siltä linkki jätetään kokonaan pois.

Molemmat hoituvat samalla kartalla: `build_extra()` kirjoittaa `nav.yml`:ään
`extra.edit_source`-lohkon (docs-polku → src-polku, tyhjä arvo = ei linkkiä),
jonka malli katsoo ennen osoitteen kokoamista. Kartta syntyy `NEST_UNDER`- ja
`PRINT_PAGE`-vakioista, jotka pysyvät ainoina totuuksina myös silloin kun
siirtoja tai generoituja sivuja tulee lisää.

Todennettu rakennetusta `site/`:stä ohjelmallisesti: linkki on 189 sivulla ja
jokainen osoittaa tiedostoon, joka on olemassa `../src`:ssä (myös molemmat
siirretyt); ainoa sivu ilman linkkiä on `tulosta/`.

### Repo-linkki pois (`overrides/partials/source.html`)

`repo_url` on olemassa vain muokkauslinkkiä varten, mutta se toi mukanaan
repo-linkin (GitHub-kuvake, tähdet ja forkit) kahteen paikkaan: yläpalkin
oikeaan reunaan ja — mikä yllätti — kapean näytön laatikkovalikon
ensimmäiseksi kohdaksi, ennen ensimmäistäkään sivua. Jälkimmäiselle ei ole
mdBookissa vastinetta lainkaan, eikä nappia haluttu kumpaankaan.

Molemmat piirtää sama `partials/source.html`, ja molemmat ovat ehdollisia
vain sille onko `repo_url` asetettu — sitä ei siis voi ottaa pois
menettämättä muokkauslinkkiä. Ratkaisu on tyhjentää linkki itse:
`overrides/partials/source.html` on pelkkää kommenttia. Tämä on toinen (ja
toistaiseksi viimeinen) mallin ylikirjoitus.

Tyhjä malli eikä pelkkä CSS-piilotus siksi, että linkin mukana tulee
`<a data-md-component="source">`, jonka nähdessään teeman JavaScript hakee
tähdet ja forkit `api.github.com`ista. CSS piilottaisi kuvan mutta jättäisi
kutsun jokaiselle sivulataukselle.

Käärelaatikot jäävät silti paikoilleen (`.md-header__source`,
`.md-nav__source`), ja tyhjinäkin ne varaavat tilaa: edellinen 11,5rem
yläpalkin oikeasta reunasta, jälkimmäinen reunustetun laatikon verran
valikon yläreunasta. `layout.css` piilottaa ne `:not(:has(*))`-ehdolla, eli
ylikirjoituksen poistaminen palauttaa linkin ilman muita muutoksia.

Mitattu rakennetusta `site/`:stä leveyksillä 1440, 1000 ja 390 (molemmat
teemat): kumpikin kääre on `display: none`, `a.md-source`-elementtejä ei ole
yhdelläkään sivulla (osumat jäävät teeman omaan bundleen ja CSS:ään, eli
kuolleeksi koodiksi), `api.github.com`iin ei lähde yhtään pyyntöä, ja
muokkauslinkki on ennallaan. Kapealla näytöllä valikon ensimmäinen kohta
("Aloitus") alkaa nyt suoraan kurssin nimen alta.


### Välilehdet Zensicalin omalla ominaisuudella (107 riviä `convert.py`:hyn + 1 rivi `mkdocs.yml`:ään)

Työkalusivu on kirjan ainoa sivu, joka on kokonaan välilehtien varassa:
asennusohjeet ovat viidessä kohdassa erikseen Windowsille, macOS:lle ja
Linuxille. mdBookissa ne tekee `preprocessor.accordion`, jonka syntaksi on
otsikko ja vaakaviiva:

```markdown
### [Windows](#tab/win)

...ohjeet...

***
```

Peräkkäiset lohkot ovat yksi välilehtijoukko. Ilman esikäsittelijää ne olivat
Zensicalissa tavallisia otsikoita, joiden linkki (`#tab/win`) ei osoita
mihinkään: **työkalusivun 20 varoitusta olivat näitä**, ja sivun oikean reunan
sisällysluettelossa oli 28 kohtaa, joista 20 oli "Windows", "macOS", "Linux"
ja "Valitse" viiteen kertaan.

Välilehdet ovat Zensicalissa valmiina eikä niitä tarvitse kytkeä päälle:
`pymdownx.tabbed` on jo `DEFAULT_MARKDOWN_EXTENSIONS`-listalla asetuksineen
(`alternate_style`, `combine_header_slug`), ks. `zensical/config.py`. Sitä ei
siis pidä lisätä `markdown_extensions`-lohkoon — **annettu lohko korvaa koko
oletuslistan**, jolloin lähtisivät samalla `admonition`, `attr_list`,
`md_in_html`, `pymdownx.superfences` ja loput parikymmentä.

Tehtävää jää siis kaksi: syntaksin käännös ja yksi asetus.

**Syntaksi.** `convert.py`:n `convert_tabs` lukee lohkot (`read_tab_set`) ja
kirjoittaa ne Zensicalin muotoon — otsikko `=== "Windows"` ja sisältö neljä
välilyöntiä sisemmäs:

```markdown
=== "Windows"

    ...ohjeet...
```

Sisennys on ainoa asia mitä riveille tehdään, joten suhteelliset sisennykset
säilyvät: numeroidut listat, niiden sisällä olevat koodiaidat ja raaka HTML
(`<details>`, `<i class="bi ...">`) tulevat läpi sellaisenaan. Tämä on
**koeputken ensimmäinen sisältömuunnos**; se on myös ainoa mahdollinen paikka,
koska kyse on Markdownin syntaksista eikä ulkoasusta.

**Asetus.** `content.tabs.link`: yhden välilehden valitseminen valitsee saman
otsikon kaikkialta. mdBookin `accordion.js` teki saman sivun sisällä
tunnuksesta (`#tab/win`) ja muisti valinnan osoitteen `?tabs=`-parametrissa.
Material yhdistää otsikkotekstistä ja muistaa valinnan selaimen
`localStorage`issa (avain `<sivusto>.__tabs`, arvo `["Linux"]`), eli valinta
säilyy myös sivulta toiselle. `?tabs=`-osoitteita ei ole `src`:ssä yhtään,
joten mitään linkkejä ei katkea.

Kaksi tietoista eroa mdBookiin, molemmat siitä että Zensicalin välilehdissä
yksi välilehti on aina valittuna:

* **`#tab/default` jää pois.** mdBookissa se on lohko, jolla ei ole otsikkoa
  välilehtirivissä lainkaan ja joka näkyy kunnes käyttäjä valitsee jonkin
  muun. Sellaista tilaa ei täällä ole, joten lohkolla ei ole paikkaa. Yhdeksän
  lohkoa jää pois: työkalusivun viisi ja `01-hei-java.md`:n yksi ovat sama
  lause ("Valitse käyttöjärjestelmäsi yllä olevista vaihtoehdoista"), joka
  toistaa välilehtirivin yläpuolella jo olevan kehotuksen.
  `06-versionhallinnan-etakaytto.md`:n kolme ovat sen sijaan oikeaa ohjetta
  ("JY:n opiskelijat: valitse GitLab, muuten GitHub"). Se **katoaa** sivulta,
  ja jos se halutaan takaisin, paikka on välilehtien yläpuolella `../src`:ssä
  — eli sisältömuutos, ei muunnos.
* **Saman tunnuksen välilehdet saavat saman otsikon**, ensimmäisen esiintymän
  mukaan. mdBook yhdisti joukot tunnuksesta, Material otsikkotekstistä, joten
  `06-versionhallinnan-etakaytto.md`:n `#tab/gitlab` — joka on kahdessa
  joukossa "GitLab (JY)" ja yhdessä "GitLab (JYU)" — jäisi muuten kolmen
  joukon sijasta kahdeksi eri valinnaksi.

**Tulostus tuli teemalta ilmaiseksi.** mdBookissa `accordion.css` näyttää
paperilla kaikki lohkot otsikoineen (`.accordion-title-print`) ja piilottaa
`default`-lohkon. Materialin oma tyylitiedosto tekee saman ilman lisäyksiä:
`@media print` muuttaa otsikkorivin ja sisältölohkon `display: contents`iksi
ja järjestää ne `order`illa lomittain. `print.css`:ään ei siis tarvinnut
riviäkään. Mitattu selaimella `media: print` -tilassa: kaikissa viidessä
joukossa näkyvät kaikki kolme lohkoa, ja järjestys on "Windows" 579 →
sisältö 626 → "macOS" 835 → sisältö 882 → "Linux" 1010 → sisältö 1057.
Sama pätee koko kirjan tulostussivulla (`/tulosta/`): 72 luvun joukossa on
kahdeksan välilehtijoukkoa, ja `media: print` -tilassa niistä näkyvät kaikki
lohkot (5 × 3 työkalusivulta, 3 × 2 osasta 8).

Mitattu muuten:

* **Varoituksia 53 → 20.** Kaikki 33 `#tab/`-ankkuria katosivat, eikä yhtään
  uutta tullut tilalle: jäljelle jäävät 20 ovat rivilleen samat kuin ennenkin.
* **Työkalusivun sisällysluettelo 28 → 8 kohtaa**, eli tasan sivun omat
  `##`-otsikot. Välilehtien otsikot ovat `<label>`-elementtejä eivätkä päädy
  sisällysluetteloon, kuten ei mdBookissakaan.
* **Sisältö säilyy rivilleen.** Ohjelmallinen vertailu `../src`:n ja `docs/`:n
  välillä (välilehtimerkinnät riisuttuna, tyhjät rivit pois): `tyokalut.md`
  419 riviä, `01-hei-java.md` 374, `06-versionhallinnan-etakaytto.md` 129 —
  **ei yhtään eroa**, kun `#tab/default`-lohkot jätetään huomiotta.
* Selaimella 1440 × 900 ja 390 × 844, molemmissa teemoissa: välilehtirivi
  piirtyy, ensimmäinen on valittuna, macOS:n valitseminen yhdestä joukosta
  vaihtaa kaikki viisi, valinta säilyy sivun latauksen yli ja sivulta toiselle
  (työkalusivu → osa 8 → työkalusivu), eikä konsoliin tule virheitä.
  Työkalusivun (Windows/macOS/Linux) ja osan 8 (GitLab/GitHub) valinnat
  muistetaan erikseen. Ei vaakavieritystä kummallakaan leveydellä.

**Yksi joukko yhdeksästä ei aluksi piirtynyt**, ja syy oli muualla:
`01-hei-java.md`:n komentorivivälilehdet ovat raa'an `<details>`-lohkon sisällä,
eikä Python-Markdown jäsennä sellaisen sisältöä lainkaan Markdownina. Samassa
lohkossa jäivät renderöimättä myös linkit ja listat — sivulla luki
sananmukaisesti `[työkaluohjeita](../tyokalut.md#java-development-kit-jdk)`.
mdBookissa lohko toimii, joten kyse oli tarkistuslistan kohdasta 8, ei
välilehdistä. Se korjautui kohdan 8 mukana (`convert_details`) eikä
välilehtiin tarvinnut koskea: kaikki yhdeksän joukkoa piirtyvät nyt.


### Tulostus: koko kirja yhdeksi PDF:ksi (`assets/js/print.js` + `assets/css/print.css` + 53 riviä `convert.py`:hyn + yläpalkin malli)

mdBookissa tämä on `output.html.print`: yläpalkissa on tulostinkuvake, joka
vie sivulle `print.html`, jolla koko kirja on yhtenä sivuna, ja sivu avaa
tulostusikkunan itsestään. Zensicalilta ei tule mitään vastaavaa, eikä
MkDocsin tulostusliitännäisiä voi ottaa avuksi: Zensical ei aja
MkDocs-liitännäisiä lainkaan, vaan siinä ovat vain sen omat (search, tags,
meta, redirects, minify, literate-nav, awesome-nav, offline).

**Ensin kokeiltiin ilmeisintä: luvut peräkkäin yhdeksi Markdown-tiedostoksi**
`convert.py`:ssä, jossa kirjan järjestys jo tiedetään. Se ei toimi. Mitattu:
yhdistetyssä tiedostossa oli 73 `#`-otsikkoa, mutta käännetyllä sivulla vain
38 `<h1>`:tä — 32 luvun otsikko katosi. Luvut eivät ole toisistaan
riippumattomia: `<details>`-lohkon sisältö on raakaa HTML:ää `</details>`:ään
asti, jolloin lohkon sisällä olevat koodiaidat jäävät laskematta. Erillisinä
sivuina vahinko rajoittuu sivun loppuun, mutta yhdistettynä tila vuotaa
seuraavaan lukuun: `osa4/01-rajapinta.md`:n lohko nielaisi 191 441 merkkiä eli
useita seuraavia lukuja.

Samalla selvisi, ettei tuo ole tulostussivun ongelma vaan olemassa oleva:
`osa4/01-rajapinta.md` menettää oman häntänsä jo nyt omalla sivullaan — sen
kuudesta `##`-otsikosta renderöityy kaksi, ja "## Rajapinnan periminen" jää
koodilohkon sisään. Kuuluu kohtiin 4 ja 8.

**Siksi liittäminen tehdään samasta paikasta kuin mdBookissa: valmiista
HTML:stä.** mdBook renderöi jokaisen luvun erikseen ja liittää palat
peräkkäin; sama tehdään selaimessa. `print.js` hakee jokaisen luvun oman
sivun, poimii siitä `.md-content__inner`-artikkelin ja liittää sen sisällön
tulostussivulle, jolloin jokainen luku on jäsennetty erikseen — täsmälleen
kuten sitä yksin luettaessa.

Sivun runko syntyy silti `convert.py`:ssä: `docs/tulosta.md` on luettelo
kaikista luvuista `nav.yml`:n järjestyksessä. Ilman JavaScriptiä sivu on siis
kirjan sisällysluettelo eikä tyhjä.

Kolme asiaa jotka kaivautuivat esiin matkalla:

* **Osoitteet.** Suhteelliset kuvat ja linkit ratkaistaan luvun oman sivun
  suhteen ja kirjoitetaan absoluuttisina (tulostussivu on eri hakemistossa),
  mutta sivun sisäiset ankkurit jäävät sivun sisäisiksi, jotta PDF:n linkit
  hyppäävät PDF:n sisällä. Se vaatii etuliitteen jokaisen luvun tunnisteisiin:
  ilman sitä sivulla oli **1767 kahteen kertaan esiintyvää tunnistetta** —
  sama otsikko toistuu luvusta toiseen ("Tehtävät"), ja Materialin
  koodirivien ankkurit (`__codelineno-0-1`) alkavat joka sivulla alusta.
* **Luvut liitetään suoraan artikkelin lapsiksi**, ei omiin kääreisiinsä.
  Materialin tyyli osuu sisältöön suorina lapsivalitsimina
  (`.md-typeset > .highlight`), joten kääre-elementti jää niiden väliin ja
  rikkoo ne: mitattuna 390 px:llä suorana lapsena koodilohko saa Materialin
  negatiiviset marginaalit (-16 px) ja levittyy reunasta reunaan 375 px:iin,
  kääreen sisällä marginaalit katoavat ja lohko kutistuu 343 px:iin 16 px
  sisennettynä. Lukujen väliin jää pelkkä tyhjä
  `<div>` — ruudulla ohut viiva, paperilla sivunvaihto — kuten mdBookin
  `print.html`:ssä.
* **Sivukohtaiset toiminnot pois.** Muokkauslinkki ja palauteruutu ovat
  artikkelin sisällä, joten ne tulisivat muuten jokaisen luvun perään.

`assets/css/print.css` on mdBookin `theme/css/print.css`:n vastine: paperilta
pois yläpalkki, valikko ja alatunniste, sisältö koko leveydelle, sivunvaihdot
pois otsikoiden ja koodilohkojen keskeltä sekä rivitys koodille (paperilla ei
ole vaakavieritystä, joten rivittämätön koodi jäisi yksinkertaisesti pois).
Zensicalin oma tulostustyyli on yksi rivi (`.md-typeset { font-size: .68rem }`).

Tumma teema vaihdetaan tulostuksen ajaksi vaaleaksi (`beforeprint` ->
`data-md-color-scheme="default"`, `afterprint` takaisin): selaimet jättävät
taustavärit oletuksena tulostamatta, joten tummasta teemasta jäisi paperille
vaalea teksti valkoiselle. Teeman omat muuttujat kelpaavat sellaisenaan, joten
värejä ei tarvitse toistaa CSS:ssä. Mitattu: slate -> default -> slate, ja
sääntö on kaikilla sivuilla, koska yksittäisen luvun voi tulostaa ilman
tulostussivuakin.

Painike on yläpalkissa teemanvaihtimen vieressä kuten mdBookissa. Se vaatii
kopion teeman `partials/header.html`:stä, koska Materialissa yläpalkkiin ei
ole omaa laajennuspistettä — `base.html` tarjoaa vain koko `header`-lohkon.
Lisäys on neljä riviä ja merkitty tiedostossa; jos Zensical muuttaa
yläpalkkiaan, kopio on päivitettävä käsin. Mitattu leveyksillä 1920, 1440,
1100, 768 ja 390: painike on paikallaan kaikilla eikä vaakavieritystä tule.

Mitattu käännetystä sivustosta (1440 × 900, localhost):

|                         |                                                           |
| ----------------------- | --------------------------------------------------------- |
| Lukuja koottu           | 72/72, sivunvaihtoja väliin 71                            |
| Otsikoita               | 73 × `h1`, 229 × `h2` (Markdown-yhdistämisellä 38 × `h1`) |
| Kuvia                   | 53, joista lataamatta 0                                   |
| Sivun sisäisiä linkkejä | 7347, joista rikki 0                                      |
| Tunnisteita             | 14 351, joista kahteen kertaan 0                          |
| Kokoaminen              | 1,7 s                                                     |
| Tulostettuna            | A4, **noin 500 sivua** (mitattu 497 ja 499), 48 MB                                  |

Hakuindeksiin sivu ei mene (`search: exclude: true` sivun alkumetatiedoissa):
mitattuna `site/search.json` on tavulleen sama kuin ilman sivua. Myöskään
varoitusten määrä ei muutu (20 ennen ja jälkeen), koska käännettävä sivu on
vain 72 linkin luettelo.

Kaksi tietoista eroa mdBookiin ja yksi rajoitus:

- Osoite on `/tulosta/` eikä `/print.html`.
- Tulostusikkuna avautuu itsestään kuten mdBookissa, mutta vasta kun kaikki
  luvut ja kuvat ovat valmiina; ilman sitä selain tulostaisi puolityhjän sivun.
- Kokoaminen vaatii JavaScriptin ja 72 hakua. Ilman JavaScriptiä sivulla on
  lukujen luettelo.

Mobiilissa koottu sivu vuotaa vaakasuunnassa 784 px:iin, mutta sama tapahtuu
`/javafx/validointi/`-sivulla yksinäänkin: siellä FXML-esimerkki päätyy
raakana HTML:ään (`<vbox>`, `<listview>`). Vika on siis kohdissa 1 ja 5, ei
tässä.

### Monitiedostolohkot välilehdiksi ja aitojen attribuutit (~180 riviä `convert.py`:hyn + `overrides/partials/javascripts/content.html` + 16 riviä `print.js`:ään)

Kirjan koodiesimerkit ovat usein monta tiedostoa samassa lohkossa: mdBookin
`preprocessor.codeblock-tabs` jakaa lohkon `// FILE: nimi`- ja
`// FILE_END`-merkinnöistä ja piirtää tiedostoista välilehdet. Mitattuna
`../src`:stä **73 lohkoa 18 sivulla, yhteensä 194 tiedostoa** — kaksi
tiedostoa 44 lohkossa, enimmillään seitsemän.

Merkinnät ovat aineistossa epätarkkoja, ja mdBookin esikäsittelijä sietää
sen. Säännöt on luettu sen generoimasta `book/`:sta, ei arvattu:
`//FILE:` ilman välilyöntiä kelpaa (`osa3/01-perinta.md`,
`osa3/03-abstrakti-luokka.md`), nimen perässä saa olla välilyöntejä, ja
`// FILE_END` on vapaaehtoinen — tiedoston lopettaa yhtä lailla seuraava
`// FILE:`, ja ylimääräinen `// FILE_END` ohitetaan. Kolme lohkoa nojaa
tähän. `convert.py`:n `split_files` tekee samoin, ja `convert_files`
varoittaa, jos lohkossa olisi koodia ennen ensimmäistä merkintää (niitä ei
ole yhtään) sen sijaan että pudottaisi rivit hiljaisesti pois.

Muunnos on sama mekanismi kuin kohdassa 23, `pymdownx.tabbed`: tiedosto per
välilehti, koodi omana aitanaan.

````markdown
=== "main.java"

    ```{ .java .multifile }
    public class Main { ... }
    ```

=== "Valo.java"

    ```{ .java .multifile }
    public class Valo extends Laite { ... }
    ```
````

Aidan `multifile`-määre tuli mukaan vasta kohdan 3 kanssa: ajonappi lähettää
joukon tiedostot yhtenä ohjelmana, ja siihen tarvitaan tieto siitä, mitkä
välilehtijoukot ovat tiedostoja ja mitkä käyttöjärjestelmiä (kohta 23).

Omaa CSS:ää tai JavaScriptiä ei tarvittu riviäkään: välilehdet, Pygmentsin
korostus ja kopiointinappi tulevat teemalta. Myös tulostus tulee valmiina
samasta syystä kuin kohdassa 23 — mitattuna selaimella `media: print`
-tilassa `osa3/03`:n neljästä joukosta näkyvät kaikki tiedostot nimineen
(esim. main.java, Laite.java, Valo.java, Turvakamera.java, Kahvinkeitin.java),
eli sama kuin mdBookin `codeblock-tabs-title-print`.

**Kohta 4 tuli mukaan pakosta.** Ensimmäisen ajon jälkeen 15 välilehtijoukkoa
82:sta ei näkynyt sivuilla lainkaan, ja syy oli mdBookin attribuuttilista:
` ```java,ignore ` ei ole pymdownx:lle kelvollinen aita, jolloin rivi jää
tavalliseksi tekstiksi ja *sitä seuraava sulkeva aita alkaa uuden lohkon*,
joka nielaisee seuraavan tekstin koodiksi. Kyse ei siis ollut pelkästä
korostuksesta: kokonaisia lukuja oli koodilohkon sisällä. Siksi
`convert_fences` kirjoittaa attribuuttilistan pymdownx:n muotoon, **269
aitaa** (+ 20 monitiedostolohkojen aitaa, jotka `convert_files` kirjoittaa
itse).

Määreitä ei pudoteta, koska ne ovat myöhemmin tarpeen (ajonappi = kohta 3,
editori = kohta 20): ne kirjoitetaan attr_listin luokiksi.

````markdown
```java,ignore   ->   ```{ .java .ignore }
````

Tuloksena `<div class="language-java ignore highlight">`: kieli säilyy,
korostus toimii ja tieto on tallessa luokkana. Sivustolla on nyt 285
`ignore`-, 21 `noplayground`- ja 2 `editable`-lohkoa.

Mitattu ero yhdessä ja samassa rakennuksessa (ensin pelkkä
monitiedostomuunnos, sitten aidat perään):

* **Välilehtijoukkoja 67 → 81** (kaikki paitsi yksi, ks. alempana).
* **`language-java`-lohkoja 262 → 637, `language-text` 250 → 87.**
* **Varoituksia 20 → 16.** Neljä linkkiä osoitti otsikkoon, joka oli
  nielaistuna koodilohkon sisään: `#alykoti` (osa 3.3),
  `#valmiita-funktiorajapintoja` (6.1), `#geneerinen-metodi` (4.4) ja
  `#filteredlist` (`javafx/tableview.md`). Otsikot ovat taas otsikoita.

**Välilehtien linkitys rajattiin käyttöjärjestelmävälilehtiin.** Materialin
`content.tabs.link` (kohta 23) tekee kaksi asiaa: valinta tarttuu saman
otsikon kaikkiin sivun joukkoihin, ja otsikko jää selaimen muistiin
(`localStorage`, avain `/.__tabs`), josta se palautetaan joka sivulla.
Käyttöjärjestelmävalinnassa molemmat ovat koko pointti; tiedostoissa
molemmat ovat väärin, koska sama tiedostonimi toistuu monessa lohkossa 11
sivulla 18:sta ja mdBookissa jokainen lohko on erillinen. Mitattu ennen
rajausta: `Valo.java`n klikkaus `osa4/01`:ssä avasi `osa3/03`:n **kaikki
neljä** lohkoa `Valo.java`sta (kolmessa tekijän ensimmäinen tiedosto on
`main.java`), ja yksi klikkaus `osa2/02`:ssa vaihtoi **12 lohkoa 13:sta**.

Molemmat rajataan mallin ylikirjoituksessa
(`overrides/partials/javascripts/content.html`). Tiedostojoukon tunnistaa
otsikoista, eikä se ole arvaus otsikon muodosta: listan `#tab/`-välilehtien
otsikoista kerää `convert.py` samalla kun se muuntaa ne (`nav.yml`:
`extra.tab_labels` = Windows, macOS, Linux, GitHub, GitLab (JY)).

* **Muisti:** palautetaan vain listalla olevat otsikot.
* **Tarttuminen:** teeman oma linkitys ohittaa vaihdon, jos otsikossa on
  `data-md-switching` — sillä se erottaa käyttäjän klikkauksen omasta
  ketjureaktiostaan. Sama lippu asetetaan tiedostojoukkojen otsikoihin niiden
  `change`-tapahtumassa, jolloin teema jättää tekemättä sekä muiden joukkojen
  vaihtamisen että muistiin kirjoittamisen. Tämä nojaa teeman sisäiseen
  yksityiskohtaan: jos Zensical muuttaa sen, linkitys palaa entiselleen eikä
  mikään muu hajoa.

Todennettu selaimella jälkikäteen: `osa2/02`:ssa klikkaus vaihtaa enää oman
lohkonsa 13:sta, sama näppäimistöllä (nuolinäppäin radiopainikkeissa),
korostuspalkki liikkuu yhä (`--md-indicator-x` 0px → 259px), muistiin ei
kirjoiteta tiedostonimiä (`/.__tabs` on työkalusivun klikkauksen jälkeen
`["Linux"]`), työkalusivun Linux-valinta vaihtaa yhä kaikki viisi joukkoa ja
säilyy latauksen yli, eikä tiedostovalinta enää seuraa sivulta toiselle.

**Tulostussivu (`/tulosta/`).** Välilehdet ovat radiopainikkeita, ja niiden
`for`- ja `name`-attribuutit eivät ole tunnisteita, joten `print.js`:n
tunniste-etuliite ei osunut niihin: kootulla sivulla jokaisen luvun
`__tabbed_1` olisi kuulunut samaan ryhmään, jolloin koko sivulla olisi ollut
yksi valinta ja labelien `for` olisi osoittanut olemattomaan `id`:hen. Vika
oli olemassa jo kohdan 23 jälkeen, mutta koski yhdeksää joukkoa; nyt niitä on
71. Etuliite laitetaan nyt myös näihin (16 riviä `print.js`:ään). Todennettu
selaimella: 71 joukkoa, 193 radiota, **71 eri ryhmää ja 71 valittuna**, ja
välilehteä voi vaihtaa myös kootulla sivulla. Paperille tämä ei näkynyt,
koska tulostussäännöt näyttävät kaikki lohkot joka tapauksessa.

Erot mdBookiin, jotka jäävät:

* Yhden tiedoston lohkot (4 kpl) saavat yhden välilehden rivin, kuten
  mdBookissakin.
* `javafx/nakymat.md`:n `.fxml`-lohkossa ei ole kieltä eikä siis korostusta —
  sama kuin mdBookissa, jossa aidassa ei lue mitään.

### Sisällytykset (99 riviä `convert.py`:hyn)

mdBookin `{{#include}}` on sen sisäänrakennettu `links`-esikäsittelijä, ja se
ajetaan ennen kaikkia muita. Sama järjestys tässä (`convert_includes` ennen
`convert_files`iä), ja se on myös pakko: koodiaidan sisällä oleva makro on
vasta laajennuksen jälkeen sitä koodia, jonka kohdan 5 muunnos jakaa
välilehdiksi.

Mitattuna `../src`:stä **194 makroa 44 sivulla, 118 eri kohdetta**. Sijainti
ratkaisi järjestyksen:

| Missä makro on                                     | kpl | Mitä siitä tulee             |
| -------------------------------------------------- | --- | ---------------------------- |
| koodiaidan sisällä, `// FILE:`-merkintöjen välissä | 19  | kohdan 5 välilehtien sisältö |
| `<handout>`-lohkossa                                | 169 | tehtävänannot                |
| taulukon solussa                                    | 6   | takarajat                    |

**Kohta 5 oli tehty vain puoliksi.** Ennen tätä jokaisessa niistä 19
välilehdestä luki yksi rivi makroa java-koodiksi väritettynä
(`<span class="n">E31_Kisu_vaihe0</span>`), ei riviäkään sitä luokkaa, jonka
nimi välilehdessä lukee.

Muotoja aineistossa on kaksi: koko tiedosto (188) ja yksi rivi (6). Ankkureita
(`{{#include tiedosto:ANCHOR}}`) ei ole yhtään, joten niitä ei toteuteta —
tunnistamaton rivivalinta jättää makron näkyviin ja varoittaa. Kaksi
yksityiskohtaa on luettu mdBookin generoimasta `book/`:sta eikä arvattu:

- `{{#include ./takarajat.md:1}}` on **yksi rivi**, ei riviltä 1 loppuun.
  Suorittamissivun taulukossa kuudessa solussa on kuusi eri takarajaa
  (`book/suorittaminen.html`).
- Valitut rivit kootaan **ilman loppurivinvaihtoa** (mdBookin `take_lines`),
  joten solu pysyy solussa eikä koodiaidan sisään jää tyhjää riviä ennen
  sulkevaa aitaa.

Sisällytettävä tiedosto luetaan `../src`:stä eikä `docs/`:sta: tehtävänannot
ovat itsekin `docs/`:n sivuja ja muuntuvat samassa silmukassa, joten kopiosta
lukeva sisällytys saisi eri tekstin sen mukaan, kumpi tiedosto on aakkosissa
ensin.

Todennettu kolmella tavalla:

- **Koodi vastaa mdBookin omaa tulosta.** Sivuilla `osa3/01-perinta`,
  `osa4/03-perinta-ja-rajapinta` ja `javafx/viitteiden-hallinta` mdBook
  renderöi 656 koodiriviä; Zensicalin sivuilta niistä puuttuu 0.
- **Jokainen sisällytys näkyy sivullaan.** 167 sisällytystä, joista saa
  yksikäsitteisen tekstirivin, etsittiin käännetyistä sivuista: 0 puuttuu.
- **Käännöksen varoitukset eivät lisääntyneet:** 16 ennen ja jälkeen.

**Tehtävänantojen Markdown jäsentyy.** `<task>` ja `<handout>` ovat
tuntemattomia tageja ja niiden ympärillä on tyhjät rivit, joten sisältö on oma
lohkonsa: linkit, listat ja korostukset renderöityvät. Kortin ulkoasu
(`<task-title>`, `<points>`, `<task-link>`) on yhä tyylitön — se on kohta 6.

Neljä makroa jää näkyviin ja varoittaa joka ajolla:
`extra/luetelma-ja-hahmonsovitus.md` sisällyttää kolme tehtävänantoa, joita ei
ole olemassa. Sivu ei ole `SUMMARY.md`:ssä, joten mdBook ei käännä sitä
lainkaan; koeputki kääntää, koska `convert.py` kopioi koko puun.

Yksi asia kannattaa katsoa erikseen: tehtävänannot ovat nyt sekä osana lukuja
että **103 omana sivunaan** `docs/`:ssä, eli sama teksti on hakuindeksissä
kahdesti. mdBook ei julkaise niitä lainkaan (`book/exercises/` on tyhjiä
hakemistoja). Kuuluu kohtaan 6 tai omaksi rivikseen.

### Alertit admonitioneiksi (88 riviä `convert.py`:hyn)

`> [!VINKKI]` on GitHubin alert-syntaksia, jonka mdBookissa tekee
`preprocessor.alerts` (mdbook-alerts). Zensicalissa se on tavallinen
lainauslohko, jonka ensimmäisellä rivillä lukee `[!VINKKI]` — ja niin se on
tähän asti sivuilla näkynytkin, 75 kertaa.

**`mkdocs.yml`:ään ei tullut riviäkään.** Vastine on Markdownin oma
`admonition`-laajennus, joka on jo `DEFAULT_MARKDOWN_EXTENSIONS`-listalla
(`zensical/config.py`) — sama tilanne kuin välilehdillä kohdassa 23, ja samasta
syystä sitä ei saa lisätä `markdown_extensions`-lohkoon: annettu lohko korvaisi
koko oletuslistan.

Tehtävää jäi siis vain syntaksin käännös, `convert_alerts`. Tunnusrivi
kirjoitetaan admonitionin otsikoksi ja lainauksen loput rivit sen sisällöksi:
`>`-etuliite pois ja neljä välilyöntiä tilalle, samalla `indent_block`illa jolla
välilehdet sisennetään. Silloin lohkon omat sisennykset säilyvät ja koodiaidat,
luetelmat ja raaka HTML tulevat läpi sellaisenaan.

```markdown
> [!VINKKI]
>
> Käytä `List<T>`-tyyppiä.
```

```markdown
!!! tip "Vinkki"

    Käytä `List<T>`-tyyppiä.
```

**Tyyppi valittiin värin ja kuvakkeen mukaan, ei nimen.** Otsikko kirjoitetaan
joka tapauksessa näkyviin (ilman sitä Material näyttäisi tyypin oman
englanninkielisen nimen, "Tip"), joten tyypistä jää jäljelle vain väri ja
kuvake. Materialin 12 tyyppiä ovat värejä siinä missä mdBookin
`theme/alerts-style.css`:n seitsemän sääntöäkin, joten valinta on vertailu
kahden paletin välillä:

| Tunnus            | kpl | mdBookin väri      | Materialin tyyppi | Materialin väri |
| ----------------- | --- | ------------------ | ----------------- | --------------- |
| Osaamistavoitteet | 35  | `#4675e2` sininen  | `abstract`        | `#00b0ff`       |
| Huomautus         | 18  | `#448aff` sininen  | `note`            | `#448aff`       |
| Tärkeää           | 7   | `#a3699f` violetti | `tip`             | `#00bfa5`       |
| Vinkki            | 4   | `#38b3a3` turkoosi | `tip`             | `#00bfa5`       |
| WIP               | 4   | `#ff0000` punainen | `danger`          | `#ff1744`       |
| Varoitus          | 3   | `#ff9100` oranssi  | `warning`         | `#ff9100`       |
| Todo              | 3   | *(ei sääntöä)*     | `info`            | `#00b8d4`       |

Kaksi riviä osuu kohdalleen tarkalleen (`Huomautus`, `Varoitus`) ja kaksi
lähelle (`Vinkki`, `WIP`). Loput kolme ansaitsevat perustelun:

* **Tärkeää on `tip`, ja se on ainoa kohta jossa jotain menetetään.**
  Materialissa `important` on `tip`in alias, joten oikea sana on olemassa —
  mutta *vain sanana*: Zensicalin mukana tulevassa CSS:ssä ei ole yhtään
  alias-valitsinta (`.admonition.important` ei esiinny kummassakaan teemassa,
  `.admonition.tip` esiintyy), joten `!!! important` jäisi kokonaan
  tyylittömäksi. Vaihtoehto olisi ollut violetti `example`, jolla mdBookin
  ero Vinkkiin olisi säilynyt, mutta jonka kuvake on koeputki. Valittu ero:
  Tärkeää ja Vinkki näyttävät nyt samalta ja erottuvat vain otsikosta. Jos ero
  halutaan takaisin, se on oma sääntönsä ja kuuluu kohtaan 18.
* **Osaamistavoitteet on `abstract`.** Se on kirjan yleisin alertti ja
  35 sivusta 33:lla sivun ensimmäinen lohko: luettelo siitä, mitä luvusta
  pitäisi jäädä käteen. Sekä väri (sininen) että kuvake (mdBookissa
  muistikirja, Materialissa muistilista) osuvat lähemmäs kuin millään muulla
  tyypillä.
* **Todo on `info`**, joka on Materialin oma alias sanalle `todo`. mdBookissa
  `.mdbook-alerts-todo`-sääntöä ei ole lainkaan, joten `--mdbook-alerts-color`
  jää määrittelemättä eikä väriä tule: nämä kolme alerttia näyttävät
  Zensicalissa paremmalta kuin mdBookissa.

Tunnus luetaan pienaakkosina, koska aineistossa se on kirjoitettu miten
sattuu (`VINKKI` ja `Vinkki`, `TODO` ja `todo`); mdBook teki saman ja palautti
ison alkukirjaimen vasta CSS:n `text-transform: capitalize`illa. Tässä
oikeinkirjoitus on taulukossa, joten se on kerralla kunnossa — myös `WIP`, jolle
mdBookissa oli oma `text-transform: uppercase` -sääntö.

**Yksi tuntematon tunnus.** `extra/luetelma-ja-hahmonsovitus.md`:ssä on
`[!Tärkeää — invariantti]`, joka ei ole taulukossa. Se ei katoa: otsikoksi tulee
tunnus sellaisenaan, tyypiksi `note`, ja `convert.py` kertoo siitä ajon lopuksi
(`alertit: 75 lohkoa, tuntematon tunnus: Tärkeää — invariantti`). Sivu ei ole
`SUMMARY.md`:ssä, joten mdBook ei käännä sitä lainkaan — mdBookissa tunnus
olisi jäänyt yhtä lailla värittömäksi.

`convert_alerts` ajetaan ennen `convert_tabs`ia: välilehden sisältö sisennetään,
ja sisennetty `>` ei ole enää lainauslohkon alku. Aineistossa yhtään alerttia ei
tällä hetkellä ole välilehden sisällä, mutta järjestys on ilmainen.

Todennettu kolmella tavalla:

- **Jokainen 75 lohkosta muuntui:** `docs/`:ssä on 75 admonitionia ja 0
  jäljelle jäänyttä `[!`-merkintää. Lainaukset, jotka eivät ole alertteja,
  ovat tallessa kuudella sivulla.
- **Käännöksen varoitukset eivät muuttuneet:** 16 ennen ja jälkeen.
- **Selaimessa molemmilla teemoilla:** kaikki seitsemän tyyppiä renderöityvät
  otsikkoineen, kuvakkeineen ja yllä olevine väreineen, ja koodiaidat alerttien
  sisällä (esim. `osa8/04-useita-nakymia`) saavat korostuksensa.

Mitä ei tullut: mdBookin omat kuvakkeet (muistikirja, hehkulamppu, jakoavain)
ovat nyt Materialin vastaavat, värit ovat Materialin oletuspaletti ja Tärkeää
on samannäköinen kuin Vinkki — kaikki kolme kuuluvat kohtaan 18.

### Alerttilaatikoiden tyyli (uusi `assets/css/admonitions.css` + 1 rivi `mkdocs.yml`:ään)

Zensicalilla on kaksi teemavarianttia (`zensical/config.py`: `theme.variant`),
ja ne piirtävät admonitionin eri tavalla. Oletus `modern` tekee siitä yhden
väripinnan: koko laatikko on tyypin väriä 10 %:n peitolla, reunusta ei ole,
kulmat ovat `.4rem` ja teksti `.64rem` eli pienempää kuin leipäteksti
(`.md-typeset`: `.75rem`). `classic` eli Material for MkDocsin tuttu ulkoasu
tekee saman toisin: ohut reunus koko laatikon ympäri, väriä vain otsikkorivillä,
sisältö sivun omalla taustalla. Jälkimmäinen valittiin.

**`theme.variant: classic` olisi ollut yksi rivi, mutta se vaihtaisi koko
sivuston:** kirjasimiksi tulisi Roboto ja Roboto Mono Interin ja JetBrains Monon
tilalle, kuvakkeiksi Material-ikonit Luciden tilalle, ja välistykset koko
teemasta. Halutaan vain laatikot, joten kohteeksi otetaan ne.

**Värit ovat teeman omat.** `--adm`-muuttujaan luetaan sama Materialin
oletuspaletti, joka teemalla oli jo käytössä (ks. kohta 7); vain se, mihin väri
laitetaan, muuttuu. Reunus, otsikkopalkki ja kuvake ottavat sen samasta
paikasta.

Kaksi poikkeamaa Materialin classicista:

* **Tekstikoko on ympäröivän leipätekstin** (`font-size: inherit`). Materialilla
  laatikon teksti on `.64rem` molemmissa varianteissa; mdBookissa alertin teksti
  on samaa kokoa kuin leipäteksti, koska `theme/alerts-style.css` ei koske
  `font-size`een. Kirjan tapa säilytettiin. `inherit` seuraa myös `print.css`:n
  `.md-typeset { font-size: .68rem }` -sääntöä, joten omaa tulostussääntöä ei
  tarvita.
* **Väljyys on suurempi kuin classicin `.6rem`:** `1rem` sivuilla ja
  alalaidassa, `.5rem` otsikkorivin ylä- ja alapuolella. Kun kokoeroa
  leipätekstiin ei enää ole, erottuminen jää reunuksen, otsikkopalkin ja ilman
  varaan.

**Tarkkuus vaati kaksi ratkaisua**, molemmat kommentoitu tiedostossa. Teeman
säännöt ovat tyyppikohtaisia (`.md-typeset .admonition.note`) eli tarkkuudeltaan
(0,3,0), kun taas `.md-typeset .admonition` on (0,2,0). Tiedosto ladataan
`extra_css`:nä teeman jälkeen, joten sama tarkkuus riittää voittamaan mutta
pienempi ei: taustaväri kumotaan siksi `[class]`-valitsimella, joka ei rajaa
mitään vaan nostaa tarkkuuden. Otsikkorivin sisennykset kirjoitetaan
`[dir=ltr]`-etuliitteellä samasta syystä, kuten Material itse tekee.

**Avattavat osiot eivät ole alertteja.** Sisällössä on 57 sivullista raakoja
`<details>`-lohkoja, joilla ei ole admonition-tyyppiä. Teema antaa niille
silloin oletuksen eli `note`n sinisen ja paperiliitinkuvakkeen, ja avausnuoli
jää yksin oikeaan laitaan. Reunuksen kanssa lohko alkoi näyttää alertilta — ja
vieläpä samalta kuin oikea `!!! tip "Vinkki"`, joita samoilla sivuilla on. Kaksi
eroa tehtiin: väri neutraaliksi (`--md-default-fg-color--lighter`) ja nuoli
otsikkotekstin viereen kuvakkeen paikalle, mistä se kääntyy auetessa — alas kun
lohkon voi avata, ylös kun sen voi sulkea. Oikean laidan toinen nuoli on pois,
ja otsikkorivillä on osoitin ja hover.

Kaksi mittaa piti hoitaa erikseen, ja molemmilla on sama juuri: osassa lohkoista
sisältö on jäänyt Markdowniksi eli pelkiksi tekstisolmuiksi (kohta 8, joka
korjattiin vasta tämän jälkeen).

* **Suljetun lohkon alle jäi tyhjä kaistale.** `:last-child` katsoo DOM:ia eikä
  sitä, mitä piirretään: suljetun lohkon sisältö on paikallaan, se vain jätetään
  piirtämättä, joten otsikkorivi ei ole viimeinen lapsi. Sivulla
  `suorittaminen.md` kaksi kolmesta lohkosta oli sattumalta kunnossa, koska
  niiden sisältö on tekstisolmuja, jotka `:last-child` ohittaa — kolmannessa on
  `<video>`. Sääntö on siksi `details:not([open]) > summary`.
* **Avatun lohkon pohjalla ei ollut tilaa.** Väljyys tuli viimeisen lapsen
  marginaalista, eikä tekstisolmulla ole marginaalia. Nyt se tulee laatikon
  omasta paddingista (`details[open] { padding-bottom: 1rem }`), ja viimeisen
  lapsen marginaali nollataan, ettei elementtisisältöisiin lohkoihin tulisi
  molempia.

Todennettu selaimessa molemmilla teemoilla: seitsemän alerttityyppiä
otsikkoineen, kuvakkeineen ja väreineen, sekä `<details>` suljettuna ja
avattuna, kummallakin sisältömuodolla. Käännöksen varoitukset eivät muuttuneet:
16 ennen ja jälkeen.

**Kaksi kuvaketta vaihdettiin, sarja ei.** Lucide pysyy, koska sama sarja
piirtää sivun valikon, haun, edellisen ja seuraavan sekä avattavan osion nuolen.
Teeman oletus `note`-tyypille on kuitenkin paperiliitin, joka ei kerro
huomautuksesta mitään — mdBookissa Huomautus on info-ympyrä — joten Huomautus
osoitetaan `--md-admonition-icon--info`-muuttujaan. Silloin Todo (`info`, 3 kpl)
näyttäisi samalta kuin Huomautus (18 kpl), sillä ne eroaisivat vain sinisen
sävyssä, joten Todo saa kysymysmerkin (`--md-admonition-icon--question`).
mdBookissa Todolla ei ollut kuvaketta lainkaan, joten siinä ei menetetä mitään.
Tiedostossa ei ole yhtään SVG:tä: molemmat ovat teeman omia muuttujia, joten
riittää osoittaa toiseen niistä.

Mitä ei tullut: muut kuvakkeet ovat Luciden eivätkä mdBookin omat — Vinkin
liekki ja WIP:n salama ovat eri kuvia kuin kirjan hehkulamppu ja jakoavain — ja
Tärkeää on
edelleen samannäköinen kuin Vinkki — molemmat kuuluvat kohtaan 18. Jos ero
halutaan takaisin, se ei vaadi CSS-kikkailua vaan yhden sanan `convert.py`:hyn:
python-markdownin admonition-syntaksi ottaa tyypin perään lisäluokkia, eli `!!!
tip tarkeaa "Tärkeää"` tuottaisi `class="admonition tip tarkeaa"`, jolloin
`.md-typeset .tarkeaa { --adm: … }` hoitaisi loput.

### Avattavat osiot (49 riviä `convert.py`:hyn)

`<details><summary>Vinkki</summary>` on raakaa HTML:ää, ja Python-Markdown
päästää raa'an HTML-lohkon sisällön läpi sellaisenaan: numeroitu lista jää
muotoon `1.`, linkki muotoon `[teksti](osoite)` ja `` `koodi` `` backtickeineen.
Automaattilinkki `<https://…>` katoaa kokonaan, koska selain lukee sen
tuntemattomaksi tagiksi — `index.md`:n Teams-ohjeessa luki "osoitteessa ." ilman
osoitetta. mdBookin pulldown-cmark lopettaa HTML-lohkon tyhjään riviin ja jatkaa
Markdownin jäsentämistä, joten kirjassa lohkot ovat kunnossa.

**`mkdocs.yml`:ään ei tullut riviäkään.** Vastine on `md_in_html`-laajennus,
joka on jo `DEFAULT_MARKDOWN_EXTENSIONS`-listalla (`zensical/config.py`) — sama
tilanne kuin alerteissa kohdassa 7 ja välilehdissä kohdassa 23, ja samasta
syystä sitä ei saa lisätä `markdown_extensions`-lohkoon: annettu lohko korvaisi
koko oletuslistan. Puuttui siis vain attribuutti itse avaustagissa.

```markdown
<details><summary>Vinkki</summary>
```

```markdown
<details markdown="1"><summary>Vinkki</summary>
```

**Avaustagi on aineistossa kahta muotoa:** `<details>` (70) ja `<details
closed>` (18). Jälkimmäinen ei ole HTML:ää — attribuutti on `open`, eikä
`closed` tarkoita mitään — mutta lopputulos on silti se, mitä kirjoittaja
tarkoitti, ja sama kummallakin generaattorilla, joten attribuutti jätettiin
paikalleen. Regexissä on negatiivinen lookahead, joten uudelleenajo ei lisää
toista attribuuttia, ja koodiaidat ohitetaan pareittain kuten
`convert_fences`issä. Aineistossa yhtään `<details>`-tagia ei tällä hetkellä ole
aidan sisällä, mutta HTML-esimerkki koodilohkossa on juuri sitä, mitä aidan
sisällä voisi olla.

**Yhdeksäs välilehtijoukko piirtyi samalla.** `01-hei-java.md`:n
käyttöjärjestelmävälilehdet ovat `<details>`-lohkon sisällä, ja ne jäivät
piirtymättä kohdissa 5 ja 23 tehdystä työstä huolimatta. Nyt joukko piirtyy,
eikä välilehtiin tarvinnut koskea.

**Kaksi kuollutta ankkuria tuli näkyviin**, kumpikaan ei tämän muutoksen
aiheuttama: molemmat linkit ovat `<details>`-lohkon sisällä, eikä niistä ennen
syntynyt linkkiä lainkaan. Syyt ovat eri, ja molemmat on kirjattu
`tests/test_book.py`:n `KNOWN_DEAD_ANCHORS`-joukkoon perusteluineen.

| Ankkuri                                            | Syy                                                                                                        |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `#opas-java-ohjelmien-kääntäminen-ja-ajaminen`     | Kohta 13: Zensical riisuu tunnisteesta ääkköset, linkissä ne ovat tallessa. mdBookissa linkki toimii.      |
| `#harjoitustyön-tekniset-vaatimukset-ja-arviointi` | Aineiston virhe: otsikko on `## Tekniset vaatimukset ja arviointi` ilman etuliitettä. Rikki myös kirjassa. |

Todennettu kolmella tavalla:

- **Jokainen tagi muuntui:** ajossa 143 tagia, enemmän kuin lähdepuun 88, koska
  `convert_includes` tuo tehtävänannot sivuille ennen tätä. `docs/`:ssä on 107
  `<details markdown="1">` ja 36 `<details closed markdown="1">`, jokainen tasan
  yhdellä attribuutilla, eikä yhtään käsittelemätöntä tagia jäänyt.
- **Käännöksen varoitukset eivät muuttuneet:** 16 ennen ja jälkeen.
- **Selaimessa:** `index.md`:n Teams-ohje renderöityy `<ol>`:nä, viisi kohtaa,
  kolme linkkiä ja neljä `<code>`-jaksoa — myös ne kaksi `<https://…>`-linkkiä,
  jotka olivat kadonneet kokonaan. Sivulla `osa1/01-hei-java.md` ei ole enää
  yhtään raakaa Markdown-linkkiä.

**Väljyydeksi kirjoitetut `<br />`-rivit pois (`drop_breaks`, 58 riviä `convert.py`:hyn).**
Kahden avattavan osion väli oli kolminkertainen muihin nähden sivulla
`exercises/3-3-verkkokauppa-3/handout.md`. Syy ei ollut CSS vaan lähde: lohkojen
välissä on oma rivinsä `<br />`, josta Python-Markdown tekee kappaleen
(`<p><br /></p>`). Se vie kokonaisen rivin verran tilaa omien marginaaliensa
lisäksi, ja päälle tulee vielä laatikon oma `margin: 1.5625em 0`, joka ei enää
pääse limittymään naapurin kanssa: väli oli selaimessa mitattuna 74 px siinä
missä kaksi peräkkäistä lohkoa ovat muuten 23 px:n päässä toisistaan.

Rivit on kirjoitettu aikanaan väljyydeksi, mutta kummallakin generaattorilla
laatikolla on nyt oma marginaali (mdBookissa `margin-block: 1em`,
`theme/css/general.css`), joten ne ovat turhia molemmissa. `src/` on yhteinen
mdBookin kanssa eikä siihen kosketa, joten rivi pudotetaan käännöksessä:
neljä riviä kolmessa tiedostossa, ajossa 10 kertaa, koska `convert_includes` tuo
tehtävänannot myös tehtäväsivuille. Ehtona on tyhjä rivi kummallakin puolella —
juuri se tekee rivistä oman kappaleen — ja sarake 0: rivin lopussa `<br />` on
oikea rivinvaihto kappaleen sisällä ja sisennetty rivi voisi olla sisennettyä
koodia. Toinen ympäröivistä tyhjistä riveistä lähtee tagin mukana, jottei
tilalle jää kahta peräkkäistä.

Todennettu: `docs/`:ssä ei ole yhtään `<br />`-riviä eikä `site/`:ssä yhtään
`<p><br /></p>`-kappaletta, käännöksen varoitukset ovat yhä 16, ja selaimessa
mitattuna sivun kahden lohkon väli on 74 px:n sijaan 23 px. Aineistossa ei ole
yhtään kappaleen sisäistä `<br />`:ää, joten muunnos ei voinut osua sellaiseen —
ehto on silti testeissä.

### Tehtäväkortit (uusi `assets/css/tasks.css` + 128 riviä `convert.py`:hyn + 1 rivi `mkdocs.yml`:ään)

Tehtävä on kirjassa omia elementtejä, joita HTML ei tunne:

```markdown
<task>
  <task-title num="2.1">Kello<points>1 p.</points></task-title>
  <handout>

  {{#include ../exercises/2-1-kello/handout.md}}

  </handout>
  <task-link><a href="...">Tee tehtävä TIMissä</a></task-link>
</task>
```

Kirjassa ne tyylitetään sellaisenaan — `theme/tasks.css` osoittaa suoraan
tageihin, ja selain tyylittää tuntemattomankin elementin — mutta täällä ne
eivät kelvanneet. Python-Markdown tunnistaa HTML-lohkon tagin nimestä
(`markdown.util.BLOCK_LEVEL_ELEMENTS`), eikä `<task>` ole listalla: koko
kortti jäi kappaleen sisään muotoon `<p><task> … <handout></p>` ja
tehtävänannon Markdown jäsentyi väärään paikkaan. Samasta syystä `md_in_html`
ei olisi käsitellyt lohkon sisältöä, vaikka tageihin olisi lisännyt
`markdown`-attribuutin. Kortti on siis käännettävä diveiksi.

```html
<div class="task" markdown="1">

<div class="task-head"><span class="task-num">2.1</span><span class="task-name">Kello</span><span class="task-points">1 p.</span></div>

<div class="task-handout" markdown="1">

Tee luokka `Kello`…

</div>

<div class="task-link"><a href="...">Tee tehtävä TIMissä</a></div>

</div>
```

**`mkdocs.yml`:ään tuli yksi rivi** (`assets/css/tasks.css`), ei muuta:
`md_in_html` on jo `DEFAULT_MARKDOWN_EXTENSIONS`-listalla, sama tilanne kuin
avattavissa osioissa kohdassa 8.

**`markdown="1"` on vain kahdessa paikassa.** Ulommassa divissä siksi, että
`md_in_html` ei etene sisempiin lohkoihin, jos uloin on käsittelemätöntä
raakaa HTML:ää; tehtävänannossa siksi, että se on Markdownia. Tunnusrivi ja
TIM-linkki ovat tekstiä ja valmista HTML:ää, joten ne jäävät ilman. Sisennys
poistetaan ja jokainen tagirivi erotetaan tyhjällä rivillä: lohkotason HTML
tunnistetaan vain omana kappaleenaan, ja neljällä välilyönnillä sisennetty
rivi olisi koodilohko. Aineistossa samoja tageja on neljällä eri
sisennyssyvyydellä, eli sisennys on lähteessä pelkkää muotoilua.

**Ilme on tarkoituksella eri kuin kirjassa.** mdBookissa kortti on laatikko:
täytetty numerolaatta otsikkopalkissa, tehtävänanto omalla alueellaan ja
TIM-nappi alapalkissa. Täällä numero riippuu vasemmassa marginaalissa
oppikirjan tapaan ja tehtävät erottuvat toisistaan ohuella viivalla. TIM-nappi
sen sijaan jäi kirjasta: se on kortin ainoa toiminto, ja tehtävänannossa on
usein omia linkkejä, joista täytetty nappi erottuu heti. Alapalkkia sillä ei
ole, vaan se on kaistan viimeinen rivi. Syitä kevyempään korttiin on
kaksi: tehtävänanto kulkee samalla palstalla kuin luvun muu teksti, joten
koodilohkot saavat täyden leveyden (43 tehtävänannossa on koodiaita), ja osan
tehtäväsivulla tehtäviä on 8–12 peräkkäin, jolloin yhtä monta laatikkoa
peräkkäin on raskas sivu. Peräkkäiset tehtävät ovat yhtä kaistaa: alempi
kortti kumoaa ylemmän alamarginaalin negatiivisella ylämarginaalilla ja jättää
yläviivan pois, joten viivoja on tasan yksi kahden tehtävän välissä.

**Kapean palstan säännöt ovat container- eivätkä media-kyselyitä.** Kortti on
itse kyselysäiliö (`container-type: inline-size`), joten mitta on
artikkelipalstan leveys eikä ikkunan: sama sääntö osuu myös silloin kun ikkuna
on jaettu tai kun sivu tulostetaan. Kapea on perustila ja leveä lisäys, joten
selain joka ei tunne `@containeria` piirtää kortin kapeana eikä rikkinäisenä.
Säiliöksi valittiin kortti eikä `.md-content__inner`, koska `container-type`
tekee elementistä sijoituksen sisältävän lohkon absoluuttisesti sijoitetuille
jälkeläisille — omalle kortille se on turvallista, koko artikkelille ei.

**Bonustähti ei tarvinnut ikonifonttia.** Lähteessä se on `<i class="bi
bi-stars">`, ja Bootstrap Iconsia ei ladata (kohta 17). Muunnos poimii tagista
vain tiedon "tämä on bonus" ja kirjoittaa nimen sisään liuskan
`<span class="task-bonus">Bonus</span>`; tähden piirtää tyyli `::before`-
sisältönä, eli se ei päädy ruudunlukijalle eikä sivun hakuun. Liuska jää nimen
*sisälle* kuten lähteessäkin, jolloin se seuraa nimen viimeistä sanaa myös
silloin kun nimi rivittyy. `vertical-align: middle` on siinä välttämätön eikä
kosmeettinen: `inline-flex`-laatikolla, jonka oma `align-items` on `center`,
ei ole tekstin peruslinjaa, jolloin selain synnyttää sen laatikon alareunasta
ja tunnusrivin `align-items: baseline` kohdistaisi liuskan *alareunan* otsikon
peruslinjaan.

**Värit tulevat `--md-typeset-a-color`-muuttujasta**, eli samasta jolla teema
piirtää linkit. Se on ainoa Materialin muuttuja, joka on molemmissa teemoissa
oikea: vaaleassa se on indigo `#4051b5`, tummassa teema vaihtaa sen
vaaleampaan `#5488e8`:aan. `--md-primary-fg-color` olisi molemmissa sama tumma
indigo eli tummassa teemassa lukukelvoton. Napin täyttö on sama väri, mutta
teksti on vaaleassa teemassa valkoinen (6,9:1) ja tummassa lähes musta: tumman
teeman vaaleammalla sinisellä valkoinen jäisi 3,5:1:een eli alle pienen tekstin
4,5:1:n rajan. Kirjassa on sama ratkaisu, siellä tumman teeman kultanapissa on
musta teksti. Osoittimen alla ja näppäimistökohdistuksessa napin ympärille
syttyy saman sävyn hehku: kaksi siirtämätöntä `box-shadow`ia, tiukka sumu ja
sen ulkopuolella laajempi kajo, jolloin nappi näyttää syttyvän eikä nousevan
sivulta. Tummassa teemassa hehku on hieman vahvempi, koska tumma tausta imee
värin. Paperille nappi palaa tekstilinkiksi, koska selain ei tulosta
taustavärejä oletuksena ja valkoinen teksti katoaisi paperiin. Erotinviiva on
`--md-default-fg-color--lightest` `.05rem`:n paksuisena, tasan se mitä teema
käyttää `<hr>`:ssä. Bonuskullalle ei ole teeman muuttujaa, koska JYU-paletti on
kokonaan tekemättä (kohta 18): mdBookin `.jyu-gold` `#C29A5B` on valkoista
vasten kontrastiltaan 2,4:1, eli liian vähän pienelle tekstille, joten liuska
käyttää siitä tummennettua (4,7:1) ja tummassa teemassa vaalennettua sävyä.

Todennettu neljällä tavalla:

- **Jokainen kortti muuntui:** ajossa 169 korttia, tasan yhtä monta kuin
  lähdepuussa on `<task>`-tagia, ja niistä 36 bonuksena. `docs/`:ssä ei ole
  enää yhtään `<task>`-, `<points>`-, `<handout>`- tai
  `<task-link>`-tagia.
- **Käännöksen varoitukset eivät muuttuneet:** 16 ennen ja jälkeen.
- **Testit:** 82 läpi, joista seitsemän uutta `test_convert.py`:ssä.
  Koekirjaan (`tests/book`) lisättiin kaksi tehtävää, joista toinen bonus ja
  avattava lohko tehtävänannossa.
- **Selaimessa mitattuna** (`osa1/05-tehtavat`, tehtävä 1.7): 835 px:n
  palstalla numero on kohdassa 324 px ja nimi, tehtävänanto ja TIM-linkki
  kaikki kohdassa 436 px, eli sisennys on tasan 5,6 rem; 353 px:n palstalla
  numero on nimen edessä kohdassa 16 px eikä sisennystä ole. Kahden peräkkäisen
  tehtävän väli on 0 px ja alemman yläviiva 0 px, eli kaista on yhtenäinen.
  Numeron väri on `rgb(64, 81, 181)` vaaleassa ja `rgb(84, 136, 232)`
  tummassa.

Kohta 17 kutistui samalla: 136 Bootstrap-ikonista 36 oli tehtävien
bonustähtiä, eivätkä ne enää tarvitse fonttia. Loput 100 odottavat yhä omaa
ratkaisuaan: 45 `bi-chevron-right` valikkomaisissa linkeissä, 30
`bi-stars jyu-gold` avattavien lohkojen `<summary>`-riveillä ja 25 muuta.

### Taulukoiden tyyli (uusi `assets/css/tables.css` + 1 rivi `mkdocs.yml`:ään)

Kirjassa taulukko on keskitetty ja väritetty (`theme/css/general.css`:
`table { margin: auto auto 1.5em auto }`, otsikkorivillä `--table-header-bg`
ja joka toisella rivillä `--table-alternate-bg`). Zensical piirtää sen
harmaana ristikkona sivun vasempaan laitaan: reunus ja rivien väliviivat ovat
`--md-typeset-table-color`, ja väriä on vain hover-korostuksessa. Aineiston 27
taulukosta 22 on 2-3-sarakkeisia eli kapeita, ja vasempaan laitaan
tarrautuneena ne näyttävät tekstin sekaan unohtuneilta.

**Värit tulevat teeman muuttujista.** Sävy on `--md-typeset-a-color` eli sama,
jolla teema piirtää linkit ja jolla tehtäväkortit on jo väritetty: se on ainoa
Materialin muuttuja, joka on molemmissa teemoissa oikea (vaaleassa indigo
`#4051b5`, tummassa vaaleampi `#5488e8`). `--md-primary-fg-color` olisi
molemmissa sama tumma indigo, eli tummalla taustalla se ei erottuisi. Tästä
seuraa, että **kohta 18 (JYU-paletti) hoitaa taulukot mukanaan**: kun paletti
vaihdetaan, otsikkorivi vaihtuu samalla eikä tähän tiedostoon tarvitse koskea.
Kirjan `#dfe9f0` ei siksi ole kovakoodattuna, vaikka lopputulos vaaleassa
teemassa on käytännössä sama vaalea sinisävy.

Sävyt kirjoitetaan `color-mix`illä läpinäkyviksi eikä valmiiksi väreiksi, jotta
sama arvo toimii kummallakin taustalla — teema antaa taululle
`--md-default-bg-color`-taustan, jonka päälle ne sekoittuvat. Tummassa teemassa
otsikkorivi ja hover ovat vahvempia (20 % ja 12 % vastaan 12 % ja 8 %), koska
suuremmalla kontrastilla sama peitto näyttää laimeammalta.

Neljä pintaa: otsikkorivi korostusvärin sävyllä, sen alla `.1rem` korostusviiva,
joka toinen sisältörivi 3,5 % tekstin väriä, ja hover korostusvärin sävyllä.
Kaksi yksityiskohtaa piti hoitaa erikseen:

* **Otsikon alla olisi ollut kaksi viivaa.** Teema piirtää rivien väliviivat
  solujen ylälaitaan, joten ensimmäisen sisältörivin viiva otetaan pois.
* **Raita voittaisi hoverin**, koska tarkkuus on molemmilla sama (0,3,3), joten
  hover-sääntö on tiedostossa raidan jälkeen. Sen väri on korostusvärin sävy
  eikä teeman oma `--md-typeset-table-color--light`, joka on käytännössä sama
  harmaa kuin raita. Teeman laatikkovarjo otetaan pois: se piirsi rivin
  ylälaitaan taustanvärisen viivan peittämään väliviivan, mikä raitojen kanssa
  katkaisee rivin.

**Keskitys ei kohdistu tauluun vaan kääreeseen.** Teema kietoo taulukon
ajonaikaisesti kahteen diviin (`bundle.js`: `md-typeset__scrollwrap` >
`md-typeset__table`), jotta leveä taulukko vierii vaakasuunnassa palstan
levyisessä laatikossa. Sisempi kääre on `inline-block` eli valmiiksi sisältönsä
levyinen mutta kiinni vasemmassa laidassa; `display: block` + `width:
fit-content` pitää leveyden ennallaan mutta tekee automarginaaleista tehokkaat.
Taulukko itse saa jäädä tauluksi, mikä on myös saavutettavuuden kannalta oikein:
osa ruudunlukijoista menettää taulukkosemantiikan, jos taulun oma `display`
vaihdetaan.

Sama sääntö kirjoitetaan varalta myös taululle itselleen, koska kääreen tekee
JavaScript: **tulostussivun luvut kootaan sivulle sen jälkeen**, eivätkä ne saa
käärettä lainkaan. Ilman tätä koko kirjan PDF:ssä taulukot olisivat vasemmassa
laidassa. Kääreen sisällä taulukon oma sääntö on kumottava takaisin
tauluksi; teemalla on siihen oma sääntönsä (`html .md-typeset__table table`),
mutta sen tarkkuus (0,1,2) on pienempi kuin tämän tiedoston (0,2,1), joten se
on toistettava.

Todennettu selaimessa 1400 px:n ikkunassa, palstan leveys 779 px:
`osa1/02-muuttujat-ja-tietotyypit` (3 saraketta, 449 px) on keskitetty — 165 px
tilaa molemmin puolin — ja `luennot` (5 saraketta) täyttää palstan reunasta
reunaan kuten ennenkin, eli vierityskäyttäytyminen ei muuttunut.
Tulostussivulla taulukko on kääreetön ja keskitetty (395 px molemmin puolin).
Otsikkorivi on `rgb(232, 234, 246)` vaaleassa ja `rgb(26, 37, 58)` tummassa;
hover erottuu raidasta molemmissa. Testit 82/82 läpi, käännöksen varoitukset
16 ennen ja jälkeen.

Mitä ei tullut: kirjan pystyviivat. Kirjassa jokaisella solulla on reunus joka
sivulla, Materialilla vain rivien välissä; jälkimmäinen säilytettiin, koska
väritys tekee rivit muutenkin luettaviksi. Vuororivi on 3,5 % tekstin väriä
kirjan `#e6e8ea`:n sijaan, koska Materialin solupehmuste on kirjaa reilumpi
(`.9375em` vastaan 5 px) ja yhtä tumma raita olisi paljon isompi pinta.

### Harjoitustyösivu: vaatimuslohkot ja aiheiden yhteenvedot (uusi `assets/css/requirements.css` + 1 rivi `mkdocs.yml`:ään + ~60 riviä `convert.py`:hyn)

`harjoitustyo.md` oli aineiston ainoa sivu, jolla raakaa HTML:ää on muutakin
kuin `<details>`-tageja, ja se näkyi: sivun 751 rivistä yli 200 tuli ulos
lähdemuodossaan.

**Pahin oli arviointiperuste.** Osio "Tekniset vaatimukset ja arviointi" on 193
riviä yhden `<div class="ht-reqs">`:n sisällä, ja siellä kahdeksan
`<div class="req">`-lohkoa otsikkoineen ja numeroituine kohtineen. Ilman
markdown-attribuuttia koko osio piirtyi yhtenä pötkönä, jossa luki
"### Vaatimus 1: Tietomalli 1. \*\*Sovelluksessa on vähintään kaksi...\*\*" —
eli tasan se sivu, jonka perusteella harjoitustyö arvioidaan, oli sivuston
huonoiten luettava. Sama syy kuin kohdassa 8: Python-Markdown päästää raa'an
HTML-lohkon sisällön läpi sellaisenaan.

Vastine on sama `md_in_html` kuin kohdissa 6, 7, 8 ja 23, eli laajennuslistaan
ei tarvinnut koskea; `mkdocs.yml`:n ainoa uusi rivi on alempana kuvatun
tyylitiedoston lataus. Attribuutti tarvitaan myös uloimpaan diviin —
laajennus ei etene sisempiin lohkoihin, jos uloin on käsittelemätöntä HTML:ää —
ja `convert_divs` ajetaan ennen `convert_tasksia`, jotta se näkee vain lähteen
omat yhdeksän diviä eikä tehtäväkorttien omia, jotka saavat attribuuttinsa (tai
jäävät tarkoituksella ilman) siellä.

**Numerointi on tyyli, ei tekstiä.** Lähteessä vaatimuskohdat ovat tavallinen
numeroitu lista, ja jokainen lohko alkaa ykkösestä; kirjassa listanumeroksi tulee
lohkon ja kohdan numero yhdessä (`theme/css/general.css`: `div.ht-reqs`), eli
1.1, 1.2, ... 8.3. Numeroon viitataan sekä samalla sivulla ("yksilötöissä kaksi;
vaatimus 1.1") että osien 9-12 ohjeissa, joten pelkkä juokseva numerointi
osoittaisi väärään kohtaan. Sama CSS-laskuri siis tänne, omaan tiedostoonsa
samasta syystä kuin `admonitions.css`, `tasks.css` ja `tables.css`. Kaksi eroa
kirjan sääntöön: sisäkkäinen kirjoitustapa on purettu erillisiksi valitsimiksi
kuten muukin koeputken CSS, ja lista on rajattu lohkon suoraksi lapseksi
(`> ol`), ettei sisennetty alalista saisi samaa numerointia.

**Aiheiden yhteenvedot olivat toinen puoli.** Kuudessa avattavassa lohkossa
yhteenveto ei ole yksi rivi vaan otsikko ja kappale:

```markdown
<details><summary>

### Kulujen seuranta

Tässä sovelluksessa käyttäjä voi seurata omia kulujaan ja menojaan.

</summary>
```

Avauspalkissa luki "### Kulujen seuranta Tässä sovelluksessa...". Kohdan 8
attribuutti ei auta tähän, koska se on `<details>`-tagissa eikä etene
`<summary>`:yn, ja `<summary>` on `md_in_html`:n `span_tags`-listalla — samassa
joukossa kuin `<p>` ja `<li>` — eli `markdown="1"` tarkoittaisi sille samaa kuin
`markdown="span"` ja otsikko jäisi yhä risuaidoiksi. Vain `markdown="block"`
pakottaa lohkojäsennyksen.

**Ehtona on tyhjä rivi, ei rivien määrä.** Aineistossa on kaksi yhteenvetoa,
joissa teksti jatkuu seuraavalle riville ilman tyhjää riviä
(`osa4/04-tyyppiparametrit-ja-geneerisyys.md`, `osa8/02-tableview.md`). Niissä ei
ole Markdownia, eikä kirjakaan jäsennä niitä: pulldown-cmark lopettaa raa'an
HTML-lohkon ensimmäiseen tyhjään riviin, ja ilman sitä koko yhteenveto menee läpi
sellaisenaan. Sama raja siis tänne — muuten `markdown="block"` olisi kääntänyt
niiden tekstin `<p>`:ksi ja tuonut avauspalkkiin kappaleen marginaalit. Ensimmäinen
versio muunnoksesta osui niihin, ja ne näkyivät ajossa heti: 8 yhteenvetoa,
kun sivulla piti olla 6.

Palkin tyyli tuli `admonitions.css`:ään, missä avattavien osioiden ilme jo on:
otsikon ylä- ja kappaleen alamarginaali pois (teema mitoittaa palkin yhdelle
riville) ja kuvaus takaisin normaalivahvuiseksi. Lihavointi jää otsikkoon:
palkin `font-weight: 700` on teeman ja yhden rivin yhteenvedoissa paikallaan,
mutta kokonainen kappale lihavoituna on raskas eikä erota otsikkoa mitenkään.

Todennettu neljällä tavalla:

- **Muunnokset osuivat siihen mihin pitikin:** ajossa 9 diviä ja 6 monirivistä
  yhteenvetoa, kaikki `harjoitustyo.md`:ssä. Kaikkiaan `docs/`:ssä on 347
  `markdown="1"`-diviä, joista 338 on tehtäväkorttien (kohta 6).
- **Käännöksen varoitukset eivät muuttuneet:** 16 ennen ja jälkeen.
- **Selaimessa:** kahdeksan vaatimuslohkoa piirtyy otsikoineen, listoineen ja
  koodijaksoineen, ja ensimmäisen kohdan numero on 1.1 kuten kirjassa. Oikean
  reunan sisällysluetteloon tuli 14 uutta riviä: kuusi aihetta ja kahdeksan
  vaatimusta, jotka olivat ennen tekstin sisällä.
- **Testit 91, ennen 82.** Uusia yhdeksän: seitsemän `test_convert.py`:hyn
  (yhteenvedon kolme tapausta ja divien neljä) ja kaksi `test_book.py`:hyn.
  Jälkimmäisistä ensimmäinen käy läpi koko kirjan tekstisolmut koodilohkot
  ohittaen eikä salli yhtäkään riviä, joka alkaa risuaidalla tai sisältää
  `**`-lihavoinnin — se on se testi, joka huomaa seuraavan attribuutittoman
  `<div>`:n tai `<summary>`:n aineistossa. Toinen kysyy laskuria
  (`counter-reset`, `counter-increment`, `::marker`), koska pelkkä
  `mkdocs.yml`:n unohtunut rivi numeroisi vaatimukset hiljaisesti uudelleen
  ykkösestä.

Mitä ei tullut: sivun kuusi `plantuml`-luokkakaaviota ovat yhä tekstilohkoja
(kohta 15) ja kymmenen bonustähteä näkymättömiä (kohta 17), eli sivulla on
tämän jälkeenkin kaksi tarkistuslistan avointa kohtaa. Rikki on myös yhä sivun
oma linkki `#harjoitustyön-tekniset-vaatimukset-ja-arviointi`, mutta se on
aineiston virhe ja rikki myös kirjassa (ks. `KNOWN_DEAD_ANCHORS`).

### Kaaviot: luokkakaaviot, ascii-kaaviot ja mermaid (uusi `assets/css/diagrams.css` + 1 rivi `mkdocs.yml`:ään + ~180 riviä `convert.py`:hyn)

Kolme eri kaaviolajia, kolme eri tilannetta. Yksi toimi jo, kaksi ei.

**Mermaid toimi ilman mitään.** Tarkistuslistalla luki "puuttuu", mutta se oli
väärä havainto: Zensicalin `pymdownx.superfences` on oletuksena määritelty niin,
että ```mermaid-aidasta tulee `<pre class="mermaid">`, ja teeman oma
JavaScript lataa mermaid 11:n ja piirtää kaavion. Tarkistus näytti tyhjältä
divistä, koska teema piirtää kaavion **suljettuun shadow rootiin**
(`attachShadow({mode:"closed"})`): DOM-kysely ei näe SVG:tä, vaikka se on
ruudulla. Kummatkin kaksi kaaviota piirtyvät, eikä `mkdocs.yml`:ään tarvittu
riviäkään. Yksi varaus: mermaid tulee unpkg.comista ajonaikaisesti, eli se on
ainoa kohta sivustolla, joka vaatii lukijalta verkkoa.

**Luokkakaaviot (17 kpl) haetaan PlantUML-palvelimelta käännöksessä.** Kirjassa
sen tekee `mdbook-plantuml` (`book.toml`: `plantuml-cmd`), joka lähettää
```plantuml-aidan sisällön palvelimelle ja tallettaa vastauksen tiedostoksi.
Sama tänne: kaavio pakataan osoitteeseen PlantUMLin omalla koodauksella (raaka
deflate ja base64 aakkostolla, jossa `+/`:n tilalla on `-_`), ja vastaus
talletetaan nimellä, joka on lähteen sha1. Nimet osuivat riville `book/`:n
kanssa — mdbook-plantuml laskee sha1:n samasta asiasta — eli tiedostot ovat
samat kuin kirjassa.

Ilman muunnosta sivulla oli 20 riviä `@startuml / class Kategoria { ... }`
siinä missä kirjassa on kaavio. Ero on isoin harjoitustyösivulla, jossa kaavio
on jokaisen aiheen tietomalli.

**Ascii-kaaviot (11 kpl) piirretään svgbobilla.** Piirtäjää ei ole Pythonille.
Sama piirtäjä on kuitenkin saatavana omana komentonaan:

```bash
cargo install svgbob_cli     # svgbob 0.7.6, sama kuin mdbook-svgbobin sisällä
```

Vaihtoehto olisi ollut ajaa `mdbook-svgbob`ia, joka on koneella jo kirjan takia
— se toimii, kokeiltiin — mutta se on mdBookin esikäsittelijä: sille pitäisi
rakentaa mdBookin oma JSON-sanoma, ja koeputken idea on päästä mdBookista eroon,
ei rakentaa sen protokollaa uudelleen.

**Kummankin riippuvuus on pehmeä.** Valmiit kaaviot ovat versionhallinnassa
(`assets/plantuml/`, 17 tiedostoa, 180 kt; `cache/svgbob/`, 11 tiedostoa, 76 kt),
joten käännös ei tarvitse verkkoa eikä svgbobia lainkaan: tavallinen ajo lukee
ne levyltä. Palvelimelle tai piirtäjälle mennään vain, kun kaavion lähde on
muuttunut tai uusi kaavio on lisätty, ja jos kumpaakaan ei saada, aita jätetään
ennalleen ja ajo varoittaa — käännös ei kaadu koneella, jolla ei ole kumpaakaan.
Käyttämättömät tiedostot siivotaan ajon lopuksi, jottei muokatun kaavion vanha
versio jäisi hakemistoon.

**Luokkakaavio on kuva, ascii-kaavio upotetaan.** Ero on värissä. PlantUMLin SVG
tuo omat värinsä palvelimelta (vaaleanvihreät laatikot, musta teksti, valkoinen
tausta) eikä niistä ole tummaa varianttia, joten se voi olla `<img>` — kuten
kirjassakin. Svgbobin SVG sen sijaan ottaa viivan ja tekstin värin
CSS-muuttujasta, ja `<img>`:n sisällä oleva SVG ei näe sivun muuttujia: siksi se
upotetaan sivulle sellaisenaan, jolloin kaavio seuraa teemanvaihtoa kuten
kirjassa (siellä muuttujat ovat `--fg` ja `--mono-font`, täällä
`--md-default-fg-color` ja `--md-code-font-family`). Siksi myös `cache/svgbob/`
on `assets/`:n ulkopuolella: se on välimuisti, ei julkaistava tiedosto.

Upottaminen vaati kolme asiaa, joista jokainen oli oma virheensä ennen kuin se
huomattiin:

* **Kääre on `<div>`.** `<svg>` ei ole Python-Markdownin
  `BLOCK_LEVEL_ELEMENTS`-listalla, joten paljas kaavio päätyi kappaleen sisään
  ja sen rivinvaihdot `<br />`-tageiksi.
* **Tyhjät rivit pois.** Svgbobin tyylilohkossa on tyhjiä rivejä, ja tyhjä rivi
  lopettaa raa'an HTML-lohkon: loppu kaaviosta olisi tullut sivulle tekstinä.
  Samasta syystä muunnos ajetaan `convert_divs`in **jälkeen** — muuten kääre
  olisi saanut `markdown="1"`:n ja `md_in_html` olisi jäsentänyt SVG:n
  Markdownina.
* **Tunnisteet omaan nimiavaruuteensa.** Svgbob kirjoittaa jokaiseen kaavioon
  samat viisi nuolenkärkimäärittelyä (`id="arrow"` ja neljä muuta) käytti kaavio
  niitä tai ei. Sivulla `osa6/02` kaavioita on neljä, eli sivulla oli 15
  kahteen kertaan esiintyvää tunnistetta ja `url(#arrow)` osoitti aina
  ensimmäiseen. Tunnisteet saavat siksi sivukohtaisen juoksevan etuliitteen
  (`bob1-arrow`), jonka päälle tulostussivulla tulee vielä `print.js`:n luvun
  oma etuliite. Tämän huomasi `test_identifiers_stay_unique`, joka oli
  paikallaan jo ennen tätä kohtaa.

`mkdocs.yml`:ään tuli yksi rivi: `assets/css/diagrams.css`. Siinä on kaksi
asiaa. Luokkakaavion valkoisesta pohjasta tehdään tarkoituksellinen — sama
valkoinen pehmusteeksi kuvan ympärille ja pyöristetyt kulmat — jolloin kaavio on
tummassa teemassa kortti eikä näytä siltä että sivun tausta vuotaa; vaaleassa
teemassa sääntö ei näy. Ascii-kaavio taas saa vierityksen: svgbobin SVG:ssä ei
ole viewBoxia, joten teeman `max-width: 100%` ei pienennä piirrosta vaan rajaa
sen reunan yli menevän osan pois — 400 px:n ikkunassa 736 px leveästä kaaviosta
jäi näkyviin 353 px. Rajoitus otetaan pois ja kääre vierittää, kuten teema tekee
leveille taulukoille.

Todennettu neljällä tavalla:

- **Ajossa 21 luokkakaaviota ja 12 ascii-kaaviota**, eli 17 ja 11 eri kaaviota:
  loput ovat tehtävänantoja, jotka `convert_includes` tuo useammalle sivulle.
  Yksi 12:sta on HTML-kommentin sisällä (`osa7/06`, aineistossa pois otettu
  osuus) — se piirtyy mutta ei näy, kuten muutkin muunnokset tekevät kommentin
  sisällä.
- **Käännöksen varoitukset eivät muuttuneet:** 16 ennen ja jälkeen.
- **Selaimessa:** luokkakaaviot piirtyvät samannäköisinä kuin kirjassa,
  ascii-kaaviot viivoina eivätkä `+---+`-merkkeinä, ja nuolenkärjet ovat
  paikallaan tunnisteiden etuliitteen jälkeenkin. Ascii-kaavio vaihtaa väriä
  teeman mukana; 400 px:n ikkunassa leveä kaavio vierii omassa laatikossaan
  eikä sivu itse vieri vaakasuunnassa.
- **Testit 101, ennen 91.** Uusia kymmenen: yhdeksän `test_convert.py`:hyn
  (koodauksen paluumatka, aita kuvaksi, kuvan osoite sivun syvyyden mukaan,
  palvelimeton ja piirtäjätön tapaus, sulkematon aita, kääre, tyhjät rivit,
  tunnisteet) ja yksi `test_book.py`:hyn: koko kirjan tulosteessa ei saa esiintyä sanaa
  `@startuml` — se esiintyy aineistossa vain aidan ensimmäisellä rivillä, joten
  näkyvissä se tarkoittaa kääntämättä jäänyttä kaaviota.

Mitä ei tullut: **mermaid ei piirry tulostussivulle.** Teema piirtää mermaidin
sivun latautuessa, ja `print.js` liittää luvut sivulle vasta sen jälkeen, joten
kirjan kahdesta mermaid-kaaviosta jää PDF:ään lähdeteksti. Luokkakaaviot ja
ascii-kaaviot tulostuvat oikein, koska ne ovat valmiina HTML:ssä.

### Java-ohjelmien ajonapit (uusi `assets/js/playground.js` + uusi `assets/css/playground.css` + 2 riviä `mkdocs.yml`:ään + 1 rivi `convert.py`:hyn)

Kirjan koodiesimerkit ovat ajettavia. mdBookissa jokainen ` ```java `-lohko,
jossa ei ole määrettä `ignore` eikä `noplayground`, saa oikeaan yläkulmaan
nuolinapin: se lähettää lohkon koodin JYU:n suorituspalvelimelle ja näyttää
tulosteen koodin alle (`theme/playground_ext.js`). Palvelin on sama ja pyyntö
kenttä kentältä sama, joten kirjan ohjelmat ajetaan täsmälleen kuten ennenkin:

```json
{ "language": "java", "code": "void main() { ... }", "multifile": false }
```

Tämä on kohdista se, jota teema ei voi antaa: koodin ajaminen ei ole teeman
ominaisuus vaan JYU:n oman palvelimen varassa. Kaikki muu kuin ajaminen tulee
silti teemalta.

* **Nappi** on teeman oma koodilohkon nappi (`nav.md-code__nav` >
  `button.md-code__button`, samat luokat kuin kopiointi- ja valintanapissa),
  joten paikka, koko, värit ja hover-käytös tulevat teeman CSS:stä. Nappirivin
  teema tekee itse vain, jos jompikumpi noista ominaisuuksista on päällä —
  kumpikaan ei ole — joten `playground.js` tekee rivin samannimisenä ja samaan
  paikkaan kuin teema sen tekisi (`pre`:n sisään ennen koodia). Jos napit joskus
  otetaan käyttöön, se käyttää valmista riviä eikä tee omaansa.
* **Tuloste** on tavallinen koodilohko (`div.highlight`), eli teema piirtää sen
  samalla taustalla, kirjasimella ja reunoilla kuin koodin, ja pitkä rivi vierii
  lohkon sisällä. Väli koodin ja tulosteen välillä on mitattuna 15 px,
  mdBookissa 10 px (`theme/css/chrome.css`: `pre > .result`). Toinen ajo korvaa
  saman lohkon tulosteen eikä kasvata sivua uudella laatikolla.
* **Monitiedostolohkon välilehdet** ovat teeman välilehtiä (kohta 5), joista
  koodit luetaan sellaisinaan.

Omaa CSS:ää on siksi vain kuvake, jota teemalla ei ole, ja kolme yksityiskohtaa:
odottavan napin himmennys, tyhjän tulosteen kursiivi (mdBookin
`.result-no-output`) ja nappirivin piilotus paperilta. Kokeiltu myös oma
marginaali tulosteelle — se ei tee mitään, koska koodilohkon oma alamarginaali
on suurempi.

**Monitiedostolohko ajetaan yhtenä ohjelmana**, kuten mdBookissa: kaikkien
välilehtien koodit lähtevät yhdessä hakemistona `{"main.java": "...",
"Valo.java": "..."}` ja `multifile: true`, ja tuloste tulee koko joukon alle
eikä yhden välilehden. Tieto siitä, mitkä välilehtijoukot ovat tiedostoja, ei
ole arvattavissa sivulta: samannäköisiä joukkoja ovat myös käyttöjärjestelmien
välilehdet (kohta 23), joissa jokainen lohko on oma ohjelmansa. Siksi merkintä
tehdään siellä, missä asia tiedetään — `convert_files` kirjoittaa jokaisen
tiedoston aitaan määreen `multifile`, joka päätyy luokaksi lohkon diviin. Se on
yksi rivi `convert.py`:hyn ja sama tapa kuin kohdassa 4: määre ei katoa vaan
muuttuu luokaksi.

**Piilorivit lähtevät ajoon siinä missä muutkin.** Aineiston ` ```java `
-lohkoista 97:ssä 231:stä on `//-`-alkuisia rivejä, joissa on ohjelman runko:
usein juuri `void main() {` ja sen sulkeva aaltosulje. Ne ovat lohkon HTML:ssä
tallessa, vaikka CSS piilottaa ne (kohta 2), eikä `textContent` välitä
näkyvyydestä — sama tapa kuin mdBookissa. Etuliite on riisuttu jo
käännösaikana, joten napin ei tarvitse tietää piiloriveistä mitään.

Todennettu selaimella koko kirjalla ja rinnakkain mdBookin kanssa:

- **338 nappia 65 sivulla.** Jokaisella ajettavalla lohkolla on tasan yksi
  nappi eikä yhdelläkään muulla ole nappia. Yksikään sivu ei tuottanut
  JavaScript-virhettä, ja konsoliin jäi vain kaksi tunnettua 404:ää samasta
  puuttuvasta kuvasta (`osa4/images/adventure.png`, ks. "Testit").
  Lähdepuun 231 aitaa (+ 1 javascript) kasvaa tähän kahdesta
  syystä: sisällytykset tuovat saman tehtävänannon monelle sivulle (kohta 1), ja
  yksi monitiedostoaita on sivulla monta lohkoa — 149 lohkoa 338:sta on 52
  monitiedostojoukon välilehtiä.
- **Sama sivu, sama määrä kuin mdBookissa:** `osa1/02-muuttujat-ja-tietotyypit`
  25 nappia molemmissa.
- **Sama tuloste kuin mdBookissa:** `osa1/02`:n piilorivinen lohko antaa
  molemmissa `korkokerroin = 0.05` ja `paaoma = 0.05`. `osa3/03`:n viiden
  tiedoston joukko ajettiin täällä ja tulosti `Valon kirkkaus on 50%.`,
  `Turvakameran tallennus on päällä.`, `Kahvinkeittimen pannu on päällä.`
- **Kestot palvelimelta mitattuna:** tuore ohjelma kääntyy ja ajetaan 2,5-3,4
  sekunnissa, sama koodi uudelleen 0,07 sekunnissa (palvelin muistaa tuloksen).
  Raja on mdBookin 6 s. Se pysyy mdBookin arvona, mutta ero on hyvä tietää:
  raskaampi ohjelma voi osua rajaan.
- **Paperilla** nappirivi on `display: none` ja tuloste jää näkyviin.

Kaksi eroa mdBookin koneistoon, molemmat tarkoituksellisia: nappi on ajon ajan
poissa käytöstä (mdBookissa saman ohjelman voi lähettää monta kertaa
peräkkäin), ja vastaamatta jäänyt pyyntö katkaistaan `AbortController`illa
(mdBook lopettaa odottamisen mutta jättää pyynnön käyntiin).

Erot mdBookiin, jotka jäävät:

* **Editoitavat lohkot eivät ole editoitavia** (kohta 20, 2 lohkoa): nappi ajaa
  sen koodin, joka sivulla lukee.
* **Kuvia tulosteessa ei tueta.** mdBookin `playground_ext.js` osaa poimia
  tulosteesta `@@@DATA_URI_BEGIN@@@`-merkinnät ja tehdä niistä kuvia. Ne
  liittyvät `feature-`-määreisiin lohkoihin, joita aineistossa ei ole yhtään, ja
  kokeiltuna palvelin ei palauttanut merkintöjä png-tiedoston kirjoittavalle
  ohjelmallekaan, joten koodia ei kirjoitettu tapaukseen jota ei ole.
* **Tulostussivulle ei tule ajonappeja.** `print.js` hakee luvut vasta sivun
  latauduttua, eikä paperille menevässä kirjassa ajonapista olisi hyötyä.
  (Silmänappi sen sijaan tulee, koska piilorivit on siellä joka tapauksessa
  piilotettava, ks. kohta 2.)
* **Napin tekstit ovat suomeksi** ("Suorita ohjelma", "Suoritetaan…", "Ei
  tulostetta"), koska sivuston kieli on suomi; mdBookissa ne ovat playgroundin
  englanninkielisiä oletuksia.

**Testit 120, ennen 107** (kohta 2 nosti luvun myöhemmin 134:ään). Uusia
kolmetoista: yksitoista uudessa `test_playground.py`:ssä ja kaksi
`test_convert.py`:hyn (monitiedostoaidan merkintä, ja se että kielettömästä
aidasta merkintä jää pois kielen mukana).
Uudet testit eivät kutsu suorituspalvelinta vaan vastaavat pyyntöön itse, eli
ne mittaavat sitä mitä selain lähettää ja mitä se vastauksesta näyttää — myös
tyhjän tulosteen, kääntäjän virheilmoituksen, katkenneen yhteyden ja
vastaamatta jäämisen. Koekirjaan tuli kolme lohkoa (ajettava lohko
piiloriveineen, `noplayground`-lohko ja ajettava monitiedostolohko), minkä takia
`test_print.py`:n välilehtijoukkojen määrä nousi kahdesta kolmeen.

### Piilorivit ja silmänappi (uusi `assets/js/hidelines.js` + uusi `assets/css/hidelines.css` + ~50 riviä `convert.py`:hyn + 2 riviä `mkdocs.yml`:ään + 4 riviä `print.js`:ään)

Kirjan koodiesimerkeissä on rivejä, jotka kuuluvat ohjelmaan muttei sivulle.
`//-`-alkuinen rivi on mdBookissa piilossa, ja lohkon silmänapista sen saa
esiin (`book.toml`: `[output.html.code.hidelines] java = "//-"`). Piilossa on
useimmiten juuri ohjelman runko — `void main() {` ja sen sulkeva aaltosulje —
jotta esimerkissä näkyisi vain se, mistä on kyse, mutta ajonappi (kohta 3)
saisi silti kokonaisen ohjelman. Mitattuna lähdepuussa **1103 riviä 135
lohkossa**; tarkistuslistan aiempi luku 1094 jätti laskematta yhdeksän riviä,
jotka ovat kolmessa alertin sisällä olevassa lohkossa.

Työ jakautuu kahtia samalla tavalla kuin mdBookissa:

* **`convert.py` (`hide_lines`)** riisuu etuliitteen ja kirjoittaa piilorivien
  numerot aidan attribuutiksi: ` ```{ .java data-hidden="1 7 8 9" } `.
  Etuliite lähtee jo käännöksessä kahdesta syystä. Rivi on ohjelmassa mukana,
  ja `//-` tekisi siitä kommentin — 97 lohkoa 231:stä ei kääntyisi. Ja korostus
  menisi väärin: koko rivi olisi Pygmentsille kommenttia, joten esiin otettuna
  se olisi harmaata kommenttitekstiä eikä koodia. mdBook tekee saman ennen
  korostusta ja kääri rivin `<span class="boring">`iin.
* **`assets/js/hidelines.js`** merkitsee numeroita vastaavat rivit, piilottaa ne
  ja lisää lohkoon silmänapin. Rivit ovat Pygmentsin rivispaneja (Zensicalin
  oletus `line_spans`), eli merkitseminen on `code`:n suorien span-lasten
  läpikäynti. Selain on ainoa paikka, jossa tämä voi tapahtua: Markdownissa ei
  ole tapaa merkitä yksittäistä koodiriviä, eikä CSS osaa valita riviä
  numerolistan perusteella.

Nappi on sama teeman nappi kuin ajonapissa ja samassa rivissä sen kanssa
(kirjassa ne ovat samassa `.buttons`-rivissä). Piilotus itse on kaksi
CSS-sääntöä: rivi on sivun HTML:ssä tallessa myös piilotettuna — ajonappi
lähettää sen ja kopiointi kopioisi sen — ja vain näkyminen on kiinni luokasta.
Esiin otettuna rivi jää himmeäksi (`opacity: 0.6`), kuten mdBookissa, jolloin
näkee mikä oli piilossa.

**Numerointi oli koko tehtävän ainoa mutka, ja se meni kahdesti pieleen ennen
kuin meni oikein.** Ensimmäinen versio numeroi aidan rungon sellaisenaan ja
tunnisti etuliitteen vain rivin alusta. Molemmat kaatuivat samaan kolmeen
lohkoon (`osa1/02`, alertin sisällä):

* Aita alkaa niissä kahdella tyhjällä rivillä, ja **Markdown pudottaa aidan
  alusta ja lopusta tyhjät rivit**. Numerot olivat siis kaksi liikaa, ja
  piilotus osui vääriin riveihin. Nyt numerot lasketaan siitä rungosta, joka
  lopulta piirretään.
* Lohkot ovat lainauslohkon sisällä, eli jokaisen rivin alussa on vielä ">"
  (`convert_alerts` purkaa lainauksen vasta myöhemmin). Etuliitteen tunnistus
  sallii nyt lainausmerkin ja kirjoittaa sen takaisin.

Kumpikin näkyi heti: yhdeksän `//-`-riviä jäi sivulle näkyviin ja kolmessa
lohkossa piilotus osui väärään riviin. Molemmat ovat nyt myös testeissä.

**Monitiedostolohkot käsittelee `convert_files`** omine aitoineen (kohta 5),
koska rivinumerot lasketaan sen aidan sisällä, jossa rivi lopulta on:
yhdeksässä monitiedostolohkossa on piilorivejä, ja niissä jokainen tiedosto saa
omat numeronsa.

**Tulostussivu tarvitsi oman kytkennän.** `print.js` hakee luvut vasta sivun
latauduttua, joten `hidelines.js` ei ole nähnyt niitä sivun latautuessa — ilman
mitään piilorivit tulostuisivat kirjan mukana. Kokoamisen jälkeen `print.js`
lähettää tapahtuman (`jyu-print-assembled`), jota `hidelines.js` kuuntelee;
kumpikaan ei tiedä toisestaan sen enempää. mdBookissa vastaavaa ei tarvita,
koska print.html on tavallinen sivu, jolla book.js ajetaan muiden tapaan.

Todennettu vertaamalla mdBookin omaan käännökseen ja selaimella:

- **Samat rivit piilossa kuin kirjassa.** 22:lla sivulla, joista on sekä
  mdBookin että Zensicalin versio, piilotettujen rivien joukot ovat 17 sivulla
  merkki merkiltä samat. Viidellä sivulla ero on yhdessä rivissä ja sekin
  pelkkää tyhjää: mdBook säilyttää rivin, jolla on vain välilyönti, Pygments
  siivoaa sen.
- **1103 riviä 142 lohkossa 24 sivulla**, ja jokaisessa lohkossa on silmänappi.
  Merkittyjä rivejä on tasan yhtä monta kuin numeroita, eikä yksikään numero
  osoita lohkon ulkopuolelle. Lähdepuun 135 lohkoa kasvaa 142:een, koska
  yhdeksän monitiedostolohkoa on sivulla kuutenatoista aitana.
- **Sivuilla ei näy enää yhtään `//-`-riviä**, ja käännöksen varoitukset
  pysyivät 16:ssa.
- **Selaimessa:** silmä näyttää rivit ja toinen painallus piilottaa ne, otsikko
  vaihtuu ("Näytä piilotetut rivit" / "Piilota rivit"), esiin otetut rivit ovat
  himmeitä ja korostettuja koodina — ja ajonappi lähettää saman ohjelman kuin
  ennenkin.
- **Aidan attribuutit 297 -> 389 aitaa.** Numerot saaneita aitoja on 142: 93
  ilman muita määreitä, 33 `ignore`-määreellä, 14 monitiedostolohkon
  tiedostoaitaa ja kaksi, joissa on molemmat. Uusiksi kirjoitettavien määrä
  kasvaa siis 92:lla eikä 93:lla, koska yhdessä lohkossa
  (`osa6/01-funktiorajapinnat...`) aidan otsikko on ` ```java, ` — tyhjä
  määrelista, joka on kirjoitettu uusiksi jo ennestään.

Yksi ero mdBookiin jää, ja se on sama molemmissa: **ilman JavaScriptiä rivit
näkyvät.** Kirjassa ne ovat silloin himmeinä, täällä tavallisina, koska luokan
lisää kummassakin skripti.

**Testit 134, ennen 120.** Uusia neljätoista: kahdeksan `test_convert.py`:hyn
(etuliitteen riisuminen, rivin loppu ennallaan, lainausmerkki, numerointi
piirretystä rungosta, kielet, aita ilman määreitä, valmiiseen aitaan ei
kosketa, monitiedostolohkon tiedostokohtaiset numerot), viisi uudessa
`test_hidelines.py`:ssä (rivit ovat sivulla muttei näkyvissä, oikeat rivit
merkittyinä, silmä näyttää ja piilottaa, silmä vain lohkoihin joissa on
piilorivejä, molemmat napit samassa rivissä) ja yksi `test_print.py`:hyn:
piilorivit eivät tulostu kirjan mukana.

### Koodin ja taulukoiden erottuminen taustasta (uusi `assets/css/code.css` + 1 rivi `mkdocs.yml`:ään + 1 rivi `tables.css`:ään)

Havainto halvalta paneelilta: taulukon viivoitus ja koodin tausta eivät erotu
taustasta. Mittaus vahvisti sen. Modern-variantin paleteissa

* taulukon reunus ja rivien väliviivat ovat tummassa teemassa
  `--md-typeset-table-color` eli 12 % valkoista, ja kun sivun tausta on lähes
  musta (`hsla(hue, 15%, 5%, 1)`), viiva on **1,32:1**;
* koodin tausta on molemmissa teemoissa **1,09:1** — vaaleassa `#f5f5f5`
  valkoisella (3,5 vaaleusyksikköä), tummassa `hsla(hue, 20%, 10%, 1)`
  (4,5 yksikköä).

Hyvällä näytöllä kaikki näkyvät, mutta jo kohtalainen katselukulma tai halpa
paneeli syö erot.

**Taulukon viiva .38 tekstin väriä** eli **3,01:1**, WCAG:n raja muulle kuin
tekstille. Se on tarkoituksella vahvempi kuin sivun muiden hiusviivojen
`--jyu-rule` (.20): se on sivun *rakenteen* viiva — yläpalkin alareuna,
alatunniste, `hr` — jota katsotaan sivun mittaista pintaa vasten, kun taas
taulukon ristikko on pieni kohde keskellä leipätekstiä. Muuttuja asetetaan
tauluun, ja teema käyttää sitä vain taulun reunuksessa ja solujen
`border-topissa`, joten ylikirjoitus ei vuoda muualle. Vain tummaan teemaan:
vaaleassa sama 12 % on mustaa valkoisella eli selvästi jyrkempi ero.

**Koodissa työ tehdään pelkällä taustalla.** Lohkon rajaava hiusviiva olisi
kontrastina tehokkaampi, ja se kokeiltiin, mutta laatikko jokaisen
koodinpätkän ympärillä on levottomampi kuin pinta.

**Pieni kohde tarvitsee suuremman eron kuin iso**, ja siitä seuraa kohtien
jako: koko palstan levyinen lohko erottuu vaalealla taustalla vielä 3,5
vaaleusyksiköllä, mutta muutaman merkin nappula keskellä riviä ei.

* **Rivitekstin koodi, molemmat teemat: teeman oman tekstivärin peitto,
  vaaleassa 10 % ja tummassa 20 %.** Peitto ei kasaudu teeman
  `--md-code-bg-colorin` päälle vaan korvaa sen — `background-color` on yksi
  ominaisuus, ei pino — joten läpinäkyvä sävy sekoittuu siihen, mitä nappulan
  takana on. Juuri sitä tarvitaan, koska rivitekstin koodia on myös
  alerttilaatikoissa, taulukoissa ja tehtäväkorteissa, joiden tausta on eri.
  Arvot ovat eri, vaikka mitattu vaalausero olisi samalla luvulla lähes sama
  (20 % olisi vaaleassa -16,5 ja tummassa +16,2 yksikköä): vaalealla pohjalla
  silmä erottaa saman eron selvästi helpommin, koska se on sopeutunut
  kirkkaampaan pintaan, ja 20 % näyttää siellä raskaalta harmaalta laatikolta.
  Vaalean 10 % on `#e8e8e8` eli -8,2 yksikköä, reilu kaksinkertainen ero
  teeman omaan `#f5f5f5`:een. Koodin oma teksti on nappulaa vasten 8,0:1
  (vaalea) ja 7,9:1 (tumma). Merkeissä on lisäksi kohokuviointi
  (`text-shadow: 0 1px`) taustan suuntaisella värillä — vaaleassa valkoinen,
  tummassa musta — joka terävöittää reunan nappulaa vasten. Ilman sumennusta,
  jottei pieni kirjasin mene utuiseksi.
* **Lohkon tausta, vain tumma teema: 10 % -> 18 %.** Kattona ovat kommentit,
  operaattorit ja välimerkit, jotka teema piirtää
  `--md-default-fg-color--lightillä`: se on nykytaustalla 5,16:1 ja putoaa
  taustan noustessa. 18 % on suurin arvo, jolla ne ovat vielä yli WCAG AA:n
  (4,62:1), ja ero sivun taustaan kolminkertaistuu (4,5 -> 13,6
  vaaleusyksikköä). Kaikki kolme muuttujaa (`--md-code-bg-color` ja sen
  `--light`/`--lighter`) nostetaan yhdessä, koska jälkimmäiset ovat nappirivin
  (`.md-code__nav`) tausta, joka kelluu lohkon päällä — pelkkä perusarvo olisi
  jättänyt nappirivin lohkoa tummemmaksi läiskäksi.

Todennettu selaimessa molemmissa teemoissa: taulukon viivat, Java-lohko
syntaksiväreineen, ajon tuloste ja rivitekstin nappulat erottuvat. Testit 136
läpi, käännöksen varoitukset 16 ennen ja jälkeen.

Mitä ei tullut: `--jyu-rulen` nostoa. Sivun rakenteen viivat ovat tummalla
taustalla 1,64:1, eli sama havainto koskee niitäkin, mutta ne ovat pitkiä
yhtenäisiä viivoja isoa tyhjää vasten eivätkä olleet valituksen kohteena.
Vaalean teeman koodilohko jäi myös ennalleen samasta syystä kuin nappula
korjattiin: iso pinta erottuu pienemmälläkin erolla.

### Nappirivi: ajonappi ja silmä napin näköisiksi (uusi `assets/css/codebuttons.css` + 1 rivi `mkdocs.yml`:ään + 4 riviä `playground.css`:ään)

Kaksi havaintoa peräkkäin: ajonappi ja silmä ovat liian himmeitä eivätkä erotu
koodilohkosta, ja kun ne saa näkyviin, ne eivät silti näytä napeilta, joita
tekisi mieli painaa.

**Himmeys on teeman oletus.** Nappirivin kuvakkeet piirretään levossa
`--md-default-fg-color--lightestillä`, ja teema nostaa ne `--lightiin` vasta kun
osoitin on lohkon päällä (`:hover > * > .md-code__button`). Lepotila on
koodilohkon taustaa vasten **1,12:1** (vaalea) ja **1,38:1** (tumma) eli
käytännössä näkymätön: kuvakkeen muodon näkee vain, jos tietää etsivänsä sitä.

Se on oikea valinta *kopiointinapille*: se on mukavuus, jonka paikan tuntee
entuudestaan, ja piilossa se pitää koodilohkon rauhallisena. Ajonappi ja silmä
eivät ole sitä. Ne ovat kirjan omia toimintoja, joita lukija ei osaa etsiä
hoverin takaa — eikä kosketusnäytöllä ole hoveria lainkaan, joten siellä himmeä
lepotila on ainoa tila, joka koskaan näkyy.

**Kuvakkeesta laataksi.** Pelkkä värin nosto olisi korjannut näkyvyyden muttei
painettavuutta: paljas kuvake koodilohkon nurkassa on yhtä hyvin koriste kuin
nappi. Napille annetaan siksi oma pinta, hiusviivareunus, pyöristys ja varjo.

* **Pinta on molemmissa teemoissa lohkoa vaaleampi**, koska ylöspäin osoittava
  pinta ottaa valoa — vaaleassa valkoinen lohkon `#f5f5f5`:tä vasten, tummassa
  26 % lohkon 18 %:aa vasten. Kuvake on omaa pintaansa vasten **5,74:1**
  (vaalea) ja **4,41:1** (tumma), eli reilusti yli WCAG:n 3:1:n muulle kuin
  tekstille. Lepoväri on `--md-default-fg-color--light`, sama jonka teema antaa
  lohkon päällä; uutta sävyä ei keksitä.
* **Reunus on sama `--jyu-rule`** kuin sivun muissa rajoissa
  (`assets/css/layout.css`). Laatan oma pinta erottuu lohkosta vaaleassa vain
  1,09:1 — valkoinen `#f5f5f5`:tä vasten on hiuksenhieno — joten reunus ja varjo
  tekevät siellä suurimman osan työstä. Tummassa pinta erottuu 1,31:1 ja reunus
  2,21:1.
* **Nappirivin oma tausta pois.** Se on olemassa siksi, että paljaat kuvakkeet
  erottuisivat allaan juoksevasta koodista; nappien omat pinnat tekevät sen nyt
  paremmin, eikä laatikkoa laatikon sisään tarvita.

**Liike tekee lopun.** Kohdistuksessa laatta nousee 1 px, varjo kasvaa ja
aksenttiväri tulee kuvakkeeseen, reunukseen ja 8 %:n verran pintaan.
Painettaessa laatta painuu saman verran alas ja varjo katoaa — ylös, alas, ja
liikkeestä tulee napsahdus. Nosto ja painallus ovat teeman `.25 s`:ää
nopeammat (`.1 s` ja `.05 s`), koska hidas liu'utus tuntuu vetelältä.
`prefers-reduced-motion: reduce` jättää värit ja pudottaa liikkeen pois.

Silmällä on lisäksi **päällä-tila** (`aria-pressed="true"`): kun piilorivit ovat
näkyvissä, laatta on painettuna pohjaan ja aksenttivärissä. Ilman sitä ainoa
merkki tilasta olisi kuvakkeen vaihtuminen yliviivatuksi silmäksi.

**Pois käytöstä oleva nappi ei saa näyttää painettavalta.** Ajon ajaksi
ajonappi himmennetään (`playground.css`), ja nosto ja painallus jäävät pois
`codebuttons.css`:n `:not(:disabled)`-ehdoista. Väri on silti pakko palauttaa
erikseen: selain antaa `:hoverin` myös `disabled`-napille, joten teeman oma
`.md-code__button:hover` värittäisi odottavan napin aksenttivärillä. Neljä
riviä `playground.css`:ään, samaan kohtaan jossa himmennys jo oli.

Sääntöt ovat omassa tiedostossaan eivätkä `playground.css`:ssä tai
`hidelines.css`:ssä, koska ne koskevat riviä eivätkä yksittäistä nappia: saman
`.md-code__navin` napit on piirrettävä samannäköisiksi. Ne kaksi tiedostoa
antavat kumpikin vain oman kuvakkeensa, `codebuttons.css` antaa napin. Jos
teeman kopiointinappi joskus kytketään päälle (`content.code.copy`, ks.
tarkistuslista), se saa saman ulkoasun ilman lisätyötä.

Luvut on mitattu piirretyistä pikseleistä eikä laskettu paletin alfoista, koska
modern-variantin efektiiviset arvot eivät ole samat kuin teeman perus-CSS:n:
`--md-default-fg-color--light` on vaaleassa 0,6 mustaa ja tummassa 0,62
valkoista, ei 0,55/0,56 kuten `main.css` antaa ymmärtää.

Todennettu selaimessa molemmissa teemoissa: lepo, kohdistus, painallus, silmän
päällä-tila ja ajonapin odotustila. Testit 136 läpi, käännöksen varoitukset 16
ennen ja jälkeen.

Mitä ei tullut: aksenttiväristä ajonappia levossa. Vihreä tai sininen kolmio
joka Java-lohkossa olisi vahvin mahdollinen kutsu, ja niitä lohkoja on 231 —
sivu täyttyisi väristä. Neutraali laatta, joka värittyy vasta kosketuksesta,
kutsuu riittävästi ja pitää koodin pääosassa.


### Korostetut rivit (uusi `assets/js/highlights.js` + uusi `assets/css/highlights.css` + ~90 riviä `convert.py`:hyn + 2 riviä `mkdocs.yml`:ään)

Kirjan koodiesimerkeissä osa riveistä on väritetty: vihreä on se, mikä lisättiin
tai on oikein, punainen se, mikä on väärin, keltainen se, mihin kannattaa
katsoa. Merkintä on koodin sisällä kommenttiparina
(`// HIGHLIGHT_GREEN_BEGIN` ... `// HIGHLIGHT_GREEN_END`), ja mdBookissa
`theme/code-highlights.js` poistaa merkinnät ja värittää väliin jääneet rivit.
Mitattuna lähdepuussa **120 aluetta 76 lohkossa 24 sivulla**: vihreä 81,
punainen 20, keltainen 19. Ennen tätä merkinnät näkyivät sivuilla sellaisinaan,
eli 240 riviä kirjan koodia oli rivejä, joita kirjassa ei ole.

Työ jakautuu kolmeen osaan, kaksi ensimmäistä samalla tavalla kuin
piiloriveillä (kohta 2):

* **`convert.py` (`mark_highlights`)** poistaa merkintärivit ja kirjoittaa
  väliin jääneiden rivien numerot aidan attribuutiksi väreittäin:
  ` ```{ .java data-hl-green="2 3" } `. Merkinnät lähtevät jo käännöksessä,
  koska rivi lähtee ajoon sellaisenaan (kohta 3) ja mdBook riisuu ne niin ikään
  ennen korostusta.
* **`assets/js/highlights.js`** lisää numeroita vastaaville riveille luokan.
  Rivit ovat Pygmentsin rivispaneja, eli sama tie kuin piiloriveillä ja samasta
  syystä: Markdownissa ei ole tapaa merkitä yksittäistä koodiriviä. Selaimen
  osuus on tässä paljon pienempi kuin kirjassa — mdBookissa rivejä ei ole
  elementteinä, joten skripti ajaa korostuksen uudestaan, pilkkoo hljs:n
  tuottaman HTML:n riveiksi ja sulkee ja avaa kesken rivin jäävät spanit itse.
* **`assets/css/highlights.css`** värittää ne.

**Merkinnät ennen piilorivejä.** Molemmat numeroivat rivit, ja merkintärivit
lähtevät rungosta pois, joten piilorivien numerot on laskettava vasta sen
jälkeen — muuten jokainen alueen jälkeinen piilorivi olisi kahden verran
väärässä paikassa. Monitiedostolohkot käsittelee `convert_files` omine
aitoineen kuten piiloriveillä: kahdessatoista niistä on korostuksia, ja
jokainen tiedosto saa omat numeronsa.

**Värit ovat tämän kohdan koko työ, ja ne on tehty toisin kuin kirjassa.**
Kirjassa korostus on peittoväri koodin päällä (vihreä 42 %, keltainen 40 %,
punainen 42 %). Sitä ei voi kopioida sellaisenaan, koska teemojen
syntaksivärit ovat eri paikassa: Zensicalin modern-variantissa koodin
syntaksivärit ovat heikoimmillaan koodin taustaa vasten **4,5:1** (vaaleassa
4,52, tummassa 4,49), eli tasan WCAG AA:n rajalla, kun mdBookin omissa
väriteemoissa on varaa. Kirjan peitto pudottaisi ne täällä vaaleassa teemassa
3,2-4,1:een ja tummassa 2,1-3,7:ään. Korostettu rivi on
juuri se rivi, jota luetaan tarkimmin, joten sitä ei haluta lukea sivun
heikoimmalla kontrastilla.

Väri otetaan siksi toisesta suunnasta: **kirkkaus pidetään, värisävy vaihtuu.**
Kontrasti riippuu vain kirkkaudesta, joten sävyn ja kylläisyyden muutos on
ilmainen. Mitattuna koodin taustaa vasten (CIELAB):

| väri      | teema  | ero taustaan | kirkkausero | heikoin syntaksiväri |
| --------- | ------ | ------------ | ----------- | -------------------- |
| vihreä    | vaalea | dE 21,5      | -2,1        | 4,29:1               |
| keltainen | vaalea | dE 25,7      | -1,5        | 4,36:1               |
| punainen  | vaalea | dE 12,1      | -5,2        | 3,96:1               |
| vihreä    | tumma  | dE 35,6      | -0,5        | 4,55:1               |
| keltainen | tumma  | dE 30,4      | -0,2        | 4,52:1               |
| punainen  | tumma  | dE 36,2      | -1,9        | 4,57:1               |

Kirjan omat palkit ovat vaaleassa teemassa dE 22-26, eli vihreä ja keltainen
ovat tässä yhtä erottuvia kuin kirjassa mutta ilman kirjan 8-12
kirkkausyksikön pudotusta. Tummassa teemassa ero on kirjaa suurempi eikä maksa
mitään: siellä syntaksivärit ovat korostetulla rivillä samat 4,5:1 kuin
muuallakin.

**Punainen on vaalean teeman ainoa mutka.** Vaalealla pinnalla ei ole kylläistä
punaista, joten sen on pakko tummua näkyäkseen; 5,2 yksikköä on se, minkä
jälkeen syntaksivärit ovat vielä 4,0:1. Se on sama luku, jolla teema itse
korostaa rivin (`hl_lines`: -4,1 yksikköä ja 4,07:1), eli korostettu rivi ei
ole täällä huonompi kuin teeman omassa korostuksessa.

**Rivin vasempaan reunaan tulee lisäksi 2 pikselin palkki täydessä värissä**,
kuten teeman omassa korostuksessa. Se on toinen merkki värin rinnalle: sävy
yksin erottuu huonosti puna-vihersokealle, ja juuri se pari kirjassa merkitsee
oikean ja väärän tavan. Palkki on taustaansa vasten 3,5-5,6:1. Ero ei silti
katoa: väri on kirjan tapaan ainoa tapa erottaa vihreä punaisesta, eikä sitä
korjata kirjaa muuttamatta.

**Väri ulottuu lohkon reunasta reunaan**, myös silloin kun rivi on lohkoa
pidempi ja lohkoa vieritetään. Kirjassa se vaatii JavaScriptiä: skripti mittaa
lohkon leveyden ja vaihtaa `<code>`:n inline-blockiksi, jos sisältö ei mahdu.
Täällä riittää CSS — rivi on enintään oman sisältönsä levyinen (`max-content`)
ja vähintään lohkon levyinen. Jälkimmäisessä on mukana rivin oma sisennys
(`calc(100% + 2.5em)`), koska laatikkomalli on border-box: pelkkä 100 % jättäisi
rivin oikean reunan sisennyksen verran vajaaksi. Se oli tämän kohdan ainoa
mittaamalla löytynyt virhe, ja se on nyt testissä.

**`highlights.css` on `mkdocs.yml`:ssä ennen `hidelines.css`:ää.** Korostettu
rivi on lohkotason elementti ja piilotettu rivi `display: none`; valitsimet ovat
yhtä tarkkoja, joten piilotus voittaa vain myöhempänä. Ilman järjestystä
piilorivi, joka on korostetulla alueella, jäisi sivulle näkyviin —
aineistossa niitä on kolmessa lohkossa. Esiin otettuna sellainen rivi on
himmeä ja värillinen, kuten kirjassakin.

**Tulostussivu ei tarvinnut mitään uutta.** `print.js` lähettää kokoamisen
jälkeen tapahtuman (`jyu-print-assembled`), jota `hidelines.js` jo kuunteli;
`highlights.js` kuuntelee samaa. Kumpikaan ei tiedä toisestaan eikä print.js
kummastakaan.

Todennettu vertaamalla mdBookin omaan käännökseen ja selaimella:

- **Samat rivit korostettuina kuin kirjassa.** 22:lla sivulla, joista on sekä
  mdBookin että Zensicalin versio, korostettujen rivien joukot ovat merkki
  merkiltä samat: **348 riviä, ei yhtään eroa kummallakaan puolella**. Kaksi
  jäljelle jäävää sivua (`extra/luetelma-ja-hahmonsovitus`, `osa4/jemma`) eivät
  ole `SUMMARY.md`:ssä, joten mdBookin käännöksessä ei ole niitä lainkaan.
- **374 riviä 79 aidassa 24 sivulla**, ja jokainen numero osuu lohkon riviin.
  Lähdepuun 76 lohkoa kasvaa 79:ään, koska kaksitoista monitiedostolohkoa on
  sivulla useampana aitana. Aidan attribuutit 389 -> 392: uusiksi kirjoitettavia
  aitoja tulee vain kolme lisää, koska korostetuissa lohkoissa on lähes aina jo
  jokin määre (`ignore`) tai piilorivejä.
- **Sivuilla ei näy enää yhtään `HIGHLIGHT_`-riviä**, ja käännöksen varoitukset
  pysyivät 16:ssa.
- **Selaimessa molemmissa teemoissa:** vihreä, punainen ja keltainen erottuvat,
  koodi on niiden päällä luettavaa, palkki näkyy rivin reunassa, pitkän rivin
  väri jatkuu vieritettäessä, ja ajonappi lähettää saman ohjelman kuin ennen
  (merkinnät eivät koskaan päädy suoritettavaan koodiin).

Mitä ei tullut: **sinistä**, jonka kirjan CSS tuntee neljäntenä värinä. Sitä ei
ole aineistossa yhtään aluetta. Se on kolme riviä CSS:ää, jos sellainen tulee.
Ja kuten kirjassa: **ilman JavaScriptiä rivit ovat värittömiä**, koska luokan
lisää kummassakin skripti.

**Testit 154, ennen 136.** Uusia kahdeksantoista: kymmenen `test_convert.py`:hyn
(merkintöjen poisto ja numerointi, kirjoitusasujen sietäminen, numerointi
piirretystä rungosta, useat alueet ja värit, kielirajaus, varoitus
tuntemattomasta väristä, attribuutit aidassa, aita ilman muita määreitä,
piilorivien numerointi merkintöjen jälkeen, monitiedostolohkon
tiedostokohtaiset numerot), kuusi uudessa
`test_highlights.py`:ssä (merkinnät poissa sivulta, oikeat rivit merkittyinä,
väri tulee tyylitiedostosta, väri reunasta reunaan, korostettu piilorivi pysyy
piilossa ja tulee esiin himmeänä, monitiedostolohkon tiedostot omine
numeroineen), yksi `test_print.py`:hyn (korostukset tulostuvat kirjan mukana) ja
yksi `test_book.py`:hyn (koko kirjassa ei ole yhtään merkintää jäljellä eikä
yhtään numeroa lohkon ulkopuolella).


## Mitattu ensimmäisestä ajosta

Rakennus kestää **16 s** (MkDocs + Material samasta sisällöstä: 31 s) ja
tuottaa **53 varoitusta**: 49 × "anchor does not exist", 4 × "page does not
exist". Kertyminen: `tyokalut.md` 20, `osa8/06-versionhallinnan-etakaytto.md`
9, `osa1/01-hei-java.md` 7. Suurin osa on mdBookin `#tab/...`-ankkureita ja
ääkkösellisiä ankkureita — nämä liittyvät listan kohtiin 13 ja 14.

Ilman mitään konfiguraatiota toimivat jo: Pygments-syntaksiväritys
(`language-java highlight`), oikean reunan sisällysluettelo, haku suomeksi ja
kokoontaittuva navigaatio. (Ensimmäisessä ajossa listalla oli myös
edellinen/seuraava-linkit — ne olivat väärä havainto: Zensicalissa on niitä
varten `navigation.footer`, mutta se on oletuksena pois päältä.)


## Avoin kysymys: muunnosaskel pois työnkulusta

Kun koeputkesta tulee oikea alusta, jäljelle jää yksi ratkaisematon kohta:
**`convert.py` on erillinen komento, joka on ajettava joka kerta.**
`zensical serve` seuraa `docs/`-hakemistoa, jonka `convert.py` kirjoittaa, ei
lähdepuuta `../src`, joten kesken kirjoittamisen tehty muutos ei näy selaimessa
ennen uutta ajoa. Kolme tapaa päästä siitä eroon, järjestyksessä huonoimmasta
parhaimpaan:

**A. Lähde pysyy mdBookin syntaksina, `convert.py` jää ja sen ympärille
tehdään vahti.** Halvin: `run.sh`:hyn silmukka, joka ajaa `convert.py`:n kun
`../src` muuttuu. Käännösaskel on silloin olemassa muttei näy käsityönä.

**B. Käännetään kerran ja `docs/` committoidaan uudeksi lähdepuuksi.** Ei
enää muunnoksia lainkaan, mutta hinta on kohtuuton juuri niissä kohdissa,
jotka on tässä tehty: kirjoittaisit käsin ` ```{ .java data-hidden="1 3"
data-hl-green="2" } ` ja laskisit rivinumerot itse — ja numeroisit ne
uudelleen joka kerta kun lisäät rivin lohkon alkuun. Merkintäpari
`// HIGHLIGHT_GREEN_BEGIN` on olemassa juuri siksi, ettei numeroita tarvitse
kirjoittaa. Sama koskee piilorivejä (kohta 2) ja monitiedostolohkoja
(kohta 5).

**C. Sivukohtaiset muunnokset siirretään Python-Markdown-laajennukseksi.**
Silloin merkinnät käännetään sivua renderöitäessä: ei erillistä komentoa, ei
`docs/`-kopiota, ja `serve` seuraa suoraan lähdettä. Kirjoittaja kirjoittaa
edelleen `// HIGHLIGHT_GREEN_BEGIN`, ja rivinumerot lasketaan joka
renderöinnillä uudelleen.

Tie C:hen on tarkistettu Zensicalin koodista: **yleistä plugin-rajapintaa
ei ole** (`config.py` osaa vain kovakoodatun listan tunnettuja MkDocs-plugineja,
eikä MkDocsin `hooks:`-avainta tueta lainkaan), mutta `markdown_extensions`
menee sellaisenaan Python-Markdownille (`zensical/markdown/render.py`), joten
oma laajennus latautuu nimellä:

```yaml
markdown_extensions:
  - ohj2.highlights
```

Laajennuksen on oltava .venv:stä importattavissa. Muunnokset ovat
esikäsittelijöitä (`Preprocessor`), koska ne katsovat raakoja rivejä ennen
jäsennystä — samaa työtä kuin `mark_highlights` ja `hide_lines` tekevät nyt.

**Kaikkea ei voi siirtää.** Navigaatio (`SUMMARY.md` -> `nav.yml`),
tulostussivun runko, PlantUML-kuvien haku ja `NEST_UNDER`-siirrot ovat koko
kirjan tason työtä, eivät yhden sivun Markdownia, joten pieni käännösaskel jää
sittenkin — mutta se ajetaan vain kun rakenne muuttuu, ei jokaisen
tekstimuutoksen jälkeen.

**Ratkaisevaa on yksi vielä mittaamaton luku: kauanko tallennuksesta kuluu
selaimen päivittymiseen**, kun `zensical serve` huomaa muutoksen. Jos se on
sekunnin luokkaa, A riittää. Jos se on kymmeniä sekunteja, C on perusteltu,
koska silloin käännettävää on vain muuttunut sivu. Mittaus: käynnistä serveri,
muuta `docs/`:n sivua ja katso, montako sekuntia kuluu ennen kuin muutos näkyy
osoitteessa. Vertailuluvut: koko kirjan käännös kylmänä 24 s ja muuttumattomana
14 s.

**Ympäristö on tämän mittauksen edellytys.** Tiedostovahti (inotify) ei saa
tapahtumia lainkaan, jos repo on Windowsin levyllä 9p-liitoksen takana
(`/workspaces/...` bind-mountina): mitattuna sama koe antoi siellä nolla
tapahtumaa ja ext4:llä tapahtumat normaalisti. Repo kuuluu siis Linuxin
tiedostojärjestelmään — devcontainerin volumeen tai WSL:n omaan hakemistoon —
tai `serve` ei reagoi tallennuksiin, olipa muunnokset tehty kummalla tavalla
tahansa.

**Sivuston hakemistorakenne** ratkeaa samalla. Zensicalin oma konventio on
`docs/` konfiguraatiotiedoston vieressä, mutta `docs_dir` on pelkkä asetus:
`docs_dir: src` säilyttää sivujen sisäiset linkit, kuvapolut, `edit_uri`:n ja
Gitin historian koskemattomina. Assetit (`zensical/assets/`) muuttavat silloin
`docs_dir`:in sisään, koska `extra_css` ja `extra_javascript` ovat suhteessa
siihen; polut `mkdocs.yml`:ssä ovat jo valmiiksi siinä muodossa.
