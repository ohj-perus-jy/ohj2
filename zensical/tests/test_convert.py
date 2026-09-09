"""convert.py:n muunnokset yksin: ei käännöstä, ei selainta.

Nämä ovat testeistä nopeimmat ja tiheimmät. Ne vastaavat kysymykseen
"tekeekö skripti sen mitä README.md väittää" ilman että mitään käännetään,
ja siksi jokainen väite on kirjattu samoin sanoin kuin README:n perustelu.

Lähdepuuna on tests/book/src, joka on tarkoituksella pieni mutta sisältää
yhden esimerkin jokaisesta muunnoksesta.
"""

import zlib

import pytest

import convert


@pytest.fixture
def book_src(monkeypatch):
    """convert.SRC osoittamaan koekirjaan.

    build_nav lukee lähdepuun moduulivakiosta, joten testi vaihtaa sen.
    Skriptiin itseensä ei tarvita testejä varten riviäkään.
    """
    src = convert.ROOT / "tests" / "book" / "src"
    monkeypatch.setattr(convert, "SRC", src)
    return src


# --- Sisällytykset (README kohta 1) -----------------------------------------

@pytest.mark.parametrize("selector, expected", [
    ("", "a\nb\nc"),
    ("2", "b"),
    ("2:3", "b\nc"),
    ("2:", "b\nc"),
    (":2", "a\nb"),
    ("ANCHOR", None),
    ("1:2:3", None),
    (":", None),
])
def test_take_lines(selector, expected):
    """mdBookin rivivalinnat 1-pohjaisina ja molemmat päät mukaan lukien;
    ankkuri ja tunnistamaton muoto palautuvat None:na."""
    assert convert.take_lines("a\nb\nc\n", selector) == expected


def test_convert_includes_keeps_the_code_fence_tight(tmp_path):
    """Koko tiedosto paikalleen ilman loppurivinvaihtoa: koodiaidan sisään ei
    jää tyhjää riviä ennen sulkevaa aitaa, kuten ei mdBookissakaan."""
    (tmp_path / "Main.java").write_text("class Main {\n}\n", encoding="utf-8")
    page = tmp_path / "luku.md"
    converted, includes = convert.convert_includes(
        "```java\n{{#include ./Main.java}}\n```\n", page)
    assert includes == 1
    assert converted == "```java\nclass Main {\n}\n```\n"


def test_convert_includes_single_line_fits_in_a_table_cell(tmp_path):
    """Yhden rivin valinta pysyy yhdellä rivillä: takarajataulukon solu."""
    (tmp_path / "takarajat.md").write_text("eka\ntoka\n", encoding="utf-8")
    page = tmp_path / "luku.md"
    converted, includes = convert.convert_includes(
        "| 2   |{{#include ./takarajat.md:2}}|\n", page)
    assert (converted, includes) == ("| 2   |toka|\n", 1)


def test_convert_includes_reads_the_file_beside_the_page(tmp_path):
    """Polku on suhteessa sivuun, ei työhakemistoon."""
    (tmp_path / "exercises").mkdir()
    (tmp_path / "exercises" / "handout.md").write_text("Tee tämä.", encoding="utf-8")
    (tmp_path / "osa1").mkdir()
    page = tmp_path / "osa1" / "05-tehtavat.md"
    converted, includes = convert.convert_includes(
        "<handout>\n\n{{#include ../exercises/handout.md}}\n\n</handout>\n", page)
    assert includes == 1
    assert "Tee tämä." in converted


@pytest.mark.parametrize("spec, warning", [
    ("./puuttuu.md", "sisällytettävä tiedosto puuttuu"),
    ("./on.md:ANCHOR", "tuntematon rivivalinta"),
])
def test_convert_includes_warns_instead_of_dropping_content(tmp_path, capsys,
                                                            spec, warning):
    """Hiljaa katoava sisällytys näyttäisi sivulla samalta kuin tyhjä
    tehtävänanto, joten makro jää näkyviin ja siitä varoitetaan."""
    (tmp_path / "on.md").write_text("sisältö\n", encoding="utf-8")
    text = f"{{{{#include {spec}}}}}\n"
    converted, includes = convert.convert_includes(text, tmp_path / "luku.md")
    assert (converted, includes) == (text, 0)
    assert warning in capsys.readouterr().err


