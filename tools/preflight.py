#!/usr/bin/env python3
"""Preflight: every mechanical publication check in one command. Run it before publishing any book version.

  preflight.py BOOKDIR [--epubcheck JAR | --skip-epubcheck] [--report FILE] [-v]

BOOKDIR is wip/<slug> or books/<slug>. The book is built into a temporary directory (JSON, HTML, EPUB,
ODT) and the checks in CHECKS are run on the page files and on what was built. Exit status 0 = may be
published, 1 = not.

Two modes per check:
  enforce   every item must be fixed, or waived in book.json with a reason;
  observe   items are listed for a look and counted, but do not block. A new check starts here and is
            promoted once notes/metrics.md shows its alarms are mostly real.

Waivers (book.json):  "waivers": [{"check": "spacing", "match": "p0145", "why": "printed so: a spaced French quotation"}]
  `match` is a substring of the item line; `why` is required. Unused waivers are reported.

Rule (CLAUDE.md): this file is not edited, and no check is moved to observe, in a session that is
publishing a book the check is blocking. Waive with the reason, record the false alarm in
notes/metrics.md, fix the check (with a test) in a later session.

The last line printed is the stamp: copy it into the book's log.md.
"""
import argparse, collections, datetime, difflib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_site, compile_book, inline, render_html as rh  # noqa: E402

CHECKS = collections.OrderedDict([
    ("meta",            ("enforce", "book.json: required fields present and sane")),
    ("markup",          ("enforce", "page files: every [[…]] is a known form, inline tags balanced, no 〓")),
    ("compile",         ("enforce", "compile warnings other than page-break hyphen joins (notes, images, [[cont]], divisions)")),
    ("conservation",    ("enforce", "the words of the page files are in the JSON, and the reading parts in HTML, EPUB and ODT, in order, nothing else")),
    ("stray-markup",    ("enforce", "no markup ([[…]], escaped tags, 〓) shows in the reading editions")),
    ("straight-quotes", ("enforce", "no straight ' or \" in the text")),
    ("spacing",         ("enforce", "modern spacing: no space before ; : ! ? , . or inside quotation marks, no doubled spaces")),
    ("sc-caps",         ("enforce", "text inside <sc> is typed in lower case with real capitals, not in capitals")),
    ("heading-caps",    ("enforce", "headings, chapter titles and captions are in upper and lower case, not all capitals")),
    ("links",           ("enforce", "every link inside the book's web pages and EPUB has a target")),
    ("wellformed",      ("enforce", "HTML pages, EPUB documents and ODT XML parse")),
    ("nav",             ("enforce", "contents: at least one reading division; each has a title and text")),
    ("epubcheck",       ("enforce", "epubcheck: 0 fatals / 0 errors / 0 warnings")),
    ("odt",             ("enforce", "LibreOffice opens the ODT and converts it to PDF")),
    ("audit",           ("enforce", "book.json records the sampled audit of this version")),
    ("hyphen-joins",    ("observe", "page-break hyphen joins (hyphen removed): read the list once")),
    ("joins",           ("observe", "page joins: missing [[cont]], or [[cont]] after a closed sentence")),
    ("folios",          ("observe", "printed page numbers that break the sequence")),
    ("quote-balance",   ("observe", "paragraphs with a closing double quote and no opening one, or the reverse at the paragraph end")),
    ("contents",        ("observe", "entries of the printed contents with no matching heading")),
    ("images",          ("observe", "image files not used by any page")),
    ("source",          ("observe", "source.json: the Drive cache of the page images is recorded")),
])
INLINE_TAGS = inline.INLINE
PAGE_TAG = re.compile(r'</?(?:%s|blockquote|verse)>|<pref(?: to="\w+")?>|</pref>' % "|".join(INLINE_TAGS))


def squash(s):
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[\s\-­]+", "", s)


# ---------------------------------------------------------------- text streams

