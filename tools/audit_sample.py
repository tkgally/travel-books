#!/usr/bin/env python3
"""Sampled audit of a finished text against the scans — measures the checker as well as the book.

  audit_sample.py --pages-dir DIR --images DIR --out DIR --rules PROMPT.md
                  [--n 6 | --pages p0012,p0040] [--seed NAME] [--model opus] [--conditions whole,strips]
                  [--workers 5] [--no-seeds]

What it does (English page markup; images are pNNN.png/jpg named like the page files):
1. picks N pages at random (repeatable: --seed, default the directory name), with enough text on them;
2. PLANTS known errors in a copy of each page's text (5 per page: a modernized spelling or a lowered
   capital, a look-alike letter, a real word swapped for a look-alike real word (these/those, it/if),
   a dropped small word, a changed punctuation mark) and records where;
3. asks a fresh model call per page to proofread that text against the scan and list every difference
   ("whole" = one call with the whole page image; "strips" = three calls, each with a third of the page
   at higher magnification);
4. scores: which planted errors were found (the reader's RECALL, per kind of error), and lists every
   other difference it reported — these are candidate REAL errors in the book. Each candidate must
   then be looked at on the scan (crop it; do not trust the list: readers are often wrong) and the
   confirmed ones corrected and counted in notes/metrics.md.

Why plant errors: a reader that finds nothing proves nothing unless we know how much it would have
found. Recall on the planted errors turns "k real errors found" into an estimate of how many remain
(roughly k / recall), and shows the kinds of error this reader is blind to.

Output in OUT: pNNN.given.txt (text with planted errors), seeds.json, <condition>/pNNN*.txt (raw
replies), log.jsonl (cost), report.txt and candidates.tsv. Resumable: finished calls are not repeated.
Italics, small caps and notes are not audited (the text is compared as plain words).
"""
import argparse, concurrent.futures as cf, difflib, hashlib, json, os, random, re, subprocess, time
from refusal import is_refusal

TASK = """

## Your task now: PROOFREAD a transcription against the scan (do not transcribe)

Below is a transcription of {what}, made under the rules above and shown as plain text: italics, small
capitals, footnotes and their marks have been removed on purpose — do not report them. It may begin or end in
the middle of a sentence.

Compare it with the scan word by word and letter by letter, and report EVERY place where the transcription
does not say what the print says:
- a wrong letter or word; a spelling that has been modernized or "corrected" (the printed spelling always wins,
  even an obvious misprint — look hard at every word that looks modern: `show` for printed `shew`,
  `today` for `to-day`, `connection` for `connexion`), and at every proper name and foreign word;
- a wrong capital or lower-case initial; a missing or added word; a missing line or sentence; words that are not
  on the page; a wrong punctuation mark; a wrong paragraph break.
Do NOT report the conventions of the transcription: ligatures written as plain letters, modern spacing around
punctuation and inside quotation marks, words rejoined across line ends, omitted running heads, page numbers
and signature marks, straight or curly quotes, dash length, tables left out.

The transcription reads fluently even where it is wrong, so do not read it for sense: check it against the
shapes on the scan. {where}

Reply with one JSON object per difference, one per line, and nothing else:
{{"given": "4 to 8 consecutive words copied exactly from the transcription, including the wrong part", "print": "the same words exactly as the scan prints them", "sure": "high" | "medium" | "low"}}
If you find no difference, reply with the single word NONE.

<transcription>
{text}
</transcription>
"""

MODERN = [(r"\b([Tt])o-(day|morrow|night)\b", r"\1o\2"), (r"\b([Ss])hew", r"\1how"), (r"\b([Cc])onnexion", r"\1onnection"),
          (r"\b([A-Za-z]{3,})our\b", r"\1or"), (r"\b([Aa])ny one\b", r"\1nyone"), (r"\b([Ee])very one\b", r"\1veryone"),
          (r"\b([Ss])ome one\b", r"\1omeone"), (r"\b([Ff])or ever\b", r"\1orever"), (r"\b([A-Za-z]{4,})ise\b", r"\1ize"),
          (r"\b([Gg])rey\b", r"\1ray"), (r"\b([A-Za-z]{3,})tre\b", r"\1ter"), (r"\b([Ww])aggon", r"\1agon"),
          (r"\b([A-Za-z]{3,})'d\b", r"\1ed")]
