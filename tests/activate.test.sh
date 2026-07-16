#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
hooks="$root/hooks/hooks.json"

out="$(
  CLAUDE_PLUGIN_ROOT="$root" \
    sh -c 'if [ -r "$CLAUDE_PLUGIN_ROOT/kevin-voice.md" ]; then cat "$CLAUDE_PLUGIN_ROOT/kevin-voice.md"; else printf "%s\n" "Use Kevin voice: fewest clear words, prose only."; fi'
)"

for needle in "KEVIN MODE ACTIVE" "Cut filler words" "Drop the voice for"; do
  grep -qF "$needle" <<<"$out"
done

if grep -qE '"(UserPromptSubmit|SubagentStart)"|node ' "$hooks"; then
  echo "FAIL: hooks must not require Node or run on prompts/subagents" >&2
  exit 1
fi

grep -qF '"matcher": "startup|resume|clear"' "$hooks"
grep -qF '"matcher": "compact"' "$hooks"

echo "PASS: runtime-free SessionStart hook emits Kevin rules"