def page_streams(pages):
    """(main, notes) text of the page files, markup removed."""
    main, notes = [], []
    for leaf, text in pages:
        for ln in text.splitlines():
            s = ln.strip()
            if not s or re.fullmatch(r"\[\[(page [^\]]*|blank|break)\]\]", s) or re.match(r"\[\[image:", s):
                continue
            if re.fullmatch(r"</?(blockquote|verse)>", s):
                continue
            tgt = main
            m = re.match(r"\[\[fn ([^\]]+)\]\]\s*(.*)", s)
            if m:
                tgt, s = notes, m.group(2)
            s = re.sub(r"\[\[corr [^|\]]*\|([^\]]*)\]\]", r"\1", s)
            s = re.sub(r"\[\[fnref [^\]]+\]\]", "", s)
            s = re.sub(r"\[\[(cont|right|center|subtitle|caption)\]\]", "", s)
            s = PAGE_TAG.sub("", s)
            if s.startswith("|") and s.endswith("|"):
                if re.fullmatch(r"\|[-| :]+\|", s):
                    continue
                s = s.replace("|", " ")
            s = re.sub(r"^#{1,3} ", "", s)
            tgt.append(s)
    return " ".join(main), " ".join(notes)


def json_streams(book, reading_only=False):
    main, notes = [], []
    for d in book["divisions"]:
        if reading_only and not d.get("reading"):
            continue
        for b in d["blocks"]:
            main += [inline.plain(s) for s in rh.strings(b)]
        notes += [inline.plain(n["text"]) for n in d["notes"]]
    return " ".join(main), " ".join(notes)


def html_text(x):
    x = re.sub(r'<a class="pb"[^>]*>.*?</a>|<span class="pb"[^>]*>.*?</span>', "", x, flags=re.S)
    x = re.sub(r'<a class="note(?:ref|back)"[^>]*>.*?</a>|<span class="noteback">.*?</span>', "", x, flags=re.S)
    x = re.sub(r"</(p|h\d|td|figcaption|span)>|<br/>", " ", x)
    return inline.html.unescape(re.sub(r"<[^>]+>", "", x))


def html_streams(docs):
    """docs = list of body strings of the reading divisions (web article or EPUB section)."""
    main, notes = [], []
    for x in docs:
        a, sep, b = x.partition('<section class="notes"')
        main.append(html_text(a))
        if sep:
            notes.append(html_text("<" + b))
    return " ".join(main), " ".join(notes)


T = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"
SKIP_STYLES = {"Title", "Subtitle", "Author", "Imprint", "Edition_20_Note", "Section_20_Break", "VerseEnd"}


def odt_streams(data):
    z = zipfile.ZipFile(data)
    root = ET.fromstring(z.read("content.xml"))
    body = root.find(".//{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text")
    main, notes = [], []

    def text_of(el, with_notes=False):
        out = [el.text or ""]
        for c in el:
            if c.tag.endswith("}frame") or c.tag == T + "note-ref":
                pass                     # images; a second mark for a note (cross-reference)
            elif c.tag == T + "note":
                nb = c.find(T + "note-body")
                notes.append(" ".join(text_of(p) for p in nb))
            elif c.tag == T + "s":
                out.append(" " * int(c.get(T + "c", "1")))
            else:
                out.append(text_of(c))
            out.append(c.tail or "")
        return "".join(out)

    def walk(el):
        for c in el:
            if c.tag in (T + "p", T + "h"):
                if c.get(T + "style-name") in SKIP_STYLES:
                    continue
                main.append(text_of(c))
            else:
                walk(c)
    walk(body)
    return " ".join(main), " ".join(notes)


def compare(a, b, label, limit=12):
    a, b = squash(a), squash(b)
    if a == b:
        return []
    items = []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False) if len(a) + len(b) < 60000 else None
    if sm is None:
        # long texts: find the first difference only (cheap), show context
        i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
        return [f"{label}: texts differ from character {i}: …{a[max(0, i - 30):i + 30]}… / …{b[max(0, i - 30):i + 30]}…"]
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            items.append(f"{label}: {op} …{a[max(0, i1 - 20):i1]}[{a[i1:i2][:60]}]→[{b[j1:j2][:60]}]{a[i2:i2 + 20]}…")
            if len(items) >= limit:
                break
    return items


# ---------------------------------------------------------------- checks on the page files

