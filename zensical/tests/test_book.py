"""Oikea materiaali (../src) käännettynä.

Koekirja (test_print.py, test_change.py) kertoo, toimiiko koneisto. Tämä
kertoo, toimiiko se sillä materiaalilla joka oikeasti on olemassa: 72 lukua,
joissa on mdBookin syntaksia, raakaa HTML:ää ja puolivalmiita lohkoja.
Nämä testit ovat siksi ne, jotka reagoivat materiaalin muuttumiseen.

Kestää n. 25 s, koska koko kirja käännetään. `pytest --nobuild` käyttää
olemassa olevaa site/:ä, kun muutos on jo käännetty (esim. run.sh:n jäljiltä).
"""

import re

import pytest

import convert
from conftest import ROOT, open_print_page

SRC = ROOT.parent / "src"

# SUMMARY.md:n rivi: "[Otsikko](./polku.md)" tai "- [Otsikko](./polku.md)".
# Luetaan tässä erikseen eikä convert.build_navilla, jotta testi vertaa
# tulostetta lähteeseen eikä skriptiä itseensä.
SUMMARY_LINK = re.compile(r"^\s*(?:-\s*)?\[[^\]]*\]\((?P<href>[^)]*)\)")
EDIT_LINK = re.compile(r'href="[^"]*/edit/main/src/(?P<path>[^"]*)"')


def chapter_titles() -> list[str]:
    """SUMMARY.md:n luvut kirjan järjestyksessä, otsikkona sivun oma H1.

    Ulkoiset linkit eivät ole lukuja eivätkä päädy tulostussivulle.
    NEST_UNDER-siirto tehdään tässä samasta vakiosta, josta convert.py sen
    lukee: siirto on koeputken oma päätös (Tenttiohjeet Tentin alasivuksi),
    ei asia jonka tuloste saisi keksiä itse.
    """
    order: list[str] = []
    for line in (SRC / "SUMMARY.md").read_text(encoding="utf-8").splitlines():
        match = SUMMARY_LINK.match(line)
        if not match:
            continue
        href = match["href"].strip().lstrip("./")
        if href.endswith(".md"):
            order.append(href)
    for child, parent in convert.NEST_UNDER.items():
        order.remove(child)
        order.insert(order.index(parent) + 1, child)
    return [next(line[2:].strip()
                 for line in (SRC / href).read_text(encoding="utf-8").splitlines()
                 if line.startswith("# "))
            for href in order]


# Tarkistuslistan kohta 1: sisällytys tuo tehtävänannon kuvaviittaukset sivulle
# sellaisenaan, ja suhteellinen polku ratkeaa sen sivun mukaan, jolle anto
# sisällytetään. exercises/4-3-seikkailupeli/handout.md viittaa
# "images/adventure.png":hen, mutta kuva on osa3/images/:ssä ja anto
# sisällytetään osa4:n kahdelle sivulle. Sama on mdBookin omassa käännöksessä
# (book/osa4/03-perinta-ja-rajapinta.html, book/osa4/05-tehtavat.html), eli
# aineiston virhe, joka korjataan ../src:ssä eikä täällä.
KNOWN_BROKEN_IMAGES = {"osa4/images/adventure.png"}


@pytest.fixture(scope="session")
def printed(real_site, serve, browser):
    return open_print_page(browser, serve(real_site))


def test_every_chapter_is_printed(printed):
    """Jokainen SUMMARY.md:n luku on tulosteessa omalla otsikollaan ja kirjan
    järjestyksessä. Tämä on se testi, joka huomaa, jos luku katoaa paperilta
    materiaalia muutettaessa."""
    headings = printed.evaluate(
        "() => [...document.querySelectorAll('.md-content__inner > h1')]"
        "        .map(h => h.textContent.replace(/\\u00b6/g, '').trim())")
    assert headings == chapter_titles()


def test_print_is_requested_after_the_whole_book_is_ready(printed):
    assert printed.print_calls == [f"Koottu {len(chapter_titles())} lukua."]


def test_page_break_between_every_chapter(printed):
    assert printed.evaluate(
        "() => document.querySelectorAll('.jyu-print-break').length"
    ) == len(chapter_titles()) - 1


def test_identifiers_stay_unique(printed):
    """Sama otsikko toistuu luvusta toiseen ("Tehtävät") ja koodirivien
    ankkurit alkavat joka sivulla alusta: ilman luvun etuliitettä sivulla
    olisi 1767 kahteen kertaan esiintyvää tunnistetta."""
    duplicates = printed.evaluate("""() => {
      const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
      return ids.filter((id, i) => ids.indexOf(id) !== i);
    }""")
    assert duplicates == []


