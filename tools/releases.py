#!/usr/bin/env python3
"""The EPUB and ODT downloads as GitHub Release files of this repository (Tom, 2026-11-23: the site must stay
under GitHub Pages' 1 GB limit; download links to github.com are allowed; one release per book).

  releases.py SITE_DIR [--upload] [--remove] [--tag-prefix book-] [--only SLUG]
  releases.py --delete-prefix PREFIX         delete every release (and its tag) whose tag starts with PREFIX

Run by the Pages workflow after build_site.py: for each book built in SITE_DIR/books/<slug>/, the release with tag
`book-<slug>` holds `<slug>-v<N>.epub` and `<slug>-v<N>.odt` (N = the book's version, from its JSON), which is where
the book's page links (build_site.download_url). A file is uploaded only when it is missing or its bytes changed (the
sha256 of each file is kept in a comment in the release text), so a deploy uploads only what changed; files of
earlier versions are kept. --remove then deletes the EPUB and ODT from SITE_DIR, so that Pages does not publish
them. Without --upload: lists what would be uploaded. Needs GITHUB_TOKEN and GITHUB_REPOSITORY (set in Actions).
Standard library only.
"""
import argparse, glob, hashlib, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

TAG_PREFIX = "book-"
TYPES = {".epub": "application/epub+zip", ".odt": "application/vnd.oasis.opendocument.text"}
SITE_URL = "https://tkgally.github.io/travel-books"
MARK = re.compile(r"<!-- files: (\{.*?\}) -->", re.S)
PAUSE = 1.0          # seconds between requests that create content (GitHub: at most 80 a minute)


def tag_for(slug, prefix=TAG_PREFIX):
    return prefix + slug


def asset_name(slug, version, ext):
    return f"{slug}-v{version}{ext}"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def recorded(body):
    """The sha256 of each file, as kept in the release text."""
    m = MARK.search(body or "")
    try:
        return json.loads(m.group(1)) if m else {}
    except ValueError:
        return {}


def release_body(book, shas):
    title = book.get("short_title") or book.get("title") or book["id"]
    return (f"The EPUB and ODT files of *{title}* for the Travel Books site: {SITE_URL}/books/{book['id']}/\n\n"
            f"Each file is named with the version of the book; earlier versions are kept.\n\n"
            f"<!-- files: {json.dumps(shas, sort_keys=True)} -->")


def local_books(site, only=None):
    """[(book JSON, {asset name: path})] for the books built in SITE_DIR."""
    out = []
    for jf in sorted(glob.glob(os.path.join(site, "books", "*", "*.json"))):
        slug = os.path.basename(os.path.dirname(jf))
        if os.path.basename(jf) != slug + ".json" or (only and slug != only):
            continue
        book = json.load(open(jf, encoding="utf-8"))
        files = {}
        for ext in TYPES:
            p = os.path.join(os.path.dirname(jf), slug + ext)
            if os.path.exists(p):
                files[asset_name(slug, book["version"], ext)] = p
        if files:
            out.append((book, files))
    return out


def sync(site, api, upload=True, prefix=TAG_PREFIX, only=None, log=print):
    """Bring the releases up to date with SITE_DIR. Returns the number of files uploaded (or to upload)."""
    releases = {r["tag_name"]: r for r in api.list_releases()}
    n = 0
    for book, files in local_books(site, only):
        tag = tag_for(book["id"], prefix)
        rel = releases.get(tag)
        shas = recorded(rel["body"]) if rel else {}
        assets = {a["name"]: a for a in rel.get("assets", [])} if rel else {}
        todo = []
        for name, path in sorted(files.items()):
            h = sha(path)
            a = assets.get(name)
            if not (a and a.get("state") == "uploaded" and shas.get(name) == h):
                todo.append((name, path, h))
        if not todo:
            continue
        n += len(todo)
        log(f"{tag}: {', '.join(t[0] for t in todo)}")
        if not upload:
            continue
        if rel is None:
            rel = api.create_release(tag, book.get("short_title") or book.get("title") or book["id"], release_body(book, {}))
            assets = {}
        for name, path, h in todo:
            if name in assets:
                api.delete_asset(assets[name]["id"])
            api.upload_asset(rel, name, path, TYPES[os.path.splitext(name)[1]])
            shas[name] = h
        api.update_release(rel["id"], release_body(book, shas))
    return n