# --- Aidan attribuuttilista (README kohta 4) ---------------------------------

@pytest.mark.parametrize("info, expected", [
    ("java,ignore", "{ .java .ignore }"),
    ("java, ignore ", "{ .java .ignore }"),
    ("java,ignore,noplayground", "{ .java .ignore .noplayground }"),
    ("java", "java"),
    ("", ""),
])
def test_fence_info(info, expected):
    """mdBookin määreet attr_listin luokiksi, kieli ennallaan."""
    assert convert.fence_info(info) == expected


def test_convert_fences_rewrites_opening_fence():
    text = "```java,ignore\nkoodi\n```\n"
    converted, fences = convert.convert_fences(text)
    assert converted == "```{ .java .ignore }\nkoodi\n```\n"
    assert fences == 1


def test_convert_fences_keeps_indent_and_quote():
    """Sisennetty ja lainauslohkon sisällä oleva aita: rivin alku ennallaan."""
    converted, fences = convert.convert_fences("> ```java,ignore\n> x\n> ```\n")
    assert converted.startswith("> ```{ .java .ignore }")
    assert fences == 1


def test_convert_fences_ignores_fences_inside_code():
    """Aidat käydään pareittain, jottei koodilohkon sisällä oleva
    aidannäköinen rivi muutu vahingossa."""
    text = "````text\n```java,ignore\n````\n"
    converted, fences = convert.convert_fences(text)
    assert converted == text
    assert fences == 0


# --- Monitiedostolohkot (README kohta 5) -------------------------------------

def test_split_files_tolerates_sloppy_markers():
    """Merkinnät ovat aineistossa epätarkkoja ja mdBook sietää sen:
    "//FILE:" ilman välilyöntiä, nimen perässä välilyöntejä, FILE_END
    vapaaehtoinen ja ylimääräinen FILE_END ohitetaan."""
    body = [
        "//FILE: Main.java",
        "public class Main { }",
        "// FILE_END",
        "// FILE: Valo.java  ",
        "public class Valo { }",
    ]
    assert convert.split_files(body) == [
        ("Main.java", ["public class Main { }"]),
        ("Valo.java", ["public class Valo { }"]),
    ]


def test_split_files_without_markers():
    assert convert.split_files(["tavallista koodia"]) == []


def test_convert_files_makes_one_tab_per_file():
    text = "```java,ignore\n// FILE: A.java\na\n// FILE: B.java\nb\n```\n"
    converted, blocks, files = convert.convert_files(text)
    assert (blocks, files) == (1, 2)
    # Jokainen tiedosto omaksi välilehdekseen ja omaksi koodiaidakseen,
    # alkuperäisen aidan määreineen.
    assert converted == (
        '=== "A.java"\n'
        "\n"
        "    ```{ .java .ignore }\n"
        "    a\n"
        "    ```\n"
        "\n"
        '=== "B.java"\n'
        "\n"
        "    ```{ .java .ignore }\n"
        "    b\n"
        "    ```\n"
        "\n"
    )


def test_convert_files_leaves_ordinary_block_alone():
    text = "```java\nkoodi\n```\n"
    assert convert.convert_files(text) == (text, 0, 0)


def test_convert_files_warns_instead_of_dropping_code(capsys):
    """Koodi ennen ensimmäistä merkintää: lohko jätetään ennalleen ja siitä
    varoitetaan, koska muunnos pudottaisi rivit hiljaisesti pois."""
    text = "```java\nirrallinen\n// FILE: A.java\na\n```\n"
    converted, blocks, files = convert.convert_files(text)
    assert (converted, blocks, files) == (text, 0, 0)
    assert "koodia ennen ensimmäistä" in capsys.readouterr().err


# --- Alertit (README kohta 7) -----------------------------------------------

