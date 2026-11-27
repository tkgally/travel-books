#!/usr/bin/env python3
"""Review a corrections-mode run before trusting it; write the spots that need judging.

  review.py DRAFT_DIR VERIFIED_DIR [--out spots.json]

Reads the verifier's raw lists (VERIFIED_DIR/pNNNN.corr) against the draft pages and prints:
  * counts by kind — words (letters or digits changed), punctuation, markup/spacing;
  * corrections that could not be applied (find text missing or not unique): look at each;
  * page-length outliers: draft and verified text differ in length by more than 5% (a runaway, truncated
    or duplicated page);
  * pages with no .corr or an error in log.jsonl.
spots.json lists every change of kind words or punctuation, with both readings and context, for judge.py:
  {"p0123": [{"n": 1, "draft": "...", "verified": "...", "kind": "words", "context": "..."}]}
"""
import argparse, difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections  # noqa: E402


def bare(t):
    return re.sub(r"</?[a-z]+>|\[\[(?:cont|right|center|subtitle|caption|break|blank)\]\]", "", t)


def letters(t):
    return re.sub(r"[^0-9A-Za-zÀ-ÿ]", "", bare(t))


def nospace(t):
    return re.sub(r"\s", "", bare(t)).replace("'", "’").replace('"', "”").replace("“", "”").replace("‘", "’")


def kind_of(a, b):
    if letters(a) != letters(b):
        return "words"
    if nospace(a) != nospace(b):
        return "punctuation"
    return "markup"


def cont_change(draft, verified):
    """'removed' / 'added' when the verified text has fewer / more [[cont]] marks than the draft, else None.
    Such a change is 'markup' and is applied without a spot, so it is listed for a look at the indent on the scan
    (*The Nile without a Dragoman*, 2026-11-21: two page-top joins dropped unseen)."""
    a, b = draft.count("[[cont]]"), verified.count("[[cont]]")
    return None if a == b else ("removed" if b < a else "added")


def cont_at(text, find):
    """A few words where a [[cont]] change was proposed, for finding it on the scan."""
    return corrections.CONT.sub("", find).strip()[:40]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft"); ap.add_argument("verified"); ap.add_argument("--out")
    a = ap.parse_args()
    kinds, skipped, spots, outliers, missing, conts, proposed = {}, [], {}, [], [], [], []
    for f in sorted(os.listdir(a.draft)):
        if not re.fullmatch(r"p\d+[a-z]?\.txt", f):
            continue
        pg = f[:-4]
        draft = open(os.path.join(a.draft, f), encoding="utf-8").read()
        cf_ = os.path.join(a.verified, pg + ".corr")
        vf = os.path.join(a.verified, f)
        if not os.path.exists(cf_) or not os.path.exists(vf):
            missing.append(pg)
            continue
        cur = draft
        for c in corrections.parse(open(cf_, encoding="utf-8").read()):
            fnd, rep = c["find"], c["replace"]
            if corrections.blank_filled(fnd, rep):
                proposed.append(f"{pg}: [[blank]] page filled by the verifier, NOT applied: {rep[:50]!r}")
                continue
            if corrections.cont_only(fnd, rep):
                if cur.count(fnd) == 1:
                    proposed.append(f"{pg}: [[cont]] {'added' if rep.count('[[cont]]') > fnd.count('[[cont]]') else 'removed'}"
                                    f" at {cont_at(cur, fnd)!r}")
                continue
            if cur.count(fnd) != 1 or fnd == rep:
                if fnd != rep:
                    skipped.append(f"{pg}: {cur.count(fnd)}x {fnd[:40]!r} -> {rep[:40]!r}")
                continue
            k = kind_of(fnd, rep)
            kinds[k] = kinds.get(k, 0) + 1
            i = cur.index(fnd)
            if k != "markup":
                # shrink to the changed core, keep a little context
                sm = difflib.SequenceMatcher(None, fnd, rep, autojunk=False)
                ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
                i1, i2, j1, j2 = ops[0][1], ops[-1][2], ops[0][3], ops[-1][4]
                ctx = (cur[max(0, i - 60):i] + fnd + cur[i + len(fnd):i + len(fnd) + 60]).replace("\n", " ⏎ ")
                spots.setdefault(pg, []).append({"n": len(spots.get(pg, [])) + 1, "kind": k, "find": fnd, "replace": rep,
                                                 "draft": fnd[max(0, i1 - 12):i2 + 12], "verified": rep[max(0, j1 - 12):j2 + 12],
                                                 "context": ctx})
            cur = cur.replace(fnd, rep)
        vtext = open(vf, encoding="utf-8").read()
        cc = cont_change(draft, vtext)
        if cc:
            conts.append(f"{pg}: [[cont]] {cc}")
        la, lb = len(nospace(draft)), len(nospace(vtext))
        if abs(la - lb) > 0.05 * max(la, 1) + 10:
            outliers.append((pg, la, lb))
    lf = os.path.join(a.verified, "log.jsonl")
    errs = [json.loads(x)["page"] for x in open(lf, encoding="utf-8") if '"error"' in x] if os.path.exists(lf) else []
    print("changes by kind:", kinds)
    print(f"not applied ({len(skipped)}):")
    for s in skipped:
        print("  ", s)
    print(f"proposed by the verifier and NOT applied — [[cont]] changes (the draft's join stands; the verifier was wrong in "
          f"13 of 15 so far) and [[blank]] pages filled (show-through): look at each on the scan ({len(proposed)}):")
    for c in proposed:
        print("  ", c)
    print(f"[[cont]] added or removed by the verifier with other changes, applied unjudged: look at the indent on the scan ({len(conts)}):")
    for c in conts:
        print("  ", c)
    print("length outliers (page, draft chars, verified chars):", outliers)
    print("pages without a verified text:", missing)
    print("pages with an error in log.jsonl (re-run them):", errs)
    n = sum(len(v) for v in spots.values())
    print(f"spots to judge: {n} on {len(spots)} pages")
    if a.out:
        json.dump(spots, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
