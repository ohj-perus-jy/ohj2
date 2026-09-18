"""Vaiheittaisen ohjeen äänten teko (puhe.py) ilman puhepalvelua: synteesi
korvataan funktiolla, joka kirjaa pyynnöt."""

import convert
import puhe

PAGE = ('<walkthrough scenes="images/k.js" audio="images/puhe">\n\n'
        '<step scene="a">\n\nEka.\n\n</step>\n\n'
        '<step scene="b">\n\nToka.\n\n</step>\n\n'
        "</walkthrough>\n")


def test_ssml_escapes_the_text_and_keeps_the_lines_as_paragraphs():
    assert puhe.ssml("A & B.\nC <D>.", "fi-FI-NooraNeural") == (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="fi-FI">'
        '<voice name="fi-FI-NooraNeural"><p>A &amp; B.</p><p>C &lt;D&gt;.</p></voice></speak>')


def test_refresh_makes_only_missing_and_changed_audio(tmp_path):
    """Ensimmäinen ajo tekee kaikki, toinen ei mitään. Muuttunut vaihe tehdään
    uudelleen ja poistuneen ääni poistetaan; käännös hyväksyy tuloksen.
    Äänen vaihto tekee kaikki uudelleen."""
    page = tmp_path / "sivu.md"
    page.write_text(PAGE, encoding="utf-8")
    requests: list[str] = []

    def synthesize(document: str) -> bytes:
        requests.append(document)
        return b"mp3"

    def refresh(**options) -> list[str]:
        return puhe.refresh(page, synthesize, log=lambda _: None, **options)

    assert refresh() == ["a", "b"]
    assert "<p>Eka.</p>" in requests[0] and puhe.VOICE in requests[0]
    assert refresh() == []
    page.write_text(PAGE.replace('<step scene="a">\n\nEka.\n\n</step>\n\n', "")
                    .replace("Toka.", "Toinen."), encoding="utf-8")
    assert refresh() == ["b"]
    folder = tmp_path / "images" / "puhe"
    assert sorted(file.name for file in folder.iterdir()) == ["b.mp3", "puhe.json"]
    assert convert.walkthrough_audio(page.read_text(encoding="utf-8"), "sivu.md", tmp_path) == (
        {"b": "../images/puhe/b.mp3"}, [])
    assert refresh(voice="fi-FI-NooraNeural") == ["b"]