# pairs of real words that old type and poor scans confuse (and that judges have swapped in past books):
# the hardest kind to catch, because the wrong text still reads well
REAL = [("these", "those"), ("it", "if"), ("then", "than"), ("on", "or"), ("not", "nor"), ("he", "be"), ("had", "bad"),
        ("sound", "found"), ("same", "fame"), ("sit", "fit"), ("soul", "foul"), ("sight", "fight"), ("set", "let"),
        ("hear", "bear"), ("hand", "band"), ("heat", "beat"), ("this", "his"), ("when", "then"), ("were", "where")]
REALMAP = {a: b for a, b in REAL}
REALMAP.update({b: a for a, b in REAL})
LOOKALIKE = {"s": "f", "f": "s", "e": "c", "c": "e", "h": "b", "n": "u", "u": "n"}


def plain_page(t):
    """Page markup -> plain paragraphs (no page line, notes, images, tags or markers)."""
    out = []
    for ln in t.splitlines():
        s = ln.strip()
        if not s or re.match(r"\[\[(page|blank|image:|fn )", s) or s in ("<blockquote>", "</blockquote>", "<verse>", "</verse>"):
            continue
        s = re.sub(r"\[\[fnref [^\]]*\]\]", "", s)
        s = re.sub(r"\[\[corr ([^|\]]*)\|[^\]]*\]\]", r"\1", s)      # the audit compares the PRINTED reading
        s = re.sub(r"\[\[supplied ([^\]]*)\]\]", r"\1", s).replace("[[gap]]", "[…]")   # letters lost in the scan
        if s.startswith("|") and s.endswith("|"):
            continue
        s = re.sub(r"\[\[[a-z]+\]\] ?", "", s)
        s = re.sub(r"^#{1,3} ", "", s)
        s = re.sub(r"</?[a-z]+(?: [^>]*)?>", "", s)
        out.append(s)
    return "\n\n".join(out)


def plant(text, rng):
    """Return (text with planted errors, [seed dicts]). Each seed: kind, at (offset in new text), was, now."""
    seeds, taken = [], []

    def free(a, b):
        return all(b + 40 < x or a - 40 > y for x, y in taken)

    def apply(kind, a, b, new):
        nonlocal text
        was = text[a:b]
        text = text[:a] + new + text[b:]
        d = len(new) - (b - a)
        for s in seeds:
            if s["at"] > a:
                s["at"] += d
        taken[:] = [(x + d, y + d) if x > a else (x, y) for x, y in taken]
        taken.append((a, a + len(new)))
        seeds.append({"kind": kind, "at": a, "was": was, "now": new,
                      "context": text[max(0, a - 30):a + len(new) + 30].replace("\n", " ")})

    def pick(cands):
        cands = [c for c in cands if free(c[0], c[1])]
        return rng.choice(cands) if cands else None
    # 1 modernized spelling, else a lowered capital
    cands = []
    for pat, rep in MODERN:
        for m in re.finditer(pat, text):
            cands.append((m.start(), m.end(), m.expand(rep)))
    c = pick(cands)
    if c:
        apply("modernized", *c)
    else:
        c = pick([(m.start(1), m.end(1), m.group(1).lower()) for m in re.finditer(r"(?<=[a-z,] )([A-Z])(?=[a-z]{4,})", text)])
        if c:
            apply("capital", *c)
    # 2 look-alike letter inside a word of 6+ lower-case letters
    cands = []
    for m in re.finditer(r"\b[a-z]{6,}\b", text):
        idx = [i for i, ch in enumerate(m.group()) if ch in LOOKALIKE and 0 < i < len(m.group()) - 1]
        if idx:
            i = rng.choice(idx)
            cands.append((m.start() + i, m.start() + i + 1, LOOKALIKE[m.group()[i]]))
    c = pick(cands)
    if c:
        apply("letter", *c)
    # 2b a real word swapped for a look-alike real word
    c = pick([(m.start(), m.end(), REALMAP[m.group().lower()].capitalize() if m.group()[0].isupper() else REALMAP[m.group()])
              for m in re.finditer(r"\b[A-Za-z]+\b", text) if m.group().lower() in REALMAP])
    if c:
        apply("real word", *c)
    # 3 dropped small word
    c = pick([(m.start(), m.end(), " ") for m in re.finditer(r"(?<=[a-z]) (?:the|of|and|to|a|in) (?=[a-zA-Z])", text)])
    if c:
        apply("dropped word", *c)
    # 4 punctuation
    c = pick([(m.start(), m.end(), ";" if m.group() == "," else ",") for m in re.finditer(r"(?<=[a-z])[,;](?= [a-z])", text)])
    if c:
        apply("punctuation", *c)
    return text, seeds