def check_markup(pages):
    items = []
    for leaf, text in pages:
        lines = text.splitlines()
        if not lines or not re.fullmatch(r"\[\[page [^\]]*\]\]", lines[0].strip()):
            items.append(f"{leaf}: first line is not [[page N]]")
        for ln in lines:
            rest = compile_book.MARK.sub("", ln)
            if "[[" in rest or "]]" in rest:
                items.append(f"{leaf}: unknown or broken [[…]]: {ln.strip()[:70]!r}")
            if "〓" in ln:
                items.append(f"{leaf}: illegible mark 〓: {ln.strip()[:70]!r}")
            body = PAGE_TAG.sub("", re.sub(r"\[\[corr [^\]]*\]\]", "", ln))
            if re.search(r"</?[A-Za-z][^<>]{0,30}>", body):
                items.append(f"{leaf}: unknown tag: {ln.strip()[:70]!r}")
            for m in re.finditer(r"<sc>(.*?)</sc>", ln):
                pass
            if re.search(r"(?<!^)(?<!\|)\s#{1,3} \w", ln) and not ln.lstrip().startswith("#"):
                items.append(f"{leaf}: '#' inside a line (heading not on its own line?): {ln.strip()[:70]!r}")
        if re.search(r"\[\[(cont|right|center|subtitle|caption)\]\]\s*$", text, flags=re.M):
            items.append(f"{leaf}: a marker with no text after it")
    return items


def check_sc(pages):
    items = []
    for leaf, text in pages:
        for m in re.finditer(r"<sc>(.*?)</sc>", text):
            t = re.sub(r"<[^>]+>", "", m.group(1))
            letters = [c for c in t if c.isalpha()]
            if len(letters) > 1 and all(c.isupper() for c in letters):
                items.append(f"{leaf}: <sc>{t[:40]}</sc>")
    return items


def check_heading_caps(pages):
    items = []
    for leaf, text in pages:
        for ln in text.splitlines():
            m = re.match(r"\s*(?:#{1,3} |\[\[(?:subtitle|caption)\]\])(.*)", ln)
            if not m:
                continue
            t = re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", "", m.group(1))
            words = [w for w in re.findall(r"[A-Za-z]{2,}", t) if not re.fullmatch(r"[IVXLCDM]+", w)]
            if words and all(w.isupper() for w in words) and sum(len(w) for w in words) > 3:
                items.append(f"{leaf}: {ln.strip()[:60]!r}")
    return items


def check_folios(pages):
    items, prev = [], None
    for leaf, text in pages:
        m = re.match(r"\[\[page (\d+)\]\]", text)
        if not m:
            continue
        n = int(m.group(1))
        if prev is not None and not (prev[1] < n <= prev[1] + 6):
            items.append(f"{leaf}: page {n} after page {prev[1]} ({prev[0]})")
        prev = (leaf, n)
    return items


def first_text(text):
    for ln in text.splitlines():
        s = ln.strip()
        if s and not re.fullmatch(r"\[\[(page [^\]]*|blank)\]\]", s) and not re.fullmatch(r"<(blockquote|verse)>", s):
            return s
    return ""


def last_text(text):
    for ln in reversed(text.splitlines()):
        s = ln.strip()
        if s and not s.startswith("[[fn ") and not re.fullmatch(r"</(blockquote|verse)>", s):
            return s
    return ""


def check_joins(pages):
    items = []
    for (l0, t0), (l1, t1) in zip(pages, pages[1:]):
        a, b = last_text(t0), first_text(t1)
        if not a or not b or a.startswith(("#", "[[image", "[[caption", "|")) or b.startswith(("#", "[[image", "|")):
            continue
        pa = re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", "", a).strip()
        pb = re.sub(r"<[^>]+>|\[\[[^\]]*\]\]", "", b).strip()
        cont = b.startswith("[[cont]]")
        closed = bool(re.search(r"[.?!][”’\")\]]*$", pa))
        if not cont and (pa.endswith("-") or (not closed and pb[:1].islower())):
            items.append(f"{l1}: no [[cont]] but the page before ends …{pa[-25:]!r} and this one starts {pb[:25]!r}")
        elif cont and closed and pb[:1].isupper() and not pa.endswith(("Mr.", "Mrs.", "Dr.", "St.")):
            items.append(f"{l1}: [[cont]] after a closed sentence …{pa[-25:]!r} | {pb[:25]!r}")
    return items


# ---------------------------------------------------------------- checks on what was built

