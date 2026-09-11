"""Kun materiaalia muutetaan, muuttuuko tuloste mukana?

Tulostussivu kootaan kolmen mutkan kautta (convert.py, zensical, print.js), ja
jokainen voi jäädä jälkeen ilman näkyvää vikaa. Siksi testit katsovat, päätyykö
juuri kirjoitettu virke paperille; koekirjaa muutetaan oikeasti, omassa kopiossa.
"""

from conftest import open_print_page


def headings(printed) -> list[str]:
    return printed.evaluate(
        "() => [...document.querySelectorAll('.md-content__inner > h1')]"
        "        .map(h => h.textContent.replace(/\\u00b6/g, '').trim())")


def text(printed) -> str:
    return printed.evaluate("() => document.body.innerText")


def test_edited_text_is_printed(mutable_book, serve, browser):
    """Muutettu virke tulee tulosteeseen ja vanha jää pois."""
    base_url = serve(mutable_book.site)
    printed = open_print_page(browser, base_url)
    assert "Ankkurin kohde." in text(printed)
    assert "Uusi virke tenttiohjeisiin." not in text(printed)

    page = mutable_book.src / "tenttiohjeet.md"
    page.write_text(page.read_text(encoding="utf-8").replace(
        "Ankkurin kohde.", "Uusi virke tenttiohjeisiin."), encoding="utf-8")
    mutable_book.rebuild()

    printed = open_print_page(browser, base_url)
    assert "Uusi virke tenttiohjeisiin." in text(printed)
    assert "Ankkurin kohde." not in text(printed)


def test_new_chapter_is_printed(mutable_book, serve, browser):
    """SUMMARY.md:hen lisätty luku päätyy tulosteeseen oikeaan kohtaan — ketjun
    pisin muoto: navigaatio, käännös ja haku tulostussivulle."""
    base_url = serve(mutable_book.site)
    printed = open_print_page(browser, base_url)
    before = headings(printed)
    assert "Uusi luku" not in before

    (mutable_book.src / "osa2" / "04-uusi.md").write_text(
        "# Uusi luku\n\nTämän pitää päätyä paperille asti.\n", encoding="utf-8")
    summary = mutable_book.src / "SUMMARY.md"
    summary.write_text(summary.read_text(encoding="utf-8").replace(
        "  - [Sisällytys](./osa2/03-sisallytys.md)\n",
        "  - [Sisällytys](./osa2/03-sisallytys.md)\n  - [Uusi luku](./osa2/04-uusi.md)\n"),
        encoding="utf-8")
    mutable_book.rebuild()

    printed = open_print_page(browser, base_url)
    assert headings(printed) == before + ["Uusi luku"]
    assert "Tämän pitää päätyä paperille asti." in text(printed)
    assert printed.print_calls == [f"Koottu {len(before) + 1} lukua."]
    # Uusi luku ei saa törmätä muiden lukujen tunnisteisiin. Soittimet rajataan
    # ulos: soittimen SVG-maski saa saman tunnuksen joka soittimessa.
    assert printed.evaluate("""() => {
      const ids = [...document.querySelectorAll('[id]')]
        .filter(e => !e.closest('.ap-wrapper')).map(e => e.id);
      return ids.filter((id, i) => ids.indexOf(id) !== i);
    }""") == []


def test_removed_chapter_leaves_the_print_page(mutable_book, serve, browser):
    """Poistettu luku katoaa myös tulosteesta: convert.py poistaa docs/:sta
    lähteestä kadonneet sivut (sync_docs)."""
    base_url = serve(mutable_book.site)
    printed = open_print_page(browser, base_url)
    before = headings(printed)

    summary = mutable_book.src / "SUMMARY.md"
    summary.write_text(summary.read_text(encoding="utf-8").replace(
        "  - [Tehtävät](./osa1/02-tehtavat.md)\n", ""), encoding="utf-8")
    (mutable_book.src / "osa1" / "02-tehtavat.md").unlink()
    mutable_book.rebuild()

    printed = open_print_page(browser, base_url)
    assert len(headings(printed)) == len(before) - 1
    assert "Sama otsikko kuin osan 2 tehtäväsivulla" not in text(printed)
