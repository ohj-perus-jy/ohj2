"""Java-ohjelmien ajonapit koekirjalla (README.md kohta 3).

Nappi on ainoa kohta koeputkessa, jossa sivu puhuu ulos päin: se lähettää
koodin JYU:n suorituspalvelimelle ja näyttää vastauksen. Siksi testit eivät
kutsu palvelinta vaan vastaavat pyyntöön itse (page.route). Silloin ne
mittaavat sitä mitä selain lähettää ja mitä se vastauksesta näyttää — eivät
sitä, onko lakane.it.jyu.fi juuri nyt pystyssä.

Koekirjassa on yksi esimerkki kustakin lajista: ajettava lohko piiloriveineen,
noplayground-lohko, ajettava monitiedostolohko ja ignore-määreinen
monitiedostolohko (tests/book/src/osa1/01-hei.md).
"""

import json
from dataclasses import dataclass, field

import pytest

# Ajettava tavallinen lohko ja ajettava monitiedostolohko. Molemmissa
# valitsimissa on sama sääntö kuin playground.js:ssä, jotta testi ei osu
# vahingossa lohkoon, jossa napin ei kuulukaan olla.
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
        """Vastaa suorituspyyntöön ilman palvelinta.

        Vastauksessa on samat kentät kuin oikeassa (errors, output).
        `abort` katkaisee yhteyden ja `hang` jättää vastaamatta kokonaan.
        """
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
    """Nappi tulee ```java-lohkoon, jossa ei ole ignore- eikä noplayground-
    määrettä, ja monitiedostolohkossa jokaiseen välilehteen — sama sääntö kuin
    mdBookissa (theme/playground_ext.js: get_playgrounds)."""
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
    """Pyyntö on kenttä kentältä sama kuin mdBookissa: kieli, koodi ja tieto
    siitä, onko kyseessä monitiedostolohko."""
    chapter.answer(output="Hei, maailma!\n")
    assert chapter.run(SINGLE) == "Hei, maailma!"
    assert chapter.requests == [{
        "language": "java",
        "code": 'void main() {\nIO.println("Hei, maailma!");\n}\n',
        "multifile": False,
    }]


def test_hidden_lines_are_run_although_they_are_not_visible(chapter):
    """Piilorivit (kohta 2) eivät näy sivulla mutta kuuluvat ohjelmaan: ilman
    niitä lähtisi koodi, josta puuttuu runko eikä mikään kääntyisi. Etuliite on
    riisuttu jo käännösaikana, joten napin ei tarvitse tietää niistä mitään."""
    chapter.answer()
    chapter.run(SINGLE)
    assert "void main() {" not in chapter.page.inner_text(SINGLE)
    assert chapter.requests[0]["code"].startswith("void main() {")
    assert "//-" not in chapter.requests[0]["code"]


def test_multifile_block_is_sent_as_one_program(chapter):
    """Monitiedostolohkon välilehdet ovat yhdessä yksi ohjelma: nimi ->
    sisältö -hakemistona, samoin kuin mdBook lähettää ne."""
    chapter.answer()
    chapter.run(MULTIFILE)
    request = chapter.requests[0]
    assert request["multifile"] is True
    assert json.loads(request["code"]) == {
        "Main.java": "public class Main { }\n",
        "Valo.java": "public class Valo { }\n",
    }


def test_output_appears_under_the_whole_block(chapter):
    """Tuloste tulee koodin alle ja monitiedostolohkossa koko välilehtijoukon
    alle: ohjelma on yksi, joten tulosteitakin on yksi."""
    chapter.answer(output="rivi\n")
    chapter.run(MULTIFILE)
    assert chapter.page.evaluate(
        "() => document.querySelector('.jyu-result')"
        "        .previousElementSibling.classList.contains('tabbed-set')")
    assert chapter.page.eval_on_selector_all(".jyu-result", "e => e.length") == 1


def test_second_run_replaces_the_first_output(chapter):
    """Toinen ajo korvaa edellisen tulosteen eikä kasvata sivua uudella
    laatikolla."""
    chapter.answer(output="eka\n")
    assert chapter.run(SINGLE) == "eka"
    chapter.page.unroute("**/executor/execute")
    chapter.answer(output="toka\n")
    assert chapter.run(SINGLE) == "toka"
    assert chapter.page.eval_on_selector_all(".jyu-result", "e => e.length") == 1


def test_empty_output_is_said_out_loud(chapter):
    """Tyhjä tuloste on ohjelman tulos siinä missä muutkin. Ilman tekstiä napin
    painaminen näyttäisi siltä, ettei mitään tapahtunut; mdBook sanoo saman
    ("No output")."""
    chapter.answer(output="\n")
    assert chapter.run(SINGLE) == "Ei tulostetta"


def test_compiler_errors_are_shown(chapter):
    """Kääntäjän virheilmoitus on se, mitä opiskelija tarvitsee useimmin."""
    chapter.answer(errors="main.java:1: error: ';' expected\n")
    assert chapter.run(SINGLE) == "main.java:1: error: ';' expected"


def test_lost_connection_is_shown(chapter):
    """Jos palvelimeen ei saada yhteyttä, se sanotaan. Muuten napissa jäisi
    lukemaan "Suoritetaan…" ikuisesti."""
    chapter.answer(abort=True)
    assert "Suorituspalvelimeen ei saatu yhteyttä" in chapter.run(SINGLE)


def test_silence_is_given_up_on(chapter):
    """Vastaamatta jäänyt pyyntö katkaistaan 6 sekunnissa, kuten mdBookissa.
    Tämä testi siis kestää ne 6 sekuntia."""
    chapter.answer(hang=True)
    assert chapter.run(SINGLE) == "Ohjelma ei vastannut 6 sekunnissa."


def test_no_console_errors(chapter):
    chapter.answer(output="rivi\n")
    chapter.run(SINGLE)
    assert chapter.errors == []
