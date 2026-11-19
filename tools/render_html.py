#!/usr/bin/env python3
"""Book JSON -> XHTML-compatible HTML for the website and for the EPUB (shared block renderer).

Used by build_site.py and render_epub.py. Nothing here reads page files: the book JSON is the only input.
"""
import html, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inline  # noqa: E402


SHORT_SUBTITLE = 80


def short_subtitle(text):
    """A chapter title or short summary (one line) is centred under the heading; a long list of topics is not."""
    return len(inline.plain(text)) <= SHORT_SUBTITLE

esc = lambda s: html.escape(s, quote=False)
attr = lambda s: html.escape(s, quote=True)


def reading_divisions(book):
    return [d for d in book["divisions"] if d.get("reading")]


def file_names(book, ext):
    """division id -> file name, for the divisions of the reading editions."""
    return {d["id"]: f"{i:02d}{ext}" for i, d in enumerate(reading_divisions(book), 1)}


def page_targets(book, names):
    """printed page number -> 'file#pg-N' for pages that start inside the reading editions (first occurrence wins)."""
    where = {}
    for d in reading_divisions(book):
        for n in page_starts(d):
            if n["n"] and n["n"] not in where:
                where[n["n"]] = f"{names[d['id']]}#pg-{anchor(n['n'])}"
    return where


def anchor(n):
    return re.sub(r"[^0-9A-Za-z]", "", n)


