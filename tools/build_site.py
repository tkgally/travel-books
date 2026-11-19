#!/usr/bin/env python3
"""Build the whole website into a directory (default _site/). Run by the Pages workflow and by preflight.

  build_site.py [--out _site] [--only SLUG] [--bookdir DIR]

For every book in books/<slug>/ (or the one given with --bookdir, e.g. a book still in wip/):
  books/<slug>/index.html     the book's page
  books/<slug>/NN.html        the reading text, one file per division
  books/<slug>/<slug>.json    the book JSON (base of everything else)
  books/<slug>/<slug>.epub, <slug>.odt
  books/<slug>/images/
Plus index.html, about.html, json-format.html, assets/. Standard library only; output is deterministic.
"""
import argparse, html, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import compile_book, inline, render_html as rh, render_epub, render_odt  # noqa: E402

SITE = "Travel Books"
REPO_URL = "https://github.com/tkgally/travel-books"
esc = rh.esc
attr = rh.attr


def page(title, body, root, crumbs=(), extra_head="", book_css=False):
    """root = relative path to the site root ('' or '../../')."""
    nav = "".join(f'<li><a href="{attr(h)}">{esc(t)}</a></li>' for t, h in crumbs)
    css = f'<link rel="stylesheet" href="{root}assets/book.css"/>' if book_css else ""
    full = f"{title} – {SITE}" if title != SITE else SITE
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(full)}</title>
<link rel="stylesheet" href="{root}assets/site.css"/>
{css}{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to the text</a>
<header class="site">
<p class="sitename"><a href="{root}index.html">{SITE}</a></p>
<nav aria-label="Site"><ul><li><a href="{root}index.html#books">Books</a></li><li><a href="{root}about.html">About</a></li></ul></nav>
</header>
{f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{nav}</ol></nav>' if nav else ''}
<main id="main">
{body}
</main>
<footer class="site">
<p>The transcriptions on this site are in the public domain (<a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>).
Found an error? <a href="{REPO_URL}/issues">Report it on GitHub</a>.</p>
</footer>
</body>
</html>
"""


def book_line(b, href):
    a = rh.authors_text(b)
    regions = ", ".join(b.get("regions", []))
    return (f'<li><a href="{attr(href)}"><cite>{esc(b.get("short_title") or b["title"])}</cite></a>, {esc(a)} ({b.get("year", "")})'
            + (f'<br/><span class="meta">{esc(regions)}</span>' if regions else "") + "</li>")


def sort_key(b):
    a = (b.get("authors") or [{}])[0]
    return (a.get("sort") or a.get("name") or "", b.get("year") or 0)


def build_index(out, books, queue):
    items = "\n".join(book_line(b, f"books/{b['id']}/index.html") for b in sorted(books, key=sort_key))
    q = [x for x in queue if x.get("status") in ("queued", "in progress")]
    qitems = "\n".join(
        f'<li><cite>{esc(inline.smart_quotes(x["title"]))}</cite>, {esc(inline.smart_quotes(x.get("author", "")))} ({x.get("year", "")})'
        + (' <span class="meta">— in progress</span>' if x["status"] == "in progress" else "")
        + (f' <span class="meta"><a href="https://archive.org/details/{attr(x["ia"])}">scan</a></span>' if x.get("ia") else "") + "</li>"
        for x in q)
    body = f"""<h1>{SITE}</h1>
<p>First-person travel books written in English and published before 1914, transcribed from library scans at the
Internet Archive. The books here have no other digital text edition and were not reprinted after 1914.
Each can be read on this site or downloaded as EPUB, ODT or JSON. <a href="about.html">About the project.</a></p>
<h2 id="books">Books</h2>
{f'<ul class="books">{items}</ul>' if items else '<p>No books have been published yet.</p>'}
<h2 id="queue">In the queue</h2>
{f'<p>Books chosen for transcription, not yet published.</p><ul class="books">{qitems}</ul>' if qitems else '<p>The queue is empty.</p>'}
"""
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page(SITE, body, ""))


def md_page(out, name, title, src):
    """A very small Markdown subset (headings, paragraphs, lists, code blocks, tables, `code`, [links](url), *em*)."""
    lines = open(src, encoding="utf-8").read().splitlines()
    outl, i = [], 0

    def inl(s):
        s = esc(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", s)
        return s
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            outl.append("<pre><code>" + esc("\n".join(lines[i + 1:j])) + "</code></pre>")
            i = j + 1
        elif re.match(r"#{1,3} ", ln):
            n = len(ln.split(" ")[0])
            text = ln[n + 1:]
            ident = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            outl.append(f'<h{n} id="{ident}">{inl(text)}</h{n}>')
            i += 1
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("  ")):
                if lines[i].startswith("- "):
                    items.append(lines[i][2:])
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            outl.append("<ul>" + "".join(f"<li>{inl(x)}</li>" for x in items) + "</ul>")
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.fullmatch(r"\|[-| :]+\|", lines[i].strip()):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head = "<tr>" + "".join(f'<th scope="col">{inl(c)}</th>' for c in rows[0]) + "</tr>"
            rest = "".join("<tr>" + "".join(f"<td>{inl(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            outl.append(f'<div class="tablewrap"><table class="doc"><thead>{head}</thead><tbody>{rest}</tbody></table></div>')
        elif not ln.strip():
            i += 1
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,3} |- |\||```)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            outl.append("<p>" + inl(" ".join(para)) + "</p>")
    open(os.path.join(out, name), "w", encoding="utf-8").write(page(title, "\n".join(outl), "", crumbs=[(SITE, "index.html"), (title, name)]))


def build_book(out, bookdir, strict=True):
    book, warnings = compile_book.compile_book(bookdir)
    slug = book["id"]
    cfg = json.load(open(os.path.join(bookdir, "book.json"), encoding="utf-8"))
    bout = os.path.join(out, "books", slug)
    os.makedirs(bout, exist_ok=True)
    idir = os.path.join(bookdir, "images")
    open(os.path.join(bout, slug + ".json"), "w", encoding="utf-8").write(compile_book.dumps(book))
    open(os.path.join(bout, slug + ".epub"), "wb").write(render_epub.render(book, idir))
    open(os.path.join(bout, slug + ".odt"), "wb").write(render_odt.render(book, idir))
    names = rh.file_names(book, ".html")
    ctx = rh.Ctx(book, "web", names)
    divs = rh.reading_divisions(book)
    used = set()
    short = book.get("short_title") or book["title"]
    extra = f"<style>{cfg['css_extra']}</style>" if cfg.get("css_extra") else ""
    for i, d in enumerate(divs):
        body = ctx.blocks(d)
        used.update(re.findall(r'<img src="images/([^"]+)"', body))
        prev_ = f'<a rel="prev" href="{names[divs[i - 1]["id"]]}">← {esc(divs[i - 1]["title"])}</a>' if i else "<span></span>"
        next_ = f'<a rel="next" href="{names[divs[i + 1]["id"]]}">{esc(divs[i + 1]["title"])} →</a>' if i + 1 < len(divs) else "<span></span>"
        pager = f'<nav class="pager" aria-label="Chapters">{prev_}<a href="index.html#contents">Contents</a>{next_}</nav>'
        toggle = ('<p class="pbtoggle"><label><input type="checkbox" id="showpb"/> Show the page numbers of the printed book '
                  "(each links to the scanned page)</label></p>")
        html_ = page(f"{d['title']} – {short}",
                     f'{pager}\n{toggle}\n<article class="book">\n{body}\n</article>\n{pager}', "../../",
                     crumbs=[(SITE, "../../index.html"), (short, "index.html"), (d["title"], names[d["id"]])],
                     extra_head=extra + '<script src="../../assets/site.js" defer=""></script>', book_css=True)
        open(os.path.join(bout, names[d["id"]]), "w", encoding="utf-8").write(html_)
    if os.path.isdir(idir):
        os.makedirs(os.path.join(bout, "images"), exist_ok=True)
        for f in sorted(used | ({"cover.jpg"} & set(os.listdir(idir)))):
            if os.path.exists(os.path.join(idir, f)):
                shutil.copyfile(os.path.join(idir, f), os.path.join(bout, "images", f))
    open(os.path.join(bout, "index.html"), "w", encoding="utf-8").write(book_page(book, names, os.path.exists(os.path.join(idir, "cover.jpg"))))
    return book, warnings


def book_page(book, names, has_cover=False):
    src = book.get("source", {})
    ia = src.get("ia_identifier")
    slug = book["id"]
    rows = []

    def row(k, v):
        if v:
            rows.append(f'<tr><th scope="row">{esc(k)}</th><td>{v}</td></tr>')
    authors = []
    for a in book.get("authors", []):
        dates = f' ({a.get("born", "?")}–{a.get("died", "?")})' if a.get("born") or a.get("died") else ""
        authors.append(esc(a["name"] + dates))
    row("Author" if len(authors) < 2 else "Authors", "; ".join(authors) or "Anonymous")
    row("Title", f'<cite>{esc(book["title"])}</cite>' + (f': {esc(book["subtitle"])}' if book.get("subtitle") else ""))
    row("Published", esc(", ".join(x for x in (book.get("place"), book.get("publisher"), str(book.get("year", ""))) if x)))
    row("Edition transcribed", esc(book.get("edition_statement", "")))
    row("Volumes", esc(str(book.get("volumes", ""))) if book.get("volumes") else "")
    row("Places", esc(", ".join(book.get("regions", []))))
    row("Time of the journey", esc(book.get("period", "")))
    row("Subjects", esc("; ".join(book.get("subjects", []))))
    if ia:
        row("Scan", f'<a href="https://archive.org/details/{attr(ia)}">archive.org/details/{esc(ia)}</a>'
            + (f', from {esc(src["contributor"])}' if src.get("contributor") else ""))
    row("This edition", f'version {book["version"]}, {esc(book["date"])}')
    summary = book.get("summary", "")
    summary = [summary] if isinstance(summary, str) else summary
    npages = sum(1 for p in book["pages"] if not p["blank"])
    first = names[rh.reading_divisions(book)[0]["id"]] if rh.reading_divisions(book) else None
    viewer = (f'<details class="viewer"><summary>Look through the scanned pages here</summary>'
              f'<iframe src="https://archive.org/embed/{attr(ia)}" title="Scanned pages of the book at the Internet Archive" loading="lazy" allowfullscreen=""></iframe></details>') if ia else ""
    corr = book.get("corrections", [])
    pnum = {p["leaf"]: p["number"] for p in book["pages"]}
    corr_rows = "".join(
        f'<tr><td>{esc(pnum.get(c["leaf"], "") or c["leaf"])}</td><td>{esc(c["printed"])}</td><td>{esc(c["corrected"])}</td></tr>' for c in corr)
    notes = "".join(f"<li>{esc(n)}</li>" for n in book.get("notes_on_text", []))
    hist = "".join(f'<li>Version {h["version"]}, {esc(h["date"])}: {esc(h["note"])}</li>' for h in book.get("history", []))
    cover = '<img class="cover" src="images/cover.jpg" alt="Cover of the book"/>' if has_cover else ""
    body = f"""<h1><cite>{esc(book.get("short_title") or book["title"])}</cite></h1>
<p class="byline">{esc(rh.authors_text(book))}, {book.get("year", "")}</p>
{cover}
{"".join(f"<p>{esc(s)}</p>" for s in summary)}
<h2 id="read">Read</h2>
<ul class="actions">
{f'<li><a href="{first}">Read on this site</a> (contents below)</li>' if first else ''}
<li><a href="{slug}.epub" download="">EPUB</a> for e-readers</li>
<li><a href="{slug}.odt" download="">ODT</a> for word processors</li>
<li><a href="{slug}.json">JSON</a>: the complete transcription, including the parts left out of the other versions
(<a href="../../json-format.html">format</a>)</li>
{f'<li><a href="https://archive.org/details/{attr(ia)}">The scan at the Internet Archive</a></li>' if ia else ''}
</ul>
{viewer}
<h2 id="contents">Contents</h2>
<nav class="toc" aria-label="Contents of the book">{rh.nav_list(book, names)}</nav>
<h2 id="about-book">The book</h2>
<div class="tablewrap"><table class="bib">{"".join(rows)}</table></div>
<h2 id="text">The text</h2>
<p>Transcribed from the scan ({npages} pages with text or pictures) with the spelling, punctuation and wording of the original;
spaces around punctuation follow modern practice. {esc(book.get("omitted_from_reading", ""))}</p>
{f'<ul>{notes}</ul>' if notes else ''}
{f'<h3>Printer’s errors corrected</h3><div class="tablewrap"><table class="doc"><thead><tr><th scope="col">Page</th><th scope="col">Printed</th><th scope="col">Corrected to</th></tr></thead><tbody>{corr_rows}</tbody></table></div>' if corr else '<p>No corrections were made to the printed text.</p>'}
{f'<h3>Versions</h3><ul>{hist}</ul>' if hist else ''}
"""
    return page(book.get("short_title") or book["title"], body, "../../",
                crumbs=[(SITE, "../../index.html"), (book.get("short_title") or book["title"], "index.html")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "_site"))
    ap.add_argument("--bookdir", action="append", default=[], help="also build this book directory (e.g. wip/<slug>)")
    ap.add_argument("--only", help="build only the book with this id (plus the site pages)")
    a = ap.parse_args()
    out = a.out
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    for f in sorted(os.listdir(os.path.join(REPO, "site", "assets"))):
        shutil.copyfile(os.path.join(REPO, "site", "assets", f), os.path.join(out, "assets", f))
    open(os.path.join(out, ".nojekyll"), "w").close()
    dirs = [os.path.join(REPO, "books", d) for d in sorted(os.listdir(os.path.join(REPO, "books")))
            if os.path.exists(os.path.join(REPO, "books", d, "book.json"))] if os.path.isdir(os.path.join(REPO, "books")) else []
    dirs += a.bookdir
    books, nwarn = [], 0
    for d in dirs:
        if a.only and os.path.basename(os.path.normpath(d)) != a.only:
            continue
        book, warnings = build_book(out, d)
        books.append(book)
        nwarn += len(warnings)
        print(f"built {book['id']} v{book['version']}: {len(rh.reading_divisions(book))} reading divisions, {len(warnings)} compile warnings")
    qf = os.path.join(REPO, "data", "queue.json")
    queue = json.load(open(qf, encoding="utf-8"))["books"] if os.path.exists(qf) else []
    build_index(out, books, queue)
    md_page(out, "about.html", "About", os.path.join(REPO, "site", "about.md"))
    md_page(out, "json-format.html", "The JSON format", os.path.join(REPO, "site", "json-format.md"))
    print(f"site written to {out}: {len(books)} books")


if __name__ == "__main__":
    main()
