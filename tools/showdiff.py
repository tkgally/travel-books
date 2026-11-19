#!/usr/bin/env python3
"""showdiff.py GOLD_DIR RUN_DIR en|ja [max] — list each difference (gold -> run) with a little context."""
import sys, os, glob, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import normalize, read
gold, run, lang = sys.argv[1:4]
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 60
n = 0
for gp in sorted(glob.glob(os.path.join(gold, "p*.txt"))):
    pg = os.path.basename(gp)
    rp = os.path.join(run, pg)
    if not os.path.exists(rp):
        continue
    g, h = read(gp), normalize(read(rp), lang)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, g, h, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        n += 1
        if n <= mx:
            a, b = g[i1:i2], h[j1:j2]
            if len(a) > 40: a = a[:20] + f"…({len(a)})…" + a[-10:]
            if len(b) > 40: b = b[:20] + f"…({len(b)})…" + b[-10:]
            print(f"{pg} {g[max(0,i1-10):i1]}[{a} -> {b}]{g[i2:i2+10]}")
print(n, "differences")
