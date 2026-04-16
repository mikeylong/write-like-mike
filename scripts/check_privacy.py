#!/usr/bin/env python3
"""Check a skill package for obvious source-message leakage."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
QUOTED_REPLY_RE = re.compile(r"^\s*>\s*(On .+ wrote:|From:|To:|Subject:)", re.IGNORECASE)
HEADER_RE = re.compile(r"^\s*(From|To|Cc|Bcc|Subject):\s+\S+", re.IGNORECASE)
LONG_LINE_RE = re.compile(r".{280,}")
UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)
MEMORY_JSON_RE = re.compile(
    r'"(?:content|metadata|scope|created_at|updated_at|importance|tags|id)"\s*:',
    re.IGNORECASE,
)
MEMORY_TOOL_RE = re.compile(
    r"\b(?:memory_get_context|memory_search|memory_capture|memory_upsert|memory_delete)\s*[{(]",
    re.IGNORECASE,
)
SOURCE_MAIL_URL_PARTS = ("mail.", "com/mail")
TEXT_SUFFIXES = {".json", ".md", ".yaml", ".yml", ".txt"}


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == Path(__file__).name:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return files


def check_file(path: Path, root: Path) -> list[str]:
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(root)

    if EMAIL_RE.search(text):
        findings.append(f"{rel}: contains an email address-like string")

    if all(part in text for part in SOURCE_MAIL_URL_PARTS):
        findings.append(f"{rel}: contains a sent-mail URL-like string")

    if UUID_RE.search(text):
        findings.append(f"{rel}: contains a UUID-like memory identifier")

    if MEMORY_JSON_RE.search(text):
        findings.append(f"{rel}: contains raw memory payload-like JSON fields")

    if MEMORY_TOOL_RE.search(text):
        findings.append(f"{rel}: contains raw memory tool-call-like text")

    for index, line in enumerate(text.splitlines(), start=1):
        if QUOTED_REPLY_RE.search(line):
            findings.append(f"{rel}:{index}: looks like a quoted email reply")
        if HEADER_RE.search(line):
            findings.append(f"{rel}:{index}: looks like copied email header metadata")
        if LONG_LINE_RE.fullmatch(line) and not line.lstrip().startswith("description:"):
            findings.append(f"{rel}:{index}: unusually long line may be copied source prose")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skill_dir",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1]),
        help="Skill directory to scan. Defaults to this script's parent skill package.",
    )
    args = parser.parse_args()

    root = Path(args.skill_dir).resolve()
    if not root.is_dir():
        print(f"FAIL {root}: not a directory", file=sys.stderr)
        return 2

    findings: list[str] = []
    for path in iter_files(root):
        findings.extend(check_file(path, root))

    if findings:
        print(f"FAIL {root}")
        for finding in findings:
            print(f"  {finding}")
        return 1

    print(f"PASS {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
