#!/usr/bin/env python3
"""Kääntää mdBookin lähdepuun (../src) Zensicalin docs/-hakemistoksi.

Yksi ajo tekee viisi vaihetta tässä järjestyksessä (main):

1. Muut kuin Markdown-tiedostot paikalleen (sync_docs). Kuvat ja liitteet
   kopioidaan suoraan lopulliseen paikkaansa NEST_UNDER-siirtoineen, ja
   SUMMARY.md jätetään kopioimatta: siitä tulee navigaatio eikä sivu. Samalla
   selviää, mitä docs/:ssa on edellisen ajon jäljiltä — poisto on vaiheessa 5.

2. Jokainen sivu erikseen: sivu luetaan lähdepuusta, ajetaan viidentoista
   muunnoksen läpi ja kirjoitetaan docs/:iin, jos tulos muuttui. Muunnokset
   ajojärjestyksessä:

    1. drop_sections       DROP_SECTIONS-osio pois: mdBookin käyttöliittymää
                           kuvaava neuvo, joka ei täällä pidä paikkaansa
    2. convert_includes    {{#include}} -> tiedoston sisältö
    3. convert_anchors     ääkköset pois linkin ankkurista (#käyttö ->
                           #kaytto) ja välilyönti otsikon oman tunnuksen eteen
    4. convert_files       // FILE: -> välilehti per tiedosto
    5. convert_fences      aidan attribuutit (java,ignore) pymdownx:n muotoon,
                           ja samalla piilorivit (hide_lines) ja korostukset
                           (mark_highlights) aidan attribuutiksi
    6. convert_plantuml    plantuml-aita kuvaksi (SVG assets/plantuml/:iin)
    7. convert_alerts      > [!VINKKI] -> !!! tip "Vinkki"
    8. convert_details     <details> -> <details markdown="1">
    9. drop_breaks         lohkojen väliset <br />-rivit pois
   10. convert_divs        rivin aloittava <div> -> <div markdown="1">
   11. convert_svgbob      bob-aita upotetuksi SVG:ksi (cache/svgbob/)
   12. convert_tasks       <task>-kortit diveiksi
   13. convert_bonus_marks <i class="bi bi-stars"> -> bonusmerkki
   14. convert_icons       loput ikonitagit merkeiksi ja teeman glyfeiksi
   15. convert_tabs        ### [Windows](#tab/win) -> === "Windows"

   Järjestys ei ole vapaa: kaksi ensimmäistä on tehtävä ennen kaikkea muuta ja
   convert_tabs viimeisenä, ja väliin jäävistä vain convert_anchors,
   convert_details ja drop_breaks voisivat olla missä tahansa. Perustelu on jokaisen kohdalla
   erikseen mainissa.

3. Assetit docs/assets/:iin (copy_if_changed). Tyylit, skriptit ja vaiheen 2
   piirtämät PlantUML-kuvat päätyvät sivustolle vain tätä kautta.

4. Navigaatio ja tulostussivu. build_nav kääntää src/SUMMARY.md:n nav.yml:ksi,
   jonka mkdocs.yml perii (INHERIT); build_extra lisää sen perään
   muokkauslinkin polkukartan ja välilehtimuistin sallitut otsikot; ja
   build_print_page tekee samasta nav-lohkosta docs/tulosta.md:n rungon.

5. Siivous ja raportti. Vaiheen 1 jäänteet poistetaan vasta nyt, kun kaikki muu
   on paikallaan, ja käyttämättömät kaaviotiedostot välimuisteista
   (prune_diagrams). Lopuksi tulostuu rivi jokaisesta muunnoksesta: luku on
   ainoa tapa huomata, että jokin lakkasi osumasta mihinkään.

Kaksi sääntöä pätee koko ajon läpi:

* Kirjoitetaan vain se, mikä oikeasti muuttui (write_if_changed,
  copy_if_changed). Se ei ole nopeusoptimointi vaan ehto sille, että muutos
  näkyy selaimessa lainkaan, ks. write_if_changed.
* Yksi ajo kerrallaan, myös eri prosesseista (only_one_run). Kaksi
  rinnakkaista ajoa sekoittaa docs/:n keskenään, ks. only_one_run.

Mitä ei muunneta: <asciinema>-upotukset (kohta 16). Tagi menee Markdownin läpi
sellaisenaan ja Zensical kirjoittaa sen suhteellisen osoitteen sivun uuteen
sijaintiin, joten muunnettavaa ei ole; soittimen tekee assets/js/asciinema.js.

Ajo ilman argumentteja muuntaa kerran. `--watch` jää seuraamaan lähdepuuta ja
assetteja ja ajaa muunnoksen jokaisesta muutoksesta; run.sh käynnistää sen
palvelimen rinnalle, ks. watch.

Generoitu docs/ on kertakäyttöinen — tämä skripti on totuus.
"""

import contextlib
import fcntl
import filecmp
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import traceback
import urllib.error
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "src"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

# Kuvakkeiden glyfit, ks. ICON_MAP. Kopioita eikä lukua suoraan teemalta,
# koska run.sh ajaa tämän skriptin systeemin python3:lla eikä .venv:stä:
# "import zensical" kaatuisi siihen, ja .venv:n polun arvaaminen sitoisi
# skriptin virtuaaliympäristön sisäiseen rakenteeseen. Tiedostot ovat
# sellaisenaan Zensical 0.0.60:n templates/.icons/-hakemistosta, ja testi
# vertaa niitä siihen (test_convert.py), joten ero näkyy heti kun teema
# vaihtaa glyfiä.
ICONS = ROOT / "icons"

SUMMARY_LINK_RE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>-\s*)?\[(?P<title>[^\]]*)\]\((?P<href>[^)]*)\)")

# mdBookin SUMMARY.md ei salli etulinkkien (prefix chapters) sisäkkäisyyttä:
# sisennetty rivi jää mdBookissa samalle tasolle ja jättää navigaatioon vielä
# tyhjän rivin. Zensicalissa sisäkkäisyys onnistuu, joten se tehdään tässä.
# Avain = alasivun polku, arvo = sen sivun polku, jonka alle se siirretään.
NEST_UNDER = {
    "tenttiohjeet.md": "tentti.md",
}

# Osiot, jotka kuvaavat mdBookin käyttöliittymää eivätkä pidä Zensicalissa
# paikkaansa. Ne eivät ole ikoni- vaan sisältöongelma: etusivun "Navigointi
# tässä materiaalissa" kertoo, että sivuja selataan nuolikuvakkeista sivun
# vasemmassa ja oikeassa laidassa, mutta Zensicalissa laitanuolia ei ole
# lainkaan — navigation.footer laittaa edellisen ja seuraavan linkit aina
# alalaitaan, myös työpöydällä. Osio jää siis pois kokonaan; sen kaksi muuta
# neuvoa (sisällysluettelo ja haku) ovat jo osan 1 etusivun listassa.
#
# Lähde ei muutu (README: "ei koske ../src:ään"), joten poisto tehdään tässä.
# Avain = sivun polku lähdepuussa, arvo = osion otsikko sellaisenaan.
DROP_SECTIONS = {
    "index.md": "Navigointi tässä materiaalissa",
}
HEADING_RE = re.compile(r"(?P<level>#+)\s+(?P<title>.*?)\s*$")

# Ankkurit, ks. convert_anchors (README kohta 13).
#
# Linkin ankkuriosa "](../sivu.md#käyttö)". Riisuttavaksi kelpaa vain
# sivuston oma linkki: ulkopuolisen osoitteen ankkuri kuuluu toisen sivuston
# tunnuksiin, joten skeemallinen kohde jätetään rauhaan (ks. convert_anchors).
ANCHOR_LINK_RE = re.compile(r"\]\((?P<target>[^)\s]*)#(?P<fragment>[^)\s]+)\)")

