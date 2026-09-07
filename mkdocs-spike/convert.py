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
ASSETS = ROOT / "assets"

SUMMARY_LINK_RE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>-\s*)?\[(?P<title>[^\]]*)\]\((?P<href>[^)]*)\)")


def build_nav() -> str:
    """src/SUMMARY.md -> mkdocs nav: -lohko.

    Numerointi vastaa mdBookia: numeron saavat vain listakohdat
    ("- [Luku](...)"), juoksevasti myös ---erottimien yli. Etu- ja
    jälkilinkit (Aloitus, Työkalut, Luennot) jäävät numeroimatta, jolloin
    ne erottuvat osista ilman erillisiä erottimia.
    """
    entries: list[tuple[int, str, str, bool]] = []
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
        entries.append((len(match.group("indent")) // 2, title.replace('"', "'"), href,
                        bool(match.group("bullet"))))

    counters: list[int] = []

    def number_for(depth: int) -> str:
        """Juokseva numero syvyydelle: 1., 1.1., 1.2., 2., ..."""
        del counters[depth + 1:]
        while len(counters) <= depth:
            counters.append(0)
        counters[depth] += 1
        return ".".join(str(n) for n in counters) + "."

    def emit(index: int, depth: int, out: list[str]) -> int:
        pad = "  " * (depth + 1)
        while index < len(entries):
            level, title, href, numbered = entries[index]
            if level < depth:
                return index
            if numbered:
                title = f"{number_for(level)} {title}"
            has_children = index + 1 < len(entries) and entries[index + 1][0] > level
            if has_children:
                out.append(f'{pad}- "{title}":')
                # Paljas polku ensimmäisenä = Materialin navigation.indexes:
                # osan etusivusta tulee osan oma otsikkolinkki, kuten mdBookissa.
                out.append(f"{pad}  - {href}")
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
    shutil.copytree(ASSETS, DOCS / "assets", dirs_exist_ok=True)
    (ROOT / "nav.yml").write_text(build_nav(), encoding="utf-8")
    print(f"kopioitu {len(list(DOCS.rglob('*.md')))} markdown-tiedostoa -> {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