@pytest.mark.parametrize("label, expected", [
    ("Osaamistavoitteet", '!!! abstract "Osaamistavoitteet"'),
    ("HUOMAUTUS", '!!! note "Huomautus"'),
    ("VINKKI", '!!! tip "Vinkki"'),
    ("Vinkki", '!!! tip "Vinkki"'),
    ("TÄRKEÄÄ", '!!! tip "Tärkeää"'),
    ("VAROITUS", '!!! warning "Varoitus"'),
    ("todo", '!!! info "Todo"'),
    ("WIP", '!!! danger "WIP"'),
])
def test_convert_alerts_writes_the_title_out(label, expected):
    """Tunnus -> tyyppi ja otsikko, kirjainkoosta riippumatta. Otsikko
    kirjoitetaan aina näkyviin, koska muuten Material näyttäisi tyypin oman
    englanninkielisen nimen ("Tip")."""
    converted, alerts, unknown = convert.convert_alerts(f"> [!{label}]\n> teksti\n")
    assert (alerts, unknown) == (1, set())
    assert converted.startswith(expected)


def test_convert_alerts_keeps_an_unknown_label_as_the_title():
    """Tuntematon tunnus ei katoa: se jää otsikoksi sellaisenaan ja
    palautuu kutsujalle, joka kertoo siitä ajon lopuksi."""
    converted, alerts, unknown = convert.convert_alerts(
        "> [!Tärkeää — invariantti]\n> teksti\n")
    assert (alerts, unknown) == (1, {"Tärkeää — invariantti"})
    assert converted.startswith('!!! note "Tärkeää — invariantti"')


def test_convert_alerts_keeps_the_block_indentation():
    """Lainauksen etuliitteestä syödään yksi välilyönti, jolloin lohkon omat
    sisennykset säilyvät: koodiaita pysyy aitana ja luetelma luetelmana."""
    text = ("> [!HUOMAUTUS]\n>\n> kappale\n>\n> ```java\n> int x = 1;\n> ```\n"
            ">\n> - eka\n>   - toka\n")
    converted, _, _ = convert.convert_alerts(text)
    assert converted == ('!!! note "Huomautus"\n\n'
                         "    kappale\n\n"
                         "    ```java\n    int x = 1;\n    ```\n\n"
                         "    - eka\n      - toka\n")


def test_convert_alerts_leaves_an_ordinary_quote_alone():
    """Lainaus ilman tunnusriviä on lainaus, ei alertti."""
    text = "> Tavallinen sitaatti\n> jatkuu\n"
    assert convert.convert_alerts(text) == (text, 0, set())


def test_convert_alerts_keeps_paragraphs_apart():
    """Tyhjä rivi eteen jos sitä ei ollut, muttei toista perään: lainauksen
    päättävä tyhjä rivi tulee mukaan sellaisenaan."""
    text = "edellinen\n> [!VINKKI]\n> vinkki\n\nseuraava\n"
    converted, _, _ = convert.convert_alerts(text)
    assert converted == 'edellinen\n\n!!! tip "Vinkki"\n\n    vinkki\n\nseuraava\n'


# --- Avattavat osiot (README kohta 8) ----------------------------------------

def test_convert_details_marks_the_block_for_markdown():
    """Ilman markdown-attribuuttia Python-Markdown ei käsittele lohkon
    sisältöä lainkaan, vaan numeroitu lista ja linkit jäävät lähdemuotoonsa."""
    text = "<details><summary>Vinkki</summary>\n\n1. eka\n2. toka\n\n</details>\n"
    converted, tags, summaries = convert.convert_details(text)
    assert converted.startswith('<details markdown="1"><summary>Vinkki</summary>')
    assert (tags, summaries) == (1, 0)


def test_convert_details_keeps_existing_attributes():
    """Aineistossa on myös <details closed>. Attribuutti ei ole HTML:ää eikä
    tee mitään, mutta se jätetään paikalleen — lopputulos on sama."""
    converted, tags, summaries = convert.convert_details("<details closed>\n")
    assert converted == '<details closed markdown="1">\n'
    assert (tags, summaries) == (1, 0)


