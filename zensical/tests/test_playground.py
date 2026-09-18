"""Java-ohjelmien ajonapit koekirjalla (README.md kohta 3).

Nappi lähettää koodin JYU:n suorituspalvelimelle, joten testit vastaavat
pyyntöön itse (page.route): mitataan mitä selain lähettää ja näyttää, ei
palvelimen tilaa. Koekirjassa on yksi esimerkki kustakin lohkolajista.
Lopussa ohj1:n C#-lohkot omalla sivullaan (osa1/csharp.md).
"""

import json
from dataclasses import dataclass, field

import pytest

# Sama sääntö kuin playground.js:ssä, jotta testi ei osu lohkoon, jossa napin
# ei kuulukaan olla.
SINGLE = "div.highlight.language-java:not(.ignore):not(.noplayground):not(.multifile)"
MULTIFILE = ".tabbed-set:has(.highlight.language-java.multifile:not(.ignore))"


@dataclass
class Chapter:
    """Avattu luku, jonka suorituspyyntöihin testi vastaa itse."""

    page: object
    requests: list = field(default_factory=list)
    errors: list = field(default_factory=list)

    def answer(self, output: str = "", errors: str = "", abort: bool = False,
               hang: bool = False) -> None:
        """Vastaa suorituspyyntöön ilman palvelinta; `abort` katkaisee
        yhteyden ja `hang` jättää vastaamatta."""
        def handle(route):
            self.requests.append(json.loads(route.request.post_data))
            if hang:
                return
            if abort:
                route.abort()
                return
            route.fulfill(status=200, content_type="application/json",
                          body=json.dumps({"errors": errors, "output": output}))

        self.page.route("**/executor/execute", handle)

    def run(self, selector: str) -> str:
        """Paina lohkon ajonappia ja odota tuloste. -> tulosteen teksti."""
        self.page.locator(f"{selector} [data-md-type=run]").first.click()
        self.page.wait_for_function(
            "() => { const code = document.querySelector('.jyu-result code');"
            "        return code && code.textContent !== 'Suoritetaan…'; }",
            timeout=15_000)
        return self.page.inner_text(".jyu-result code")


@pytest.fixture(scope="session")
def chapter_url(book, serve) -> str:
    return f"{serve(book.site)}/osa1/01-hei/"


@pytest.fixture
def chapter(browser, chapter_url) -> Chapter:
    """Oma sivu joka testille: napit ja tulosteet jäävät sivulle."""
    page = browser.new_page()
    opened = Chapter(page)
    page.on("pageerror", lambda error: opened.errors.append(str(error)))
    page.on("console", lambda message: message.type == "error"
            and opened.errors.append(message.text))
    page.goto(chapter_url, wait_until="load")
    yield opened
    page.close()


def test_button_is_added_to_runnable_blocks_only(chapter):
    """Nappi tulee ```java-lohkoon ilman ignore- tai noplayground-määrettä, ja
    monitiedostolohkossa jokaiseen välilehteen."""
    blocks = chapter.page.evaluate("""() => [...document.querySelectorAll('div.highlight')]
      .map(block => [[...block.classList].filter(name => name !== 'highlight').join(' '),
                     block.querySelectorAll('[data-md-type=run]').length])""")
    assert blocks == [
        ["language-java ignore multifile", 0],
        ["language-java ignore multifile", 0],
        ["language-java", 1],
        ["language-java noplayground", 0],
        ["language-java multifile", 1],
        ["language-java multifile", 1],
    ]


def test_request_is_the_same_as_mdbook_sends(chapter):
    """Pyyntö on kenttä kentältä sama kuin ohj1:n mdBookissa: yhden lohkon
    pyynnössä ei ole multifile-kenttää, koska suorituspalvelimen C#-polku
    aikakatkaisee pyynnön, jossa on multifile: false."""
    chapter.answer(output="Hei, maailma!\n")
    assert chapter.run(SINGLE) == "Hei, maailma!"
    assert chapter.requests == [{
        "language": "java",
        "code": 'void main() {\nIO.println("Hei, maailma!");\n}\n',
    }]