def strings(x):
    """Every inline string of a block or note, in reading order."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x:
            yield from strings(y)
    elif isinstance(x, dict):
        for k in ("text", "paragraphs", "stanzas", "rows", "caption"):
            if k in x:
                yield from strings(x[k])


def page_starts(div):
    out = []
    for b in div["blocks"]:
        out += b.get("pb", [])
        for s in strings(b):
            out += [{"n": html.unescape(n), "leaf": l} for n, l in re.findall(r'<pb n="([^"]*)" leaf="([^"]+)"/>', s)]
    return out


LONG_ITALIC_WORDS = 30     # a wholly italic paragraph or quotation of at least this many words is set in roman
LONG_ITALIC_LINES = 4      # a wholly italic piece of verse of at least this many lines likewise
ITALIC_SHARE = 0.9


def roman_long_italics(div):
    """A copy of a division for the reading editions (notes/style.md §Editions): long passages printed in italic
    — whole paragraphs, whole poems, chapter summaries, whole tables — are set in roman, and words that
    the print set in roman inside them, for contrast, in italic. The JSON keeps the italics as printed."""
    def stats(strs):
        it = tot = words = 0
        for s in strs:
            a, b, c = inline.italic_share(s)
            it, tot, words = it + a, tot + b, words + c
        return (it / tot if tot else 0), words

    def long_(strs, min_words):
        share, words = stats(strs)
        return share >= ITALIC_SHARE and words >= min_words
    out = dict(div)
    blocks = []
    for b in div["blocks"]:
        b = dict(b)
        t = b["type"]
        if t == "paragraph":
            if long_([b["text"]], 2 if b.get("role") == "subtitle" else LONG_ITALIC_WORDS):
                b["text"] = inline.swap_italics(b["text"])
        elif t == "quote":
            whole = long_([p["text"] for p in b["paragraphs"]], LONG_ITALIC_WORDS)
            b["paragraphs"] = [dict(p, text=inline.swap_italics(p["text"])) if whole or long_([p["text"]], LONG_ITALIC_WORDS) else p
                               for p in b["paragraphs"]]
        elif t == "verse":
            lines = [x for s in b["stanzas"] for x in s]
            if len(lines) >= LONG_ITALIC_LINES and long_(lines, 1):
                b["stanzas"] = [[inline.swap_italics(x) for x in s] for s in b["stanzas"]]
        elif t == "table":
            cells = [c for r in b["rows"] for c in r]
            if len(b["rows"]) >= 2 and long_(cells, 1):
                b["rows"] = [[inline.swap_italics(c) for c in r] for r in b["rows"]]
        blocks.append(b)
    out["blocks"] = blocks
    out["notes"] = [dict(n, text=inline.swap_italics(n["text"])) if long_([n["text"]], LONG_ITALIC_WORDS) else n for n in div["notes"]]
    return out


class Ctx:
    """What differs between the website and the EPUB."""
    def __init__(self, book, flavor, names):
        self.book, self.flavor, self.names = book, flavor, names
        self.targets = page_targets(book, names)
        self.seen_pg, self.seen_ref = set(), set()
        src = book.get("source", {})
        self.ia = src.get("ia_identifier")
        self.hidden = sorted(src.get("hidden_leaves", []))

    def scan_url(self, leaf):
        if not self.ia:
            return None
        m = re.search(r"\d+", leaf)
        n = int(m.group(0))
        n -= sum(1 for h in self.hidden if h < n)
        return f"https://archive.org/details/{self.ia}/page/n{n}/mode/1up"

    def pb(self, n, leaf):
        a = anchor(n)
        ident = ""
        if a and a not in self.seen_pg:
            self.seen_pg.add(a)
            ident = f' id="pg-{a}"'
        if self.flavor == "epub":
            if not ident:
                return ""
            return f'<span epub:type="pagebreak" role="doc-pagebreak"{ident} aria-label="{attr(n)}"></span>'
        url = self.scan_url(leaf)
        label = n or "–"
        title = f"Page {n} of the printed book: open the scan" if n else "Unnumbered page: open the scan"
        if url:
            return f'<a class="pb"{ident} href="{attr(url)}" title="{attr(title)}">{esc(label)}</a>'
        return f'<span class="pb"{ident}>{esc(label)}</span>'

    def inline(self, s):
        out, closers = [], []
        for t in inline.tokens(s):
            if t[0] == "text":
                out.append(esc(t[1]))
            elif t[0] == "empty" and t[1] == "pb":
                out.append(self.pb(t[2].get("n", ""), t[2].get("leaf", "")))
            elif t[0] == "open":
                name, a = t[1], t[2]
                close = f"</{name}>"
                if name == "sc":
                    out.append('<span class="sc">'); close = "</span>"
                elif name == "noteref":
                    et = ' epub:type="noteref"' if self.flavor == "epub" else ""
                    # a second reference to the same note ([[fnref * again]]) gets no id: ids must be unique
                    ident = "" if a["to"] in self.seen_ref else f' id="r-{a["to"]}"'
                    self.seen_ref.add(a["to"])
                    out.append(f'<a class="noteref"{et} role="doc-noteref" href="#{a["to"]}"{ident}>'); close = "</a>"
                elif name == "pageref":
                    tgt = self.targets.get(a.get("n", ""))
                    out.append(f'<a class="pageref" href="{attr(tgt)}">' if tgt else "")
                    close = "</a>" if tgt else ""
                elif name == "corr":
                    web = self.flavor == "web"
                    out.append(f'<span class="corr" title="Printed: {attr(a.get("orig", ""))}">' if web else "")
                    close = "</span>" if web else ""
                else:
                    out.append(f"<{name}>")
                closers.append(close)
            elif t[0] == "close":
                out.append(closers.pop() if closers else "")
        return "".join(out)

    def blocks(self, div):
        div = roman_long_italics(div)
        body, prev = [], None
        targets = section_targets(div)
        for bi, b in enumerate(div["blocks"]):
            n0 = len(body)
            t = b["type"]
            pbs = "".join(self.pb(p["n"], p["leaf"]) for p in b.get("pb", []))
            if t == "heading":
                lv = b["level"]
                body.append(f'<h{lv}>{pbs}{self.inline(b["text"])}</h{lv}>')
            elif t == "paragraph":
                cls = []
                if b.get("role") == "subtitle":
                    cls += ["subtitle", "short"] if short_subtitle(b["text"]) else ["subtitle"]
                elif b.get("align"):
                    cls.append(b["align"])
                elif prev in (None, "heading", "image", "break", "subtitle", "table", "quote", "verse"):
                    cls.append("first")
                c = f' class="{" ".join(cls)}"' if cls else ""
                body.append(f'<p{c}>{pbs}{self.inline(b["text"])}</p>')
            elif t == "quote":
                ps = []
                for i, p in enumerate(b["paragraphs"]):
                    c = f' class="{p["align"]}"' if p.get("align") else ""
                    ps.append(f'<p{c}>{pbs if i == 0 else ""}{self.inline(p["text"])}</p>')
                body.append("<blockquote>" + "".join(ps) + "</blockquote>")
            elif t == "verse":
                st = []
                for i, s in enumerate(b["stanzas"]):
                    lines = "".join(f'<span class="line">{pbs if i == 0 and j == 0 else ""}{self.inline(x)}</span>' for j, x in enumerate(s))
                    st.append(f'<p>{lines}</p>')
                body.append('<div class="verse">' + "".join(st) + "</div>")
            elif t == "image":
                cap = f'<figcaption>{self.inline(b["caption"])}</figcaption>' if b.get("caption") else ""
                body.append(f'<figure>{pbs}<img src="{attr(b["src"])}" alt="{attr(b["alt"])}"/>{cap}</figure>')
            elif t == "table":
                trs = "".join("<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in r) + "</tr>" for r in b["rows"])
                body.append(f'<div class="tablewrap">{pbs}<table>{trs}</table></div>')
            elif t == "break":
                body.append(f'<hr class="break"/>{pbs}')
            if bi in targets and len(body) > n0:
                # the anchor of a contents entry goes on the block's first element
                body[n0] = re.sub(r"^<(\w+)", lambda m: f'<{m.group(1)} id="{targets[bi]}"', body[n0], count=1)
            prev = "subtitle" if b.get("role") == "subtitle" else t
        if div["notes"]:
            items = []
            for n in div["notes"]:
                et = ' epub:type="footnote"' if self.flavor == "epub" else ""
                back = f'<a class="noteback" href="#r-{n["id"]}" aria-label="Back to the text">{esc(n["mark"])}</a>'
                items.append(f'<aside class="note"{et} role="doc-footnote" id="{n["id"]}"><p>{back} {self.inline(n["text"])}</p></aside>')
            body.append('<section class="notes" aria-label="Notes"><hr/>' + "\n".join(items) + "</section>")
        s = "\n".join(body)
        # a reference whose note is in the same file keeps its link; its back-link needs the reference to exist
        ids = set(re.findall(r' id="(r-[^"]+)"', s))
        s = re.sub(r'<a class="noteback" href="#(r-[^"]+)" aria-label="[^"]*">(.*?)</a>',
                   lambda m: m.group(0) if m.group(1) in ids else f'<span class="noteback">{m.group(2)}</span>', s)
        return s


def nav_tree(book):
    """[(division, [child divisions])] for the reading editions: chapters nest under the part before them."""
    tree, part = [], None
    for d in reading_divisions(book):
        if d["kind"] == "part":
            part = (d, [])
            tree.append(part)
        elif d["kind"] == "chapter" and part is not None:
            part[1].append(d)
        else:
            part = None
            tree.append((d, []))
    return tree


def toc_title(d):
    """The division's entry in the contents: `toc_title` (e.g. the chapter summary in full) or its title."""
    return d.get("toc_title") or d["title"]


