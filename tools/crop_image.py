#!/usr/bin/env python3
"""Crop an illustration from a full-size leaf image into the book's images directory.

  crop_image.py FULL_LEAF.jpg OUT.jpg x0,y0,x1,y1 [--max 1600] [--quality 85] [--gray]
The box is in fractions of the leaf (0-1): work it out on the small page image, then LOOK at the result.
Longest side is reduced to --max pixels. Naming: images/pNNNN-k.jpg = k-th [[image:]] on leaf pNNNN;
images/cover.jpg = the front cover (or the title page if the binding is a plain library one).
"""
import argparse
from PIL import Image, ImageOps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("box")
    ap.add_argument("--max", type=int, default=1600); ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--gray", action="store_true", help="engravings and line drawings: greyscale with contrast stretched")
    a = ap.parse_args()
    im = Image.open(a.src)
    x0, y0, x1, y1 = (float(v) for v in a.box.split(","))
    im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    if a.gray:
        im = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    else:
        im = im.convert("RGB")
    im.thumbnail((a.max, a.max), Image.LANCZOS)
    im.save(a.out, "JPEG", quality=a.quality, optimize=True)
    print(a.out, im.size)


if __name__ == "__main__":
    main()
