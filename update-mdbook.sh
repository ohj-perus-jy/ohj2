#!/usr/bin/env bash

# Check if cargo is installed
if ! command -v cargo &> /dev/null
then
    echo "cargo could not be found, please install Rust and Cargo."
    exit 1
fi

cargo install mdbook@0.4.52 \
              mdbook-mermaid \
              mdbook-alerts \
              mdbook-katex

cargo install --locked --path ./preprocessors/rust/mdbook-codeblock-tabs