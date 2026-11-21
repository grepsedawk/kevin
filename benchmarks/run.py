#!/usr/bin/env python3
# Benchmark taken directly from caveman (https://github.com/JuliusBrussee/caveman, MIT).
"""Measure whether the Kevin voice saves tokens or only buys cognitive overhead.

For each prompt, call the API twice: once with a plain assistant system prompt,
once with the Kevin voice as the system prompt. Count input/output tokens,
median over N trials. Report the output-token delta split by bucket (prose vs
code) plus the fixed input "tax" of injecting the voice block.

Kevin leaves code itself alone, so savings on code prompts come from the prose
around the code. The voice block also costs input tokens on every request
whether it saves output or not.

    KEVIN_BENCH_MODELS  comma-separated model ids
                        (default: claude-opus-5-5,claude-sonnet-5-5,claude-haiku-5-5)
    KEVIN_BENCH_MODEL   one model id, used when KEVIN_BENCH_MODELS is unset
    KEVIN_BENCH_TRIALS  trials per prompt (default: 5)
    ANTHROPIC_API_KEY   required
"""

import json
import os
import statistics
from pathlib import Path

import anthropic

from voice import startup_prompt

VOICE = startup_prompt()
PROMPTS = json.loads((Path(__file__).parent / "prompts.json").read_text())["prompts"]

PLAIN_SYSTEM = "You are a helpful assistant."
MODELS = os.environ.get(
    "KEVIN_BENCH_MODELS",
    os.environ.get("KEVIN_BENCH_MODEL", "claude-opus-5-5,claude-sonnet-5-5,claude-haiku-5-5"),
).split(",")
TRIALS = int(os.environ.get("KEVIN_BENCH_TRIALS", "5"))


def call(client, model, system, prompt):
    r = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in r.content if b.type == "text")
    return r.usage.input_tokens, r.usage.output_tokens, len(text.split())


def bench(client, model):
    buckets = {}
    input_tax = []
    print(f"\n## {model}")
    for p in PROMPTS:
        plain_out, kevin_out, plain_words, kevin_words = [], [], [], []
        for _ in range(TRIALS):
            pi, po, pw = call(client, model, PLAIN_SYSTEM, p["prompt"])
            ki, ko, kw = call(client, model, VOICE, p["prompt"])
            plain_out.append(po)
            kevin_out.append(ko)
            plain_words.append(pw)
            kevin_words.append(kw)
        input_tax.append(ki - pi)
        b = buckets.setdefault(p["bucket"], {"plain": [], "kevin": [], "plain_words": [], "kevin_words": []})
        b["plain"].append(statistics.median(plain_out))
        b["kevin"].append(statistics.median(kevin_out))
        b["plain_words"].append(statistics.median(plain_words))
        b["kevin_words"].append(statistics.median(kevin_words))
        print(f"  {p['bucket']:5}  plain={b['plain'][-1]:4.0f}  kevin={b['kevin'][-1]:4.0f}  {p['prompt'][:48]}")

    summary = {}
    for bucket, r in buckets.items():
        summary[bucket] = {key: statistics.median(values) for key, values in r.items()}
        plain, kevin = summary[bucket]["plain"], summary[bucket]["kevin"]
        delta = (kevin - plain) / plain * 100 if plain else 0
        print(f"{bucket:5} output: plain {plain:4.0f} -> kevin {kevin:4.0f}  ({delta:+.0f}%)")
    tax = statistics.median(input_tax)
    print(f"Input tax of the voice block: ~{tax:.0f} tokens added to every request.")
    return {"model": model, "trials": TRIALS, "input_tax": tax, "buckets": summary}


def main():
    client = anthropic.Anthropic(max_retries=6)
    results = [bench(client, model) for model in MODELS]
    out = Path(__file__).parent / "data" / "savings.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2) + "\n")
    print("wrote", out)
    print("Verdict: Kevin saves tokens only if output drops by more than the input")
    print("tax each request pays (less with prompt caching). If the prose delta is")
    print("flat or positive, it is cognitive overhead, not token savings.")


if __name__ == "__main__":
    main()
