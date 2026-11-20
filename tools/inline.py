#!/usr/bin/env python3
"""Inline text: page markup -> the inline markup used in the book JSON, and helpers to read it.

Book JSON inline markup (documented for users in docs/json-format.md) is a well-formed XML fragment:
  text with & < > escaped
  <i> <b> <sc> <sup> <sub>            italic, bold, small capitals, superscript, subscript
  <pb n="97" leaf="p0123"/>           a page of the printed book starts here (n = printed number, may be "")
  <noteref to="d004-n3">*</noteref>   reference to a note of the same division
  <pageref n="34">34</pageref>        the book's own reference to one of its pages
  <corr orig="teh">the</corr>         a printer's error corrected by the editors; orig = the printed reading
  <side>Arrival at Macao.</side>      a marginal note (side-note) printed beside the line whose first word follows it;
                                      kept in the JSON, left out of the reading editions (drop_sides) and of plain()
"""
import html, re

INLINE = ("i", "b", "sc", "sup", "sub")
TAG_RE = re.compile(r"(</?(?:%s)>)" % "|".join(INLINE))

# A ' at the start of a word is an apostrophe when the word is a known elision, otherwise an opening quote.
ELISIONS = re.compile(r"(?i)(tis|twas|twere|twill|twould|tho|twixt|tween|till|em|gainst|mongst|midst|bout|bove|cause|"
                      r"neath|pon|ere|d|ll|s|t|n|re|ve|o|un|ud|ome|im|is|er|ave|ad|ow|and|an|ee|appen|as|ope|alf|ead|ouse|ome|ell|orse|ard|art|eart|eaven)(?![a-z])|\d")
OPENERS = set(" \t\n([{—–-/“‘⟦⟧")


def smart_quotes(text):
    """Straight quotes -> curly. Tags and [[...]] markup are passed over."""
    out, prev = [], " "
    i = 0
    while i < len(text):
        c = text[i]
        if c == "<":
            j = text.find(">", i)
            if j > 0 and re.fullmatch(r"</?[a-z]+(?: [^<>]*)?/?>", text[i:j + 1]):
                out.append(text[i:j + 1]); i = j + 1; continue
        if c == "[" and text.startswith("[[", i):
            j = text.find("]]", i)
            if j > 0:
                out.append(text[i:j + 2]); i = j + 2; continue
        if c == "⟦":                       # internal token
            j = text.find("⟧", i)
            if j > 0:
                out.append(text[i:j + 1]); i = j + 1; continue
        if c == '"':
            c = "“" if prev in OPENERS else "”"
        elif c == "'":
            if prev in OPENERS:
                rest = re.sub(r"</?[a-z]+>", "", text[i + 1:i + 40])
                c = "’" if ELISIONS.match(rest) else "‘"
            else:
                c = "’"
        out.append(c); prev = c; i += 1
    return "".join(out)


def attr(s):
    return html.escape(s, quote=True)


def convert(text, warn=lambda m: None, ctx=""):
    """Page-markup inline text -> book-JSON inline markup.
    Note references come out as <noteref mark="*"/> placeholders; compile_book resolves them."""
    # a side-note stands before the word it is printed beside: the space after it goes, so that dropping it
    # leaves the sentence as printed; one at the end of a paragraph takes the space before it instead
    text = re.sub(r"\s*\[\[side:\s*([^\[\]]*?)\s*\]\]\s*$", r"⟦side⟧\1⟦/side⟧", text)
    text = re.sub(r"\[\[side:\s*([^\[\]]*?)\s*\]\]\s*", r"⟦side⟧\1⟦/side⟧", text)
    text = smart_quotes(text)
    hold = []

    def keep(s):
        hold.append(s)
        return f"\x00{len(hold) - 1}\x00"

    def esc(s):
        return html.escape(s, quote=False)

    def corr(m):
        return keep(f'<corr orig="{attr(m.group(1).strip())}">') + m.group(2).strip() + keep("</corr>")
    text = re.sub(r"\[\[corr ([^|\]]*)\|([^\]]*)\]\]", corr, text)
    text = re.sub(r"\[\[fnref ([^\]]+)\]\]", lambda m: keep(f'<noteref mark="{attr(m.group(1).strip())}"/>'), text)
    text = re.sub(r'<pref to="(\w+)">(.*?)</pref>', lambda m: keep(f'<pageref n="{m.group(1)}">') + m.group(2) + keep("</pageref>"), text)
    text = re.sub(r"<pref>(.*?)</pref>",
                  lambda m: keep('<pageref n="%s">' % re.sub(r"[^0-9A-Za-z]", "", m.group(1))) + m.group(1) + keep("</pageref>"), text)
    text = text.replace("⟦side⟧", keep("<side>")).replace("⟦/side⟧", keep("</side>"))
    text = re.sub(r"⟦pb:([^:⟧]*):([^⟧]*)⟧", lambda m: keep(f'<pb n="{attr(m.group(2))}" leaf="{m.group(1)}"/>'), text)
    parts = TAG_RE.split(text)
    stack, out, ok = [], [], True
    for p in parts:
        m = re.fullmatch(r"<(/?)(\w+)>", p) if TAG_RE.fullmatch(p or "") else None
        if not m:
            out.append(esc(p)); continue
        if m.group(1):
            if not stack or stack[-1] != m.group(2):
                ok = False; break
            stack.pop()
        else:
            if m.group(2) in stack:
                ok = False; break
            stack.append(m.group(2))
        out.append(p)
    if not ok or stack:
        warn(f"unbalanced or nested inline tags, stripped: {ctx} {text[:50]!r}")
        s = esc(TAG_RE.sub("", text))
    else:
        s = "".join(out)
    return re.sub(r"\x00(\d+)\x00", lambda m: hold[int(m.group(1))], s)


