#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
hooks="$root/hooks/hooks.json"
voice="$root/skills/kevin/SKILL.md"

if [ -e "$root/kevin-voice.md" ] || [ -e "$root/hooks/session-start.md" ]; then
  echo "FAIL: a second prompt file duplicates the canonical portable skill" >&2
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

body="$(python3 -c 'import sys; print(open(sys.argv[1]).read().split("\n---\n", 1)[1], end="")' "$voice")"
diff -u <(printf '%s\n' "$body") <(printf '%s\n' "$out")

if grep -qF "name: kevin" <<<"$out"; then
  echo "FAIL: hook output still carries the skill frontmatter" >&2
  exit 1
fi

for needle in "starts active" "stop kevin" "normal mode" "start kevin" "kevin mode" "few word do trick" "Never concatenate words" "correctness and safety" "Answer every explicit part" "verification results" "externally attributed" "goes last" "Drop the voice" "destructive or irreversible"; do
  grep -qF "$needle" <<<"$out"
done

grep -qF 'few word do trick' "$voice"
grep -qF '"Fix what? Which file?"' "$voice"
grep -qF "Never concatenate words" "$voice"
grep -qF "externally attributed" "$voice"

fallback="$(CLAUDE_PLUGIN_ROOT="$root/missing" PATH="/usr/bin:/bin" sh -c "$hook_command")"
grep -qF "fewest clear words" <<<"$fallback"

fixtures="$(mktemp -d)"
trap 'rm -rf "$fixtures"' EXIT

fixture() {
  mkdir -p "$fixtures/$1/skills/kevin"
  printf '%b' "$2" > "$fixtures/$1/skills/kevin/SKILL.md"
  printf '%b' "$3" > "$fixtures/$1.expected"
}

real_body="$fixtures/real.expected"
printf '%s\n' "$body" > "$real_body"
mkdir -p "$fixtures/crlf/skills/kevin" "$fixtures/bom/skills/kevin"
sed $'s/$/\r/' "$voice" > "$fixtures/crlf/skills/kevin/SKILL.md"
cp "$real_body" "$fixtures/crlf.expected"
{ printf '\357\273\277'; cat "$voice"; } > "$fixtures/bom/skills/kevin/SKILL.md"
cp "$real_body" "$fixtures/bom.expected"
fixture plain '# Title\n\nBody text.\n' '# Title\n\nBody text.\n'
fixture rules '# Title\n\n---\n\nMiddle.\n\n---\n\nEnd.\n' '# Title\n\n---\n\nMiddle.\n\n---\n\nEnd.\n'
fixture empty_frontmatter '---\n---\n# Title\n\n---\n\nAfter rule.\n' '# Title\n\n---\n\nAfter rule.\n'
fixture unclosed '---\n# Title\n\nNo closing fence.\n' '---\n# Title\n\nNo closing fence.\n'
fixture crlf_bom_no_frontmatter '\357\273\277# Title\r\n\r\nBody.\r\n' '# Title\n\nBody.\n'
fixture frontmatter_only_eof '---\nname: x\n---' ''

cases=(crlf bom plain rules empty_frontmatter unclosed crlf_bom_no_frontmatter frontmatter_only_eof)
for case in "${cases[@]}"; do
  CLAUDE_PLUGIN_ROOT="$fixtures/$case" PATH="/usr/bin:/bin" sh -c "$hook_command" > "$fixtures/$case.out"
  if ! cmp -s "$fixtures/$case.expected" "$fixtures/$case.out"; then
    echo "FAIL: hook output for $case fixture" >&2
    diff -u "$fixtures/$case.expected" "$fixtures/$case.out" >&2 || true
    exit 1
  fi
done

CLAUDE_PLUGIN_ROOT="$root" PATH="/usr/bin:/bin" sh -c "$hook_command" > "$fixtures/real.out"
python3 - "$root/benchmarks" "$fixtures" "$root" "${cases[@]}" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from voice import startup_prompt

fixtures, root = Path(sys.argv[2]), Path(sys.argv[3])
assert startup_prompt() == (fixtures / "real.out").read_text(), "voice.py differs from hook on SKILL.md"
for case in sys.argv[4:]:
    got = startup_prompt(fixtures / case / "skills" / "kevin" / "SKILL.md")
    assert got == (fixtures / f"{case}.expected").read_text(), f"voice.py differs from hook on {case}"
PY

if grep -qE '"(UserPromptSubmit|SubagentStart)"|node ' "$hooks"; then
  echo "FAIL: hooks must not require Node or run on prompts/subagents" >&2
  exit 1
fi

grep -qF '"matcher": "startup|resume|clear"' "$hooks"
grep -qF '"matcher": "compact"' "$hooks"

python3 - "$hooks" "$fixtures" "${cases[@]}" <<'PY'
import json
import re
import sys
from pathlib import Path

with open(sys.argv[1]) as source:
    windows = json.load(source)["hooks"]["SessionStart"][0]["hooks"][0]["commandWindows"]
pattern = re.search(r"-replace '([^']+)'", windows).group(1).replace(r"\z", r"\Z")
fixtures = Path(sys.argv[2])
for case in sys.argv[3:]:
    with open(fixtures / case / "skills" / "kevin" / "SKILL.md", encoding="utf-8-sig", newline="") as source:
        raw = source.read()
    got = re.sub(pattern, "", raw, count=1).replace("\r\n", "\n")
    assert got == (fixtures / f"{case}.expected").read_text(), f"Windows regex mishandles {case}"
PY

python3 - "$hooks" "$root/.codex-plugin/plugin.json" "$root/.claude-plugin/plugin.json" "$voice" <<'PY'
import json
import re
import sys

with open(sys.argv[1]) as source:
    session_hooks = json.load(source)["hooks"]["SessionStart"]

compact = next(hook for hook in session_hooks if hook["matcher"] == "compact")
assert "statusMessage" not in compact["hooks"][0]
assert len({hook["hooks"][0]["command"] for hook in session_hooks}) == 1
windows = {hook["hooks"][0]["commandWindows"] for hook in session_hooks}
assert len(windows) == 1
windows = windows.pop()
assert windows.count("skills\\kevin\\SKILL.md") == 2
pattern = re.search(r"-replace '([^']+)'", windows).group(1).replace(r"\z", r"\Z")
skill = open(sys.argv[4]).read()
assert re.sub(pattern, "", skill, count=1) == skill.split("\n---\n", 1)[1]

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