def test_convert_details_is_repeatable():
    """convert.py ajetaan uudelleen aina kun lähde muuttuu: jo käännetty tagi
    ei saa saada toista attribuuttia."""
    text = '<details markdown="1">\n'
    assert convert.convert_details(text) == (text, 0, 0)


def test_convert_details_ignores_details_inside_code():
    """Aidat käydään pareittain kuten convert_fencesissä, jottei koodilohkossa
    näytetty HTML-esimerkki muuttuisi."""
    text = "```html\n<details>\n```\n"
    assert convert.convert_details(text) == (text, 0, 0)


def test_convert_details_marks_a_summary_that_is_its_own_block():
    """Harjoitustyön aihelohkoissa yhteenveto on otsikko ja kappale. Ilman
    attribuuttia ne jäävät avauspalkkiin muodossa "### Kulujen seuranta ...".

    Arvo on "block" eikä "1": md_in_html jäsentäisi <summary>-tagin sisällön
    muuten vain rivinsisäisesti, ks. SUMMARY_RE."""
    text = ("<details><summary>\n\n### Kulujen seuranta\n\nKuvaus.\n\n"
            "</summary>\n\nSisältö.\n\n</details>\n")
    converted, tags, summaries = convert.convert_details(text)
    assert converted.startswith(
        '<details markdown="1"><summary markdown="block">')
    assert (tags, summaries) == (1, 1)


def test_convert_details_leaves_a_one_line_summary_alone():
    """Yhden rivin yhteenvedossa ei ole Markdownia, ja markdown="block"
    käärisi tekstin <p>:hen eli muuttaisi avauspalkin välistyksen."""
    converted, _, summaries = convert.convert_details(
        "<details><summary>Vinkki</summary>\n")
    assert "<summary>" in converted
    assert summaries == 0


def test_convert_details_leaves_a_wrapped_summary_alone():
    """Kahdessa yhteenvedossa teksti jatkuu seuraavalle riville ilman tyhjää
    riviä. Sama raja kuin kirjassa: ilman tyhjää riviä pulldown-cmark ei
    jäsennä yhteenvetoa Markdownina, joten sitä ei tarvitse merkitä."""
    text = "<details><summary>Valinnaista lisätietoa:\nJava ei voi</summary>\n"
    converted, _, summaries = convert.convert_details(text)
    assert "<summary>Valinnaista" in converted
    assert summaries == 0


def test_drop_breaks_removes_the_spacer_between_two_blocks():
    """Väljyydeksi kirjoitettu <br /> jää omaksi kappaleekseen (<p><br /></p>)
    ja kolminkertaistaa lohkojen välin, ks. BREAK_LINE_RE. Tyhjiä rivejä jää
    yksi, ei kahta."""
    text = "</details>\n\n<br />\n\n<details>\n"
    assert convert.drop_breaks(text) == ("</details>\n\n<details>\n", 1)


def test_drop_breaks_accepts_every_spelling():
    """Aineistossa muoto on <br />, mutta HTML sallii myös nämä."""
    for tag in ("<br>", "<br/>", "<br />", "<br />  "):
        text = f"eka\n\n{tag}\n\ntoka\n"
        assert convert.drop_breaks(text) == ("eka\n\ntoka\n", 1)


def test_drop_breaks_keeps_a_line_break_inside_a_paragraph():
    """Rivin lopussa <br /> on oikea rivinvaihto eikä väljyyttä."""
    text = "rivi<br />\nseuraava rivi\n"
    assert convert.drop_breaks(text) == (text, 0)


def test_drop_breaks_keeps_an_indented_tag():
    """Sisennetty rivi voisi olla sisennettyä koodia, ks. BREAK_LINE_RE."""
    text = "eka\n\n    <br />\n\ntoka\n"
    assert convert.drop_breaks(text) == (text, 0)


def test_drop_breaks_ignores_breaks_inside_code():
    """Aidat käydään pareittain kuten convert_detailsissä."""
    text = "```html\n\n<br />\n\n```\n"
    assert convert.drop_breaks(text) == (text, 0)


