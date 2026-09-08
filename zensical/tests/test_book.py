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


# Ankkurit, jotka eivät osu mihinkään. Kaksi eri syytä, kumpikaan ei ole
# tulostuksen vika.
#
# Kaksi ensimmäistä ovat tarkistuslistan kohta 13, ääkköset ankkureissa:
# Zensical riisuu otsikoiden tunnisteista ääkköset (#käyttö -> #kaytto), mutta
# sivujen omissa linkeissä ne ovat yhä tallessa. mdBookissa nämä linkit
# toimivat (book/osa1/01-hei-java.html: sekä href että id ovat ääkkösineen),
# eli ne poistuvat kohdan 13 mukana.
#
# Kolmas on aineiston virhe: harjoitustyo.md linkittää ankkuriin
# "#harjoitustyön-tekniset-vaatimukset-ja-arviointi", mutta otsikko on
# "## Tekniset vaatimukset ja arviointi" ilman etuliitettä. Linkki on rikki myös
# mdBookin omassa käännöksessä (book/harjoitustyo.html:
# href="#harjoitusty%C3%B6n-..." ilman kohdetta), eli se korjataan ../src:ssä
# eikä täällä — kuten KNOWN_BROKEN_IMAGES.
#
# Kaksi jälkimmäistä tulivat näkyviin vasta kohdan 8 mukana: molemmat ovat
# <details>-lohkon sisällä, eikä niistä ennen markdown-attribuuttia syntynyt
# linkkiä lainkaan.
KNOWN_DEAD_ANCHORS = {
    "comparable-rajapinta-ja-luonnollinen-järjestys",
    "opas-java-ohjelmien-kääntäminen-ja-ajaminen",
    "harjoitustyön-tekniset-vaatimukset-ja-arviointi",
}

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
    """Sivun sisäisiä linkkejä on yli 9000; yhdenkään ei pitäisi jäädä
    osoittamaan tyhjään paitsi tunnetun poikkeuksen verran."""
    dead = printed.evaluate("""() => {
      const ids = new Set([...document.querySelectorAll('[id]')].map(e => e.id));
      return [...document.querySelectorAll('a[href^="#"]')]
        .map(a => decodeURIComponent(a.getAttribute('href').slice(1)))
        .filter(target => target && !ids.has(target));
    }""")
    # Etuliite on luvun oma, joten sama rikkinäinen linkki näkyy tässä
    # luvun nimellä varustettuna.
    assert {anchor.split("--", 1)[-1] for anchor in dead} <= KNOWN_DEAD_ANCHORS


def test_every_include_is_expanded(printed):
    """Yksikään luku ei jätä {{#include}}-makroa näkyviin. Neljä makroa jää,
    mutta ne ovat kirjan ulkopuolisella sivulla (extra/), joka ei ole
    SUMMARY.md:ssä eikä siksi tulosteessa."""
    assert printed.evaluate(
        r"() => document.body.textContent.match(/\{\{#include[^}]*\}\}/g)") is None


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
