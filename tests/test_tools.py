"""Regression tests for the tools. A few seconds, no model calls, no network. Invented text only.

Run: tools/run_tests.sh        Rules (CLAUDE.md): run before trusting the tools in a session and after any
edit under tools/; every tool bug fixed gets a test here in the same commit; a test is never loosened to
get a book published.
"""
import copy, json, os, shutil, sys, tempfile, unittest, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import build_site, compile_book, corrections, drive_cache, inline, judge, normalize, preflight, render_epub, render_odt, review  # noqa: E402
import render_html as rh  # noqa: E402

SAMPLE = os.path.join(REPO, "tests", "sample")
CFG = {"id": "t", "version": 1, "date": "2026-01-01", "title": "T", "authors": [{"name": "A", "sort": "A"}]}


def comp(pages, **cfg):
    c = dict(CFG, **cfg)
    return compile_book.compile_pages(c, [(f"p{i:04d}", t) for i, t in enumerate(pages, 1)])


def texts(book):
    return [s for d in book["divisions"] for b in d["blocks"] for s in rh.strings(b)]


class Quotes(unittest.TestCase):
    def test_curly(self):
        self.assertEqual(inline.smart_quotes('"Yes," he said, \'tis so; don\'t.'), "“Yes,” he said, ’tis so; don’t.")
        self.assertEqual(inline.smart_quotes("called 'a little damp.'"), "called ‘a little damp.’")
        self.assertEqual(inline.smart_quotes("<i>Paul</i>'s"), "<i>Paul</i>’s")

    def test_markup_untouched(self):
        self.assertEqual(inline.smart_quotes('[[fnref *]] "a"'), "[[fnref *]] “a”")


class Inline(unittest.TestCase):
    def test_convert(self):
        w = []
        s = inline.convert('A & B <i>c</i> [[corr teh|the]] p. <pref>34</pref>[[fnref *]]', w.append)
        self.assertEqual(s, 'A &amp; B <i>c</i> <corr orig="teh">the</corr> p. <pageref n="34">34</pageref><noteref mark="*"/>')
        self.assertEqual(w, [])

    def test_unbalanced_stripped(self):
        w = []
        self.assertEqual(inline.convert("a <i>b", w.append), "a b")
        self.assertEqual(len(w), 1)

    def test_plain(self):
        s = 'x <corr orig="teh">the</corr> <pb n="2" leaf="p0002"/>y<noteref to="d1-n1">*</noteref>'
        self.assertEqual(inline.plain(s), "x the y")
        self.assertEqual(inline.plain(s, corrected=False), "x teh y")