def test_hidden_lines_are_run_although_they_are_not_visible(chapter):
    """Piilorivit (kohta 2) kuuluvat ohjelmaan vaikka eivät näy: ilman niitä
    koodista puuttuisi runko."""
    chapter.answer()
    chapter.run(SINGLE)
    assert "void main() {" not in chapter.page.inner_text(SINGLE)
    assert chapter.requests[0]["code"].startswith("void main() {")
    assert "//-" not in chapter.requests[0]["code"]


def test_multifile_block_is_sent_as_one_program(chapter):
    """Välilehdet lähtevät yhtenä ohjelmana nimi -> sisältö -hakemistona."""
    chapter.answer()
    chapter.run(MULTIFILE)
    request = chapter.requests[0]
    assert request["multifile"] is True
    assert json.loads(request["code"]) == {
        "Main.java": "public class Main { }\n",
        "Valo.java": "public class Valo { }\n",
    }


def test_output_appears_under_the_whole_block(chapter):
    """Tuloste tulee koko välilehtijoukon alle: ohjelma on yksi, tulostekin."""
    chapter.answer(output="rivi\n")
    chapter.run(MULTIFILE)
    assert chapter.page.evaluate(
        "() => document.querySelector('.jyu-result')"
        "        .previousElementSibling.classList.contains('tabbed-set')")
    assert chapter.page.eval_on_selector_all(".jyu-result", "e => e.length") == 1


def test_second_run_replaces_the_first_output(chapter):
    """Toinen ajo korvaa edellisen tulosteen eikä lisää uutta laatikkoa."""
    chapter.answer(output="eka\n")
    assert chapter.run(SINGLE) == "eka"
    chapter.page.unroute("**/executor/execute")
    chapter.answer(output="toka\n")
    assert chapter.run(SINGLE) == "toka"
    assert chapter.page.eval_on_selector_all(".jyu-result", "e => e.length") == 1


def test_empty_output_is_said_out_loud(chapter):
    """Tyhjä tuloste sanotaan ääneen; muuten nappi näyttäisi tekemättömältä."""
    chapter.answer(output="\n")
    assert chapter.run(SINGLE) == "Ei tulostetta"


def test_compiler_errors_are_shown(chapter):
    """Kääntäjän virheilmoitus on se, mitä opiskelija tarvitsee useimmin."""
    chapter.answer(errors="main.java:1: error: ';' expected\n")
    assert chapter.run(SINGLE) == "main.java:1: error: ';' expected"


def test_lost_connection_is_shown(chapter):
    """Yhteysvirhe sanotaan; muuten napissa lukisi "Suoritetaan…" ikuisesti."""
    chapter.answer(abort=True)
    assert "Suorituspalvelimeen ei saatu yhteyttä" in chapter.run(SINGLE)


def test_silence_is_given_up_on(chapter):
    """Vastaamatta jäänyt pyyntö katkaistaan 6 sekunnissa; testi kestää sen
    ajan."""
    chapter.answer(hang=True)
    assert chapter.run(SINGLE) == "Ohjelma ei vastannut 6 sekunnissa."


def test_no_console_errors(chapter):
    chapter.answer(output="rivi\n")
    chapter.run(SINGLE)
    assert chapter.errors == []


# --- ohj1: C#-lohkot -----------------------------------------------------------

CSHARP = "div.highlight.language-csharp:not(.ignore):not(.feature-jypeli)"
JYPELI = "div.highlight.language-csharp.feature-jypeli"

# Suorituspalvelin palauttaa Jypelin ikkunan PNG-kuvana data-URI:na merkkien
# välissä tulosteen seassa (playground.js: DATA_URI_RE); tässä 1×1 pikseli.
PIXEL = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAA"
         "C0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
WINDOW = f"@@@DATA_URI_BEGIN@@@{PIXEL}@@@DATA_URI_END@@@"


@pytest.fixture
def csharp_chapter(chapter, book, serve) -> Chapter:
    """chapter koekirjan C#-sivulla, joka on SUMMARY.md:n ulkopuolella, jottei
    ohj2:n testien laskemat luvut ja lohkot muutu."""
    chapter.page.goto(f"{serve(book.site)}/osa1/csharp/", wait_until="load")
    return chapter