def remove(site):
    """Delete the EPUB and ODT files from SITE_DIR (they are served from the releases)."""
    k = 0
    for ext in TYPES:
        for p in glob.glob(os.path.join(site, "books", "*", "*" + ext)):
            os.remove(p)
            k += 1
    return k


class GitHub:
    """The few calls of the GitHub REST API that sync needs, with retries and pauses."""
    def __init__(self, repo, token):
        self.repo, self.token = repo, token

    def call(self, method, url, data=None, ctype="application/json", tries=5):
        if not url.startswith("https://"):
            url = f"https://api.github.com/repos/{self.repo}{url}"
        body = json.dumps(data).encode() if isinstance(data, dict) else data
        for i in range(tries):
            req = urllib.request.Request(url, data=body, method=method, headers={
                "Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28", "Content-Type": ctype, "User-Agent": "travel-books-releases"})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    raw = r.read()
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                if e.code in (403, 429, 500, 502, 503, 504) and i < tries - 1:
                    wait = int(e.headers.get("Retry-After") or 0) or 10 * (i + 1)
                    print(f"  {method} {url}: HTTP {e.code}, again in {wait} s", file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise SystemExit(f"{method} {url}: HTTP {e.code} {e.read()[:300]!r}")
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if i < tries - 1:
                    time.sleep(10 * (i + 1))
                    continue
                raise SystemExit(f"{method} {url}: {e}")

    def list_releases(self):
        out, page = [], 1
        while True:
            got = self.call("GET", f"/releases?per_page=100&page={page}")
            out += got
            if len(got) < 100:
                return out
            page += 1

    def create_release(self, tag, name, body):
        time.sleep(PAUSE)
        return self.call("POST", "/releases", {"tag_name": tag, "name": name, "body": body,
                                               "target_commitish": os.environ.get("GITHUB_SHA", "main"),
                                               "make_latest": "false"})

    def update_release(self, rid, body):
        time.sleep(PAUSE)
        return self.call("PATCH", f"/releases/{rid}", {"body": body})

    def delete_asset(self, aid):
        time.sleep(PAUSE)
        return self.call("DELETE", f"/releases/assets/{aid}")

    def upload_asset(self, rel, name, path, ctype):
        time.sleep(PAUSE)
        base = rel["upload_url"].split("{")[0]
        return self.call("POST", f"{base}?name={urllib.parse.quote(name)}", open(path, "rb").read(), ctype)

    def delete_prefix(self, prefix):
        k = 0
        for r in self.list_releases():
            if r["tag_name"].startswith(prefix):
                time.sleep(PAUSE)
                self.call("DELETE", f"/releases/{r['id']}")
                self.call("DELETE", f"/git/refs/tags/{urllib.parse.quote(r['tag_name'])}")
                k += 1
        return k


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("site", nargs="?")
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--remove", action="store_true", help="then delete the EPUB and ODT files from SITE_DIR")
    ap.add_argument("--tag-prefix", default=TAG_PREFIX)
    ap.add_argument("--only")
    ap.add_argument("--delete-prefix")
    a = ap.parse_args()
    token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not (token and repo):
        raise SystemExit("GITHUB_TOKEN and GITHUB_REPOSITORY are needed (they are set in GitHub Actions)")
    api = GitHub(repo, token)
    if a.delete_prefix:
        if a.delete_prefix == TAG_PREFIX:
            raise SystemExit(f"refusing to delete the real releases ({TAG_PREFIX}…)")
        print(f"deleted {api.delete_prefix(a.delete_prefix)} releases")
        return
    if not a.site:
        ap.error("SITE_DIR is needed")
    n = sync(a.site, api, upload=a.upload, prefix=a.tag_prefix, only=a.only)
    print(f"{n} files {'uploaded' if a.upload else 'to upload'}")
    if a.remove:
        print(f"removed {remove(a.site)} EPUB and ODT files from {a.site}")


if __name__ == "__main__":
    main()
