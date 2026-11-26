#!/usr/bin/env python3
"""Move pictures that interrupt a paragraph to the end of that paragraph, in page files.

Cuts set into the text column split a paragraph in print. The corrections pass (and sometimes the draft) types the
picture at the exact line: `text… | [[image:]] + [[caption]] | [[cont]]rest…` or `| rest…` starting in lower case. The
editions read better with the picture after the paragraph, and preflight `image-splits` fails the second form. This
joins the two halves and puts the picture (with its caption) after the joined paragraph. Done by hand in *Vacation
Days*, *Sunny Lands and Seas*, *Norway Nights* and *The Land of the Muskeg* before it was a tool (2026-11-26).

    python3 tools/move_pictures.py PAGES_DIR [--pages p0059,p0107]    rewrites the files; prints what it moved
"""
import argparse, glob, os, re

CONT = re.compile(r"^\[\[cont\]\]\s*")


def _last_line(block):
    return block.split("\n")[-1]


def _is_text(line):
    """A line of running text (possibly after a [[cont]]), not markup such as a heading, picture or [[page]]."""
    return bool(line.strip()) and (not line.startswith(("[[", "#", "<verse>", "<blockquote>", "|")) or line.startswith("[[cont]]"))


def move(text):
    """(new text, number of pictures moved)."""
    tail = text[len(text.rstrip()):]
    blocks = text.rstrip().split("\n\n")
    out, i, n = [], 0, 0
    while i < len(blocks):
        b = blocks[i]
        if (b.startswith("[[image:") and out and i + 1 < len(blocks) and _is_text(_last_line(out[-1]))
                and (CONT.match(blocks[i + 1])
                     or (re.match(r"[a-z]", blocks[i + 1]) and not re.search(r"[.!?:;”’)\]—]\s*$", _last_line(out[-1]))))):
            out[-1] = out[-1].rstrip() + " " + CONT.sub("", blocks[i + 1]).lstrip()
            out.append(b)
            i, n = i + 2, n + 1
            continue
        out.append(b)
        i += 1
    return "\n\n".join(out) + tail, n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pages_dir")
    ap.add_argument("--pages", help="comma-separated leaf names (default: every page)")
    a = ap.parse_args()
    names = a.pages.split(",") if a.pages else [os.path.basename(f)[:-4] for f in sorted(glob.glob(os.path.join(a.pages_dir, "p*.txt")))]
    total = 0
    for leaf in names:
        f = os.path.join(a.pages_dir, leaf + ".txt")
        s = open(f, encoding="utf-8").read()
        new, n = move(s)
        if n:
            open(f, "w", encoding="utf-8").write(new)
            print(f"{leaf}: {n} picture(s) moved after the paragraph")
            total += n
    print(f"{total} picture(s) moved")


if __name__ == "__main__":
    main()
