#!/usr/bin/env python3
"""Kopioi mdBookin lähdepuu (../src) Zensicalin docs/-hakemistoksi.

Barebones-lähtötilanne: tämä skripti EI muunna sisältöä mitenkään. Se vain
kopioi tiedostot ja kääntää src/SUMMARY.md:n nav-lohkoksi, koska ilman
navigaatiota sivustoa ei voi selata lainkaan.

Kaikki mdBookin oma syntaksi ({{#include}}, //- piilorivit, java,ignore,
> [!VINKKI], <task>-kortit) jää siis sellaisenaan sivuille näkyviin. Se on
tarkoitus: näin näkee yhdellä silmäyksellä, mitä oikeasti pitää korjata.
Muunnokset lisätään takaisin yksi kerrallaan, ks. README.md.

Generoitu docs/ on kertakäyttöinen — tämä skripti on totuus.
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "src"
DOCS = ROOT / "docs"

SUMMARY_LINK_RE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>-\s*)?\[(?P<title>[^\]]*)\]\((?P<href>[^)]*)\)")


def build_nav() -> str:
    """src/SUMMARY.md -> mkdocs nav: -lohko.

    Otsikot ja järjestys tulevat sellaisenaan SUMMARY.md:stä. mdBookin
    automaattinen lukujen numerointi EI ole mukana — se on yksi
    tarkistuslistan kohta, ei oletus.
    """
    entries: list[tuple[int, str, str]] = []
    for raw in (SRC / "SUMMARY.md").read_text(encoding="utf-8").split("\n"):
        if not raw.strip() or raw.strip().startswith("#") or set(raw.strip()) == {"-"}:
            continue
        match = SUMMARY_LINK_RE.match(raw)
        if not match:
            continue
        href = match.group("href").strip()
        title = match.group("title").strip()
        if not href:
            # SUMMARY.md:n kikka ulkoiselle linkille: [Otsikko<https://url>]()
            embedded = re.match(r"^(?P<t>.*?)<(?P<u>https?://[^>]+)>$", title)
            if not embedded:
                continue
            title, href = embedded.group("t").strip(), embedded.group("u")
        else:
            href = href.lstrip("./")
        entries.append((len(match.group("indent")) // 2, title.replace('"', "'"), href))

    def emit(index: int, depth: int, out: list[str]) -> int:
        pad = "  " * (depth + 1)
        while index < len(entries):
            level, title, href = entries[index]
            if level < depth:
                return index
            has_children = index + 1 < len(entries) and entries[index + 1][0] > level
            if has_children:
                out.append(f'{pad}- "{title}":')
                out.append(f'{pad}  - "{title}": {href}')
                index = emit(index + 1, depth + 1, out)
            else:
                out.append(f'{pad}- "{title}": {href}')
                index += 1
        return index

    lines = ["nav:"]
    emit(0, 0, lines)
    return "\n".join(lines) + "\n"


def main() -> int:
    if not SRC.is_dir():
        print(f"lähdepuu puuttuu: {SRC}", file=sys.stderr)
        return 1
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(SRC, DOCS)
    (DOCS / "SUMMARY.md").unlink(missing_ok=True)
    (ROOT / "nav.yml").write_text(build_nav(), encoding="utf-8")
    print(f"kopioitu {len(list(DOCS.rglob('*.md')))} markdown-tiedostoa -> {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
