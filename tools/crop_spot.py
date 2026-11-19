#!/usr/bin/env python3
"""Crop the place on a page image where some words are printed, enlarged, to check a reading by eye.

  crop_spot.py IMAGE 'two or three words' OUT.png [--pad 60] [--scale 2]
  crop_spot.py IMAGE --box x0,y0,x1,y1 OUT.png          a region given as fractions of the page (0-1)

Tesseract is used only to find the words (it need not read them correctly: the best fuzzy match of the
word sequence is taken). Several matches -> all are stacked in OUT.png. No match -> exit status 1; then
use --box with a guess (e.g. 0,0.4,1,0.6 for the middle fifth of the page).
"""
import argparse, difflib, re, subprocess, sys
from PIL import Image


def words(image):
    tsv = subprocess.run(["tesseract", image, "-", "-l", "eng", "--psm", "6", "tsv"], capture_output=True, text=True).stdout
    out = []
    for r in tsv.splitlines()[1:]:
        r = r.split("\t")
        if len(r) == 12 and r[11].strip():
            out.append((r[11], int(r[6]), int(r[7]), int(r[8]), int(r[9])))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image"); ap.add_argument("text", nargs="?"); ap.add_argument("out")
    ap.add_argument("--box"); ap.add_argument("--pad", type=int, default=60); ap.add_argument("--scale", type=float, default=2)
    a = ap.parse_args()
    im = Image.open(a.image)
    boxes = []
    if a.box:
        x0, y0, x1, y1 = (float(v) for v in a.box.split(","))
        boxes.append((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    else:
        ws = words(a.image)
        want = [re.sub(r"\W", "", w).lower() for w in a.text.split()]
        want = [w for w in want if w]
        n = len(want)
        scored = []
        for i in range(len(ws) - n + 1):
            got = [re.sub(r"\W", "", w[0]).lower() for w in ws[i:i + n]]
            sc = difflib.SequenceMatcher(None, " ".join(want), " ".join(got)).ratio()
            scored.append((sc, i))
        scored.sort(reverse=True)
        for sc, i in scored[:3]:
            if sc < 0.7 or (boxes and sc < scored[0][0] - 0.05):
                break
            seg = ws[i:i + n]
            x0 = min(w[1] for w in seg); y0 = min(w[2] for w in seg)
            x1 = max(w[1] + w[3] for w in seg); y1 = max(w[2] + w[4] for w in seg)
            if y1 - y0 > 6 * max(w[4] for w in seg):      # words on different lines far apart: take the first line only
                y1 = y0 + 2 * seg[0][4]
            boxes.append((x0 - 4 * a.pad, y0 - a.pad, x1 + 4 * a.pad, y1 + a.pad))
    if not boxes:
        print("not found"); sys.exit(1)
    crops = []
    for b in boxes:
        c = im.crop((max(0, b[0]), max(0, b[1]), min(im.width, b[2]), min(im.height, b[3])))
        crops.append(c.resize((int(c.width * a.scale), int(c.height * a.scale)), Image.LANCZOS))
    out = Image.new("RGB", (max(c.width for c in crops), sum(c.height + 10 for c in crops)), "white")
    y = 0
    for c in crops:
        out.paste(c, (0, y)); y += c.height + 10
    out.save(a.out)
    print(f"{len(crops)} crop(s) -> {a.out}")


if __name__ == "__main__":
    main()
