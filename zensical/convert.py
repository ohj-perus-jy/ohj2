#!/usr/bin/env python3
"""Kääntää mdBookin lähdepuun (../src) Zensicalin docs/-hakemistoksi.

Ajo ilman argumentteja muuntaa kerran; `--watch` ajaa muunnoksen jokaisesta
lähdepuun tai assettien muutoksesta (run.sh käynnistää sen palvelimen rinnalle).

main: sync_docs kopioi muut kuin Markdown-tiedostot, jokainen sivu ajetaan
muunnosten läpi mainin järjestyksessä (järjestys ei ole vapaa, perustelut
mainissa), assetit kopioidaan, SUMMARY.md:stä tulee nav.yml ja tulostussivu,
ja lopuksi siivotaan jäänteet ja tulostetaan muunnosten lukumäärät.

Kirjoitetaan vain muuttunut (write_if_changed) ja yksi ajo kerrallaan
(only_one_run). <asciinema>-tagit menevät läpi sellaisenaan (assets/js/asciinema.js).
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

# Kuvakkeiden glyfit (ks. ICON_MAP) kopioina Zensicalin templates/.icons/:sta,
# koska run.sh ajaa skriptin systeemin python3:lla eikä .venv:stä. test_convert.py
# vertaa kopiot teemaan.
ICONS = ROOT / "icons"

SUMMARY_LINK_RE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>-\s*)?\[(?P<title>[^\]]*)\]\((?P<href>[^)]*)\)")

# Etulinkkien sisäkkäisyys, jota mdBookin SUMMARY.md ei salli.
# Avain = alasivun polku, arvo = sen sivun polku, jonka alle se siirretään.
NEST_UNDER = {
    "tenttiohjeet.md": "tentti.md",
}

# Osiot, jotka kuvaavat mdBookin käyttöliittymää (laitanuolet) eivätkä pidä
# Zensicalissa paikkaansa. Lähteeseen ei kosketa, joten poisto tehdään tässä.
# Avain = sivun polku lähdepuussa, arvo = osion otsikko sellaisenaan.
DROP_SECTIONS = {
    "index.md": "Navigointi tässä materiaalissa",
}
HEADING_RE = re.compile(r"(?P<level>#+)\s+(?P<title>.*?)\s*$")

# Linkin ankkuriosa "](../sivu.md#käyttö)", ks. convert_anchors.
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

# mdBookin välilehdet (preprocessor.accordion): "### [Windows](#tab/win)" aloittaa
# lohkon, "***" lopettaa, peräkkäiset lohkot ovat yksi joukko. Otsikkotasolla ei
# ole väliä, lähde käyttää sekaisin ### ja ####.
TAB_HEADING_RE = re.compile(
    r"^#{1,6}\s+\[(?P<label>[^\]]+)\]\(#tab/(?P<id>[^)]+)\)\s*$")
TAB_END = "***"

# mdBookin "ei vielä valintaa" -välilehti. Zensicalissa yksi välilehti on aina
# valittuna, joten tälle ei ole paikkaa; ks. PERUSTELUT.md.
TAB_PLACEHOLDER = "default"

# mdBookin monitiedostolohkot (preprocessor.codeblock-tabs). Merkinnät ovat
# lähteessä epätarkkoja ("//FILE:", välilyöntejä lopussa, FILE_END puuttuu tai
# on liikaa) ja mdBook sietää sen, joten sama sietokyky tässä.
FILE_BEGIN_RE = re.compile(r"^\s*//\s*FILE:\s*(?P<name>.+?)\s*$")
FILE_END_RE = re.compile(r"^\s*//\s*FILE_END\s*$")

# Koodiaita. Sisennys otetaan talteen ja kirjoitetaan takaisin sellaisenaan.
CODE_FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)(?P<info>[^\n`]*)$")

# Sama aita myös lainauslohkon sisällä ("> ```java,ignore"). Vain convert_fences
# käyttää: se kirjoittaa pelkän otsikon, joten ">" kelpaa sisennykseksi.
QUOTED_FENCE_RE = re.compile(
    r"^(?P<indent>[\s>]*)(?P<fence>```+|~~~+)(?P<info>[^\n`]*)$")

# mdBookin piilorivit (book.toml: hidelines): "//-"-alkuinen rivi kuuluu
# ohjelmaan muttei näy. Vain javalle ja javascriptille, kuten kirjassa.
# Lainausmerkit rivin alussa otetaan talteen: alertin sisällä olevassa aidassa
# ">" on vielä paikallaan, koska convert_alerts ajetaan myöhemmin.
HIDELINE_RE = re.compile(r"^((?:[ \t]*>)*[ \t]*)//-")
HIDELINE_LANGUAGES = ("java", "javascript")

# mdBookin korostusmerkinnät (theme/code-highlights.js): "// HIGHLIGHT_GREEN_BEGIN"
# ... "// HIGHLIGHT_GREEN_END" värittää väliin jäävät rivit, merkintärivit eivät
# näy. Väli "//":n jälkeen on valinnainen ja rivi voi olla sisennetty tai
# lainauksessa, kuten piiloriveillä.
HIGHLIGHT_RE = re.compile(
    r"^[\s>]*//\s*HIGHLIGHT_(?P<color>[A-Z0-9]+)_(?P<edge>BEGIN|END)\s*$")
HIGHLIGHT_COLORS = ("green", "yellow", "red", "blue")

# mdBookin skripti käsittelee vain javan; muissa kielissä rivi on kommentti.
HIGHLIGHT_LANGUAGES = ("java",)

# mdBookin sisällytysmakro. Polun perässä voi olla rivivalinta, ks. take_lines.
INCLUDE_RE = re.compile(r"\{\{#include\s+(?P<spec>[^}\s][^}]*?)\s*\}\}")

# mdBookin alertit (mdbook-alerts): lainauslohko, jonka ensimmäinen rivi on
# pelkkä "[!TUNNUS]". Tunnuksen kirjainkoko vaihtelee lähteessä.
ALERT_RE = re.compile(r"^>\s*\[!(?P<label>[^\]]+)\]\s*$")

# Tunnus (pienellä) -> admonition-tyyppi ja otsikko. Tyyppi valittu mdBookin
# värin ja kuvakkeen mukaan. Vain kanoniset tyypit: Zensicalin CSS:ssä ei ole
# aliaksia, joten esim. "important" jäisi tyylittömäksi — siksi Tärkeää on "tip".
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

# <details>-lohkot. Python-Markdown päästää raa'an HTML-lohkon sisällön läpi
# jäsentämättä; markdown-attribuutti (md_in_html, Zensicalin oletuslistalla)
# korjaa sen. <details closed> ei ole HTML:ää mutta toimii, joten attribuutit
# jätetään paikalleen. Lookahead ohittaa jo käännetyn tagin (toistokelpoisuus).
DETAILS_RE = re.compile(r"<details(?![^>]*\bmarkdown=)(?P<attrs>[^>]*)>")

# Sama <summary>-tagille, mutta vain kun yhteenvedossa on tyhjä rivi ennen
# </summary>:ä: se on sama raja, jolla mdBookin pulldown-cmark alkaa jäsentää
# Markdownia. Yksirivinen tai rivitetty teksti jätetään rauhaan, muuten se
# käärittäisiin <p>:hen ja avauspalkki saisi kappaleen marginaalit.
# Arvo on "block" eikä "1": <summary> on md_in_html:n span_tags-listalla, joten
# "1" tarkoittaisi vain rivinsisäistä jäsennystä ja otsikko jäisi risuaidoiksi.
SUMMARY_RE = re.compile(r"<summary(?![^>]*\bmarkdown=)(?P<attrs>[^>]*)>")
SUMMARY_END = "</summary>"

# Omaksi kappaleekseen jäänyt <br />, lähteessä väljyydeksi lohkojen väliin.
# Python-Markdown tekee siitä <p><br /></p>, joka moninkertaistaa lohkojen välin;
# laatikoiden omat marginaalit riittävät. Vain omalla rivillään sarakkeessa 0
# oleva tagi pudotetaan: rivin lopussa se on rivinvaihto, sisennetty voi olla koodia.
BREAK_LINE_RE = re.compile(r"^<br\s*/?>\s*$")

# Harjoitustyön vaatimusdivit (harjoitustyo.md), sama ongelma kuin <details>.
# Myös uloin divi tarvitsee attribuutin: md_in_html ei etene sisempiin lohkoihin,
# jos uloin on käsittelemätöntä HTML:ää. Divi ei ole span_tagsissa, joten "1" riittää.
DIV_RE = re.compile(r"<div(?![^>]*\bmarkdown=)(?P<attrs>[^>]*)>")

# Luokkakaaviot: ```plantuml-aita lähetetään samalle PlantUML-palvelimelle kuin
# kirjassa ja vastaus talletetaan tiedostoksi (nimi = lähteen sha1), aita
# korvataan kuvaviittauksella. Tiedostot ovat versionhallinnassa
# (assets/plantuml/), joten käännös tarvitsee verkkoa vain uudelle tai
# muuttuneelle kaaviolle; jos palvelin ei vastaa, aita jää ennalleen ja ajo
# varoittaa. Palvelin vaatii User-Agentin (muuten 403).
PLANTUML_FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)plantuml\s*$")
PLANTUML_URL = "https://www.plantuml.com/plantuml/svg/"
PLANTUML_AGENT = "ohj2-zensical-koeputki"
PLANTUML_DIR = ASSETS / "plantuml"
PLANTUML_ALPHABET = (
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_")

# Kaikki kaaviot ovat luokkakaavioita, joten alt-teksti voi olla tarkka.
PLANTUML_ALT = "UML-luokkakaavio"

# ASCII-kaaviot: ```bob-aita piirretään svgbob_cli:llä (cargo install svgbob_cli,
# sama svgbob kuin mdbook-svgbobissa). Riippuvuus on pehmeä: valmiit kaaviot
# ovat versionhallinnassa (cache/svgbob/), ja ilman komentoa aita jää ennalleen.
# SVG upotetaan sivulle eikä viitata <img>:llä, koska sen värit tulevat sivun
# CSS-muuttujista, joita <img>:n sisältö ei näe; siksi hakemisto on välimuisti
# eikä asset. Kääre on <div>, koska <svg> ei ole Python-Markdownin
# BLOCK_LEVEL_ELEMENTS-listalla ja päätyisi kappaleen sisään.
SVGBOB_FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)bob\s*$")
SVGBOB_DIR = ROOT / "cache" / "svgbob"

# svgbob kirjoittaa jokaiseen kaavioon samat id="arrow" ym. määrittelyt, joten
# saman sivun kaaviot saavat juoksevan etuliitteen; print.js lisää tulostussivulla
# vielä luvun oman etuliitteen.
SVGBOB_ID_RE = re.compile(r'\bid="(?P<name>[^"]+)"')
SVGBOB_REF_RE = re.compile(r"url\(#(?P<name>[^)]+)\)")

# book.tomlin piirtoasetukset, värit ja kirjasin Zensicalin muuttujina.
SVGBOB_COMMAND = [
    "svgbob_cli",
    "--font-size", "14",
    "--font-family", "var(--md-code-font-family)",
    "--fill-color", "var(--md-default-fg-color)",
    "--stroke-color", "var(--md-default-fg-color)",
    "--stroke-width", "2",
    "--background", "transparent",
]

# Tehtäväkortit: mdBookin omat elementit <task>, <task-title num="">, <points>,
# <handout>, <task-link>. <task> ei ole Python-Markdownin BLOCK_LEVEL_ELEMENTS-
# listalla, joten kortti jäisi kappaleen sisään eikä md_in_html käsittelisi sitä
# edes attribuutilla. Siksi diveiksi: nimi luokkaan (assets/css/tasks.css),
# tehtävänanto markdown="1":llä. Tunnusrivi on raakaa HTML:ää ilman attribuuttia.
TASK_TAG_RE = re.compile(r"</?(?:task|task-title|task-link|handout)[ >]")
TASK_TITLE_RE = re.compile(
    r'<task-title\s+num="(?P<num>[^"]*)"\s*>(?P<inner>.*?)</task-title>')
TASK_POINTS_RE = re.compile(r"<points>(?P<points>.*?)</points>")

# Bonusmerkki <i class="bi bi-stars">. Bootstrap Iconsia ei ladata, joten merkki
# piirretään Materialin creation-kuvakkeella (.icons/material/creation.svg).
# Valmis inline-SVG eikä lyhytkoodi, koska <summary>-rivillä Python-Markdown ei
# jäsennä lyhytkoodia. Kääre .twemoji on teeman oma, joten koko, kohdistus ja
# väri tulevat teeman CSS:stä; oma sääntö vain väriin, ks. assets/css/tasks.css.
BONUS_TAG_RE = re.compile(r'<i\s+class="[^"]*\bbi-stars\b[^"]*"\s*>\s*</i>')
BONUS_MARK_PATH = (
    "m19 1-1.26 2.75L15 5l2.74 1.26L19 9l1.25-2.74L23 5l-2.75-1.25"
    "M9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5"
    "M19 15l-1.26 2.74L15 19l2.74 1.25L19 23l1.25-2.75L23 19l-2.75-1.26")

# Rivillä jo oleva bonussana: merkki nimetään ruudunlukijalle vain, jos rivillä
# ei ole samaa tietoa tekstinä.
BONUS_WORD_RE = re.compile(r"bonus|valinnais", re.IGNORECASE)
TASK_TAGS = (
    ("<task>", '<div class="task" markdown="1">'),
    ("</task>", "</div>"),
    ("<handout>", '<div class="task-handout" markdown="1">'),
    ("</handout>", "</div>"),
    ("<task-link>", '<div class="task-link">'),
    ("</task-link>", "</div>"),
)

# Loput ikonitagit (<i class="bi bi-play-fill">, <i class="fa fa-eye">); fontteja
# ei ladata, joten ilman muunnosta ne ovat tyhjää tilaa. Etsitään koko tekstistä
# eikä riveittäin, koska tagi voi olla rivitetty kesken — myös lainauslohkossa,
# jolloin jatkorivi alkaa ">":llä; siksi [\s>]+ eikä \s+. (?P=prefix) pitää
# parit bi bi- / fa fa- erillään.
ICON_TAG_RE = re.compile(
    r'<i[\s>]+class="(?P<prefix>bi|fa)[\s>]+(?P=prefix)-(?P<name>[a-z0-9-]+)'
    r'[^"]*"\s*>\s*</i>')

# Valikkopolun nuoli (File › New) on välimerkki, ei kuvake: pelkkä merkki
# riittää. › (U+203A) siksi, että Source Serif 4:n latin-osajoukko sisältää sen
# (→ ja ▸ eivät kuulu siihen, ja tulisivat varakirjasimesta). Väri vaimennetaan
# assets/css/icons.css:ssä.
PATH_ARROW_ICONS = ("bi-chevron-right", "bi-arrow-right")
PATH_ARROW = '<span class="jyu-path">›</span>'

# Oikeat kuvakkeet: käyttöliittymän nappeja, joihin teksti viittaa. Sivuston
# omille napeille sama glyfi kuin napissa (header.html, mkdocs.yml,
# playground.css, hidelines.css); IntelliJ:n ja SceneBuilderin napeille
# Materialin lähin vastine, ääriviivaversio leipätekstin painon takia.
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

# Piirtäjät, jotka epäonnistuivat tässä ajossa ("plantuml", "svgbob"); main
# tyhjentää ajon aluksi. prune_diagrams ei saa siivota vajaan käytettyjen joukon
# perusteella. Moduulitason joukko, koska testit nojaavat paluuarvojen muotoon.
FAILED: set[str] = set()


def only_one_run():
    """Vain yksi muunnos kerrallaan, myös eri prosesseista. -> kontekstivaraaja.

    Rinnakkaiset ajot (kaksi run.sh:ta) sekoittavat docs/:n, ja prune_diagrams
    poistaisi versionhallinnassa olevia kaavioita, joita toinen ajo ei enää
    nähnyt käytetyiksi. flock eikä lukkotiedosto, jotta lukko vapautuu myös
    tapetusta ajosta.
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

    navigation.indexes tekee osion otsikosta linkin vain, jos ensimmäinen sivu
    on hakemistonsa index.md. Alasivu siirretään samaan hakemistoon, jotta
    sivujen väliset suhteelliset linkit osoittavat yhä oikein.
    """
    moves: dict[str, str] = {}
    for child, parent in NEST_UNDER.items():
        folder = parent.removesuffix(".md")
        moves[parent] = f"{folder}/index.md"
        moves[child] = f"{folder}/{Path(child).name}"
    return moves


def prune_diagrams(folder: Path, used: set[str], complete: bool = True) -> int:
    """Käyttämättömät kaaviotiedostot pois. -> poistettuja.

    Nimi on lähteen sha1, joten muokattu kaavio jättäisi vanhan tiedoston.
    Ei siivota, jos used on tyhjä tai complete=False (ks. FAILED): silloin
    joukko on vajaa, ja tiedostot ovat versionhallinnassa eli poisto on
    menetettyä työtä.
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

    tab_labels: convert_tabsin välilehtiotsikot, jotka content.tabs.link saa
    muistaa selaimessa (overrides/partials/javascripts/content.html) — ei
    tiedostonimiä, jotta klikattu tiedosto ei avaisi muita lohkoja väärältä
    välilehdeltä. edit_source: docs/-polku -> src-polku NEST_UNDER-siirroille,
    tyhjä PRINT_PAGElle = ei muokkauslinkkiä (overrides/partials/copyright.html).
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

    Pelkkä runko: assets/js/print.js hakee luvut omilta sivuiltaan valmiina
    HTML:nä. Lukuja ei voi liittää yhdeksi Markdown-tiedostoksi, koska kesken
    jäänyt HTML-lohko tai pariton aita nielaisisi seuraavan luvun alun.
    Ilman JavaScriptiä luettelo jää näkyviin sisällysluettelona.
    """
    lines = [PRINT_INTRO]
    for match in NAV_ENTRY_RE.finditer(nav_yaml):
        lines.append(f"- [{match['title']}]({match['href']})")
    lines.append("\n</div>\n")
    return "\n".join(lines)


def build_nav() -> str:
    """src/SUMMARY.md -> mkdocs nav: -lohko.

    Numerointi kuten mdBookissa: vain listakohdat, juoksevasti erottimien yli;
    etu- ja jälkilinkit jäävät numeroimatta.
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
                # Osan etusivu ensimmäisenä lapsena (navigation.indexes) tekee
                # osion otsikosta linkin. Otsikko numeroineen myös lapselle,
                # koska edellinen/seuraava-linkit ja <title> lukevat sen sieltä.
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

    Osio on otsikkorivi ja kaikki seuraavaan samantasoiseen tai ylempään
    otsikkoon asti. Koodiaidat ohitetaan: aidan sisällä "#" on kommentti.
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

    mdBookin muodot "", "N", "A:B", "A:" ja ":B"; numerot 1-pohjaisia, päät
    mukaan. Ilman loppurivinvaihtoa kuten mdBookissa, jotta sisällytys mahtuu
    taulukon soluun. Ankkurimuotoa (":ANCHOR") ei toteuteta: se palauttaa
    None ja makro jää näkyviin.
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

    page on lähdepuun sivu, ei docs/-kopio: sisällytettävä tiedosto luetaan
    aina muuntamattomana, koska tehtävänannot ovat itsekin muunnettavia sivuja.
    Rivin sisennystä ei toisteta, kuten ei mdBookkaan. Puuttuvasta tiedostosta
    ja tuntemattomasta valinnasta varoitetaan ja makro jätetään näkyviin.
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

    1. Ääkköset pois linkin ankkurista ("#käyttö" -> "#kaytto"): Python-Markdownin
       slugify pudottaa ei-ascii-merkit, mdBook ei. Vain sivuston omiin
       linkkeihin; skeemallisen osoitteen ankkurista päättää toinen sivusto.
    2. Välilyönti otsikon oman tunnuksen eteen ("## Otsikko {#tunnus}"), jota
       attr_list vaatii; muuten tunnukseksi tulisi "otsikkotunnus".
    Koodiaidat ohitetaan: aidassa näytetty linkki on esimerkki.
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

    Markdown pudottaa aidan alun ja lopun tyhjät rivit, joten rivinumerot on
    laskettava jäljelle jäävästä rungosta. Pelkkä "> " on tyhjä, koska
    lainausmerkki katoaa myöhemmin (convert_alerts).
    """
    first, last = 0, len(body)
    while first < last and not body[first].strip(" \t>"):
        first += 1
    while last > first and not body[last - 1].strip(" \t>"):
        last -= 1
    return first, last


def hide_lines(body: list[str], language: str) -> tuple[list[str], list[int]]:
    """Piiloriveiltä etuliite pois. -> (rivit, piilorivien numerot).

    Etuliite on riisuttava, koska ajonappi lähettää koodin sellaisenaan ja
    "//-" tekisi rivistä kommentin; myös korostus menisi väärin. Piilotus
    tapahtuu selaimessa: numerot menevät aidan attribuutiksi (fence_info) ja
    assets/js/hidelines.js merkitsee rivit.
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

    Sama työnjako kuin hide_lines: merkintärivit pois, numerot aidan
    attribuutiksi (fence_info). Alue päättyy ensimmäiseen END-riviin väristä
    riippumatta, kuten mdBookissa; sulkematon alue jatkuu lohkon loppuun.
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
    # Rungon rajat vasta merkintärivien poiston jälkeen: BEGIN-rivi aidan
    # alussa ei ole tyhjä rivi.
    first, last = rendered_body(lines)
    colors: dict[str, list[int]] = {}
    for index in range(first, last):
        if marked[index]:
            colors.setdefault(marked[index], []).append(index - first + 1)
    return lines, colors


