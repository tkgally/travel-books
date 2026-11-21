#!/usr/bin/env python3
"""The carousel of covers on the home page (Tom, 2026-11-21): which books are in it, and their thumbnails.

  carousel.py check                     published books that are neither in the carousel nor left out, thumbnails
                                        that are missing or belong to no book; exit 1 if there is anything to do
  carousel.py add SLUG --kind cover|title [--from IMAGE] [--note TEXT]
                                        make site/carousel/SLUG.jpg and record it. Without --from the picture is
                                        books/SLUG/images/cover.jpg (which is the cover or the title page: say
                                        which with --kind). --from: another picture, e.g. the leaf of the title
                                        page fetched from the Drive cache into the scratchpad (never into the repo)
  carousel.py omit SLUG --note TEXT     the book has neither a cover nor a title page with a readable title

The rule (notes/site.md §"The carousel"): the cover if the title is clearly readable on it, otherwise the title
page; a book with neither is left out. Someone has to look at the picture: this tool does not judge it.
The record is data/carousel.json; build_site.py puts into the home page the books that are published, are in the
record and have their thumbnail. Needs Pillow.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BOX = (300, 450)        # the thumbnail fits in this: shown about 7rem wide, so enough for a screen of double density
QUALITY = 80
KINDS = {"cover": "cover", "title": "title page"}


def paths(repo=REPO):
    return os.path.join(repo, "data", "carousel.json"), os.path.join(repo, "site", "carousel"), os.path.join(repo, "books")


def load(repo=REPO):
    f = paths(repo)[0]
    d = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    d.setdefault("books", {})
    d.setdefault("omitted", {})
    return d


def save(d, repo=REPO):
    d = {"books": dict(sorted(d["books"].items())), "omitted": dict(sorted(d["omitted"].items()))}
    os.makedirs(os.path.dirname(paths(repo)[0]), exist_ok=True)
    with open(paths(repo)[0], "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write("\n")


def thumbnail(src, dest):
    """Write the thumbnail (JPEG, no metadata, the same bytes for the same picture); return its (width, height)."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im.thumbnail(BOX, Image.LANCZOS)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, "JPEG", quality=QUALITY, optimize=True)
    return im.size


def add(slug, kind, source=None, note="", repo=REPO):
    _, thumbs, books = paths(repo)
    if not os.path.exists(os.path.join(books, slug, "book.json")):
        raise SystemExit(f"no published book {slug}")
    src = source or os.path.join(books, slug, "images", "cover.jpg")
    if not os.path.exists(src):
        raise SystemExit(f"no picture {src}")
    w, h = thumbnail(src, os.path.join(thumbs, slug + ".jpg"))
    d = load(repo)
    d["omitted"].pop(slug, None)
    d["books"][slug] = {"image": KINDS[kind], "from": "images/cover.jpg" if not source else "scan " + os.path.basename(source),
                        "width": w, "height": h}
    if note:
        d["books"][slug]["note"] = note
    save(d, repo)
    return w, h


def omit(slug, note, repo=REPO):
    _, thumbs, _ = paths(repo)
    d = load(repo)
    d["books"].pop(slug, None)
    d["omitted"][slug] = note
    save(d, repo)
    f = os.path.join(thumbs, slug + ".jpg")
    if os.path.exists(f):
        os.remove(f)


def check(repo=REPO):
    """What is to be done, as lines of text (none: the carousel is up to date)."""
    _, thumbs, books = paths(repo)
    d = load(repo)
    published = sorted(s for s in (os.listdir(books) if os.path.isdir(books) else [])
                       if os.path.exists(os.path.join(books, s, "book.json")))
    out = [f"not decided: {s} (look at its cover; carousel.py add or omit)" for s in published
           if s not in d["books"] and s not in d["omitted"]]
    out += [f"in the record but not a published book: {s}" for s in sorted(set(d["books"]) | set(d["omitted"])) if s not in published]
    out += [f"thumbnail missing: site/carousel/{s}.jpg" for s in sorted(d["books"]) if not os.path.exists(os.path.join(thumbs, s + ".jpg"))]
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
    a.add_argument("--from", dest="source")
    a.add_argument("--note", default="")
    o = sub.add_parser("omit")
    o.add_argument("slug")
    o.add_argument("--note", required=True)
    args = ap.parse_args()
    if args.cmd == "check":
        todo = check()
        d = load()
        print("\n".join(todo) if todo else f"carousel: {len(d['books'])} books, {len(d['omitted'])} left out; nothing to do")
        sys.exit(1 if todo else 0)
    if args.cmd == "add":
        w, h = add(args.slug, args.kind, args.source, args.note)
        print(f"site/carousel/{args.slug}.jpg {w}x{h} ({KINDS[args.kind]})")
    else:
        omit(args.slug, args.note)
        print(f"{args.slug} left out")


if __name__ == "__main__":
    main()
