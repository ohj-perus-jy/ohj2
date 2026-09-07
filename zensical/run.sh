#!/usr/bin/env bash
# Zensical-koeputken ajo:
#   ./run.sh              -> kopioi ../src -> docs/ ja tarjoile portissa 8001
#   ./run.sh 8003         -> sama, eri portissa
#   ./run.sh build        -> pelkkä rakennus site/-hakemistoon
set -euo pipefail
cd "$(dirname "$0")"

[[ -x .venv/bin/zensical ]] || ./setup.sh

python3 convert.py

if [[ ${1:-} == build ]]; then
    exec .venv/bin/zensical build
fi
exec .venv/bin/zensical serve --dev-addr "0.0.0.0:${1:-8001}"
