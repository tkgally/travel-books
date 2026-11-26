#!/usr/bin/env python3
"""Compare a book's page files with tesseract's reading of the scans: two lists for the spot-read to settle on crops.

1. **Words.** The page file's words and tesseract's (hOCR) are aligned page by page (difflib). Listed:
   - `print?`  tesseract read a word found nowhere in the collection where the file has a common word one or two
     letters away: often a printed misprint that every model silently corrected (“scentific”, *Brown Men and Women*;
     “disre-pect” and “themsleves” in other books);
   - `misread?` the file has a word seen at most once in the collection where tesseract read a common word one or two
     letters away: often a model's misreading (“ou” for “on”).
   Most items are tesseract's own errors; each is looked at on a crop (`crop_spot.py`). Done by hand-written scripts in
   the spot-reads since 2026-11-22; made a tool at the review after ninety-five books.
2. **Line pitch.** The median distance between lines on each page against the book's median. A page set wholly in
   smaller type (a long quotation, a letter, a document) has a pitch about 0.8 of the body's, and the drafts type such
   pages as body text (*Round about Armenia* 3 pages, *From Japan to Jerusalem* 2, *Gentle Japs* 4). Listed: pages
   under `--pitch` (0.88) of the median that have no `<blockquote>`, and pages with a blockquote whose pitch is normal
   are not listed (part pages are for the eye).

    python3 tools/tess_compare.py --pages-dir $W/pages --images $B/pages --out $W/tess.txt [--workers 6] [--leaves p0010-p0300]

No model calls. Tesseract runs one page per worker with OMP_THREAD_LIMIT=1; hOCR is cached in `--cache` (default:
`<images>/../hocr`).
"""
import argparse, collections, difflib, glob, html, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import preflight  # noqa: E402

WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")
BBOX = re.compile(r"bbox (\d+) (\d+) (\d+) (\d+)")


def parse_hocr(text):
    """(lines, words) from an hOCR page: lines as (x0, y0, x1, y1), words as strings in reading order."""
    lines, words = [], []
    for m in re.finditer(r"<span class=['\"]ocr_(?:line|textfloat|header|caption)['\"][^>]*title=['\"]([^'\"]*)['\"]", text):
        b = BBOX.search(m.group(1))
        if b:
            lines.append(tuple(int(v) for v in b.groups()))
    for m in re.finditer(r"<span class=['\"]ocrx_word['\"][^>]*>(.*?)</span>", text, flags=re.S):
        w = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        if w:
            words.append(w)
    return lines, words


