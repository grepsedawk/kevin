#!/usr/bin/env python3
"""Regenerate examples.md: one real capture per question, Normal versus Kevin.

    KEVIN_BENCH_MODEL   model id (default: claude-opus-5-5)
    ANTHROPIC_API_KEY   required
"""

import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

from voice import startup_prompt

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = json.loads((Path(__file__).parent / "examples.json").read_text())["questions"]
MODEL = os.environ.get("KEVIN_BENCH_MODEL", "claude-opus-5-5")
PLAIN = "You are a helpful assistant."


def answer(client, system, question):
    r = client.messages.create(
        model=MODEL, max_tokens=8192, system=system, messages=[{"role": "user", "content": question}]
    )
    return "".join(b.text for b in r.content if b.type == "text").strip()


def quote(text):
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def main():
    client = anthropic.Anthropic(max_retries=6)
    voice = startup_prompt()
    jobs = [(q, system) for q in QUESTIONS for system in (PLAIN, voice)]
    with ThreadPoolExecutor(8) as pool:
        answers = list(pool.map(lambda job: answer(client, job[1], job[0]), jobs))

    parts = [
        "# Examples",
        "",
        f"Real captures from `benchmarks/examples.py` on `{MODEL}`. Same question, a default assistant "
        "(**Normal**, system prompt \"You are a helpful assistant.\") versus the Kevin voice. "
        "One sample each, verbatim. Nothing here is edited.",
        "",
        "Back to the [README](README.md).",
    ]
    for i, question in enumerate(QUESTIONS):
        normal, kevin = answers[2 * i], answers[2 * i + 1]
        parts += [
            "", f"## {question}", "",
            f"**Normal** ({len(normal.split())} words)", "", quote(normal), "",
            f"**Kevin** ({len(kevin.split())} words)", "", quote(kevin), "", "---",
        ]
    (ROOT / "examples.md").write_text("\n".join(parts) + "\n")
    print("wrote", ROOT / "examples.md")


if __name__ == "__main__":
    main()
