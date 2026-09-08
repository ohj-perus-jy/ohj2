#!/usr/bin/env python3
"""Kopioi mdBookin lähdepuu (../src) Zensicalin docs/-hakemistoksi.

Barebones-lähtötilanne: skripti kopioi tiedostot ja kääntää src/SUMMARY.md:n
nav-lohkoksi, koska ilman navigaatiota sivustoa ei voi selata lainkaan.

Sisältöä muunnetaan neljässä kohdassa: sisällytysmakrot tiedostojen sisällöksi
({{#include}}, convert_includes), koodilohkojen monitiedostomerkinnät
välilehdiksi (// FILE:, convert_files), mdBookin aidan attribuuttilista
(java,ignore) pymdownx:n muotoon (convert_fences) ja työkalusivun
käyttöjärjestelmävalinnat välilehdiksi (### [Windows](#tab/win),
convert_tabs). Muu mdBookin syntaksi (//- piilorivit, > [!VINKKI],
<task>-kortit) jää sellaisenaan sivuille näkyviin. Se on tarkoitus: näin näkee
yhdellä silmäyksellä, mitä oikeasti pitää korjata. Muunnokset lisätään takaisin
yksi kerrallaan, ks. README.md.

Generoitu docs/ on kertakäyttöinen — tämä skripti on totuus.
"""

import re
import shutil
import sys
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


def tab_body(body: list[str]) -> list[str]:
    """Osion sisältö välilehden sisällöksi: tyhjät päät pois, muu 4 välilyöntiä
    sisemmäs. Suhteelliset sisennykset säilyvät, joten listat, koodiaidat ja
    raaka HTML pysyvät ennallaan."""
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
            out.extend(tab_body([f"{marker}{info}", *content, marker]))
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
            out.extend(tab_body(body))
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
    sets = placeholders = blocks = files = fences = includes = 0
    tab_labels: set[str] = set()
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