def fence_info(info: str, hidden: tuple[int, ...] | list[int] = (),
               colors: dict[str, list[int]] | None = None) -> str:
    """mdBookin aidan attribuuttilista -> pymdownx:n aitaotsikko.

    "java,ignore" -> "{ .java .ignore data-hidden="1 5" data-hl-green="2 3" }".
    pymdownx ei tunnista aitaa, jonka otsikossa on pilkku, ja tunnistamaton
    aita nielaisee seuraavan tekstin koodiksi. Määreet säilyvät luokkina
    (ajonappi ym. tarvitsevat niitä), rivinumerot data-attribuutteina.
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
    """Aitojen attribuuttilistat pymdownx:n muotoon, piilorivit ja korostukset
    talteen. -> (teksti, aitoja, piilorivilohkoja, korostuslohkoja).

    Otsikko kirjoitetaan vasta sulkevalla aidalla, koska rivinumerot selviävät
    rungosta; sulkematon aita jää ennalleen. Korostukset ennen piilorivejä,
    koska merkintärivien poisto muuttaa rivinumeroita.
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

    -> (lainauslohkon loput rivit, ensimmäinen rivi lohkon jälkeen). Lohko
    loppuu ensimmäiseen riviin, joka ei ala ">"-merkillä; laiskoja jatkorivejä
    ei tueta.
    """
    index = start + 1
    while index < len(lines) and lines[index].startswith(">"):
        index += 1
    return lines[start + 1:index], index


def alert_body(body: list[str]) -> list[str]:
    """Lainauslohkon rivit admonitionin sisällöksi: ">" ja yksi välilyönti pois,
    neljä välilyöntiä sisemmäs. Lohkon omat sisennykset säilyvät."""
    return indent_block([line[1:].removeprefix(" ") for line in body])


def convert_alerts(text: str) -> tuple[str, int, set[str]]:
    """mdBookin alertit -> admonitionit. -> (teksti, lohkoja, tuntemattomat).

    "> [!VINKKI]" -> '!!! tip "Vinkki"'. Otsikko aina näkyviin, koska muuten
    Material näyttää tyypin englanninkielisen nimen.
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
        # Tyhjä rivi perään vain jos lähteessä ei jo ollut.
        if index < len(lines) and lines[index].strip():
            out.append("")
    return "\n".join(out), alerts, unknown


