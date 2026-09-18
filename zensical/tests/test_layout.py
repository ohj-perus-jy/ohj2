"""Sivun asettelu koekirjalla (assets/css/layout.css).

Asettelu näkyy vasta selaimessa, ja teeman JavaScript mittaa sen, joten sivu
avataan oikeasti. Matala ikkuna, jotta luvun otsikon voi vierittää yläreunaan.
"""

import pytest

TOC = ".md-sidebar--secondary"


@pytest.fixture(scope="session")
def chapter_url(book, serve) -> str:
    return f"{serve(book.site)}/osa1/01-hei/"


@pytest.fixture
def page(browser, chapter_url):
    context = browser.new_context(viewport={"width": 1280, "height": 600})
    page = context.new_page()
    page.goto(chapter_url, wait_until="load")
    yield page
    context.close()


def test_contents_link_highlights_its_own_heading(page):
    """Sisällysluettelon linkistä avattu otsikko korostuu itse eikä edellinen
    kohta: teema mittaa korostuksen rajan .md-main__inner-marginaalista."""
    link = page.locator(f"{TOC} a.md-nav__link").nth(2)
    href = link.get_attribute("href")
    link.click()
    page.wait_for_function(
        f"document.getElementById('{href[1:]}').getBoundingClientRect().top < 100")
    page.wait_for_selector(f"{TOC} a.md-nav__link--active[href='{href}']", timeout=2000)


def test_contents_stays_put_when_scrolling(page):
    """Sisällysluettelo ei liiku sisällön mukana ensimmäisiä vierityspikseleitä."""
    title = page.locator(f"{TOC} .md-nav__title")
    start = title.bounding_box()["y"]
    page.evaluate("scrollTo(0, 40)")
    assert title.bounding_box()["y"] == pytest.approx(start, abs=1)


# Luvun avausnuolen kulma asteina chevron-rightistä: 90 alas, -90 ylös, 0 oikealle.
ARROW_ANGLE = """item => {
    const icon = item.querySelector(":scope > .md-nav__container .md-nav__icon")
    const transform = getComputedStyle(icon, "::after").transform
    if (transform === "none")
        return 0
    const [a, b] = transform.match(/matrix\\(([^)]*)\\)/)[1].split(",").map(Number)
    return Math.round(Math.atan2(b, a) * 180 / Math.PI)
}"""


@pytest.mark.parametrize("width", [400, 1280], ids=["puhelin", "työpöytä"])
def test_chapter_arrow_points_where_the_list_moves(browser, chapter_url, width):
    """Avausnuoli osoittaa alas suljettuna ja ylös avattuna myös kapean näytön
    laatikossa: teeman oletus on oikealle ja avattuna alas, mutta alaluvut
    aukeavat paikalleen kaikilla leveyksillä."""
    context = browser.new_context(viewport={"width": width, "height": 700})
    page = context.new_page()
    page.goto(chapter_url, wait_until="load")
    if width < 1220:
        page.click(".md-header__button[for=__drawer]")
    chapters = ".md-sidebar--primary .md-nav--primary > .md-nav__list > .md-nav__item--nested"
    current = page.locator(f"{chapters}.md-nav__item--active")
    other = page.locator(f"{chapters}:not(.md-nav__item--active)").first
    assert current.evaluate(ARROW_ANGLE) == -90
    assert other.evaluate(ARROW_ANGLE) == 90
    other.locator(":scope > .md-nav__container > label.md-nav__link").click()
    page.wait_for_function(f"item => ({ARROW_ANGLE})(item) === -90",
                           arg=other.element_handle(), timeout=2000)
    context.close()


def test_drawer_scrollbar_stays_between_the_rounded_corners(browser, chapter_url):
    """Kapean näytön laatikon vierityspalkin raita alkaa ja päättyy kulmien
    pyöristyksen sisäpuolella, mutta vieritysalue on yhä koko laatikon korkuinen."""
    context = browser.new_context(viewport={"width": 1100, "height": 500})
    page = context.new_page()
    page.goto(chapter_url, wait_until="load")
    page.click(".md-header__button[for=__drawer]")
    box, rail, radius, track = page.evaluate("""() => {
        const drawer = document.querySelector(".md-sidebar--primary")
        const rail = drawer.querySelector(".md-sidebar__scrollwrap")
        const track = getComputedStyle(rail, "::-webkit-scrollbar-track")
        const rect = element => element.getBoundingClientRect().toJSON()
        return [rect(drawer), rect(rail), getComputedStyle(drawer).borderTopLeftRadius,
                [track.marginTop, track.marginBottom]]
    }""")
    assert radius != "0px"
    assert track == [radius, radius]
    assert (rail["top"], rail["bottom"]) == (box["top"], box["bottom"])
    context.close()
