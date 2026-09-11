"""Oikea materiaali (../src) käännettynä.

Koekirja kertoo, toimiiko koneisto; tämä kertoo, toimiiko se oikealla
materiaalilla, ja reagoi siksi materiaalin muuttumiseen. Koko kirja käännetään,
ellei `pytest --nobuild` käytä olemassa olevaa site/:ä.
"""

import re

import pytest

import convert
from conftest import ROOT, open_print_page

SRC = ROOT.parent / "src"

# SUMMARY.md:n linkkirivi. Luetaan erikseen eikä convert.build_navilla, jotta
# testi vertaa tulostetta lähteeseen eikä skriptiä itseensä.
SUMMARY_LINK = re.compile(r"^\s*(?:-\s*)?\[[^\]]*\]\((?P<href>[^)]*)\)")
EDIT_LINK = re.compile(r'href="[^"]*/edit/main/src/(?P<path>[^"]*)"')


def chapter_titles() -> list[str]:
    """SUMMARY.md:n luvut kirjan järjestyksessä, otsikkona sivun oma H1.

    NEST_UNDER-siirto tehdään samasta vakiosta kuin convert.py:ssä: siirto on
    koeputken päätös, ei asia jonka tuloste saisi keksiä itse.
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


# Sisällytetyn tehtävänannon kuvapolku ratkeaa sisällyttävän sivun mukaan ja
# osuu ohi. Sama virhe on mdBookin käännöksessä: korjataan ../src:ssä, ei täällä.
KNOWN_BROKEN_IMAGES = {"osa4/images/adventure.png"}


@pytest.fixture(scope="session")
def printed(real_site, serve, browser):
    return open_print_page(browser, serve(real_site))


def test_every_chapter_is_printed(printed):
    """Jokainen SUMMARY.md:n luku on tulosteessa omalla otsikollaan kirjan
    järjestyksessä: tämä huomaa, jos luku katoaa paperilta."""
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
    """Sama otsikko toistuu luvusta toiseen ja koodirivien ankkurit alkavat joka
    sivulla alusta, joten tunnisteet tarvitsevat luvun etuliitteen. Soittimet
    rajataan ulos: niiden SVG-maski saa saman tunnuksen joka soittimessa."""
    duplicates = printed.evaluate("""() => {
      const ids = [...document.querySelectorAll('[id]')]
        .filter(e => !e.closest('.ap-wrapper')).map(e => e.id);
      return ids.filter((id, i) => ids.indexOf(id) !== i);
    }""")
    assert duplicates == []


def test_internal_anchors_resolve(printed):
    """Yksikään sivun sisäinen linkki ei jää osoittamaan tyhjään."""
    dead = printed.evaluate("""() => {
      const ids = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
      return [...document.querySelectorAll('a[href^="#"]')]
        .map(a => decodeURIComponent(a.getAttribute('href').slice(1)))
        .filter(target => target && !ids.has(target));
    }""")
    # Luvun etuliite riisutaan, jotta virheilmoitus näyttää itse ankkurin.
    assert [anchor.split("--", 1)[-1] for anchor in dead] == []


def test_every_include_is_expanded(printed):
    """Yksikään luku ei jätä {{#include}}-makroa näkyviin."""
    assert printed.evaluate(
        r"() => document.body.textContent.match(/\{\{#include[^}]*\}\}/g)") is None


def test_every_diagram_is_drawn(printed):
    """Kaaviot ovat kuvia, eivät lähdekoodia (kohta 15). "@startuml" esiintyy
    vain plantuml-aidan alussa, joten sivulla näkyvä tarkoittaa kääntämättä
    jäänyttä aitaa. Lukumäärää ei väitetä, koska se muuttuu materiaalin
    mukana."""
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
    """Raaka HTML-lohko ilman markdown-attribuuttia päästää sisältönsä läpi
    sellaisenaan: otsikko jää risuaidoiksi ja lihavointi tähdiksi. Koodi
    rajataan ulos, koska aidassa risuaita on kommentti ja tähti laskutoimitus."""
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
    """Korostukset (kohta 9) koko kirjan mitassa: yhtään merkintää ei jää
    sivulle, jokainen rivinumero osuu lohkon riviin ja merkittyjä rivejä on
    yhtä monta kuin numeroita."""
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
    """Vaatimuskohtien numerot (1.1, 1.2, ...) tulevat CSS-laskurista: jos
    requirements.css jää pois, kohdat numeroituisivat hiljaisesti uudelleen."""
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


def test_every_recording_is_drawn(printed):
    """Jokainen nauhoitus (kohta 16) on soittimena ja kokonaan piirrettynä jo
    tulostushetkellä: rivejä on yhtä monta kuin tageissa rows-määreitä."""
    recordings = printed.evaluate("""() => {
      const tags = [...document.querySelectorAll('asciinema')];
      return {
        tags: tags.length,
        players: tags.filter(tag => tag.querySelector('.ap-wrapper')).length,
        rows: tags.reduce((sum, tag) => sum + Number(tag.getAttribute('rows')), 0),
      };
    }""")
    assert recordings["tags"] > 0
    assert recordings["players"] == recordings["tags"]
    assert printed.drawn_lines == [recordings["rows"]]


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
    """Tunnetun puuttuvan kuvan 404 on ainoa sallittu virhe."""
    assert [error for error in printed.errors
            if not any(image in error for image in KNOWN_BROKEN_IMAGES)] == []


# --- Sivusto ilman selainta --------------------------------------------------

def test_every_edit_link_points_to_an_existing_source_file(real_site):
    """Muokkauslinkki osoittaa ../src:ään, ei docs/:iin. Siirretyt sivut
    hoidetaan polkukartalla, joten uusi siirto rikkoisi linkin hiljaisesti."""
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
