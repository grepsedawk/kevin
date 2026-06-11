#!/usr/bin/env python3
# Benchmark taken directly from caveman (https://github.com/JuliusBrussee/caveman, MIT).
"""Measure whether the Kevin voice saves tokens or only buys cognitive overhead.

For each prompt, call the API twice: once with a plain assistant system prompt,
once with the Kevin voice as the system prompt. Count input/output tokens,
median over N trials. Report the output-token delta split by bucket (prose vs
code) plus the fixed input "tax" of injecting the voice block.

The honest read: Kevin only governs prose, so savings (if any) show up in the
prose bucket. Code output it cannot shrink. And the voice block costs input
tokens every session whether it saves output or not.

    KEVIN_BENCH_MODEL   model id (default: claude-haiku-4-5-20251001)
    KEVIN_BENCH_TRIALS  trials per prompt (default: 5)
    ANTHROPIC_API_KEY   required
"""

import json
import os
import statistics
import time
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
VOICE = (ROOT / "kevin-voice.md").read_text()
PROMPTS = json.loads((Path(__file__).parent / "prompts.json").read_text())["prompts"]

PLAIN_SYSTEM = "You are a helpful assistant."
MODEL = os.environ.get("KEVIN_BENCH_MODEL", "claude-haiku-4-5-20251001")
TRIALS = int(os.environ.get("KEVIN_BENCH_TRIALS", "5"))


def call(client, system, prompt):
    delays = [5, 10, 20, 30]
    for attempt in range(len(delays) + 1):
        try:
            r = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
            return r.usage.input_tokens, r.usage.output_tokens
        except anthropic.RateLimitError:
            if attempt == len(delays):
                raise
            time.sleep(delays[attempt])


def main():
    client = anthropic.Anthropic()
    buckets = {}
    input_tax = []

    for p in PROMPTS:
        plain_out, kevin_out = [], []
        for _ in range(TRIALS):
            pi, po = call(client, PLAIN_SYSTEM, p["prompt"])
            ki, ko = call(client, VOICE, p["prompt"])
            plain_out.append(po)
            kevin_out.append(ko)
        mp, mk = statistics.median(plain_out), statistics.median(kevin_out)
        input_tax.append(ki - pi)  # ~ size of the voice block, stable across prompts
        buckets.setdefault(p["bucket"], {"plain": [], "kevin": []})
        buckets[p["bucket"]]["plain"].append(mp)
        buckets[p["bucket"]]["kevin"].append(mk)
        print(f"  {p['bucket']:5}  plain={mp:4.0f}  kevin={mk:4.0f}  {p['prompt'][:48]}")

    print("\n=== Kevin token verdict ===")
    for bucket, r in buckets.items():
        plain, kevin = statistics.median(r["plain"]), statistics.median(r["kevin"])
        delta = (kevin - plain) / plain * 100 if plain else 0
        print(f"{bucket:5} output: plain {plain:4.0f} -> kevin {kevin:4.0f}  ({delta:+.0f}%)")

    tax = statistics.median(input_tax)
    print(f"\nInput tax of the voice block: ~{tax:.0f} tokens, injected once per session.")
    print("Verdict: Kevin saves tokens only if prose output drops by more than the")
    print("input tax amortized over a session. If prose delta is flat or positive,")
    print("it is cognitive overhead, not token savings.")


if __name__ == "__main__":
    main()
