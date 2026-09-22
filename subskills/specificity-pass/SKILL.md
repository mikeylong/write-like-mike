---
name: specificity-pass
description: Audit any prose for sentences that make the reader do the writer's work - unnamed referents, partial thoughts, one-sided comparisons, abstract nouns standing in for specific things, and sections that do not do the job their heading names. Use on emails, reports, messages, docs, PRs, recaps, deck copy and speaker notes, before a human reads them. Not a voice pass and not a length pass.
---

# Specificity pass

This is a required subskill of [write-like-mike](../../SKILL.md). Run it on every draft and revision, including short replies. Return the reviewed text to the parent workflow for voice polish; never invoke the parent skill recursively.

A draft fails this pass when a sentence is true but unusable: the reader has to supply a fact the writer already had. The characteristic reaction is "what does that mean?", and it
does not mean the reader is slow. It means the sentence named a category where it should have named a thing.

This is not a style preference. A reader who has to reconstruct your meaning either does it wrong or stops reading.

## The one rule

**Every sentence carries the specific thing it is about.** If a phrase could describe fifty situations, it describes none of them.

## The seven patterns

Check all seven. They are ordered by how often they showed up in real correction rounds.

### 1. The unnamed referent

A definite noun phrase pointing at something never identified. "The line", "that call", "the same point", "the weak spot", "that case", "the test", "the step", "the thread", "the piece".

> "One row used language the team does not use."

Which row, which language, and what replaced it. All three are missing, and the writer knew all three.

> The rule asked whether work was "greenfield", a word they do not use. They dictated the replacement, and it now asks whether the work is new, an extension, or a mix.

### 2. The abstract noun standing in for a specific thing

The boundary, the standard, the bar, the gate, the ceiling, the cap, the floor, the rule, the weighting, the flow, the guardrail. These feel precise because they are nouns. They name a category.

> "The guardrail is not written down yet."

Which guardrail. Name it once, then it is available as shorthand for the rest of the document.

### 3. The one-sided comparison

Something moved, came down, improved, was rescored, changed. Half a comparison is not a fact.

> "The default send moved to activation."

From what? A move needs an origin and a destination. Same for every score, count, duration and price.

### 4. The partial thought that leans on the previous sentence

A sentence that only parses if you are still holding the one before it.

> "The sessions produced the evidence for it, but the skill file does not yet state it."

Two pronouns, one referent, and the reader is carrying context across a sentence boundary to no benefit. Either make the sentence stand alone or fold it into the one it depends on.

### 5. The heading that the section does not deliver

A section headed Goal states goals. A section headed Next Steps contains steps. When a section reads as something else, the fix is not more words, it is writing the thing the heading promised.

> A "Directed Effort Goal" that opens with three sentences about what was broken is a problem statement wearing a goal's heading.

### 6. The repeated word inside one passage

"The allowance ran out in the first and again before the second. Extra capacity carried the first and a reset carried the second."

The second, the second, the second. Ordinals, dates, and names all do this. Read the passage aloud; repetition you cannot hear on the page is obvious in the ear.

### 7. The claim made once and never carried through

A caveat or commitment that appears in one section and is missing everywhere it should have consequences. If the opening says something was never measured, the closing owes the reader a measurement step.

## Two things this pass is not

1. **Not a length pass.** The instruction is almost always "shorter *and* more specific", and those are not in tension. What goes is the connective padding, the restatement, and
   the clause that justifies the sentence before it. What arrives is the noun, the number, the name. A passage usually gets shorter while carrying more.
2. **Not a voice pass.** Metaphors, AI tells and house style belong to `write-like-mike`, which always runs after this one. Run this first, since voice work on a sentence that is
   about to be rewritten for content is wasted. When called by the parent workflow, continue with its voice passes after this review.

## Calibrate to the actual reader

The strongest trap is over-firing. A reader with no context flags every piece of shared vocabulary, and applying that literally produces prose that explains the recipient's own job to them.

Before the pass, write down one line: who reads this, and what do they already know. Then:

1. **Fill** anything the real reader cannot resolve, and anything factually one-sided.
2. **Leave** vocabulary the reader owns, terms of art in their field, and anything defined in the same breath.
3. **Never** define a recipient's own systems, roles, or processes back to them.

A useful test for a borderline term: would the reader have used this phrase themselves last week? If yes, leave it.

## How to run it

1. State the reader and their existing knowledge in one internal line. Keep the calibration and findings out of the finished prose unless the user requested them.
2. Run the mechanical scan for the patterns a regex can see:

   ```bash
   python3 scripts/scan.py <file> [<file> ...]
   ```

   The scan takes file paths and does not read stdin. Write the actual draft to a UTF-8 file in a task-specific directory under `/private/tmp` if it is not already a file. Scan that file; do not read the clipboard or substitute unrelated text.

   Paths in this skill are relative to the skill's own directory, which is given to you as its base directory when the skill loads. Resolve them against that rather than against the working directory.

   It flags candidates, not defects. Every hit needs judgment; many will be correct as written.
3. Read the draft once per pattern rather than once for everything. Pattern-at-a-time catches repetition and heading mismatches that a single read glides over.
4. For a long or important document, add a context-starved reader: give an agent the draft **alone**, with no background, and ask which references it cannot resolve. Expect it to
   over-fire, and triage against the reader line from step 1. Its real value is not the vagueness list, it is that reading only the text catches **contradictions between sections**
   that anyone holding the full context reads straight past.
5. Fix in one pass, not per finding. Use only supported facts; if a needed detail is unavailable, preserve the uncertainty, use a placeholder when suitable, or ask if the missing
   fact is essential. Re-read the changed sentences afterwards: filling one gap routinely introduces a repeated word or a new dangling pronoun.

## When the document is full

A draft at its length limit cannot absorb specificity for free. Every fill needs a cut, so name the cut when you make the fill. The best cuts are duplications between sections,
caveats that already live in the closing, and sentences whose only job is to tell the reader the previous sentence mattered.

## Evidence

Every pattern here came from a real correction round on client prose, most of them phrased at the time as "what does that mean?" or "you're making the reader do too much heavy
lifting". Patterns 1, 2 and 3 account for most findings. Pattern 5 is the one writers resist, because the section reads fine sentence by sentence.
