# Agent Memory Refresh

Use this reference when `$write-like-mike` needs Agent Memory to improve a draft or when the user asks to refresh the style profile from memory.

Agent Memory is a preference layer. It is not a prose source. Use it to discover durable user preferences, prior corrections, channel norms, and recurring taste signals. Do not copy memory entries into drafts or into this skill package.

## Runtime Retrieval

Run a focused `memory_search` only when memory can materially improve the output. Good triggers include:

- the user asks for prose in their voice but gives little style direction
- the channel or artifact type matters, such as email, Slack, memo, doc, plan, comment, or review note
- the topic has likely durable context in memory
- the user asks to make something more like them
- the draft involves recurring preferences such as concise, direct, less corporate, or lower hype

Use short search queries built from the current task:

- `writing style preference tone direct concise less corporate`
- `rewrite in my voice make it more like me`
- `email message memo status update prose preference`
- `feedback correction assistant wording style`
- the current channel, audience, topic, or artifact type

Keep the result set small. Prefer high-confidence, durable entries over broad recall.

## Include

Use memory facts when they are:

- explicit user preferences
- corrections to assistant tone, structure, or wording
- approved rewrite patterns
- repeated constraints across turns or projects
- durable channel norms
- stable facts needed to avoid awkward or generic prose
- current and relevant to the artifact being written

## Exclude

Ignore memory facts when they are:

- assistant-only prose with no user approval
- broad project summaries unrelated to writing
- old imported chat fragments with unclear authorship
- raw logs or transcript fragments
- secrets, credentials, tokens, URLs, or private identifiers
- names, dates, commitments, or private context not supplied in the current request
- one-off task details that would make the draft overfit to an old situation
- contradictory to the user's current instruction

## Precedence

Resolve conflicts in this order:

1. Current user instructions.
2. Facts, commitments, constraints, and asks supplied in the current request.
3. Relevant, durable Agent Memory facts.
4. The static style profile.

Memory can shape tone and emphasis. It cannot authorize new facts, promises, availability, relationships, private details, or claims.

## Profile Refresh Workflow

When refreshing the style profile from Agent Memory:

1. Run focused searches for writing preferences, tone corrections, approved rewrites, and channel norms.
2. Discard unrelated project facts, assistant-only text, raw imported fragments, and anything sensitive.
3. Group repeated signals into themes such as directness, structure, tone, bullets, critique, or channel behavior.
4. Convert each theme into a synthesized style rule.
5. Add only durable rules to `references/style-profile.md`.
6. Run the package privacy checker before finishing.

Do not add raw snippets, memory identifiers, search payloads, names, URLs, secrets, or identifying examples to the skill package.

## Candidate Rule Format

Use this shape when proposing a style-profile update:

```markdown
## Candidate Style Rules

- Theme: [short label]
  Rule: [synthesized writing rule]
  Source basis: [general description, such as "repeated user corrections about tone"]
  Confidence: [low, medium, high]
  Add to: [target section in style-profile.md]
```

The `Source basis` field should describe the type of evidence, not quote or identify specific memory entries.

## Review Checklist

- Is the rule durable across future writing tasks?
- Does it improve Mike's voice rather than imitate assistant prose?
- Is it free of raw memory text and identifying details?
- Does it avoid adding facts the user did not provide for the current artifact?
- Does it preserve the skill's synthesized-notes-only privacy model?
