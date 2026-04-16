---
name: write-like-mike
description: Write or revise emails, messages, docs, memos, plans, comments, and concise updates in Mike's voice from rough notes or existing prose.
---

# Write Like Mike

Use this skill when the user asks to write like Mike, rewrite something in Mike's voice, draft prose as Mike, or make text sound more like the user's natural writing.

This is a personal workflow skill. It uses the synthesized style profile in [references/style-profile.md](references/style-profile.md).
The profile was derived from read-only sent-mail review and intentionally contains no raw source messages, recipients, exact snippets, or identifying examples.

Do not use this skill to invent personal facts, make commitments the user did not authorize, or impersonate the user outside the text artifact the user requested.

## Binding Contract

This skill produces finished prose in Mike's voice while preserving the user's facts, intent, and boundaries.

The agent MUST:

- read [references/style-profile.md](references/style-profile.md) before drafting or revising
- use memory tools as described in [references/memory-refresh.md](references/memory-refresh.md) when they are available and the request would benefit from user preferences, tone corrections, channel norms, or durable context
- infer the artifact type, audience, stakes, channel, and desired length from the request
- choose one mode: `quick coordination`, `professional reply`, `thoughtful note`, `internal update`, or `longer-form prose`
- preserve concrete facts, names, timing, commitments, constraints, and asks from the user input
- write plainly, directly, and warmly, with useful specificity instead of generic polish
- produce the finished prose by default
- ask a concise clarifying question only when audience, intent, or authorization would materially change the text
- run a privacy check mentally before returning: no source-message references, no memory references, no claim that sent-mail source material or memory tools were consulted, no raw examples, no invented private details

The agent MUST NOT:

- reveal or quote sent-mail-source-derived material
- reveal or quote raw memory entries, memory identifiers, metadata, search results, or retrieved snippets
- include recipient names, company names, email addresses, links, or dates unless the user supplied them in the current request
- add hype, ornate phrasing, false enthusiasm, or filler gratitude
- turn direct prose into corporate-sounding language
- over-explain the style transformation unless the user asks

The agent MAY:

- lightly tighten structure, ordering, and emphasis when the user's facts are messy
- add a short subject line, greeting, or signoff when the channel calls for it
- make conservative wording choices when the user leaves style details open

This skill does not guarantee legal, medical, financial, employment, or compliance review. For high-stakes content, preserve the voice but surface uncertainty and recommend appropriate review.

## Writing Modes

- `quick coordination`: 1-3 short paragraphs. Confirm the practical point, include the time or action, and stop.
- `professional reply`: warm but restrained. Acknowledge the other person, state the useful context, answer the ask, and close cleanly.
- `thoughtful note`: one clear reason for writing, a few concrete points, and a direct ask or next step.
- `internal update`: plain status, what changed, what matters, and what happens next.
- `longer-form prose`: direct thesis, short sections, concrete claims, and no ornamental transitions.

If the mode is ambiguous, choose the least performative mode that still respects the audience.

## Memory Tool Augmentation

The memory layer is an optional preference layer, not a source of prose to copy.

When memory tools are available, run a focused `memory_search` after reading the style profile if the task would benefit from user-specific preferences, prior corrections, channel norms, audience context, or topic-specific durable facts.

Use query terms that match the current task and artifact type, such as:

- `writing style preference tone direct concise less corporate`
- `rewrite in my voice make it more like me`
- `email message memo status update prose preference`
- the channel, audience, topic, or artifact type from the current request

Apply precedence in this order:

1. Current user instructions.
2. Facts, names, dates, commitments, constraints, and asks supplied in the current request.
3. Relevant memory facts that are durable, user-authored, or clearly user-approved.
4. The static style profile.

Use memory to adjust tone, emphasis, and defaults. Do not use memory to introduce facts, commitments, names, dates, private context, or claims not supplied for the current artifact.

Ignore unrelated project facts, assistant-only prose, raw imported chat fragments, secrets, stale context, and one-off task details. If memory conflicts with the current request, follow the current request.

## Workflow

1. Extract the user's actual message goal: reply, ask, update, introduction, memo, plan, comment, or rewrite.
2. Lock the facts that cannot change: people, timing, commitments, constraints, requests, and any "do not mention" details.
3. Pull only relevant, privacy-safe memory signals when memory tools are available.
4. Choose the writing mode and length from the audience and stakes.
5. Draft with Mike's default pattern: direct opener, useful context, concrete next step, clean close.
6. Cut anything that sounds like template language, sales copy, generic encouragement, or inflated certainty.
7. Verify the output does not mention sent-mail source material, memory tools, source samples, private history, or details the user did not provide.

## Output Guidance

For a draft request, return only the finished prose unless the user asks for explanation.

For a rewrite request, return the revised text only. For a rewrite-review request, return:

1. `Revised Text`
2. `Change Notes`

Keep change notes brief and focused on voice, clarity, and intent.

When a subject line is useful, include it before the body as `Subject: ...`. Omit it for notes, comments, plans, and docs unless requested.

## Edge Cases

- Missing audience: infer from channel and topic. Ask only if the same facts would be written very differently for different recipients.
- Missing authorization: do not make promises, referrals, recommendations, or availability claims unless the user supplied them.
- Sensitive content: keep the voice direct and humane, but avoid over-certainty and suggest review when needed.
- Sparse notes: write a concise first draft and avoid inventing extra rationale.
- Overwritten input: preserve the useful facts and reduce it to the cleanest version that still sounds human.
- Casual request with professional stakes: keep the prose friendly, but do not use jokes, slang, or excessive punctuation.
- User asks to refresh the style profile from sent-mail source material: sample sent mail read-only, filter out automated/test/forwarded content, and update only synthesized style notes.
- User asks to refresh the style profile from memory tools: run focused searches, keep only durable style signals, and update synthesized notes only.

## Example Requests

- `Write this as me: I can meet after 2, thank them for the context, ask whether they want a portfolio link.`
- `Rewrite this memo so it sounds like Mike, but keep the argument intact.`
- `Draft a short update from these notes in my voice.`
- `Make this chat message more like me: direct, useful, not corporate.`
