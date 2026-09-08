"""convert.py:n muunnokset yksin: ei käännöstä, ei selainta.

Nämä ovat testeistä nopeimmat ja tiheimmät. Ne vastaavat kysymykseen
"tekeekö skripti sen mitä README.md väittää" ilman että mitään käännetään,
ja siksi jokainen väite on kirjattu samoin sanoin kuin README:n perustelu.

Lähdepuuna on tests/book/src, joka on tarkoituksella pieni mutta sisältää
yhden esimerkin jokaisesta muunnoksesta.
"""

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