def test_internal_anchors_resolve(printed):
    """Sivun sisäisiä linkkejä on yli 9000; yksikään ei jää osoittamaan
    tyhjään.

    Poikkeuksia oli kolme siihen asti, kunnes tarkistuslistan kohta 13
    tehtiin. Kaksi niistä oli ääkkösiä ankkurissa, jotka toimivat mdBookissa
    mutta eivät täällä; ne poistuivat convert_anchorsin mukana. Kolmas oli
    aineiston virhe, joka oli rikki mdBookissakin
    (harjoitustyo.md linkitti ankkuriin
    "#harjoitustyön-tekniset-vaatimukset-ja-arviointi", vaikka otsikko on
    "## Tekniset vaatimukset ja arviointi"), ja se korjattiin ../src:ssä
    — toisin kuin KNOWN_BROKEN_IMAGES, joka on yhä auki."""
    dead = printed.evaluate("""() => {
      const ids = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
      return [...document.querySelectorAll('a[href^="#"]')]
        .map(a => decodeURIComponent(a.getAttribute('href').slice(1)))
        .filter(target => target && !ids.has(target));
    }""")
    # Etuliite on luvun oma, joten sama rikkinäinen linkki näkyisi tässä
    # luvun nimellä varustettuna.
    assert [anchor.split("--", 1)[-1] for anchor in dead] == []


def test_every_include_is_expanded(printed):
    """Yksikään luku ei jätä {{#include}}-makroa näkyviin. Neljä makroa jää,
    mutta ne ovat kirjan ulkopuolisella sivulla (extra/), joka ei ole
    SUMMARY.md:ssä eikä siksi tulosteessa."""
    assert printed.evaluate(
        r"() => document.body.textContent.match(/\{\{#include[^}]*\}\}/g)") is None


def test_every_diagram_is_drawn(printed):
    """Kaaviot ovat kuvia, eivät lähdekoodia (kohta 15).

    "@startuml" ei esiinny aineistossa muualla kuin ```plantuml-aidan
    ensimmäisellä rivillä, joten jos se näkyy sivulla, jokin aita on jäänyt
    kääntämättä — esimerkiksi siksi, että kaavio on uusi eikä sitä ole
    assets/plantuml/:ssä eikä PlantUML-palvelinta saatu kiinni.

    Kaavioiden lukumäärää ei väitetä, koska se muuttuu materiaalin mukana;
    sen sijaan vaaditaan, ettei yksikään kääre ole tyhjä."""
    diagrams = printed.evaluate("""() => ({
      startuml: (document.body.textContent.match(/@startuml/g) || []).length,
      uml: document.querySelectorAll('img.uml').length,
      svgbob: document.querySelectorAll('div.svgbob').length,
      emptyBob: [...document.querySelectorAll('div.svgbob')]
        .filter(d => !d.querySelector('svg')).length,
    })""")
    assert diagrams["startuml"] == 0
    assert diagrams["uml"] > 0 and diagrams["svgbob"] > 0
    assert diagrams["emptyBob"] == 0


def test_no_raw_markdown_leaks_into_the_page(printed):
    """Raaka HTML-lohko päästää sisältönsä läpi sellaisenaan, ja silloin
    otsikko jää risuaidoiksi ja lihavointi tähdiksi keskelle leipätekstiä.
    Näin kävi harjoitustyön kahdeksalle vaatimuslohkolle (kohta 25) ja kuudelle
    aihelohkolle (kohta 8), ja sama toistuu heti, jos aineistoon tulee uusi
    <div> tai <summary> ilman markdown-attribuuttia.

    Koodi rajataan ulos: aidan sisällä risuaita on kommentti ja tähti
    laskutoimitus."""
    leaked = printed.evaluate(r"""() => {
      const walker = document.createTreeWalker(
        document.querySelector('.md-content__inner'), NodeFilter.SHOW_TEXT);
      const raw = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (node.parentElement.closest('pre, code')) continue;
        for (const line of node.textContent.split('\n'))
          if (/^\s*#{1,6}\s\S/.test(line) || /\*\*\S/.test(line))
            raw.push(line.trim().slice(0, 70));
      }
      return raw;
    }""")
    assert leaked == []


def test_every_marked_line_is_a_real_line(printed):
    """Korostukset (kohta 9): merkinnät riisutaan käännöksessä ja rivinumerot
    kirjoitetaan aidan attribuutiksi, joten kaksi asiaa voi mennä pieleen koko
    kirjan mitassa. Merkintä voi jäädä sivulle, jos aineistossa on kirjoitusasu
    jota lauseke ei tunne, ja numero voi osoittaa lohkon ulkopuolelle, jos
    numerointi laskee eri rungosta kuin se, joka lopulta piirretään — juuri
    niin kävi piiloriveillä (kohta 2) ennen kuin numerointi korjattiin.

    Kysytään siis kirjalta itseltään: yhtään merkintää ei ole jäljellä,
    jokainen numero osuu lohkon riviin, ja merkittyjä rivejä on tasan yhtä
    monta kuin numeroita."""
    marked = printed.evaluate(r"""() => {
      let numbers = 0, outside = 0, blocks = 0;
      for (const block of document.querySelectorAll('div.highlight')) {
        const lines = block.querySelectorAll('code > span');
        let coloured = false;
        for (const [name, value] of Object.entries(block.dataset)) {
          if (!/^hl[A-Z]/.test(name)) continue;
          coloured = true;
          for (const number of value.split(' ')) {
            numbers++;
            if (!lines[Number(number) - 1]) outside++;
          }
        }
        blocks += coloured ? 1 : 0;
      }
      return {
        numbers, outside, blocks,
        lines: document.querySelectorAll('.hl-line').length,
        markers: (document.querySelector('.md-content__inner').textContent
                  .match(/HIGHLIGHT_/g) || []).length,
      };
    }""")
    assert marked["markers"] == 0
    assert marked["outside"] == 0
    assert marked["blocks"] > 0
    assert marked["numbers"] == marked["lines"] > 0


