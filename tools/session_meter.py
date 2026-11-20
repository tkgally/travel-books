#!/usr/bin/env python3
"""How full the session's context window is, and how long the session has run.

  session_meter.py            a few lines: tokens in the context now, the share of the window, whether the
                              conversation has been summarized (compacted), start time and hours elapsed
  session_meter.py --row      the same as the first cells of a row for notes/sessions.md

RESUME.md §"How long a session runs" says what to do with the numbers. Tom (2026-11-20): sessions run longer,
several books where possible, up to a reasonable fraction of the context window; he sets the routine's interval
from the clock time the sessions report.

Where the numbers come from: Claude Code writes the session's transcript to
~/.claude/projects/<folder>/<session id>.jsonl; each reply of the model records the tokens it was sent
(input + cache) and wrote. The context in use is that sum for the last reply of the main conversation
(subagents' replies, marked isSidechain, are not counted). The size of the window is not in the transcript:
it is WINDOW below unless the environment variable TRAVEL_BOOKS_CONTEXT_WINDOW or --window says otherwise.
Standard library only. Reads nothing but the transcript; prints no part of the conversation.
"""
import argparse, datetime, glob, json, os, sys

WINDOW = 1_000_000        # tokens: the window of the Opus models in Claude Code (model catalog, 2026-11-20); change here if that changes
DROP = 0.6                # a reply sent under 60% of the tokens of the one before = the conversation was summarized


def find_transcript(home=None, session_id=None):
    home = home or os.path.expanduser("~")
    session_id = session_id if session_id is not None else os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    base = os.path.join(home, ".claude", "projects")
    if session_id:
        hits = glob.glob(os.path.join(base, "*", session_id + ".jsonl"))
        if hits:
            return hits[0]
    hits = glob.glob(os.path.join(base, "*", "*.jsonl"))
    return max(hits, key=os.path.getmtime) if hits else None


def read(path):
    """-> dict: tokens (context at the last main reply), peak, compactions, start, end (datetimes or None)."""
    sizes, marks, first, last = [], 0, None, None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue                      # a line still being written
            if not isinstance(d, dict):
                continue
            ts = d.get("timestamp")
            if isinstance(ts, str):
                try:
                    t = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    first = first or t
                    last = t
                except ValueError:
                    pass
            if d.get("isSidechain"):
                continue
            if d.get("isCompactSummary") or d.get("subtype") == "compact_boundary":
                marks += 1
            u = (d.get("message") or {}).get("usage") if d.get("type") == "assistant" and isinstance(d.get("message"), dict) else None
            if isinstance(u, dict):
                n = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
                if n:
                    sizes.append(n)
    drops = sum(1 for a, b in zip(sizes, sizes[1:]) if a > 20_000 and b < a * DROP)
    return {"tokens": sizes[-1] if sizes else 0, "peak": max(sizes) if sizes else 0,
            "compactions": max(marks, drops), "start": first, "end": last}


def window(arg=None):
    v = arg or os.environ.get("TRAVEL_BOOKS_CONTEXT_WINDOW")
    try:
        return int(v) if v else WINDOW
    except ValueError:
        return WINDOW


def report(m, win, now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    pct = round(100 * m["tokens"] / win) if win else 0
    start = m["start"]
    hours = (now - start).total_seconds() / 3600 if start else 0.0
    return {"tokens": m["tokens"], "window": win, "percent": pct, "compactions": m["compactions"],
            "start": start.strftime("%Y-%m-%d %H:%M") if start else "?", "now": now.strftime("%H:%M"),
            "hours": round(hours, 1)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--transcript"); ap.add_argument("--window"); ap.add_argument("--row", action="store_true")
    a = ap.parse_args(argv)
    path = a.transcript or find_transcript()
    if not path or not os.path.exists(path):
        print("session_meter: no transcript found; use the rule in RESUME.md for a session without a meter")
        return 2
    r = report(read(path), window(a.window))
    if a.row:
        print(f"| {r['start']} | {r['now']} | {r['hours']} | {r['tokens']:,} ({r['percent']}%) | {r['compactions']} |")
    else:
        print(f"context: {r['tokens']:,} of {r['window']:,} tokens ({r['percent']}%)   summarized: {r['compactions']} time(s)")
        print(f"session: started {r['start']} UTC, now {r['now']} UTC, {r['hours']} h")
    return 0


if __name__ == "__main__":
    sys.exit(main())
