import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "benchmarks" / "codex_eval.py"
SPEC = importlib.util.spec_from_file_location("codex_eval", MODULE_PATH)
codex_eval = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(codex_eval)


class CodexEvalTest(unittest.TestCase):
    def args(self, candidate, output):
        return Namespace(
            baseline_ref="HEAD",
            candidate=Path(candidate),
            model="subject-model",
            judge_model="judge-model",
            output=Path(output),
        )

    def answers(self, prefix):
        answers = {case.id: f"{prefix} answer for {case.id}" for case in codex_eval.CASES}
        answers["exact_command"] = codex_eval.EXACT_REBASE_COMMAND
        answers["normal_mode"] = "An index speeds reads.\n\nIt adds write work."
        answers["destructive"] = "Validate the backup and confirm the exact target first."
        return answers

    def verdicts(self, winner="candidate", candidate_passed=True):
        return [
            {
                "id": case.id,
                "winner": winner,
                "reason": "stub verdict",
                "semantic": {
                    "baseline": {"passed": True, "misses": []},
                    "candidate": {
                        "passed": candidate_passed,
                        "misses": [] if candidate_passed else ["requested recommendation B"],
                    },
                },
            }
            for case in codex_eval.CASES
        ]

    def evaluate(self, *arguments, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return codex_eval.evaluate(*arguments, **kwargs)

    def test_model_is_required(self):
        with patch.dict("os.environ", {}, clear=True), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                codex_eval.parse_args([])
        self.assertEqual(error.exception.code, 2)

    def test_identical_prompts_fail_before_subject_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.md"
            candidate.write_text("same prompt")
            calls = []
            with self.assertRaisesRegex(RuntimeError, "identical"):
                self.evaluate(
                    self.args(candidate, Path(directory) / "report.json"),
                    baseline_loader=lambda _ref: "same prompt",
                    subject_runner=lambda *arguments: calls.append(arguments),
                )
        self.assertEqual(calls, [])

    def test_positive_pass_records_word_totals_and_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.md"
            output = Path(directory) / "report.json"
            candidate.write_text("candidate prompt")
            report = self.evaluate(
                self.args(candidate, output),
                baseline_loader=lambda _ref: "baseline prompt",
                subject_runner=lambda _model, prompt: self.answers(
                    "baseline" if prompt == "baseline prompt" else "candidate"
                ),
                judge_runner=lambda _model, _rows: self.verdicts(),
            )
        self.assertTrue(report["gate"]["passed"])
        self.assertEqual(report["runtime"]["reasoning_effort"], "low")
        self.assertIn("percent_delta", report["totals"]["words"])
        self.assertEqual(len(report["cases"]), 14)

    def test_semantic_failure_rejects_keyword_false_positive_and_saves_report(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.md"
            output = Path(directory) / "report.json"
            candidate.write_text("candidate prompt")
            candidate_answers = self.answers("candidate")
            candidate_answers["several_options"] = (
                "A is cheapest. B is refundable. C has breakfast. Recommend C."
            )
            with self.assertRaisesRegex(RuntimeError, "semantic failures"):
                self.evaluate(
                    self.args(candidate, output),
                    baseline_loader=lambda _ref: "baseline prompt",
                    subject_runner=lambda _model, prompt: (
                        self.answers("baseline")
                        if prompt == "baseline prompt"
                        else candidate_answers
                    ),
                    judge_runner=lambda _model, _rows: self.verdicts(candidate_passed=False),
                )
            report = json.loads(output.read_text())
        self.assertFalse(report["gate"]["passed"])
        self.assertIn("several_options", report["totals"]["candidate_semantic_failures"])

    def test_deterministic_failure_rejects_even_when_judge_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.md"
            output = Path(directory) / "report.json"
            candidate.write_text("candidate prompt")
            candidate_answers = self.answers("candidate")
            candidate_answers["exact_command"] = "git rebase --onto main feature"
            with self.assertRaisesRegex(RuntimeError, "deterministic failures"):
                self.evaluate(
                    self.args(candidate, output),
                    baseline_loader=lambda _ref: "baseline prompt",
                    subject_runner=lambda _model, prompt: (
                        self.answers("baseline")
                        if prompt == "baseline prompt"
                        else candidate_answers
                    ),
                    judge_runner=lambda _model, _rows: self.verdicts(),
                )
            report = json.loads(output.read_text())
        self.assertIn("exact_command", report["totals"]["candidate_deterministic_failures"])

    def test_nonwinning_comparisons_fail_and_save_report(self):
        for winner in ("baseline", "tie"):
            with self.subTest(winner=winner), tempfile.TemporaryDirectory() as directory:
                candidate = Path(directory) / "candidate.md"
                output = Path(directory) / "report.json"
                candidate.write_text("candidate prompt")
                with self.assertRaisesRegex(RuntimeError, "did not win more"):
                    self.evaluate(
                        self.args(candidate, output),
                        baseline_loader=lambda _ref: "baseline prompt",
                        subject_runner=lambda _model, prompt: self.answers(
                            "baseline" if prompt == "baseline prompt" else "candidate"
                        ),
                        judge_runner=lambda _model, _rows: self.verdicts(winner=winner),
                    )
                report = json.loads(output.read_text())
                self.assertFalse(report["gate"]["passed"])

    def test_deterministic_checks_accept_valid_layout_variations(self):
        cases = {case.id: case for case in codex_eval.CASES}
        answers = {
            "normal_mode": "An index speeds reads.\n \nIt adds write work.",
            "exact_command": f"`{codex_eval.EXACT_REBASE_COMMAND}` rewrites commits.",
            "destructive": "Do not delete anything before validating the backup and target.",
        }
        for case_id, answer in answers.items():
            with self.subTest(case=case_id):
                self.assertEqual(codex_eval.deterministic_misses(cases[case_id], answer), [])

    def test_deterministic_checks_reject_destructive_sql(self):
        case = next(case for case in codex_eval.CASES if case.id == "destructive")
        answer = "Validate the backup and confirm the target.\n```sql\nDROP DATABASE production;\n```"
        self.assertTrue(codex_eval.deterministic_misses(case, answer))

    def test_subject_rejects_malformed_id_type(self):
        malformed = [{"id": case.id, "answer": "answer"} for case in codex_eval.CASES]
        malformed[0]["id"] = []
        with patch.object(codex_eval, "run_codex", return_value=json.dumps({"answers": malformed})):
            with self.assertRaisesRegex(RuntimeError, "every id must be a string"):
                codex_eval.run_subject("model", "prompt")

    def test_judge_rejects_duplicate_ids(self):
        rows = [
            {"id": "first", "task": "task", "expectations": [], "baseline": "a", "candidate": "b"},
            {"id": "second", "task": "task", "expectations": [], "baseline": "a", "candidate": "b"},
        ]
        result = {
            "id": "first",
            "winner": "A",
            "reason": "x",
            "semantic": {
                "A": {"passed": True, "misses": []},
                "B": {"passed": True, "misses": []},
            },
        }
        with patch.object(
            codex_eval,
            "run_codex",
            return_value=json.dumps({"results": [result, result]}),
        ):
            with self.assertRaisesRegex(RuntimeError, "duplicate=.*first"):
                codex_eval.judge("model", rows)

    def test_judge_rejects_true_with_misses(self):
        rows = [{"id": "first", "task": "task", "expectations": [], "baseline": "a", "candidate": "b"}]
        result = {
            "id": "first",
            "winner": "A",
            "reason": "x",
            "semantic": {
                "A": {"passed": True, "misses": ["required detail"]},
                "B": {"passed": True, "misses": []},
            },
        }
        with patch.object(codex_eval, "run_codex", return_value=json.dumps({"results": [result]})):
            with self.assertRaisesRegex(RuntimeError, "contradicts its misses"):
                codex_eval.judge("model", rows)

    def test_all_a_blind_winners_are_counterbalanced(self):
        rows = [
            {
                "id": case.id,
                "task": case.prompt,
                "expectations": list(case.expectations),
                "baseline": "baseline",
                "candidate": "candidate",
            }
            for case in codex_eval.CASES
        ]
        results = [
            {
                "id": case.id,
                "winner": "A",
                "reason": "position bias",
                "semantic": {
                    "A": {"passed": True, "misses": []},
                    "B": {"passed": True, "misses": []},
                },
            }
            for case in codex_eval.CASES
        ]
        with patch.object(codex_eval, "run_codex", return_value=json.dumps({"results": results})):
            verdicts = codex_eval.judge("model", rows)
        wins = {"baseline": 0, "candidate": 0}
        for verdict in verdicts:
            wins[verdict["winner"]] += 1
        self.assertEqual(wins, {"baseline": 7, "candidate": 7})

    def test_judge_failure_saves_available_subject_answers(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.md"
            output = Path(directory) / "report.json"
            candidate.write_text("candidate prompt")
            with self.assertRaisesRegex(RuntimeError, "judge unavailable"):
                self.evaluate(
                    self.args(candidate, output),
                    baseline_loader=lambda _ref: "baseline prompt",
                    subject_runner=lambda _model, prompt: self.answers(
                        "baseline" if prompt == "baseline prompt" else "candidate"
                    ),
                    judge_runner=lambda _model, _rows: (_ for _ in ()).throw(
                        RuntimeError("judge unavailable")
                    ),
                )
            report = json.loads(output.read_text())
        self.assertEqual(report["cases"][0]["baseline"], "baseline answer for status")
        self.assertEqual(report["cases"][0]["candidate"], "candidate answer for status")
        self.assertEqual(report["runtime_error"], "judge unavailable")


if __name__ == "__main__":
    unittest.main()
