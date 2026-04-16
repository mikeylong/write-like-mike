# Write Like Mike

Skill package for drafting and revising prose in Mike's voice.

The skill supports emails, messages, docs, memos, plans, comments, status updates, and other prose. It uses a synthesized style profile plus optional memory retrieval as a filtered preference layer.

## Privacy Model

This package stores style rules only. It must not contain raw email bodies, raw memory entries, recipient details, exact snippets, message URLs, secrets, or identifying examples.

Runtime memory retrieval can adjust tone and emphasis, but it must not introduce facts, commitments, names, dates, or private context not supplied for the current artifact.

## Package Contents

- `SKILL.md`: core routing, behavior contract, writing modes, and workflow
- `agents/openai.yaml`: agent UI metadata
- `references/style-profile.md`: synthesized writing style profile
- `references/memory-refresh.md`: safe memory retrieval and refresh guidance
- `scripts/check_privacy.py`: package privacy leakage checker

## Validation

Run these checks before publishing changes:

```bash
python3 /path/to/validate_skill.py /path/to/write-like-mike
/path/to/write-like-mike/scripts/check_privacy.py /path/to/write-like-mike
python3 -m py_compile /path/to/write-like-mike/scripts/check_privacy.py /path/to/write-like-mike/scripts/run_eval.py
```

## Eval Workflow

The reusable eval suite lives in `evals/` and uses synthetic prompts only.

Generate a blank report template:

```bash
python3 scripts/run_eval.py > evals/reports/YYYY-MM-DD.md
```

After filling in case outputs and scores, validate the report:

```bash
python3 scripts/run_eval.py --report evals/reports/YYYY-MM-DD.md
```

The eval passes when the aggregate score is at least 85%, there are no hard failures, and the package privacy check passes.