def test_drop_breaks_is_repeatable():
    """convert.py ajetaan uudelleen aina kun lähde muuttuu."""
    text = "</details>\n\n<details>\n"
    assert convert.drop_breaks(text) == (text, 0)


# --- Luokkakaaviot (README kohta 15) -----------------------------------------

def test_plantuml_encode_round_trips():
    """Osoitepala on raakaa deflatea PlantUMLin omalla base64-aakkostolla.

    Palvelimen vastauksesta ei voi tehdä testiä (se vaatisi verkon), eikä
    valmista vertailumerkkijonoa voi kirjoittaa tähän: zlib saa tuottaa saman
    tekstin monella eri tavalla pakattuna. Sen sijaan puretaan takaisin —
    silloin testi kattaa juuri sen mikä voi mennä rikki: aakkoston ja
    kehyksettömän deflaten."""
    source = "@startuml\nclass Kissa\n@enduml"
    encoded = convert.plantuml_encode(source)
    reverse = {ch: i for i, ch in enumerate(convert.PLANTUML_ALPHABET)}
    bits = "".join(f"{reverse[ch]:06b}" for ch in encoded)
    data = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) // 8 * 8, 8))
    assert zlib.decompress(data, -15) == source.encode("utf-8")


def test_convert_plantuml_replaces_the_fence_with_an_image(monkeypatch):
    """Ilman muunnosta aidan sisältö on sivulla koodilohkona: kirjassa on
    kaavio, tässä 20 riviä @startuml-lähdettä."""
    monkeypatch.setattr(convert, "plantuml_svg", lambda source: "abc.svg")
    text = "ennen\n\n```plantuml\n@startuml\nclass Kissa\n@enduml\n```\n\njälkeen\n"
    converted, diagrams, used = convert.convert_plantuml(
        text, convert.DOCS / "harjoitustyo.md")
    assert converted == ("ennen\n\n![UML-luokkakaavio]"
                         "(assets/plantuml/abc.svg){ .uml }\n\njälkeen\n")
    assert (diagrams, used) == (1, {"abc.svg"})


def test_convert_plantuml_path_follows_the_page(monkeypatch):
    """Zensical ratkaisee suhteellisen osoitteen lähdetiedoston mukaan, joten
    alahakemistossa oleva sivu tarvitsee yhden "../":n."""
    monkeypatch.setattr(convert, "plantuml_svg", lambda source: "abc.svg")
    converted, _, _ = convert.convert_plantuml(
        "```plantuml\n@startuml\n@enduml\n```\n", convert.DOCS / "osa3/01-perinta.md")
    assert "(../assets/plantuml/abc.svg)" in converted


def test_convert_plantuml_keeps_the_fence_when_the_server_is_silent(monkeypatch):
    """Kaaviot ovat versionhallinnassa, joten käännös ei tarvitse verkkoa. Jos
    kaavio on uusi eikä palvelin vastaa, sivu palaa siihen mitä se oli ennen
    tätä kohtaa — käännös ei kaadu."""
    monkeypatch.setattr(convert, "plantuml_svg", lambda source: None)
    text = "```plantuml\n@startuml\n@enduml\n```\n"
    assert convert.convert_plantuml(text, convert.DOCS / "sivu.md") == (text, 0, set())


def test_convert_plantuml_leaves_an_unclosed_fence_alone(monkeypatch):
    """Sulkematon aita on aineiston virhe, ei syy niellä loppusivua."""
    monkeypatch.setattr(convert, "plantuml_svg", lambda source: "abc.svg")
    text = "```plantuml\n@startuml\n"
    assert convert.convert_plantuml(text, convert.DOCS / "sivu.md") == (text, 0, set())