def plantuml_encode(source: str) -> str:
    """Kaavion lähde -> PlantUML-palvelimen osoitepala.

    Raaka deflate (zlib-otsikko ja tarkiste pois) ja base64 PlantUMLin omalla
    aakkostolla ilman "="-täytettä.
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
    # Syntaksivirheestä palvelin vastaa 200:lla ja virhekuvalla; se kelpaa,
    # mutta muu kuin SVG ei.
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

    Kuvan osoite on suhteellinen sivun sijaintiin docs/:ssä, siis
    NEST_UNDER-siirron jälkeiseen polkuun.
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

    Ajetaan convert_divsin jälkeen, jottei kääre saisi markdown="1":tä.
    Tyhjät rivit pois, koska ne päättäisivät raa'an HTML-lohkon.
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
    -> (teksti, details-tageja, summary-tageja). Ks. DETAILS_RE ja SUMMARY_RE.
    Koodiaidat ohitetaan, jottei aidassa näytetty HTML-esimerkki muuttuisi.
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

    Ks. BREAK_LINE_RE. Ehtona tyhjä rivi kummallakin puolella (se tekee
    rivistä kappaleen); toinen tyhjä poistetaan tagin mukana. Koodiaidat
    ohitetaan.
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

    Ks. DIV_RE. Vain rivin aloittava tagi, koska Python-Markdown tunnistaa
    lohkotason HTML:n vain omana kappaleenaan. Ajetaan ennen convert_tasksia,
    jotta tehtäväkorttien divit jäävät tämän ulkopuolelle. Koodiaidat ohitetaan.
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

    labelled=True antaa merkille nimen ruudunlukijalle, ks. BONUS_WORD_RE.
    """
    attrs = ' role="img" aria-label="Bonus"' if labelled else ' aria-hidden="true"'
    return (f'<span class="twemoji jyu-bonus"{attrs}>'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            f'<path d="{BONUS_MARK_PATH}"/></svg></span>')


