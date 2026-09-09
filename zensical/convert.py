#!/usr/bin/env python3
"""Kopioi mdBookin lähdepuu (../src) Zensicalin docs/-hakemistoksi.

Barebones-lähtötilanne: skripti kopioi tiedostot ja kääntää src/SUMMARY.md:n
nav-lohkoksi, koska ilman navigaatiota sivustoa ei voi selata lainkaan.

Sisältöä muunnetaan seitsemässä kohdassa: sisällytysmakrot tiedostojen sisällöksi
({{#include}}, convert_includes), koodilohkojen monitiedostomerkinnät
välilehdiksi (// FILE:, convert_files), mdBookin aidan attribuuttilista
(java,ignore) pymdownx:n muotoon (convert_fences), alertit admonitioneiksi
(> [!VINKKI], convert_alerts), avattavien osioiden sisältö Markdowniksi
(<details markdown="1">, convert_details), tehtäväkortit diveiksi
(<task>, convert_tasks) ja työkalusivun
käyttöjärjestelmävalinnat välilehdiksi (### [Windows](#tab/win),
convert_tabs). Muu mdBookin syntaksi
(//- piilorivit) jää sellaisenaan sivuille näkyviin. Se on
tarkoitus: näin näkee yhdellä silmäyksellä, mitä oikeasti pitää korjata. Muunnokset lisätään takaisin
yksi kerrallaan, ks. README.md.

Generoitu docs/ on kertakäyttöinen — tämä skripti on totuus.
"""

import hashlib
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "src"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

SUMMARY_LINK_RE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>-\s*)?\[(?P<title>[^\]]*)\]\((?P<href>[^)]*)\)")

# mdBookin SUMMARY.md ei salli etulinkkien (prefix chapters) sisäkkäisyyttä:
# sisennetty rivi jää mdBookissa samalle tasolle ja jättää navigaatioon vielä
# tyhjän rivin. Zensicalissa sisäkkäisyys onnistuu, joten se tehdään tässä.
# Avain = alasivun polku, arvo = sen sivun polku, jonka alle se siirretään.
NEST_UNDER = {
    "tenttiohjeet.md": "tentti.md",
}

# Tulostussivu: koko kirja yhdellä sivulla, ks. assets/js/print.js.
PRINT_PAGE = "tulosta.md"

PRINT_INTRO = """\
---
title: Koko kirja
search:
  exclude: true
hide:
  - toc
---

<div id="jyu-print-intro" markdown>

# Koko kirja yhtenä sivuna

<p id="jyu-print-status">Selain kokoaa luvut tälle sivulle ja avaa
tulostusikkunan itsestään. Jos JavaScript ei ole käytössä, alla oleva
luettelo on kirjan sisällysluettelo.</p>

</div>

<div id="jyu-print" markdown>

"""

NAV_ENTRY_RE = re.compile(r'^\s*-\s+"(?P<title>[^"]+)":\s*(?P<href>\S+\.md)\s*$', re.M)

# mdBookin välilehdet (preprocessor.accordion). Otsikko "### [Windows](#tab/win)"
# aloittaa lohkon, "***"-rivi lopettaa sen, ja peräkkäiset lohkot ovat yksi
# välilehtijoukko. Otsikkotasolla ei ole väliä: sama sivu käyttää sekä ### että
# ####, eikä mdBook tee otsikoista otsikoita vaan välilehtirivin.
TAB_HEADING_RE = re.compile(
    r"^#{1,6}\s+\[(?P<label>[^\]]+)\]\(#tab/(?P<id>[^)]+)\)\s*$")
TAB_END = "***"

# Välilehti, jolla mdBook täytti tilanteen "ei vielä valintaa": sen otsikko ei
# ole välilehtirivissä lainkaan, ja se näkyy kunnes joku muu välilehti
# valitaan. Zensicalin välilehdissä yksi on aina valittuna, joten tälle ei ole
# paikkaa; ks. README.md.
TAB_PLACEHOLDER = "default"

# mdBookin monitiedostolohkot (preprocessor.codeblock-tabs): yhden koodiaidan
# sisällä on useita tiedostoja, jotka mdBook näyttää välilehtinä. Merkinnät
# ovat aineistossa epätarkkoja ja mdBookin esikäsittelijä sietää sen, joten
# sama sietokyky tässä (todennettu mdBookin generoimasta book/:sta):
# "//FILE:" ilman välilyöntiä, rivin lopussa välilyöntejä, ja FILE_END joko
# puuttuu tai on liikaa. Tiedoston lopettaa yhtä lailla seuraava FILE-merkintä.
FILE_BEGIN_RE = re.compile(r"^\s*//\s*FILE:\s*(?P<name>.+?)\s*$")
FILE_END_RE = re.compile(r"^\s*//\s*FILE_END\s*$")

