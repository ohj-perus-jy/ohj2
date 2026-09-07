#!/usr/bin/env python3
"""Convert the mdBook source tree (../src) into a MkDocs docs/ tree.

The generated docs/ directory is disposable — this script is the source of
truth. Run it again after every change to ../src.

Transformations:
  {{#include p}}         ->  --8<-- "p"            (pymdownx.snippets)
  ```java,ignore         ->  ```{ .java .ignore }  (superfences brace format)
  //-<code>              ->  <code>, line recorded in data-boring="..."
  // FILE: x  ... FILE_END -> Material content tabs, one per file
"""

import re
import shutil
import sys
from pathlib import Path

# Sama slugify jota mkdocs.yml käyttää, jotta kiinnitetyt ankkurit vastaavat
# niitä joita Python-Markdown muuten tuottaisi.
from pymdownx.slugs import slugify

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "src"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

# book.toml: [output.html.code.hidelines] java = "//-", javascript = "//-"
HIDELINE_PREFIX = "//-"
HIDELINE_LANGS = {"java", "javascript"}
PLAYGROUND_LANGS = {"java", "javascript"}

FENCE_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<ticks>`{3,})(?P<info>[^`]*)$")
H1_RE = re.compile(r"^#\s+\S")
H2_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
PINNED_ID_RE = re.compile(r"\{[^}]*#[^}]*\}\s*$")
INCLUDE_RE = re.compile(r"\{\{#include\s+(?P<path>[^}]+?)\s*\}\}")
FILE_START_RE = re.compile(r"^\s*//\s*FILE:\s*(?P<name>.+?)\s*$")
FILE_END_RE = re.compile(r"^\s*//\s*FILE_END\s*$")
# md_in_html renderöi HTML-lohkon sisällön markdownina vain markdown="1":llä.
MD_IN_HTML_TAGS = ("task", "handout")
OPEN_TAG_RE = re.compile(r"<(?P<tag>" + "|".join(MD_IN_HTML_TAGS) + r")(?P<attrs>[^>]*)>")


def mark_md_in_html(line: str) -> str:
    def repl(match: re.Match) -> str:
        attrs = match.group("attrs")
        if "markdown=" in attrs:
            return match.group(0)
        return f'<{match.group("tag")}{attrs} markdown="1">'

    return OPEN_TAG_RE.sub(repl, line)


def convert_include(match: re.Match, md_path: Path) -> str:
    """{{#include ../a/b.java}} -> --8<-- "a/b.java" (relative to docs root)."""
    raw = match.group("path")
    # mdBook line anchors: "file:6" means line 6 only, "file:2:5" a range.
    parts = raw.split(":")
    target, anchor = parts[0], parts[1:]
    resolved = (md_path.parent / target).resolve()
    try:
        rel = resolved.relative_to(SRC)
    except ValueError:
        # Outside src/ — leave the include untouched so it shows up as a defect.
        return match.group(0)
    suffix = ""
    if len(anchor) == 1:
        suffix = f":{anchor[0]}:{anchor[0]}"
    elif len(anchor) == 2:
        suffix = f":{anchor[0]}:{anchor[1]}"
    return f'--8<-- "{rel.as_posix()}{suffix}"'


def split_files(body: list[str]) -> list[tuple[str | None, list[str]]]:
    """Split a code block on // FILE: markers into (filename, lines) parts."""
    if not any(FILE_START_RE.match(line) for line in body):
        return [(None, body)]
    parts: list[tuple[str | None, list[str]]] = []
    name: str | None = None
    current: list[str] = []
    for line in body:
        start = FILE_START_RE.match(line)
        if start:
            if name is not None or current:
                parts.append((name, current))
            name, current = start.group("name"), []
            continue
        if FILE_END_RE.match(line):
            parts.append((name, current))
            name, current = None, []
            continue
        current.append(line)
    if current and any(l.strip() for l in current):
        parts.append((name, current))
    return [(n, strip_blank_edges(ls)) for n, ls in parts if n is not None or any(l.strip() for l in ls)]


