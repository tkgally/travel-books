#!/usr/bin/env python3
"""Page images for the pipeline from an Internet Archive page-image archive.

  prep_pages.py SRC_DIR OUT_DIR [--height 1800] [--quality 72] [--color] [--workers 4]

SRC_DIR is what `ia.py fetch` wrote (…_jp2.zip or .tar, …_scandata.xml). Writes OUT_DIR/pNNNN.jpg, where NNNN is
the leaf number in the archive's file names (…_0012.jp2 -> p0012.jpg), scaled to --height pixels, greyscale
unless --color; and OUT_DIR/leaves.json: for each leaf the Archive's page type and asserted page number, and
"hidden_leaves" (leaves the Archive's viewer does not show, e.g. colour cards) for book.json `source`.
These are the working set that is cached in Drive. Illustrations are cropped from full-size leaves:
  prep_pages.py SRC_DIR OUT_DIR --full p0012,p0045      -> OUT_DIR/full/p0012.jpg at full size, colour, quality 90
"""
import argparse, concurrent.futures as cf, io, json, os, re, sys, tarfile, zipfile
import xml.etree.ElementTree as ET


def archive(src):
    for f in sorted(os.listdir(src)):
        if re.search(r"_(jp2|tif|jpg|images)\.(zip|tar)$", f):
            return os.path.join(src, f)
    sys.exit("no page-image archive in " + src)


def members(path):
    if path.endswith(".zip"):
        names = zipfile.ZipFile(path).namelist()
    else:
        names = [m.name for m in tarfile.open(path).getmembers()]
    return [(n, path) for n in sorted(names) if re.search(r"_\d{4}\.(jp2|tif|jpg)$", n)]


def read_member(path, name):
    if path.endswith(".zip"):
        return zipfile.ZipFile(path).read(name)
    return tarfile.open(path).extractfile(name).read()


def scandata(src):
    out, hidden = {}, []
    for f in os.listdir(src):
        if f.endswith("scandata.xml"):
            root = ET.parse(os.path.join(src, f)).getroot()
            for p in root.iter("page"):
                n = int(p.get("leafNum"))
                acc = (p.findtext("addToAccessFormats") or "true").strip().lower()
                out[n] = {"type": p.findtext("pageType") or "", "number": p.findtext("pageNumber") or ""}
                if acc == "false":
                    hidden.append(n)
                    out[n]["hidden"] = True
    return out, hidden


def convert(job):
    name, read, out, height, quality, color = job
    from PIL import Image
    if os.path.exists(out):
        return
    im = Image.open(io.BytesIO(read_member(read, name)))
    im = im.convert("RGB" if color else "L")
    if height and im.height > height:
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    im.save(out + ".tmp", "JPEG", quality=quality, optimize=True)
    os.replace(out + ".tmp", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--height", type=int, default=1800)
    ap.add_argument("--quality", type=int, default=72)
    ap.add_argument("--color", action="store_true")
    ap.add_argument("--full", help="comma-separated leaves to write at full size into OUT/full/")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    arc = archive(a.src)
    ms = members(arc)
    os.makedirs(a.out, exist_ok=True)
    jobs = []
    if a.full:
        want = set(a.full.split(","))
        os.makedirs(os.path.join(a.out, "full"), exist_ok=True)
        for n, read in ms:
            leaf = "p" + re.search(r"_(\d{4})\.\w+$", n).group(1)
            if leaf in want:
                jobs.append((n, read, os.path.join(a.out, "full", leaf + ".jpg"), 0, 90, True))
    else:
        for n, read in ms:
            leaf = "p" + re.search(r"_(\d{4})\.\w+$", n).group(1)
            jobs.append((n, read, os.path.join(a.out, leaf + ".jpg"), a.height, a.quality, a.color))
        info, hidden = scandata(a.src)
        json.dump({"archive": os.path.basename(arc), "leaf_count": len(ms), "height": a.height, "quality": a.quality,
                   "color": a.color, "hidden_leaves": hidden, "leaves": {f"p{k:04d}": v for k, v in sorted(info.items())}},
                  open(os.path.join(a.out, "leaves.json"), "w", encoding="utf-8"), indent=1)
    with cf.ProcessPoolExecutor(a.workers) as ex:
        list(ex.map(convert, jobs))
    files = [f for f in os.listdir(os.path.join(a.out, "full") if a.full else a.out) if f.endswith(".jpg")]
    total = sum(os.path.getsize(os.path.join(os.path.join(a.out, "full") if a.full else a.out, f)) for f in files)
    print(f"{len(files)} images, {total / 1e6:.1f} MB in {a.out}{'/full' if a.full else ''}")


if __name__ == "__main__":
    main()
