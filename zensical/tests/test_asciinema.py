"""Terminaalinauhoitukset koekirjalla (README.md kohta 16).

Nauhoitus on lähteessä raakaa HTML:ää (`<asciinema src="...">`), joten
convert.py ei tee sille mitään: tagi menee käännöksen läpi sellaisenaan ja
kaikki muu tapahtuu selaimessa. Siksi sivu on avattava oikeasti, samasta
syystä kuin piiloriveillä (test_hidelines.py).

Koekirjan luvussa (tests/book/src/osa1/01-hei.md) on kaksi nauhoitusta samasta
tiedostosta: yksi ilman toistopalkkia ja yksi `controls`-määreellä, kuten
kirjassa. Nauhoitus (`images/nauhoitus.cast`) on kolme riviä pitkä ja sen
osoite on suhteellinen luvun omaan hakemistoon.
"""

import pytest

PLAYER = "assets/js/asciinema-player.min.js"


@pytest.fixture(scope="session")
def chapter_url(book, serve) -> str:
    return f"{serve(book.site)}/osa1/01-hei/"


@pytest.fixture
def page(browser, chapter_url):
    """Oma sivu joka testille: soitin muuttaa sivua ja toisto jää päälle."""
    opened = browser.new_page()
    errors: list[str] = []
    opened.on("pageerror", lambda error: errors.append(str(error)))
    opened.on("console", lambda message: message.type == "error"
              and errors.append(f"{message.text} {message.location['url']}".strip()))
    opened.goto(chapter_url, wait_until="load")
    opened.wait_for_selector("asciinema .ap-line")
    yield opened
    assert errors == []
    opened.close()


def test_every_recording_becomes_a_player(page):
    """Ilman soitinta tagi on selaimelle tuntematon elementti, joka ei näy
    sivulla mitenkään — juuri niin kohta 16 oli rikki."""
    assert page.eval_on_selector_all(
        "asciinema", "elements => elements.map(element =>"
        "  element.querySelectorAll(':scope > .ap-wrapper').length)") == [1, 1]


def test_the_first_frame_is_drawn_from_the_recording(page):
    """Poster näyttää nauhoituksen ensimmäisen ruudun ilman toistoa. Sisältö
    tulee .cast-tiedostosta, eli tämä on samalla ainoa tapa nähdä, että
    suhteellinen osoite osui oikeaan tiedostoon."""
    assert page.eval_on_selector(
        "asciinema", "element => [...element.querySelectorAll('.ap-line')]"
        "                          .map(line => line.textContent.trim())") == [
        "$ javac Ohjelma.java", "$ java Ohjelma", "Hei, maailma!"]


def test_the_attributes_of_the_tag_reach_the_player(page):
    """rows on nauhoituksen korkeus riveinä ja controls kertoo, näkyykö
    toistopalkki: kirjassa se on yhdessä nauhoituksessa kolmestatoista."""
    assert page.eval_on_selector_all(
        "asciinema", "elements => elements.map(element => ["
        "  element.getAttribute('rows'),"
        "  element.querySelectorAll('.ap-line').length,"
        "  element.hasAttribute('controls'),"
        "  element.querySelectorAll('.ap-control-bar').length])") == [
        ["3", 3, False, 0], ["3", 3, True, 1]]


def test_the_recording_plays(page):
    """Toistonappi on nauhoituksen ainoa tarkoitus. Toisto alkaa alusta, joten
    ensimmäinen rivi on kesken kirjoittamisen eikä enää sama kuin poster."""
    page.click("asciinema .ap-play-button")
    page.wait_for_function(
        "() => document.querySelector('asciinema .ap-line').textContent.trim()"
        "        !== '$ javac Ohjelma.java'")


def test_the_player_is_fetched_only_where_it_is_needed(browser, book, serve):
    """Soitin ja sen tyyli ovat 207 kt, eivätkä ne kuulu sivulle, jolla ei ole
    nauhoitusta: kirjassa niitä on kolmella sivulla 190:stä. Siksi mkdocs.yml
    lataa vain assets/js/asciinema.js:n, joka hakee soittimen tarvittaessa."""
    base = serve(book.site)
    for path, wanted in (("/osa1/01-hei/", True), ("/osa2/02-huomiot/", False)):
        opened = browser.new_page()
        fetched: list[str] = []
        opened.on("request", lambda request: PLAYER in request.url
                  and fetched.append(request.url))
        opened.goto(f"{base}{path}", wait_until="load")
        if wanted:
            opened.wait_for_selector("asciinema .ap-line")
        else:
            opened.wait_for_timeout(500)
        assert bool(fetched) is wanted, path
        opened.close()
