#!/usr/bin/env bash

./update-mdbook.sh
python3 preprocessors/python/update_bootstrap_icons.py
mdbook serve --hostname 0.0.0.0 --port 3000 --open