def convert_bonus_marks(text: str) -> tuple[str, int]:
    """<i class="bi bi-stars"> -> bonusmerkki. -> (teksti, merkkejä).

    Tehtäväkorttien merkit on jo käsitelty (task_head). Nimeäminen ratkaistaan
    riveittäin (BONUS_WORD_RE). Koodiaidat ohitetaan.
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

    Kääre .twemoji kuten bonusmerkissä. Aina koriste (aria-hidden), koska
    nappi on lähteessä nimetty samalla rivillä sanoina. Glyfi luetaan joka
    kerta tiedostosta; välimuisti pitäisi tyhjentää testien välissä.
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

    Valikkopolun nuolesta PATH_ARROW, muista ICON_MAPin glyfi. Tuntematon tagi
    jää näkyviin ja palautuu kutsujalle varoitettavaksi. Teksti käsitellään
    aitojen välisinä paloina eikä riveittäin, koska tagi voi olla rivitetty.
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
    # Aidan rajalle syntyvä tyhjä pala ei saa muuttua riviksi yhdistettäessä.
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

    Bonusliuska jää nimen sisään, jotta se seuraa viimeistä sanaa rivittyessä.
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
    """<task>-kortit diveiksi. -> (teksti, kortteja). Ks. TASK_TAG_RE.

    Tagirivien sisennys pois ja tyhjä rivi väliin: Python-Markdown tunnistaa
    lohkotason HTML:n vain omana kappaleenaan, ja neljän välilyönnin sisennys
    olisi koodilohko. Koodiaidat ohitetaan.
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
            # Lähteen oma tyhjä rivi tagin perässä ei tule toiseen kertaan.
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

    Merkintöjen ulkopuoliset rivit putoavat pois; convert_files tarkistaa ne
    ennen kutsua. Tyhjä lista = lohkossa ei ole merkintöjä.
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

    Jokainen tiedosto omaksi välilehdekseen ja aidakseen, jossa alkuperäiset
    määreet ja lisäksi "multifile": ajonappi lähettää tällaisen joukon yhtenä
    ohjelmana, eikä sitä voi päätellä DOM:sta. Piilorivit ja korostukset
    käsitellään tässä, koska rivinumerot lasketaan tiedoston omasta aidasta;
    convert_fences ei enää koske valmiisiin aitoihin (fence_language).
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
        # Sulkematon aita, tavallinen lohko tai koodia ennen ensimmäistä
        # merkintää: jätetään ennalleen. Viimeisestä varoitetaan, koska
        # split_files pudottaisi rivit hiljaa pois.
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

    #tab/default jää pois (TAB_PLACEHOLDER). Saman tunnuksen välilehdet saavat
    saman otsikon ensimmäisen esiintymän mukaan, koska Material yhdistää
    sivun välilehtijoukot otsikkotekstistä, mdBook tunnuksesta.
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
        # Tyhjä rivi myös kun koko joukko jäi pois: read_tab_set söi joukon
        # jälkeiset tyhjät rivit, ja kappaleet liimautuisivat yhteen.
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
    """Kopioi ../src:n muut kuin Markdown-tiedostot docs/:iin. -> edellisen ajon jäänteet.

    docs/:ia ei tyhjennetä eikä hakemistoja poisteta: `zensical serve` vahtii
    hakemistoa ja kaatuu tai unohtaa docs/assets/:n, jos tiedosto katoaa kesken
    rakennuksen. Siksi kaikki kirjoitetaan suoraan lopulliseen paikkaansa
    (NEST_UNDER-siirrot mukaan lukien), vain muuttunut (copy_if_changed), ja
    Markdown-sivut jätetään mainille kirjoitettaviksi muunnettuina. Jäänteet
    (poistetut sivut) main poistaa vasta lopuksi.
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

    Vertailu koosta ja ajasta, ei sisällöstä: copy2 kopioi ajan lähteestä, ja
    sisällön lukeminen maksaisi koko puun joka ajolla.
    """
    if target.is_file() and filecmp.cmp(source, target, shallow=True):
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def write_if_changed(path: Path, text: str) -> None:
    """Kirjoita vain jos sisältö muuttuu: turha kirjoitus on vahdille tapahtuma.

    `zensical serve` lataa sivun selaimessa uudelleen jokaisesta docs/:n
    muutoksesta, ja nav.yml:n muutoksesta se rakentaa koko sivuston alusta.
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
    used_diagrams: set[str] = set()
    used_drawings: set[str] = set()
    tab_labels: set[str] = set()
    unknown_alerts: set[str] = set()
    unknown_icons: set[str] = set()
    moves = nest_moves()
    # Silmukka käy lähdepuun eikä docs/:n, jottei sivua tarvitse ensin kopioida
    # raakana paikalleen (turha kirjoitus on vahdille tapahtuma).
    for origin in sorted(SRC.rglob("*.md")):
        source_path = origin.relative_to(SRC).as_posix()
        if source_path == "SUMMARY.md":
            # Navigaatio, ei sivu: ks. build_nav.
            continue
        # Sivu kirjoitetaan NEST_UNDER-siirron jälkeiseen paikkaan, mutta
        # sisällytykset ja DROP_SECTIONS ratkeavat lähdepuun polusta.
        page = DOCS / moves.get(source_path, source_path)
        source = origin.read_text(encoding="utf-8")
        # Järjestys: poistuvat osiot ja sisällytykset ensin, jotta muut
        # muunnokset näkevät lopullisen tekstin (sisällytyksissä on koodiaitoja
        # ja FILE-merkintöjä). Ankkurit ennen kuin mikään muunnos kirjoittaa
        # omia linkkejään tai SVG-tunnuksiaan. Muunnosten laskurit jäävät
        # käyttämättä.
        converted, _ = drop_sections(source, source_path)
        converted, _ = convert_includes(converted, origin)
        converted, _, _ = convert_anchors(converted)
        # Monitiedostolohkot ennen convert_fencesiä: convert_fences ei koske
        # niiden valmiisiin aitoihin. Aidat, kaaviot, alertit ja tehtäväkortit
        # ennen convert_tabsia, koska se sisentää välilehden sisällön, eikä
        # sisennettyä aitaa, ">":tä tai HTML-lohkoa enää tunnisteta.
        converted, *_ = convert_files(converted)
        converted, *_ = convert_fences(converted)
        converted, _, page_used = convert_plantuml(converted, page)
        converted, _, page_unknown = convert_alerts(converted)
        # details ja drop_breaks: paikalla ei ole väliä.
        converted, *_ = convert_details(converted)
        converted, _ = drop_breaks(converted)
        # Divit ennen tehtäväkortteja (näkee vain lähteen divit) ja ennen
        # svgbobia (kääre ei saa markdown="1":tä).
        converted, _ = convert_divs(converted)
        converted, _, page_art = convert_svgbob(converted)
        # Tehtäväkortit ennen bonusmerkkejä (task_head lukee kortin tagin itse)
        # ja bonusmerkit ennen ikoneita (bi-stars ei ole ICON_MAPissa).
        converted, _ = convert_tasks(converted)
        converted, _ = convert_bonus_marks(converted)
        converted, _, _, page_unknown_icons = convert_icons(converted)
        converted, _, _, page_labels = convert_tabs(converted)
        write_if_changed(page, converted)
        tab_labels |= page_labels
        unknown_icons |= page_unknown_icons
        used_diagrams |= page_used
        used_drawings |= page_art
        unknown_alerts |= page_unknown
    for asset in ASSETS.rglob("*"):
        if asset.is_file():
            copy_if_changed(asset, DOCS / "assets" / asset.relative_to(ASSETS))
    nav = build_nav()
    write_if_changed(ROOT / "nav.yml", nav + build_extra(tab_labels))
    write_if_changed(DOCS / PRINT_PAGE, build_print_page(nav))
    prune_diagrams(PLANTUML_DIR, used_diagrams, "plantuml" not in FAILED)
    prune_diagrams(SVGBOB_DIR, used_drawings, "svgbob" not in FAILED)
    # Jäänteet viimeisenä, kun kaikki muu on jo paikallaan (ks. sync_docs).
    for file in sorted(stale):
        file.unlink()
    if unknown_icons:
        print(f"varoitus: tuntematon ikoni: {', '.join(sorted(unknown_icons))}",
              file=sys.stderr)
    if unknown_alerts:
        print("varoitus: tuntematon alertin tunnus: "
              f"{', '.join(sorted(unknown_alerts))}", file=sys.stderr)
    print(f"kopioitu {len(list(DOCS.rglob('*.md')))} markdown-tiedostoa -> {DOCS}"
          + (f", {len(stale)} jäänyttä tiedostoa pois" if stale else ""))
    return 0


# --- Vahti ------------------------------------------------------------------

# Kyselyväli sekunteina; tiheämpi ei näkyisi kierrosajassa, muunnos on hitaampi.
WATCH_INTERVAL = 0.3


def watch_paths() -> tuple[Path, ...]:
    """Vahdittavat puut: lähdepuu ja assetit (nekin päätyvät sivustolle vain
    tätä kautta). Funktio eikä vakio, jotta testien vaihtama SRC näkyy."""
    return (SRC, ASSETS)


def snapshot() -> dict[str, int]:
    """Vahdittavien tiedostojen polut ja muokkausajat.

    Kysely eikä inotify, koska inotify ei saa tapahtumia 9p-liitoksen takaa
    (WSL, PERUSTELUT.md). os.scandir on rglobia nopeampi ja st_mtime_ns ei
    vaadi tiedostojen lukemista.
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
            # Tiedosto katosi kesken kyselyn (editorin tallennus); seuraava
            # kysely näkee lopputilan.
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
    """main ilman kopiointiriviä. -> paluuarvo.

    Vahdin tulostus kulkee palvelimen lokin seassa. Varoitukset menevät
    stderriin, joten vaimennus ei piilota niitä.
    """
    with only_one_run(), contextlib.redirect_stdout(io.StringIO()):
        return main()


