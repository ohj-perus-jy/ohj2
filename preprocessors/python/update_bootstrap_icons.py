#!/usr/bin/env python3
"""
Scans the project for Bootstrap Icons usage (bi-* classes and direct codepoint
references) and generates a minimal, self-contained theme/bootstrap-icons.css
with only the required icon glyphs subset and base64-inlined into the CSS.

Requirements: fonttools, brotli  (pip install fonttools brotli)

Usage:
    python3 preprocessors/python/update_bootstrap_icons.py

The script will:
  1. Scan src/ and theme/ for bi-* class usage and direct \\fXXXX codepoints
  2. Download the full Bootstrap Icons font + CSS (cached in .cache/bootstrap-icons/)
  3. Subset the font to only the required glyphs
  4. Generate theme/bootstrap-icons.css with base64-inlined fonts
"""

import base64
import os
import re
import sys
import urllib.request
from pathlib import Path

BI_VERSION = "1.11.3"
BI_CDN_BASE = f"https://cdn.jsdelivr.net/npm/bootstrap-icons@{BI_VERSION}/font"

# Resolve project root (two levels up from this script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CACHE_DIR = PROJECT_ROOT / ".cache" / "bootstrap-icons"
OUTPUT_CSS = PROJECT_ROOT / "theme" / "bootstrap-icons.css"

# Directories to scan for icon usage
SCAN_DIRS = [PROJECT_ROOT / "src", PROJECT_ROOT / "theme"]
SCAN_EXTENSIONS = {".md", ".hbs", ".css", ".html", ".js"}

# Patterns
BI_CLASS_PATTERN = re.compile(r'\bbi-([\w-]+)\b')
# Matches codepoints used with bootstrap-icons font-family in CSS (e.g. content: "\f285")
BI_CODEPOINT_PATTERN = re.compile(r'content:\s*"\\([0-9a-fA-F]{4,5})"')
# Matches .bi-ICON::before{content:"XXXX"} in the full CSS
BI_CSS_RULE_PATTERN = re.compile(r'\.bi-([\w-]+)(?:::before|:before)\{content:"\\([0-9a-fA-F]+)"\}')


