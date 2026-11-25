#!/usr/bin/env python3
"""Work done by helper models (other companies' models; Tom, 2026-11-25): the kit they get, the check of what they
deliver, and taking a delivery into wip/. How the whole process runs: notes/helpers.md.

  helper.py kit OUT_DIR             writes OUT_DIR/kit.zip: the instructions (helper/*.md), the transcription rules
                                    (prompts/transcribe.md), notes/page-markup.md and book-json.md, the invented sample book (tests/sample) and the tools a
                                    helper runs itself (this file, compile_book.py, inline.py, normalize.py,
                                    crop_image.py). Upload it to "Helper model workspace/References".
  helper.py check DIR [--job JOB.json]
                                    checks a delivery directory (book.json, pages/, images/, NOTES.md): names, every
                                    leaf of the job has a page file, markup, that it compiles, pictures (one file per
                                    [[image:]], JPEG, longest side at most 1000 px, a cover). Ends "RESULT: PASS" or
                                    "RESULT: FAIL". The helper runs it before delivering; the session runs it again.
  helper.py intake ZIP DEST_DIR     unpacks a delivered zip as untrusted data: only the expected names and kinds of
                                    file, size limits, text must be UTF-8, every picture is decoded and written again
                                    by Pillow. DEST_DIR must not exist. Then run `check` on it.

A delivery is the first reading of a book, not a finished text: it then goes through the corrections pass, the
judge, the spot-read, preflight and the audit like a draft of our own (notes/workflow.md).
"""
import argparse, io, json, os, re, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compile_book  # noqa: E402

MAX_SIDE = 1000
PAGE_RE = re.compile(r"pages/p\d{4}[a-z]?\.txt")
IMAGE_RE = re.compile(r"images/(p\d{4}[a-z]?-\d+|cover)\.jpg")
OTHER = {"book.json", "NOTES.md"}
MARKERS = {"page", "blank", "cont", "subtitle", "right", "center", "break", "image:", "caption", "fnref", "fn",
           "corr", "supplied", "gap", "side:", "stream"}
TAGS = ("i", "b", "sc", "sup", "sub", "pref")
LIMITS = {"page": 200_000, "image": 3_000_000, "other": 2_000_000, "files": 6000, "total": 400_000_000}
KIT_TOOLS = ["helper.py", "compile_book.py", "inline.py", "normalize.py", "crop_image.py"]
BOOK_KEYS = ["id", "version", "date", "title", "short_title", "authors", "place", "publisher", "year",
             "edition_statement", "regions", "period", "summary", "source", "omitted_from_reading", "history",
             "divisions"]


def allowed(name, slug=None):
    return bool(PAGE_RE.fullmatch(name) or IMAGE_RE.fullmatch(name) or name in OTHER
                or (re.fullmatch(r"[a-z0-9-]+\.json", name) and "/" not in name))


def leaves_of(job):
    """The leaf names a job asks for: {"leaves": ["p0005", "p0141"]} = that range, inclusive; "skip": [...] left out."""
    if not job or "leaves" not in job:
        return None
    a, b = (int(x[1:]) for x in job["leaves"])
    return [f"p{i:04d}" for i in range(a, b + 1) if f"p{i:04d}" not in set(job.get("skip", []))]


def check_page(leaf, text):
    """Problems of one page file, as strings."""
    out = []
    lines = text.split("\n")
    if not re.fullmatch(r"\[\[page [^\]]+\]\]", lines[0].strip()):
        out.append(f"{leaf}: line 1 is not [[page N]] (or [[page ?]])")
    if "```" in text:
        out.append(f"{leaf}: a code fence (```) in the page file")
    for m in re.finditer(r"\[\[([a-z]+:?)", text):
        if m.group(1) not in MARKERS:
            out.append(f"{leaf}: unknown marker [[{m.group(1)}")
    if text.count("[[") != text.count("]]"):
        out.append(f"{leaf}: [[ and ]] do not pair up")
    for n, ln in enumerate(lines, 1):
        for t in TAGS:
            if len(re.findall(rf"<{t}\b[^>]*>", ln)) != len(re.findall(rf"</{t}>", ln)):
                out.append(f"{leaf} line {n}: <{t}> not closed within the paragraph")
    body = [ln for ln in lines[1:] if ln.strip()]
    if "[[blank]]" in text and len(body) > 1:
        out.append(f"{leaf}: [[blank]] on a page that has text")
    return out