class Compile(unittest.TestCase):
    def test_join_and_hyphen(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nThe road was with-", "[[page 2]]\n[[cont]]out end, and long", "[[page 3]]\n[[cont]]as well."])
        t = texts(book)
        self.assertEqual(t[1], 'The road was with<pb n="2" leaf="p0002"/>out end, and long <pb n="3" leaf="p0003"/>as well.')
        self.assertEqual(len([x for x in w if x.startswith("hyphen join")]), 1)

    def test_keep_hyphen(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nat the water-", "[[page 2]]\n[[cont]]side."], keep_hyphens=["p0002"])
        self.assertIn('water-<pb n="2" leaf="p0002"/>side.', texts(book)[1])
        self.assertEqual(w, [])

    def test_dash_join_has_no_space(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\nHe stopped—", "[[page 2]]\n[[cont]]then went on."])
        self.assertIn('stopped—<pb n="2" leaf="p0002"/>then', texts(book)[1])

    def test_cont_skips_notes_and_images(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nIt began[[fnref *]] and\n\n[[fn *]] A note.", "[[page ?]]\n[[image: a map]]",
                        "[[page 3]]\n[[cont]]went on."])
        self.assertIn("and <pb", texts(book)[1])
        self.assertTrue(texts(book)[1].endswith("went on."))
        self.assertEqual(w, [])

    def test_notes_pair_by_occurrence(self):
        book, w = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b.\n\n[[fn *]] First.", "[[page 2]]\nC[[fnref *]] d.\n\n[[fn *]] Second."])
        d = book["divisions"][0]
        self.assertEqual([n["id"] for n in d["notes"]], ["d001-n1", "d001-n2"])
        self.assertIn('to="d001-n1"', texts(book)[1])
        self.assertIn('to="d001-n2"', texts(book)[2])
        self.assertEqual(w, [])

    def test_note_problems_reported(self):
        _, w = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b.\n\n[[fn †]] Orphan."])
        self.assertEqual(len(w), 2)

    def test_note_continued(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b.\n\n[[fn *]] It runs", "[[page 2]]\nC.\n\n[[fn cont]] over."])
        self.assertEqual(inline.plain(book["divisions"][0]["notes"][0]["text"]), "It runs over.")

    def test_divisions(self):
        book, w = comp(["[[page ?]]\nTITLE", "[[page ?]]\nCONTENTS\n\nOne, 1", "[[page 1]]\n# PART I.", "[[page 2]]\n# CHAPTER I.\n\n[[subtitle]] The Start\n\nText.",
                        "[[page 3]]\n# INDEX\n\nA, 1"],
                       divisions=[{"at": "p0002", "kind": "contents"}, {"at": "p0005", "kind": "index"}])
        got = [(d["kind"], d["reading"], d["title"]) for d in book["divisions"]]
        self.assertEqual(got, [("front", False, "Front matter"), ("contents", False, "Contents"), ("part", True, "PART I"),
                               ("chapter", True, "CHAPTER I. The Start"), ("index", False, "INDEX")])
        self.assertEqual(w, [])
        self.assertEqual([d["title"] for d, kids in rh.nav_tree(book)], ["PART I"])

    def test_unused_division_override_reported(self):
        _, w = comp(["[[page 1]]\n# ONE\n\nText."], divisions=[{"at": "p0009", "kind": "index"}])
        self.assertEqual(len(w), 1)

    def test_verse_and_quote_continue(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\n<verse>\nLine one,\nLine two;\n\nLine three,\n</verse>", "[[page 2]]\n<verse>\n[[cont]]Line four.\n</verse>\n\n<blockquote>\nA letter that runs\n</blockquote>",
                        "[[page 3]]\n<blockquote>\n[[cont]]over the page.\n[[right]]J. D.\n</blockquote>"])
        b = book["divisions"][0]["blocks"]
        self.assertEqual(b[1]["stanzas"], [["Line one,", "Line two;"], ["Line three,", '<pb n="2" leaf="p0002"/>Line four.']])
        self.assertEqual(b[2]["paragraphs"], [{"text": 'A letter that runs <pb n="3" leaf="p0003"/>over the page.'}, {"text": "J. D.", "align": "right"}])

    def test_corrections_listed_with_leaf(self):
        book, _ = comp(["[[page 1]]\n# ONE\n\nA long", "[[page 2]]\n[[cont]]line with [[corr teh|the]] error."])
        self.assertEqual(book["corrections"], [{"leaf": "p0002", "division": "d001", "printed": "teh", "corrected": "the"}])

    def test_caption_and_table(self):
        book, w = comp(["[[page 1]]\n# ONE\n\n[[image: a cart]]\n[[caption]] THE CART.\n\n| a | b |\n| c | d |"], )
        b = book["divisions"][0]["blocks"]
        self.assertEqual(b[1]["caption"], "THE CART.")
        self.assertEqual(b[2]["rows"], [["a", "b"], ["c", "d"]])


class Sample(unittest.TestCase):
    """The sample book in tests/sample goes through every builder and every check."""
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.dir = os.path.join(cls.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, cls.dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_preflight_clean(self):
        verdict, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        enforce = {k: v for k, v in res.items() if preflight.CHECKS[k][0] == "enforce" and v}
        self.assertEqual(enforce, {}, report)
        self.assertEqual(verdict, "INCOMPLETE")       # a run with skipped checks can never say PASS

    def test_deterministic(self):
        book, _ = compile_book.compile_book(self.dir)
        idir = os.path.join(self.dir, "images")
        self.assertEqual(render_epub.render(book, idir), render_epub.render(copy.deepcopy(book), idir))
        self.assertEqual(render_odt.render(book, idir), render_odt.render(copy.deepcopy(book), idir))

    def test_reading_editions_leave_out_index(self):
        out = os.path.join(self.tmp, "site")
        book, _ = build_site.build_book(out, self.dir)
        bdir = os.path.join(out, "books", book["id"])
        self.assertEqual(sorted(f for f in os.listdir(bdir) if f[0].isdigit()), ["01.html", "02.html", "03.html"])
        j = json.load(open(os.path.join(bdir, book["id"] + ".json"), encoding="utf-8"))
        self.assertIn("index", [d["kind"] for d in j["divisions"]])
        z = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".epub"))
        self.assertNotIn("INDEX", "".join(z.read(n).decode() for n in z.namelist() if n.endswith(".xhtml")))
        page = open(os.path.join(bdir, "02.html"), encoding="utf-8").read()
        self.assertIn('href="02.html#pg-4"', page)                      # "see p. 4" links to where page 4 starts
        self.assertIn("archive.org/details/samplejourney00doe/page/n4/", page)   # leaf 5, one hidden leaf before it

    def planted(self, leaf, old, new):
        d = os.path.join(self.tmp, "planted", "sample-journey-doe")
        shutil.rmtree(os.path.dirname(d), ignore_errors=True)
        shutil.copytree(SAMPLE, d)
        p = os.path.join(d, "pages", leaf + ".txt")
        t = open(p, encoding="utf-8").read()
        self.assertIn(old, t)
        open(p, "w", encoding="utf-8").write(t.replace(old, new))
        _, _, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
        return res

    def test_catches_unknown_marker(self):
        self.assertTrue(self.planted("p0009", "So we paid", "[[contd]] So we paid")["markup"])

    def test_catches_spacing(self):
        self.assertTrue(self.planted("p0009", "and slept,", "and slept ;")["spacing"])

    def test_catches_capital_small_caps(self):
        self.assertTrue(self.planted("p0009", "<sc>The Landlord.</sc>", "<sc>THE LANDLORD.</sc>")["sc-caps"])

    def test_catches_orphan_note(self):
        self.assertTrue(self.planted("p0004", "[[fnref *]]", "")["compile"])

    def test_catches_illegible(self):
        self.assertTrue(self.planted("p0009", "slept", "sl〓pt")["markup"])

    def test_catches_missing_image(self):
        d = os.path.join(self.tmp, "noimg", "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        os.remove(os.path.join(d, "images", "p0007-1.jpg"))
        _, _, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
        self.assertTrue(res["compile"])

    def test_join_check_sees_wrong_cont(self):
        res = self.planted("p0004", "for an hour, while", "for an hour.")
        self.assertTrue(res["joins"])

    def test_waiver(self):
        d = os.path.join(self.tmp, "waived", "sample-journey-doe")
        shutil.copytree(SAMPLE, d)
        p = os.path.join(d, "pages", "p0009.txt")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("and slept,", "and slept ;"))
        c = json.load(open(os.path.join(d, "book.json"), encoding="utf-8"))
        c["waivers"] = [{"check": "spacing", "match": "p0009", "why": "test"}]
        json.dump(c, open(os.path.join(d, "book.json"), "w", encoding="utf-8"))
        _, report, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
        self.assertEqual(res["spacing"], [])
        self.assertIn("1 waived", report)


class Normalize(unittest.TestCase):
    def test_spacing(self):
        self.assertEqual(normalize.norm_page("[[page 3]]\n\n\n“ Well ! ” said he ; “ I do n't know .”  Then -- nothing."),
                         "[[page 3]]\n\n“Well!” said he; “I don't know.” Then—nothing.\n")

    def test_small_caps_lowered_and_tags_merged(self):
        self.assertEqual(normalize.norm_text("T<sc>HE MORNING</sc> was <i>very</i> <i>fine</i>"), "T<sc>he morning</sc> was <i>very fine</i>")
        self.assertEqual(normalize.norm_text("<sc>Cairo</sc>"), "<sc>Cairo</sc>")

    def test_letters_never_change(self):
        s = "He shewed us the waggon to-day, . . . and Mr. B——'s connexion."
        self.assertEqual(normalize.norm_text(s), s)

    def test_markers_untouched(self):
        self.assertEqual(normalize.norm_page("[[page 3]]\n[[image: a man ; a cart]]\n| a | b |"), "[[page 3]]\n[[image: a man ; a cart]]\n| a | b |\n")


class Corrections(unittest.TestCase):
    def test_apply(self):
        out, n, sk = corrections.apply("the cat sat on the mat", '{"find": "cat sat", "replace": "cat sits"}\n{"find": "the", "replace": "a"}\nNONE')
        self.assertEqual((out, n, len(sk)), ("the cat sits on the mat", 1, 1))

    def test_review_kinds(self):
        self.assertEqual(review.kind_of("shew", "show"), "words")
        self.assertEqual(review.kind_of("so, then", "so; then"), "punctuation")
        self.assertEqual(review.kind_of("a <i>b</i>", "a b"), "markup")

    def test_judge_apply(self):
        spots = [{"n": 1, "find": "we shew", "replace": "we show", "draft": "shew", "verified": "show"},
                 {"n": 2, "find": "so, then", "replace": "so; then", "draft": "so, t", "verified": "so; t"}]
        a1 = "A" if judge.labels("p0001", 1) else "B"          # the label of the draft's reading at spot 1
        v2 = "B" if judge.labels("p0001", 2) else "A"          # the label of the verifier's reading at spot 2
        text, rows = judge.apply("Here we show it; so; then on.", spots, {1: {"is": a1}, 2: {"is": v2}}, "p0001")
        self.assertEqual(text, "Here we shew it; so; then on.")
        self.assertEqual([r[0] for r in rows], ["draft", "verified"])


class Drive(unittest.TestCase):
    def test_pack_parts_are_independent_and_small(self):
        tmp = tempfile.mkdtemp()
        try:
            pages = os.path.join(tmp, "pages")
            os.makedirs(pages)
            for i in range(7):
                open(os.path.join(pages, f"p{i:04d}.jpg"), "wb").write(os.urandom(1000))
            src = os.path.join(tmp, "source.json")
            json.dump({"ia_identifier": "x"}, open(src, "w"))
            drive_cache.pack(pages, os.path.join(tmp, "parts"), src, limit=3500)
            s = json.load(open(src))
            self.assertEqual(s["ia_identifier"], "x")
            self.assertEqual(sum(len(p["files"]) for p in s["parts"]), 7)
            self.assertTrue(all(p["bytes"] <= 3500 for p in s["parts"]))
            drive_cache.setid(src, "pages-001.zip", "ID1")
            drive_cache.pack(pages, os.path.join(tmp, "parts"), src, limit=3500)      # repacking keeps the ids of unchanged parts
            self.assertEqual(json.load(open(src))["parts"][0].get("drive_id"), "ID1")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class Books(unittest.TestCase):
    """Every published book still compiles without warnings other than hyphen joins (a builder change must not break one)."""
    def test_published_books_compile(self):
        bdir = os.path.join(REPO, "books")
        for slug in sorted(os.listdir(bdir)) if os.path.isdir(bdir) else []:
            if os.path.exists(os.path.join(bdir, slug, "book.json")):
                _, w = compile_book.compile_book(os.path.join(bdir, slug))
                self.assertEqual([x for x in w if not x.startswith("hyphen join")], [], slug)


if __name__ == "__main__":
    unittest.main()