TOKEN = re.compile(r"<(/?)([a-z]+)((?: [a-z]+=\"[^\"]*\")*)\s*(/?)>")


def tokens(s):
    """Book-JSON inline markup -> list of ("text", str) | ("open", name, attrs) | ("close", name) | ("empty", name, attrs)."""
    out, pos = [], 0
    for m in TOKEN.finditer(s):
        if m.start() > pos:
            out.append(("text", html.unescape(s[pos:m.start()])))
        attrs = {k: html.unescape(v) for k, v in re.findall(r'([a-z]+)="([^"]*)"', m.group(3))}
        if m.group(1):
            out.append(("close", m.group(2)))
        elif m.group(4):
            out.append(("empty", m.group(2), attrs))
        else:
            out.append(("open", m.group(2), attrs))
        pos = m.end()
    if pos < len(s):
        out.append(("text", html.unescape(s[pos:])))
    return out


def untokens(toks):
    """The inverse of tokens()."""
    out = []
    for t in toks:
        if t[0] == "text":
            out.append(html.escape(t[1], quote=False))
        elif t[0] == "close":
            out.append(f"</{t[1]}>")
        else:
            a = "".join(f' {k}="{attr(v)}"' for k, v in t[2].items())
            out.append(f"<{t[1]}{a}{'/' if t[0] == 'empty' else ''}>")
    return "".join(out)


def italic_share(s):
    """(letters in italic, letters in all, words) of an inline string; note marks are not counted."""
    it = tot = depth = skip = 0
    words = 0
    for t in tokens(s):
        if t[0] == "open":
            depth += t[1] == "i"
            skip += t[1] in ("noteref", "side")
        elif t[0] == "close":
            depth -= t[1] == "i"
            skip -= t[1] in ("noteref", "side")
        elif t[0] == "text" and not skip:
            n = sum(c.isalpha() for c in t[1])
            tot += n
            it += n if depth else 0
            words += len(re.findall(r"[^\W\d_]+", t[1]))
    return it, tot, words


def swap_italics(s):
    """Italic text becomes roman, and roman words inside it italic (they were set off by contrast in print)."""
    out, depth, skip = [], 0, 0
    for t in tokens(s):
        if t[0] in ("open", "close") and t[1] == "i":
            depth += 1 if t[0] == "open" else -1
            continue
        if t[0] == "open" and t[1] == "noteref":
            skip += 1
        elif t[0] == "close" and t[1] == "noteref":
            skip -= 1
        if t[0] == "text" and not depth and not skip and any(c.isalpha() for c in t[1]):
            lead = t[1][:len(t[1]) - len(t[1].lstrip())]
            trail = t[1][len(t[1].rstrip()):]
            core = t[1].strip()
            m = re.fullmatch(r"(\W*)(.*?)(\W*)", core, flags=re.S)
            out += [("text", lead + m.group(1)), ("open", "i", {}), ("text", m.group(2)), ("close", "i"), ("text", m.group(3) + trail)]
        else:
            out.append(t)
    return untokens([t for t in out if not (t[0] == "text" and t[1] == "")])


def drop_sides(s):
    """An inline string without its side-notes (the reading editions leave them out: Tom, 2026-11-19)."""
    if "<side>" not in s:
        return s
    out = re.sub(r"<side>.*?</side>", "", s, flags=re.S)
    return out.rstrip() if s.rstrip().endswith("</side>") else out


def sides(s):
    """The plain text of each side-note in an inline string."""
    return [plain(m.group(1)) for m in re.finditer(r"<side>(.*?)</side>", s, flags=re.S)]


def plain(s, corrected=True):
    """The words of an inline string, markup removed; side-notes left out (sides() gives them).
    corrected=False gives the printed readings."""
    out, skip = [], 0
    for t in tokens(s):
        if t[0] == "text":
            if not skip:
                out.append(t[1])
        elif t[0] == "open" and t[1] == "corr":
            if not corrected:
                out.append(t[2].get("orig", "")); skip += 1
        elif t[0] == "close" and t[1] == "corr":
            skip = max(0, skip - 1)
        elif t[0] == "open" and t[1] in ("noteref", "side"):
            skip += 1
        elif t[0] == "close" and t[1] in ("noteref", "side"):
            skip = max(0, skip - 1)
    return "".join(out)