def strip_blank_edges(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def extract_hidelines(lines: list[str], lang: str) -> tuple[list[str], list[int]]:
    """Strip the //- prefix, returning cleaned lines and 1-based hidden line numbers."""
    if lang not in HIDELINE_LANGS:
        return lines, []
    out: list[str] = []
    boring: list[int] = []
    for number, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith(HIDELINE_PREFIX):
            indent = line[: len(line) - len(stripped)]
            out.append(indent + stripped[len(HIDELINE_PREFIX):])
            boring.append(number)
        else:
            out.append(line)
    return out, boring


def build_attrs(lang: str, flags: set[str], boring: list[int], filename: str | None) -> str:
    classes = [f".{lang}"] if lang else []
    for flag in ("ignore", "noplayground", "editable"):
        if flag in flags:
            classes.append(f".{flag}")
    if lang in PLAYGROUND_LANGS and not flags & {"ignore", "noplayground"}:
        classes.append(".playground")
    attrs = " ".join(classes)
    if lang:
        # superfences kuluttaa .java-luokan kielimäärittelyksi eikä se päädy
        # HTML:ään, joten ajonappi tarvitsee kielen omana attribuuttinaan.
        attrs += f' data-lang="{lang}"'
    if boring:
        attrs += f' data-boring="{" ".join(str(n) for n in boring)}"'
    if filename:
        attrs += f' data-file="{filename}"'
    return "{ " + attrs + " }"


def render_fence(indent: str, ticks: str, lang: str, flags: set[str],
                 body: list[str]) -> list[str]:
    parts = split_files(body)
    if len(parts) == 1 and parts[0][0] is None:
        lines, boring = extract_hidelines(parts[0][1], lang)
        attrs = build_attrs(lang, flags, boring, None)
        return [f"{indent}{ticks}{attrs}", *lines, f"{indent}{ticks}"]

    # Multi-file block -> Material content tabs.
    out: list[str] = []
    pad = indent + "    "
    for filename, raw in parts:
        lines, boring = extract_hidelines(raw, lang)
        attrs = build_attrs(lang, flags, boring, filename)
        out.append(f'{indent}=== "{filename}"')
        out.append("")
        out.append(f"{pad}{ticks}{attrs}")
        out.extend(pad + line if line.strip() else "" for line in lines)
        out.append(f"{pad}{ticks}")
        out.append("")
    return out


def has_h1(lines: list[str]) -> bool:
    """Onko tiedosto oikea sivu vai pelkkä include (exercises/handout.md)?"""
    for line in lines:
        if line.strip():
            return bool(H1_RE.match(line))
    return False


def number_heading(line: str, number: int) -> str:
    """## Otsikko  ->  ## 1. Otsikko { #alkuperainen-ankkuri }

    Ankkuri kiinnitetään eksplisiittisesti, jotta numeron lisääminen ei muuta
    sitä — muuten sisäiset linkit ja TIMistä tulevat viittaukset hajoaisivat.
    """
    match = H2_RE.match(line)
    if not match or PINNED_ID_RE.search(line):
        return line
    title = match.group("title")
    return f"## {number}. {title} {{ #{slugify(case='lower')(title, '-')} }}"


def convert_markdown(text: str, md_path: Path) -> str:
    out: list[str] = []
    lines = text.split("\n")
    numbering = has_h1(lines)
    section = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        fence = FENCE_RE.match(line)
        if not fence:
            if numbering and H2_RE.match(line):
                section += 1
                line = number_heading(line, section)
            out.append(mark_md_in_html(
                INCLUDE_RE.sub(lambda m: convert_include(m, md_path), line)))
            index += 1
            continue

        indent, ticks = fence.group("indent"), fence.group("ticks")
        info = fence.group("info").strip()
        body: list[str] = []
        index += 1
        while index < len(lines):
            closing = FENCE_RE.match(lines[index])
            if closing and not closing.group("info").strip() and len(closing.group("ticks")) >= len(ticks):
                index += 1
                break
            body.append(lines[index])
            index += 1

        body = [INCLUDE_RE.sub(lambda m: convert_include(m, md_path), l) for l in body]
        tokens = [t for t in info.split(",") if t.strip()]
        lang = tokens[0].strip() if tokens else ""
        flags = {t.strip() for t in tokens[1:]}
        if not lang or info.startswith("{"):
            out.extend([line, *body, f"{indent}{ticks}"])
            continue
        out.extend(render_fence(indent, ticks, lang, flags, body))
    return "\n".join(out)


SUMMARY_LINK_RE = re.compile(
    r"^(?P<indent>\s*)(?P<bullet>-\s*)?\[(?P<title>[^\]]*)\]\((?P<href>[^)]*)\)")


def build_nav() -> str:
    """Turn src/SUMMARY.md into a mkdocs nav: block.

    mdBook numbers only the list items ("- [Luku](...)"), continuously and
    across the `---` separators; the prefix/suffix links (Työkalut, Luennot,
    Eteneminen) stay unnumbered. Reproduced here so the sidebar reads the same.
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
            # SUMMARY hack: [Title<https://url>]() — an external link.
            embedded = re.match(r"^(?P<t>.*?)<(?P<u>https?://[^>]+)>$", title)
            if not embedded:
                continue
            title, href = embedded.group("t").strip(), embedded.group("u")
        else:
            href = href.lstrip("./")
        depth = len(match.group("indent")) // 2
        numbered = bool(match.group("bullet"))
        entries.append((depth, title.replace('"', "'"), href, numbered))

    counters: list[int] = []

    def number_for(depth: int) -> str:
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
            label = f"{number_for(level)} {title}" if numbered else title
            has_children = index + 1 < len(entries) and entries[index + 1][0] > level
            if has_children:
                out.append(f'{pad}- "{label}":')
                # mkdocs-section-index tekee osan etusivusta itse otsikon linkin,
                # kuten mdBookissa — ilman sitä sivu toistuisi lapsena.
                out.append(f"{pad}  - {href}")
                index = emit(index + 1, depth + 1, out)
            else:
                out.append(f'{pad}- "{label}": {href}')
                index += 1
        return index

    lines = ["nav:"]
    emit(0, 0, lines)
    return "\n".join(lines) + "\n"


def copy_ace() -> None:
    """Vendor the ACE editor from the mdBook build output, if one exists.

    mdBook toimittaa ace.js:n itse; MkDocs ei. Editoitavia lohkoja on koko
    materiaalissa vain kaksi, joten tässä riittää kopio olemassa olevasta
    buildista — oikeassa migraatiossa ACE otettaisiin npm:stä tai CDN:stä.
    """
    book = ROOT.parent / "book"
    vendor = DOCS / "assets" / "js" / "vendor"
    names = ["ace.js", "theme-dawn.js", "theme-tomorrow_night.js"]
    available = [n for n in names if (book / n).is_file()]
    if not available:
        print("note: ../book not built, ACE not vendored (editable blocks stay static)")
        return
    vendor.mkdir(parents=True, exist_ok=True)
    for name in available:
        shutil.copy2(book / name, vendor / name)
    mode_java = ROOT.parent / "theme" / "mode-java.js"
    if mode_java.is_file():
        shutil.copy2(mode_java, vendor / "mode-java.js")


def main() -> int:
    if not SRC.is_dir():
        print(f"source tree missing: {SRC}", file=sys.stderr)
        return 1
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(SRC, DOCS)

    converted = 0
    for md_path in sorted(SRC.rglob("*.md")):
        target = DOCS / md_path.relative_to(SRC)
        target.write_text(
            convert_markdown(md_path.read_text(encoding="utf-8"), md_path),
            encoding="utf-8",
        )
        converted += 1
    (DOCS / "SUMMARY.md").unlink(missing_ok=True)

    shutil.copytree(ASSETS, DOCS / "assets", dirs_exist_ok=True)
    copy_ace()
    (ROOT / "nav.yml").write_text(build_nav(), encoding="utf-8")

    print(f"converted {converted} markdown files into {DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
