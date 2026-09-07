#!/usr/bin/env bash
# Kertaluontoinen asennus koeputkea varten. Ajettavissa uudelleen turvallisesti.
#
# Devcontainer-imagessa on python3 mutta ei pip:iä eikä venv:iä, joten ne
# asennetaan tässä. Oikeassa migraatiossa nämä menisivät tooling-imageen.
set -euo pipefail
cd "$(dirname "$0")"

if ! python3 -c "import ensurepip" >/dev/null 2>&1; then
    echo "Asennetaan python3-venv ja python3-pip (vaatii sudon)..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq python3-venv python3-pip
fi

[[ -d .venv ]] || python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

echo
echo "Valmis. Käynnistä koeputki:  ./mkdocs-spike/run.sh"
echo "Se muuntaa ../src -> docs/ ja tarjoilee sivuston porttiin 8001."
