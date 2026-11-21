# kevin

Talk like Kevin from The Office. Fewest words that still carry the meaning.

> "Why waste time say lot word when few word do trick?"

Kevin Malone said that to defend the way he talks, and he had a point. Most of what an AI assistant types back at you is padding: throat-clearing, hedges, restating your own question, three sentences where one would do. Kevin is a portable [Agent Skill](https://agentskills.io) that strips it out. You get the answer, not the essay.

It governs prose only. Chat replies, summaries, explanations. It leaves code, commit messages, and anything that ships under a real name completely alone.

## Before / after

<a href="examples.md">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/before-after-dark.png">
    <img alt="Same answer, fewer words. Which would you rather read?" src="docs/before-after-light.png">
  </picture>
</a>

Real captures, same prompt with and without Kevin. [See all 30.](examples.md)

What Kevin won't touch: code, commit messages, PR descriptions, and security or destructive-action warnings stay in full, plain English. Compression is for the chat, not for the things you read back later under your name.

## Why this exists, and why it isn't really about tokens

Every compression tool in this space sells token savings. Kevin saves tokens too (numbers below), but that's not the reason to run it.

Tokens are cheap. A long-winded Opus answer costs a fraction of a cent. The resource you're actually spending is your own attention, reading the same preamble for the hundredth time today. That cost never shows up on an invoice, which is exactly why it's the one worth cutting. Kevin optimizes for your reading time. The API bill is an afterthought.

"Found two bug." is clear and funny. Kevin bends grammar to cut words, never to add them, whenever the result stays obvious, but never crushes words together. Every requested option, constraint, and decision-relevant caveat stays. It doesn't add unasked coverage, repeat the verdict, or tack on a punchline. Replies come out concise on the first pass.

The token savings are a side effect. A good one.

## Easier to read, not just shorter

Shorter only counts if nothing important falls out, so Kevin is also checked against a plain assistant on 24 held-out cases (status updates, dense summaries, safety warnings, emails, mode switches) with Claude Opus 5.5 and a blind judge from another model family. Kevin answers took noticeably less effort to read (a quick skim instead of a normal read), used about a third fewer words, and dropped fewer facts and caveats than the plain assistant did. That comparison ran on 0.3.2. Against 0.3.2, 0.4.0 took less effort to read and used about 11% fewer words on Claude Opus 5.5 across 20 cases written after the earlier versions were picked, with about the same number of missed facts. When Kevin needs something from you, an approval or a missing value, it goes on its own line at the end.

## The savings

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/savings-dark.png">
  <img alt="Output tokens per answer on Opus, Sonnet, and Haiku 5.5: Kevin cuts 68 to 81%" src="docs/savings-light.png">
</picture>

## It compounds over a chat

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/compounding-dark.png">
  <img alt="Total tokens over a 10-turn chat on Opus 5.5: Kevin uses 50% fewer by turn 10" src="docs/compounding-light.png">
</picture>

A single answer understates it. The API is stateless, so the whole transcript rides along on every turn. Kevin's shorter replies keep that history lean, and the gap widens turn over turn. These are raw token counts from one uncached conversation.

## One skill, any compatible agent

[`skills/kevin/SKILL.md`](skills/kevin/SKILL.md) is the single source of truth. It follows the open Agent Skills format: standard YAML metadata plus Markdown instructions, with no scripts, network calls, or dependencies.

Install that folder using any agent's normal skill workflow. Invoke `kevin` explicitly when you want the most predictable activation. The exact syntax and install location belong to the host; common examples are below.

Turn it off by saying "stop kevin" or "normal mode." Turn it back on with "start kevin" or "kevin mode." The latest explicit choice wins while those instructions remain in context.

Agent Skills standardizes the package, not every host's lifecycle. A standard skill may load only when selected and may need to be invoked again after a new session, compaction, or subagent handoff. Kevin's optional plugin hooks preserve the old always-on behavior in hosts that support those hooks.

## Install

### Portable skill

Install [`skills/kevin/`](skills/kevin/) with your agent's documented Agent Skills flow. The folder can be copied, symlinked, or packaged without rewriting it.

The cross-harness [`skills` CLI](https://www.skills.sh/docs/cli) can discover the standard repository layout and install Kevin for the agents you select:

```sh
npx skills add grepsedawk/kevin --skill kevin
```

The CLI is optional; review it and the skill before running third-party installers.

- [Codex](https://developers.openai.com/codex/build-skills) discovers repository skills under `.agents/skills/` and user skills under `~/.agents/skills/`. Invoke with `$kevin`.
- [Claude Code](https://code.claude.com/docs/en/skills) discovers project skills under `.claude/skills/` and user skills under `~/.claude/skills/`. Invoke with `/kevin`.
- Other Agent Skills-compatible hosts use the same `SKILL.md`; follow that host's discovery or upload instructions.

Review third-party skills before installing them. This one contains instructions only.

### Plugin compatibility

The existing marketplace install remains available for Claude Code and Codex. It bundles the same portable skill plus two `SessionStart` hooks for startup/resume/clear and post-compaction reload. The hooks inject the skill's instructions without its YAML frontmatter, which the model never needed.

Add the marketplace:

```
/plugin marketplace add grepsedawk/kevin
```

Then install the plugin:

```
/plugin install kevin@kevin
```

For Codex:

Add the marketplace and install the plugin:

```sh
codex plugin marketplace add grepsedawk/kevin
codex plugin add kevin@kevin
```

In Codex, open `/hooks`, review and trust both Kevin `SessionStart` hooks, then start a new thread. Enabling the plugin does not trust its hooks. Claude Code applies its own plugin and hook permission flow.

After an update, check `/hooks` again. Codex tracks trust for both hook definitions and plugin contents, so a voice-prompt change can require fresh approval even when the hook command is unchanged. Hooks marked for review are skipped.

## Benchmarks

Reproduce the charts:

```
python3 -m pip install anthropic
ANTHROPIC_API_KEY=... python3 benchmarks/run.py        # per-answer savings
ANTHROPIC_API_KEY=... python3 benchmarks/session.py    # 10-turn compounding
ANTHROPIC_API_KEY=... python3 benchmarks/examples.py   # rewrites examples.md
python3 benchmarks/charts.py                           # renders docs/*.png (Chrome)
```

Every script sends the same text the plugin hook injects: the skill without its frontmatter. `run.py` reports the output-token delta split into prose and code buckets for each model in `KEVIN_BENCH_MODELS` (default Opus 5.5, Sonnet 5.5, Haiku 5.5; `KEVIN_BENCH_MODEL` also works for one model), with `KEVIN_BENCH_TRIALS` trials per prompt (default 5). `session.py` runs one scripted conversation through both arms and records per-turn and cumulative tokens; `examples.py` captures one Normal and one Kevin answer per question. Set `KEVIN_BENCH_MODEL` to change the model for those two. Results land in `benchmarks/data/`, and `charts.py` renders the light and dark PNGs from that data with headless Chrome.

Test prompt quality with Codex while editing. Choose the model you actually use:

```sh
python3 benchmarks/codex_eval.py --model gpt-6-astra
```

The model is required, either through `--model` or `KEVIN_CODEX_MODEL`. The judge uses the same model unless you pass `--judge-model`.

The evaluator compares the working skill with `HEAD` (and understands the pre-0.3 `kevin-voice.md` path). Identical prompts fail before any model calls. After committing, choose an older baseline:

```sh
python3 benchmarks/codex_eval.py --model gpt-6-astra --baseline-ref HEAD^
```

Three batched calls generate both sets of answers and a blinded comparison. Cases cover concise updates, progress and blocked messages, recommendations, requested scope, mixed validation results, professional artifacts, and safety. The judge checks meaning separately from style. Clear broken grammar is allowed; polish and unasked detail earn no extra credit. The subject also gets typical host guidance ("be concise, use plain language"), and chat cases fail if the answer slips back to assistant helper verbs like "I'll" or "I'm."

A run passes only when the candidate preserves the required meaning and wins more comparisons than it loses. Ties alone don't establish an improvement. Each run saves the prompts, hashes, models, answers, checks, and verdicts in an ignored JSON report under `benchmarks/results/`, including failed comparisons. Use `--output` to choose another path. Inspect the saved answers; one judge run is a screening result, not proof of consistent improvement.

Run the local checks without model calls:

```sh
bash tests/activate.test.sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

## License

MIT. See [LICENSE](LICENSE).
