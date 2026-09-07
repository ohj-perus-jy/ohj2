#!/usr/bin/env bash
# MkDocs-koeputken ajo:  ./run.sh          -> muunna ja tarjoile portissa 8001
#                        ./run.sh build    -> muunna ja rakenna site/
# PYTHONPATH tuo extensions/custom_blocks.py:n Python-Markdownin saataville.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/python convert.py
command=${1:-serve}
if [[ $command == serve ]]; then
    PYTHONPATH=extensions .venv/bin/mkdocs serve -a 0.0.0.0:8001
else
    PYTHONPATH=extensions .venv/bin/mkdocs "$@"
fi
