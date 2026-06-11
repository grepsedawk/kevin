#!/usr/bin/env python3
# Benchmark taken directly from caveman (https://github.com/JuliusBrussee/caveman, MIT).
"""Multi-turn session benchmark: total token use, Normal vs Kevin.

A single answer understates Kevin. The API is stateless, so the whole
transcript is re-sent every turn. Kevin's shorter replies keep the history
lean, so the savings compound: Kevin starts behind (it pays the voice-block
input tax up front) and crosses over as Normal's transcript bloats.

Runs one scripted conversation through both arms, feeding each model's own
replies back as history, and records per-turn and cumulative input+output
tokens so you can graph the crossover. Raw token counts, no caching (the
conservative read; caching only helps Kevin more on cost).

    KEVIN_BENCH_MODEL   model id (default: claude-opus-4-8)
    ANTHROPIC_API_KEY   required
"""

import json
import os
import time
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
VOICE = (ROOT / "kevin-voice.md").read_text()
PLAIN = "You are a helpful assistant."
MODEL = os.environ.get("KEVIN_BENCH_MODEL", "claude-opus-4-8")

TURNS = [
    "I need to add rate limiting to my API. What are my options?",
    "Let's go with the token bucket. How does it actually work?",
    "Show me a minimal implementation in Python.",
    "What happens under bursty traffic with that implementation?",
    "How would I make this work across multiple servers?",
    "Walk me through using Redis for the shared counter.",
    "What's the failure mode if Redis goes down?",
    "How do I return proper rate-limit headers to clients?",
    "Should I rate limit per-user or per-IP?",
    "Give me a checklist to take this to production.",
]


def call(client, system, messages):
    delays = [5, 10, 20, 30, 45]
    for attempt in range(len(delays) + 1):
        try:
            r = client.messages.create(
                model=MODEL, max_tokens=4096, system=system, messages=messages
            )
            text = "".join(b.text for b in r.content if b.type == "text")
            return r.usage.input_tokens, r.usage.output_tokens, text
        except anthropic.RateLimitError:
            if attempt == len(delays):
                raise
            time.sleep(delays[attempt])


def run(client, system, label):
    messages, rows, cum = [], [], 0
    for i, user in enumerate(TURNS, 1):
        messages.append({"role": "user", "content": user})
        inp, out, text = call(client, system, messages)
        messages.append({"role": "assistant", "content": text})
        cum += inp + out
        rows.append({"turn": i, "input": inp, "output": out, "total": inp + out, "cum": cum})
        print(f"  [{label}] turn {i}: in={inp:5} out={out:4} total={inp+out:5} cum={cum:6}")
    return rows


def main():
    client = anthropic.Anthropic()
    print("NORMAL arm:")
    normal = run(client, PLAIN, "normal")
    print("KEVIN arm:")
    kevin = run(client, VOICE, "kevin")

    print("\n=== cumulative total tokens ===")
    print(f"{'turn':>4} {'normal':>8} {'kevin':>8} {'delta':>8} {'kevin%':>8}")
    for n, k in zip(normal, kevin):
        d = k["cum"] - n["cum"]
        print(f"{n['turn']:>4} {n['cum']:>8} {k['cum']:>8} {d:>+8} {k['cum']/n['cum']*100:>7.0f}%")

    nt, kt = normal[-1]["cum"], kevin[-1]["cum"]
    print(f"\nSession total: normal {nt}, kevin {kt}  ({(kt-nt)/nt*100:+.0f}% total token use)")

    out = ROOT / "benchmarks" / "session-result.json"
    out.write_text(json.dumps({"model": MODEL, "turns": TURNS, "normal": normal, "kevin": kevin}, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
