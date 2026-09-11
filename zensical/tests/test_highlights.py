"""Korostetut rivit koekirjalla (README.md kohta 9).

convert.py riisuu merkinnät ja kirjoittaa rivinumerot aidan attribuutiksi
(test_convert.py); selain merkitsee rivit luokalla, jonka CSS värittää.
Koekirjan lohkossa rivit 1 ja 2 ovat korostettuja ja 1 ja 3 piilossa.
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
    """Merkintärivit riisutaan käännöksessä: ne ovat ohje, eivät koodia."""
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
    """Ilman highlights.css:ää rivit merkittäisiin mutta mikään ei näkyisi."""
    style = page.eval_on_selector(
        f"{BLOCK} .hl-green:not(.boring)",
        "line => getComputedStyle(line)['background-color']")
    assert style not in ("rgba(0, 0, 0, 0)", "transparent")


def test_the_band_covers_the_line_from_edge_to_edge(page):
    """Väri ulottuu lohkon reunasta reunaan eikä lopu tekstin loppuun."""
    assert page.eval_on_selector(f"{BLOCK} .hl-green:not(.boring)", """line => {
      const code = line.parentElement.getBoundingClientRect();
      const band = line.getBoundingClientRect();
      return Math.abs(band.left - code.left) < 1
          && Math.abs(band.right - code.right) < 1;
    }""")


def test_a_marked_line_that_is_hidden_stays_hidden(page):
    """Piilotus voittaa korostuksen; silmästä rivi tulee esiin väreineen,
    himmeänä kuten muutkin piilorivit."""
    marked_and_hidden = f"{BLOCK} code > span.boring.hl-green"
    assert page.eval_on_selector(
        marked_and_hidden, "line => getComputedStyle(line).display") == "none"

    page.click(f"{BLOCK} {EYE}")
    assert page.eval_on_selector(marked_and_hidden, """line => {
      const style = getComputedStyle(line);
      return [style.display, style.opacity];
    }""") == ["block", "0.6"]


def test_every_file_of_a_multifile_block_is_marked_on_its_own(page):
    """Rivinumerot lasketaan tiedoston omassa aidassa: kummankin rivi 1 on
    korostettu, eri värillä."""
    assert page.eval_on_selector_all(
        "div.highlight[data-hl-red], div.highlight[data-hl-yellow]",
        """blocks => blocks.map(block => [
             block.querySelector('code > span').className,
             block.querySelectorAll('.hl-line').length])""") == [
        ["hl-line hl-red", 1], ["hl-line hl-yellow", 1]]
