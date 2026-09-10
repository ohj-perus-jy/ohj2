"""Tulostussivun koneisto koekirjalla (tests/book/src).

Tulostussivu on koeputken ainoa kohta, jossa lopputulos syntyy vasta
selaimessa: convert.py kirjoittaa sivulle luettelon luvuista ja print.js
hakee jokaisen luvun oman sivun ja liittää siitä artikkelin. Siksi näitä ei
voi testata käännöksen tuloksesta, vaan sivu on avattava oikeasti.

Koekirja on tarkoituksella pieni, mutta siinä on yksi esimerkki jokaisesta
asiasta, joka kokoamisessa voi mennä rikki: sama otsikko kahdessa luvussa
(tunnisteiden törmäys), kuva alihakemistosta (suhteellinen osoite),
sivun sisäinen ankkuri, lukujen välinen linkki, neljä välilehtijoukkoa
(käyttöjärjestelmävalinta ja kolme monitiedostolohkoa), huomiolaatikot ja
sisällytykset.
Oikealla materiaalilla samat asiat mitataan test_book.py:ssä.
"""

import re

import pytest

from conftest import open_print_page

# Koekirjan luvut SUMMARY.md:n järjestyksessä, NEST_UNDER-siirto mukaan
# luettuna (Tenttiohjeet siirtyy Tentin alle mutta pysyy sen perässä).
CHAPTERS = [
    "Aloitus",
    "Tentti",
    "Tenttiohjeet",
    "Perusteet",
    "Hei, maailma",
    "Tehtävät",
    "Työkalut",
    "Tehtävät",
    "Huomiot",
    "Sisällytys",
]


@pytest.fixture(scope="session")
def printed(book, serve, browser):
    """Koekirjan /tulosta/ avattuna kerran: sivu on koottu ja tulostus pyydetty."""
    return open_print_page(browser, serve(book.site))


def test_print_is_requested_only_when_the_book_is_ready(printed):
    """Tulostusikkuna avautuu itsestään, mutta vasta kun kaikki luvut ja kuvat
    ovat valmiina — muuten selain tulostaisi puolityhjän sivun."""
    assert printed.print_calls == [f"Koottu {len(CHAPTERS)} lukua."]


def test_every_chapter_is_assembled_in_order(printed):
    """Jokainen luku on sivulla omana otsikkonaan kirjan järjestyksessä, ja
    luvut ovat suoraan artikkelin lapsina (ei omissa kääreissään, jotka
    rikkoisivat Materialin suorat lapsivalitsimet)."""
    headings = printed.evaluate(
        "() => [...document.querySelectorAll('.md-content__inner > h1')]"
        "        .map(h => h.textContent.replace(/\\u00b6/g, '').trim())")
    assert headings == CHAPTERS
    assert printed.evaluate(
        "() => document.querySelectorAll('.jyu-print-break').length"
    ) == len(CHAPTERS) - 1


def test_identifiers_stay_unique(printed):
    """Sama otsikko esiintyy kirjassa monta kertaa ("Tehtävät"), ja Materialin
    koodirivien ankkurit alkavat joka sivulla alusta. Ilman luvun etuliitettä
    sivulla olisi kaksi kertaa esiintyviä tunnisteita ja linkki veisi
    ensimmäiseen osumaan."""
    duplicates = printed.evaluate("""() => {
      const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
      return ids.filter((id, i) => ids.indexOf(id) !== i);
    }""")
    assert duplicates == []


def test_internal_anchors_still_point_inside_the_page(printed):
    """Sivun sisäiset ankkurit jäävät sivun sisäisiksi, jotta PDF:n linkit
    hyppäävät PDF:n sisällä."""
    dead = printed.evaluate("""() => {
      const ids = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
      return [...document.querySelectorAll('a[href^="#"]')]
        .map(a => decodeURIComponent(a.getAttribute('href').slice(1)))
        .filter(target => target && !ids.has(target));
    }""")
    assert dead == []


def test_links_between_chapters_become_absolute(printed):
    """Suhteelliset linkit ratkaistaan luvun oman sivun suhteen: tulostussivu
    on eri hakemistossa, joten muuten ne osoittaisivat väärään paikkaan.

    Katsotaan vain koottua sisältöä: teeman oma navigaatio ja alatunniste
    ovat artikkelin ulkopuolella eikä print.js koske niihin."""
    relative = printed.evaluate("""() => [...document.querySelectorAll(
        '.md-content__inner a[href]')]
      .map(a => a.getAttribute('href'))
      .filter(href => !/^(#|[a-z][a-z0-9+.-]*:|\\/\\/)/i.test(href))""")
    assert relative == []