def line_pitch(lines):
    """Median distance between the tops of successive lines of one column (gaps over twice the median line height,
    such as a paragraph space or a picture, and overlapping lines of another column are left out); None if fewer
    than four lines."""
    if len(lines) < 4:
        return None
    heights = sorted(y1 - y0 for _, y0, _, y1 in lines)
    h = heights[len(heights) // 2]
    tops = sorted(y0 for _, y0, _, _ in lines)
    gaps = sorted(b - a for a, b in zip(tops, tops[1:]) if 0.6 * h <= b - a <= 2.2 * h)
    if len(gaps) < 3:
        return None
    return gaps[len(gaps) // 2]


def file_words(text):
    """The words of a page file as a reader sees them: markup out, [[corr printed|corrected]] read as printed
    (tesseract sees the print), a line-end hyphen joined."""
    t = re.sub(r"\[\[corr ([^|\]]*)\|[^\]]*\]\]", r"\1", text)
    t = re.sub(r"\[\[(?:side|image)[^\]]*\]\]", " ", t)
    t = re.sub(r"\[\[[^\]]*\]\]", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    return WORD.findall(t)


def _near(a, b, limit=2):
    if a == b or abs(len(a) - len(b)) > limit:
        return False
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    return sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in ops if op != "equal") <= limit


def word_items(leaf, fwords, twords, counts, common=20, rare=1):
    """Aligned word pairs that differ, by the two rules of the docstring."""
    fl = [w.lower() for w in fwords]
    tl = [re.sub(r"^[^\w]+|[^\w]+$", "", w).lower() for w in twords]
    out = []
    sm = difflib.SequenceMatcher(None, fl, tl, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "replace" or i2 - i1 != j2 - j1:
            continue
        for k in range(i2 - i1):
            f, t = fl[i1 + k], tl[j1 + k]
            if not t or not t.isalpha() or len(f) < 3 or not _near(f, t):
                continue
            if counts[t] == 0 and counts[f] >= common:
                out.append(f"{leaf}: print?   file “{fwords[i1 + k]}”, tesseract “{twords[j1 + k]}”")
            elif fwords[i1 + k].islower() and counts[f] <= rare and counts[t] >= common:
                out.append(f"{leaf}: misread? file “{fwords[i1 + k]}”, tesseract “{twords[j1 + k]}”")
    return out


def pitch_items(pitches, texts, ratio=0.88):
    """Pages whose line pitch is under `ratio` of the book's median and whose file has no blockquote."""
    vals = sorted(p for p in pitches.values() if p)
    if len(vals) < 5:
        return []
    med = vals[len(vals) // 2]
    out = []
    for leaf in sorted(pitches):
        p = pitches[leaf]
        if p and p < ratio * med and "<blockquote>" not in texts.get(leaf, "") and len(file_words(texts.get(leaf, ""))) > 40:
            out.append(f"{leaf}: pitch {p} against the book's {med} ({p / med:.2f}): small type typed as body text?")
    return out


def hocr(image, cache):
    path = os.path.join(cache, os.path.basename(image)[:-4] + ".hocr")
    if not os.path.exists(path):
        env = dict(os.environ, OMP_THREAD_LIMIT="1")
        r = subprocess.run(["tesseract", image, "stdout", "hocr"], capture_output=True, env=env)
        with open(path, "wb") as f:
            f.write(r.stdout)
    return open(path, encoding="utf-8", errors="replace").read()


def leaf_range(spec):
    a, _, b = spec.partition("-")
    return a, (b or a)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages-dir", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache")
    ap.add_argument("--leaves", help="a range of leaf names, e.g. p0010-p0300")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--pitch", type=float, default=0.88)
    a = ap.parse_args()
    cache = a.cache or os.path.join(os.path.dirname(os.path.abspath(a.images.rstrip("/"))), "hocr")
    os.makedirs(cache, exist_ok=True)
    texts = {}
    for f in sorted(glob.glob(os.path.join(a.pages_dir, "p*.txt"))):
        leaf = os.path.basename(f)[:-4]
        if a.leaves:
            lo, hi = leaf_range(a.leaves)
            if not lo <= leaf[:5] <= hi:
                continue
        t = open(f, encoding="utf-8").read()
        if os.path.exists(os.path.join(a.images, leaf + ".jpg")) and "[[blank]]" not in t:
            texts[leaf] = t
    with ThreadPoolExecutor(a.workers) as ex:
        hocrs = dict(zip(texts, ex.map(lambda l: hocr(os.path.join(a.images, l + ".jpg"), cache), texts)))
    counts = preflight.corpus_counts()
    counts.update(w.lower() for t in texts.values() for w in file_words(t))
    words, pitches = [], {}
    for leaf, t in texts.items():
        lines, tw = parse_hocr(hocrs[leaf])
        pitches[leaf] = line_pitch(lines)
        words += word_items(leaf, file_words(t), tw, counts)
    pitch = pitch_items(pitches, texts, a.pitch)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(f"# tess_compare: {len(texts)} pages; {len(words)} word items; {len(pitch)} pitch items\n")
        f.write("## Line pitch\n" + "".join(i + "\n" for i in pitch))
        f.write("## Words\n" + "".join(i + "\n" for i in words))
    print(f"{len(texts)} pages; {len(words)} word items; {len(pitch)} pitch items → {a.out}")


if __name__ == "__main__":
    main()
