from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "kevin" / "SKILL.md"


def startup_prompt(path=SKILL):
    """Return SKILL.md as the SessionStart hook emits it: BOM, CRs and frontmatter stripped."""
    text = Path(path).read_text(encoding="utf-8-sig")
    lines = [line[:-1] if line.endswith("\r") else line for line in text.split("\n")]
    if lines[0] == "---" and "---" in lines[1:]:
        lines = lines[lines.index("---", 1) + 1:]
    return "\n".join(lines)
