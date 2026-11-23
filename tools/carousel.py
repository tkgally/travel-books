#!/usr/bin/env python3
"""The carousel of covers on the home page (Tom, 2026-11-21): which books are in it, and their thumbnails.

  carousel.py check                     published books not yet in the carousel, thumbnails that are missing, belong to
                                        no book, or were made from a picture that has since changed; exit 1 if there
                                        is anything to do
  carousel.py add SLUG --kind cover|title|page [--note TEXT]
                                        make site/carousel/SLUG.jpg from books/SLUG/images/cover.jpg and record it

The picture of a book is one picture, books/SLUG/images/cover.jpg: it is shown on the book's own page, it is the
cover of the EPUB, and the thumbnail is made from it (Tom, 2026-11-21: the two must be the same). The rule for
choosing it (notes/site.md §"The carousel"; notes/workflow.md §5): the cover if the title is clearly readable on it
(--kind cover), otherwise the title page (title); if neither has a readable title, the first page of the first
chapter or a similar representative page (page). Someone has to look at the picture: this tool does not judge it.
The record is data/carousel.json; build_site.py puts into the home page the books that are published, are in the
record and have their thumbnail, and words the alt text of the picture on the book's page by the kind. Needs Pillow.
"""
import argparse, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BOX = (300, 450)        # the thumbnail fits in this: shown about 7rem wide, so enough for a screen of double density
QUALITY = 80
KINDS = {"cover": "cover", "title": "title page", "page": "page of the text"}


def paths(repo=REPO):
    return os.path.join(repo, "data", "carousel.json"), os.path.join(repo, "site", "carousel"), os.path.join(repo, "books")


def load(repo=REPO):
    f = paths(repo)[0]
    d = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    d.setdefault("books", {})
    return d


def save(d, repo=REPO):
    d = {"books": dict(sorted(d["books"].items()))}
    os.makedirs(os.path.dirname(paths(repo)[0]), exist_ok=True)
    with open(paths(repo)[0], "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write("\n")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def thumbnail(src, dest):
    """Write the thumbnail (JPEG, no metadata, the same bytes for the same picture); return its (width, height)."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im.thumbnail(BOX, Image.LANCZOS)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, "JPEG", quality=QUALITY, optimize=True)
    return im.size


def add(slug, kind, note="", repo=REPO):
    _, thumbs, books = paths(repo)
    if not os.path.exists(os.path.join(books, slug, "book.json")):
        raise SystemExit(f"no published book {slug}")
    src = os.path.join(books, slug, "images", "cover.jpg")
    if not os.path.exists(src):
        raise SystemExit(f"no picture {src}")
    w, h = thumbnail(src, os.path.join(thumbs, slug + ".jpg"))
    d = load(repo)
    d["books"][slug] = {"image": KINDS[kind], "width": w, "height": h, "sha256": sha(src)}
    if note:
        d["books"][slug]["note"] = note
    save(d, repo)
    return w, h


def check(repo=REPO):
    """What is to be done, as lines of text (none: the carousel is up to date)."""
    _, thumbs, books = paths(repo)
    d = load(repo)
    published = sorted(s for s in (os.listdir(books) if os.path.isdir(books) else [])
                       if os.path.exists(os.path.join(books, s, "book.json")))
    out = [f"not decided: {s} (look at books/{s}/images/cover.jpg: is the title readable? then carousel.py add)" for s in published
           if s not in d["books"]]
    out += [f"in the record but not a published book: {s}" for s in sorted(d["books"]) if s not in published]
    out += [f"thumbnail missing: site/carousel/{s}.jpg" for s in sorted(d["books"]) if not os.path.exists(os.path.join(thumbs, s + ".jpg"))]
    for s in sorted(d["books"]):
        src = os.path.join(books, s, "images", "cover.jpg")
        if s in published and (not os.path.exists(src) or sha(src) != d["books"][s].get("sha256")):
            out.append(f"the picture has changed since the thumbnail was made: books/{s}/images/cover.jpg (look at it; carousel.py add)")
    have = sorted(f for f in (os.listdir(thumbs) if os.path.isdir(thumbs) else []) if f.endswith(".jpg"))
    out += [f"thumbnail of no book in the record: site/carousel/{f}" for f in have if f[:-4] not in d["books"]]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    a = sub.add_parser("add")
    a.add_argument("slug")
    a.add_argument("--kind", required=True, choices=sorted(KINDS))
    a.add_argument("--note", default="")
    args = ap.parse_args()
    if args.cmd == "check":
        todo = check()
        print("\n".join(todo) if todo else f"carousel: {len(load()['books'])} books; nothing to do")
        sys.exit(1 if todo else 0)
    w, h = add(args.slug, args.kind, args.note)
    print(f"site/carousel/{args.slug}.jpg {w}x{h} ({KINDS[args.kind]})")


if __name__ == "__main__":
    main()