# Otsikon oma tunnus "## Otsikko{#tunnus}" ilman välilyöntiä aaltosulun edellä.
HEADING_ANCHOR_RE = re.compile(
    r"^(?P<heading>#+\s+\S.*?\S)(?P<anchor>\{#[^}\s]+\})\s*$")

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
# paikkaa; ks. PERUSTELUT.md.
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

# mdBookin piilorivit (book.toml: [output.html.code.hidelines]). Rivi, joka
# alkaa etuliitteellä "//-", kuuluu ohjelmaan muttei näy sivulla: mdBook riisuu
# etuliitteen käännösaikana ja kääri rivin <span class="boring">iin, jonka
# book.js piilottaa ja silmänappi näyttää. Etuliite on kirjassa määritelty
# javalle ja javascriptille, ei muille kielille, joten muut kielet jäävät
# rauhaan — myös silloin kun niissä sattuisi olemaan sama merkkijono.
#
# Rivin alussa voi olla myös lainausmerkkejä: kolme lohkoa on alertin sisällä
# (osa1/02, "> ```java"), ja siellä jokaisella rivillä on ">"-etuliite, koska
# convert_alerts purkaa lainauksen vasta myöhemmin. Ne otetaan talteen ja
# kirjoitetaan takaisin sellaisinaan, jotta lainaus pysyy ehjänä.
HIDELINE_RE = re.compile(r"^((?:[ \t]*>)*[ \t]*)//-")
HIDELINE_LANGUAGES = ("java", "javascript")

# mdBookin korostusmerkinnät (theme/code-highlights.js ja code-highlights.css).
# Koodiaidan sisällä rivi "// HIGHLIGHT_GREEN_BEGIN" aloittaa ja "..._END"
# lopettaa alueen, jonka riveille tulee värillinen tausta; merkintärivit itse
# eivät näy sivulla. Aineistossa värejä on kolme (green 81 aluetta, red 20,
# yellow 19) ja kirjan CSS tuntee neljännen (blue).
#
# Väli "//":n ja tunnuksen välissä on milloin on milloin ei
# ("//HIGHLIGHT_GREEN_BEGIN", extra/luetelma), ja rivi on useimmiten
# sisennetty. mdBookin oma lauseke sallii molemmat, ja sama sietokyky on
# tässä; lisäksi rivin alussa sallitaan lainausmerkki samasta syystä kuin
# piiloriveillä, vaikkei yksikään alue ole aineistossa alertin sisällä.
HIGHLIGHT_RE = re.compile(
    r"^[\s>]*//\s*HIGHLIGHT_(?P<color>[A-Z0-9]+)_(?P<edge>BEGIN|END)\s*$")
HIGHLIGHT_COLORS = ("green", "yellow", "red", "blue")

# mdBookin skripti käy läpi vain "pre > code.language-java", eli missä tahansa
# muussa kielessä sama rivi on tavallinen kommentti. Sama rajaus tässä;
# aineistossa jokainen 76 lohkosta on javaa.
HIGHLIGHT_LANGUAGES = ("java",)

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
# Bonusmerkki jää nimen *sisälle*, kuten lähteessäkin; tyyli tekee siitä
# liuskan (ks. BONUS_MARK_PATH).
TASK_TAG_RE = re.compile(r"</?(?:task|task-title|task-link|handout)[ >]")
TASK_TITLE_RE = re.compile(
    r'<task-title\s+num="(?P<num>[^"]*)"\s*>(?P<inner>.*?)</task-title>')
TASK_POINTS_RE = re.compile(r"<points>(?P<points>.*?)</points>")

# Bonusmerkki. Lähteessä se on <i class="bi bi-stars"> kolmessa paikassa:
# tehtävän nimen sisällä (36), avattavien lohkojen <summary>-riveillä (21) ja
# harjoitustyön vaatimuslistoissa (9). Bootstrap Iconsia ei ladata (kohta 17),
# joten merkki piirretään Materialin creation-kuvakkeella: kolme kimallusta,
# sama sommittelu kuin bi-starsissa. Polku on Zensicalin omasta
# ikonihakemistosta (.icons/material/creation.svg) sellaisenaan.
#
# Kuvake kirjoitetaan valmiiksi inline-SVG:ksi eikä lyhytkoodiksi
# (:material-creation:), vaikka teema osaa lyhytkoodin ilman yhtään riviä
# mkdocs.yml:ään. Syy on <summary>: Python-Markdown ei jäsennä sen sisältöä,
# koska markdown="1" on <details>-tagissa ja md_in_html käsittelee sillä vain
# lohkotason lapset. Mitattuna lyhytkoodi kääntyy listassa ja kappaleessa
# mutta jää <summary>-rivillä raakana näkyviin — ja siellä on 21 merkkiä
# kolmestakymmenestä. Sama merkintä kaikkiin kolmeen paikkaan on siis ainoa,
# joka kääntyy kaikissa.
#
# Kääre .twemoji on teeman oma ikonikääre, sama jonka lyhytkoodi tuottaisi,
# joten koon (--md-icon-size), kohdistuksen (vertical-align: text-top) ja
# värin periytymisen (fill: currentcolor) hoitaa teeman CSS. Omaa sääntöä
# tarvitaan vain väriin, ks. assets/css/tasks.css.
BONUS_TAG_RE = re.compile(r'<i\s+class="[^"]*\bbi-stars\b[^"]*"\s*>\s*</i>')
BONUS_MARK_PATH = (
    "m19 1-1.26 2.75L15 5l2.74 1.26L19 9l1.25-2.74L23 5l-2.75-1.25"
    "M9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5"
    "M19 15l-1.26 2.74L15 19l2.74 1.25L19 23l1.25-2.75L23 19l-2.75-1.26")

# Rivillä jo oleva bonussana. Kirjassa merkki on ikonifontti ilman nimeä, eli
# ruudunlukija ei saa siitä mitään; tässä se nimetään silloin kun rivillä ei
# ole samaa tietoa tekstinä. <summary>-rivit alkavat sanalla "Bonus:" tai
# "Valinnaista lisätietoa:", jolloin nimi vain toistaisi otsikon, mutta
# harjoitustyön vaatimuslistassa merkki on rivin ainoa ero pakolliseen
# vaatimukseen.
BONUS_WORD_RE = re.compile(r"bonus|valinnais", re.IGNORECASE)
TASK_TAGS = (
    ("<task>", '<div class="task" markdown="1">'),
    ("</task>", "</div>"),
    ("<handout>", '<div class="task-handout" markdown="1">'),
    ("</handout>", "</div>"),
    ("<task-link>", '<div class="task-link">'),
    ("</task-link>", "</div>"),
)

# Loput ikonit. Lähteessä ne ovat Bootstrap Iconsin tageja
# (<i class="bi bi-play-fill">) ja kolmessa kohdassa Font Awesomen
# (<i class="fa fa-eye">). Kumpaakaan fonttia ei ladata, joten sivulla ne ovat
# tyhjää tilaa. Lähdepuussa tageja on 150: bonusmerkki (bi-stars) on niistä 66
# ja hoidettu edellä, DROP_SECTIONS vie mennessään neljä, ja loput 80
# jakautuvat kahtia — 58 valikkopolun nuolta ja 22 oikeaa kuvaketta.
#
# Tagia ei etsitä riviltä vaan koko tekstistä, koska lähteessä 19 tagia on
# rivitetty kesken tagin. Katkos on kahdessa paikassa, <i:n ja class="bi:n
# jäljessä, ja kahdessa tapauksessa jatkorivi on lainauslohkossa, jolloin
# väliin tulee myös lainausmerkki:
#
#     **File** <i class="bi
#     > bi-chevron-right"></i> **Settings**
#
# Siksi tagin sisäinen väli on [\s>]+ eikä \s+. Se on turvallista juuri
# tässä: kohta on lainausmerkkien sisällä eli attribuutin arvossa, jossa ">"
# ei voi olla mitään muuta kuin lainauslohkon merkki. Takaisinviittaus
# (?P=prefix) pitää parit erillään: bi bi- ja fa fa-, ei ristiin.
ICON_TAG_RE = re.compile(
    r'<i[\s>]+class="(?P<prefix>bi|fa)[\s>]+(?P=prefix)-(?P<name>[a-z0-9-]+)'
    r'[^"]*"\s*>\s*</i>')

