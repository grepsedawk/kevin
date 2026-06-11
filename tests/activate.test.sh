#!/usr/bin/env bash
# Smoke test: the SessionStart hook emits the voice rules.
set -euo pipefail

out="$(node "$(dirname "$0")/../hooks/kevin-activate.js")"

fail=0
for needle in "KEVIN MODE ACTIVE" "Cut filler words" "Swap table" "Drop the voice for"; do
  if ! grep -qF "$needle" <<<"$out"; then
    echo "FAIL: hook output missing: $needle"
    fail=1
  fi
done

if [ "$fail" -eq 0 ]; then
  echo "PASS: activate hook emits the voice rules"
fi
exit "$fail"
