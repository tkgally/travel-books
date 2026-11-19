#!/usr/bin/env python3
"""Compare page-markup transcriptions from several models/workflows.

  score.py consensus --runs RUNS_DIR --voters a,b,c --lang en|ja --out GOLD_DIR
      Build a per-page consensus text by character-level majority vote among
      the voter runs (RUNS_DIR/<voter>/pNNN.txt). Writes GOLD_DIR/pNNN.txt
      (normalized text) and GOLD_DIR/contested.tsv listing every spot where the
      vote was not decisive, for manual adjudication against the page image.

  score.py score --runs RUNS_DIR --gold GOLD_DIR --lang en|ja [--fixes FILE]
      Print character error rate (CER) of every run against the gold text, plus
      ruby (furigana) / italic recall+precision against the voters' majority.

Normalization strips page markup so that only the transcribed characters are
compared: tags, [[markers]], heading #s; whitespace is collapsed (en) or removed
(ja). Ruby <rt> text is excluded from the base text and scored separately.
"""
import argparse, collections, difflib, glob, json, os, re, sys, unicodedata


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def strip_markup(t, lang, keep_rt=False):
    t = re.sub(r"\[\[page [^\]]*\]\]", "", t)
    t = re.sub(r"\[\[image:[^\]]*\]\]", "", t)
    t = re.sub(r"\[\[fnref ([^\]]*)\]\]", "", t)
    t = re.sub(r"\[\[fn ([^\]]*)\]\]", r"\1 ", t)
    t = re.sub(r"\[\[[a-z]+\]\]", "", t)
    if not keep_rt:
        t = re.sub(r"<rt>.*?</rt>", "", t)
    # small caps: case is a typographic choice, compare case-insensitively
    t = re.sub(r"<sc>(.*?)</sc>", lambda m: m.group(1).lower(), t, flags=re.S)
    t = re.sub(r"</?[a-zA-Z][^>]*>", "", t)
    t = re.sub(r"^#+ ", "", t, flags=re.M)
    t = re.sub(r"^\|[-| :]+\|$", "", t, flags=re.M)
    return t


def normalize(t, lang):
    t = strip_markup(t, lang)
    if lang == "en":
        t = t.replace(" ", " ")
        t = re.sub(r"\.\s\.\s\.", "...", t).replace("…", "...")
        t = t.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        t = re.sub(r"\s+", " ", t).strip()
    else:
        # full-width ASCII -> half-width, but keep full-width punctuation distinct
        out = []
        for ch in t:
            o = ord(ch)
            if 0xFF10 <= o <= 0xFF19 or 0xFF21 <= o <= 0xFF3A or 0xFF41 <= o <= 0xFF5A:
                ch = chr(o - 0xFEE0)
            out.append(ch)
        t = "".join(out)
        t = t.replace("，", "、").replace(",", "、").replace("．", "。")
        t = re.sub(r"[─—―‐－-]", "―", t)
        t = t.replace("…", "…").replace("・・・", "…")
        t = re.sub(r"[()]", lambda m: "（" if m.group() == "(" else "）", t)
        t = re.sub(r"\s+", "", t)
        # variant glyph pairs that cannot be told apart reliably in a 300-dpi scan;
        # which one to use is a per-book policy decision, not an OCR error
        for a, b in VARIANTS:
            t = t.replace(a, b)
    return t


VARIANTS = [("焰", "焔"), ("唧", "喞"), ("瘦", "痩"), ("麵", "麺"), ("剌", "刺"), ("Ⅰ", "I"), ("Ⅱ", "II")]


def rubies(t):
    return re.findall(r"<ruby>(.*?)<rt>(.*?)</rt></ruby>", t)


def italics(t):
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip(" .,;:!?\"'“”‘’()")
            for x in re.findall(r"<i>(.*?)</i>", t, flags=re.S)]


def emphs(t):
    return [re.sub(r"<[^>]+>", "", x) for x in re.findall(r"<em>(.*?)</em>", t, flags=re.S)]