def test_convert_svgbob_wraps_the_drawing_in_a_div(monkeypatch):
    """Paljas <svg> ei ole Python-Markdownille lohkotason HTML:ää: se päätyisi
    kappaleen sisään ja rivinvaihdot <br />-tageiksi. Kääre on divi, joka on."""
    monkeypatch.setattr(convert, "svgbob_svg",
                        lambda art: '<svg class="svgbob">\n<text>a</text>\n</svg>')
    converted, drawings, used = convert.convert_svgbob(
        "ennen\n\n```bob\n+---+\n```\n\njälkeen\n")
    assert converted == ('ennen\n\n<div class="svgbob">\n<svg class="svgbob">\n'
                         "<text>a</text>\n</svg>\n</div>\n\njälkeen\n")
    assert (drawings, len(used)) == (1, 1)


def test_convert_svgbob_drops_blank_lines(monkeypatch):
    """svgbobin tyylilohkossa on tyhjiä rivejä, ja tyhjä rivi lopettaisi raa'an
    HTML-lohkon: loppu kaaviosta päätyisi sivulle tekstinä."""
    monkeypatch.setattr(convert, "svgbob_svg",
                        lambda art: "<svg>\n\n<text>a</text>\n\n</svg>")
    converted, _, _ = convert.convert_svgbob("```bob\n+---+\n```\n")
    assert "\n\n" not in converted.strip()


def test_convert_svgbob_gives_every_diagram_its_own_ids(monkeypatch):
    """svgbob kirjoittaa jokaiseen kaavioon samat nuolenkärkimäärittelyt, joten
    saman sivun kaavioilla olisi samat tunnisteet ja url(#arrow) osoittaisi aina
    ensimmäiseen. Sivulla osa6/02 kaavioita on neljä."""
    monkeypatch.setattr(
        convert, "svgbob_svg",
        lambda art: '<svg><marker id="arrow"/><line marker-end="url(#arrow)"/></svg>')
    converted, _, _ = convert.convert_svgbob("```bob\na\n```\n\n```bob\nb\n```\n")
    assert 'id="bob1-arrow"' in converted and 'url(#bob1-arrow)' in converted
    assert 'id="bob2-arrow"' in converted and 'url(#bob2-arrow)' in converted


def test_convert_svgbob_keeps_the_fence_without_the_tool(monkeypatch):
    """Kaaviot ovat välimuistissa versionhallinnassa, joten svgbobia tarvitaan
    vain uuteen tai muuttuneeseen piirrokseen. Jos sitä ei ole, aita jää
    ennalleen eikä käännös kaadu."""
    monkeypatch.setattr(convert, "svgbob_svg", lambda art: None)
    text = "```bob\n+---+\n```\n"
    assert convert.convert_svgbob(text) == (text, 0, set())


# --- Vaatimusdivit (README kohta 25) -----------------------------------------

def test_convert_divs_marks_the_block_for_markdown():
    """Ilman attribuuttia divin sisältö menee sivulle lähdemuodossaan. Myös
    uloin divi tarvitsee sen: md_in_html ei etene sisempiin lohkoihin, jos
    uloin on käsittelemätöntä HTML:ää."""
    text = '<div class="ht-reqs">\n\n<div class="req">\n\n### Vaatimus 1\n\n'
    converted, tags = convert.convert_divs(text)
    assert converted.startswith('<div class="ht-reqs" markdown="1">')
    assert '<div class="req" markdown="1">' in converted
    assert tags == 2


def test_convert_divs_leaves_a_div_inside_a_paragraph_alone():
    """Python-Markdown tunnistaa lohkotason HTML:n vain omana kappaleenaan,
    joten kesken kappaleen olevalle diville attribuutti ei tekisi mitään."""
    text = "teksti <div>ei lohko</div>\n"
    assert convert.convert_divs(text) == (text, 0)


def test_convert_divs_is_repeatable():
    """Kuten convert_details: jo käännetty tagi ei saa saada toista
    attribuuttia."""
    text = '<div class="req" markdown="1">\n'
    assert convert.convert_divs(text) == (text, 0)


def test_convert_divs_ignores_divs_inside_code():
    """Aidat käydään pareittain kuten convert_detailsissä."""
    text = '```html\n<div class="req">\n```\n'
    assert convert.convert_divs(text) == (text, 0)