# Valikkopolun nuoli on tageista 58 eli kolme neljäsosaa (bi-chevron-right 56,
# bi-arrow-right 2). Se ei ole kuvake vaan välimerkki: se erottaa valikon
# kohdat toisistaan (File › New › Project). Siihen riittää merkki, eikä
# merkki tarvitse fonttia, SVG:tä eikä yhtään tavua verkosta.
#
# Merkiksi valittiin › (U+203A), ja ratkaisu on kirjasimessa. Zensical hakee
# leipätekstin Source Serif 4:n Google Fontsista, ja sen latin-osajoukko
# kattaa alueet U+0000–00FF ja U+2000–206F: › osuu jälkimmäiseen ja » (U+00BB)
# edelliseen, eli kirjan oma kirjasin piirtää molemmat. Nuoli → (U+2192) ei
# osu kumpaankaan — osajoukon nuolista mukana ovat vain ↑ ja ↓ — eikä kolmio
# ▸ (U+25B8), joten selain hakisi ne varakirjasimesta kesken virkkeen.
#
# Merkki jää lisäksi tekstiksi: se menee hakuindeksiin ja ruudunlukija saa
# siitä välimerkin, kun ikonifontin glyfi oli kummallekin tyhjää.
#
# Väri vaimennetaan omalla luokalla (assets/css/icons.css), jotta erotin
# erottuu polun kohdista silloinkin kun ne on lihavoitu.
PATH_ARROW_ICONS = ("bi-chevron-right", "bi-arrow-right")
PATH_ARROW = '<span class="jyu-path">›</span>'

# Loput 22 tagia ovat oikeita kuvakkeita: käyttöliittymän painikkeita, joihin
# teksti viittaa ("ajopainikkeesta (<i class="bi bi-play-fill">)"). Niissä
# kuvakkeen tehtävä on näyttää se nappi, jota lukija etsii ruudulta, joten
# glyfi otetaan sieltä mistä sivusto itse ottaa omansa — silloin ohje ei voi
# näyttää eri kuvaketta kuin nappi, johon se osoittaa:
#
#   - yläpalkin napit ovat overrides/partials/header.html:ssä material/menu ja
#     material/magnify, tulostusnappi lucide/printer ja teemanappi
#     mkdocs.yml:n palettivalinnassa material/weather-night
#   - koodilohkon ajonappi on material/play (assets/css/playground.css) ja
#     piiloriviennappi material/eye-outline (assets/css/hidelines.css)
#
# Loput ovat IntelliJ:n ja SceneBuilderin painikkeita, joille valittiin
# Materialin lähin vastine. Ääriviivaversio siellä missä valinta on: täytetty
# lightbulb-on ja folder ovat leipätekstissä ympäristöään selvästi
# painavampia. Kaksi lähteen eri ikonia (bi-folder, bi-folder2) tarkoittaa
# samaa IntelliJ:n nappia, joten ne saavat saman glyfin.
#
# fa-history on ainoa, joka osoittaa nappiin jota sivustolla ei ole: se on
# muokattavan koodilohkon "Peruuta muutokset", ja ACE-editori on yhä tekemättä
# (README kohta 20). Kuvake piirretään silti, koska tyhjä väli ei kerro
# lukijalle enempää kuin väärä kuvake — korjattava on virke, ei glyfi.
#
# Glyfit ovat kopioina icons/-hakemistossa, ks. ICONS.
ICON_MAP = {
    "bi-layout-sidebar": "material/menu",
    "bi-list": "material/menu",
    "bi-search": "material/magnify",
    "bi-printer": "lucide/printer",
    "bi-circle-half": "material/weather-night",
    "bi-play-fill": "material/play",
    "fa-play": "material/play",
    "fa-eye": "material/eye-outline",
    "fa-history": "material/history",
    "bi-bug": "material/bug",
    "bi-folder": "material/folder-outline",
    "bi-folder2": "material/folder-outline",
    "bi-terminal": "material/console-line",
    "bi-gear-fill": "material/cog",
    "bi-lightbulb-fill": "material/lightbulb-on-outline",
    "bi-info-circle": "material/information-outline",
}


# Muunnoksen lukko, ks. only_one_run.
LOCK = ROOT / ".convert.lock"

# Kaaviot, joita ei tässä ajossa saatu piirrettyä (plantuml_svg, svgbob_svg).
# Moduulitason joukko eikä paluuarvo, koska muunnosfunktioiden kolmen mittaiset
# paluuarvot ovat testien varassa; main tyhjentää tämän joka ajon aluksi.
# Merkitystä on vain prune_diagramsille: epäonnistunut kaavio puuttuu käytettyjen
# joukosta, eikä siivota saa sen perusteella.
FAILED: set[str] = set()


def only_one_run():
    """Vain yksi muunnos kerrallaan, myös eri prosesseista. -> kontekstivaraaja.

    Kaksi yhtä aikaa ajavaa muunnosta sekoittaa docs/:n keskenään, ja
    seurauksena on tiedostojen katoaminen: mitattuna kaksi rinnakkaista
    ajoa (kaksi run.sh:ta) poisti kymmenen versionhallinnassa ollutta
    cache/svgbob/-tiedostoa. Toinen ajo näki sivun, jonka ensimmäinen oli
    jo muuntanut, ei löytänyt siitä bob-aitaa eikä siis laskenut kaaviota
    käytetyksi — ja prune_diagrams poisti sen. Vahti tekee tilanteesta
    tavallisen: kaksi avointa terminaalia riittää.

    Lukko on tiedostolukko eikä tiedoston olemassaolo, jotta se vapautuu
    itsestään myös silloin kun ajo tapetaan kesken kaiken.
    """
    return _locked()


@contextlib.contextmanager
def _locked():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


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


def prune_diagrams(folder: Path, used: set[str], complete: bool = True) -> int:
    """Käyttämättömät kaaviotiedostot pois. -> poistettuja.

    Nimi on kaavion lähteen sha1, joten muokattu kaavio jättäisi vanhan
    tiedoston hakemistoon ikuisiksi ajoiksi. Siivotaan vain, jos ajossa
    ylipäätään syntyi kaavioita: tyhjä joukko tarkoittaa, ettei piirtäjää
    saatu, eikä silloin saa poistaa sitä mitä levyllä jo on.

    complete=False tarkoittaa, että ainakin yksi kaavio jäi piirtämättä (ks.
    FAILED). Silloin käytettyjen joukko on vajaa eikä kerro, mikä on
    käyttämätöntä: puuttuva piirtäjä poistaisi juuri ne tiedostot, joita
    ilman piirtäjää eniten tarvitaan. Tiedostot ovat versionhallinnassa,
    joten poisto on menetettyä työtä eikä välimuistin uudelleentäyttö.
    """
    if not complete or not used or not folder.is_dir():
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


