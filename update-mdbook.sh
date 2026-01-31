#!/usr/bin/env bash

# Check if cargo is installed
if ! command -v cargo &> /dev/null
then
    echo "cargo could not be found, please install Rust and Cargo."
    exit 1
fi

export CARGO_TARGET_DIR="$HOME/.cargo-target-cache"

cargo install mdbook@0.4.52 \
              mdbook-mermaid@0.16.2 \
              mdbook-alerts@0.8.0 \
              mdbook-katex@0.9.4 \
              mdbook-plantuml@0.8.0 \
              mdbook-inline-highlighting@1.0.0

cargo install --git https://github.com/boozook/mdbook-svgbob.git#3431f100c08eeca8b132241d0c372ec0f4aed85b

cargo install --path ./preprocessors/rust/mdbook-codeblock-tabs