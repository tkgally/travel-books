#!/usr/bin/env python3
"""Transcribe page images with a vision model through OpenRouter.

Usage:
  ocr_openrouter.py --model google/gemini-... --prompt prompts/en.md \
      --images DIR --out DIR [--pages 20-35] [--workers 6] [--context-text DIR]

Writes one <page>.txt per image plus log.jsonl (latency, tokens, cost per page)
into --out. Pages that already have a .txt are skipped, so runs are resumable.

--context-text DIR: for each page image NAME.jpg, if DIR/NAME.txt exists its
contents are appended to the prompt as a draft transcription to be corrected
against the image (used for "cheap OCR first, frontier model cleans up" workflows).
--no-image: send only the draft text (text-only cleanup, no vision).

Needs OPENROUTER_API_KEY. Never prints the key.

Spending rule (CLAUDE.md): OpenRouter is for second opinions on difficult scans only, at most $3.00 a
day for the whole project. Every run appends its cost to data/openrouter-spend.jsonl (commit it); a run
is refused when today's recorded spending plus --estimate would pass the limit, and stops early when
the limit is reached. --estimate (dollars for this run) is required.
"""
import argparse, base64, concurrent.futures as cf, json, os, re, sys, time
import urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrections

API = "https://openrouter.ai/api/v1/chat/completions"
DAILY_LIMIT = 3.00
LEDGER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "openrouter-spend.jsonl")


def spent_today(ledger=None, today=None):
    import datetime
    today = today or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    total = 0.0
    if os.path.exists(ledger or LEDGER):
        for ln in open(ledger or LEDGER, encoding="utf-8"):
            if ln.strip():
                r = json.loads(ln)
                if r.get("date") == today:
                    total += r.get("cost") or 0
    return total


def record(cost, model, what, ledger=None):
    import datetime
    os.makedirs(os.path.dirname(ledger or LEDGER), exist_ok=True)
    with open(ledger or LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps({"date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
                            "cost": round(cost, 4), "model": model, "what": what}) + "\n")


def call(model, prompt, image_path, max_tokens, reasoning, timeout=600):
    content = [{"type": "text", "text": prompt}]
    if image_path:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        mime = "image/png" if image_path.endswith(".png") else "image/jpeg"
        content.append({"type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"}})
    body = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "usage": {"include": True},
    }
    if reasoning:
        body["reasoning"] = {"effort": reasoning}
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def strip_fences(t):
    t = t.strip()
    t = re.sub(r"^```[a-zA-Z]*\n", "", t)
    t = re.sub(r"\n```$", "", t)
    return t.strip() + "\n"


def do_page(args, prompt, img):
    name = os.path.splitext(os.path.basename(img))[0]
    out = os.path.join(args.out, name + ".txt")
    if os.path.exists(out):
        return None
    p = prompt
    if args.context_text:
        ctx = os.path.join(args.context_text, name + ".txt")
        if os.path.exists(ctx):
            p += "\n\n<draft>\n" + open(ctx, encoding="utf-8").read() + "\n</draft>\n"
    last = None
    for attempt in range(4):
        t0 = time.time()
        try:
            r = call(args.model, p, None if args.no_image else img,
                     args.max_tokens, args.reasoning)
            if "error" in r:
                raise RuntimeError(json.dumps(r["error"])[:400])
            msg = r["choices"][0]["message"]["content"]
            if not args.corrections and (not msg or not msg.strip()):
                raise RuntimeError("empty content; finish=" +
                                   str(r["choices"][0].get("finish_reason")))
            dt = time.time() - t0
            u = r.get("usage", {})
            ncorr = None
            if args.corrections:
                with open(out[:-4] + ".corr", "w", encoding="utf-8") as f:
                    f.write(msg)
                msg, ncorr, _ = corrections.apply(open(ctx, encoding="utf-8").read(), msg)
            with open(out, "w", encoding="utf-8") as f:
                f.write(strip_fences(msg))
            return {"corrections": ncorr,"page": name, "model": args.model, "seconds": round(dt, 1),
                    "prompt_tokens": u.get("prompt_tokens"),
                    "completion_tokens": u.get("completion_tokens"),
                    "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
                    "cost": u.get("cost"),
                    "finish": r["choices"][0].get("finish_reason"),
                    "attempts": attempt + 1}
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300]!r}"
        except Exception as e:  # noqa
            last = repr(e)[:400]
        time.sleep(3 * (attempt + 1))
    return {"page": name, "model": args.model, "error": last}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pages", help="e.g. 20-35 (matches trailing number in filename)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--reasoning", default=None, help="minimal|low|medium|high")
    ap.add_argument("--context-text", default=None)
    ap.add_argument("--corrections", action="store_true",
                    help="model replies with a corrections list (tools/corrections.py) that is applied to the --context-text draft")
    ap.add_argument("--no-image", action="store_true")
    ap.add_argument("--estimate", type=float, required=True, help="expected cost of this run in dollars")
    ap.add_argument("--what", default="", help="book and purpose, for the spending ledger")
    args = ap.parse_args()
    before = spent_today()
    if before + args.estimate > DAILY_LIMIT:
        sys.exit(f"refused: ${before:.2f} already spent today (UTC) + estimate ${args.estimate:.2f} > daily limit ${DAILY_LIMIT:.2f}")

    os.makedirs(args.out, exist_ok=True)
    prompt = open(args.prompt, encoding="utf-8").read()
    imgs = sorted(f for f in os.listdir(args.images)
                  if f.lower().endswith((".jpg", ".jpeg", ".png")))
    if args.pages:
        lo, hi = (int(x) for x in args.pages.split("-"))
        imgs = [f for f in imgs
                if lo <= int(re.findall(r"(\d+)", f)[-1]) <= hi]
    imgs = [os.path.join(args.images, f) for f in imgs]

    t0 = time.time()
    total = 0.0
    with cf.ThreadPoolExecutor(args.workers) as ex, \
            open(os.path.join(args.out, "log.jsonl"), "a") as log:
        def guarded(i):
            if before + total >= DAILY_LIMIT:
                return {"page": os.path.basename(i), "model": args.model, "error": "daily OpenRouter limit reached; not sent"}
            return do_page(args, prompt, i)
        for rec in ex.map(guarded, imgs):
            if rec is None:
                continue
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
            if "error" in rec:
                print("FAIL", rec["page"], rec["error"], file=sys.stderr)
            else:
                total += rec.get("cost") or 0
    record(total, args.model, args.what or args.out)
    print(f"{args.model}: {len(imgs)} pages, wall {time.time()-t0:.0f}s, cost ${total:.4f}; today so far ${before + total:.2f} of ${DAILY_LIMIT:.2f}")


if __name__ == "__main__":
    main()