def check_text(streams):
    stray, straight, spacing = [], [], []
    for label, text in streams:
        for m in re.finditer(r"\[\[|\]\]|</?(?:i|b|sc|sup|sub|pref|blockquote|verse|pb|corr|noteref|pageref)\b|〓|[⟦⟧]|&(?:lt|gt|amp);", text):
            stray.append(f"{label}: …{text[max(0, m.start() - 30):m.end() + 30]!r}…")
        for m in re.finditer(r"['\"]", text):
            straight.append(f"{label}: …{text[max(0, m.start() - 25):m.end() + 25]!r}…")
        for m in re.finditer(r"\w [;:!?,](?!\S*[;:!?,.]{2})|(?<=\w) \.(?= |$)(?! \. )|[“‘] +\w|\w[,.;:!?]? +[”](?=[\s,.;:!?]|$)|\S  +\S", text):
            ctxt = text[max(0, m.start() - 25):m.end() + 25]
            if re.search(r"\. \. \.|\.\.\.", ctxt) and m.group(0).strip() in (".", " ."):
                continue
            spacing.append(f"{label}: …{ctxt!r}…")
    return stray[:40], straight[:40], spacing[:60]


def spacing_items(book):
    """Spacing is judged block by block on the JSON (the joins between blocks are not text)."""
    items = []
    for d in book["divisions"]:
        for b in d["blocks"] + d["notes"]:
            for s in rh.strings(b):
                t = inline.plain(s)
                items += [f"{b['leaf']}: {i[6:]}" for i in check_text([("x", t)])[2]]
                if t != t.strip():
                    items.append(f"{b['leaf']}: space at the start or end of a block: {t[:40]!r}")
    return items[:80]


def check_quote_balance(book):
    items = []
    for d in book["divisions"]:
        if not d.get("reading"):
            continue
        for b in d["blocks"]:
            if b["type"] != "paragraph":
                continue
            t = inline.plain(b["text"])
            depth = 0
            for c in t:
                if c == "“":
                    depth += 1
                elif c == "”":
                    depth -= 1
                    if depth < 0:
                        break
            if depth < 0:
                items.append(f"{b['leaf']}: closing ” with no opening “: {t[:60]!r}")
            elif depth > 1:
                items.append(f"{b['leaf']}: {depth} quotations left open: {t[:60]!r}")
    return items


