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
./zensical/run.sh test                        # kaikki, 59 testiä
./zensical/run.sh test tests/test_convert.py  # pelkät muunnokset, 0,2 s
./zensical/run.sh test --nobuild              # käytä olemassa olevaa site/:ä
```

Ensimmäisellä kerralla asentuvat `pytest`, `playwright` ja sen chromium
(`requirements-dev.txt`); sivuston rakentamiseen riittää yhä pelkkä
`zensical`.

Kerroksia on kolme, koska rikkoutumisia on kolmea lajia:

| Tiedosto                | Mitä                                                          | Kesto      |
| ----------------------- | ------------------------------------------------------------- | ---------- |
| `tests/test_convert.py` | `convert.py`:n muunnokset yksin: ei käännöstä eikä selainta   | 0,2 s      |
| `tests/test_print.py`   | tulostussivun kokoaminen selaimessa, koekirjalla              | 6 s        |
| `tests/test_change.py`  | koekirjan materiaalia muutetaan: näkyykö muutos tulosteessa   | 25 s       |
| `tests/test_book.py`    | sama oikealla materiaalilla, 72 lukua                          | 10 s       |

Mitään ei jäljitellä: testit ajavat `convert.py`:n ja `zensical build`in
oikeasti ja avaavat sivun oikeassa selaimessa. Tulostussivu on koeputken
ainoa kohta, jossa lopputulos syntyy vasta selaimessa — `print.js` hakee
jokaisen luvun oman sivun ja liittää siitä artikkelin — joten käännöksen
tuloksesta sitä ei voi lukea.

**Koekirja (`tests/book/src`) on kymmenen tiedostoa.** Se on olemassa kahdesta
syystä. Ensinnäkin materiaalin muuttamista pitää päästä *kokeilemaan*, eikä
sitä voi tehdä `../src`:ään; koekirjasta jokainen testi saa oman kopionsa,
jota se saa rikkoa. Toiseksi se on nopea: koko kirjan kääntäminen kestää
50 s, koekirjan 3 s. Siinä on yksi esimerkki jokaisesta asiasta, joka
kokoamisessa voi mennä rikki — sama otsikko kahdessa luvussa, kuva
alihakemistosta, sivun sisäinen ankkuri, lukujen välinen linkki, kaksi
välilehtijoukkoa, `NEST_UNDER`-siirto ja ulkoinen linkki.

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
vaan havaintoja. Sisältöä muunnetaan toistaiseksi neljässä kohdassa
(sisällytykset ja välilehdet, ks. kohdat 1, 4, 5 ja 23); jokainen uusi muunnos
kuuluu perustella samalla tavalla kuin muutkin rivit.

Aiempi, täysin viritetty versio on tallessa branchissa `spike/mkdocs`
(siellä hakemisto on nimeltään `mkdocs-spike/`):
sieltä saa jokaisen palasen takaisin, kun se on ensin todettu tarpeelliseksi.

## Tarkistuslista

Käydään läpi yksi kerrallaan. Jokaiselle kolme kysymystä: mitä mdBook teki,
näyttääkö Zensical sen jo itse, ja tarvitaanko sitä oikeasti.

| #  | mdBookin ominaisuus                          | Esiintymiä                | Tila nyt                                                                                                           |
| -- | -------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1  | `{{#include tiedosto}}`                      | 194                       | **tehty** — `convert_includes`; 4 makroa jää näkyviin, kohde puuttuu aineistosta                                   |
| 2  | `//-` piilorivit                             | 1094                      | rikki — rivit näkyvät                                                                                              |
| 3  | ` ```java ` ajonappi (playground)            | 231                       | puuttuu — `.ignore`/`.noplayground` säilyy nyt luokkana, ks. kohta 4                                               |
| 4  | ` ```java,ignore` / `,noplayground`          | 289                       | **tehty** — attribuutit luokiksi (`{ .java .ignore }`), korostus palasi                                            |
| 5  | `// FILE:` monitiedostolohkot                | 73 lohkoa / 194 tiedostoa | **tehty** — `pymdownx.tabbed`, tiedosto per välilehti                                                              |
| 6  | `<task>` / `<points>` / `<handout>`          | 507                       | rikki — 501 tagia menee HTML:ään tyylittöminä                                                                      |
| 7  | `> [!VINKKI]`-tyyliset alertit               | 75                        | rikki — näkyy lainauksena                                                                                          |
| 8  | `<details>`-lohkot                           | 88                        | puolittain — lohko aukeaa (72 kpl HTML:ssä), mutta sisältö jää Markdowniksi: 21:ssä raakoja linkkejä, ks. kohta 23 |
| 9  | `HIGHLIGHT_*_BEGIN/END`                      | 120                       | rikki — merkinnät näkyvät                                                                                          |
| 10 | Lukujen numerointi navigaatiossa             | koko nav                  | **tehty** — `convert.py`, 12 riviä                                                                                 |
| 11 | Osan etusivu = osan oma linkki navissa       | 13 osaa                   | **tehty** — `navigation.indexes`                                                                                   |
| 12 | Otsikoiden numerointi sivun sisällä          | —                         | ei ollut mdBookissakaan                                                                                            |
| 13 | Ääkköset ankkureissa (`#käyttö`)             | —                         | riisutaan (`#kaytto`)                                                                                              |
| 14 | `.html`-päätteiset osoitteet (TIM)           | —                         | puuttuu — nyt hakemistopolut                                                                                       |
| 15 | plantuml / bob / mermaid                     | 17 / 8 / 2                | rikki / rikki / puuttuu                                                                                            |
| 16 | `<asciinema>`-upotukset                      | 13                        | rikki                                                                                                              |
| 17 | Bootstrap-ikonit `<i class="bi ...">`        | 136                       | puuttuu — ei fonttia                                                                                               |
| 18 | JYU-paletti, kultainen korostus              | 30                        | puuttuu                                                                                                            |
| 19 | Lisenssi + "Ehdota muutosta" alatunnisteessa | —                         | **tehty** — tekijät, lisenssi ja muokkauslinkki; "Ilmoita ongelmasta" puuttuu                                      |
| 20 | ACE-editori (`editable`-lohkot)              | 2                         | puuttuu — `.editable` säilyy nyt luokkana, ks. kohta 4                                                             |
| 21 | KaTeX                                        | 0                         | voi jättää pois                                                                                                    |
| 22 | Edellinen/seuraava sivun alareunassa         | joka sivu                 | **tehty** — `navigation.footer`                                                                                    |
| 23 | `### [Windows](#tab/win)`-välilehdet         | 33 lohkoa / 9 joukkoa     | **tehty** — `pymdownx.tabbed` + `content.tabs.link`                                                                |
| 24 | Tulostuspainike: koko kirja yhdeksi PDF:ksi  | joka sivu                 | **tehty** — `assets/js/print.js`, `print.css`, runko `convert.py`:stä, yläpalkin malli                             |

Zensical antaa itse ilman mitään lisäystä: oikean reunan sisällysluettelon,
haun, kopioi koodi -napin ja responsiivisen navigaation. Edellinen/seuraava
-linkit ja alatunnisteen se osaa myös, mutta ne ovat oletuksena pois päältä;
ks. kohdat 19 ja 22.

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

**Yksi joukko yhdeksästä ei piirry**, ja syy on muualla: `01-hei-java.md`:n
komentorivivälilehdet ovat raa'an `<details>`-lohkon sisällä, eikä
Python-Markdown jäsennä sellaisen sisältöä lainkaan Markdownina. Samassa
lohkossa jäävät renderöimättä myös linkit ja listat — sivulla lukee
sananmukaisesti `[työkaluohjeita](../tyokalut.md#java-development-kit-jdk)`.
mdBookissa lohko toimii, joten tämä on tarkistuslistan kohta 8, ei
välilehtien: se korjautuu samalla kun `<details>`-lohkot korjataan
(`md_in_html` vaatii `<details markdown>`). Muut kahdeksan joukkoa — kaikki
työkalusivun viisi ja osan 8 kolme — piirtyvät.


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

    ```java
    public class Main { ... }
    ```

=== "Valo.java"

    ```java
    public class Valo extends Laite { ... }
    ```
````

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
* Yksi välilehtijoukko 82:sta ei piirry: `01-hei-java.md`:n
  käyttöjärjestelmävälilehdet ovat raa'an `<details>`-lohkon sisällä. Sama
  havainto kuin kohdassa 23, ja se korjautuu kohdan 8 mukana.

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
