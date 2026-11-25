#!/usr/bin/env python3
"""Fetch a job's scans: the page images and the full-size leaves a helper model works from (notes/helpers.md).

  python3 fetch_scans.py [--list scans.json] [--out scans] [--base URL_WITH_{id}]

A job zip is small (a session cannot upload more than about 3 MB to Drive in one file), so the scans are not in
it: scans.json lists the parts, each a zip of at most 3 MB kept in the project's Google Drive and readable by
anyone who has its link. This script downloads every part, checks its sha256 and unpacks it:
  scans/pages/pNNNN.jpg   one grey image per leaf, 1800 pixels high   (parts of kind "pages")
  scans/full/pNNNN.jpg    full-size colour leaves for the pictures    (parts of kind "full")
Parts already unpacked are skipped, so it can be run again after a failure. Python 3 standard library only.
"""
import argparse, hashlib, io, json, os, re, sys, time, urllib.request, zipfile

BASE = "https://drive.usercontent.google.com/download?id={id}&export=download&confirm=t"
NAME = re.compile(r"p\d{4}[a-z]?\.(jpg|png)|leaves\.json|[A-Za-z0-9_.-]+_djvu\.txt")


def fetch(parts, out, base=BASE, tries=4, log=print):
    """Download and unpack the parts. Returns the number of files written. Raises RuntimeError on failure."""
    n = 0
    for p in parts:
        dest = os.path.join(out, p["kind"])
        os.makedirs(dest, exist_ok=True)
        want = [f for f in p["files"] if not f.endswith("_djvu.txt")]
        if all(os.path.exists(os.path.join(dest, f)) for f in want):
            continue
        data = None
        for attempt in range(tries):
            try:
                with urllib.request.urlopen(base.format(id=p["drive_id"]), timeout=120) as r:
                    data = r.read()
            except Exception as e:  # noqa: BLE001
                data, err = None, repr(e)[:200]
            if data is not None and hashlib.sha256(data).hexdigest() == p["sha256"]:
                break
            data = None
            time.sleep(3 * attempt)
        if data is None:
            raise RuntimeError(f"could not fetch {p['kind']}/{p['name']} (download failed or sha256 mismatch)")
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for name in z.namelist():
                if not NAME.fullmatch(name):
                    raise RuntimeError(f"unexpected name in {p['name']}: {name}")
                if name.endswith("_djvu.txt"):
                    continue  # the Archive's OCR text is not for the helper
                with open(os.path.join(dest, name), "wb") as f:
                    f.write(z.read(name))
                n += 1
        log(f"{p['kind']}/{p['name']}: ok")
    return n


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", default=os.path.join(here, "scans.json"))
    ap.add_argument("--out", default=os.path.join(here, "scans"))
    ap.add_argument("--base", default=BASE)
    a = ap.parse_args()
    parts = json.load(open(a.list, encoding="utf-8"))["parts"]
    try:
        n = fetch(parts, a.out, a.base)
    except RuntimeError as e:
        sys.exit(f"FAILED: {e}\nRun the script again. If it keeps failing, stop and tell Tom: do not get the scans "
                 f"from anywhere else.")
    for kind in sorted({p["kind"] for p in parts}):
        d = os.path.join(a.out, kind)
        print(f"{kind}: {len([f for f in os.listdir(d) if f.endswith('.jpg')])} images in {d}")
    print(f"done ({n} files written this run)")


if __name__ == "__main__":
    main()