def norm_title(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def check_contents(book):
    cont = [d for d in book["divisions"] if d["kind"] == "contents"]
    if not cont:
        return []
    heads = set()
    for d in book["divisions"]:
        heads.add(norm_title(d["title"]))
        for b in d["blocks"]:
            if b["type"] == "heading" or b.get("role") == "subtitle":
                heads.add(norm_title(inline.plain(b["text"])))
    blob = " | ".join(sorted(heads))
    items = []
    for d in cont:
        for b in d["blocks"]:
            for s in rh.strings(b):
                t = norm_title(re.sub(r"[\d ivxlc.]+$", "", inline.plain(s).strip(), flags=re.I))
                t = re.sub(r"^(chapter|chap|part|book|letter) [ivxlc\d]+ ?", "", t)
                if len(t) < 6 or t in ("contents", "page"):
                    continue
                key = " ".join(t.split()[:5])
                if key not in blob:
                    items.append(f"{b['leaf']}: {inline.plain(s).strip()[:70]!r}")
    return items


def check_links(out_dir, slug, epub_bytes):
    items = []
    bdir = os.path.join(out_dir, "books", slug)
    docs = {f: open(os.path.join(bdir, f), encoding="utf-8").read() for f in os.listdir(bdir) if f.endswith(".html")}
    z = zipfile.ZipFile(epub_bytes)
    edocs = {os.path.basename(n): z.read(n).decode("utf-8") for n in z.namelist() if n.endswith(".xhtml")}
    for label, group, base in (("web", docs, bdir), ("epub", edocs, None)):
        ids = {f: set(re.findall(r' id="([^"]+)"', x)) for f, x in group.items()}
        for f, x in group.items():
            for dup in {i for i in re.findall(r' id="([^"]+)"', x) if re.findall(r' id="([^"]+)"', x).count(i) > 1}:
                items.append(f"{label} {f}: id {dup!r} used twice")
            for href in re.findall(r' href="([^"]+)"', x):
                if re.match(r"[a-z]+:", href) or href.startswith("../"):
                    continue
                path, _, frag = href.partition("#")
                tgt = path or f
                if tgt in group:
                    if frag and frag not in ids[tgt]:
                        items.append(f"{label} {f}: link to missing anchor {href!r}")
                elif base is None or not os.path.exists(os.path.join(base, tgt)):
                    items.append(f"{label} {f}: link to missing file {href!r}")
            for src in re.findall(r' src="([^"]+)"', x):
                if label == "web" and not src.startswith(("http", "../")) and not os.path.exists(os.path.join(base, src)):
                    items.append(f"{label} {f}: missing image {src!r}")
    return items


def check_wellformed(out_dir, slug, epub_bytes, odt_bytes):
    items = []
    bdir = os.path.join(out_dir, "books", slug)
    for f in sorted(os.listdir(bdir)):
        if f.endswith(".html"):
            x = open(os.path.join(bdir, f), encoding="utf-8").read().replace("<!DOCTYPE html>", "", 1)
            try:
                ET.fromstring(x)
            except ET.ParseError as e:
                items.append(f"web {f}: {e}")
    for label, data in (("epub", epub_bytes), ("odt", odt_bytes)):
        z = zipfile.ZipFile(data)
        if z.testzip():
            items.append(f"{label}: damaged zip")
        if z.infolist()[0].filename != "mimetype" or z.infolist()[0].compress_type != zipfile.ZIP_STORED:
            items.append(f"{label}: mimetype is not the first, uncompressed entry")
        for n in z.namelist():
            if n.endswith((".xhtml", ".xml", ".opf")):
                try:
                    ET.fromstring(re.sub(rb"<!DOCTYPE html>", b"", z.read(n), count=1))
                except ET.ParseError as e:
                    items.append(f"{label} {n}: {e}")
    return items


def check_meta(cfg, bookdir):
    items = []
    need = ("id", "version", "date", "title", "authors", "place", "publisher", "year", "regions", "summary", "source", "history")
    for k in need:
        if not cfg.get(k):
            items.append(f"book.json: missing {k!r}")
    if cfg.get("id") != os.path.basename(os.path.normpath(bookdir)):
        items.append(f"book.json: id {cfg.get('id')!r} is not the directory name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(cfg.get("id", ""))):
        items.append("book.json: id must be lower-case words joined by hyphens")
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", str(cfg.get("date", ""))):
        items.append("book.json: date must be YYYY-MM-DD")
    if isinstance(cfg.get("year"), int) and cfg["year"] > 1913:
        items.append(f"book.json: year {cfg['year']} is not before 1914")
    if not (cfg.get("source") or {}).get("ia_identifier"):
        items.append("book.json: source.ia_identifier missing")
    if not any(h.get("version") == cfg.get("version") for h in cfg.get("history", [])):
        items.append("book.json: history has no entry for this version")
    for a in cfg.get("authors", []):
        if not a.get("name") or not a.get("sort"):
            items.append("book.json: each author needs name and sort")
    s = cfg.get("summary", "")
    s = " ".join(s) if isinstance(s, list) else s
    if s and not (30 <= len(s.split()) <= 220):
        items.append(f"book.json: summary has {len(s.split())} words (30–220 expected)")
    return items


def run_epubcheck(epub_path, jar):
    r = subprocess.run(["java", "-jar", jar, epub_path], capture_output=True, text=True)
    out = r.stdout + r.stderr
    m = re.search(r"Messages: (\d+) fatals? / (\d+) errors? / (\d+) warnings?", out)
    if m and m.groups() == ("0", "0", "0"):
        return []
    return [ln for ln in out.splitlines() if re.match(r"(FATAL|ERROR|WARNING)", ln)][:30] or [out.strip()[-300:] or "epubcheck gave no result"]


def run_soffice(odt_path, tmp):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        return ["LibreOffice (soffice) is not installed: cannot check the ODT"]
    r = subprocess.run([exe, "--headless", f"-env:UserInstallation=file://{tmp}/lo", "--convert-to", "pdf", "--outdir", tmp, odt_path],
                       capture_output=True, text=True, timeout=600)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(odt_path))[0] + ".pdf")
    if not os.path.exists(pdf) or os.path.getsize(pdf) < 2000:
        return [f"LibreOffice did not convert the ODT: {(r.stdout + r.stderr).strip()[-200:]}"]
    return []


