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
if [[ ${1:-} == test ]]; then
    shift
    if ! .venv/bin/python -c "import pytest, playwright" 2>/dev/null; then
        .venv/bin/pip install --quiet -r requirements-dev.txt
        .venv/bin/playwright install chromium
    fi
    exec .venv/bin/python -m pytest "$@"
fi

python3 convert.py

if [[ ${1:-} == build ]]; then
    exec .venv/bin/zensical build
fi
exec .venv/bin/zensical serve --dev-addr "0.0.0.0:${1:-8001}"
