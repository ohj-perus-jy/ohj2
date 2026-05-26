FROM mcr.microsoft.com/devcontainers/rust:1-1-bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        python3 \
    && rm -rf /var/lib/apt/lists/*

COPY preprocessors /tmp/preprocessors

ENV CARGO_TARGET_DIR=/tmp/cargo-target

RUN cargo install \
        mdbook@0.4.52 \
        mdbook-mermaid@0.16.2 \
        mdbook-alerts@0.8.0 \
        mdbook-katex@0.9.4 \
        mdbook-plantuml@0.8.0 \
        mdbook-inline-highlighting@1.0.0 \
    && cargo install \
        --git https://github.com/boozook/mdbook-svgbob.git \
        --rev 3431f100c08eeca8b132241d0c372ec0f4aed85b \
    && cargo install --path /tmp/preprocessors/rust/mdbook-codeblock-tabs \
    && mkdir -p /opt/mdbook-preprocessors \
    && cp -R /tmp/preprocessors/python /opt/mdbook-preprocessors/python \
    && printf '%s\n' \
        '#!/usr/bin/env bash' \
        'set -euo pipefail' \
        'export PYTHONPATH="/opt/mdbook-preprocessors/python${PYTHONPATH:+:$PYTHONPATH}"' \
        'exec python3 /opt/mdbook-preprocessors/python/accordion.py "$@"' \
        > /usr/local/bin/mdbook-accordion \
    && chmod +x /usr/local/bin/mdbook-accordion \
    && rm -rf "$CARGO_TARGET_DIR" /tmp/preprocessors /usr/local/cargo/registry /usr/local/cargo/git
