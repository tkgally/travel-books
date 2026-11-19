#!/usr/bin/env python3
"""A draft for the pages whose transcription the API's output filter refused.

  ocr_fallback.py --images PAGES_DIR --draft DRAFT_DIR [--pages 116-118,128-129] [--model opus] [--workers 4]

Why: the filter refuses to let a Claude model type out certain pages (ordinary prose; the same pages every
time, whichever model is asked, and it ends a SESSION that tries to type one itself). It does not refuse a
corrections list. So for those pages no model types the page:
  1. tesseract reads the page image (machine OCR, no model)  ->  DRAFT_DIR/_ocr/pNNNN.txt, in rough page markup;
  2. the draft model (Opus) proofreads that against the image in corrections mode (prompts/verify.md), as
     ocr_claude.py --corrections does  ->  DRAFT_DIR/pNNNN.txt and pNNNN.corr.
The page then goes through the Sonnet corrections pass, the judge and the audit like any other page, so it
still has two differently biased readings. The pages done this way are listed in DRAFT_DIR/fallback.json:
name them in the book's log and put them in the audit (audit_sample.py --pages).

Without --pages, the pages are those that DRAFT_DIR/log.jsonl records as refused and that have no .txt.
A page refused here as well stays without a .txt (preflight `leaves` lists it): the book waits.
"""
import argparse, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refusal import is_refusal

HERE = os.path.dirname(os.path.abspath(__file__))


def to_markup(raw):
    """Tesseract's plain text -> rough page markup: one line per paragraph, line-end hyphens joined, a
    [[page ?]] line. Running heads, the page number, italics, [[cont]] and notes are left to the proofreader."""
    paras = []
    for p in re.split(r"\n[ \t]*\n", raw):
        s = ""
        for ln in (x.strip() for x in p.splitlines()):
            if not ln:
                continue
            if re.search(r"\w-$", s):
                s = s[:-1] + ln if ln[:1].islower() else s + ln      # inter-|national; twenty-|Third stays
            else:
                s = (s + " " + ln).strip()
        if s:
            paras.append(s)
    return "[[page ?]]\n\n" + "\n\n".join(paras) + "\n"


def refused_pages(draft_dir):
    """Leaf names whose last record in log.jsonl is a filter refusal and that have no .txt."""
    last = {}
    log = os.path.join(draft_dir, "log.jsonl")
    if os.path.exists(log):
        for ln in open(log, encoding="utf-8"):
            try:
                r = json.loads(ln)
            except ValueError:
                continue
            last[r.get("page")] = r
    return sorted(p for p, r in last.items()
                  if p and is_refusal(r.get("error")) and not os.path.exists(os.path.join(draft_dir, p + ".txt")))


def parse_pages(spec):
    """'116-118,128' -> [116, 117, 118, 128]"""
    out = []
    for part in spec.split(","):
        lo, _, hi = part.strip().lstrip("p").partition("-")
        out += range(int(lo), int(hi.lstrip("p") or lo) + 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True)
    ap.add_argument("--draft", required=True)
    ap.add_argument("--pages")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--prompt", default=os.path.join(HERE, "..", "prompts", "verify.md"))
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    names = [f"p{n:04d}" for n in parse_pages(a.pages)] if a.pages else refused_pages(a.draft)
    names = [n for n in names if not os.path.exists(os.path.join(a.draft, n + ".txt"))]
    if not names:
        print("no refused pages without a draft")
        return
    ocr = os.path.join(a.draft, "_ocr")
    os.makedirs(ocr, exist_ok=True)
    for n in names:
        img = next((os.path.join(a.images, n + e) for e in (".jpg", ".jpeg", ".png")
                    if os.path.exists(os.path.join(a.images, n + e))), None)
        if img is None:
            sys.exit(f"no image for {n} in {a.images}")
        raw = subprocess.run(["tesseract", img, "-", "--psm", "4", "-l", "eng"],
                             capture_output=True, text=True, check=True).stdout
        with open(os.path.join(ocr, n + ".txt"), "w", encoding="utf-8") as f:
            f.write(to_markup(raw))
    spec = ",".join(str(int(n[1:])) for n in names)
    subprocess.run([sys.executable, os.path.join(HERE, "ocr_claude.py"), "--model", a.model, "--prompt", a.prompt,
                    "--images", a.images, "--out", a.draft, "--corrections", "--context-text", ocr,
                    "--pages", spec, "--workers", str(a.workers)], check=False)
    done = [n for n in names if os.path.exists(os.path.join(a.draft, n + ".txt"))]
    fb = os.path.join(a.draft, "fallback.json")
    rec = json.load(open(fb, encoding="utf-8")) if os.path.exists(fb) else {"method": "tesseract, then corrections by the draft model", "pages": []}
    rec["pages"] = sorted(set(rec["pages"]) | set(done))
    json.dump(rec, open(fb, "w", encoding="utf-8"), indent=1)
    left = [n for n in names if n not in done]
    print(f"fallback draft: {len(done)} done ({', '.join(done)})" + (f"; STILL WITHOUT A DRAFT: {', '.join(left)}" if left else ""))
    print("next: normalize.py on the draft; name these pages in the log; audit them with audit_sample.py --pages " + ",".join(done))


if __name__ == "__main__":
    main()
