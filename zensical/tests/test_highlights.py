"""Korostetut rivit koekirjalla (README.md kohta 9).

Korostus on kaksiosainen samalla tavalla kuin piilorivit: convert.py riisuu
merkinnät ja kirjoittaa rivien numerot aidan attribuutiksi (test_convert.py),
ja selain merkitsee numeroita vastaavat rivit luokalla, jonka CSS värittää.
Jälkimmäistä ei näe käännöksen tuloksesta, joten sivu avataan oikeasti —
samasta syystä kuin piiloriveillä (test_hidelines.py).

Koekirjan ajettavassa lohkossa (tests/book/src/osa1/01-hei.md) on kolme riviä:
rivit 1 ja 2 ovat korostettuja ja rivit 1 ja 3 piilossa, eli yksi rivi on
molempia. Monitiedostolohkossa kummallakin tiedostolla on oma korostuksensa.
"""

import pytest

BLOCK = "div.highlight[data-hl-green]"
EYE = "[data-md-type=hidelines]"


@pytest.fixture(scope="session")
def chapter_url(book, serve) -> str:
    return f"{serve(book.site)}/osa1/01-hei/"


@pytest.fixture
def page(browser, chapter_url):
    """Oma sivu joka testille: silmänappi jättää jälkensä sivulle."""
    opened = browser.new_page()
    errors: list[str] = []
    opened.on("pageerror", lambda error: errors.append(str(error)))
    opened.goto(chapter_url, wait_until="load")
    yield opened
    assert errors == []
    opened.close()


def test_the_markers_are_not_in_the_page(page):
    """Merkintärivit riisutaan jo käännöksessä, kuten mdBookissakin: ne eivät
    ole koodia vaan ohje sille, mitkä rivit väritetään."""
    assert "HIGHLIGHT_" not in page.inner_text(".md-content__inner")
    assert page.eval_on_selector(BLOCK, "block => block.textContent") == (
        'void main() {\nIO.println("Hei, maailma!");\n}\n')


def test_the_marked_lines_are_the_ones_between_the_markers(page):
    """Numerot osoittavat Pygmentsin rivispaneihin: rivit 1 ja 2, ei rivi 3."""
    assert page.get_attribute(BLOCK, "data-hl-green") == "1 2"
    assert page.eval_on_selector_all(
        f"{BLOCK} code > span",
        "lines => lines.map(line => line.classList.contains('hl-green'))") == [
        True, True, False]


def test_the_colour_comes_from_the_stylesheet(page):
    """Luokka on turha ilman assets/css/highlights.css:ää: jos tiedosto jäisi
    pois mkdocs.yml:stä, rivit merkittäisiin mutta mikään ei näkyisi."""
    style = page.eval_on_selector(
        f"{BLOCK} .hl-green:not(.boring)",
        "line => getComputedStyle(line)['background-color']")
    assert style not in ("rgba(0, 0, 0, 0)", "transparent")


def test_the_band_covers_the_line_from_edge_to_edge(page):
    """Väri ulottuu lohkon reunasta reunaan eikä lopu tekstin loppuun, kuten
    kirjassa: rivi on lohkotason elementti, joka ulottuu koodin sisennyksen
    verran yli molempiin reuniin."""
    assert page.eval_on_selector(f"{BLOCK} .hl-green:not(.boring)", """line => {
      const code = line.parentElement.getBoundingClientRect();
      const band = line.getBoundingClientRect();
      return Math.abs(band.left - code.left) < 1
          && Math.abs(band.right - code.right) < 1;
    }""")


def test_a_marked_line_that_is_hidden_stays_hidden(page):
    """Rivi voi olla sekä piilossa että korostettu (aineistossa kolme lohkoa).
    Piilotus voittaa, ja silmästä rivi tulee esiin väreineen — himmeänä, kuten
    muutkin esiin otetut piilorivit."""
    marked_and_hidden = f"{BLOCK} code > span.boring.hl-green"
    assert page.eval_on_selector(
        marked_and_hidden, "line => getComputedStyle(line).display") == "none"

    page.click(f"{BLOCK} {EYE}")
    assert page.eval_on_selector(marked_and_hidden, """line => {
      const style = getComputedStyle(line);
      return [style.display, style.opacity];
    }""") == ["block", "0.6"]


def test_every_file_of_a_multifile_block_is_marked_on_its_own(page):
    """Rivinumerot lasketaan sen aidan sisällä, jossa rivi lopulta on, joten
    kummankin tiedoston oma rivi 1 on korostettu — eri värillä."""
    assert page.eval_on_selector_all(
        "div.highlight[data-hl-red], div.highlight[data-hl-yellow]",
        """blocks => blocks.map(block => [
             block.querySelector('code > span').className,
             block.querySelectorAll('.hl-line').length])""") == [
        ["hl-line hl-red", 1], ["hl-line hl-yellow", 1]]