# ---------- consensus ----------

def mapper(ops):
    def start(a):
        for tag, i1, i2, j1, j2 in ops:
            if i1 == a:
                return j1
            if tag == "equal" and i1 < a < i2:
                return j1 + (a - i1)
        return ops[-1][4] if ops else 0

    def end(b):
        r = None
        for tag, i1, i2, j1, j2 in ops:
            if i2 == b:
                r = j2
            elif tag == "equal" and i1 < b < i2:
                r = j1 + (b - i1)
        return r if r is not None else 0
    return start, end


def consensus_page(texts):
    """texts: dict voter -> normalized text. Returns (gold, contested list)."""
    names = list(texts)
    # pivot: the text closest to the median length
    pivot_name = sorted(names, key=lambda n: len(texts[n]))[len(names) // 2]
    P = texts[pivot_name]
    opsets = {}
    blocks = []
    for n in names:
        if n == pivot_name:
            opsets[n] = [("equal", 0, len(P), 0, len(P))]
            continue
        sm = difflib.SequenceMatcher(None, P, texts[n], autojunk=False)
        ops = sm.get_opcodes()
        opsets[n] = ops
        for tag, i1, i2, j1, j2 in ops:
            if tag != "equal":
                blocks.append((i1, i2))
    blocks.sort()
    merged = []
    for a, b in blocks:
        if merged and a <= merged[-1][1] and not (a == merged[-1][1] and a == b and merged[-1][0] == merged[-1][1] and a != merged[-1][0]):
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    maps = {n: mapper(opsets[n]) for n in names}
    gold, pos, contested = [], 0, []
    for a, b in merged:
        gold.append(P[pos:a])
        votes = collections.Counter()
        who = collections.defaultdict(list)
        for n in names:
            s, e = maps[n]
            j1, j2 = s(a), e(b)
            v = texts[n][j1:j2] if j2 >= j1 else ""
            votes[v] += 1
            who[v].append(n)
        top, cnt = votes.most_common(1)[0]
        gold.append(top)
        if cnt * 3 < len(names) * 2:   # less than two-thirds agree
            ctx = P[max(0, a - 12):a] + "【" + top + "】" + P[b:b + 12]
            contested.append({"ctx": ctx, "votes": {v: who[v] for v in votes}})
        pos = b
    gold.append(P[pos:])
    return "".join(gold), contested


def cmd_consensus(a):
    voters = a.voters.split(",")
    os.makedirs(a.out, exist_ok=True)
    pages = sorted({os.path.basename(p) for v in voters
                    for p in glob.glob(os.path.join(a.runs, v, "p*.txt"))})
    allc = []
    for pg in pages:
        texts = {}
        for v in voters:
            f = os.path.join(a.runs, v, pg)
            if os.path.exists(f):
                texts[v] = normalize(read(f), a.lang)
        gold, contested = consensus_page(texts)
        with open(os.path.join(a.out, pg), "w", encoding="utf-8") as f:
            f.write(gold)
        for c in contested:
            allc.append((pg, c))
    with open(os.path.join(a.out, "contested.tsv"), "w", encoding="utf-8") as f:
        for pg, c in allc:
            f.write(pg + "\t" + c["ctx"] + "\t" + json.dumps(c["votes"], ensure_ascii=False) + "\n")
    print(f"{len(pages)} pages, {len(allc)} contested spots -> {a.out}/contested.tsv")


# ---------- scoring ----------

def edit_ops(g, h):
    sm = difflib.SequenceMatcher(None, g, h, autojunk=False)
    sub = ins = dele = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace":
            sub += max(i2 - i1, j2 - j1)
        elif tag == "delete":
            dele += i2 - i1
        elif tag == "insert":
            ins += j2 - j1
    return sub, ins, dele


def bag_pr(ref, hyp):
    r, h = collections.Counter(ref), collections.Counter(hyp)
    tp = sum((r & h).values())
    return tp, sum(r.values()), sum(h.values())


def apply_fixes(gold, fixes, pg):
    for p, old, new in fixes:
        if p == pg:
            if old not in gold:
                print(f"  (fix not applicable on {pg}: {old!r})", file=sys.stderr)
            gold = gold.replace(old, new)
    return gold


def cmd_score(a):
    fixes = []
    if a.fixes and os.path.exists(a.fixes):
        for line in read(a.fixes).splitlines():
            if line.strip() and not line.startswith("#"):
                p, old, new = line.split("\t")
                fixes.append((p, old, new))
    gold = {os.path.basename(p): apply_fixes(read(p), fixes, os.path.basename(p))
            for p in glob.glob(os.path.join(a.gold, "p*.txt"))}
    voters = a.voters.split(",") if a.voters else []
    # majority ruby / italic reference from voters
    ref_feat = {}
    for pg in gold:
        cnt = collections.Counter()
        n = 0
        for v in voters:
            f = os.path.join(a.runs, v, pg)
            if os.path.exists(f):
                n += 1
                t = read(f)
                feats = [("r",) + x for x in rubies(t)] if a.lang == "ja" else []
                feats += [("i", x) for x in italics(t)] + [("e", x) for x in emphs(t)]
                for k, c in collections.Counter(feats).items():
                    cnt[k] += 1  # presence vote
        ref_feat[pg] = [k for k, c in cnt.items() if n and c * 2 > n]
    rows = []
    for run in sorted(os.listdir(a.runs)):
        d = os.path.join(a.runs, run)
        if not os.path.isdir(d) or run.startswith("_"):
            continue
        tot = err = 0
        s = i = dl = 0
        ftp = fref = fhyp = 0
        npages = 0
        for pg, g in gold.items():
            f = os.path.join(d, pg)
            if not os.path.exists(f):
                continue
            npages += 1
            raw = read(f)
            h = normalize(raw, a.lang)
            x, y, z = edit_ops(g, h)
            s += x; i += y; dl += z
            tot += len(g)
            feats = [("r",) + x for x in rubies(raw)] if a.lang == "ja" else []
            feats += [("i", x) for x in italics(raw)] + [("e", x) for x in emphs(raw)]
            tp, nr, nh = bag_pr(ref_feat[pg], set(feats))
            ftp += tp; fref += nr; fhyp += nh
        if not npages:
            continue
        secs = cost = 0.0
        lp = os.path.join(d, "log.jsonl")
        if os.path.exists(lp):
            for line in read(lp).splitlines():
                r = json.loads(line)
                secs += r.get("seconds") or 0
                cost += r.get("cost") or 0
        rows.append((100.0 * (s + i + dl) / max(tot, 1), run, npages, tot, s, i, dl,
                     ftp, fref, fhyp, secs, cost))
    print(f"{'run':34} pg  chars   CER%   sub  ins  del | fmt recall  prec | s/page  $/page")
    for cer, run, npg, tot, s, i, dl, ftp, fref, fhyp, secs, cost in sorted(rows):
        rec = f"{100*ftp/fref:5.1f}%" if fref else "   - "
        prec = f"{100*ftp/fhyp:5.1f}%" if fhyp else "   - "
        print(f"{run:34} {npg:2} {tot:6} {cer:6.3f} {s:5} {i:4} {dl:4} |    {rec} {prec} |"
              f" {secs/npg:6.1f} {cost/npg:7.4f}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("consensus")
    c.add_argument("--runs", required=True); c.add_argument("--voters", required=True)
    c.add_argument("--lang", required=True); c.add_argument("--out", required=True)
    s = sub.add_parser("score")
    s.add_argument("--runs", required=True); s.add_argument("--gold", required=True)
    s.add_argument("--lang", required=True); s.add_argument("--voters", default="")
    s.add_argument("--fixes", default=None)
    a = ap.parse_args()
    {"consensus": cmd_consensus, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
