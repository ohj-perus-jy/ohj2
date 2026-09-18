"""Testaa tietosi -visa koekirjalla (assets/js/visa.js).

Koesivu osa1/visa.md on SUMMARY.md:n ulkopuolella: yksi väittämä (tarua) ja
yksi monivalinta (b), jonka kysymyksessä on koodilohko. convert.py kirjoittaa
kysymyksen listaksi ja perustelun <details>-lohkoksi (test_convert.py); napit,
paljastus ja muisti syntyvät vasta selaimessa. Jokainen testi saa oman
selainkontekstin, koska vastaukset jäävät localStorageen.
"""

import json

import pytest

QUESTION = ".jyu-visa-q"
BUTTON = ".jyu-visa-nappi"
CLEAR = ".jyu-visa-nollaus button"

# Kysymyksen vaihtoehdot: [arvo, valittu, oikeaksi merkitty].
MARKS = """question => [...question.querySelectorAll('.jyu-visa-vaihtoehdot > li')].map(option => [
  option.dataset.arvo,
  option.classList.contains('jyu-visa-valittu'),
  option.classList.contains('jyu-visa-oikea')])"""

STORED = "JSON.parse(localStorage.getItem('jyu-visa') || '{}')"


@pytest.fixture(scope="session")
def visa_url(book, serve) -> str:
    return f"{serve(book.site)}/osa1/visa/"


@pytest.fixture
def context(browser):
    opened = browser.new_context()
    yield opened
    opened.close()


@pytest.fixture
def page(context, visa_url):
    opened = context.new_page()
    errors: list[str] = []
    opened.on("pageerror", lambda error: errors.append(str(error)))
    opened.goto(visa_url, wait_until="load")
    yield opened
    assert errors == []


def test_options_are_buttons_and_the_explanation_waits(page):
    """Vastausta ei voi kurkata: perustelu tulee näkyviin vasta valinnasta."""
    assert page.locator(f"{QUESTION} {BUTTON}").all_inner_texts() == [
        "Totta", "Tarua",
        "Hei ja sen perään List<int>, koska rivi on niin pitkä, että se jatkuu toiselle riville",
        "Moi", "Ei mitään"]
    assert page.locator(f"{QUESTION} > details").count() == 2
    assert not page.locator(f"{QUESTION} > details").first.is_visible()
    assert not page.locator(CLEAR).is_visible()


def test_an_option_stays_one_piece_of_text(page):
    """Nappi on flex-säiliö; ilman käärettä jokainen koodinpätkä olisi oma
    kohteensa ja pitkä vaihtoehto hajoaisi palstoiksi."""
    assert page.locator(f"{QUESTION} {BUTTON}").nth(2).evaluate(
        "button => [...button.children].map(child => child.tagName)") == ["SPAN"]


def test_the_question_keeps_its_code_block(page):
    assert page.locator(f"{QUESTION} >> nth=1").locator("pre code").inner_text().strip() == (
        'Console.WriteLine("Moi");')


def test_a_right_answer_shows_the_explanation(page):
    question = page.locator(QUESTION).first
    question.locator(BUTTON, has_text="Tarua").click()
    assert question.evaluate(MARKS) == [["totta", False, False], ["tarua", True, True]]
    details = question.locator("details")
    assert details.get_attribute("data-tulos") == "oikein"
    assert details.locator("summary").inner_text() == "Oikein!"
    assert details.locator("p").inner_text() == "Tarua. Käännösvirhe estää kääntämisen."
    assert details.locator("p").is_visible()


def test_a_wrong_answer_shows_the_right_one_too(page):
    question = page.locator(QUESTION).nth(1)
    question.locator(BUTTON).nth(2).click()
    assert question.evaluate(MARKS) == [
        ["a", False, False], ["b", False, True], ["c", True, False]]
    assert question.locator("details").get_attribute("data-tulos") == "vaarin"
    assert question.locator("details summary").inner_text() == "Väärin"


def test_the_first_answer_stays(page):
    """Toinen painallus ei vaihda vastausta: oikea on jo näkyvissä."""
    question = page.locator(QUESTION).nth(1)
    question.locator(BUTTON).nth(2).click()
    question.locator(BUTTON).nth(1).click(force=True)
    assert question.get_attribute("data-vastattu") == "c"
    assert list(page.evaluate(STORED).values()) == ["c"]


def test_answers_are_remembered_by_the_question(context, page, visa_url):
    """Avain on kysymyksen tekstin tiiviste (data-id), ei sen järjestysnumero."""
    page.locator(QUESTION).first.locator(BUTTON, has_text="Totta").click()
    identifier = page.locator(QUESTION).first.get_attribute("data-id")
    assert page.evaluate(STORED) == {identifier: "totta"}

    again = context.new_page()
    again.goto(visa_url, wait_until="load")
    assert again.locator(QUESTION).first.evaluate(MARKS) == [
        ["totta", True, False], ["tarua", False, True]]
    assert again.locator(QUESTION).first.locator("details summary").inner_text() == "Väärin"
    assert again.locator(QUESTION).nth(1).get_attribute("data-vastattu") is None


def test_clearing_forgets_this_quiz_only(context, page, visa_url):
    """Muiden sivujen vastaukset ovat samassa avaimessa ja jäävät talteen."""
    page.evaluate("localStorage.setItem('jyu-visa', JSON.stringify({muu: 'a'}))")
    page.locator(QUESTION).first.locator(BUTTON, has_text="Tarua").click()
    page.locator(CLEAR).click()
    assert page.evaluate(STORED) == {"muu": "a"}
    assert page.locator(QUESTION).first.evaluate(MARKS) == [
        ["totta", False, False], ["tarua", False, False]]
    assert not page.locator(f"{QUESTION} > details").first.is_visible()
    assert page.locator(f"{QUESTION} > details summary").first.text_content() == "Näytä vastaus"
    assert not page.locator(CLEAR).is_visible()


@pytest.mark.parametrize("stored", ["ei jsonia", "[1]", "5", json.dumps({"x": "zzz"})])
def test_broken_storage_is_an_empty_one(context, visa_url, stored):
    context.add_init_script(f"localStorage.setItem('jyu-visa', {json.dumps(stored)})")
    page = context.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(visa_url, wait_until="load")
    page.locator(QUESTION).first.locator(BUTTON, has_text="Tarua").click()
    assert page.locator(QUESTION).first.get_attribute("data-vastattu") == "tarua"
    assert errors == []


def test_without_the_script_the_quiz_is_a_list_and_an_openable_answer(browser, visa_url):
    """Sama tila kuin tulostussivulla, jonne napit eivät tule."""
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(visa_url, wait_until="load")
    question = page.locator(QUESTION).nth(1)
    assert question.locator("ol > li").all_inner_texts()[1:] == ["Moi", "Ei mitään"]
    assert question.locator("ol").evaluate(
        "list => getComputedStyle(list).listStyleType") == "lower-alpha"
    assert question.locator("details summary").inner_text() == "Näytä vastaus"
    assert question.locator("details summary").is_visible()
    context.close()
