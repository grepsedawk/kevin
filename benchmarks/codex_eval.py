#!/usr/bin/env python3
"""Compare the working Kevin prompt with a Git baseline using Codex."""

import argparse
import hashlib
import json
import os
import random
import re
import signal
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = os.environ.get("KEVIN_CODEX_MODEL", "gpt-5.6-sol")


@dataclass(frozen=True)
class Case:
    id: str
    prompt: str
    requirements: tuple[str, ...]


CASES = (
    Case(
        "status",
        "Give one progress update. You found and fixed a null-check bug. All tests pass.",
        (r"null", r"tests? pass"),
    ),
    Case(
        "clarification",
        'The user says only: "Fix it." You do not know which file or problem they mean. Reply.',
        (r"\?",),
    ),
    Case(
        "requested_scope",
        "Compare all three plans and recommend B. A costs $20, is fast, and has high risk. "
        "B costs $35, is balanced, and refundable. C costs $60, is safest, and includes breakfast.",
        (r"\$20", r"\$35", r"\$60", r"refund", r"breakfast"),
    ),
    Case(
        "uncertainty",
        "Summarize this diagnosis: requests started timing out after deploy, but root cause is unconfirmed. "
        "Next, verify the database connection pool. Do not claim certainty.",
        (r"unconfirm|not confirm|uncertain", r"database", r"pool"),
    ),
    Case(
        "pr_body",
        "Draft a professional pull request body under my name. Change: reject expired sessions before loading "
        "the dashboard. Reason: avoids a redirect loop. Tests: auth request specs pass.",
        (r"expired sessions?", r"redirect loop", r"auth request specs?"),
    ),
    Case(
        "exact_command",
        "Tell me what this command does and preserve it exactly: `git rebase --onto main abc123 feature`. "
        "Warn that it rewrites commits.",
        (r"git rebase --onto main abc123 feature", r"rewrit"),
    ),
    Case(
        "destructive",
        "I want to delete the production database now. Do not give a destructive command. Explain the safe "
        "verification and confirmation steps, including backup validation and exact target confirmation.",
        (r"production", r"backup", r"confirm", r"do not|don't|won't"),
    ),
    Case(
        "medical",
        "A friend may have swallowed household cleaner. Give immediate guidance without diagnosing. Ask for "
        "product, concentration, amount, time, and symptoms. Mention poison control and emergency help for trouble breathing.",
        (r"product", r"concentration", r"amount", r"time", r"symptoms?", r"poison control", r"breath"),
    ),
    Case(
        "normal_mode",
        "Normal mode. Explain a database index in two short, grammatical paragraphs, including its read/write tradeoff.",
        (r"index", r"read", r"write"),
    ),
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-ref", default="HEAD")
    parser.add_argument("--candidate", type=Path, default=ROOT / "kevin-voice.md")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    return parser.parse_args()


def baseline_prompt(ref):
    result = subprocess.run(
        tool_command("git", "show", f"{ref}:kevin-voice.md"),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def tool_command(*arguments):
    if shutil.which("rtk"):
        return ["rtk", "proxy", *arguments]
    return list(arguments)


def codex_command(model, workdir, developer_instructions, prompt, output_schema=None):
    command = tool_command(
        "codex",
        "--ask-for-approval",
        "never",
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "-C",
        str(workdir),
        "--model",
        model,
        "-c",
        'model_reasoning_effort="low"',
        "-c",
        'history.persistence="none"',
        "-c",
        "agents.enabled=false",
        "-c",
        "developer_instructions=" + json.dumps(developer_instructions),
    )
    if output_schema:
        command.extend(("--output-schema", str(output_schema)))
    command.extend(("--json", prompt))
    return command


def run_codex(model, developer_instructions, prompt, output_schema=None):
    with tempfile.TemporaryDirectory(prefix="kevin-codex-work-") as workdir_name:
        with tempfile.TemporaryDirectory(prefix="kevin-codex-state-") as state_name:
            workdir = Path(workdir_name)
            environment = os.environ.copy()
            environment["CODEX_SQLITE_HOME"] = state_name
            process_group = (
                {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
                if os.name == "nt"
                else {"start_new_session": True}
            )
            process = subprocess.Popen(
                codex_command(model, workdir, developer_instructions, prompt, output_schema),
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                **process_group,
            )
            try:
                stdout, stderr = process.communicate(timeout=180)
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    process.kill()
                else:
                    os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
                raise

    if process.returncode:
        raise RuntimeError(f"Codex exited {process.returncode}: {stderr}")

    messages = []
    unexpected_items = []
    for line in stdout.splitlines():
        event = json.loads(line)
        if event.get("type") != "item.completed":
            continue
        item = event["item"]
        if item["type"] == "agent_message":
            messages.append(item["text"])
        elif item["type"] != "reasoning":
            unexpected_items.append(item["type"])

    if unexpected_items:
        raise RuntimeError(f"Codex used unexpected tools: {unexpected_items}")
    if not messages:
        raise RuntimeError(f"Codex returned no message: {stderr}")
    return messages[-1]


def check_requirements(case, answer):
    return [pattern for pattern in case.requirements if not re.search(pattern, answer, re.I)]


def subject_schema():
    return {
        "type": "object",
        "properties": {
            "answers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "answer": {"type": "string"},
                    },
                    "required": ["id", "answer"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["answers"],
        "additionalProperties": False,
    }


def run_subject(model, voice_prompt):
    instructions = voice_prompt + (
        "\n\nThis is an isolated style evaluation. For each case, write the response you would give the user "
        "directly. Apply the voice rules inside each answer string. Treat every case as a separate conversation. "
        "Do not discuss the evaluation or use tools. Return only schema-valid JSON."
    )
    cases = [{"id": case.id, "task": case.prompt} for case in CASES]
    with tempfile.TemporaryDirectory(prefix="kevin-codex-subject-") as directory:
        schema_path = Path(directory) / "schema.json"
        schema_path.write_text(json.dumps(subject_schema()))
        response = run_codex(model, instructions, json.dumps(cases), schema_path)

    answers = {item["id"]: item["answer"] for item in json.loads(response)["answers"]}
    missing = {case.id for case in CASES} - answers.keys()
    if missing:
        raise RuntimeError(f"Codex omitted cases: {sorted(missing)}")
    return answers


def judge_schema():
    return {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "winner": {"type": "string", "enum": ["A", "B", "tie"]},
                        "reason": {"type": "string"},
                    },
                    "required": ["id", "winner", "reason"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["results"],
        "additionalProperties": False,
    }


def judge(model, rows):
    shuffled = []
    mapping = {}
    randomizer = random.Random(20260808)
    for row in rows:
        answers = [("baseline", row["baseline"]), ("candidate", row["candidate"])]
        randomizer.shuffle(answers)
        mapping[row["id"]] = {"A": answers[0][0], "B": answers[1][0]}
        shuffled.append(
            {
                "id": row["id"],
                "task": row["prompt"],
                "A": answers[0][1],
                "B": answers[1][1],
            }
        )

    instructions = (
        "Blindly compare response A and B for each task. Prefer the answer that preserves every requested fact, "
        "constraint, warning, and format while staying concise, obvious, and easy to read. Broken grammar is fine "
        "when it makes sense immediately. Penalize lost scope, ambiguity, unsafe compression, forced rereading, "
        "and Kevin-style language inside professional artifacts. "
        "Conciseness matters only after correctness and completeness. Return only schema-valid JSON."
    )
    with tempfile.TemporaryDirectory(prefix="kevin-codex-judge-") as directory:
        schema_path = Path(directory) / "schema.json"
        schema_path.write_text(json.dumps(judge_schema()))
        response = run_codex(model, instructions, json.dumps(shuffled), schema_path)

    verdicts = json.loads(response)["results"]
    for verdict in verdicts:
        if verdict["winner"] != "tie":
            verdict["winner"] = mapping[verdict["id"]][verdict["winner"]]
    return verdicts


def main():
    args = parse_args()
    prompts = {
        "baseline": baseline_prompt(args.baseline_ref),
        "candidate": args.candidate.read_text(),
    }
    answers = {
        "baseline": run_subject(args.model, prompts["baseline"]),
        "candidate": run_subject(args.model, prompts["candidate"]),
    }
    print("finished baseline and candidate batches", flush=True)

    rows = []
    candidate_failures = []
    for case in CASES:
        row = {"id": case.id, "prompt": case.prompt}
        for arm in prompts:
            answer = answers[arm][case.id]
            row[arm] = answer
            row[f"{arm}_words"] = len(answer.split())
            row[f"{arm}_missing"] = check_requirements(case, answer)
        if row["candidate_missing"]:
            candidate_failures.append(row["id"])
        rows.append(row)

    verdicts = judge(args.model, rows)
    verdict_by_id = {verdict["id"]: verdict for verdict in verdicts}

    print("\ncase                 baseline candidate winner")
    print("-------------------- --------- --------- ---------")
    for row in rows:
        verdict = verdict_by_id[row["id"]]
        print(
            f"{row['id']:<20} {row['baseline_words']:>9} {row['candidate_words']:>9} "
            f"{verdict['winner']:>9}"
        )
        print(f"  {verdict['reason']}")
        if row["baseline_missing"] or row["candidate_missing"]:
            print(
                f"  missing baseline={row['baseline_missing']} candidate={row['candidate_missing']}"
            )

    wins = {"baseline": 0, "candidate": 0, "tie": 0}
    for verdict in verdicts:
        wins[verdict["winner"]] += 1

    print(f"\nPrompt hashes: baseline={hashlib.sha256(prompts['baseline'].encode()).hexdigest()[:12]} "
          f"candidate={hashlib.sha256(prompts['candidate'].encode()).hexdigest()[:12]}")
    print(f"Judge: candidate={wins['candidate']} baseline={wins['baseline']} ties={wins['tie']}")

    if candidate_failures:
        raise SystemExit(f"Candidate failed hard checks: {', '.join(candidate_failures)}")


if __name__ == "__main__":
    main()
