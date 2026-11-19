#!/usr/bin/env python3
"""The Google Drive cache of a book's working files (page images, IA metadata, IA OCR text).

Why: so that the Internet Archive is asked for a book's files once, and the repository holds no scans.
Drive folder "Travel Books" (id in CLAUDE.md) / one subfolder per book id.

  drive_cache.py pack PAGES_DIR OUT_DIR --source SOURCE.json [--extra FILE ...]
        Zips the page images (and extra small files) into independent parts of at most 3 MB each
        (OUT_DIR/pages-001.zip …; the Drive connector refuses larger uploads from a session) and writes
        their names, contents and sha256 into SOURCE.json under "parts". Then, for each part, the SESSION
        uploads it with the Drive connector (create_file, parentId = the book's folder,
        contentMimeType application/zip, disableConversionToGoogleType true, base64Content =
        "sha256:<hex>:<absolute path>" as printed) and records the returned id:
  drive_cache.py setid SOURCE.json PART_NAME DRIVE_ID
  drive_cache.py todo SOURCE.json OUT_DIR         the parts still without a drive_id, as upload lines
  drive_cache.py fetch SOURCE.json DEST_DIR [--pages p0010-p0040]
        Downloads the parts (all, or those holding the pages asked for) with curl, checks sha256 and
        unzips into DEST_DIR. Files already there are kept.

SOURCE.json lives in the book's directory in the repo (wip/<slug>/source.json, later books/<slug>/).
"""
import argparse, hashlib, json, os, re, subprocess, sys, time, zipfile

LIMIT = 3_000_000


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save(p, d):
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(p, "a").write("\n")


def pack(pages_dir, out_dir, source, extra=(), limit=LIMIT):
    os.makedirs(out_dir, exist_ok=True)
    files = [os.path.join(pages_dir, f) for f in sorted(os.listdir(pages_dir))
             if re.fullmatch(r"p\d+[a-z]?\.(jpg|png)", f) or f == "leaves.json"] + list(extra)
    groups, cur, size = [], [], 0
    for f in files:
        s = os.path.getsize(f) + 300
        if s > limit:
            sys.exit(f"{f} is {s} bytes: larger than one part. Lower --height/--quality in prep_pages.py.")
        if cur and size + s > limit:
            groups.append(cur); cur, size = [], 0
        cur.append(f); size += s
    if cur:
        groups.append(cur)
    src = load(source)
    old = {p["sha256"]: p for p in src.get("parts", [])}
    parts = []
    for i, g in enumerate(groups, 1):
        name = f"pages-{i:03d}.zip"
        path = os.path.join(out_dir, name)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
            for f in g:
                zi = zipfile.ZipInfo(os.path.basename(f), (1980, 1, 1, 0, 0, 0))
                z.writestr(zi, open(f, "rb").read())
        h = sha(path)
        part = {"name": name, "sha256": h, "bytes": os.path.getsize(path), "files": [os.path.basename(f) for f in g]}
        if h in old and old[h].get("drive_id"):
            part["drive_id"] = old[h]["drive_id"]
        parts.append(part)
    src["parts"] = parts
    save(source, src)
    print(f"{len(parts)} parts, {sum(p['bytes'] for p in parts) / 1e6:.1f} MB, in {out_dir}")
    todo(source, out_dir)


def todo(source, out_dir):
    src = load(source)
    left = [p for p in src.get("parts", []) if not p.get("drive_id")]
    print(f"{len(left)} of {len(src.get('parts', []))} parts to upload (Drive folder id: {src.get('drive_folder_id', 'NOT SET — create the book folder first')})")
    for p in left:
        print(f"{p['name']}\tsha256:{p['sha256']}:{os.path.abspath(os.path.join(out_dir, p['name']))}")


def setid(source, name, drive_id):
    src = load(source)
    for p in src.get("parts", []):
        if p["name"] == name:
            p["drive_id"] = drive_id
            save(source, src)
            return
    sys.exit("no such part: " + name)


def page_filter(pages):
    """--pages: 'p0036', 'p0030-p0040' or a comma list of either. Returns a test on file names (None = all).
    Before 2026-11-19 a comma list was taken as one name and fetched the wrong parts without a word."""
    if not pages:
        return None
    spans = []
    for item in pages.split(","):
        item = item.strip()
        m = re.fullmatch(r"(p\d{4})(?:-(p\d{4}))?", item)
        if not m:
            sys.exit(f"--pages: '{item}' is not pNNNN or pNNNN-pNNNN")
        spans.append((m.group(1), m.group(2) or m.group(1)))
    return lambda f: not f.startswith("p") or any(lo <= f.split(".")[0] <= hi for lo, hi in spans)


def fetch(source, dest, pages=None):
    src = load(source)
    os.makedirs(dest, exist_ok=True)
    keep = page_filter(pages)
    for p in src.get("parts", []):
        want = [f for f in p["files"] if keep is None or keep(f)]
        if not want or all(os.path.exists(os.path.join(dest, f)) for f in want):
            continue
        if not p.get("drive_id"):
            sys.exit(f"{p['name']} has no drive_id: the cache is incomplete (fetch the book from the Internet Archive again)")
        tmp = os.path.join(dest, "_" + p["name"])
        for attempt in range(4):
            subprocess.run(["curl", "-sSL", "-o", tmp, f"https://drive.usercontent.google.com/download?id={p['drive_id']}&export=download&confirm=t"])
            if os.path.exists(tmp) and sha(tmp) == p["sha256"]:
                break
            time.sleep(5 * (attempt + 1))
        else:
            sys.exit(f"could not fetch {p['name']} from Drive (sha256 mismatch or download failed)")
        with zipfile.ZipFile(tmp) as z:
            for n in z.namelist():
                if os.path.basename(n) != n or n.startswith("."):
                    sys.exit("unexpected name in archive: " + n)
                open(os.path.join(dest, n), "wb").write(z.read(n))
        os.remove(tmp)
    n = len([f for f in os.listdir(dest) if re.fullmatch(r"p\d+[a-z]?\.(jpg|png)", f)])
    print(f"{n} page images in {dest}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("pack"); s.add_argument("pages_dir"); s.add_argument("out_dir"); s.add_argument("--source", required=True); s.add_argument("--extra", nargs="*", default=[])
    s = sub.add_parser("setid"); s.add_argument("source"); s.add_argument("name"); s.add_argument("drive_id")
    s = sub.add_parser("todo"); s.add_argument("source"); s.add_argument("out_dir")
    s = sub.add_parser("fetch"); s.add_argument("source"); s.add_argument("dest"); s.add_argument("--pages")
    a = ap.parse_args()
    if a.cmd == "pack":
        pack(a.pages_dir, a.out_dir, a.source, a.extra)
    elif a.cmd == "setid":
        setid(a.source, a.name, a.drive_id)
    elif a.cmd == "todo":
        todo(a.source, a.out_dir)
    else:
        fetch(a.source, a.dest, a.pages)


if __name__ == "__main__":
    main()
