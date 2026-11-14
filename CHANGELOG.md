# Changelog

## 0.3.1 - 2026-11-14

- Make Kevin's speech the default again in real sessions. Progress updates and final answers had drifted back to plain assistant prose even with the skill loaded.
- Add a Voice section with examples for progress updates, blockers, and final answers.
- State that instructions to be concise or plain do not turn Kevin off, and that "Kevin, ..." addresses the assistant.
- Stop the skill description from implying Kevin applies only on explicit request.
- Evaluate under realistic host guidance and fail candidates whose chat answers lose the voice.

## 0.3.0 - 2026-10-30

- Make `skills/kevin/SKILL.md` the canonical, open Agent Skills package.
- Support discovery by the cross-harness `skills` CLI through the standard `skills/<name>/SKILL.md` layout.
- Keep Claude Code and Codex plugin installs as compatibility wrappers around the same skill.
- Document portable installation and honest host-specific activation and persistence limits.
- Keep concise chat readable: never concatenate words, and preserve professional or externally attributed writing.
- Point hooks, benchmarks, and tests at the shared skill.

## 0.2.1 - 2026-10-30

- Preserve requested meaning, uncertainty, validation boundaries, artifacts, and safety guidance while shortening chat prose.
- Add Codex plugin support and prompt-quality evaluation.
