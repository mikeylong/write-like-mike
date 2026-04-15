# Write Like Mike

Codex skill package for drafting and revising prose in Mike's voice.

The skill supports emails, messages, docs, memos, plans, comments, status updates, and other prose. It uses a synthesized style profile plus optional Agent Memory retrieval as a filtered preference layer.

## Privacy Model

This package stores style rules only. It must not contain raw email bodies, raw Agent Memory entries, recipient details, exact snippets, message URLs, secrets, or identifying examples.

Runtime memory retrieval can adjust tone and emphasis, but it must not introduce facts, commitments, names, dates, or private context not supplied for the current artifact.

## Package Contents

- `SKILL.md`: core routing, behavior contract, writing modes, and workflow
- `agents/openai.yaml`: Codex UI metadata
- `references/style-profile.md`: synthesized writing style profile
- `references/memory-refresh.md`: safe Agent Memory retrieval and refresh guidance
- `scripts/check_privacy.py`: package privacy leakage checker

## Validation

Run these checks before publishing changes:

```bash
python3 /Users/mike/SkillSkill/scripts/validate_skill.py --expect-codex /Users/mike/.codex/skills/write-like-mike
/Users/mike/.codex/skills/write-like-mike/scripts/check_privacy.py /Users/mike/.codex/skills/write-like-mike
python3 -m py_compile /Users/mike/.codex/skills/write-like-mike/scripts/check_privacy.py
```