def watch() -> int:
    """Aja muunnos aina kun lähdepuu tai assetit muuttuvat. -> paluuarvo.

    Ensimmäistä muunnosta ei tehdä: run.sh ajaa sen ennen vahtia, jotta
    `zensical serve` näkee valmiin docs/:n heti.
    """
    print(f"vahti: {SRC} ja {ASSETS}, lopeta Ctrl-C", flush=True)
    state = snapshot()
    try:
        while True:
            time.sleep(WATCH_INTERVAL)
            fresh = snapshot()
            if fresh == state:
                continue
            # Odota, että tallennus on ohi: yksi tallennus tai `git checkout`
            # näkyy monena muutoksena.
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
                # Virhe ei saa tappaa vahtia; se näkyy ja seuraava tallennus
                # yrittää uudelleen.
                traceback.print_exc()
                status = 1
            elapsed = f"{time.monotonic() - started:.1f}".replace(".", ",")
            print(f"{time.strftime('%H:%M:%S')} {watch_label(changed)} -> "
                  + (f"muunnettu {elapsed} s" if status == 0
                     else "muunnos epäonnistui"), flush=True)
            # Lähtötila vasta ajon jälkeen: muunnos kirjoittaa itse
            # assets/plantuml/:iin, eikä se saa laukaista seuraavaa ajoa.
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
