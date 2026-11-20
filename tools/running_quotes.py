#!/usr/bin/env python3
"""Running quotation marks: older books (here, 1797) repeat the opening mark “ at the start of every printed line
of a quotation. Joined into paragraphs, the repeats stand inside the text ('the “bar', 'ab“sence'). The text
policy (notes/style.md §"Running quotation marks", 2026-11-20) keeps the opening and closing marks of the quotation
and leaves out the repeats, as line-end hyphens are left out.

  running_quotes.py PAGES_DIR            list the repeats found (page, context)
  running_quotes.py PAGES_DIR --apply    take them out of the page files

A “ is a repeat when a quotation opened earlier in the same paragraph (or in the paragraph this page's [[cont]]
continues) has not been closed by ”. Single marks ‘ ’ (nested quotations, apostrophes) are not touched.
Side-notes, note lines and markup are passed over. Look at the list before --apply: a closing mark the printer
left out would make every later opening mark in the paragraph look like a repeat.
"""
import os, re, sys

SKIP = re.compile(r"\[\[[^\]]*\]\]|<[^<>]*>")


def scan(text, open_=False):
    """(new text, positions removed, open at the end) for one paragraph line."""
    out, removed, i = [], [], 0
    while i < len(text):
        m = SKIP.match(text, i)
        if m:
            out.append(m.group(0)); i = m.end(); continue
        c = text[i]
        if c == "“":
            if open_:
                removed.append(i)
                i += 1
                continue
            open_ = True
        elif c == "”":
            open_ = False
        out.append(c); i += 1
    return "".join(out), removed, open_


def is_para(line):
    s = line.strip()
    return bool(s) and not re.fullmatch(r"\[\[(page [^\]]*|blank|break)\]\]|</?(blockquote|verse)>", s) \
        and not s.startswith(("[[fn ", "[[image:", "#", "|"))


def process(pages):
    """pages = [(leaf, text)] in reading order -> ([(leaf, new text)], [(leaf, context)])."""
    out, changes, carry = [], [], False
    for leaf, text in pages:
        lines = text.split("\n")
        paras = [k for k, ln in enumerate(lines) if is_para(ln)]
        state = False
        for n, k in enumerate(paras):
            ln = lines[k]
            start = carry if (n == 0 and ln.lstrip().startswith("[[cont]]")) else False
            new, rem, state = scan(ln, start)
            for p in rem:
                changes.append((leaf, ln[max(0, p - 30):p + 30]))
            lines[k] = new
        carry = state if paras else carry
        out.append((leaf, "\n".join(lines)))
    return out, changes


def main():
    d = sys.argv[1]
    apply = "--apply" in sys.argv
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import compile_book
    names = compile_book.page_files(d)
    pages = [(f[:-4], open(os.path.join(d, f), encoding="utf-8").read()) for f in names]
    cfg = os.path.join(os.path.dirname(os.path.abspath(d)), "book.json")
    if os.path.exists(cfg):                        # reading order (leaves bound out of order)
        import json
        pages = compile_book.apply_leaf_order(pages, json.load(open(cfg, encoding="utf-8")).get("leaf_order"))
    new, changes = process(pages)
    for leaf, ctx in changes:
        print(f"{leaf}\t…{ctx}…")
    print(f"{len(changes)} repeated opening marks on {len({c[0] for c in changes})} pages", file=sys.stderr)
    if apply:
        for (leaf, old), (_, txt) in zip(pages, new):
            if txt != old:
                open(os.path.join(d, leaf + ".txt"), "w", encoding="utf-8").write(txt)


if __name__ == "__main__":
    main()