def drop_sections(text: str, relative: str) -> tuple[str, int]:
    """DROP_SECTIONS-osio pois sivulta. -> (teksti, osioita).

    Osio on otsikkorivi ja kaikki sen jälkeen aina seuraavaan samantasoiseen
    tai ylempään otsikkoon asti, eli juuri se mitä sisällysluettelossakin on
    otsikon alla. Tasoa verrataan ristikkojen määrästä, joten "## Navigointi"
    vie mukanaan omat ###-alaotsikkonsa mutta jättää seuraavan ##:n rauhaan.

    Ajetaan ensimmäisenä, ennen sisällytyksiä: silloin muut muunnokset eivät
    tee turhaa työtä poistuvalle tekstille eivätkä varoita siitä. Koodiaidat
    ohitetaan pareittain kuten convert_detailsissä, koska aidan sisällä rivin
    aloittava ristikko on kommentti eikä otsikko.
    """
    title = DROP_SECTIONS.get(relative)
    if title is None:
        return text, 0
    out: list[str] = []
    open_fence: str | None = None
    dropping = 0
    sections = 0
    for line in text.split("\n"):
        fence = CODE_FENCE_RE.match(line)
        if fence and open_fence is None:
            open_fence = fence["fence"]
        elif (fence and not fence["info"].strip()
                and len(fence["fence"]) >= len(open_fence)):
            open_fence = None
        match = HEADING_RE.match(line) if open_fence is None else None
        if match and dropping and len(match["level"]) <= dropping:
            dropping = 0
        if match and not dropping and match["title"] == title:
            dropping = len(match["level"])
            sections += 1
        if not dropping:
            out.append(line)
    if not sections:
        print(f"varoitus: DROP_SECTIONS-osiota ei löytynyt: {relative}: {title}",
              file=sys.stderr)
    return "\n".join(out), sections


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


def convert_anchors(text: str) -> tuple[str, int, int]:
    """Ankkurit Zensicalin muotoon. -> (teksti, linkkiä, otsikkoa).

    Kaksi eroa mdBookiin. Molemmat ovat sitä lajia, että linkki osoittaa
    mdBookissa olemassa olevaan otsikkoon mutta täällä ei mihinkään, ja
    molemmat näkyvät käännöksessä samana rivinä: "anchor does not exist".

    1. Ääkköset pois linkin ankkurista: "#käyttö" -> "#kaytto". Zensical tekee
       otsikon tunnuksen Python-Markdownin slugifylla
       (markdown.extensions.toc), joka normalisoi tekstin NFKD:llä ja pudottaa
       kaiken ascii-alueen ulkopuolisen; mdBook jättää ääkköset paikoilleen.
       Lähde kirjoittaa ankkurit mdBookin muodossa, joten sama riisuminen
       tehdään tässä linkin päähän. Vain ankkuriin: polut ovat jo
       ascii-muotoisia, ja skeemallinen osoite (https://...) ohitetaan
       kokonaan, koska sen ankkurin muodosta päättää toinen sivusto.

    2. Välilyönti otsikon oman tunnuksen eteen: "## Otsikko{#tunnus}" ->
       "## Otsikko {#tunnus}". Python-Markdownin attr_list vaatii
       välilyönnin aaltosulun edellä, mdBook ei; ilman sitä sulkulauseke jää
       otsikkotekstiin ja tunnukseksi tulee "otsikkotunnus". Lähdepuun 19
       tunnuksesta yksi on kirjoitettu näin.

    Sisällytysten jälkeen, jotta myös sisällytetyn tehtävänannon linkit
    tulevat mukaan. Koodiaidat ohitetaan pareittain kuten convert_detailsissä:
    aidassa näytetty linkki on esimerkki eikä linkki.
    """
    links = headings = 0

    def fold(match: re.Match) -> str:
        nonlocal links
        if "://" in match["target"]:
            return match[0]
        folded = (unicodedata.normalize("NFKD", match["fragment"])
                  .encode("ascii", "ignore").decode("ascii"))
        if folded == match["fragment"]:
            return match[0]
        links += 1
        return f']({match["target"]}#{folded})'

    out: list[str] = []
    open_fence: str | None = None
    for line in text.split("\n"):
        match = CODE_FENCE_RE.match(line)
        if match and open_fence is None:
            open_fence = match["fence"]
        elif (match and not match["info"].strip()
                and len(match["fence"]) >= len(open_fence)):
            open_fence = None
        elif open_fence is None:
            line, spaced = HEADING_ANCHOR_RE.subn(
                r"\g<heading> \g<anchor>", line)
            headings += spaced
            line = ANCHOR_LINK_RE.sub(fold, line)
        out.append(line)
    return "\n".join(out), links, headings


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


def fence_language(info: str) -> str:
    """Aidan otsikon kieli mdBookin muodossa: "java,ignore" -> "java".

    Valmiiksi pymdownx:n muodossa oleva otsikko ("{ .java .multifile }") ei
    palauta kieltä. Ne kirjoittaa convert_files, joka on käsitellyt oman
    lohkonsa piilorivit jo itse, eikä samaa runkoa pidä käsitellä kahdesti.
    """
    info = info.strip()
    return "" if info.startswith("{") else info.split(",")[0].strip()


def rendered_body(body: list[str]) -> tuple[int, int]:
    """Piirtyvän rungon rajat aidan sisällä. -> (ensimmäinen, viimeisen jälkeinen).

    Rivinumerot lasketaan siitä rungosta, joka lopulta piirretään: Markdown
    pudottaa aidan alusta ja lopusta tyhjät rivit. Mitattuna kolmessa lohkossa
    (osa1/02, alertin sisällä) aita alkaa kahdella tyhjällä rivillä, jolloin
    numerointi olisi muuten kaksi liikaa. Tyhjäksi lasketaan myös lainauslohkon
    oma rivi ("> "), koska lainausmerkki katoaa myöhemmin (convert_alerts).
    """
    first, last = 0, len(body)
    while first < last and not body[first].strip(" \t>"):
        first += 1
    while last > first and not body[last - 1].strip(" \t>"):
        last -= 1
    return first, last


def hide_lines(body: list[str], language: str) -> tuple[list[str], list[int]]:
    """Piiloriveiltä etuliite pois. -> (rivit, piilorivien numerot).

    mdBook riisuu etuliitteen ennen korostusta, joten piilotettu rivi on
    sivun HTML:ssä tavallista koodia — vasta CSS piilottaa sen. Sama tehdään
    tässä, ja kahdesta syystä juuri näin eikä esimerkiksi jättämällä etuliite
    paikalleen:

    * Rivi on ohjelmassa mukana. Ajonappi (kohta 3) lähettää lohkon koodin
      sellaisenaan, ja "//-" tekisi rivistä kommentin — 97 lohkoa 231:stä ei
      kääntyisi, koska juuri niissä riveissä on ohjelman runko.
    * Korostus menisi väärin. Koko rivi olisi Pygmentsille kommenttia, joten
      näytettäessä se olisi harmaata kommenttitekstiä eikä koodia.

    Rivinumerot palautetaan, koska piilottaminen itse tapahtuu vasta
    selaimessa: Markdownissa ei ole tapaa merkitä yksittäistä koodiriviä,
    joten numerot kirjoitetaan aidan attribuutiksi (fence_info) ja
    assets/js/hidelines.js merkitsee niitä vastaavat rivit sivulla.
    """
    if language not in HIDELINE_LANGUAGES:
        return body, []
    first, _ = rendered_body(body)
    lines: list[str] = []
    hidden: list[int] = []
    for index, line in enumerate(body):
        stripped = HIDELINE_RE.sub(r"\1", line, count=1)
        if stripped != line:
            hidden.append(index - first + 1)
        lines.append(stripped)
    return lines, hidden


