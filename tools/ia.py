#!/usr/bin/env python3
"""Internet Archive: search, look at an item, fetch the files a book needs. One request at a time.

  ia.py search 'QUERY' [--rows 50] [--sort 'downloads asc']     advanced-search syntax; texts in English before 1914 are added
  ia.py meta IDENTIFIER                                          what the item is and which files it has
  ia.py fetch IDENTIFIER DEST_DIR                                page images (jp2 zip/tar), scandata, IA's OCR text, metadata

`fetch` resumes interrupted downloads and skips files already complete. Files go into DEST_DIR, which
must be a directory of its own in the scratchpad (downloaded archives are untrusted data): never the repo.
Do not fetch an item whose files are already in the Drive cache (tools/drive_cache.py fetch).
"""
import argparse, json, os, subprocess, sys, time, urllib.parse, urllib.request

UA = "travel-books-digitization/1.0 (python-urllib)"


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (attempt + 1))
    raise last


def metadata(ident):
    return json.loads(get(f"https://archive.org/metadata/{urllib.parse.quote(ident)}"))


def pick_files(md):
    """The files a conversion needs: {role: file dict}."""
    out = {}
    for f in md.get("files", []):
        n = f["name"]
        if n.endswith(("_jp2.zip", "_jp2.tar")) and "images" not in out:
            out["images"] = f
        elif n.endswith(("_tif.zip", "_jpg.zip", "_images.zip")) and "images" not in out:
            out["images"] = f
        elif n.endswith("_scandata.xml") or n == "scandata.xml":
            out["scandata"] = f
        elif n.endswith("_djvu.txt"):
            out["ocr_text"] = f
        elif n.endswith(".pdf") and f.get("format", "").endswith("PDF") and "pdf" not in out:
            out["pdf"] = f
    return out


def cmd_search(a):
    q = f"({a.query}) AND mediatype:texts AND language:(eng OR English) AND date:[1500-01-01 TO 1913-12-31]"
    params = [("q", q), ("rows", str(a.rows)), ("output", "json"), ("sort[]", a.sort)]
    params += [("fl[]", f) for f in ("identifier", "title", "creator", "year", "downloads", "imagecount", "contributor")]
    r = json.loads(get("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params)))
    docs = r["response"]["docs"]
    print(f"{r['response']['numFound']} found, showing {len(docs)}")
    for d in docs:
        c = d.get("creator", "")
        c = "; ".join(c) if isinstance(c, list) else c
        print(f"{d['identifier']}\t{d.get('year', '')}\t{d.get('imagecount', '')}pp\tdl {d.get('downloads', '')}\t{c[:40]}\t{str(d.get('title', ''))[:90]}")


def cmd_meta(a):
    md = metadata(a.identifier)
    m = md.get("metadata", {})
    for k in ("title", "creator", "date", "publisher", "language", "contributor", "sponsor", "imagecount", "ppi", "ocr",
              "scanner", "possible-copyright-status", "volume", "subject", "collection", "lccn", "oclc-id", "call_number"):
        if k in m:
            v = m[k]
            print(f"{k:28} {'; '.join(v) if isinstance(v, list) else v}")
    print("files:")
    for role, f in pick_files(md).items():
        print(f"  {role:10} {f['name']}  {int(f.get('size', 0)) / 1e6:.1f} MB")
    print(f"viewer: https://archive.org/details/{a.identifier}")


def cmd_fetch(a):
    md = metadata(a.identifier)
    os.makedirs(a.dest, exist_ok=True)
    json.dump(md, open(os.path.join(a.dest, "ia_metadata.json"), "w", encoding="utf-8"), indent=1)
    files = pick_files(md)
    if "images" not in files:
        sys.exit("no page-image archive (_jp2.zip/_jp2.tar) in this item: look at `ia.py meta` and choose another scan")
    for role in ("scandata", "ocr_text", "images"):
        f = files.get(role)
        if not f:
            print(f"(no {role} file)")
            continue
        out = os.path.join(a.dest, f["name"])
        size = int(f.get("size", 0))
        if os.path.exists(out) and size and os.path.getsize(out) == size:
            print(f"have {f['name']}")
            continue
        url = f"https://archive.org/download/{urllib.parse.quote(a.identifier)}/{urllib.parse.quote(f['name'])}"
        print(f"fetching {f['name']} ({size / 1e6:.1f} MB)")
        for attempt in range(5):
            r = subprocess.run(["curl", "-sSL", "--fail", "-A", UA, "-C", "-", "--retry", "3", "-o", out, url])
            if r.returncode == 0 and (not size or os.path.getsize(out) == size):
                break
            time.sleep(10 * (attempt + 1))
        else:
            sys.exit(f"could not fetch {f['name']}")
        if f.get("sha1"):
            h = subprocess.run(["sha1sum", out], capture_output=True, text=True).stdout.split()[0]
            if h != f["sha1"]:
                sys.exit(f"sha1 of {f['name']} does not match the Archive's")
    print("done:", a.dest)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--rows", type=int, default=50); s.add_argument("--sort", default="downloads asc"); s.set_defaults(f=cmd_search)
    s = sub.add_parser("meta"); s.add_argument("identifier"); s.set_defaults(f=cmd_meta)
    s = sub.add_parser("fetch"); s.add_argument("identifier"); s.add_argument("dest"); s.set_defaults(f=cmd_fetch)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