def test_images_are_loaded(printed):
    """Kuvat ovat valmiina ennen tulostusikkunaa: selain tulostaa sen mitä
    ruudulla on, ja lataamaton kuva jäisi tyhjäksi laatikoksi. Koekirjassa
    kuvia on kaksi, joista toinen viitataan alihakemistosta."""
    images = printed.evaluate("""() => [...document.querySelectorAll('img')]
      .map(img => ({src: img.getAttribute('src'), ok: img.complete && img.naturalWidth > 0}))""")
    assert len(images) == 2
    assert [image for image in images if not image["ok"]] == []


def test_tab_sets_stay_independent(printed):
    """Välilehtien for- ja name-attribuutit eivät ole tunnisteita, joten ne
    tarvitsevat etuliitteen erikseen: muuten jokaisen luvun __tabbed_1
    kuuluisi samaan ryhmään ja koko sivulla olisi yksi valinta."""
    tabs = printed.evaluate("""() => ({
      sets: document.querySelectorAll('.tabbed-set').length,
      groups: new Set([...document.querySelectorAll('.tabbed-set input[name]')]
        .map(input => input.name)).size,
      checked: document.querySelectorAll('.tabbed-set input:checked').length,
    })""")
    assert tabs == {"sets": 4, "groups": 4, "checked": 4}


def test_admonitions_keep_their_own_titles(printed):
    """Alertin otsikko kirjoitetaan käännöksessä näkyviin (kohta 7): ilman sitä
    Material näyttäisi tyypin oman englanninkielisen nimen ("Tip")."""
    assert printed.evaluate(
        "() => [...document.querySelectorAll('.admonition-title')]"
        "        .map(title => title.textContent.trim())") == [
        "Vinkki", "Huomautus"]


def test_includes_are_expanded_before_the_book_is_built(printed):
    """Sisällytys ratkaistaan lähdepuussa (kohta 1), joten paperille tulee
    tiedoston sisältö eikä makro: koko tiedosto, yksi rivi taulukon soluun ja
    koodiaidan sisällä monitiedostolohkon välilehdeksi."""
    content = printed.evaluate(
        "() => document.querySelector('.md-content__inner').innerText")
    assert "{{#include" not in content
    assert content.count("Ensimmäinen rivi mahtuu taulukon soluun.") == 2
    assert "Sisällytetty tiedosto." in content


def test_hidden_lines_stay_hidden_on_paper(printed):
    """Piilorivit (kohta 2) piilotetaan selaimessa, ja tulostussivun luvut ovat
    olemassa vasta kokoamisen jälkeen. Ilman print.js:n ilmoitusta ne
    tulostuisivat kirjan mukana; mdBookissa print.html on tavallinen sivu,
    jolla book.js piilottaa ne muiden sivujen tapaan."""
    assert printed.evaluate(
        "() => document.querySelectorAll('.boring').length") == 2
    assert printed.evaluate(
        "() => document.querySelector('.hide-boring') !== null")
    assert "void main() {" not in printed.evaluate(
        "() => document.querySelector('.md-content__inner').innerText")


def test_marked_lines_are_coloured_on_paper(printed):
    """Korostukset (kohta 9) merkitään selaimessa, ja tulostussivun luvut ovat
    olemassa vasta kokoamisen jälkeen. Ilman print.js:n ilmoitusta korostukset
    jäisivät kirjasta pois; sama kytkentä kuin piiloriveillä.

    Koekirjassa korostettuja rivejä on neljä: kaksi ajettavassa lohkossa
    (toinen niistä piilorivi) ja yksi kummassakin monitiedostolohkon
    tiedostossa."""
    assert printed.evaluate(
        "() => document.querySelectorAll('.hl-line').length") == 4
    assert printed.evaluate("""() => [...document.querySelectorAll('.hl-line')]
        .every(line => getComputedStyle(line)['background-color']
                       !== 'rgba(0, 0, 0, 0)')""")


def test_per_page_actions_are_dropped(printed):
    """Muokkauslinkki ja palauteruutu ovat artikkelin sisällä, joten ne
    tulisivat muuten jokaisen luvun perään."""
    assert printed.evaluate(
        "() => document.querySelectorAll("
        "'.md-content__button, .md-source-file, .md-feedback').length") == 0


def test_no_console_errors(printed):
    assert printed.errors == []


def test_without_javascript_the_page_is_a_table_of_contents(book):
    """Sivun rungon kirjoittaa convert.py, joten ilman JavaScriptiä sivulla on
    kirjan sisällysluettelo eikä tyhjä sivu."""
    html = (book.site / "tulosta" / "index.html").read_text(encoding="utf-8")
    listing = re.search(r'<div id="jyu-print">(.*?)</div>', html, re.S)
    assert listing, "tulostussivulta puuttuu luettelo"
    assert len(re.findall(r"<li>", listing.group(1))) == len(CHAPTERS)
