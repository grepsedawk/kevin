#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
hooks="$root/hooks/hooks.json"
voice="$root/skills/kevin/SKILL.md"

if [ -e "$root/kevin-voice.md" ]; then
  echo "FAIL: kevin-voice.md duplicates the canonical portable skill" >&2
  exit 1
fi

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

for needle in "name: kevin" "correctness and safety" "Answer every explicit part" "clipped grammar" "Drop the voice"; do
  grep -qF "$needle" <<<"$out"
done

grep -qF '"Me fix."' "$voice"
grep -qF '"No understand. Say more?"' "$voice"
grep -qF "Never concatenate words" "$voice"
grep -qF "externally attributed" "$voice"

fallback="$(CLAUDE_PLUGIN_ROOT="$root/missing" PATH="/usr/bin:/bin" sh -c "$hook_command")"
grep -qF "fewest clear words" <<<"$fallback"

if grep -qE '"(UserPromptSubmit|SubagentStart)"|node ' "$hooks"; then
  echo "FAIL: hooks must not require Node or run on prompts/subagents" >&2
  exit 1
fi

grep -qF '"matcher": "startup|resume|clear"' "$hooks"
grep -qF '"matcher": "compact"' "$hooks"

python3 - "$hooks" "$root/.codex-plugin/plugin.json" "$root/.claude-plugin/plugin.json" "$voice" <<'PY'
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
        if path.endswith(".json"):
            versions.append(json.load(source)["version"])
        else:
            for line in source:
                if line.strip().startswith("version:"):
                    versions.append(line.split(":", 1)[1].strip().strip('"'))
                    break

assert len(set(versions)) == 1, versions
PY

echo "PASS: portable skill and runtime-free SessionStart hook emit Kevin rules"
