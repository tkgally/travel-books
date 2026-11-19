#!/usr/bin/env python3
"""Contact sheets of the page images, to look at the whole book (page map, completeness, illustrations).

  contact_sheets.py PAGES_DIR OUT_DIR [--per 40] [--cols 8] [--thumb 300]
Writes OUT_DIR/sheet-01.jpg … with the leaf name under each thumbnail. Look at ALL of them.
"""
import argparse, os, re
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages"); ap.add_argument("out")
    ap.add_argument("--per", type=int, default=40); ap.add_argument("--cols", type=int, default=8); ap.add_argument("--thumb", type=int, default=300)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    files = sorted(f for f in os.listdir(a.pages) if re.fullmatch(r"p\d+[a-z]?\.(jpg|png)", f))
    for s in range(0, len(files), a.per):
        chunk = files[s:s + a.per]
        tw, th = int(a.thumb * 0.68), a.thumb
        rows = -(-len(chunk) // a.cols)
        sheet = Image.new("L", (a.cols * (tw + 8), rows * (th + 22)), 255)
        d = ImageDraw.Draw(sheet)
        for i, f in enumerate(chunk):
            im = Image.open(os.path.join(a.pages, f)).convert("L")
            im.thumbnail((tw, th))
            x, y = (i % a.cols) * (tw + 8), (i // a.cols) * (th + 22)
            sheet.paste(im, (x, y))
            d.text((x + 2, y + th + 4), f[:-4], fill=0)
        sheet.save(os.path.join(a.out, f"sheet-{s // a.per + 1:02d}.jpg"), quality=70)
    print(f"{-(-len(files) // a.per)} sheets for {len(files)} pages in {a.out}")


if __name__ == "__main__":
    main()
