#!/usr/bin/env python3
"""Generate and validate eval reports for the write-like-mike skill."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CATEGORIES = [
    "Voice fit",
    "Factual discipline",
    "Privacy and source safety",
    "Usefulness and actionability",
    "Mode fit",
    "Hidden-source discipline",
]

CASE_HEADING_RE = re.compile(r"^## Case (WLM-\d{3}): .+$", re.MULTILINE)
CASE_SCORE_RE = re.compile(r"^Score:\s*(\d+)\s*/\s*12\s*$", re.MULTILINE)
CASE_HARD_FAIL_RE = re.compile(r"^Hard failure:\s*(yes|no)\s*$", re.MULTILINE | re.IGNORECASE)
CATEGORY_RE = re.compile(r"^- (.+?):\s*([0-2])\s*$", re.MULTILINE)
AGGREGATE_RE = re.compile(r"^Aggregate score:\s*(\d+)\s*/\s*(\d+)\s*\(([0-9]+(?:\.[0-9]+)?)%\)\s*$", re.MULTILINE)
RESULT_RE = re.compile(r"^Result:\s*(PASS|FAIL)\s*$", re.MULTILINE)
HARD_FAILURES_RE = re.compile(r"^Hard failures:\s*(\d+)\s*$", re.MULTILINE)
PASSING_THRESHOLD = 0.85


@dataclass
class CaseResult:
    case_id: str
    score: int
    hard_failure: bool


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_cases_path() -> Path:
    return repo_root() / "evals" / "cases.json"


def load_cases(cases_path: Path) -> list[dict[str, object]]:
    with cases_path.open(encoding="utf-8") as handle:
        cases = json.load(handle)
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases.json must contain a non-empty list")
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("each case must be an object")
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id.startswith("WLM-"):
            raise ValueError("each case must have a case_id like WLM-001")
        if case_id in seen:
            raise ValueError(f"duplicate case_id: {case_id}")
        seen.add(case_id)
        for key in ("title", "prompt", "expected_mode", "must_preserve", "risk_checks"):
            if key not in case:
                raise ValueError(f"{case_id} missing required key: {key}")
    return cases


def template_for(cases: list[dict[str, object]]) -> str:
    total = len(cases) * 12
    lines = [
        "# Write Like Mike Eval Report - YYYY-MM-DD",
        "",
        "Cases file: `evals/cases.json`",
        "Rubric: `evals/rubric.md`",
        "",
        f"Aggregate score: 0 / {total} (0.0%)",
        "Result: FAIL",
        "Hard failures: 0",
        "",
        "## Summary",
        "",
        "- Replace this line with the main findings.",
        "",
        "## Case Results",
        "",
    ]
    for case in cases:
        case_id = str(case["case_id"])
        title = str(case["title"])
        lines.extend(
            [
                f"## Case {case_id}: {title}",
                "",
                "Score: 0 / 12",
                "Hard failure: no",
                "",
                "Scores:",
            ]
        )
        for category in CATEGORIES:
            lines.append(f"- {category}: 0")
        lines.extend(
            [
                "",
                "Output:",
                "",
                "```text",
                "[generated output]",
                "```",
                "",
                "Notes:",
                "",
                "- [scoring notes]",
                "",
            ]
        )
    lines.extend(["## Recommended Improvements", "", "- [improvement]", ""])
    return "\n".join(lines)


def split_case_sections(report_text: str) -> dict[str, str]:
    matches = list(CASE_HEADING_RE.finditer(report_text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        case_id = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report_text)
        sections[case_id] = report_text[match.start() : end]
    return sections


def parse_case(case_id: str, section: str) -> CaseResult:
    score_match = CASE_SCORE_RE.search(section)
    if not score_match:
        raise ValueError(f"{case_id} is missing Score: N / 12")
    score = int(score_match.group(1))
    if score < 0 or score > 12:
        raise ValueError(f"{case_id} score must be between 0 and 12")

    hard_match = CASE_HARD_FAIL_RE.search(section)
    if not hard_match:
        raise ValueError(f"{case_id} is missing Hard failure: yes|no")
    hard_failure = hard_match.group(1).lower() == "yes"

    category_scores = {name: int(value) for name, value in CATEGORY_RE.findall(section)}
    missing = [category for category in CATEGORIES if category not in category_scores]
    if missing:
        raise ValueError(f"{case_id} missing category scores: {', '.join(missing)}")
    category_sum = sum(category_scores[category] for category in CATEGORIES)
    if category_sum != score:
        raise ValueError(f"{case_id} score {score} does not equal category sum {category_sum}")

    if "```text" not in section:
        raise ValueError(f"{case_id} missing text output block")

    return CaseResult(case_id=case_id, score=score, hard_failure=hard_failure)


def validate_report(report_path: Path, cases: list[dict[str, object]]) -> None:
    report_text = report_path.read_text(encoding="utf-8")
    sections = split_case_sections(report_text)
    expected_ids = [str(case["case_id"]) for case in cases]
    missing = [case_id for case_id in expected_ids if case_id not in sections]
    extra = [case_id for case_id in sections if case_id not in expected_ids]
    if missing:
        raise ValueError(f"report missing cases: {', '.join(missing)}")
    if extra:
        raise ValueError(f"report has unknown cases: {', '.join(extra)}")

    results = [parse_case(case_id, sections[case_id]) for case_id in expected_ids]
    aggregate = sum(result.score for result in results)
    total = len(expected_ids) * 12
    hard_failures = sum(1 for result in results if result.hard_failure)

    aggregate_match = AGGREGATE_RE.search(report_text)
    if not aggregate_match:
        raise ValueError("report missing Aggregate score line")
    reported_score = int(aggregate_match.group(1))
    reported_total = int(aggregate_match.group(2))
    reported_percent = float(aggregate_match.group(3))
    expected_percent = round((aggregate / total) * 100, 1)
    if reported_score != aggregate or reported_total != total:
        raise ValueError("reported aggregate does not match case scores")
    if abs(reported_percent - expected_percent) > 0.1:
        raise ValueError("reported percentage does not match case scores")

    hard_match = HARD_FAILURES_RE.search(report_text)
    if not hard_match:
        raise ValueError("report missing Hard failures line")
    if int(hard_match.group(1)) != hard_failures:
        raise ValueError("reported hard failure count does not match cases")

    result_match = RESULT_RE.search(report_text)
    if not result_match:
        raise ValueError("report missing Result: PASS|FAIL")
    expected_pass = aggregate / total >= PASSING_THRESHOLD and hard_failures == 0
    expected_result = "PASS" if expected_pass else "FAIL"
    if result_match.group(1) != expected_result:
        raise ValueError(f"reported result should be {expected_result}")


def run_privacy_check() -> None:
    script = repo_root() / "scripts" / "check_privacy.py"
    subprocess.run([str(script), str(repo_root())], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=default_cases_path(),
        help="Path to eval cases JSON.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Completed Markdown report to validate. Omit to print a report template.",
    )
    args = parser.parse_args()

    try:
        cases = load_cases(args.cases)
        if args.report is None:
            print(template_for(cases))
        else:
            validate_report(args.report, cases)
            run_privacy_check()
            print(f"PASS {args.report}")
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