def check(d, job=None):
    """Returns (fails, warns) for delivery directory d."""
    from PIL import Image
    fails, warns = [], []
    names = sorted(os.path.relpath(os.path.join(r, f), d).replace(os.sep, "/")
                   for r, _, fs in os.walk(d) for f in fs)
    for n in names:
        if not allowed(n):
            fails.append(f"unexpected file: {n}")
    for need in ("book.json", "NOTES.md"):
        if need not in names:
            fails.append(f"missing {need}")
    pages = {n[6:-4]: open(os.path.join(d, n), encoding="utf-8").read() for n in names if PAGE_RE.fullmatch(n)}
    if not pages:
        fails.append("no page files (pages/pNNNN.txt)")
    want = leaves_of(job)
    if want:
        fails += [f"no page file for leaf {x}" for x in want if x not in pages]
        warns += [f"page file for a leaf outside the job: {x}" for x in pages if x not in want and not x[-1].isalpha()]
    for leaf, text in sorted(pages.items()):
        fails += check_page(leaf, text)
    # pictures
    imgs = {n[7:-4] for n in names if IMAGE_RE.fullmatch(n)}
    marks = set()
    for leaf, text in pages.items():
        for k in range(1, len(re.findall(r"\[\[image:", text)) + 1):
            marks.add(f"{leaf}-{k}")
    fails += [f"[[image:]] without a file: images/{x}.jpg" for x in sorted(marks - imgs)]
    fails += [f"picture without an [[image:]] line: images/{x}.jpg" for x in sorted(imgs - marks - {"cover"})]
    if "cover" not in imgs:
        fails.append("missing images/cover.jpg")
    for x in sorted(imgs):
        p = os.path.join(d, "images", x + ".jpg")
        try:
            with Image.open(p) as im:
                if im.format != "JPEG":
                    fails.append(f"images/{x}.jpg is not a JPEG")
                if max(im.size) > MAX_SIDE:
                    fails.append(f"images/{x}.jpg is {im.size[0]}×{im.size[1]}: longest side over {MAX_SIDE} px")
                if min(im.size) < 60:
                    warns.append(f"images/{x}.jpg is only {im.size[0]}×{im.size[1]} px")
                if im.mode not in ("RGB", "L"):
                    fails.append(f"images/{x}.jpg has mode {im.mode} (RGB or L wanted)")
        except Exception as e:  # noqa: BLE001
            fails.append(f"images/{x}.jpg cannot be opened: {e!r}"[:160])
    # book.json and compiling
    cfg = None
    if "book.json" in names:
        try:
            cfg = json.load(open(os.path.join(d, "book.json"), encoding="utf-8"))
        except ValueError as e:
            fails.append(f"book.json is not valid JSON: {e}")
    if isinstance(cfg, dict):
        fails += [f"book.json lacks “{k}”" for k in BOOK_KEYS if k not in cfg]
        if job and job.get("slug") and cfg.get("id") != job["slug"]:
            fails.append(f"book.json id is {cfg.get('id')!r}, the job's is {job['slug']!r}")
        if not any(x.get("kind") == "titlepage" for x in cfg.get("divisions", []) if isinstance(x, dict)):
            fails.append("book.json divisions has no entry of kind “titlepage”")
        s = cfg.get("summary", "")
        n = len((" ".join(s) if isinstance(s, list) else str(s)).split())
        if not 60 <= n <= 150:
            warns.append(f"summary has {n} words (60–150 wanted)")
        if pages and all(k in cfg for k in ("id", "version", "date", "title", "authors")):
            try:
                book, cw = compile_book.compile_book(d)
                warns += [f"compiler: {w}" for w in cw if w.startswith("hyphen join")]
                fails += [f"compiler: {w}" for w in cw if not w.startswith("hyphen join")]
                kinds = [x["kind"] for x in book["divisions"]]
                if "chapter" not in kinds:
                    warns.append("no division of kind “chapter”")
            except Exception as e:  # noqa: BLE001
                fails.append(f"the book does not compile: {e!r}"[:300])
    if "NOTES.md" in names and len(open(os.path.join(d, "NOTES.md"), encoding="utf-8").read().split()) < 30:
        fails.append("NOTES.md says almost nothing: see the instructions for what it must contain")
    return fails, warns