# --- Tehtäväkortit (README kohta 6) -----------------------------------------

TASK = """\
<task>
  <task-title num="2.1">Kello<points>1 p.</points></task-title>
  <handout>

Tee luokka `Kello`.

  </handout>
  <task-link><a href="https://tim.jyu.fi/x">Tee tehtävä TIMissä</a></task-link>
</task>
"""


def test_convert_tasks_names_every_part():
    """Kortista tulee divit, joilla on luokka: tyyli (assets/css/tasks.css)
    osoittaa niihin, eikä yhtään tuntematonta tagia jää sivulle."""
    converted, cards = convert.convert_tasks(TASK)
    assert cards == 1
    assert '<div class="task" markdown="1">' in converted
    assert ('<div class="task-head"><span class="task-num">2.1</span>'
            '<span class="task-name">Kello</span>'
            '<span class="task-points">1 p.</span></div>') in converted
    assert '<div class="task-handout" markdown="1">' in converted
    assert ('<div class="task-link">'
            '<a href="https://tim.jyu.fi/x">Tee tehtävä TIMissä</a></div>') in converted
    assert "<task" not in converted and "<points>" not in converted


def test_convert_tasks_marks_only_the_handout_for_markdown():
    """Tehtävänanto on Markdownia ja tarvitsee attribuutin, tunnusrivi ja
    TIM-linkki ovat tekstiä ja HTML:ää eivätkä tarvitse."""
    converted, _ = convert.convert_tasks(TASK)
    assert converted.count('markdown="1"') == 2


def test_convert_tasks_puts_the_bonus_badge_inside_the_name():
    """<i class="bi bi-stars"> jää nimen sisään, kuten lähteessäkin: liuska
    seuraa nimen viimeistä sanaa myös silloin kun nimi rivittyy."""
    text = ('<task-title num="1.7"><i class="bi bi-stars"></i>'
            "Numerolaskuri<points>1 p.</points></task-title>\n")
    converted, _ = convert.convert_tasks(text)
    assert ('<span class="task-name">Numerolaskuri '
            '<span class="task-bonus">Bonus</span></span>') in converted
    assert "bi-stars" not in converted


def test_convert_tasks_lifts_the_tags_out_of_the_indentation():
    """Python-Markdown tunnistaa lohkotason HTML:n vain omana kappaleenaan,
    ja neljällä välilyönnillä sisennetty rivi olisi koodilohko. Sisennys on
    lähteessä pelkkää muotoilua — aineistossa sitä on neljää eri syvyyttä."""
    converted, _ = convert.convert_tasks("    <handout>\nteksti\n")
    assert converted.startswith('<div class="task-handout" markdown="1">\n\n')


def test_convert_tasks_does_not_pile_up_blank_lines():
    """Tagin perässä on lähteessä usein jo tyhjä rivi; sitä ei oteta toiseen
    kertaan, jotta docs/ pysyy luettavana."""
    converted, _ = convert.convert_tasks("<task>\n\nteksti\n")
    assert converted == '<div class="task" markdown="1">\n\nteksti\n'


def test_convert_tasks_is_repeatable():
    """convert.py ajetaan uudelleen aina kun lähde muuttuu: valmiissa
    tekstissä ei ole enää tagia, johon muunnos osuisi."""
    converted, _ = convert.convert_tasks(TASK)
    assert convert.convert_tasks(converted) == (converted, 0)


def test_convert_tasks_ignores_tasks_inside_code():
    """Aidat käydään pareittain kuten convert_fencesissä, jottei koodilohkossa
    näytetty merkkausesimerkki muuttuisi."""
    text = "```markdown\n<task>\n```\n"
    assert convert.convert_tasks(text) == (text, 0)


# --- Käyttöjärjestelmävälilehdet (README kohta 23) ---------------------------

def test_convert_tabs_drops_placeholder():
    """#tab/default jää pois: Zensicalissa yksi välilehti on aina valittuna."""
    text = ("### [Windows](#tab/win)\n\nW\n\n***\n\n"
            "### [Valitse](#tab/default)\n\nvalitse\n\n***\n")
    converted, sets, placeholders, labels = convert.convert_tabs(text)
    assert (sets, placeholders) == (1, 1)
    assert labels == {"Windows"}
    assert "valitse" not in converted
    assert '=== "Windows"' in converted


