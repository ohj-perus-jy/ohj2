#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

cargo install --path "$SCRIPT_DIR/preprocessors/rust/mdbook-codeblock-tabs"

mkdir -p "$HOME/.cargo/bin"
cat > "$HOME/.cargo/bin/mdbook-accordion" <<EOF
#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$SCRIPT_DIR/preprocessors/python\${PYTHONPATH:+:\$PYTHONPATH}"
exec python3 "$SCRIPT_DIR/preprocessors/python/accordion.py" "\$@"
EOF
chmod +x "$HOME/.cargo/bin/mdbook-accordion"
