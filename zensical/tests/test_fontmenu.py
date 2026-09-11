"""Leipätekstin kirjasinvalikko koekirjalla, selaimessa.

Valikon vaikutus syntyy vasta selaimessa (attribuutti, localStorage,
inline-skripti ennen sisältöä), joten sivu on avattava oikeasti.
"""

import pytest

KEY = "jyu-font"


@pytest.fixture(scope="module")
def base_url(book, serve):
    return serve(book.site)


def open_page(browser, url, init_script=None):
    """Avaa sivun ja kerää skriptivirheet. -> (sivu, virheet)."""
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    if init_script:
        page.add_init_script(init_script)
    page.goto(url, wait_until="load")
    return page, errors


def body_font(page) -> str | None:
    return page.evaluate("document.body.getAttribute('data-jyu-font')")


def content_font(page) -> str:
    """Artikkelin kirjasinperheen ensimmäinen nimi, lainausmerkit riisuttuna."""
    family = page.evaluate(
        "getComputedStyle(document.querySelector('.md-content__inner')).fontFamily")
    return family.split(",")[0].strip().strip('"')


def label(page) -> str:
    """Painikkeen vihje, jossa nykyinen valinta kerrotaan."""
    return page.get_attribute(".jyu-font__button", "title")


def test_without_a_choice_the_page_is_as_before(browser, base_url):
    """Oletus on Source Serif 4 eikä bodyssä ole attribuuttia: ilman valintaa
    sivu on täsmälleen entisensä, ja painikkeen vihje kertoo nykyisen
    kirjasimen."""
    page, errors = open_page(browser, base_url)
    assert body_font(page) is None
    assert content_font(page) == "Source Serif 4"
    assert label(page) == "Leipätekstin kirjasin: Serif"
    assert page.evaluate(f"localStorage.getItem('{KEY}')") is None
    assert page.is_hidden(".jyu-font__list")
    assert errors == []


def test_a_choice_changes_the_font_and_is_remembered(browser, base_url):
    """Valinta vaihtaa artikkelin kirjasimen, päivittää painikkeen vihjeen ja
    tallentuu selaimeen. Seuraavalla sivulla
    valinta on voimassa jo ennen fontmenu.js:n latautumista (header.html:n
    inline-skripti), joten teksti ei välähdä oletuskirjasimella."""
    page, errors = open_page(browser, base_url)
    page.click(".jyu-font__button")
    assert page.is_visible(".jyu-font__list")
    assert page.evaluate("document.querySelectorAll('.jyu-font__item').length") == 3
    assert page.get_attribute(".jyu-font__button", "aria-expanded") == "true"

    page.click(".jyu-font__item[data-font=literata]")
    assert page.is_hidden(".jyu-font__list")
    assert body_font(page) == "literata"
    assert content_font(page) == "Literata"
    assert label(page) == "Leipätekstin kirjasin: Literata"
    assert page.evaluate(f"localStorage.getItem('{KEY}')") == "literata"
    # Otsikot ja koodi eivät vaihda kirjasinta.
    assert page.evaluate(
        "getComputedStyle(document.querySelector('.md-content__inner h1')).fontFamily"
    ).startswith('"Source Sans 3"')
    assert page.get_attribute(".jyu-font__item[data-font=literata]", "aria-selected") == "true"
    assert page.get_attribute(".jyu-font__item[data-font='']", "aria-selected") == "false"

    # Uusi sivulataus ilman fontmenu.js:ää: attribuutin on oltava silti paikallaan.
    page.route("**/fontmenu.js", lambda route: route.abort())
    page.goto(base_url, wait_until="domcontentloaded")
    assert body_font(page) == "literata"
    assert content_font(page) == "Literata"
    assert errors == []


def test_the_print_page_follows_the_choice(browser, base_url):
    """Tulostussivu liittää luvut samaan .md-content__inneriin, joten valittu
    kirjasin pätee myös siellä ilman omaa koodia."""
    page, errors = open_page(
        browser, f"{base_url}/tulosta/",
        init_script=f"localStorage.setItem('{KEY}', 'atkinson')")
    assert body_font(page) == "atkinson"
    assert content_font(page) == "Atkinson Hyperlegible Next"
    assert label(page) == "Leipätekstin kirjasin: Atkinson"
    assert errors == []


def test_choosing_the_default_forgets_the_choice(browser, base_url):
    """Oletuksen valitseminen poistaa tallennuksen ja attribuutin: "ei
    valintaa" ja "Source Serif 4" ovat sama asia."""
    page, errors = open_page(
        browser, base_url,
        init_script=f"localStorage.setItem('{KEY}', 'atkinson')")
    assert body_font(page) == "atkinson"
    page.click(".jyu-font__button")
    page.click(".jyu-font__item[data-font='']")
    assert body_font(page) is None
    assert content_font(page) == "Source Serif 4"
    assert label(page) == "Leipätekstin kirjasin: Serif"
    assert page.evaluate(f"localStorage.getItem('{KEY}')") is None
    assert errors == []


def test_an_unknown_stored_value_is_ignored(browser, base_url):
    """Vanha tai käsin muokattu arvo ei saa jättää bodyyn attribuuttia, jolle
    ei ole kirjasinta."""
    page, errors = open_page(
        browser, base_url,
        init_script=f"localStorage.setItem('{KEY}', 'comic-sans')")
    assert body_font(page) is None
    assert content_font(page) == "Source Serif 4"
    assert label(page) == "Leipätekstin kirjasin: Serif"
    assert errors == []


def test_the_menu_works_from_the_keyboard(browser, base_url):
    """Sama malli kuin <select>: nuoli alas avaa ja kohdistaa valittuun,
    nuolet liikkuvat, Enter valitsee, Esc sulkee ja palauttaa kohdistuksen."""
    page, errors = open_page(browser, base_url)
    page.focus(".jyu-font__button")
    page.keyboard.press("ArrowDown")
    assert page.is_visible(".jyu-font__list")
    assert page.evaluate("document.activeElement.dataset.font") == ""
    page.keyboard.press("ArrowDown")
    assert page.evaluate("document.activeElement.dataset.font") == "atkinson"
    page.keyboard.press("Enter")
    assert page.is_hidden(".jyu-font__list")
    assert body_font(page) == "atkinson"
    assert page.evaluate("document.activeElement.id") == "jyu-font-button"

    page.keyboard.press("ArrowDown")
    assert page.is_visible(".jyu-font__list")
    assert page.evaluate("document.activeElement.dataset.font") == "atkinson"
    page.keyboard.press("Escape")
    assert page.is_hidden(".jyu-font__list")
    assert body_font(page) == "atkinson"
    assert page.evaluate("document.activeElement.id") == "jyu-font-button"
    assert errors == []
