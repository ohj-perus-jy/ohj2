"""Testien yhteiset palikat: käännetty sivusto, palvelin ja selain.

Sivusto käännetään oikeasti (convert.py + zensical build): tulostussivu
kootaan valmiista HTML:stä, joten testattava syntyy vasta käännöksessä.
Tiedostojako: PERUSTELUT.md, "Testien rakenne".
"""

import functools
import http.server
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# zensical-komento on samassa hakemistossa kuin testejä ajava python (.venv/bin).
ZENSICAL = Path(sys.executable).parent / "zensical"


def pytest_addoption(parser):
    parser.addoption(
        "--nobuild", action="store_true",
        help="älä käännä oikeaa kirjaa uudelleen, käytä olemassa olevaa site/:ä")


def build(zensical_dir: Path) -> Path:
    """convert.py + zensical build annetussa hakemistossa. -> site/."""
    for command in ([sys.executable, "convert.py"], [str(ZENSICAL), "build"]):
        result = subprocess.run(command, cwd=zensical_dir, capture_output=True,
                                text=True)
        if result.returncode:
            raise AssertionError(
                f"{' '.join(command)} epäonnistui:\n{result.stdout}\n{result.stderr}")
    return zensical_dir / "site"


# Kaikki, mistä käännetty sivusto riippuu: myös koeputken omat palaset
# vanhentavat sivuston muuttuessaan.
SOURCES = ("../src", "assets", "overrides", "convert.py", "mkdocs.yml")


def is_stale(site: Path) -> bool:
    """Onko käännetty sivusto jäljessä lähteistään? Käännös on hidas eikä
    sitä tehdä turhaan, mutta vanhalla sivustolla ei saa testata."""
    index = site / "index.html"
    if not index.is_file():
        return True
    built = index.stat().st_mtime
    for name in SOURCES:
        source = ROOT / name
        paths = source.rglob("*") if source.is_dir() else [source]
        if any(path.stat().st_mtime > built for path in paths if path.is_file()):
            return True
    return False


@pytest.fixture(scope="session")
def real_site(request) -> Path:
    """Oikea kirja (../src) käännettynä. Käännetään vain jos site/ on jäljessä."""
    site = ROOT / "site"
    if request.config.getoption("--nobuild"):
        if not (site / "index.html").is_file():
            pytest.skip("site/ puuttuu eikä --nobuild anna kääntää sitä")
        return site
    return build(ROOT) if is_stale(site) else site


def copy_book(target: Path) -> Path:
    """Koekirja + koeputken koneisto omaan hakemistoonsa. -> zensical-hakemisto.

    Sama rakenne kuin repossa (src/ ja zensical/ sisaruksina), koska convert.py
    etsii lähdepuun omasta sijainnistaan.
    """
    shutil.copytree(ROOT / "tests" / "book" / "src", target / "src")
    zensical = target / "zensical"
    zensical.mkdir()
    for name in ("convert.py", "mkdocs.yml"):
        shutil.copy(ROOT / name, zensical / name)
    for name in ("assets", "overrides"):
        shutil.copytree(ROOT / name, zensical / name)
    return zensical


@dataclass
class Book:
    """Käännetty koekirja, jonka materiaalia testi saa muuttaa."""

    src: Path
    zensical: Path
    site: Path

    def rebuild(self) -> None:
        self.site = build(self.zensical)


@pytest.fixture(scope="session")
def book(tmp_path_factory) -> Book:
    """Koekirja käännettynä kerran. Vain luettavaksi."""
    zensical = copy_book(tmp_path_factory.mktemp("book"))
    return Book(zensical.parent / "src", zensical, build(zensical))


@pytest.fixture
def mutable_book(tmp_path_factory) -> Book:
    """Oma koekirja testille, joka muuttaa materiaalia."""
    zensical = copy_book(tmp_path_factory.mktemp("book"))
    return Book(zensical.parent / "src", zensical, build(zensical))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def serve():
    """serve(site) -> osoite. Tulostussivu hakee luvut fetchillä, joten
    file:// ei kelpaa. Säikeistetty palvelin, koska haut lähtevät rinnakkain."""
    servers = []

    def start(site: Path) -> str:
        handler = functools.partial(QuietHandler, directory=str(site))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        servers.append(server)
        return f"http://127.0.0.1:{server.server_address[1]}"

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        instance = playwright.chromium.launch()
        yield instance
        instance.close()


@dataclass
class PrintPage:
    """Avattu /tulosta/, jolta selain on koonnut kirjan ja pyytänyt tulostusta."""

    page: object
    print_calls: list[str] = field(default_factory=list)
    drawn_lines: list[int] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def evaluate(self, script):
        return self.page.evaluate(script)


def open_print_page(browser, base_url: str, timeout: int = 120_000) -> PrintPage:
    """Avaa /tulosta/ ja odota, että sivu on koottu ja tulostusta pyydetty.

    window.print korvataan laskurilla: headless-selaimessa tulostusikkunaa ei
    ole. Kutsun hetkellä talletetaan tilarivi ja piirrettyjen terminaalirivien
    määrä, koska juuri se tila päätyy paperille.
    """
    page = browser.new_page()
    result = PrintPage(page)
    page.on("pageerror", lambda error: result.errors.append(str(error)))
    # Resurssin 404 tulee konsoliin ilman osoitetta, joten se otetaan mukaan
    # location-kentästä: muuten tunnettua puuttuvaa kuvaa ei voisi erottaa.
    page.on("console", lambda message: message.type == "error"
            and result.errors.append(
                f"{message.text} {message.location['url']}".strip()))
    page.add_init_script(
        "window.__printCalls = [];"
        "window.__drawnLines = [];"
        "window.print = () => {"
        "  window.__printCalls.push("
        "    document.getElementById('jyu-print-status').textContent.trim());"
        "  window.__drawnLines.push(document.querySelectorAll('.ap-line').length);"
        "};")
    page.goto(f"{base_url}/tulosta/", wait_until="load")
    page.wait_for_function("window.__printCalls.length > 0", timeout=timeout)
    result.print_calls = page.evaluate("window.__printCalls")
    result.drawn_lines = page.evaluate("window.__drawnLines")
    return result