def test_convert_tabs_first_label_wins_per_id():
    """Saman tunnuksen välilehdet saavat saman otsikon: Material yhdistää
    joukot otsikkotekstistä, mdBook yhdisti tunnuksesta."""
    text = ("### [GitLab (JY)](#tab/gitlab)\n\na\n\n***\n\n"
            "#### [GitLab (JYU)](#tab/gitlab)\n\nb\n\n***\n")
    converted, _, _, labels = convert.convert_tabs(text)
    assert labels == {"GitLab (JY)"}
    assert converted.count('=== "GitLab (JY)"') == 2


def test_convert_tabs_keeps_paragraphs_apart():
    """Tyhjä rivi joukon eteen myös silloin kun koko joukko jäi pois."""
    text = ("edellinen\n### [Valitse](#tab/default)\n\nx\n\n***\nseuraava\n")
    converted, sets, placeholders, _ = convert.convert_tabs(text)
    assert (sets, placeholders) == (0, 1)
    assert converted == "edellinen\n\nseuraava\n"


# --- Navigaatio (README kohdat 10, 11 ja Tenttiohjeet) -----------------------

def test_build_nav(book_src):
    """Numeron saavat vain listakohdat, juoksevasti myös ---erottimien yli;
    osan etusivu toistuu ensimmäisenä lapsena numeroineen; NEST_UNDER siirtää
    Tenttiohjeet Tentin alle; ulkoinen linkki tulee mukaan sellaisenaan."""
    assert convert.build_nav() == (
        'nav:\n'
        '  - "Aloitus": index.md\n'
        '  - "Tentti":\n'
        '    - "Tentti": tentti/index.md\n'
        '    - "Tenttiohjeet": tentti/tenttiohjeet.md\n'
        '  - "1 Perusteet":\n'
        '    - "1 Perusteet": osa1/index.md\n'
        '    - "1.1 Hei, maailma": osa1/01-hei.md\n'
        '    - "1.2 Tehtävät": osa1/02-tehtavat.md\n'
        '  - "2 Työkalut":\n'
        '    - "2 Työkalut": osa2/index.md\n'
        '    - "2.1 Tehtävät": osa2/01-tehtavat.md\n'
        '  - "Eteneminen": https://example.invalid/tim\n'
    )


def test_nest_moves():
    """Yläsivu omaan hakemistoonsa index.md:ksi, alasivu sen viereen."""
    assert convert.nest_moves() == {
        "tentti.md": "tentti/index.md",
        "tenttiohjeet.md": "tentti/tenttiohjeet.md",
    }


# --- Tulostussivun runko (README kohta 24) -----------------------------------

def test_build_print_page_lists_every_chapter(book_src):
    """Luettelo kaikista luvuista kirjan järjestyksessä. Ulkoinen linkki ei
    ole luku, joten se jää pois."""
    page = convert.build_print_page(convert.build_nav())
    assert page.count("\n- [") == 8
    assert page.index("- [Aloitus](index.md)") < page.index("- [1 Perusteet]")
    assert "example.invalid" not in page


def test_build_print_page_is_excluded_from_search(book_src):
    """Sivu ei mene hakuindeksiin: se on koko kirja toiseen kertaan."""
    page = convert.build_print_page(convert.build_nav())
    assert page.startswith("---\ntitle: Koko kirja\nsearch:\n  exclude: true\n")


def test_build_extra_maps_moved_pages_back_to_src():
    """Muokkauslinkki osoittaa ../src:ään, joten siirretyt sivut käännetään
    takaisin ja generoidulta sivulta linkki jätetään pois."""
    extra = convert.build_extra({"Windows"})
    assert '"tentti/index.md": "tentti.md"' in extra
    assert '"tulosta.md": ""' in extra
    assert '    - "Windows"' in extra
