#!/usr/bin/env bash

# Check if cargo is installed
if ! command -v cargo &> /dev/null
then
    echo "cargo could not be found, please install Rust and Cargo."
    exit 1
fi

export CARGO_TARGET_DIR="$HOME/.cargo-target-cache"

cargo install mdbook@0.5.2 \
              mdbook-mermaid@0.17.0 \
              mdbook-katex@0.10.0-alpha \
              mdbook-plantuml@2.0.0 \
              mdbook-inline-highlighting@2.0.0

# mdbook-alerts is replaced by a Python preprocessor (preprocessors/python/alerts.py)

cargo install --path ./preprocessors/rust/mdbook-codeblock-tabs
cargo install --path ./preprocessors/rust/mdbook-svgbob2