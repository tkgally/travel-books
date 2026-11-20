#!/usr/bin/env python3
"""The ledger of books (data/queue.json) and the JATSI list (data/jatsi.json): a short report and a consistency check.

  ledger.py            what is published, in progress, waiting and queued; which kind of book is due next
  ledger.py check      problems only (exit 1 if any); also run by the tests on the real data

Which kind is next. Tom (2026-11-20): the books of his list "Japan As They Saw It" (JATSI) are added at about
one in every three books. queue.json `jatsi_policy` holds the numbers: of the books started since the policy
began (`others_before` books were already published then), a JATSI book is due whenever the others started
number at least `others_per_jatsi` times the JATSI books started. "Started" = status `in progress` or
`published`. So with others_per_jatsi = 2: JATSI, other, other, JATSI, other, other, …
Standard library only.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STATUSES = ("queued", "in progress", "published", "waiting", "rejected")
STARTED = ("in progress", "published")
NEED = ("slug", "title", "author", "year", "status", "eligibility")
MIN_QUEUED_OTHER = 6      # notes/selection.md
MIN_QUEUED_JATSI = 4      # notes/jatsi.md


def load(repo=REPO):
    q = json.load(open(os.path.join(repo, "data", "queue.json"), encoding="utf-8"))
    jf = os.path.join(repo, "data", "jatsi.json")
    j = json.load(open(jf, encoding="utf-8")) if os.path.exists(jf) else {"books": []}
    return q, j


def is_jatsi(row):
    return row.get("from") == "jatsi"


def next_kind(q):
    """'jatsi' or 'other': the kind of book to start next under the policy (a suggestion: RESUME.md §2)."""
    pol = q.get("jatsi_policy")
    if not pol:
        return "other"
    started = [r for r in q["books"] if r.get("status") in STARTED]
    nj = sum(1 for r in started if is_jatsi(r))
    no = sum(1 for r in started if not is_jatsi(r)) - pol.get("others_before", 0)
    return "jatsi" if no >= pol.get("others_per_jatsi", 2) * nj else "other"


def check(q, j, repo=REPO):
    """A list of problems in the two files and between them and books/, wip/."""
    out, seen, seen_n = [], set(), set()
    numbers = {b["n"] for b in j.get("books", [])}
    if len(numbers) != len(j.get("books", [])):
        out.append("jatsi.json: two entries share a number")
    for r in q["books"]:
        name = r.get("slug") or r.get("title") or "?"
        for k in NEED:
            if r.get(k) in (None, ""):
                out.append(f"{name}: no `{k}`")
        if r.get("status") not in STATUSES:
            out.append(f"{name}: status {r.get('status')!r} is not one of {', '.join(STATUSES)}")
        if r.get("slug") in seen:
            out.append(f"{name}: slug used twice")
        seen.add(r.get("slug"))
        if not (r.get("ia") or r.get("status") == "rejected"):
            out.append(f"{name}: no `ia` identifier")
        if is_jatsi(r):
            n = r.get("jatsi")
            if n not in numbers:
                out.append(f"{name}: from JATSI but `jatsi` ({n!r}) is not a number in data/jatsi.json")
            if n in seen_n:
                out.append(f"{name}: JATSI number {n} is on two rows")
            seen_n.add(n)
        elif "jatsi" in r:
            out.append(f"{name}: has a `jatsi` number but not \"from\": \"jatsi\"")
        elif r.get("from") not in (None, "tom"):
            out.append(f"{name}: `from` is {r.get('from')!r}; known values: jatsi, tom")
        where = {"published": "books", "in progress": "wip"}.get(r.get("status"))
        cfg = None
        for d in ("books", "wip"):
            f = os.path.join(repo, d, r.get("slug") or "?", "book.json")
            if os.path.exists(f):
                cfg = json.load(open(f, encoding="utf-8"))
                if d != where:
                    out.append(f"{name}: is in {d}/ but its status is {r.get('status')!r}")
        if r.get("status") == "published" and cfg is None:
            out.append(f"{name}: published but books/{r.get('slug')}/book.json is missing")
        if cfg is not None and (cfg.get("collection") == "jatsi") != is_jatsi(r):
            out.append(f"{name}: book.json `collection` and the queue row's `from` disagree about JATSI")
    for d in ("books", "wip"):
        dd = os.path.join(repo, d)
        for slug in sorted(os.listdir(dd)) if os.path.isdir(dd) else []:
            if os.path.exists(os.path.join(dd, slug, "book.json")) and slug not in seen:
                out.append(f"{d}/{slug}: no row in data/queue.json")
    return out


def report(q, j, repo=REPO):
    rows = q["books"]
    by = {s: [r for r in rows if r.get("status") == s] for s in STATUSES}
    lines = []

    def show(title, rs, extra=lambda r: ""):
        lines.append(f"{title} ({len(rs)})")
        for r in rs:
            tag = " [JATSI]" if is_jatsi(r) else (" [Tom]" if r.get("from") == "tom" else "")
            lines.append(f"  {r.get('slug')}{tag} — {r.get('author')} ({r.get('year')}){extra(r)}")
    show("Published", by["published"], lambda r: f"  v{r.get('version', '?')} {r.get('published', '')}")
    show("In progress", by["in progress"])
    show("Waiting", by["waiting"], lambda r: f"  — {r.get('waiting_for', '')}"[:120])
    show("Queued, from JATSI", [r for r in by["queued"] if is_jatsi(r)], lambda r: f"  {r.get('images', '?')} images")
    show("Queued, others", [r for r in by["queued"] if not is_jatsi(r)], lambda r: f"  {r.get('images', '?')} images")
    lines.append(f"Rejected rows: {len(by['rejected'])}; rejected before queuing (queue.json `rejected`): {len(q.get('rejected', []))}")
    nj = sum(1 for r in by["queued"] if is_jatsi(r))
    no = len(by["queued"]) - nj
    kind = next_kind(q)
    lines.append("")
    lines.append("Next new book: " + ("one from JATSI" if kind == "jatsi" else "one that is not from JATSI")
                 + " (ledger.py docstring; a suggestion, RESUME.md §2)")
    if no < MIN_QUEUED_OTHER:
        lines.append(f"Fewer than {MIN_QUEUED_OTHER} other books queued: find more (skill select-book)")
    if j.get("books") and nj < MIN_QUEUED_JATSI:
        lines.append(f"Fewer than {MIN_QUEUED_JATSI} JATSI books queued: vet more from data/jatsi.json (notes/jatsi.md)")
    npub = len(by["published"])
    if npub and npub % 5 == 0:
        lines.append(f"{npub} books published: a review session is due if the last review covered fewer (notes/improvement.md)")
    return "\n".join(lines)


def main():
    q, j = load()
    problems = check(q, j)
    if sys.argv[1:] == ["check"]:
        print("\n".join(problems) or "ledger: no problems")
        sys.exit(1 if problems else 0)
    print(report(q, j))
    if problems:
        print("\nPROBLEMS\n" + "\n".join("  " + p for p in problems))


if __name__ == "__main__":
    main()
