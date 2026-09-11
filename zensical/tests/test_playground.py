"""Java-ohjelmien ajonapit koekirjalla (README.md kohta 3).

Nappi lähettää koodin JYU:n suorituspalvelimelle, joten testit vastaavat
pyyntöön itse (page.route): mitataan mitä selain lähettää ja näyttää, ei
palvelimen tilaa. Koekirjassa on yksi esimerkki kustakin lohkolajista.
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
    """Pyyntö on kenttä kentältä sama kuin mdBookissa."""
    chapter.answer(output="Hei, maailma!\n")
    assert chapter.run(SINGLE) == "Hei, maailma!"
    assert chapter.requests == [{
        "language": "java",
        "code": 'void main() {\nIO.println("Hei, maailma!");\n}\n',
        "multifile": False,
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
