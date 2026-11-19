#!/usr/bin/env python3
"""Crop an illustration from a full-size leaf image into the book's images directory.

  crop_image.py FULL_LEAF.jpg OUT.jpg x0,y0,x1,y1 [--max 1600] [--quality 85] [--gray] [--rotate 90|180|270]
The box is in fractions of the leaf (0-1), as the leaf is scanned: work it out on the small page image, then LOOK
at the result. A plate printed sideways is turned upright after cropping: --rotate N turns it N degrees
counter-clockwise (caption reading bottom to top along the right edge: 270; top to bottom along the left: 90).
Longest side is reduced to --max pixels. Naming: images/pNNNN-k.jpg = k-th [[image:]] on leaf pNNNN;
images/cover.jpg = the front cover (or the title page if the binding is a plain library one).
"""
import argparse
from PIL import Image, ImageOps

ROTATE = {0: None, 90: Image.Transpose.ROTATE_90, 180: Image.Transpose.ROTATE_180, 270: Image.Transpose.ROTATE_270}


def crop(im, box, gray=False, rotate=0, longest=1600):
    """Crop box (fractions of the leaf), optionally greyscale, turn upright, reduce: returns a new image."""
    x0, y0, x1, y1 = box
    im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im = ImageOps.autocontrast(im.convert("L"), cutoff=1) if gray else im.convert("RGB")
    if ROTATE[rotate] is not None:
        im = im.transpose(ROTATE[rotate])
    im.thumbnail((longest, longest), Image.LANCZOS)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("box")
    ap.add_argument("--max", type=int, default=1600); ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--gray", action="store_true", help="engravings and line drawings: greyscale with contrast stretched")
    ap.add_argument("--rotate", type=int, default=0, choices=sorted(ROTATE),
                    help="degrees counter-clockwise, to turn a plate printed sideways upright")
    a = ap.parse_args()
    box = tuple(float(v) for v in a.box.split(","))
    im = crop(Image.open(a.src), box, gray=a.gray, rotate=a.rotate, longest=a.max)
    im.save(a.out, "JPEG", quality=a.quality, optimize=True)
    print(a.out, im.size)


if __name__ == "__main__":
    main()