def mark_highlights(body: list[str],
                    language: str) -> tuple[list[str], dict[str, list[int]]]:
    """Korostusmerkinnät pois. -> (rivit, {väri: rivinumerot}).

    Työnjako on sama kuin piiloriveillä (hide_lines) ja samasta syystä:
    merkintärivit lähtevät jo käännöksessä, ja väliin jääneiden rivien numerot
    kirjoitetaan aidan attribuutiksi (fence_info), koska Markdownissa ei ole
    tapaa merkitä yksittäistä koodiriviä. Merkintä on javan kommentti eikä
    riko käännöstä, mutta se on silti riisuttava täällä: ajonappi (kohta 3)
    lähettää lohkon koodin sellaisenaan, ja mdBook riisuu merkinnät niin ikään
    ennen korostusta.

    Väri on merkinnän oma tunnus pienellä ("HIGHLIGHT_GREEN_BEGIN" -> "green").
    Alue alkaa BEGIN-rivistä ja päättyy ensimmäiseen END-riviin väristä
    riippumatta — sama sääntö kuin mdBookin skriptissä — ja sulkematon alue
    jatkuisi lohkon loppuun. Aineistossa jokainen 120 alueesta on suljettu,
    yksikään ei ole toisen sisällä eikä yhdessäkään ole tuntematonta väriä.
    """
    if language not in HIGHLIGHT_LANGUAGES:
        return body, {}
    lines: list[str] = []
    marked: list[str | None] = []
    active: str | None = None
    for line in body:
        match = HIGHLIGHT_RE.match(line)
        if not match:
            lines.append(line)
            marked.append(active)
            continue
        color = match["color"].lower()
        if color not in HIGHLIGHT_COLORS:
            print(f"varoitus: tuntematon korostusväri, rivi jää värittömäksi: "
                  f"{line.strip()}", file=sys.stderr)
        active = color if match["edge"] == "BEGIN" else None
    # Numerot piirtyvästä rungosta, kuten piiloriveillä: merkintärivit ovat
    # tässä vaiheessa poissa, joten myös aidan alun tyhjät rivit lasketaan
    # vasta nyt (BEGIN-rivi ennen ensimmäistä koodiriviä ei ole tyhjä rivi).
    first, last = rendered_body(lines)
    colors: dict[str, list[int]] = {}
    for index in range(first, last):
        if marked[index]:
            colors.setdefault(marked[index], []).append(index - first + 1)
    return lines, colors