def test_requirement_numbers_come_from_the_counter(printed):
    """Harjoitustyön vaatimuskohdat numeroidaan lohkon ja kohdan mukaan
    (1.1, 1.2, ...), koska niihin viitataan numerolla sekä samalla sivulla
    että osien 9-12 ohjeissa. Numero tulee CSS-laskurista kuten kirjassakin,
    joten testi kysyy laskuria: jos assets/css/requirements.css jää pois
    mkdocs.yml:stä, kohdat numeroituisivat hiljaisesti uudelleen 1:stä."""
    counters = printed.evaluate("""() => {
      const reqs = [...document.querySelectorAll('.ht-reqs .req')];
      return {
        blocks: reqs.length,
        reset: [...document.querySelectorAll('.ht-reqs')]
          .map(e => getComputedStyle(e).counterReset),
        increment: [...new Set(reqs.map(e => getComputedStyle(e).counterIncrement))],
        marker: [...new Set(reqs.map(e => {
          const item = e.querySelector(':scope > ol > li');
          return item && getComputedStyle(item, '::marker').content;
        }))],
      };
    }""")
    assert counters["blocks"] == 8
    assert counters["reset"] == ["req 0"]
    assert counters["increment"] == ["req 1"]
    assert counters["marker"] == ['counter(req) "." counter(list-item) " "']


def test_every_image_is_loaded(printed):
    """Tulostus odottaa kuvia, joten yksikään ei saa jäädä tyhjäksi laatikoksi
    paitsi tunnetun poikkeuksen verran."""
    broken = printed.evaluate("""() => [...document.querySelectorAll('img')]
      .filter(img => !img.complete || img.naturalWidth === 0)
      .map(img => new URL(img.src, location.href).pathname.slice(1))""")
    assert set(broken) <= KNOWN_BROKEN_IMAGES


def test_tab_sets_stay_independent(printed):
    """Jokainen välilehtijoukko on oma ryhmänsä ja yksi välilehti valittuna."""
    tabs = printed.evaluate("""() => ({
      sets: document.querySelectorAll('.tabbed-set').length,
      groups: new Set([...document.querySelectorAll('.tabbed-set input[name]')]
        .map(input => input.name)).size,
      checked: document.querySelectorAll('.tabbed-set input:checked').length,
    })""")
    assert tabs["sets"] == tabs["groups"] == tabs["checked"]
    assert tabs["sets"] > 0


def test_no_console_errors(printed):
    """Tunnetun puuttuvan kuvan 404 on ainoa sallittu; se on aineiston virhe,
    ei tulostuksen. Osoite on virhetekstissä mukana, jotta muut 404:t
    erottuvat siitä."""
    assert [error for error in printed.errors
            if not any(image in error for image in KNOWN_BROKEN_IMAGES)] == []


# --- Sivusto ilman selainta --------------------------------------------------

def test_every_edit_link_points_to_an_existing_source_file(real_site):
    """Muokkauslinkki osoittaa ../src:ään, ei koeputken kertakäyttöiseen
    docs/:iin. Siirretyt ja generoidut sivut hoidetaan polkukartalla
    (nav.yml: extra.edit_source), joten uusi siirto rikkoisi linkin
    hiljaisesti."""
    pages = missing = 0
    for page in real_site.rglob("index.html"):
        for match in EDIT_LINK.finditer(page.read_text(encoding="utf-8")):
            pages += 1
            if not (SRC / match["path"]).is_file():
                missing += 1
                print(f"{page}: {match['path']} puuttuu ../src:stä")
    assert pages > len(chapter_titles())
    assert missing == 0


def test_print_page_has_no_edit_link(real_site):
    """Tulostussivu syntyy convert.py:ssä eikä sitä voi muokata."""
    html = (real_site / "tulosta" / "index.html").read_text(encoding="utf-8")
    assert EDIT_LINK.search(html) is None


def test_print_page_is_not_in_the_search_index(real_site):
    """Sivu on koko kirja toiseen kertaan: hakuun se toisi joka osumasta
    kaksoiskappaleen."""
    index = (real_site / "search.json").read_text(encoding="utf-8")
    assert '"tulosta/"' not in index
