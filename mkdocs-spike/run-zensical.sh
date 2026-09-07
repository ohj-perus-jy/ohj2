#!/usr/bin/env bash
# Sama koeputki Zensicalilla (Material for MkDocsin tekijöiden uusi generaattori).
#
#   ./run-zensical.sh          # muunna, rakenna ja tarjoile portissa 8003
#   ./run-zensical.sh build    # pelkkä rakennus
#
# Zensical lukee saman mkdocs.yml:n. Sivusto tarjoillaan tavallisella
# staattisella palvelimella eikä "zensical serve":llä, koska dev-palvelin
# tarjoaa vain hakemistomuotoisia osoitteita, kun taas sivujen linkit
# osoittavat .html-päätteisiin (use_directory_urls: false) — jokainen linkki
# johtaisi esikatselussa 404:ään. Rakennettu sivusto on oikein.
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -x .venv-zensical/bin/zensical ]]; then
    echo "Asennetaan Zensical..."
    python3 -m venv .venv-zensical
    .venv-zensical/bin/pip install --quiet --upgrade pip
    .venv-zensical/bin/pip install --quiet -r requirements-zensical.txt
fi

.venv/bin/python convert.py
PYTHONPATH=extensions .venv-zensical/bin/zensical build

if [[ ${1:-serve} == serve ]]; then
    echo
    echo "Tarjoillaan http://localhost:8003"
    cd site && exec python3 -m http.server 8003 --bind 0.0.0.0
fi