# Koodiaita. Monitiedostolohkot ovat kaikki sarakkeessa 0, mutta aidan
# attribuuttilista (convert_fences) esiintyy myös sisennettynä, joten
# sisennys otetaan talteen ja kirjoitetaan takaisin sellaisenaan.
CODE_FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)(?P<info>[^\n`]*)$")

# Sama aita lainauslohkon sisällä ("> ```java,ignore"). convert_fences
# kirjoittaa vain otsikon ja jättää rivin alun ennalleen, joten sille ">"
# kelpaa sisennykseksi. convert_files ei käytä tätä: välilehtijoukko ei mahdu
# lainauslohkoon ilman että jokainen sen rivi saisi ">"-etuliitteen, eikä
# yhtään monitiedostolohkoa ole lainauksen sisällä.
QUOTED_FENCE_RE = re.compile(
    r"^(?P<indent>[\s>]*)(?P<fence>```+|~~~+)(?P<info>[^\n`]*)$")

# mdBookin sisällytysmakro (sisäänrakennettu links-esikäsittelijä). Polun
# perässä voi olla rivivalinta kaksoispisteen jälkeen, ks. take_lines.
INCLUDE_RE = re.compile(r"\{\{#include\s+(?P<spec>[^}\s][^}]*?)\s*\}\}")

# mdBookin alertit (preprocessor.alerts, mdbook-alerts): lainauslohko, jonka
# ensimmäinen rivi on pelkkä "[!TUNNUS]". Aineistossa tunnus on kirjoitettu
# milloin versaalilla milloin ei ("VINKKI", "Vinkki"), ja mdbook-alerts
# pienentää sen luokaksi ja palauttaa otsikon isolla alkukirjaimella vasta
# CSS:n capitalize-muunnoksella. Sama tehdään tässä taulukolla.
ALERT_RE = re.compile(r"^>\s*\[!(?P<label>[^\]]+)\]\s*$")

# Tunnus -> Materialin admonition-tyyppi ja otsikko, ks. README.md kohta 7.
# Otsikko kirjoitetaan aina näkyviin, joten tyypistä jää jäljelle vain väri ja
# kuvake — ja tyyppi on valittu sen mukaan, mikä on lähinnä sitä väriä ja
# kuvaketta, jonka mdBook antoi (theme/alerts-style.css).
#
# Vain kanoniset tyypit kelpaavat: Zensicalin mukana tulevassa CSS:ssä ei ole
# yhtään aliasta, joten esimerkiksi "important" (Materialin oma alias sanalle
# "tip") jäisi kokonaan tyylittömäksi. Siksi Tärkeää on "tip".
ALERT_KINDS = {
    "osaamistavoitteet": ("abstract", "Osaamistavoitteet"),
    "huomautus": ("note", "Huomautus"),
    "vinkki": ("tip", "Vinkki"),
    "tärkeää": ("tip", "Tärkeää"),
    "varoitus": ("warning", "Varoitus"),
    "todo": ("info", "Todo"),
    "wip": ("danger", "WIP"),
}

# Tuntematon tunnus säilyy otsikkona sellaisenaan; tyypiksi tulee neutraalein.
ALERT_FALLBACK = "note"

# mdBookin <details>-lohkot, ks. README.md kohta 8. Python-Markdown ei käsittele
# raa'an HTML-lohkon sisältöä Markdownina vaan päästää sen läpi sellaisenaan:
# numeroitu lista jää muotoon "1.", linkki muotoon "[teksti](osoite)" ja `koodi`
# backtickeineen. Automaattilinkki <https://...> katoaa kokonaan, koska selain
# lukee sen tuntemattomaksi tagiksi. mdBookin pulldown-cmark lopettaa
# HTML-lohkon tyhjään riviin ja jatkaa Markdownin jäsentämistä; sama saadaan
# tässä markdown-attribuutilla, jonka md_in_html-laajennus tunnistaa. Laajennus
# on jo Zensicalin oletuslistalla (DEFAULT_MARKDOWN_EXTENSIONS), joten
# mkdocs.yml:ään ei tule riviäkään — sama tilanne kuin alerteissa (kohta 7) ja
# välilehdissä (kohta 23).
#
# Aineistossa avaustagi on kahta muotoa: <details> (70) ja <details closed>
# (18). Jälkimmäinen ei ole HTML:ää — attribuutti on "open", eikä "closed"
# tarkoita mitään — mutta lopputulos on silti se, mitä kirjoittaja tarkoitti, ja
# sama kummallakin generaattorilla, joten attribuutti jätetään paikalleen.
#
# Lookahead pitää muunnoksen toistokelpoisena: jo käännetty tagi ohitetaan.
DETAILS_RE = re.compile(r"<details(?![^>]*\bmarkdown=)(?P<attrs>[^>]*)>")

# Sama <summary>-tagille silloin, kun yhteenveto on omia kappaleitaan.
# Aineistossa yhteenveto on kolmea muotoa:
#
#     <details><summary>Vinkki</summary>              (63, yksi rivi)
#
#     <summary><i class="bi ..."></i>Valinnaista       (2, rivitetty teksti)
#     lisätietoa: Java ei voi päätellä tyyppiä</summary>
#
#     <details><summary>                               (6, harjoitustyo.md)
#
#     ### Kulujen seuranta
#
#     Tässä sovelluksessa käyttäjä voi seurata omia kulujaan ja menojaan.
#
#     </summary>
#
# Vain viimeisessä on Markdownia, ja se jäi avauspalkkiin raakana:
# "### Kulujen seuranta Tässä sovelluksessa...".
#
# Ero kahden jälkimmäisen välillä on tyhjä rivi, ja se on tasan sama raja kuin
# kirjassa: pulldown-cmark lopettaa raa'an HTML-lohkon ensimmäiseen tyhjään
# riviin ja jäsentää siitä eteenpäin Markdownia. Ilman tyhjää riviä kirjakin
# päästää yhteenvedon läpi sellaisenaan, joten kahteen rivitettyyn tekstiin ei
# kosketa — muuten niiden teksti käärittäisiin <p>:hen, joka toisi avauspalkkiin
# kappaleen marginaalit.
#
# Arvo on "block" eikä "1", koska md_in_html jakaa lohkotason tagit kahtia
# (md_in_html.py: span_tags): <summary> on niiden joukossa, joiden sisältö saa
# oletuksena vain rivinsisäisen jäsennyksen — samoin kuin <p> ja <li> — ja
# markdown="1" tarkoittaisi siis samaa kuin markdown="span", jolloin otsikko
# jäisi yhä risuaidoiksi. Vain "block" pakottaa lohkojäsennyksen.
SUMMARY_RE = re.compile(r"<summary(?![^>]*\bmarkdown=)(?P<attrs>[^>]*)>")
SUMMARY_END = "</summary>"

# Omaksi kappaleekseen jäänyt <br />, ks. README.md kohta 8. Aineistossa niitä
# on neljä, kaikki <details>-lohkon tai koodiaidan jäljessä: ne on kirjoitettu
# väljyydeksi lohkojen väliin. Python-Markdown tekee rivistä oman kappaleen
# (<p><br /></p>), joka vie sivulla kokonaisen rivin verran tilaa omien
# marginaaliensa lisäksi — kahden peräkkäisen avattavan osion väli
# kolminkertaistui (25 px -> ~75 px). Väljyys on jo laatikossa itsessään:
# Materialilla margin: 1.5625em 0, ja mdBookissa margin-block: 1em
# (theme/css/general.css), joten rivi on nykyisin turha molemmissa.
#
# Vain omalla rivillään ja sarakkeessa 0 oleva tagi pudotetaan: rivin lopussa
# <br /> on oikea rivinvaihto kappaleen sisällä, ja sisennetty rivi voisi olla
# sisennettyä koodia.
BREAK_LINE_RE = re.compile(r"^<br\s*/?>\s*$")

# Harjoitustyön vaatimusdivit, ks. README.md kohta 25. Ongelma on sama kuin
# <details>-lohkoissa, ja aineistossa divejä on tasan yhdeksän, kaikki
# harjoitustyo.md:ssä: uloin <div class="ht-reqs"> ja sen sisällä kahdeksan
# <div class="req">, joissa on koko harjoitustyön arviointiperuste. Ilman
# attribuuttia niiden 190 riviä — kahdeksan otsikkoa, numeroidut listat ja
# lihavoinnit — jäivät sivulle yhtenä raakana Markdown-pötkönä.
#
# Attribuutti tarvitaan myös uloimpaan diviin: md_in_html ei etene sisempiin
# lohkoihin, jos uloin on käsittelemätöntä HTML:ää (sama syy kuin
# tehtäväkorttien ulommassa divissä, kohta 6).
#
# Divi ei ole span_tagsissa toisin kuin <summary>, joten tähän riittää "1".
#
# Lookahead pitää muunnoksen toistokelpoisena, kuten DETAILS_RE:ssä.
DIV_RE = re.compile(r"<div(?![^>]*\bmarkdown=)(?P<attrs>[^>]*)>")

# Luokkakaaviot, ks. README.md kohta 15. mdBookissa ```plantuml-aidan sisältö
# ei ole koodia vaan kaavion lähde, jonka mdbook-plantuml lähettää
# PlantUML-palvelimelle (book.toml: plantuml-cmd) ja korvaa aidan palvelimen
# palauttamalla SVG:llä. Zensicalille aita on tavallinen koodilohko, joten sivulla
# näkyi 20 riviä "@startuml / class Kategoria { ... }" siinä missä kirjassa on
# kaavio. Tämä on aineiston 17 kaaviosta jokaisen kohdalla iso ero: luokkien
# väliset suhteet ovat juuri se, mitä kaaviolla kerrotaan.
#
# Sama palvelin kuin kirjassa, sama tapa: kaavio pakataan URL-osoitteeseen ja
# vastaus talletetaan tiedostoksi, jonka nimi on lähteen sha1. Aita korvataan
# kuvaviittauksella.
#
# Osoitteen pakkaus on PlantUMLin oma: raaka deflate (zlib-otsikko ja
# tarkiste pois) ja base64 omalla aakkostolla. Palvelin vaatii User-Agentin;
# ilman sitä vastaus on 403.
#
# Tiedostot ovat versionhallinnassa (assets/plantuml/), eivät kertakäyttöisessä
# docs/:ssä, ja se on tarkoituksellista: silloin käännös ei tarvitse verkkoa
# eikä ole PlantUML-palvelimen varassa. Verkkoon mennään vain, kun kaavion
# lähde on muuttunut tai uusi kaavio on lisätty; muulloin luetaan levyltä.
# Jos palvelin ei vastaa, aita jätetään ennalleen ja ajo varoittaa — käännös ei
# siis kaadu koneella, jossa ei ole verkkoa, vaan sivu palaa siihen mitä se oli
# ennen tätä kohtaa.
#
# Käyttämättä jääneet tiedostot siivotaan ajon lopuksi, jottei muokatun kaavion
# vanha versio jäisi hakemistoon.
PLANTUML_FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)plantuml\s*$")
PLANTUML_URL = "https://www.plantuml.com/plantuml/svg/"
PLANTUML_AGENT = "ohj2-zensical-koeputki"
PLANTUML_DIR = ASSETS / "plantuml"
PLANTUML_ALPHABET = (
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_")

# Aineiston kaikki 17 kaaviota ovat luokkakaavioita (class/interface), joten
# vaihtoehtoinen teksti voi olla tarkka. mdBook jättää alt-tekstin tyhjäksi.
PLANTUML_ALT = "UML-luokkakaavio"

# ASCII-kaaviot, ks. README.md kohta 15. ```bob-aidan sisältö on piirros, jonka
# mdbook-svgbob kääntää SVG:ksi (book.toml: preprocessor.svgbob). Zensicalille
# aita on koodilohkoa: piirros on luettavissa, koska se on tasavälistä tekstiä,
# mutta laatikot ovat "+---+" eivätkä viivoja.
#
# Piirtäjää ei ole Pythonille. Sama piirtäjä on saatavana omana komentonaan
# (`cargo install svgbob_cli`, sama svgbob 0.7 kuin mdbook-svgbobin sisällä),
# ja sitä käytetään tässä. Vaihtoehto olisi ollut ajaa mdbook-svgbobia, joka on
# koneella jo kirjan takia, mutta se on mdBookin esikäsittelijä: sille pitäisi
# rakentaa mdBookin oma JSON-sanoma, ja koeputken idea on päästä mdBookista
# eroon, ei rakentaa sen protokollaa uudelleen.
#
# Riippuvuus on pehmeä, samoin kuin luokkakaavioissa: valmiit kaaviot ovat
# versionhallinnassa (cache/svgbob/), joten käännös ei tarvitse svgbobia
# lainkaan. Komentoa kutsutaan vain, kun piirros on uusi tai muuttunut, ja jos
# sitä ei ole asennettu, aita jätetään ennalleen ja ajo varoittaa.
#
# Kaaviot upotetaan sivulle sellaisenaan, ei <img>-viittauksena kuten
# luokkakaaviot: svgbobin SVG saa värinsä CSS-muuttujista, ja <img>:n sisällä
# oleva SVG ei näe sivun muuttujia. Upotettuna kaavio seuraa teemaa kuten
# kirjassa (siellä muuttujat ovat --fg ja --mono-font). Siksi cache/svgbob/ on
# assetsien ulkopuolella: se on välimuisti, ei julkaistava tiedosto.
#
# Tyhjät rivit poistetaan: Python-Markdown lopettaisi raa'an HTML-lohkon
# ensimmäiseen tyhjään riviin. Kääre on <div>, koska <svg> ei ole
# BLOCK_LEVEL_ELEMENTS-listalla: paljas <svg> päätyisi kappaleen sisään ja
# rivinvaihdot <br />-tageiksi.
SVGBOB_FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)bob\s*$")
SVGBOB_DIR = ROOT / "cache" / "svgbob"

# svgbob kirjoittaa jokaiseen kaavioon samat viisi nuolenkärkimäärittelyä
# (id="arrow", "circle", ...) riippumatta siitä käyttääkö kaavio niitä. Kahdella
# kaaviolla samalla sivulla olisi siis samat tunnisteet, ja url(#arrow) osoittaisi
# aina ensimmäiseen — sivulla osa6/02 kaavioita on neljä. Tunnisteille annetaan
# siksi sivukohtainen juokseva etuliite. Tulostussivulla print.js lisää vielä
# luvun oman etuliitteen, joten tunnisteet pysyvät ainutkertaisina myös silloin,
# kun koko kirja on yhdellä sivulla.
SVGBOB_ID_RE = re.compile(r'\bid="(?P<name>[^"]+)"')
SVGBOB_REF_RE = re.compile(r"url\(#(?P<name>[^)]+)\)")

# Piirtoasetukset ovat book.tomlin omat, värit ja kirjasin Zensicalin
# muuttujiin käännettyinä (kirjassa var(--fg) ja var(--mono-font)).
SVGBOB_COMMAND = [
    "svgbob_cli",
    "--font-size", "14",
    "--font-family", "var(--md-code-font-family)",
    "--fill-color", "var(--md-default-fg-color)",
    "--stroke-color", "var(--md-default-fg-color)",
    "--stroke-width", "2",
    "--background", "transparent",
]

# Tehtäväkortit. mdBookin merkkaus on omia elementtejä, joita HTML ei tunne:
#
#     <task>
#       <task-title num="2.1">Kello<points>1 p.</points></task-title>
#       <handout>
#
#       tehtävänanto Markdownina
#
#       </handout>
#       <task-link><a href="...">Tee tehtävä TIMissä</a></task-link>
#     </task>
#
# Kirjassa ne tyylitetään sellaisenaan (theme/tasks.css osoittaa suoraan
# tageihin), mutta täällä ne eivät kelpaa kahdesta syystä. Python-Markdown
# tunnistaa HTML-lohkon tagin nimestä (markdown.util.BLOCK_LEVEL_ELEMENTS),
# eikä <task> ole listalla: koko kortti jää kappaleen sisään muotoon
# "<p><task> ... <handout></p>", ja tehtävänannon Markdown jäsentyy väärään
# paikkaan. Samasta syystä md_in_html ei myöskään käsittele lohkon sisältöä,
# vaikka tageihin lisäisi markdown-attribuutin.
#
# Kortti käännetään siis diveiksi, joilla on kaksi ominaisuutta: nimi on
# luokassa (assets/css/tasks.css) ja tehtävänanto on merkitty
# markdown="1":llä, jolloin md_in_html jäsentää sen sisällön normaalisti.
# Laajennus on jo Zensicalin oletuslistalla, joten mkdocs.yml:ään ei tule
# riviäkään — sama tilanne kuin avattavissa osioissa (kohta 8).
#
# Tunnusrivistä tulee yksi rivi raakaa HTML:ää: numero, nimi ja pisteet ovat
# tekstiä eivätkä Markdownia, joten sitä ei merkitä markdown-attribuutilla.
# Bonustähti <i class="bi bi-stars"> jää nimen *sisälle*, kuten lähteessäkin;
# tyyli tekee siitä liuskan ja piirtää tähden itse, koska Bootstrap Iconsia
# ei ladata (kohta 17).
TASK_TAG_RE = re.compile(r"</?(?:task|task-title|task-link|handout)[ >]")
TASK_TITLE_RE = re.compile(
    r'<task-title\s+num="(?P<num>[^"]*)"\s*>(?P<inner>.*?)</task-title>')
TASK_POINTS_RE = re.compile(r"<points>(?P<points>.*?)</points>")
TASK_BONUS_RE = re.compile(r'<i\s+class="[^"]*\bbi-stars\b[^"]*"\s*>\s*</i>')
TASK_TAGS = (
    ("<task>", '<div class="task" markdown="1">'),
    ("</task>", "</div>"),
    ("<handout>", '<div class="task-handout" markdown="1">'),
    ("</handout>", "</div>"),
    ("<task-link>", '<div class="task-link">'),
    ("</task-link>", "</div>"),
)


def nest_moves() -> dict[str, str]:
    """NEST_UNDER -> siirrot docs/:ssä: vanha polku -> uusi polku.

    navigation.indexes tekee osion otsikosta linkin vain, jos osion ensimmäinen
    sivu on hakemistonsa index.md (Zensical katsoo pelkkää tiedostonimeä,
    ks. config.py: _is_index). Yläsivu on siis siirrettävä omaan hakemistoonsa,
    ja alasivu sen viereen — silloin sivujen väliset suhteelliset linkit
    (./tenttiohjeet.md) osoittavat yhä oikein eikä sisältöä tarvitse muuntaa.
    """
    moves: dict[str, str] = {}
    for child, parent in NEST_UNDER.items():
        folder = parent.removesuffix(".md")
        moves[parent] = f"{folder}/index.md"
        moves[child] = f"{folder}/{Path(child).name}"
    return moves


def prune_diagrams(folder: Path, used: set[str]) -> int:
    """Käyttämättömät kaaviotiedostot pois. -> poistettuja.

    Nimi on kaavion lähteen sha1, joten muokattu kaavio jättäisi vanhan
    tiedoston hakemistoon ikuisiksi ajoiksi. Siivotaan vain, jos ajossa
    ylipäätään syntyi kaavioita: tyhjä joukko tarkoittaa, ettei piirtäjää
    saatu, eikä silloin saa poistaa sitä mitä levyllä jo on.
    """
    if not used or not folder.is_dir():
        return 0
    removed = 0
    for path in folder.glob("*.svg"):
        if path.name not in used:
            path.unlink()
            removed += 1
    return removed


def build_extra(tab_labels: set[str]) -> str:
    """extra.edit_source ja extra.tab_labels mkdocs.yml:n INHERIT-lohkoon.

    extra.tab_labels on lista convert_tabsin tuottamista välilehtiotsikoista
    (Windows, macOS, ...). Materialin content.tabs.link muistaa valitun
    välilehden selaimessa ja palauttaa sen joka sivulla otsikon perusteella,
    mikä on käyttöjärjestelmävalinnassa haluttua mutta koodilohkoissa ei:
    kerran klikattu tiedostonimi avaisi kaikki sen sisältävät lohkot siitä
    tiedostosta eikä tekijän valitsemasta ensimmäisestä. Lista kertoo mallille
    (overrides/partials/javascripts/content.html), mitkä otsikot saa palauttaa.

    extra.edit_source: docs/:n polku -> ../src:n polku, tyhjä = ei lähdettä.

    Muokkauslinkki (mkdocs.yml: repo_url + edit_uri) osoittaa versionhallinnan
    src/-puuhun, mutta Zensical laskee osoitteen sivun polusta docs/:ssä.
    Polut ovat samat kahta poikkeusta lukuun ottamatta, ja molemmissa linkki
    osoittaisi tiedostoon jota src:ssä ei ole:

    * NEST_UNDER-siirrot — sivu on olemassa, mutta muualla. Käännetään takaisin.
    * PRINT_PAGE — sivu syntyy tässä skriptissä eikä sitä voi muokata.
      Tyhjä arvo, jolloin malli jättää linkin kokonaan pois.

    Kartan lukee overrides/partials/copyright.html.
    """
    sources = {new_path: old_path for old_path, new_path in nest_moves().items()}
    sources[PRINT_PAGE] = ""
    lines = ["", "# Muokkauslinkin polkukartta, ks. overrides/partials/copyright.html,",
             "# ja välilehtimuistin sallitut otsikot, ks.",
             "# overrides/partials/javascripts/content.html.",
             "extra:", "  edit_source:"]
    for docs_path, src_path in sorted(sources.items()):
        lines.append(f'    "{docs_path}": "{src_path}"')
    lines.append("  tab_labels:")
    for label in sorted(tab_labels):
        lines.append(f'    - "{label}"')
    return "\n".join(lines) + "\n"


def build_print_page(nav_yaml: str) -> str:
    """nav: -lohko -> docs/tulosta.md: linkki jokaiseen lukuun kirjan järjestyksessä.

    mdBookissa tulostussivu (print.html) on käännösaikainen: se renderöi
    jokaisen luvun erikseen ja liittää valmiit HTML-palat peräkkäin. Sama ei
    onnistu tässä Markdown-tasolla, vaikka se olisi luontevin paikka:
    kokeiltuna 73 luvun otsikosta 32 katosi, kun luvut liitettiin yhdeksi
    Markdown-tiedostoksi. Luvut eivät ole itsenäisiä — kesken jäänyt raaka
    HTML-lohko (<details>, <task>) tai pariton koodiaita jatkuu yhdistetyssä
    tiedostossa seuraavaan lukuun ja nielaisee sen alun, kun taas erillisinä
    sivuina jäsennin palautuu alkutilaan joka sivun lopussa.

    Siksi tämä sivu on pelkkä runko: luettelo kaikista luvuista kirjan
    järjestyksessä. Selain hakee luvut niiden omilta sivuilta ja liittää
    valmiin HTML:n tähän, eli samasta paikasta kuin mdBook. Ilman
    JavaScriptiä luettelo jää näkyviin sisällysluettelona.
    """
    lines = [PRINT_INTRO]
    for match in NAV_ENTRY_RE.finditer(nav_yaml):
        lines.append(f"- [{match['title']}]({match['href']})")
    lines.append("\n</div>\n")
    return "\n".join(lines)


def build_nav() -> str:
    """src/SUMMARY.md -> mkdocs nav: -lohko.

    Numerointi vastaa mdBookia: numeron saavat vain listakohdat
    ("- [Luku](...)"), juoksevasti myös ---erottimien yli. Etu- ja
    jälkilinkit (Aloitus, Työkalut, Luennot) jäävät numeroimatta, jolloin
    ne erottuvat osista ilman erillisiä erottimia.
    """
    entries: list[tuple[int, str, str, bool]] = []
    for raw in (SRC / "SUMMARY.md").read_text(encoding="utf-8").split("\n"):
        if not raw.strip() or raw.strip().startswith("#") or set(raw.strip()) == {"-"}:
            continue
        match = SUMMARY_LINK_RE.match(raw)
        if not match:
            continue
        href = match.group("href").strip()
        title = match.group("title").strip()
        if not href:
            # SUMMARY.md:n kikka ulkoiselle linkille: [Otsikko<https://url>]()
            embedded = re.match(r"^(?P<t>.*?)<(?P<u>https?://[^>]+)>$", title)
            if not embedded:
                continue
            title, href = embedded.group("t").strip(), embedded.group("u")
        else:
            href = href.lstrip("./")
        entries.append((len(match.group("indent")) // 2, title.replace('"', "'"), href,
                        bool(match.group("bullet"))))

    moves = nest_moves()
    entries = [(level, title, moves.get(href, href), numbered)
               for level, title, href, numbered in entries]
    for child_href, parent_href in NEST_UNDER.items():
        child = next((e for e in entries if e[2] == moves[child_href]), None)
        parent = next((e for e in entries if e[2] == moves[parent_href]), None)
        if child is None or parent is None:
            continue
        entries.remove(child)
        entries.insert(entries.index(parent) + 1,
                       (parent[0] + 1, child[1], child[2], child[3]))

    counters: list[int] = []

    def number_for(depth: int) -> str:
        """Juokseva numero syvyydelle: 1, 1.1, 1.2, 2, ..."""
        del counters[depth + 1:]
        while len(counters) <= depth:
            counters.append(0)
        counters[depth] += 1
        return ".".join(str(n) for n in counters)

    def emit(index: int, depth: int, out: list[str]) -> int:
        pad = "  " * (depth + 1)
        while index < len(entries):
            level, title, href, numbered = entries[index]
            if level < depth:
                return index
            if numbered:
                title = f"{number_for(level)} {title}"
            has_children = index + 1 < len(entries) and entries[index + 1][0] > level
            if has_children:
                out.append(f'{pad}- "{title}":')
                # Osan etusivu ensimmäisenä lapsena = Materialin
                # navigation.indexes: osan otsikosta tulee sen oma linkki,
                # kuten mdBookissa.
                #
                # Otsikko toistetaan tässä numeroineen, vaikka valikko ottaa
                # sen osiolta: sivun oma otsikko menee sellaisenaan sivun
                # alareunan edellinen/seuraava-linkkeihin ja <title>-tagiin.
                # Ilman tätä osat olisivat siellä ainoat numeroimattomat
                # ("Olio-ohjelmoinnin perusteet" vs "2.1 Kohti
                # olio-ohjelmointia"). Valikon ulkoasu ei muutu: se lukee
                # otsikon osiolta, ei tältä lapselta.
                out.append(f'{pad}  - "{title}": {href}')
                index = emit(index + 1, depth + 1, out)
            else:
                out.append(f'{pad}- "{title}": {href}')
                index += 1
        return index

    lines = ["nav:"]
    emit(0, 0, lines)
    return "\n".join(lines) + "\n"


def take_lines(content: str, selector: str) -> str | None:
    """Sisällytettävän tiedoston rivivalinta. -> teksti, tai None jos ei rivejä.

    mdBookin muodot ovat "" (koko tiedosto), "N" (yksi rivi), "A:B" (väli),
    "A:" (A:sta loppuun) ja ":B" (alusta B:hen); numerot ovat 1-pohjaisia ja
    molemmat päät kuuluvat mukaan. Aineistossa niistä esiintyy kaksi, koko
    tiedosto ja yksi rivi, mutta koko kielioppi on tässä samat rivit koodia
    eikä jätä muille muodoille hiljaista väärintulkintaa.

    Rivit kootaan yhteen ilman loppurivinvaihtoa, kuten mdBookin take_lines.
    Siksi "{{#include ./takarajat.md:1}}" mahtuu taulukon soluun eikä
    koodiaidan sisällä synny tyhjää riviä ennen sulkevaa aitaa (todennettu
    mdBookin generoimasta book/:sta).

    Ankkurit (":ANCHOR", nimetty ANCHOR-kommenteilla) ovat mdBookin kolmas
    muoto. Aineistossa ei ole yhtään, joten niitä ei toteuteta; tunnistamaton
    valinta tulee tänne ja palautuu None:na, jolloin makro jää näkyviin.
    """
    lines = content.splitlines()
    if not selector:
        return "\n".join(lines)
    bounds = selector.split(":")
    if len(bounds) > 2 or not any(bounds) or not all(b.isdigit() or not b
                                                     for b in bounds):
        return None
    first = bounds[0]
    last = bounds[1] if len(bounds) == 2 else first
    start = int(first) if first else 1
    end = int(last) if last else len(lines)
    return "\n".join(lines[max(start - 1, 0):end])


def convert_includes(text: str, page: Path) -> tuple[str, int]:
    """mdBookin {{#include}} -> tiedoston sisältö paikalleen. -> (teksti, määrä).

    Ensimmäisenä muunnoksena, kuten mdBookissa: sen links-esikäsittelijä ajetaan
    ennen muita, joten kaikki muut näkevät jo sisällytetyn tekstin. Täällä se on
    myös pakko: 19 sisällytystä on koodiaidan sisällä // FILE: -merkintöjen
    välissä, ja convert_files sisentää aidan sisällön välilehdeksi vasta tämän
    jälkeen.

    Makro korvataan sellaisenaan tekstinä eikä rivin sisennystä toisteta
    riveille, koska mdBook ei tee niin sekään: neljä sisällytystä on sisennetty
    kahdella välilyönnillä, ja niissä sisennyksen saa vain ensimmäinen rivi.
    Molemmissa lopputulos on sama, koska kahden välilyönnin sisennys ei ole
    Markdownissa merkitsevä.

    Sivu on lähdepuun sivu, ei docs/:n kopio, ja polku on suhteessa siihen.
    Sisällytettävä tiedosto luetaan siis aina koskemattomana: tehtävänannot ovat
    itsekin docs/:n sivuja ja muuntuvat samassa silmukassa, jolloin kopiosta
    lukeva sisällytys saisi eri tekstin sen mukaan, kumpi tiedosto sattuu
    olemaan aakkosissa ensin.

    Puuttuvasta tiedostosta ja ankkurivalinnasta varoitetaan ja makro jätetään
    näkyviin: hiljaa katoava sisällytys näyttäisi sivulla samalta kuin tyhjä
    tehtävänanto.
    """
    includes = 0

    def expand(match: re.Match) -> str:
        nonlocal includes
        path, _, selector = match["spec"].partition(":")
        target = page.parent / path.strip()
        if not target.is_file():
            print(f"varoitus: {page.name}: sisällytettävä tiedosto puuttuu: "
                  f"{path.strip()}", file=sys.stderr)
            return match[0]
        content = take_lines(target.read_text(encoding="utf-8"), selector.strip())
        if content is None:
            print(f"varoitus: {page.name}: tuntematon rivivalinta: "
                  f"{match['spec']}", file=sys.stderr)
            return match[0]
        includes += 1
        return content

    return INCLUDE_RE.sub(expand, text), includes


def read_tab_set(lines: list[str],
                 start: int) -> tuple[list[tuple[str, str, list[str]]], int]:
    """Lue yksi välilehtijoukko riviltä start alkaen.

    Palauttaa osiot (tunnus, otsikko, sisältörivit) ja ensimmäisen rivin
    joukon jälkeen. Osion sisältö päättyy "***"-riviin tai — jos se puuttuu —
    seuraavaan välilehtiotsikkoon, jottei rikkinäinen lohko niele loppusivua.
    """
    sections: list[tuple[str, str, list[str]]] = []
    index = start
    while index < len(lines):
        heading = TAB_HEADING_RE.match(lines[index])
        if not heading:
            break
        index += 1
        body: list[str] = []
        while (index < len(lines) and lines[index].strip() != TAB_END
               and not TAB_HEADING_RE.match(lines[index])):
            body.append(lines[index])
            index += 1
        if index < len(lines) and lines[index].strip() == TAB_END:
            index += 1
        sections.append((heading["id"], heading["label"].strip(), body))
        while index < len(lines) and not lines[index].strip():
            index += 1
    return sections, index


def indent_block(body: list[str]) -> list[str]:
    """Rivit sisäkkäisen lohkon sisällöksi: tyhjät päät pois, muu 4 välilyöntiä
    sisemmäs. Suhteelliset sisennykset säilyvät, joten listat, koodiaidat ja
    raaka HTML pysyvät ennallaan. Sama sisennys kelpaa välilehdelle
    (convert_tabs, convert_files) ja admonitionille (convert_alerts)."""
    while body and not body[0].strip():
        body = body[1:]
    while body and not body[-1].strip():
        body = body[:-1]
    return [f"    {line}" if line.strip() else "" for line in body]


def fence_info(info: str) -> str:
    """mdBookin aidan attribuuttilista -> pymdownx:n aitaotsikko.

    mdBookissa aidan kielen perässä on pilkulla erotettuja lisämääreitä
    ("java,ignore" = älä käännä, ",noplayground" = ei ajonappia, ",editable" =
    ACE-editori). pymdownx ei tunne niitä eikä silloin tunnista koko aitaa —
    ei niin, että lohko jäisi korostamatta, vaan niin, että aita jää
    tavalliseksi tekstiksi ja sitä seuraava sulkeva aita alkaa uuden lohkon,
    joka nielaisee seuraavan tekstin koodiksi. Siksi tämä ei ole kosmetiikkaa;
    ks. README.md kohta 4.

    Määreet eivät ole turhia myöhemmin (ajonappi = kohta 3, editori = kohta
    20), joten niitä ei pudoteta vaan ne kirjoitetaan attr_listin luokiksi:
    "java,ignore" -> "{ .java .ignore }" -> <div class="language-java ignore
    highlight">. Kieli säilyy, korostus toimii ja tieto on tallessa luokkana.
    """
    parts = [part.strip() for part in info.strip().split(",")]
    language, attributes = parts[0], [part for part in parts[1:] if part]
    if not language or not attributes:
        return language
    return "{ ." + " .".join([language, *attributes]) + " }"


def convert_fences(text: str) -> tuple[str, int]:
    """Aitojen attribuuttilistat -> pymdownx:n muotoon. -> (teksti, aitoja).

    Käydään aidat läpi pareittain, jottei koodilohkon sisällä oleva
    aidannäköinen rivi muutu vahingossa. Sulkeva aita on vähintään yhtä pitkä
    eikä siinä ole otsikkoa.
    """
    out: list[str] = []
    open_fence: str | None = None
    fences = 0
    for line in text.split("\n"):
        match = QUOTED_FENCE_RE.match(line)
        info = match["info"].strip() if match else ""
        if match and open_fence is None:
            open_fence = match["fence"]
            if "," in info:
                fences += 1
                line = f"{match['indent']}{match['fence']}{fence_info(info)}"
        elif match and not info and len(match["fence"]) >= len(open_fence):
            open_fence = None
        out.append(line)
    return "\n".join(out), fences


def read_alert(lines: list[str], start: int) -> tuple[list[str], int]:
    """Lue yhden alertin sisältö riviltä start alkaen (tunnusrivi on start).

    Palauttaa lainauslohkon loput rivit ja ensimmäisen rivin lohkon jälkeen.
    Lohko loppuu ensimmäiseen riviin, joka ei ala ">"-merkillä — sama raja
    kuin Markdownilla itsellään, koska tyhjä rivi päättää lainauksen. Kaikki
    75 alerttia ovat sarakkeessa 0 eikä yhdessäkään ole laiskaa jatkoriviä
    (rivi ilman ">"-merkkiä), joten muuta rajaa ei tarvita.
    """
    index = start + 1
    while index < len(lines) and lines[index].startswith(">"):
        index += 1
    return lines[start + 1:index], index


def alert_body(body: list[str]) -> list[str]:
    """Lainauslohkon rivit admonitionin sisällöksi.

    ">"-etuliite pois ja rivi neljä välilyöntiä sisemmäs. Etuliitteestä
    syödään yksi välilyönti, jolloin lohkon omat sisennykset säilyvät
    ennallaan: koodiaidat, luetelmat ja raaka HTML tulevat läpi sellaisenaan.
    """
    return indent_block([line[1:].removeprefix(" ") for line in body])


def convert_alerts(text: str) -> tuple[str, int, set[str]]:
    """mdBookin alertit -> Materialin admonitionit. -> (teksti, lohkoja, tuntemattomat).

    "> [!VINKKI]" on GitHubin alert-syntaksia, jonka mdBookissa tekee
    mdbook-alerts. Zensicalissa se on tavallinen lainauslohko, jonka
    ensimmäisellä rivillä lukee "[!VINKKI]". Vastine on Markdownin oma
    admonition-laajennus, joka on jo Zensicalin oletuslistalla
    (DEFAULT_MARKDOWN_EXTENSIONS) — mkdocs.yml:ään ei siis tule riviäkään.

    Otsikko kirjoitetaan aina näkyviin ("!!! tip \"Vinkki\""), koska ilman
    sitä Material näyttää tyypin oman englanninkielisen nimen.
    """
    lines = text.split("\n")
    out: list[str] = []
    unknown: set[str] = set()
    alerts = 0
    index = 0
    while index < len(lines):
        match = ALERT_RE.match(lines[index])
        if not match:
            out.append(lines[index])
            index += 1
            continue
        label = match["label"].strip()
        known = ALERT_KINDS.get(label.lower())
        if known is None:
            unknown.add(label)
        kind, title = known or (ALERT_FALLBACK, label)
        body, index = read_alert(lines, index)
        alerts += 1
        if out and out[-1].strip():
            out.append("")
        out.append(f'!!! {kind} "{title}"')
        out.append("")
        out.extend(alert_body(body))
        # Tyhjä rivi perään vain jos lähteessä ei jo ollut: lainauksen päättävä
        # rivi on melkein aina tyhjä ja se tulee mukaan seuraavalla kierroksella.
        if index < len(lines) and lines[index].strip():
            out.append("")
    return "\n".join(out), alerts, unknown


def plantuml_encode(source: str) -> str:
    """Kaavion lähde -> PlantUML-palvelimen osoitepala.

    Raaka deflate (zlib.compress jättää eteen kaksitavuisen otsikon ja perään
    nelitavuisen tarkisteen, joita PlantUML ei odota) ja sen jälkeen base64
    PlantUMLin omalla aakkostolla: tavallisen "+/"-parin tilalla on "-_", ja
    kuusibittiset palat luetaan samassa järjestyksessä kuin tavallisessa
    base64:ssä. Täytetavut jätetään pois, ei "="-täytettä.
    """
    data = zlib.compress(source.encode("utf-8"), 9)[2:-4]
    encoded: list[str] = []
    for start in range(0, len(data), 3):
        chunk = data[start:start + 3]
        chunk += bytes(3 - len(chunk))
        bits = chunk[0] << 16 | chunk[1] << 8 | chunk[2]
        encoded += [PLANTUML_ALPHABET[(bits >> shift) & 63]
                    for shift in (18, 12, 6, 0)]
    return "".join(encoded)[:(len(data) * 8 + 5) // 6]


def plantuml_svg(source: str) -> str | None:
    """Kaavion lähde -> tiedostonimi assets/plantuml/:ssä, tai None.

    Nimi on lähteen sha1, joten muuttunut kaavio hakee itsensä uudelleen ja
    muuttumaton luetaan levyltä. None tarkoittaa, ettei kaaviota saatu: silloin
    aita jätetään ennalleen eikä käännös kaadu.
    """
    name = hashlib.sha1(source.encode("utf-8")).hexdigest() + ".svg"
    path = PLANTUML_DIR / name
    if path.is_file():
        return name
    request = urllib.request.Request(PLANTUML_URL + plantuml_encode(source),
                                     headers={"User-Agent": PLANTUML_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            svg = response.read()
    except (urllib.error.URLError, OSError) as error:
        print(f"varoitus: plantuml-palvelin ei vastannut: {error}",
              file=sys.stderr)
        return None
    # Palvelin vastaa 200:lla myös silloin, kun kaaviossa on syntaksivirhe: se
    # piirtää virheestä oman kuvansa. Se kelpaa tiedostoksi, mutta jokin muu
    # kuin SVG ei kelpaa.
    if b"<svg" not in svg[:1000]:
        print("varoitus: plantuml-palvelin ei palauttanut SVG:tä",
              file=sys.stderr)
        return None
    PLANTUML_DIR.mkdir(parents=True, exist_ok=True)
    path.write_bytes(svg)
    return name


def convert_plantuml(text: str, page: Path) -> tuple[str, int, set[str]]:
    """```plantuml-aidat kuviksi. -> (teksti, kaavioita, käytetyt tiedostot).

    Ilman muunnosta aidan sisältö on sivulla koodilohkona, ks.
    PLANTUML_FENCE_RE. Kuvan osoite on suhteellinen sivun omaan sijaintiin,
    ja sijainti otetaan siirtojen jälkeisestä polusta (nest_moves): Zensical
    ratkaisee suhteelliset osoitteet lähdetiedoston mukaan, joten alahakemistoon
    siirtyvä sivu tarvitsee yhden "../":n enemmän. Aineiston siirrettävillä
    kahdella sivulla ei ole kaavioita, mutta polku ei saa olla sen varassa.
    """
    relative = page.relative_to(DOCS).as_posix()
    depth = len(Path(nest_moves().get(relative, relative)).parent.parts)
    prefix = "../" * depth
    lines = text.split("\n")
    out: list[str] = []
    used: set[str] = set()
    diagrams = 0
    number = 0
    while number < len(lines):
        match = PLANTUML_FENCE_RE.match(lines[number])
        if not match:
            out.append(lines[number])
            number += 1
            continue
        end = number + 1
        while end < len(lines) and lines[end].strip() != match["fence"]:
            end += 1
        if end == len(lines):  # sulkematon aita: jätetään rauhaan
            out.append(lines[number])
            number += 1
            continue
        name = plantuml_svg("\n".join(lines[number + 1:end]).strip() + "\n")
        if name is None:
            out.extend(lines[number:end + 1])
        else:
            used.add(name)
            diagrams += 1
            out.append(f'{match["indent"]}![{PLANTUML_ALT}]'
                       f"({prefix}assets/plantuml/{name})"
                       "{ .uml }")
        number = end + 1
    return "\n".join(out), diagrams, used


def svgbob_svg(art: str) -> str | None:
    """ASCII-piirros -> SVG:n rivit yhtenä merkkijonona, tai None.

    Nimi on piirroksen sha1, joten muuttunut piirros piirretään uudelleen ja
    muuttumaton luetaan välimuistista. None tarkoittaa, ettei svgbobia ole
    asennettu: silloin aita jätetään ennalleen eikä käännös kaadu.
    """
    path = SVGBOB_DIR / (hashlib.sha1(art.encode("utf-8")).hexdigest() + ".svg")
    if path.is_file():
        return path.read_text(encoding="utf-8")
    try:
        result = subprocess.run(SVGBOB_COMMAND, input=art, capture_output=True,
                                text=True, check=True)
    except FileNotFoundError:
        print("varoitus: svgbob_cli puuttuu, ascii-kaaviot jäävät koodilohkoiksi"
              " (cargo install svgbob_cli)", file=sys.stderr)
        return None
    except subprocess.CalledProcessError as error:
        print(f"varoitus: svgbob epäonnistui: {error.stderr.strip()}",
              file=sys.stderr)
        return None
    SVGBOB_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(result.stdout, encoding="utf-8")
    return result.stdout


def svgbob_prefix_ids(svg: str, number: int) -> str:
    """Kaavion tunnisteet ja niiden viittaukset omaan nimiavaruuteensa.

    Ks. SVGBOB_ID_RE: ilman tätä saman sivun kaavioilla on samat tunnisteet.
    """
    svg = SVGBOB_ID_RE.sub(lambda m: f'id="bob{number}-{m["name"]}"', svg)
    return SVGBOB_REF_RE.sub(lambda m: f'url(#bob{number}-{m["name"]})', svg)


def convert_svgbob(text: str) -> tuple[str, int, set[str]]:
    """```bob-aidat upotetuiksi SVG-kaavioiksi. -> (teksti, kaavioita, nimet).

    Ilman muunnosta piirros on sivulla koodilohkona, ks. SVGBOB_FENCE_RE.
    Ajetaan convert_divsin jälkeen: muuten kääre saisi markdown="1":n ja
    md_in_html yrittäisi jäsentää SVG:n sisällön Markdownina.

    Aineistossa yksikään bob-aita ei ole välilehtijoukon sisällä eikä
    sisennettynä, mutta aidan sisennys kirjoitetaan silti kääreeseen, jotta
    kaavio pysyisi omalla tasollaan myös sisennetyssä lohkossa.
    """
    lines = text.split("\n")
    out: list[str] = []
    used: set[str] = set()
    diagrams = 0
    number = 0
    while number < len(lines):
        match = SVGBOB_FENCE_RE.match(lines[number])
        if not match:
            out.append(lines[number])
            number += 1
            continue
        end = number + 1
        while end < len(lines) and lines[end].strip() != match["fence"]:
            end += 1
        if end == len(lines):  # sulkematon aita: jätetään rauhaan
            out.append(lines[number])
            number += 1
            continue
        art = "\n".join(lines[number + 1:end]) + "\n"
        svg = svgbob_svg(art)
        if svg is None:
            out.extend(lines[number:end + 1])
        else:
            used.add(hashlib.sha1(art.encode("utf-8")).hexdigest() + ".svg")
            diagrams += 1
            svg = svgbob_prefix_ids(svg, diagrams)
            indent = match["indent"]
            out.append(f'{indent}<div class="svgbob">')
            out += [indent + line for line in svg.split("\n") if line.strip()]
            out.append(f"{indent}</div>")
        number = end + 1
    return "\n".join(out), diagrams, used


def summary_has_blank_line(lines: list[str], number: int) -> bool:
    """Onko rivillä alkavassa yhteenvedossa tyhjä rivi ennen </summary>:ä?

    Se on raja, jonka takana yhteenveto on Markdownia myös kirjassa, ks.
    SUMMARY_RE. Yhden rivin yhteenveto ja sulkematta jäänyt tagi vastaavat
    molemmat ei.
    """
    start = lines[number].find("<summary")
    if start < 0 or SUMMARY_END in lines[number][start:]:
        return False
    for line in lines[number + 1:]:
        if SUMMARY_END in line:
            return False
        if not line.strip():
            return True
    return False


def convert_details(text: str) -> tuple[str, int, int]:
    """<details> ja monirivinen <summary> markdown-attribuutilla.

    -> (teksti, details-tageja, summary-tageja).

    Ilman attribuuttia lohkon sisältö menee sivulle lähdemuodossaan, ks.
    DETAILS_RE ja SUMMARY_RE. Koodiaidat ohitetaan, jottei aidan sisällä oleva
    HTML-esimerkki muuttuisi; aidat käydään pareittain kuten convert_fencesissä.
    Aineistossa yhtään <details>-tagia ei tällä hetkellä ole aidan sisällä,
    mutta samaa varovaisuutta noudatetaan kuin muissakin muunnoksissa.
    """
    lines = text.split("\n")
    out: list[str] = []
    open_fence: str | None = None
    tags = summaries = 0
    for number, line in enumerate(lines):
        match = CODE_FENCE_RE.match(line)
        if match and open_fence is None:
            open_fence = match["fence"]
        elif (match and not match["info"].strip()
                and len(match["fence"]) >= len(open_fence)):
            open_fence = None
        elif open_fence is None:
            line, found = DETAILS_RE.subn(
                lambda m: f'<details{m["attrs"]} markdown="1">', line)
            tags += found
            if summary_has_blank_line(lines, number):
                line, found = SUMMARY_RE.subn(
                    lambda m: f'<summary{m["attrs"]} markdown="block">', line)
                summaries += found
        out.append(line)
    return "\n".join(out), tags, summaries


def drop_breaks(text: str) -> tuple[str, int]:
    """Omaksi kappaleekseen jäänyt <br />-rivi pois. -> (teksti, rivejä).

    Ks. BREAK_LINE_RE. Tyhjä rivi kummallakin puolella on ehto, koska juuri se
    tekee rivistä oman kappaleen; toinen niistä poistetaan tagin mukana, jottei
    tilalle jäisi kahta peräkkäistä tyhjää riviä. Koodiaidat ohitetaan
    pareittain kuten convert_detailsissä, jottei koodilohkossa näytetty
    HTML-esimerkki muuttuisi.
    """
    lines = text.split("\n")
    out: list[str] = []
    open_fence: str | None = None
    breaks = 0
    drop_blank = False
    for number, line in enumerate(lines):
        match = CODE_FENCE_RE.match(line)
        if match and open_fence is None:
            open_fence = match["fence"]
        elif (match and not match["info"].strip()
                and len(match["fence"]) >= len(open_fence)):
            open_fence = None
        elif open_fence is None and BREAK_LINE_RE.match(line):
            before = out[-1].strip() if out else ""
            after = lines[number + 1].strip() if number + 1 < len(lines) else ""
            if not before and not after:
                breaks += 1
                drop_blank = True
                continue
        if drop_blank:
            drop_blank = False
            if not line.strip():
                continue
        out.append(line)
    return "\n".join(out), breaks


def convert_divs(text: str) -> tuple[str, int]:
    """Rivin aloittava <div> -> <div markdown="1">. -> (teksti, tageja).

    Ilman attribuuttia divin sisältö menee sivulle lähdemuodossaan, ks. DIV_RE.
    Vain rivin aloittava tagi muunnetaan: Python-Markdown tunnistaa lohkotason
    HTML:n vain omana kappaleenaan, joten kesken kappaleen olevalle diville
    attribuutti ei tekisi mitään. Koodiaidat ohitetaan pareittain kuten
    convert_detailsissä.

    Ajetaan ennen convert_tasksia, joten muunnos näkee vain lähteen omat divit:
    tehtäväkorttien divit syntyvät vasta sen jälkeen ja saavat attribuuttinsa
    (tai jäävät tarkoituksella ilman) siellä.
    """
    out: list[str] = []
    open_fence: str | None = None
    tags = 0
    for line in text.split("\n"):
        match = CODE_FENCE_RE.match(line)
        if match and open_fence is None:
            open_fence = match["fence"]
        elif (match and not match["info"].strip()
                and len(match["fence"]) >= len(open_fence)):
            open_fence = None
        elif open_fence is None and line.lstrip().startswith("<div"):
            line, found = DIV_RE.subn(
                lambda m: f'<div{m["attrs"]} markdown="1">', line)
            tags += found
        out.append(line)
    return "\n".join(out), tags


def task_head(match: re.Match[str]) -> str:
    """<task-title num="2.1">Kello<points>1 p.</points></task-title> -> tunnusrivi.

    Osat erotellaan sisemmistä tageista: numero attribuutista, pisteet
    <points>-elementistä ja bonusmerkintä <i class="bi bi-stars">-tagista.
    Bonusliuska jää nimen sisään, jotta se seuraa nimen viimeistä sanaa myös
    silloin kun nimi rivittyy kapealla palstalla.
    """
    inner = match["inner"]
    points = TASK_POINTS_RE.search(inner)
    inner = TASK_POINTS_RE.sub("", inner)
    bonus = TASK_BONUS_RE.search(inner) is not None
    name = TASK_BONUS_RE.sub("", inner).strip()
    if bonus:
        name += ' <span class="task-bonus">Bonus</span>'
    parts = [f'<span class="task-num">{match["num"]}</span>',
             f'<span class="task-name">{name}</span>']
    if points:
        parts.append(f'<span class="task-points">{points["points"].strip()}</span>')
    return '<div class="task-head">' + "".join(parts) + "</div>"


def convert_tasks(text: str) -> tuple[str, int]:
    """<task>-kortit diveiksi. -> (teksti, kortteja).

    Ilman muunnosta koko kortti jää kappaleen sisään ja tehtävänannon
    Markdown jäsentyy väärään paikkaan, ks. TASK_TAG_RE. Koodiaidat
    ohitetaan pareittain kuten convert_detailsissä, jottei aidan sisällä
    näytetty esimerkki muuttuisi.

    Tagirivien sisennys poistetaan ja jokainen niistä erotetaan tyhjällä
    rivillä: Python-Markdown tunnistaa lohkotason HTML:n vain omana
    kappaleenaan, ja neljällä välilyönnillä sisennetty rivi olisi
    koodilohko. Sisennys on lähteessä pelkkää muotoilua — aineistossa sitä
    on neljää eri syvyyttä samoille tageille.

    Muunnos on toistokelpoinen ilman erillistä tarkistusta: valmiissa
    tekstissä ei ole enää yhtään tagia, johon TASK_TAG_RE osuisi.
    """
    out: list[str] = []
    open_fence: str | None = None
    cards = 0
    skip_blank = False
    for line in text.split("\n"):
        match = CODE_FENCE_RE.match(line)
        if match and open_fence is None:
            open_fence = match["fence"]
        elif (match and not match["info"].strip()
                and len(match["fence"]) >= len(open_fence)):
            open_fence = None
        elif open_fence is None and TASK_TAG_RE.search(line):
            cards += line.count("<task>")
            converted = TASK_TITLE_RE.sub(task_head, line.strip())
            for tag, replacement in TASK_TAGS:
                converted = converted.replace(tag, replacement)
            if out and out[-1].strip():
                out.append("")
            out.append(converted)
            out.append("")
            # Lähteessä on tagin perässä usein jo tyhjä rivi; sitä ei oteta
            # toiseen kertaan, jotta docs/ pysyy luettavana.
            skip_blank = True
            continue
        if skip_blank and not line.strip():
            skip_blank = False
            continue
        skip_blank = False
        out.append(line)
    return "\n".join(out), cards


def split_files(body: list[str]) -> list[tuple[str, list[str]]]:
    """Koodiaidan rivit -> [(tiedostonimi, rivit)] FILE-merkintöjen mukaan.

    Merkinnän ulkopuolelle jäävät rivit eivät kuulu mihinkään tiedostoon, eikä
    niitä ole aineistossa yhtään; convert_files tarkistaa sen erikseen eikä
    kutsu tätä, jos niitä on. Tyhjä lista = lohkossa ei ole merkintöjä.
    """
    files: list[tuple[str, list[str]]] = []
    name: str | None = None
    content: list[str] = []
    for line in body:
        begin = FILE_BEGIN_RE.match(line)
        if begin:
            if name is not None:
                files.append((name, content))
            name, content = begin["name"], []
        elif FILE_END_RE.match(line):
            if name is not None:
                files.append((name, content))
            name, content = None, []
        elif name is not None:
            content.append(line)
    if name is not None:
        files.append((name, content))
    return files


def convert_files(text: str) -> tuple[str, int, int]:
    """mdBookin monitiedostolohkot -> pymdownx.tabbed. -> (teksti, lohkot, tiedostot).

    Jokainen tiedosto omaksi välilehdekseen ja omaksi koodiaidakseen. Sama
    mekanismi kuin convert_tabsissa, joten tästä ei tule omaa CSS:ää eikä
    JavaScriptiä: Material antaa välilehdet, Pygments korostuksen ja
    Zensical kopiointinapin. Myös tulostus tulee valmiina — Materialin
    print-säännöissä .tabbed-labels ja .tabbed-content ovat display: contents
    ja order lomittaa otsikot ja lohkot, joten paperille tulee jokainen
    tiedosto oman nimensä alle kuten mdBookissa.

    Jokainen tiedosto saa alkuperäisen aidan otsikon fence_infon kautta, eli
    myös lohkon mahdolliset määreet (java,ignore -> { .java .ignore }). Yksi
    lohko on ilman kieltä (.fxml-tiedostoja) ja jää sellaiseksi, kuten
    mdBookissakin.

    Ero mdBookiin: yhden tiedoston lohkot saavat yhden välilehden rivin, ja
    Materialin content.tabs.link yhdistää samannimiset välilehdet, ks. README.md.
    """
    lines = text.split("\n")
    out: list[str] = []
    blocks = files = 0
    index = 0
    while index < len(lines):
        fence = CODE_FENCE_RE.match(lines[index])
        if not fence:
            out.append(lines[index])
            index += 1
            continue
        marker = fence["fence"]
        close_re = re.compile(rf"^{marker[0]}{{{len(marker)},}}\s*$")
        end = index + 1
        while end < len(lines) and not close_re.match(lines[end]):
            end += 1
        body = lines[index + 1:end]
        begins = [i for i, line in enumerate(body) if FILE_BEGIN_RE.match(line)]
        # Sulkematon aita, tavallinen koodilohko tai lohko, jossa on koodia
        # ennen ensimmäistä merkintää: jätetään sellaisenaan. Viimeisestä
        # varoitetaan, koska muunnos pudottaisi rivit hiljaisesti pois.
        if begins and any(line.strip() for line in body[:begins[0]]):
            print(f"varoitus: koodia ennen ensimmäistä // FILE: -merkintää, "
                  f"lohko jätetään ennalleen: {lines[index]}", file=sys.stderr)
        if end >= len(lines) or not begins or any(line.strip()
                                                  for line in body[:begins[0]]):
            out.extend(lines[index:end + 1])
            index = end + 1
            continue
        info = fence_info(fence["info"])
        if out and out[-1].strip():
            out.append("")
        blocks += 1
        for name, content in split_files(body):
            files += 1
            out.append(f'=== "{name}"')
            out.append("")
            out.extend(indent_block([f"{marker}{info}", *content, marker]))
            out.append("")
        index = end + 1
    return "\n".join(out), blocks, files


def convert_tabs(text: str) -> tuple[str, int, int, set[str]]:
    """mdBookin #tab/-lohkot -> pymdownx.tabbed. -> (teksti, joukkoja, poistettuja, otsikot).

    Ainoa sisältömuunnos tässä skriptissä, ks. README.md. Zensicalissa
    välilehdet ovat oletuksena päällä (pymdownx.tabbed, alternate_style),
    joten mkdocs.yml:ään ei tule laajennusta vaan pelkkä content.tabs.link.

    Kaksi eroa mdBookiin, molemmat siitä että Zensicalissa yksi välilehti on
    aina valittuna:

    * #tab/default jää pois. Se on mdBookissa se mitä näkyy ennen valintaa,
      eikä sellaista tilaa täällä ole.
    * Saman tunnuksen välilehdet saavat saman otsikon, ensimmäisen esiintymän
      mukaan. mdBook yhdisti sivun välilehtijoukot tunnuksesta (#tab/gitlab),
      Material otsikkotekstistä — muuten "GitLab (JY)" ja "GitLab (JYU)"
      jäisivät samalla sivulla erillisiksi valinnoiksi.
    """
    lines = text.split("\n")
    labels: dict[str, str] = {}
    out: list[str] = []
    sets = placeholders = 0
    index = 0
    while index < len(lines):
        if not TAB_HEADING_RE.match(lines[index]):
            out.append(lines[index])
            index += 1
            continue
        sections, index = read_tab_set(lines, index)
        placeholders += sum(1 for tab_id, _, _ in sections
                            if tab_id == TAB_PLACEHOLDER)
        sections = [s for s in sections if s[0] != TAB_PLACEHOLDER]
        # Tyhjä rivi joukon eteen myös silloin kun koko joukko jäi pois:
        # read_tab_set söi joukon jälkeiset tyhjät rivit, joten ilman tätä
        # sitä edeltävä ja seuraava kappale liimautuisivat yhteen.
        if out and out[-1].strip():
            out.append("")
        if not sections:
            continue
        sets += 1
        for tab_id, label, body in sections:
            out.append(f'=== "{labels.setdefault(tab_id, label)}"')
            out.append("")
            out.extend(indent_block(body))
            out.append("")
    return "\n".join(out), sets, placeholders, set(labels.values())


def main() -> int:
    if not SRC.is_dir():
        print(f"lähdepuu puuttuu: {SRC}", file=sys.stderr)
        return 1
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(SRC, DOCS)
    (DOCS / "SUMMARY.md").unlink(missing_ok=True)
    sets = placeholders = blocks = files = fences = includes = alerts = 0
    details = summaries = divs = tasks = diagrams = drawings = 0
    breaks = 0
    used_diagrams: set[str] = set()
    used_drawings: set[str] = set()
    tab_labels: set[str] = set()
    unknown_alerts: set[str] = set()
    for page in sorted(DOCS.rglob("*.md")):
        source = page.read_text(encoding="utf-8")
        # Sisällytykset ennen kaikkea muuta, kuten mdBookissa: muut muunnokset
        # käsittelevät myös sisällytetyn tekstin (43 tehtävänannossa on
        # koodiaita), ja koodiaidan sisällä olevat sisällytykset ovat vasta
        # tämän jälkeen sitä koodia, jonka convert_files jakaa välilehdiksi.
        converted, page_includes = convert_includes(
            source, SRC / page.relative_to(DOCS))
        # Monitiedostolohkot ennen aitoja: silloin ne toimivat myös #tab/-osion
        # sisällä, koska convert_tabs sisentää valmiin välilehtijoukon
        # sisäkkäiseksi. Toisin päin sisennetty aita jäisi tunnistamatta.
        converted, page_blocks, page_files = convert_files(converted)
        # Aidat ennen välilehtiä: convert_tabs sisentää osion sisällön, ja
        # sisennetty aita jää tunnistamatta. convert_files kirjoittaa omat
        # aitansa jo valmiiksi oikeaan muotoon.
        converted, page_fences = convert_fences(converted)
        # Luokkakaaviot aitojen jälkeen ja välilehtien edellä: convert_tabs
        # sisentää osion sisällön, ja sisennetty aita jäisi tunnistamatta.
        # Sisällytysten jälkeen, koska kaksi kaaviota on tehtävänannoissa.
        converted, page_diagrams, page_used = convert_plantuml(converted, page)
        # Alertit ennen välilehtiä: convert_tabs sisentää osion sisällön, ja
        # sisennetty ">" ei ole enää lainauslohkon alku. Toisin päin alertti
        # jäisi välilehden sisällä kääntämättä.
        converted, page_alerts, page_unknown = convert_alerts(converted)
        # <details>- ja <summary>-tagit: paikalla ei ole väliä, sillä mikään muu
        # muunnos ei koske raakaan HTML:ään eikä tämä muuhun kuin avaustagien
        # attribuutteihin.
        converted, page_details, page_summaries = convert_details(converted)
        # <br />-rivit heti details-lohkojen jälkeen: kohde on sama eli lohkojen
        # väli, ks. drop_breaks. Muihin muunnoksiin nähden järjestyksellä ei ole
        # väliä; sisällytysten jälkeen kuten kaikki muutkin, koska kolme
        # neljästä rivistä on tehtävänannoissa.
        converted, page_breaks = drop_breaks(converted)
        # Divit ennen tehtäväkortteja: silloin muunnos näkee vain lähteen omat
        # divit, ei convert_tasksin kirjoittamia. Ks. convert_divs.
        converted, page_divs = convert_divs(converted)
        # ASCII-kaaviot divien jälkeen: convert_divs lisäisi kääreeseen
        # markdown="1":n, ja md_in_html yrittäisi jäsentää SVG:n Markdownina.
        converted, page_drawings, page_art = convert_svgbob(converted)
        # Tehtäväkortit ennen välilehtiä: convert_tabs sisentää osion sisällön
        # neljällä välilyönnillä, ja sisennetty HTML-lohko olisi koodilohko.
        # Muihin muunnoksiin nähden järjestyksellä ei ole väliä: tämä koskee
        # vain <task>-tageja eikä mikään muu muunnos koske niihin.
        converted, page_tasks = convert_tasks(converted)
        converted, page_sets, page_placeholders, page_labels = convert_tabs(converted)
        if converted != source:
            page.write_text(converted, encoding="utf-8")
        sets += page_sets
        placeholders += page_placeholders
        tab_labels |= page_labels
        blocks += page_blocks
        files += page_files
        fences += page_fences
        includes += page_includes
        alerts += page_alerts
        details += page_details
        summaries += page_summaries
        breaks += page_breaks
        divs += page_divs
        tasks += page_tasks
        diagrams += page_diagrams
        used_diagrams |= page_used
        drawings += page_drawings
        used_drawings |= page_art
        unknown_alerts |= page_unknown
    for old_path, new_path in nest_moves().items():
        source = DOCS / old_path
        if not source.is_file():
            print(f"varoitus: NEST_UNDER viittaa puuttuvaan sivuun: {old_path}",
                  file=sys.stderr)
            continue
        target = DOCS / new_path
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
    shutil.copytree(ASSETS, DOCS / "assets", dirs_exist_ok=True)
    nav = build_nav()
    (ROOT / "nav.yml").write_text(nav + build_extra(tab_labels), encoding="utf-8")
    (DOCS / PRINT_PAGE).write_text(build_print_page(nav), encoding="utf-8")
    print(f"kopioitu {len(list(DOCS.rglob('*.md')))} markdown-tiedostoa -> {DOCS}")
    print(f"välilehdet: {sets} joukkoa, {placeholders} #tab/default-lohkoa pois")
    print(f"monitiedostolohkot: {blocks} lohkoa, {files} tiedostoa")
    print(f"aidan attribuutit: {fences} aitaa")
    print(f"sisällytykset: {includes} makroa")
    print(f"details-lohkot: {details} tagia, {summaries} monirivistä summarya, "
          f"{breaks} <br />-riviä pois")
    print(f"divit: {divs} tagia")
    print(f"luokkakaaviot: {diagrams} kaaviota, "
          f"{prune_diagrams(PLANTUML_DIR, used_diagrams)} käyttämätöntä poistettu")
    print(f"ascii-kaaviot: {drawings} kaaviota, "
          f"{prune_diagrams(SVGBOB_DIR, used_drawings)} käyttämätöntä poistettu")
    print(f"tehtäväkortit: {tasks} korttia")
    print(f"alertit: {alerts} lohkoa"
          + (f", tuntematon tunnus: {', '.join(sorted(unknown_alerts))}"
             if unknown_alerts else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