def intake(zpath, dest):
    """Unpack a delivered zip into dest (which must not exist). Returns the list of names written.
    Raises ValueError on anything unexpected: the zip is untrusted data."""
    from PIL import Image
    if os.path.exists(dest):
        raise ValueError(f"{dest} exists")
    with zipfile.ZipFile(zpath) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        if len(infos) > LIMITS["files"] or sum(i.file_size for i in infos) > LIMITS["total"]:
            raise ValueError("too many files or too large")
        names = [i.filename for i in infos]
        tops = {n.split("/")[0] for n in names}
        strip = len(tops) == 1 and all("/" in n for n in names) and not ({"pages", "images"} & tops)
        out = []
        for i in infos:
            n = i.filename.split("/", 1)[1] if strip else i.filename
            if n.startswith("__MACOSX/") or os.path.basename(n) in (".DS_Store", "Thumbs.db"):
                continue
            if (i.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"symbolic link in the archive: {i.filename}")
            if not allowed(n) or ".." in n or n.startswith("/") or "\\" in n:
                raise ValueError(f"unexpected name in the archive: {i.filename}")
            kind = "page" if n.startswith("pages/") else "image" if n.startswith("images/") else "other"
            if i.file_size > LIMITS[kind]:
                raise ValueError(f"{i.filename} is {i.file_size} bytes: too large for a {kind} file")
            data = z.read(i)
            if kind == "image":
                try:
                    im = Image.open(io.BytesIO(data))
                    im.load()
                except Exception as e:  # noqa: BLE001
                    raise ValueError(f"{i.filename} is not a picture Pillow can read: {e!r}"[:200])
                if im.format != "JPEG":
                    raise ValueError(f"{i.filename} is {im.format}, not JPEG")
                buf = io.BytesIO()
                (im if im.mode in ("RGB", "L") else im.convert("RGB")).save(buf, "JPEG", quality=90)
                # written again from the decoded pixels, so nothing but the picture comes in; kept as delivered
                # when that would make it larger for no gain in safety is not attempted: quality 90 loses little
                data = buf.getvalue()
            else:
                try:
                    t = data.decode("utf-8")
                except UnicodeDecodeError:
                    raise ValueError(f"{i.filename} is not UTF-8 text")
                if "\x00" in t:
                    raise ValueError(f"{i.filename} has NUL characters")
                data = t.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
            out.append((n, data))
    for n, data in out:
        p = os.path.join(dest, n)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    return [n for n, _ in out]


def kit(out_dir, repo=None):
    """Write OUT_DIR/kit.zip (deterministic: fixed dates, sorted names). Returns its path."""
    repo = repo or os.path.dirname(HERE)
    files = []
    hdir = os.path.join(repo, "helper")
    for f in sorted(os.listdir(hdir)):
        if f.endswith(".md"):
            files.append((f"kit/{f}", os.path.join(hdir, f)))
    files.append(("kit/transcription-rules.md", os.path.join(repo, "prompts", "transcribe.md")))
    for f in ("page-markup.md", "book-json.md"):
        files.append((f"kit/{f}", os.path.join(repo, "notes", f)))
    for f in KIT_TOOLS:
        files.append((f"kit/tools/{f}", os.path.join(HERE, f)))
    sdir = os.path.join(repo, "tests", "sample")
    for r, _, fs in sorted(os.walk(sdir)):
        for f in sorted(fs):
            p = os.path.join(r, f)
            rel = os.path.relpath(p, sdir).replace(os.sep, "/")
            if rel == "source.json":
                continue
            files.append((f"kit/sample-book/{rel}", p))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "kit.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, p in files:
            zi = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(p, "rb").read())
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("kit"); k.add_argument("out_dir")
    c = sub.add_parser("check"); c.add_argument("dir"); c.add_argument("--job")
    i = sub.add_parser("intake"); i.add_argument("zip"); i.add_argument("dest")
    a = ap.parse_args()
    if a.cmd == "kit":
        print("wrote", kit(a.out_dir))
    elif a.cmd == "intake":
        try:
            names = intake(a.zip, a.dest)
        except ValueError as e:
            sys.exit(f"REFUSED: {e}")
        print(f"unpacked {len(names)} files into {a.dest}: "
              f"{sum(n.startswith('pages/') for n in names)} pages, {sum(n.startswith('images/') for n in names)} pictures")
    else:
        job = json.load(open(a.job, encoding="utf-8")) if a.job else None
        fails, warns = check(a.dir, job)
        for w in warns:
            print("WARN", w)
        for f in fails:
            print("FAIL", f)
        print(f"RESULT: {'FAIL' if fails else 'PASS'} ({len(fails)} to fix, {len(warns)} to look at)")
        sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