def images(chapter: Chapter) -> list:
    """Tulosteen kuvat ladattuina: [src, onko kuva piirtynyt]."""
    chapter.page.wait_for_function(
        "() => [...document.querySelectorAll('img.jyu-result-image')]"
        "        .every(img => img.complete)")
    return chapter.page.eval_on_selector_all(
        ".jyu-result img.jyu-result-image",
        "imgs => imgs.map(img => [img.getAttribute('src'), img.naturalWidth > 0])")


def test_csharp_button_is_added_to_runnable_blocks_only(csharp_chapter):
    """Nappi ```csharp- ja ```csharp,feature-jypeli-lohkoon, ei ignore-lohkoon."""
    blocks = csharp_chapter.page.evaluate("""() => [...document.querySelectorAll('div.highlight')]
      .map(block => [[...block.classList].filter(name => name !== 'highlight').join(' '),
                     block.querySelectorAll('[data-md-type=run]').length])""")
    assert blocks == [
        ["language-csharp", 1],
        ["language-csharp ignore", 0],
        ["language-csharp feature-jypeli", 1],
    ]


def test_csharp_request_is_the_same_as_mdbook_sends(csharp_chapter):
    """Kuten ohj1:n mdBookissa: kieli csharp, piilorivit mukana ilman
    etuliitettä, eikä multifile-kenttää, jonka palvelimen C#-polku
    aikakatkaisee."""
    csharp_chapter.answer(output="Hei, maailma!\n")
    assert csharp_chapter.run(CSHARP) == "Hei, maailma!"
    assert "using System;" not in csharp_chapter.page.inner_text(CSHARP)
    assert csharp_chapter.requests == [{
        "language": "csharp",
        "code": ("using System;\npublic class Hei\n{\n    public static void Main()\n"
                 '    {\n        Console.WriteLine("Hei, maailma!");\n    }\n}\n'),
    }]


def test_jypeli_block_is_sent_with_the_feature(csharp_chapter):
    """feature-jypeli-määre kielen perään, kuten ../theme/playground_ext.js."""
    csharp_chapter.answer(output=WINDOW)
    csharp_chapter.run(JYPELI)
    assert csharp_chapter.requests[0]["language"] == "csharp-jypeli"


def test_jypeli_window_is_the_output(csharp_chapter):
    """Pelkkä ikkunan kuva on tuloste: kuva näkyy, eikä sen yllä lue
    "Ei tulostetta" (mdBookissa lukee)."""
    csharp_chapter.answer(output=WINDOW + "\n")
    assert csharp_chapter.run(JYPELI) == ""
    assert images(csharp_chapter) == [[PIXEL, True]]
    assert not csharp_chapter.page.is_visible(".jyu-result pre")


def test_text_and_window_are_both_shown(csharp_chapter):
    """Tekstiä tulostava peli: teksti laatikkoon ilman merkkejä, kuva alle."""
    csharp_chapter.answer(output=f"Peli alkaa\n{WINDOW}\n")
    assert csharp_chapter.run(JYPELI) == "Peli alkaa"
    assert csharp_chapter.page.is_visible(".jyu-result pre")
    assert images(csharp_chapter) == [[PIXEL, True]]


def test_second_run_replaces_the_window(csharp_chapter):
    """Toinen ajo vie edellisen kuvan, ja tekstilaatikko palaa näkyviin."""
    csharp_chapter.answer(output=WINDOW)
    csharp_chapter.run(JYPELI)
    csharp_chapter.page.unroute("**/executor/execute")
    csharp_chapter.answer(output="rivi\n")
    assert csharp_chapter.run(JYPELI) == "rivi"
    assert images(csharp_chapter) == []
    assert csharp_chapter.page.is_visible(".jyu-result pre")


def test_window_has_the_corners_of_a_code_block(csharp_chapter):
    """Kuva on lohko (ei tekstirivin rakoa alla) ja pyöristetty kuten
    koodilohko; arvot tulevat tyylitiedostosta."""
    csharp_chapter.answer(output=WINDOW)
    csharp_chapter.run(JYPELI)
    images(csharp_chapter)
    assert csharp_chapter.page.evaluate("""() => {
      const img = getComputedStyle(document.querySelector('img.jyu-result-image'));
      const code = getComputedStyle(document.querySelector(
        'div.highlight.feature-jypeli pre > code'));
      return [img.display, img.borderRadius === code.borderRadius];
    }""") == ["block", True]
    assert csharp_chapter.errors == []
