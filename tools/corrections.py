#!/usr/bin/env python3
"""Apply a model-written corrections list to a draft page.

Corrections format (one JSON object per line):
  {"find": "exact text in the draft", "replace": "corrected text"}
`find` must occur exactly once in the draft; otherwise the correction is
skipped and reported. A reply of NONE (or no JSON lines) means no changes.
"""
import json, re, sys

CONT = re.compile(r"\[\[cont\]\]\s*")


def cont_only(find, replace):
    """True when a correction does nothing but add or remove [[cont]] marks. Such changes are not applied: the
    draft's join stands and review.py lists the proposal for a look at the indent on the scan. The corrections
    pass was wrong in 13 of 15 such changes checked in published books (review after 110 books, 2026-11-27)."""
    return find.count("[[cont]]") != replace.count("[[cont]]") and CONT.sub("", find) == CONT.sub("", replace)


def apply(draft, reply):
    applied, skipped = 0, []
    for line in reply.splitlines():
        line = line.strip().rstrip(",")
        if not line.startswith("{"):
            continue
        try:
            c = json.loads(line)
            f, r = c["find"], c["replace"]
        except Exception:
            skipped.append(line[:80]); continue
        if cont_only(f, r):
            skipped.append(f"[[cont]] change not applied: {f[:40]}"); continue
        if f and r != f and f in r and r in draft:
            # an insertion an earlier entry already made (models sometimes send one change twice, in two
            # forms: "called\n" -> "called Inter-\n" and "also called" -> "also called Inter-")
            skipped.append(f"already applied: {r[:40]}"); continue
        if f and draft.count(f) == 1:
            draft = draft.replace(f, r); applied += 1
        else:
            skipped.append(f"{draft.count(f)}x: {f[:40]}")
    return draft, applied, skipped


def parse(reply):
    """The corrections of a reply as dicts, in order; lines that are not valid JSON objects with find/replace
    are left out (American Stories p252, 2026-11-18: an unescaped quote in one line crashed judge.py)."""
    out = []
    for line in reply.splitlines():
        line = line.strip().rstrip(",")
        if not line.startswith("{"):
            continue
        try:
            c = json.loads(line)
            if isinstance(c.get("find"), str) and isinstance(c.get("replace"), str):
                out.append(c)
        except Exception:
            pass
    return out


if __name__ == "__main__":
    d = open(sys.argv[1], encoding="utf-8").read()
    out, n, sk = apply(d, open(sys.argv[2], encoding="utf-8").read())
    sys.stdout.write(out)
    print(f"applied {n}, skipped {len(sk)}: {sk}", file=sys.stderr)
