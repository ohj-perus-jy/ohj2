#!/usr/bin/env bash

# Check if cargo is installed
if ! command -v cargo &> /dev/null
then
    echo "cargo could not be found, please install Rust and Cargo."
    exit 1
fi

cargo install mdbook \
              mdbook-mermaid \
              mdbook-alerts \
              mdbook-katex