def section_id(k):
    return f"sec-{k + 1}"


def toc_tree(book):
    """[(title, division id, fragment or None, [children])] — the contents of the reading editions: divisions,
    chapters nested under their part, and a division's `sections` (book.json toc_entries) nested under it."""
    def node(d, kids):
        subs = [(x["title"], d["id"], section_id(k), []) for k, x in enumerate(d.get("sections", []))]
        return (toc_title(d), d["id"], None, subs + [node(c, []) for c in kids])
    return [node(d, kids) for d, kids in nav_tree(book)]


def section_targets(div):
    """block index -> anchor id, for the blocks the contents point at."""
    return {x["block"]: section_id(k) for k, x in enumerate(div.get("sections", []))}


def nav_list(book, names, prefix=""):
    def li(n):
        title, did, frag, kids = n
        inner = f'<a href="{prefix}{names[did]}{"#" + frag if frag else ""}">{esc(title)}</a>'
        if kids:
            inner += "<ol>" + "".join(li(k) for k in kids) + "</ol>"
        return f"<li>{inner}</li>"
    return "<ol>" + "\n".join(li(n) for n in toc_tree(book)) + "</ol>"


def authors_text(book):
    """'A, B' for the authors; '; edited by C' for those with "role": "editor"."""
    au = book.get("authors", [])
    main = ", ".join(a["name"] for a in au if not a.get("role")) or "Anonymous"
    eds = ", ".join(a["name"] for a in au if a.get("role") == "editor")
    return main + (f"; edited by {eds}" if eds else "")
