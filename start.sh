#!/usr/bin/env bash
set -euo pipefail

# Starting port: bash start.sh 4000  or  PORT=4000 bash start.sh
start_port="${1:-${PORT:-3000}}"
max_tries=20

busy_in_container() {
  if command -v ss >/dev/null 2>&1; then
    ss -ltnH "sport = :$1" | grep -q .
  else
    timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/$1" 2>/dev/null
  fi
}

# The browser runs on the host, so VS Code can only forward the container
# port to the same number on the host if it is free there. Peek through
# host.docker.internal; if it does not exist (plain Linux docker), skip this.
busy_on_host() {
  getent hosts host.docker.internal >/dev/null 2>&1 || return 1
  timeout 1 bash -c "exec 3<>/dev/tcp/host.docker.internal/$1" 2>/dev/null
}

port=""
for (( p = start_port; p < start_port + max_tries; p++ )); do
  if busy_in_container "$p"; then
    echo "Port $p is busy in the container, trying the next one..."
  elif busy_on_host "$p"; then
    echo "Port $p is busy on the host, trying the next one..."
  else
    port="$p"
    break
  fi
done

if [[ -z $port ]]; then
  echo "No free port found in range $start_port-$(( start_port + max_tries - 1 ))." >&2
  exit 1
fi

echo "Serving the book on port $port -> http://localhost:$port"
mdbook serve --hostname 0.0.0.0 --port "$port" --open