def locate(given, text):
    """Span of a reported snippet in the text (spacing-insensitive, then fuzzy); None if not found."""
    g = re.sub(r"\s+", " ", given).strip()
    if not g:
        return None
    m = re.search(r"\s+".join(re.escape(w) for w in g.split(" ")), text)
    if m:
        return m.start(), m.end()
    sm = difflib.SequenceMatcher(None, text, g, autojunk=False)
    blk = sm.find_longest_match(0, len(text), 0, len(g))
    if blk.size >= max(8, 0.5 * len(g)):
        return max(0, blk.a - blk.b), blk.a - blk.b + len(g)
    return None


def call(prompt, model, cwd):
    last = None
    for _ in range(3):
        t0 = time.time()
        try:
            r = subprocess.run(
                ["claude", "-p", prompt, "--model", model, "--output-format", "json",
                 "--system-prompt", "You are a meticulous proofreader of transcriptions of scanned book pages. "
                 "Follow the user's format instructions exactly.",
                 "--tools", "Read", "--allowedTools", "Read", "--strict-mcp-config", "--setting-sources", ""],
                capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL, cwd=cwd)
            j = json.loads(r.stdout)
            if j.get("is_error") or not (j.get("result") or "").strip():
                raise RuntimeError(str(j.get("result"))[:300])
            return j["result"], {"seconds": round(time.time() - t0, 1), "cost": j.get("total_cost_usd")}
        except Exception as e:  # noqa: BLE001
            last = repr(e)[:300]
            if is_refusal(last):
                break
            time.sleep(5)
    return None, {"error": last}


def strips(img, d, name, n=3, overlap=0.05):
    from PIL import Image
    os.makedirs(d, exist_ok=True)
    im = Image.open(img)
    w, h = im.size
    out = []
    for k in range(n):
        f = os.path.join(d, f"{name}-{k + 1}.png")
        if not os.path.exists(f):
            im.crop((0, max(0, int(h * (k / n - overlap))), w, min(h, int(h * ((k + 1) / n + overlap))))).save(f)
        out.append(os.path.abspath(f))
    return out