def fence_info(info: str, hidden: tuple[int, ...] | list[int] = (),
               colors: dict[str, list[int]] | None = None) -> str:
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

    Piilorivien (hide_lines) ja korostettujen rivien (mark_highlights) numerot
    tulevat mukaan attribuutteina. Aidan attribuutit menevät attr_listin kautta
    lohkon diviin sellaisinaan (<div class="language-java highlight"
    data-hidden="1 5" data-hl-green="2 3">), eli sama tie kuin luokillakin.
    """
    parts = [part.strip() for part in info.strip().split(",")]
    language, attributes = parts[0], [part for part in parts[1:] if part]
    if not language or (not attributes and not hidden and not colors):
        return language
    written = [f".{name}" for name in [language, *attributes]]
    if hidden:
        written.append(f'data-hidden="{" ".join(str(number) for number in hidden)}"')
    for color, numbers in sorted((colors or {}).items()):
        written.append(f'data-hl-{color}="{" ".join(str(n) for n in numbers)}"')
    return "{ " + " ".join(written) + " }"


def convert_fences(text: str) -> tuple[str, int, int, int]:
    """Aitojen attribuuttilistat pymdownx:n muotoon, piiloriveiltä etuliite pois
    ja korostusmerkinnät talteen.
    -> (teksti, aitoja, piilorivilohkoja, korostuslohkoja).

    Käydään aidat läpi pareittain, jottei koodilohkon sisällä oleva
    aidannäköinen rivi muutu vahingossa. Sulkeva aita on vähintään yhtä pitkä
    eikä siinä ole otsikkoa.

    Otsikko kirjoitetaan vasta sulkevalla aidalla, koska rivinumerot (kohdat 2
    ja 9, ks. hide_lines ja mark_highlights) selviävät vasta rungosta.
    Sulkematon aita jää siis ennalleen; niitä ei aineistossa ole yhtään.

    Korostusmerkinnät ennen piilorivejä, koska merkintärivit lähtevät rungosta
    pois: piilorivien numerot lasketaan siitä rungosta, joka jää jäljelle.
    """
    out: list[str] = []
    open_fence: str | None = None
    opening = 0
    header = indent = ""
    fences = blocks = marked = 0
    for line in text.split("\n"):
        match = QUOTED_FENCE_RE.match(line)
        info = match["info"].strip() if match else ""
        if match and open_fence is None:
            open_fence, opening = match["fence"], len(out)
            header, indent = info, match["indent"]
        elif match and not info and len(match["fence"]) >= len(open_fence):
            language = fence_language(header)
            body, colors = mark_highlights(out[opening + 1:], language)
            body, hidden = hide_lines(body, language)
            out[opening + 1:] = body
            blocks += bool(hidden)
            marked += bool(colors)
            if "," in header or hidden or colors:
                fences += 1
                out[opening] = (
                    f"{indent}{open_fence}{fence_info(header, hidden, colors)}")
            open_fence = None
        out.append(line)
    return "\n".join(out), fences, blocks, marked


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
        FAILED.add("plantuml")
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
        FAILED.add("svgbob")
        return None
    except subprocess.CalledProcessError as error:
        print(f"varoitus: svgbob epäonnistui: {error.stderr.strip()}",
              file=sys.stderr)
        FAILED.add("svgbob")
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


def bonus_mark(labelled: bool) -> str:
    """Bonusmerkki inline-SVG:nä. -> merkin HTML.

    labelled=True antaa merkille myös nimen ruudunlukijalle; ks.
    BONUS_WORD_RE. Liuskassa merkki on aina koriste, koska sana "Bonus"
    lukee siinä vieressä.
    """
    attrs = ' role="img" aria-label="Bonus"' if labelled else ' aria-hidden="true"'
    return (f'<span class="twemoji jyu-bonus"{attrs}>'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            f'<path d="{BONUS_MARK_PATH}"/></svg></span>')


def convert_bonus_marks(text: str) -> tuple[str, int]:
    """<i class="bi bi-stars"> -> bonusmerkki. -> (teksti, merkkejä).

    Tehtäväkorttien merkit on tässä vaiheessa jo käsitelty (task_head), joten
    jäljelle jäävät avattavien lohkojen <summary>-rivit ja harjoitustyön
    vaatimuslistat. Koodiaidat ohitetaan pareittain kuten convert_detailsissä,
    jottei aidan sisällä näytetty esimerkki muuttuisi; aineistossa yhtään
    tagia ei tosin ole aidan sisällä.

    Nimeäminen ratkaistaan riveittäin eikä merkeittäin: rivillä on aina
    korkeintaan yksi merkki, ja saman rivin muut merkit tarkoittaisivat joka
    tapauksessa samaa asiaa.
    """
    out: list[str] = []
    open_fence: str | None = None
    marks = 0
    for line in text.split("\n"):
        match = CODE_FENCE_RE.match(line)
        if match and open_fence is None:
            open_fence = match["fence"]
        elif (match and not match["info"].strip()
                and len(match["fence"]) >= len(open_fence)):
            open_fence = None
        elif open_fence is None and BONUS_TAG_RE.search(line):
            rest = BONUS_TAG_RE.sub("", line)
            mark = bonus_mark(BONUS_WORD_RE.search(rest) is None)
            line, count = BONUS_TAG_RE.subn(mark, line)
            marks += count
        out.append(line)
    return "\n".join(out), marks


def icon_mark(icon: str) -> str | None:
    """Kuvake inline-SVG:nä. -> merkin HTML, tai None jos glyfiä ei ole.

    Kääre .twemoji on teeman oma ikonikääre, sama kuin bonusmerkissä, joten
    koon (--md-icon-size), kohdistuksen (vertical-align: text-top) ja värin
    periytymisen (fill: currentcolor) hoitaa teeman CSS. Omaa sääntöä ei
    tarvita lainkaan.

    Kuvake on aina koriste: jokaisessa lähteen kohdassa nappi on nimetty
    samalla rivillä sanoina ("ajopainikkeesta (<kuvake>)"), joten nimi vain
    toistaisi vieressä olevan tekstin.

    Glyfi luetaan tiedostosta joka kerta erikseen. Se on 22 tagia kohti 22
    lukua muutaman sadan tavun tiedostosta, eli mitattuna nolla, ja säästää
    välimuistin, joka pitäisi muistaa tyhjentää testien välissä.
    """
    path = ICONS / f"{icon}.svg"
    if not path.is_file():
        print(f"varoitus: glyfi puuttuu: {path}", file=sys.stderr)
        return None
    svg = path.read_text(encoding="utf-8").strip()
    return f'<span class="twemoji" aria-hidden="true">{svg}</span>'


def convert_icons(text: str) -> tuple[str, int, int, set[str]]:
    """Ikonitagit merkeiksi ja kuvakkeiksi. -> (teksti, nuolia, kuvakkeita,
    tuntemattomia).

    Ks. ICON_TAG_RE: valikkopolun nuolesta tulee merkki (PATH_ARROW) ja
    muista Materialin tai Luciden glyfi (ICON_MAP, icon_mark). Tuntematon
    nimi jää sivulle sellaisenaan ja palautuu nimeltä kutsujalle, joka
    varoittaa siitä — sama tapa kuin tuntemattomassa alertin tunnuksessa.
    Näkyvä tagi on parempi kuin hiljaa kadonnut kuvake: lähdepuuhun voi tulla
    uusi ikoni milloin tahansa.

    Koodiaidat ohitetaan pareittain kuten convert_detailsissä, mutta teksti
    käsitellään aitojen välisinä paloina eikä riveittäin, koska tagi voi olla
    rivitetty kahdelle riville (ICON_TAG_RE).

    Ajetaan convert_bonus_marksin jälkeen: bi-stars ei ole ICON_MAPissa, joten
    aiemmin ajettuna tämä ilmoittaisi sen tuntemattomaksi.
    """
    parts: list[tuple[bool, list[str]]] = [(False, [])]
    open_fence: str | None = None
    for line in text.split("\n"):
        fence = CODE_FENCE_RE.match(line)
        if fence and open_fence is None:
            open_fence = fence["fence"]
            parts.append((True, [line]))
            continue
        if (fence and open_fence is not None and not fence["info"].strip()
                and len(fence["fence"]) >= len(open_fence)):
            open_fence = None
            parts[-1][1].append(line)
            parts.append((False, []))
            continue
        parts[-1][1].append(line)
    # Aidan rajalle syntyy tyhjä pala aina kun aita alkaa tai päättyy; se ei
    # ole rivi eikä saa muuttua sellaiseksi paloja yhdistettäessä.
    parts = [part for part in parts if part[1]]

    arrows = icons = 0
    unknown: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        nonlocal arrows, icons
        name = f'{match["prefix"]}-{match["name"]}'
        if name in PATH_ARROW_ICONS:
            arrows += 1
            return PATH_ARROW
        mark = icon_mark(ICON_MAP[name]) if name in ICON_MAP else None
        if mark is None:
            unknown.add(name)
            return match[0]
        icons += 1
        return mark

    out: list[str] = []
    for fenced, lines in parts:
        chunk = "\n".join(lines)
        out.append(chunk if fenced else ICON_TAG_RE.sub(replace, chunk))
    return "\n".join(out), arrows, icons, unknown


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
    bonus = BONUS_TAG_RE.search(inner) is not None
    name = BONUS_TAG_RE.sub("", inner).strip()
    if bonus:
        name += f' <span class="task-bonus">{bonus_mark(False)}Bonus</span>'
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


def convert_files(text: str) -> tuple[str, int, int, int, int]:
    """mdBookin monitiedostolohkot -> pymdownx.tabbed.
    -> (teksti, lohkot, tiedostot, piilorivitiedostot, korostustiedostot).

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

    Lisäksi jokainen tiedosto merkitään määreellä "multifile". Ajonappi
    (kohta 3) lähettää monitiedostolohkon kaikki tiedostot yhtenä ohjelmana
    niin kuin mdBookkin, ja siihen tarvitaan tieto siitä, mitkä
    välilehtijoukot ovat tiedostoja: sivulla on myös käyttöjärjestelmien
    välilehtiä (kohta 23), joiden lohkot ovat kukin oma ohjelmansa. Tieto on
    tässä eikä arvattavissa DOM:sta, koska vain tämä funktio tietää, että
    välilehdet syntyivät // FILE: -merkinnöistä. Kielettömässä lohkossa
    määre katoaa kielen mukana (fence_info), mikä on oikein: ilman kieltä ei
    ole ajonappia.

    Piilorivit (kohta 2) ja korostukset (kohta 9) käsitellään tässä eikä
    convert_fencesissa, koska rivinumerot lasketaan sen aidan sisällä, jossa
    rivi lopulta on: yhdeksän monitiedostolohkoa yhdeksästäkymmenestä
    kuudesta sisältää piilorivejä ja kaksitoista korostuksia, ja niissä
    jokainen tiedosto saa omat numeronsa. Valmiisiin aitoihin convert_fences
    ei enää koske, ks. fence_language.

    Ero mdBookiin: yhden tiedoston lohkot saavat yhden välilehden rivin, ja
    Materialin content.tabs.link yhdistää samannimiset välilehdet, ks. README.md.
    """
    lines = text.split("\n")
    out: list[str] = []
    blocks = files = 0
    index = 0
    hidden_files = marked_files = 0
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
        language = fence_language(fence["info"])
        if out and out[-1].strip():
            out.append("")
        blocks += 1
        for name, content in split_files(body):
            files += 1
            content, colors = mark_highlights(content, language)
            content, hidden = hide_lines(content, language)
            hidden_files += bool(hidden)
            marked_files += bool(colors)
            info = fence_info(fence["info"] + ",multifile", hidden, colors)
            out.append(f'=== "{name}"')
            out.append("")
            out.extend(indent_block([f"{marker}{info}", *content, marker]))
            out.append("")
        index = end + 1
    return "\n".join(out), blocks, files, hidden_files, marked_files


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


def sync_docs() -> set[Path]:
    """Kopioi ../src docs/:iin paikalleen. Palauttaa edellisen ajon jäänteet.

    docs/:ia ei tyhjennetä rmtree:llä, vaikka se olisi yksinkertaisin tapa,
    koska `zensical serve` seuraa hakemistoa tiedostovahdilla ja kaatuu
    (0.0.60: "RuntimeError: No such file or directory"), jos sen kesken
    rakennuksen lukema tiedosto tai hakemisto ehtii kadota. Sama vaara on
    jokaisessa tiedostossa, joka syntyy ja katoaa kesken ajon. Jos palvelin ei
    kaadu, se voi silti unohtaa docs/assets/:n staattiset tiedostot: sivut
    rakentuvat, mutta CSS:t ja JS:t puuttuvat site/:sta, ja palvelin vastaa
    niiden osoitteisiin etusivun HTML:llä (200, ei 404) — selaimessa paljas
    oletusteema ilman virheilmoitusta. Kumpikin pakottaisi käynnistämään
    palvelimen uudelleen joka convert.py-ajon jälkeen.

    Siksi tehdään vain sitä, minkä vahti kestää: tiedostot kirjoitetaan
    suoraan lopulliseen paikkaansa (myös NEST_UNDER-siirrot, joten
    tentti.md ei käy docs/:n juuressa), SUMMARY.md jätetään kopioimatta
    sen sijaan että se poistettaisiin, eikä hakemistoja poisteta koskaan.
    Tyhjiksi jäävät hakemistot eivät haittaa rakennusta.

    Jäänteet ovat tiedostoja, jotka olivat docs/:ssa ennen ajoa mutta joita
    ../src, assets/ tai tämä ajo ei tuota: lähdepuusta poistettuja sivuja.
    main poistaa ne vasta lopuksi, kun kaikki muu on paikallaan.

    Kirjoitetaan vain se, mikä oikeasti muuttui (copy_if_changed), ja
    Markdown-sivut jätetään mainille kirjoitettaviksi muunnettuina. Muuten
    yksi tallennus kirjoittaisi koko puun kahdesti — ensin raa'an kopion,
    sitten muunnoksen — ja `zensical serve` ilmoittaisi jokaisesta
    tiedostosta selaimelle erikseen. Mitattuna se oli 500-1300 WebSocket-
    viestiä tallennusta kohti, ja jokainen .js-viesti lataa sivun heti
    uudelleen: selain ehti ladata vanhan sivun ennen kuin uusi oli
    käännetty, ja muutos näkyi vasta seuraavasta tallennuksesta.
    """
    moves = nest_moves()
    before = ({f for f in DOCS.rglob("*") if f.is_file()}
              if DOCS.exists() else set())
    fresh: set[Path] = set()
    for file in SRC.rglob("*"):
        if not file.is_file():
            continue
        relative = file.relative_to(SRC).as_posix()
        if relative == "SUMMARY.md":
            continue
        target = DOCS / moves.get(relative, relative)
        fresh.add(target)
        if file.suffix == ".md":
            # Sivun kirjoittaa main muunnettuna, ks. write_if_changed.
            continue
        copy_if_changed(file, target)
    for old_path in moves:
        if not (SRC / old_path).is_file():
            print(f"varoitus: NEST_UNDER viittaa puuttuvaan sivuun: {old_path}",
                  file=sys.stderr)
    fresh |= {DOCS / "assets" / f.relative_to(ASSETS)
              for f in ASSETS.rglob("*") if f.is_file()}
    fresh.add(DOCS / PRINT_PAGE)
    return before - fresh


def copy_if_changed(source: Path, target: Path) -> None:
    """Kopioi vain jos kohde puuttuu tai eroaa lähteestä, ks. write_if_changed.

    Vertailu on tiedostotiedoista (koko ja aika) eikä sisällöstä, koska
    shutil.copy2 kopioi ajan lähteestä: muuttumaton tiedosto on kohteessa
    bitilleen sama ja samanikäinen, muuttunut eroaa kummassakin. Sisällön
    lukeminen maksaisi koko puun joka ajolla.
    """
    if target.is_file() and filecmp.cmp(source, target, shallow=True):
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def write_if_changed(path: Path, text: str) -> None:
    """Kirjoita vain jos sisältö muuttuu: turha kirjoitus on vahdille tapahtuma.

    Vahteja on kaksi ja molemmat maksavat. `zensical serve` ilmoittaa jokaisesta
    docs/:n muuttuneesta tiedostosta selaimelle, joka lataa sivun uudelleen
    kesken käännöksen, ja nav.yml:n tapauksessa kyse on lisäksi
    asetustiedoston muutoksesta, josta palvelin aloittaa koko sivuston
    rakennuksen alusta.
    """
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if not SRC.is_dir():
        print(f"lähdepuu puuttuu: {SRC}", file=sys.stderr)
        return 1
    FAILED.clear()
    stale = sync_docs()
    sets = placeholders = blocks = files = fences = includes = alerts = 0
    hidden = marked = 0
    details = summaries = divs = tasks = bonus = diagrams = drawings = 0
    breaks = dropped = arrows = icons = links = ids = 0
    used_diagrams: set[str] = set()
    used_drawings: set[str] = set()
    tab_labels: set[str] = set()
    unknown_alerts: set[str] = set()
    unknown_icons: set[str] = set()
    moves = nest_moves()
    # Silmukka käy lähdepuun eikä docs/:n: sivut luetaan sieltä, mihin ne on
    # kirjoitettu, ja tulos kirjoitetaan docs/:iin vain jos se muuttui. Docs/:n
    # yli käytäessä sivu piti ensin kopioida raakana paikalleen, ja se
    # kirjoitus oli vahdille yhtä suuri tapahtuma kuin oikea muutos.
    for origin in sorted(SRC.rglob("*.md")):
        source_path = origin.relative_to(SRC).as_posix()
        if source_path == "SUMMARY.md":
            # Navigaatio, ei sivu: ks. build_nav.
            continue
        # NEST_UNDER-siirretty sivu kirjoitetaan uuteen paikkaansa, mutta sen
        # sisällytykset ja DROP_SECTIONS ratkeavat lähdepuun omasta polusta.
        page = DOCS / moves.get(source_path, source_path)
        source = origin.read_text(encoding="utf-8")
        # Poistuvat osiot ennen kaikkea muuta: mitä ei ole, sitä ei tarvitse
        # muuntaa eikä siitä tarvitse varoittaa.
        converted, page_dropped = drop_sections(source, source_path)
        # Sisällytykset ennen kaikkea muuta, kuten mdBookissa: muut muunnokset
        # käsittelevät myös sisällytetyn tekstin (43 tehtävänannossa on
        # koodiaita), ja koodiaidan sisällä olevat sisällytykset ovat vasta
        # tämän jälkeen sitä koodia, jonka convert_files jakaa välilehdiksi.
        converted, page_includes = convert_includes(converted, origin)
        # Ankkurit heti sisällytysten jälkeen: silloin muunnos näkee myös
        # sisällytetyn tehtävänannon linkit, eikä yksikään myöhempi muunnos
        # ole vielä kirjoittanut sivulle omia linkkejään tai SVG-tunnuksiaan.
        converted, page_links, page_ids = convert_anchors(converted)
        # Monitiedostolohkot ennen aitoja: silloin ne toimivat myös #tab/-osion
        # sisällä, koska convert_tabs sisentää valmiin välilehtijoukon
        # sisäkkäiseksi. Toisin päin sisennetty aita jäisi tunnistamatta.
        (converted, page_blocks, page_files, page_hidden_files,
         page_marked_files) = convert_files(converted)
        # Aidat ennen välilehtiä: convert_tabs sisentää osion sisällön, ja
        # sisennetty aita jää tunnistamatta. convert_files kirjoittaa omat
        # aitansa jo valmiiksi oikeaan muotoon.
        converted, page_fences, page_hidden, page_marked = convert_fences(
            converted)
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
        # Bonusmerkit tehtäväkorttien jälkeen: task_head lukee kortin oman
        # tagin itse, ja aiemmin ajettuna tämä söisi sen ensin, jolloin
        # kortilta jäisi liuska pois.
        converted, page_bonus = convert_bonus_marks(converted)
        # Loput ikonit bonusmerkkien jälkeen: bi-stars ei ole ICON_MAPissa,
        # joten aiemmin ajettuna convert_icons ilmoittaisi sen tuntemattomaksi.
        (converted, page_arrows, page_icons,
         page_unknown_icons) = convert_icons(converted)
        converted, page_sets, page_placeholders, page_labels = convert_tabs(converted)
        write_if_changed(page, converted)
        sets += page_sets
        placeholders += page_placeholders
        tab_labels |= page_labels
        blocks += page_blocks
        files += page_files
        fences += page_fences
        hidden += page_hidden + page_hidden_files
        marked += page_marked + page_marked_files
        includes += page_includes
        links += page_links
        ids += page_ids
        alerts += page_alerts
        details += page_details
        summaries += page_summaries
        breaks += page_breaks
        divs += page_divs
        tasks += page_tasks
        bonus += page_bonus
        dropped += page_dropped
        arrows += page_arrows
        icons += page_icons
        unknown_icons |= page_unknown_icons
        diagrams += page_diagrams
        used_diagrams |= page_used
        drawings += page_drawings
        used_drawings |= page_art
        unknown_alerts |= page_unknown
    for asset in ASSETS.rglob("*"):
        if asset.is_file():
            copy_if_changed(asset, DOCS / "assets" / asset.relative_to(ASSETS))
    nav = build_nav()
    write_if_changed(ROOT / "nav.yml", nav + build_extra(tab_labels))
    write_if_changed(DOCS / PRINT_PAGE, build_print_page(nav))
    # Jäänteet viimeisenä, kun kaikki muu on jo paikallaan (ks. sync_docs).
    for file in sorted(stale):
        file.unlink()
    print(f"kopioitu {len(list(DOCS.rglob('*.md')))} markdown-tiedostoa -> {DOCS}"
          + (f", {len(stale)} jäänyttä tiedostoa pois" if stale else ""))
    print(f"välilehdet: {sets} joukkoa, {placeholders} #tab/default-lohkoa pois")
    print(f"monitiedostolohkot: {blocks} lohkoa, {files} tiedostoa")
    print(f"aidan attribuutit: {fences} aitaa")
    print(f"piilorivit: {hidden} lohkoa")
    print(f"korostetut rivit: {marked} lohkoa")
    print(f"sisällytykset: {includes} makroa")
    print(f"ankkurit: {links} linkkiä riisuttu, {ids} otsikon tunnusta irrotettu")
    print(f"details-lohkot: {details} tagia, {summaries} monirivistä summarya, "
          f"{breaks} <br />-riviä pois")
    print(f"divit: {divs} tagia")
    print(f"luokkakaaviot: {diagrams} kaaviota, "
          f"{prune_diagrams(PLANTUML_DIR, used_diagrams, 'plantuml' not in FAILED)}"
          " käyttämätöntä poistettu")
    print(f"ascii-kaaviot: {drawings} kaaviota, "
          f"{prune_diagrams(SVGBOB_DIR, used_drawings, 'svgbob' not in FAILED)}"
          " käyttämätöntä poistettu")
    print(f"tehtäväkortit: {tasks} korttia")
    print(f"bonusmerkit: {bonus} merkkiä korttien ulkopuolella")
    print(f"ikonit: {arrows} valikkopolun nuolta, {icons} kuvaketta"
          + (f", tuntematon ikoni: {', '.join(sorted(unknown_icons))}"
             if unknown_icons else ""))
    print(f"poistetut osiot: {dropped}")
    print(f"alertit: {alerts} lohkoa"
          + (f", tuntematon tunnus: {', '.join(sorted(unknown_alerts))}"
             if unknown_alerts else ""))
    return 0


# --- Vahti ------------------------------------------------------------------

# Kyselyväli. Kysely maksaa mitattuna 6 ms 600 tiedostolle, eli tällä välillä
# vahti vie prosentin luokkaa yhdestä ytimestä. Tiheämpi väli ei enää näkyisi
# kierrosajassa, koska muunnos itse on 0,8-1,4 s.
WATCH_INTERVAL = 0.3


def watch_paths() -> tuple[Path, ...]:
    """Vahdittavat puut: lähdepuu ja assetit.

    Assetit ovat mukana, koska nekin päätyvät sivustolle vain tämän skriptin
    kautta (docs/assets/): ilman vahtia CSS:n muutos jäisi näkymättä
    täsmälleen samalla tavalla kuin tekstin muutos.

    Funktio eikä vakio, jotta SRC:n vaihtaminen moduulivakiosta (testit
    tekevät niin) näkyy myös täällä.
    """
    return (SRC, ASSETS)


def snapshot() -> dict[str, int]:
    """Vahdittavien tiedostojen polut ja muokkausajat.

    Kysely eikä inotify, ja syy on ympäristössä: inotify ei saa tapahtumia
    lainkaan, jos repo on Windowsin levyllä 9p-liitoksen takana
    (PERUSTELUT.md). Siellä vahti olisi hiljaa rikki, mikä on pahempi vika
    kuin se, jonka vahti korjaa; kysely toimii kaikkialla samalla tavalla.

    os.scandir eikä Path.rglob: sama työ, mitattuna 6 ms 17 ms:n sijaan, ja
    ero maksetaan joka kyselyllä.

    Aika on st_mtime_ns eikä sisällön tiiviste, koska tiiviste lukisi koko
    puun joka kyselyllä.
    """
    state: dict[str, int] = {}
    stack = [str(path) for path in watch_paths() if path.is_dir()]
    while stack:
        try:
            with os.scandir(stack.pop()) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        stack.append(entry.path)
                    elif entry.is_file(follow_symlinks=False):
                        state[entry.path] = entry.stat().st_mtime_ns
        except OSError:
            # Hakemisto tai tiedosto katosi kesken kyselyn: editorin tallennus
            # on usein kirjoitus väliaikaistiedostoon ja nimeäminen sen päälle.
            # Seuraava kysely näkee lopputilan, ja muutos huomataan siitä.
            continue
    return state


def changed_files(before: dict[str, int], after: dict[str, int]) -> list[str]:
    """Muuttuneet, lisätyt ja poistetut tiedostot."""
    names = set(before) ^ set(after)
    names |= {name for name in before.keys() & after.keys()
              if before[name] != after[name]}
    return sorted(names)


def watch_label(changed: list[str]) -> str:
    """Muuttuneet tiedostot yhden rivin nimeksi: polku ja monelleko muulle."""
    try:
        name = Path(changed[0]).relative_to(ROOT.parent).as_posix()
    except ValueError:
        name = changed[0]
    return name if len(changed) == 1 else f"{name} (+{len(changed) - 1})"


def run_quietly() -> int:
    """main ilman sen viittätoista tilastoriviä. -> paluuarvo.

    Vahdin tulostus kulkee palvelimen lokin seassa, joten ajosta jää yksi rivi.
    Varoitukset menevät stderriin (esimerkiksi puuttuva sisällytys), joten
    vaimennus ei piilota niitä.
    """
    with only_one_run(), contextlib.redirect_stdout(io.StringIO()):
        return main()


def watch() -> int:
    """Aja muunnos aina kun lähdepuu tai assetit muuttuvat. -> paluuarvo.

    Ensimmäistä muunnosta ei tehdä: run.sh ajaa sen ennen vahdin käynnistystä,
    jotta `zensical serve` näkee valmiin docs/:n heti eikä rakenna sivustoa
    puolikkaasta hakemistosta.

    Mitattuna kierros on 2-3 s: kysely ja odotus 0,6 s, muunnos 1,2 s ja
    palvelimen oma käännös 0,2-0,6 s. Ks. README.md.
    """
    print(f"vahti: {SRC} ja {ASSETS}, lopeta Ctrl-C", flush=True)
    state = snapshot()
    try:
        while True:
            time.sleep(WATCH_INTERVAL)
            fresh = snapshot()
            if fresh == state:
                continue
            # Odota, että tallennus on ohi. Yksi editorin tallennus näkyy usein
            # monena muutoksena ja `git checkout` satoina, eikä kesken
            # kirjoitusta luettu tiedosto ole sitä mitä kirjoittaja tarkoitti.
            while True:
                time.sleep(WATCH_INTERVAL)
                settled = snapshot()
                if settled == fresh:
                    break
                fresh = settled
            changed = changed_files(state, fresh)
            started = time.monotonic()
            try:
                status = run_quietly()
            except Exception:
                # Yksi virhe ei saa tappaa vahtia: sen jälkeen tilanne olisi
                # sama kuin unohtunut ajo — sivu ei päivity eikä mikään kerro
                # miksi. Virhe näkyy, ja seuraava tallennus yrittää uudelleen.
                traceback.print_exc()
                status = 1
            elapsed = f"{time.monotonic() - started:.1f}".replace(".", ",")
            print(f"{time.strftime('%H:%M:%S')} {watch_label(changed)} -> "
                  + (f"muunnettu {elapsed} s" if status == 0
                     else "muunnos epäonnistui"), flush=True)
            # Uusi lähtötila vasta ajon jälkeen: muunnos kirjoittaa itse
            # assets/plantuml/:iin, kun kaavio on uusi tai muuttunut, eikä se
            # saa laukaista seuraavaa ajoa.
            state = snapshot()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if arguments and arguments != ["--watch"]:
        print(f"käyttö: {Path(__file__).name} [--watch]", file=sys.stderr)
        raise SystemExit(2)
    if arguments:
        raise SystemExit(watch())
    with only_one_run():
        raise SystemExit(main())
