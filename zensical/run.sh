#!/usr/bin/env bash
# Zensical-koeputken ajo:
#   ./run.sh              -> kopioi ../src -> docs/ ja tarjoile portissa 8001
#   ./run.sh 8003         -> sama, eri portissa
#   ./run.sh build        -> pelkkä rakennus site/-hakemistoon
#   ./run.sh test         -> testit, ks. README.md:n "Testit"
set -euo pipefail
cd "$(dirname "$0")"

[[ -x .venv/bin/zensical ]] || ./setup.sh

# Testit kääntävät itse sen mitä tarvitsevat, joten convert.py:tä ei ajeta
# tässä. Riippuvuudet asennetaan vasta ensimmäisellä ajolla.
#
# Selain tarkistetaan erikseen paketeista, koska se ei ole .venv:ssä vaan
# kotihakemistossa (~/.cache/ms-playwright) ja sen systeemikirjastot kontissa.
# Kumpikin voi puuttua, vaikka paketit importtaisivat: uusi devcontainer
# aloittaa ilman molempia. Juuri niin kävi, kun koeputki kloonattiin
# ensimmäisen kerran puhtaaseen konttiin — pytest ja playwright olivat
# paikallaan, mutta selain ei käynnistynyt (libcups.so.2 puuttui).
#
# Tarkistus on ldd eikä pelkkä asennuskomento, koska "playwright
# install-deps" ajaa apt-get updaten: se maksaisi joka ajolla ja vaatisi
# verkon myös silloin, kun kaikki on jo paikallaan.
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
exec .venv/bin/zensical serve --dev-addr "0.0.0.0:${1:-8001}"
