#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
hooks="$root/hooks/hooks.json"
voice="$root/kevin-voice.md"

hook_command="$(python3 - "$hooks" <<'PY'
import json
import sys

with open(sys.argv[1]) as source:
    hooks = json.load(source)["hooks"]["SessionStart"]

print(hooks[0]["hooks"][0]["command"])
PY
)"

out="$(CLAUDE_PLUGIN_ROOT="$root" PATH="/usr/bin:/bin" sh -c "$hook_command")"

diff -u "$voice" <(printf '%s\n' "$out")

for needle in "KEVIN MODE DEFAULT: ACTIVE" "correctness and safety" "Answer every explicit part" "Grammar may break" "Drop the voice for"; do
  grep -qF "$needle" <<<"$out"
done

grep -qF '"Me fix."' "$voice"
grep -qF '"No understand. Say more?"' "$voice"

fallback="$(CLAUDE_PLUGIN_ROOT="$root/missing" PATH="/usr/bin:/bin" sh -c "$hook_command")"
grep -qF "fewest clear words" <<<"$fallback"

if grep -qE '"(UserPromptSubmit|SubagentStart)"|node ' "$hooks"; then
  echo "FAIL: hooks must not require Node or run on prompts/subagents" >&2
  exit 1
fi

grep -qF '"matcher": "startup|resume|clear"' "$hooks"
grep -qF '"matcher": "compact"' "$hooks"

python3 - "$hooks" "$root/.codex-plugin/plugin.json" "$root/.claude-plugin/plugin.json" <<'PY'
import json
import sys

with open(sys.argv[1]) as source:
    session_hooks = json.load(source)["hooks"]["SessionStart"]

compact = next(hook for hook in session_hooks if hook["matcher"] == "compact")
assert "statusMessage" not in compact["hooks"][0]
assert len({hook["hooks"][0]["command"] for hook in session_hooks}) == 1

versions = []
for path in sys.argv[2:]:
    with open(path) as source:
        versions.append(json.load(source)["version"])

assert len(set(versions)) == 1, versions
PY

echo "PASS: runtime-free SessionStart hook emits Kevin rules"
