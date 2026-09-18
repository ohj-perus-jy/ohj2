#!/usr/bin/env bash
# Sivuston ajo: ./run.sh [portti | build | test | puhe SIVU], ks. tyokalut/README.md.
# Työkalut ovat git-submodule (github.com/ohj-perus-jy/kirjatyokalut).
set -euo pipefail
cd "$(dirname "$0")"
[[ -f tyokalut/run.sh ]] || git submodule update --init tyokalut
# "+" = tyokalut/ on eri versiossa kuin kirja odottaa (git pull ei päivitä sitä).
if git submodule status tyokalut | grep -q '^+'; then
    echo "huom: zensical/tyokalut on eri versiossa kuin kirja odottaa;" \
         "päivitä: git submodule update (tai committaa uusi versio)" >&2
fi
exec tyokalut/run.sh "$@"
