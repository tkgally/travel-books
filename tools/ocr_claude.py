#!/usr/bin/env python3
"""Transcribe page images with a Claude model through headless Claude Code.

Usage:
  ocr_claude.py --model opus --prompt prompts/transcribe.md --images DIR --out DIR
                [--pages 20-35] [--workers 4] [--context-text DIR]

One `claude -p` call per page; the model reads the image with the Read tool.
Writes <page>.txt and log.jsonl (seconds, API-equivalent cost) into --out.
Resumable: pages that already have a .txt are skipped.
Corrections mode (--corrections --context-text DRAFT_DIR, prompt = prompts/verify.md): the model replies
with a corrections list; it is saved as <page>.corr and applied to the draft.
Models: opus for drafts and judging, sonnet for the corrections pass. Never fable (CLAUDE.md).
"""
import argparse, concurrent.futures as cf, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections
from refusal import is_refusal


def strip_fences(t):
    t = t.strip()
    t = re.sub(r"^```[a-zA-Z]*\n", "", t)
    t = re.sub(r"\n```$", "", t)
    i = t.find("[[page")          # drop any preamble before the page marker
    if i > 0:
        t = t[i:]
    return t.strip() + "\n"


def make_halves(img, d, name, overlap=0.06):
    """Top and bottom halves (with overlap) so the model sees the text at higher resolution."""
    from PIL import Image
    os.makedirs(d, exist_ok=True)
    a, b = os.path.join(d, name + "-a.png"), os.path.join(d, name + "-b.png")
    if not (os.path.exists(a) and os.path.exists(b)):
        im = Image.open(img)
        w, h = im.size
        im.crop((0, 0, w, int(h * (0.5 + overlap)))).save(a)
        im.crop((0, int(h * (0.5 - overlap)), w, h)).save(b)
    return os.path.abspath(a), os.path.abspath(b)


def do_page(args, prompt, img):
    name = os.path.splitext(os.path.basename(img))[0]
    out = os.path.join(args.out, name + ".txt")
    if os.path.exists(out):
        return None
    p = prompt
    if args.context_text:
        ctx = os.path.join(args.context_text, name + ".txt")
        if args.corrections and not os.path.exists(ctx):
            # nothing to correct (e.g. the draft of this page was refused): no model call
            return {"page": name, "model": args.model, "error": "no draft to correct (skipped)"}
        if os.path.exists(ctx):
            p += "\n\n<draft>\n" + open(ctx, encoding="utf-8").read() + "\n</draft>\n"
    if args.halves:
        a, b = make_halves(img, os.path.join(args.out, "_halves"), name)
        p += (f"\n\nThe page is supplied as three image files; open all three with the Read tool. "
              f"{os.path.abspath(img)} is the whole page (use it for layout). "
              f"{a} is the top half and {b} the bottom half, at higher magnification "
              "(they overlap by a few lines: read the overlapping lines only once). Read the text from the halves. "
              + ("Then reply with the corrections list only." if args.corrections else
                 "Then reply with the transcription only (start your reply with the [[page N]] line)."))
    else:
        p += (f"\n\nThe page image is the file {os.path.abspath(img)} — open it with the Read tool, "
          + ("then reply with the corrections list only." if args.corrections else
             "then reply with the transcription only (start your reply with the [[page N]] line)."))
    last = None
    for attempt in range(3):
        t0 = time.time()
        try:
            r = subprocess.run(
                ["claude", "-p", p, "--model", args.model, "--output-format", "json",
                 # lean: own system prompt, only the Read tool, no settings/MCP -> about half the per-call cost
                 "--system-prompt", "You are a meticulous transcriber and proofreader of scanned book pages. "
                 "Follow the user's format instructions exactly.",
                 "--tools", "Read", "--allowedTools", "Read", "--strict-mcp-config", "--setting-sources", ""],
                capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL,
                cwd=args.out)
            j = json.loads(r.stdout)
            if j.get("is_error") or not (j.get("result") or "").strip():
                raise RuntimeError(str(j.get("result"))[:300])
            res, ncorr = j["result"], None
            if args.corrections:
                with open(out[:-4] + ".corr", "w", encoding="utf-8") as f:
                    f.write(res)
                res, ncorr, _ = corrections.apply(open(ctx, encoding="utf-8").read(), res)
                res = res.strip() + "\n"
            else:
                res = strip_fences(res)
            with open(out, "w", encoding="utf-8") as f:
                f.write(res)
            u = j.get("usage", {})
            return {"page": name, "model": args.model, "corrections": ncorr,
                    "seconds": round(time.time() - t0, 1),
                    "cost": j.get("total_cost_usd"),
                    "completion_tokens": u.get("output_tokens"),
                    "turns": j.get("num_turns"), "attempts": attempt + 1}
        except Exception as e:  # noqa
            last = repr(e)[:400]
            if is_refusal(last):
                break
        time.sleep(5)
    return {"page": name, "model": args.model, "error": last}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pages")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--context-text", default=None)
    ap.add_argument("--halves", action="store_true",
                    help="also give the model the top and bottom halves of the page (higher effective resolution)")
    ap.add_argument("--corrections", action="store_true",
                    help="model replies with a corrections list (tools/corrections.py) that is applied to the --context-text draft")
    args = ap.parse_args()
    if "fable" in args.model.lower() or "mythos" in args.model.lower():
        sys.exit("Fable is not used in this project without Tom's explicit permission (CLAUDE.md).")
    os.makedirs(args.out, exist_ok=True)
    prompt = open(args.prompt, encoding="utf-8").read()
    imgs = sorted(f for f in os.listdir(args.images)
                  if f.lower().endswith((".jpg", ".jpeg", ".png")))
    if args.pages:
        lo, hi = (int(x) for x in args.pages.split("-"))
        imgs = [f for f in imgs if lo <= int(re.findall(r"(\d+)", f)[-1]) <= hi]
    imgs = [os.path.join(args.images, f) for f in imgs]
    t0 = time.time()
    total = 0.0
    with cf.ThreadPoolExecutor(args.workers) as ex, \
            open(os.path.join(args.out, "log.jsonl"), "a") as log:
        for rec in ex.map(lambda i: do_page(args, prompt, i), imgs):
            if rec is None:
                continue
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
            if "error" in rec:
                print("FAIL", rec["page"], rec["error"], file=sys.stderr)
            else:
                total += rec.get("cost") or 0
    print(f"claude/{args.model}: {len(imgs)} pages, wall {time.time()-t0:.0f}s, cost ${total:.4f}")


if __name__ == "__main__":
    main()