def ensure_cached_files():
    """Download full Bootstrap Icons CSS and font files if not cached."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    font_dir = CACHE_DIR / "fonts"
    font_dir.mkdir(exist_ok=True)

    files = {
        CACHE_DIR / "bootstrap-icons.min.css": f"{BI_CDN_BASE}/bootstrap-icons.min.css",
        font_dir / "bootstrap-icons.woff2": f"{BI_CDN_BASE}/fonts/bootstrap-icons.woff2",
        font_dir / "bootstrap-icons.woff": f"{BI_CDN_BASE}/fonts/bootstrap-icons.woff",
    }

    for local_path, url in files.items():
        if not local_path.exists():
            print(f"  Downloading {url}...")
            urllib.request.urlretrieve(url, local_path)

    return CACHE_DIR / "bootstrap-icons.min.css", font_dir


def build_codepoint_map(css_path):
    """Parse the full CSS and return a dict of icon_name -> codepoint (hex string)."""
    css = css_path.read_text(encoding="utf-8")
    return {name: cp for name, cp in BI_CSS_RULE_PATTERN.findall(css)}


def scan_used_icons(codepoint_map):
    """Scan project files for bi-* class names and direct codepoint references."""
    used_icons = set()
    used_codepoints = set()
    reverse_map = {cp.lower(): name for name, cp in codepoint_map.items()}

    # Exclude the generated output file from scanning
    exclude = {OUTPUT_CSS.resolve()}

    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for path in scan_dir.rglob("*"):
            if path.suffix not in SCAN_EXTENSIONS or path.resolve() in exclude:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            # Find bi-* class references
            for match in BI_CLASS_PATTERN.finditer(text):
                icon_name = match.group(1)
                if icon_name in codepoint_map:
                    used_icons.add(icon_name)

            # Find direct codepoint references (only in CSS files with bootstrap-icons font)
            if path.suffix == ".css" and "bootstrap-icons" in text:
                for match in BI_CODEPOINT_PATTERN.finditer(text):
                    cp = match.group(1).lower()
                    used_codepoints.add(cp)
                    if cp in reverse_map:
                        used_icons.add(reverse_map[cp])

    return used_icons


def subset_font(font_path, codepoints, flavor):
    """Subset a font file to only include the given Unicode codepoints."""
    from fontTools.subset import Subsetter, load_font, save_font

    font = load_font(str(font_path), Options(flavor=flavor))
    subsetter = Subsetter(Options(flavor=flavor))
    subsetter.populate(unicodes=[int(cp, 16) for cp in codepoints])
    subsetter.subset(font)

    import io
    buf = io.BytesIO()
    save_font(font, buf, Options(flavor=flavor))
    font.close()
    return buf.getvalue()


class Options:
    """Minimal options object for fontTools subsetter."""
    def __init__(self, flavor=None):
        self.flavor = flavor


def subset_font_bytes(font_path, codepoints_hex, flavor):
    """Subset a font to only include specific codepoints. Returns bytes."""
    from fontTools.subset import main as subset_main
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=f".{flavor}", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        unicodes = ",".join(f"U+{cp}" for cp in codepoints_hex)
        # fontTools.subset.main uses sys.argv
        old_argv = sys.argv
        sys.argv = [
            "pyftsubset",
            str(font_path),
            f"--unicodes={unicodes}",
            f"--output-file={tmp_path}",
            f"--flavor={flavor}",
        ]
        try:
            subset_main()
        finally:
            sys.argv = old_argv

        return Path(tmp_path).read_bytes()
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def generate_css(used_icons, codepoint_map, woff2_b64, woff_b64):
    """Generate the minimal bootstrap-icons CSS."""
    lines = [
        f"/*!",
        f" * Bootstrap Icons v{BI_VERSION} - Subset",
        f" * Only includes icons used in this project ({len(used_icons)} icons).",
        f" * Regenerate: python3 preprocessors/python/update_bootstrap_icons.py",
        f" * Full library: https://icons.getbootstrap.com/",
        f" */",
        f"@font-face {{",
        f"  font-display: swap;",
        f"  font-family: bootstrap-icons;",
        f'  src: url("data:font/woff2;base64,{woff2_b64}") format("woff2"),',
        f'       url("data:font/woff;base64,{woff_b64}") format("woff");',
        f"}}",
        f"",
        f'[class^="bi-"]::before,',
        f'[class*=" bi-"]::before {{',
        f"  display: inline-block;",
        f"  font-family: bootstrap-icons !important;",
        f"  font-style: normal;",
        f"  font-weight: 400 !important;",
        f"  font-variant: normal;",
        f"  text-transform: none;",
        f"  line-height: 1;",
        f"  vertical-align: -.125em;",
        f"  -webkit-font-smoothing: antialiased;",
        f"  -moz-osx-font-smoothing: grayscale;",
        f"}}",
        f"",
    ]

    for name in sorted(used_icons):
        cp = codepoint_map[name]
        lines.append(f'.bi-{name}::before {{ content: "\\{cp}"; }}')

    lines.append("")  # trailing newline
    return "\n".join(lines)


def main():
    print(f"Bootstrap Icons subset generator (v{BI_VERSION})")
    print()

    # Step 1: Ensure cached files
    print("1. Checking cached font files...")
    css_path, font_dir = ensure_cached_files()

    # Step 2: Build codepoint map from full CSS
    print("2. Building codepoint map...")
    codepoint_map = build_codepoint_map(css_path)
    print(f"   {len(codepoint_map)} icons available")

    # Step 3: Scan for used icons
    print("3. Scanning project for icon usage...")
    used_icons = scan_used_icons(codepoint_map)

    if not used_icons:
        print("   No bootstrap icons found in project!")
        sys.exit(1)

    print(f"   Found {len(used_icons)} icons: {', '.join(sorted(used_icons))}")

    # Step 4: Read current CSS to check if update is needed
    current_icons = set()
    if OUTPUT_CSS.exists():
        for match in re.finditer(r'\.bi-([\w-]+)::before', OUTPUT_CSS.read_text()):
            current_icons.add(match.group(1))

    if current_icons == used_icons:
        print()
        print("Already up to date — no changes needed.")
        return

    if current_icons:
        added = used_icons - current_icons
        removed = current_icons - used_icons
        if added:
            print(f"   New icons: {', '.join(sorted(added))}")
        if removed:
            print(f"   Removed icons: {', '.join(sorted(removed))}")

    # Step 5: Subset fonts
    print("4. Subsetting fonts...")
    codepoints_hex = [codepoint_map[name] for name in used_icons]

    woff2_bytes = subset_font_bytes(
        font_dir / "bootstrap-icons.woff2", codepoints_hex, "woff2"
    )
    woff_bytes = subset_font_bytes(
        font_dir / "bootstrap-icons.woff", codepoints_hex, "woff"
    )

    woff2_b64 = base64.b64encode(woff2_bytes).decode()
    woff_b64 = base64.b64encode(woff_bytes).decode()

    print(f"   woff2: {len(woff2_bytes):,} bytes, woff: {len(woff_bytes):,} bytes")

    # Step 6: Generate CSS
    print("5. Generating theme/bootstrap-icons.css...")
    css = generate_css(used_icons, codepoint_map, woff2_b64, woff_b64)
    OUTPUT_CSS.write_text(css, encoding="utf-8")
    print(f"   Written {len(css):,} bytes")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
