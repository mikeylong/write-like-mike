#!/usr/bin/env python3
"""Flag candidates for the specificity pass. Every hit needs judgment: this finds
shapes a regex can see, not defects. Correct-as-written hits are expected and fine."""
import re, sys, collections

ABSTRACT = r"(?:line|boundary|standard|bar|gate|ceiling|cap|floor|rule|weighting|flow|thread|step|test|guardrail|point|piece|case|call|approach|process|issue|thing|stage|pass)"

CHECKS = [
    ("unnamed-referent",
     re.compile(r"\b(?:the|that|this|those|these)\s+(?:same\s+|other\s+|whole\s+)?" + ABSTRACT + r"\b", re.I),
     "Definite reference to a category. Name the specific thing, at least once."),
    ("one-sided-comparison",
     re.compile(r"\b(?:moved|came down|went up|dropped|rose|improved|increased|decreased|changed|rescored|reduced|grew|fell)\b(?![^.]*\bfrom\b)", re.I),
     "A change with no from-value. Give both sides or drop the comparison."),
    ("vague-quantity",
     re.compile(r"\b(?:some|several|a number of|a handful of|various|certain|multiple|many|a few)\s+\w+", re.I),
     "Unquantified. Use the number, or say why it is not known."),
    ("vague-evaluation",
     re.compile(r"\b(?:workable|reasonable|appropriate|significant|substantial|meaningful|robust|solid|proper|relevant|effective)\b", re.I),
     "An evaluation with no content. Say what makes it so."),
    ("dangling-opener",
     re.compile(r"(?:^|(?<=[.!?]\s))(?:It|This|That|They|Those|These|One)\s+(?:is|was|are|were|has|had|does|did|will|would|can|could)\b"),
     "Sentence opens on a pronoun. Check the antecedent is unambiguous."),
    ("hedged-nonstatement",
     re.compile(r"\b(?:sort of|kind of|somewhat|fairly|rather\b(?! than)|arguably|to some extent|in some ways)\b", re.I),
     "Hedge with no content. Commit or cut."),
]

REPEAT_STOP = set("""a an the and or but of to in on at for with by is was are were be been being
it its this that these those as from into than then so such not no we you they he she our their his her
one two three first second third next last same other more most less least any all each every""".split())


def scan(path):
    hits = []
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith(("```", "|", "<!--")):
            continue
        for name, rx, why in CHECKS:
            for m in rx.finditer(line):
                hits.append((n, name, m.group(0).strip(), why))
        # repeated content word inside one line, the "the second, the second" tell
        words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", line)]
        for w, c in collections.Counter(words).items():
            if c >= 3 and w not in REPEAT_STOP:
                hits.append((n, "repetition", f'"{w}" x{c}', "Same word three times in one passage. Vary it or restructure."))
    return hits


def main(paths):
    total = 0
    for path in paths:
        hits = scan(path)
        total += len(hits)
        print(f"\n{path}: {len(hits)} candidate(s)")
        for ln, name, frag, why in sorted(hits):
            print(f"  {path}:{ln}  [{name}] {frag}")
            print(f"      -> {why}")
    print(f"\n{total} candidate(s) across {len(paths)} file(s). Each needs judgment against your reader line.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: scan.py <file> [<file> ...]", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
