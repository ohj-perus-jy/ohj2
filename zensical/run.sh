#!/usr/bin/env bash
# Zensical-koeputken ajo:
#   ./run.sh              -> kopioi ../src -> docs/, vahdi muutoksia ja tarjoile
#                            portissa 8001
#   ./run.sh 8003         -> sama, eri portissa
#   ./run.sh build        -> pelkkä rakennus site/-hakemistoon
#   ./run.sh test         -> testit
set -euo pipefail
cd "$(dirname "$0")"

[[ -x .venv/bin/zensical ]] || ./setup.sh

# Testit kääntävät itse sen mitä tarvitsevat, joten convert.py:tä ei ajeta.
# Selain tarkistetaan erikseen, koska se ei ole .venv:ssä vaan kotihakemistossa
# ja sen systeemikirjastot kontissa; uusi devcontainer aloittaa ilman molempia.
# Tarkistus on ldd, koska "playwright install-deps" ajaisi apt-get updaten joka ajolla.
if [[ ${1:-} == test ]]; then
    shift
    if ! .venv/bin/python -c "import pytest, playwright" 2>/dev/null; then
        .venv/bin/pip install --quiet -r requirements-dev.txt
    fi
    browser=$(.venv/bin/python -c 'from playwright.sync_api import sync_playwright
with sync_playwright() as play:
    path = play.chromium.executable_path
print(path)' 2>/dev/null)
    if [[ ! -x $browser ]] || ldd "$browser" | grep -q "not found"; then
        .venv/bin/playwright install chromium
        echo "Asennetaan selaimen systeemikirjastot (vaatii sudon)..."
        sudo .venv/bin/playwright install-deps chromium
    fi
    exec .venv/bin/python -m pytest "$@"
fi

python3 convert.py

if [[ ${1:-} == build ]]; then
    exec .venv/bin/zensical build
fi

# Vahti palvelimen rinnalle: `zensical serve` seuraa docs/:ia, ei ../src:iä
# (convert.py: watch). Palvelinta ei exec:ata, jotta trap ehtii lopettaa vahdin.
python3 convert.py --watch &
watcher=$!
trap 'kill "$watcher" 2>/dev/null' EXIT INT TERM
.venv/bin/zensical serve --dev-addr "0.0.0.0:${1:-8001}"