# ---------------------------------------------------------------- main

def run(bookdir, epubcheck=None, skip_epubcheck=False, skip_odt=False, verbose=False):
    bookdir = os.path.normpath(bookdir)
    cfg, pages = compile_book.load(bookdir)
    res = collections.OrderedDict((k, []) for k in CHECKS)
    skipped = []
    tmp = tempfile.mkdtemp(prefix="preflight-")
    try:
        book, warnings = build_site.build_book(tmp, bookdir)
        slug = book["id"]
        bdir = os.path.join(tmp, "books", slug)
        epub_path, odt_path = os.path.join(bdir, slug + ".epub"), os.path.join(bdir, slug + ".odt")
        res["meta"] = check_meta(cfg, bookdir)
        res["markup"] = check_markup(pages)
        res["sc-caps"] = check_sc(pages)
        res["heading-caps"] = check_heading_caps(pages)
        res["hyphen-joins"] = [w for w in warnings if w.startswith("hyphen join")]
        res["compile"] = [w for w in warnings if not w.startswith("hyphen join")]
        res["folios"] = check_folios(pages)
        res["joins"] = check_joins(pages)
        # conservation
        pm, pn = page_streams(pages)
        jm, jn = json_streams(book)
        res["conservation"] += compare(pm, jm, "pages→JSON text") + compare(pn, jn, "pages→JSON notes")
        rm, rn = json_streams(book, reading_only=True)
        names = rh.file_names(book, ".html")
        web = []
        for d in rh.reading_divisions(book):
            x = open(os.path.join(bdir, names[d["id"]]), encoding="utf-8").read()
            web.append(re.search(r'<article class="book">(.*)</article>', x, flags=re.S).group(1))
        wm, wn = html_streams(web)
        z = zipfile.ZipFile(epub_path)
        ep = []
        for d in rh.reading_divisions(book):
            x = z.read("OEBPS/text/" + names[d["id"]].replace(".html", ".xhtml")).decode("utf-8")
            ep.append(re.search(r"<section epub:type=[^>]*>(.*)</section>\s*</body>", x, flags=re.S).group(1))
        em, en = html_streams(ep)
        om, on = odt_streams(odt_path)
        res["conservation"] += compare(rm, wm, "JSON→web text") + compare(rn, wn, "JSON→web notes")
        res["conservation"] += compare(rm, em, "JSON→EPUB text") + compare(rn, en, "JSON→EPUB notes")
        res["conservation"] += compare(rm, om, "JSON→ODT text")
        if sorted(squash(inline.plain(n["text"])) for d in rh.reading_divisions(book) for n in d["notes"]) != \
                sorted(squash(x) for x in odt_notes(odt_path)):
            res["conservation"].append("JSON→ODT notes: the footnotes of the ODT are not the notes of the JSON")
        res["stray-markup"], res["straight-quotes"], _ = check_text(
            [("text", jm), ("notes", jn), ("web", wm + " " + wn), ("epub", em + " " + en), ("odt", om)])
        # the same item in all formats is one problem: keep the JSON ("text"/"notes") report when it exists
        for k in ("stray-markup", "straight-quotes"):
            base = [i for i in res[k] if i.startswith(("text:", "notes:"))]
            res[k] = base or res[k]
        res["spacing"] = spacing_items(book)
        res["quote-balance"] = check_quote_balance(book)
        res["contents"] = check_contents(book)
        res["links"] = check_links(tmp, slug, epub_path)
        res["wellformed"] = check_wellformed(tmp, slug, epub_path, odt_path)
        rd = rh.reading_divisions(book)
        if not rd:
            res["nav"].append("no division is in the reading editions")
        for d in rd:
            if not d["title"] or d["title"].startswith("[Untitled"):
                res["nav"].append(f"{d['id']} ({d['first_leaf']}): no title")
            if not d["blocks"]:
                res["nav"].append(f"{d['id']} ({d['first_leaf']}): empty")
        idir = os.path.join(bookdir, "images")
        if os.path.isdir(idir):
            used = {os.path.basename(b["src"]) for d in book["divisions"] for b in d["blocks"] if b["type"] == "image"} | {"cover.jpg", "cover.png"}
            res["images"] = [f"images/{f} is not used" for f in sorted(os.listdir(idir)) if f not in used]
        a = cfg.get("audit") or {}
        if a.get("version") != cfg.get("version") or not a.get("pages") or "real_errors" not in a or "recall" not in a:
            res["audit"].append('book.json "audit" must record this version: {"version", "date", "pages", "recall", "real_errors", "fixed"}')
        sj = os.path.join(bookdir, "source.json")
        if not os.path.exists(sj):
            res["source"].append("no source.json")
        else:
            src = json.load(open(sj, encoding="utf-8"))
            missing = [p["name"] for p in src.get("parts", []) if not p.get("drive_id")]
            if not src.get("parts") or missing:
                res["source"].append(f"Drive cache incomplete: {len(missing)} parts without a drive_id" if src.get("parts") else "no parts recorded")
        if skip_epubcheck:
            skipped.append("epubcheck")
        else:
            jar = epubcheck or os.environ.get("EPUBCHECK_JAR")
            res["epubcheck"] = run_epubcheck(epub_path, jar) if jar and os.path.exists(jar) else ["epubcheck jar not found (set EPUBCHECK_JAR; tools/setup_env.sh installs it)"]
        if skip_odt:
            skipped.append("odt")
        else:
            res["odt"] = run_soffice(odt_path, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    waivers = cfg.get("waivers", [])
    used_w = [0] * len(waivers)
    waived = 0
    for k in res:
        keep = []
        for item in res[k]:
            w = next((i for i, w in enumerate(waivers) if w.get("check") == k and w.get("match", "") in item and w.get("why")), None)
            if w is None:
                keep.append(item)
            else:
                used_w[w] += 1
                waived += 1
        res[k] = keep
    lines, fails, observed = [], 0, []
    for k, (mode, what) in CHECKS.items():
        n = len(res[k])
        if k in skipped:
            status = "SKIPPED"
        elif mode == "enforce":
            status = "ok" if n == 0 else f"FAIL ({n})"
            fails += n
        else:
            status = "ok" if n == 0 else f"look ({n})"
            if n:
                observed.append(f"{k} {n}")
        lines.append(f"[{status:>9}] {k}: {what}")
        show = res[k] if (verbose or mode == "enforce") else res[k][:40]
        lines += [f"            - {i}" for i in show]
        if len(show) < n:
            lines.append(f"            … {n - len(show)} more (-v)")
    for i, w in enumerate(waivers):
        if not used_w[i]:
            lines.append(f"[   unused] waiver matches nothing: {w}")
        if not w.get("why"):
            lines.append(f"[  invalid] waiver without a reason: {w}")
    try:
        rev = subprocess.run(["git", "-C", HERE, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "?"
    except Exception:
        rev = "?"
    verdict = "PASS" if fails == 0 and not skipped else ("FAIL" if fails else "INCOMPLETE")
    stamp = (f"preflight {verdict}: {cfg.get('id')} v{cfg.get('version')} — {fails} to fix, {waived} waived"
             f"{'; skipped: ' + ', '.join(skipped) if skipped else ''}"
             f"{'; to look at: ' + ', '.join(observed) if observed else ''} — tools@{rev} {datetime.date.today().isoformat()}")
    lines.append(stamp)
    return verdict, "\n".join(lines), res


def odt_notes(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("content.xml"))
    out = []
    for n in root.iter(T + "note"):
        out.append("".join(n.find(T + "note-body").itertext()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bookdir")
    ap.add_argument("--epubcheck")
    ap.add_argument("--skip-epubcheck", action="store_true", help="tests only: the result is then INCOMPLETE, never PASS")
    ap.add_argument("--skip-odt", action="store_true", help="tests only")
    ap.add_argument("--report")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args()
    verdict, report, _ = run(a.bookdir, a.epubcheck, a.skip_epubcheck, a.skip_odt, a.v)
    print(report)
    if a.report:
        open(a.report, "w", encoding="utf-8").write(report + "\n")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