def parse_findings(reply):
    out = []
    for ln in (reply or "").splitlines():
        ln = ln.strip().strip("`")
        if ln.startswith("{"):
            try:
                d = json.loads(ln)
                if d.get("given") and d.get("given") != d.get("print"):
                    out.append(d)
            except ValueError:
                pass
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages-dir", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--pages")
    ap.add_argument("--seed")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--conditions", default="whole")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--no-seeds", action="store_true")
    ap.add_argument("--min-chars", type=int, default=800)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rules = open(a.rules, encoding="utf-8").read()
    rules = rules.split("## Output format")[0]            # the proofreader needs the reading rules, not the markup
    seedname = a.seed or os.path.basename(os.path.abspath(a.pages_dir))

    def image_of(p):
        for ext in (".png", ".jpg", ".jpeg"):
            f = os.path.join(a.images, p + ext)
            if os.path.exists(f):
                return os.path.abspath(f)

    plan_f = os.path.join(a.out, "seeds.json")
    if os.path.exists(plan_f):
        plan = json.load(open(plan_f, encoding="utf-8"))
    else:
        texts = {}
        for f in sorted(os.listdir(a.pages_dir)):
            if re.fullmatch(r"p\d+[a-z]?\.txt", f):
                t = plain_page(open(os.path.join(a.pages_dir, f), encoding="utf-8").read())
                if len(t) >= a.min_chars and image_of(f[:-4]):
                    texts[f[:-4]] = t
        if a.pages:
            chosen = [p for p in a.pages.split(",") if p in texts]
        else:
            rng = random.Random(int(hashlib.sha1(seedname.encode()).hexdigest(), 16))
            chosen = sorted(rng.sample(sorted(texts), min(a.n, len(texts))))
        plan = {}
        for p in chosen:
            rng = random.Random(int(hashlib.sha1((seedname + p).encode()).hexdigest(), 16))
            given, seeds = (texts[p], []) if a.no_seeds else plant(texts[p], rng)
            open(os.path.join(a.out, p + ".given.txt"), "w", encoding="utf-8").write(given)
            plan[p] = seeds
        json.dump(plan, open(plan_f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    conds = a.conditions.split(",")
    jobs = []
    for p in plan:
        text = open(os.path.join(a.out, p + ".given.txt"), encoding="utf-8").read()
        img = image_of(p)
        if "whole" in conds:
            jobs.append(("whole", p, p, "one page", f"The page image is the file {img} — open it with the Read tool first.", text))
        if "strips" in conds:
            for k, f in enumerate(strips(img, os.path.join(a.out, "_strips"), p)):
                part = ("top", "middle", "bottom")[k]
                jobs.append(("strips", p, f"{p}-{k + 1}", "one page",
                             f"The image file {f} shows only the {part} third of the page, enlarged (the thirds overlap by a "
                             f"line or two). Open it with the Read tool first, find where its first line falls in the "
                             f"transcription, and check only the part of the transcription that this image shows; ignore the rest.", text))

    def work(job):
        cond, p, name, what, where, text = job
        d = os.path.join(a.out, cond)
        os.makedirs(d, exist_ok=True)
        f = os.path.join(d, name + ".txt")
        if os.path.exists(f):
            return None
        reply, rec = call(rules + TASK.format(what=what, where=where, text=text), a.model, a.out)
        if reply is not None:
            open(f, "w", encoding="utf-8").write(reply)
        rec.update(page=name, condition=cond, model=a.model)
        return rec
    with cf.ThreadPoolExecutor(a.workers) as ex, open(os.path.join(a.out, "log.jsonl"), "a", encoding="utf-8") as log:
        for rec in ex.map(work, jobs):
            if rec:
                log.write(json.dumps(rec) + "\n")
                log.flush()

    # ---- score
    rep, cand = [], ["condition\tpage\tsure\tgiven\tprint"]
    for cond in conds:
        found = {}
        total = {}
        ncand = 0
        for p, seeds in plan.items():
            text = open(os.path.join(a.out, p + ".given.txt"), encoding="utf-8").read()
            fs = []
            for f in sorted(os.listdir(os.path.join(a.out, cond))) if os.path.isdir(os.path.join(a.out, cond)) else []:
                if f.startswith(p) and f.endswith(".txt"):
                    fs += parse_findings(open(os.path.join(a.out, cond, f), encoding="utf-8").read())
            spans = [(locate(x["given"], text), x) for x in fs]
            hit_f = set()
            for s in seeds:
                total[s["kind"]] = total.get(s["kind"], 0) + 1
                for i, (sp, x) in enumerate(spans):
                    if sp and sp[0] - 12 <= s["at"] <= sp[1] + 12:
                        hit_f.add(i)
                        s.setdefault("found_by", [])
                        if cond not in s["found_by"]:
                            s["found_by"].append(cond)
                            found[s["kind"]] = found.get(s["kind"], 0) + 1
            seen = set()
            for i, (sp, x) in enumerate(spans):
                key = (x["given"], x.get("print"))
                if i not in hit_f and key not in seen:
                    seen.add(key)
                    ncand += 1
                    cand.append(f"{cond}\t{p}\t{x.get('sure', '')}\t{x['given']}\t{x.get('print', '')}")
        tot, fnd = sum(total.values()), sum(found.values())
        rep.append(f"{cond}: found {fnd} of {tot} planted errors ({100 * fnd / tot:.0f}%)" if tot else f"{cond}: no planted errors")
        for k in sorted(total):
            rep.append(f"    {k:14} {found.get(k, 0)}/{total[k]}")
        rep.append(f"    other differences reported (candidates to check on the scan): {ncand}")
    cost = 0
    for ln in open(os.path.join(a.out, "log.jsonl"), encoding="utf-8"):
        r = json.loads(ln)
        cost += r.get("cost") or 0
    errs = sum(1 for ln in open(os.path.join(a.out, "log.jsonl"), encoding="utf-8") if '"error"' in ln)
    rep.append(f"pages: {len(plan)} ({', '.join(plan)}); model {a.model}; cost ${cost:.2f}; failed calls {errs}")
    json.dump(plan, open(plan_f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(a.out, "report.txt"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    open(os.path.join(a.out, "candidates.tsv"), "w", encoding="utf-8").write("\n".join(cand) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
