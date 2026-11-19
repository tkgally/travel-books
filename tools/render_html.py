#!/usr/bin/env python3
"""Book JSON -> XHTML-compatible HTML for the website and for the EPUB (shared block renderer).

Used by build_site.py and render_epub.py. Nothing here reads page files: the book JSON is the only input.
"""
import html, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inline  # noqa: E402

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


class Ctx:
    """What differs between the website and the EPUB."""
    def __init__(self, book, flavor, names):
        self.book, self.flavor, self.names = book, flavor, names
        self.targets = page_targets(book, names)
        self.seen_pg = set()
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
                    out.append(f'<a class="noteref"{et} role="doc-noteref" href="#{a["to"]}" id="r-{a["to"]}">'); close = "</a>"
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
        body, prev = [], None
        for b in div["blocks"]:
            t = b["type"]
            pbs = "".join(self.pb(p["n"], p["leaf"]) for p in b.get("pb", []))
            if t == "heading":
                lv = b["level"]
                body.append(f'<h{lv}>{pbs}{self.inline(b["text"])}</h{lv}>')
            elif t == "paragraph":
                cls = []
                if b.get("role") == "subtitle":
                    cls.append("subtitle")
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


def nav_list(book, names, prefix=""):
    def li(d, kids):
        inner = f'<a href="{prefix}{names[d["id"]]}">{esc(d["title"])}</a>'
        if kids:
            inner += "<ol>" + "".join(li(k, []) for k in kids) + "</ol>"
        return f"<li>{inner}</li>"
    return "<ol>" + "\n".join(li(d, kids) for d, kids in nav_tree(book)) + "</ol>"


def authors_text(book):
    return ", ".join(a["name"] for a in book.get("authors", [])) or "Anonymous"
