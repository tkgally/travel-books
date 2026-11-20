"""Regression tests for the tools. A few seconds, no model calls, no network. Invented text only.

Run: tools/run_tests.sh        Rules (CLAUDE.md): run before trusting the tools in a session and after any
edit under tools/; every tool bug fixed gets a test here in the same commit; a test is never loosened to
get a book published.
"""
import copy, json, os, re, shutil, subprocess, sys, tempfile, unittest, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import build_site, compile_book, corrections, crop_image, drive_cache, inline, judge, normalize, preflight, render_epub, render_odt, review  # noqa: E402
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

    def test_note_referenced_twice(self):
        # [[fnref * again]]: a second printed reference to the note already referenced with that mark
        book, w = comp(["[[page 1]]\n# ONE\n\nA[[fnref *]] b[[fnref * again]] c.\n\n[[fn *]] One note."])
        self.assertEqual(w, [])
        d = book["divisions"][0]
        self.assertEqual(len(d["notes"]), 1)
        t = texts(book)[1]
        self.assertEqual(t.count('to="d001-n1"'), 2)
        html = rh.Ctx(book, "web", {d["id"]: "d001.html" for d in book["divisions"]}).inline(t)
        self.assertEqual(html.count('id="r-d001-n1"'), 1)      # ids stay unique
        self.assertEqual(html.count('href="#d001-n1"'), 2)
        o = render_odt.Odt(book, None)
        o.notes = {n["id"]: n for n in d["notes"]}
        x = o.inline(t)
        self.assertEqual(x.count("<text:note "), 1)  # the note is placed once
        self.assertEqual(x.count('text:ref-name="d001-n1">*</text:note-ref>'), 1)

    def test_editor_role(self):
        b = {"authors": [{"name": "A. Writer"}, {"name": "E. Ditor", "role": "editor"}]}
        self.assertEqual(rh.authors_text(b), "A. Writer; edited by E. Ditor")
        self.assertEqual(rh.authors_text({"authors": []}), "Anonymous")

    def test_frontispiece(self):
        pages = ["[[page ?]]\n[[image: a portrait]]", "[[page ?]]\nTITLE", "[[page 1]]\n# ONE\n\nText."]
        book, w = comp(pages, frontispiece="p0001-1")
        self.assertEqual(w, [])
        one = [d for d in book["divisions"] if d["reading"]][0]
        self.assertEqual((one["blocks"][0]["type"], one["blocks"][0]["src"]), ("image", "images/p0001-1.jpg"))
        self.assertFalse(any(b["type"] == "image" for d in book["divisions"] if not d["reading"] for b in d["blocks"]))
        _, w = comp(pages, frontispiece="p0009-1")
        self.assertTrue(any("frontispiece" in x for x in w))

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


class LongItalics(unittest.TestCase):
    """Tom, 2026-11-19: italics stay in the JSON; the built versions set long italic passages in roman."""
    LONG = "<i>" + "word " * 39 + "end.</i>"

    def div(self, *pages):
        book, _ = comp(list(pages))
        return book, book["divisions"][0]

    def test_json_keeps_italics_and_reading_drops_them(self):
        book, d = self.div("[[page 1]]\n# One\n\n" + self.LONG + "\n\nHe sailed in the <i>Coronet</i> that year.")
        self.assertIn("<i>word", d["blocks"][1]["text"])
        r = rh.roman_long_italics(d)
        self.assertNotIn("<i>", r["blocks"][1]["text"])
        self.assertIn("<i>Coronet</i>", r["blocks"][2]["text"])           # short italics stay
        self.assertIn("<i>word", d["blocks"][1]["text"])                    # the JSON division is not changed
        self.assertEqual(inline.plain(r["blocks"][1]["text"]), inline.plain(d["blocks"][1]["text"]))

    def test_roman_words_inside_become_italic(self):
        s = "<i>" + "word " * 30 + "</i>Coronet<i>, " + "word " * 10 + "end.</i>[[fnref *]]"
        _, d = self.div("[[page 1]]\n# One\n\n" + s + "\n\n[[fn *]] Note.")
        t = rh.roman_long_italics(d)["blocks"][1]["text"]
        self.assertEqual(t.count("<i>"), 1)
        self.assertIn("<i>Coronet</i>,", t)
        self.assertIn("<noteref", t)

    def test_short_italic_paragraph_stays(self):
        _, d = self.div("[[page 1]]\n# One\n\n<i>A short motto in italic.</i>")
        self.assertIn("<i>", rh.roman_long_italics(d)["blocks"][1]["text"])

    def test_summary_verse_and_table(self):
        _, d = self.div("[[page 1]]\n# One\n\n[[subtitle]] <i>The Start—The River</i>\n\n<verse>\n<i>One,</i>\n<i>Two,</i>\n<i>Three,</i>\n<i>Four.</i>\n</verse>\n\n"
                        "<verse>\n<i>One,</i>\n<i>Two.</i>\n</verse>\n\n| <i>Cairo</i> | <i>Egypt</i> |\n| <i>Smyrna</i> | <i>Asia</i> |")
        b = rh.roman_long_italics(d)["blocks"]
        self.assertNotIn("<i>", b[1]["text"])
        self.assertNotIn("<i>", str(b[2]["stanzas"]))
        self.assertIn("<i>", str(b[3]["stanzas"]))                          # two lines: stays italic
        self.assertNotIn("<i>", str(b[4]["rows"]))


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

    def test_catches_heading_in_capitals(self):
        self.assertTrue(self.planted("p0007", "# Chapter II.", "# CHAPTER II.")["heading-caps"])
        self.assertTrue(self.planted("p0007", "[[caption]] The Carrier's Cart.", "[[caption]] THE CARRIER'S CART.")["heading-caps"])
        self.assertEqual(preflight.check_heading_caps([("p1", "# Chapter XIV.\n\n## II.\n\n[[subtitle]] A Day at Sea")]), [])

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


    def test_odt_note_ref_is_not_text(self):
        # a second printed mark for one note ([[fnref * again]]) is a text:note-ref in the ODT: not body text
        import io
        x = ('<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
             'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><office:body><office:text>'
             '<text:p>One<text:note text:id="n1"><text:note-citation>*</text:note-citation><text:note-body>'
             '<text:p>The note.</text:p></text:note-body></text:note> and two'
             '<text:note-ref text:note-class="footnote" text:ref-name="n1">*</text:note-ref> marks.</text:p>'
             '</office:text></office:body></office:document-content>')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("content.xml", x)
        buf.seek(0)
        main, notes = preflight.odt_streams(buf)
        self.assertEqual(main, "One and two marks.")
        self.assertEqual(notes, "The note.")

    def test_odt_contents_list_is_not_text(self):
        # the generated contents list after the title page (2026-11-19) is not book text; ordinary paragraphs
        # inserted next to it still count, so an inserted line is still caught
        import io
        x = ('<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
             'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><office:body><office:text>'
             '<text:p text:style-name="Contents_20_Heading">Contents</text:p>'
             '<text:p text:style-name="Contents_20_1"><text:a>Chapter I. The Ford</text:a></text:p>'
             '<text:p text:style-name="Contents_20_2"><text:a>3-9 May: Leeds</text:a></text:p>'
             '<text:p text:style-name="Text_20_body">An inserted line.</text:p>'
             '<text:h text:style-name="Heading_20_1">Chapter I.</text:h>'
             '</office:text></office:body></office:document-content>')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("content.xml", x)
        buf.seek(0)
        main, _ = preflight.odt_streams(buf)
        self.assertEqual(main, "An inserted line. Chapter I.")


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


class ImageInParagraph(unittest.TestCase):
    """A picture in the middle of a page that interrupts a paragraph: `[[cont]]` after it joins the paragraph again
    (the compiler dropped it and split the paragraph; South by West, 2026-11-19). Invented text."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, self.dir)
        p = os.path.join(self.dir, "pages", "p0005.txt")
        t = open(p, encoding="utf-8").read()
        old = "<pref>4</pref>, and by noon"
        self.assertIn(old, t)
        open(p, "w", encoding="utf-8").write(t.replace(old, "<pref>4</pref>, and by\n\n[[image: a mill by a river]]\n"
                                                         "[[caption]] The Mill.\n\n[[cont]]noon", 1))
        shutil.copy(os.path.join(self.dir, "images", "p0007-1.jpg"), os.path.join(self.dir, "images", "p0005-1.jpg"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_joined_and_picture_after_paragraph(self):
        book, w = compile_book.compile_book(self.dir)
        self.assertEqual([x for x in w if "[[cont]]" in x], [])
        blocks = [b for d in book["divisions"] for b in d["blocks"]]
        i = next(k for k, b in enumerate(blocks) if "and by noon we had made" in b.get("text", ""))
        self.assertIn("out a halt", blocks[i]["text"])               # and still joined over the page
        self.assertEqual(blocks[i + 1].get("caption"), "The Mill.")
        _, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        self.assertEqual(res["conservation"], [], report)

    def test_cont_mid_page_without_picture_still_warned(self):
        p = os.path.join(self.dir, "pages", "p0005.txt")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("[[image: a mill by a river]]\n[[caption]] The Mill.\n\n", "", 1))
        _, w = compile_book.compile_book(self.dir)
        self.assertTrue(any("not at the top of a page" in x for x in w), w)


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


class DrivePages(unittest.TestCase):
    """fetch --pages: a comma list was read as one name and fetched the wrong parts (2026-11-19)."""
    def test_list_and_ranges(self):
        keep = drive_cache.page_filter("p0036,p0111, p0150-p0152")
        got = [f for f in ["p0035.jpg", "p0036.jpg", "p0111.jpg", "p0150.jpg", "p0152.jpg", "p0153.jpg", "leaves.json"] if keep(f)]
        self.assertEqual(got, ["p0036.jpg", "p0111.jpg", "p0150.jpg", "p0152.jpg", "leaves.json"])
        self.assertIsNone(drive_cache.page_filter(None))

    def test_bad_item_stops(self):
        with self.assertRaises(SystemExit):
            drive_cache.page_filter("116-118")


class SetupEnv(unittest.TestCase):
    """setup_env.sh must turn the Ubuntu apt mirrors to https (plain http hangs behind the proxy); the first
    version's sed used | as delimiter with \\| inside, matched nothing, and apt hung for 20 minutes (2026-11-19)."""
    def test_apt_mirrors_become_https(self):
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, "sources.list.d"))
            f = os.path.join(tmp, "sources.list.d", "ubuntu.sources")
            open(f, "w").write("URIs: http://archive.ubuntu.com/ubuntu/\nURIs: http://security.ubuntu.com/ubuntu/\n"
                               "URIs: http://example.org/other/\n")
            subprocess.run(["bash", os.path.join(REPO, "tools", "setup_env.sh"), "--apt-https-only", tmp], check=True)
            self.assertEqual(open(f).read(), "URIs: https://archive.ubuntu.com/ubuntu/\nURIs: https://security.ubuntu.com/ubuntu/\n"
                                             "URIs: http://example.org/other/\n")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class CropImage(unittest.TestCase):
    def test_rotate_turns_sideways_plate_upright(self):
        from PIL import Image
        im = Image.new("RGB", (400, 200), "white")
        im.paste((0, 0, 0), (0, 0, 20, 200))          # dark band along the left edge of a wide picture
        out = crop_image.crop(im, (0, 0, 1, 1), rotate=90, longest=1600)
        self.assertEqual(out.size, (200, 400))
        self.assertLess(out.getpixel((100, 395)), (60, 60, 60))   # left edge turned counter-clockwise -> bottom
        self.assertGreater(out.getpixel((100, 5)), (200, 200, 200))

    def test_box_and_size(self):
        from PIL import Image
        out = crop_image.crop(Image.new("RGB", (1000, 2000), "white"), (0.1, 0.1, 0.6, 0.6), longest=500)
        self.assertEqual(out.size, (250, 500))


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


class MovedImages(unittest.TestCase):
    """The compiler moves some images; conservation must follow them (it failed a finished book, 2026-11-19)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, self.dir)
        img = os.path.join(self.dir, "images", "p0007-1.jpg")
        for leaf, old, new in (
                # a plate at the foot of a page whose paragraph runs on to the next page
                ("p0004", "for an hour, while\n", "for an hour, while\n\n[[image: a cart in a ford]]\n[[caption]] The Cart at the Ford.\n"),
                # a captioned frontispiece in the front matter
                ("p0001", "1861\n", "1861\n\n[[image: portrait of a woman]]\n[[caption]] The Author.\n")):
            p = os.path.join(self.dir, "pages", leaf + ".txt")
            t = open(p, encoding="utf-8").read()
            self.assertIn(old, t)
            open(p, "w", encoding="utf-8").write(t.replace(old, new, 1))
            shutil.copy(img, os.path.join(self.dir, "images", leaf + "-1.jpg"))
        c = json.load(open(os.path.join(self.dir, "book.json"), encoding="utf-8"))
        c["frontispiece"] = "p0001-1"
        json.dump(c, open(os.path.join(self.dir, "book.json"), "w", encoding="utf-8"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_plate_in_paragraph_and_captioned_frontispiece_pass(self):
        book, _ = compile_book.compile_book(self.dir)
        first = next(d for d in book["divisions"] if d["reading"])
        self.assertEqual(first["blocks"][0].get("caption"), "The Author.")          # moved by the compiler
        _, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        self.assertEqual(res["conservation"], [], report)
        self.assertEqual(res["compile"], [], report)

    def test_caption_lost_is_still_caught(self):
        pages = [("p0001", "[[page 1]]\nText.\n[[image: x]]\n[[caption]] A Caption.")]
        book = {"divisions": [{"reading": True, "notes": [], "blocks": [
            {"type": "paragraph", "text": "Text."}, {"type": "image", "caption": "Another Caption."}]}]}
        pc, jc = [], []
        self.assertEqual(preflight.page_streams(pages, captions=pc)[0], preflight.json_streams(book, captions=jc)[0])
        self.assertTrue(preflight.compare(" ".join(sorted(pc)), " ".join(sorted(jc)), "captions"))

    def test_caption_not_after_an_image_stays_in_the_text(self):
        pc = []
        main, _ = preflight.page_streams([("p0001", "[[page 1]]\nText.\n[[caption]] Stray.")], captions=pc)
        self.assertEqual((main.split(), pc), (["Text.", "Stray."], []))

    def test_long_texts_list_each_difference(self):
        a = "".join(f"word{i} " for i in range(12000))
        b = a.replace("word50 ", "", 1).replace("word9000 ", "wurd9000 ", 1)
        items = preflight.compare(a, b, "t")
        self.assertEqual(len(items), 1)                       # two far apart: the first, as before
        items = preflight.compare(a, a.replace("word9000 ", "", 1).replace("word9005 ", "wurd9005 ", 1), "t")
        self.assertEqual(len(items), 2, items)                # close together: each is listed, so a waiver can name one
        self.assertEqual(preflight.compare(a, a, "t"), [])


class SideNotes(unittest.TestCase):
    """Marginal notes (Staunton's Embassy, 2026-11-20): kept in the JSON, left out of the reading editions."""

    def test_convert_plain_and_drop(self):
        s = inline.convert('at [[side: Occasion of the "Embassy."]] the Embassy was')
        self.assertEqual(s, 'at <side>Occasion of the “Embassy.”</side>the Embassy was')
        self.assertEqual(inline.plain(s), "at the Embassy was")
        self.assertEqual(inline.drop_sides(s), "at the Embassy was")
        self.assertEqual(inline.sides(s), ["Occasion of the “Embassy.”"])
        end = inline.convert("He sailed. [[side: <i>Lion</i> sails.]]")
        self.assertEqual((end, inline.drop_sides(end)), ("He sailed.<side><i>Lion</i> sails.</side>", "He sailed."))

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.dir = os.path.join(self.tmp, "sample-journey-doe")
        shutil.copytree(SAMPLE, self.dir)
        p = os.path.join(self.dir, "pages", "p0004.txt")
        t = open(p, encoding="utf-8").read()
        old = "The carrier had promised nothing;"
        self.assertIn(old, t)
        t = t.replace("W<sc>e</sc> left", "[[side: Leaving the town.]] W<sc>e</sc> left", 1)
        open(p, "w", encoding="utf-8").write(t.replace(old, "The [[side: The carrier.]] carrier had promised nothing;", 1))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_json_keeps_editions_drop(self):
        book, _ = compile_book.compile_book(self.dir)
        js = [x for d in book["divisions"] for b in d["blocks"] for s in rh.strings(b) for x in inline.sides(s)]
        self.assertEqual(js, ["Leaving the town.", "The carrier."])
        _, report, res = preflight.run(self.dir, skip_epubcheck=True, skip_odt=True)
        for k in ("conservation", "markup", "stray-markup", "compile"):
            self.assertEqual(res.get(k, []), [], report)
        out = os.path.join(self.tmp, "site")
        build_site.build_book(out, self.dir)
        bdir = os.path.join(out, "books", book["id"])
        html = "".join(open(os.path.join(bdir, f), encoding="utf-8").read() for f in os.listdir(bdir) if f.endswith(".html"))
        self.assertNotIn("Leaving the town", html)
        self.assertIn("The carrier had promised nothing", html)
        odt = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".odt")).read("content.xml").decode("utf-8")
        self.assertNotIn("Leaving the town", odt)
        epub = zipfile.ZipFile(os.path.join(bdir, book["id"] + ".epub"))
        self.assertFalse(any("Leaving the town" in epub.read(n).decode("utf-8", "replace") for n in epub.namelist() if n.endswith(".xhtml")))

    def test_hyphen_join_over_a_side_note(self):
        book, w = comp(["[[page 1]]\n# One\n\nHe was accompa-", "[[page 2]]\n[[cont]][[side: Teneriffe.]] nied by two."])
        self.assertEqual(inline.plain(texts(book)[1]), "He was accompanied by two.")
        self.assertIn("accompa-|nied by two", w[0])               # the word after the join, not the side-note
        tri = preflight.triage_hyphen_joins(w, [("p0001", "x accompanied y")])
        self.assertEqual(tri, ["(and 1 joins giving a word the book prints whole elsewhere: not listed)"])

    def test_lost_side_note_is_caught(self):
        pages = [("p0001", "[[page 1]]\n[[side: A note.]] Text.")]
        ps, js = [], []
        book = {"divisions": [{"reading": True, "notes": [], "blocks": [{"type": "paragraph", "text": "Text."}]}]}
        self.assertEqual(preflight.page_streams(pages, sides=ps)[0].split(), preflight.json_streams(book, sides=js)[0].split())
        self.assertEqual(ps, ["A note."])
        self.assertTrue(preflight.compare(" ".join(ps), " ".join(js), "side-notes"))


class Volumes(unittest.TestCase):
    """A work in several IA items, and leaves bound out of order (Staunton's Embassy, 2026-11-20)."""
    SRC = {"ia_identifier": "vol1", "items": [
        {"ia_identifier": "vol1", "first_leaf": "p1000", "hidden_leaves": [0, 7]},
        {"ia_identifier": "vol2", "first_leaf": "p2000", "hidden_leaves": [0, 24, 25]}]}

    def test_scan_links_per_item(self):
        ctx = rh.Ctx({"source": self.SRC, "pages": [], "divisions": []}, "web", {})
        self.assertEqual(ctx.scan_url("p1068"), "https://archive.org/details/vol1/page/n66/mode/1up")
        self.assertEqual(ctx.scan_url("p2030"), "https://archive.org/details/vol2/page/n27/mode/1up")
        one = rh.Ctx({"source": {"ia_identifier": "x", "hidden_leaves": [0]}, "pages": [], "divisions": []}, "web", {})
        self.assertEqual(one.scan_url("p0005"), "https://archive.org/details/x/page/n4/mode/1up")

    def test_leaves_checked_per_item(self):
        items = compile_book.scan_items(self.SRC)
        pages = [(f"p{n:04d}", "") for n in list(range(1001, 1007)) + list(range(1008, 1011)) + list(range(2001, 2024)) + [2026, 2028]]
        self.assertEqual(preflight.check_leaves(pages, items=items), ["p2027: no page file"])

    def test_book_page_lists_every_item(self):
        src = copy.deepcopy(self.SRC)
        src["items"][0]["label"], src["items"][1]["label"] = "Volume I", "Volume II"
        book = {"id": "t", "title": "T", "version": 1, "date": "d", "source": src, "pages": [], "divisions": []}
        x = build_site.book_page(book, {})
        self.assertEqual(x.count("<iframe"), 2)
        self.assertIn("The scan of Volume II at the Internet Archive", x)
        self.assertIn('archive.org/embed/vol2', x)

    def test_leaf_order(self):
        pages = [(f"p{n}", n) for n in (1466, 1467, 1468, 1469, 1470, 1471)]
        out = compile_book.apply_leaf_order(pages, [["p1469", "p1470", "p1467", "p1468"]])
        self.assertEqual([x for x, _ in out], ["p1466", "p1469", "p1470", "p1467", "p1468", "p1471"])
        with self.assertRaises(ValueError):
            compile_book.apply_leaf_order(pages, [["p1469", "p9999"]])


class Fallback(unittest.TestCase):
    """Pages the output filter refuses get a machine-OCR draft that a model corrects (tools/ocr_fallback.py)."""

    def test_to_markup(self):
        import ocr_fallback
        raw = "106 A HEAD.\n\nThe first para-\ngraph runs on to twenty-\nThird Street\nhere.\n\n  \nSecond one.\n"
        self.assertEqual(ocr_fallback.to_markup(raw),
                         "[[page ?]]\n\n106 A HEAD.\n\nThe first paragraph runs on to twenty-Third Street here.\n\nSecond one.\n")

    def test_refused_pages_from_the_log(self):
        import ocr_fallback
        d = tempfile.mkdtemp()
        try:
            refusal = "RuntimeError('API Error: Output blocked by content filtering policy')"
            recs = [{"page": "p0001", "cost": 0.1}, {"page": "p0002", "error": refusal}, {"page": "p0003", "error": "timeout"},
                    {"page": "p0004", "error": refusal}, {"page": "p0004", "cost": 0.1}, {"page": "p0005", "error": refusal}]
            open(os.path.join(d, "log.jsonl"), "w").write("\n".join(json.dumps(r) for r in recs) + "\n")
            open(os.path.join(d, "p0005.txt"), "w").write("x")          # already has a draft
            self.assertEqual(ocr_fallback.refused_pages(d), ["p0002"])
        finally:
            shutil.rmtree(d)

    def test_page_lists(self):
        import ocr_claude, ocr_fallback
        self.assertEqual(ocr_claude.page_numbers("20-22"), [20, 21, 22])
        self.assertEqual(ocr_claude.page_numbers("116-118,128"), [116, 117, 118, 128])
        self.assertEqual(ocr_fallback.parse_pages("p0116-p0118,128"), [116, 117, 118, 128])


class Refusal(unittest.TestCase):
    """The output filter's refusal is never retried; corrections mode makes no call for a page with no draft."""

    def setUp(self):
        import ocr_claude, judge as jd, audit_sample  # noqa: F401
        self.mods = (ocr_claude, jd, audit_sample)
        self.tmp = tempfile.mkdtemp()
        self.calls = 0

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def fake_run(self, *a, **k):
        self.calls += 1
        class R:
            stdout = json.dumps({"is_error": True, "result": "API Error: Output blocked by content filtering policy"})
        return R()

    def patched(self, mod):
        from unittest import mock
        return mock.patch.multiple(mod, time=mock.DEFAULT), mock.patch.object(mod.subprocess, "run", self.fake_run)

    def test_is_refusal(self):
        from refusal import is_refusal
        self.assertTrue(is_refusal("RuntimeError('API Error: Output blocked by content filtering policy')"))
        self.assertFalse(is_refusal("RuntimeError('timeout')"))
        self.assertFalse(is_refusal(None))

    def test_ocr_not_retried(self):
        from types import SimpleNamespace
        ocr = self.mods[0]
        args = SimpleNamespace(out=self.tmp, context_text=None, halves=False, corrections=False, model="opus")
        a, b = self.patched(ocr)
        with a, b:
            rec = ocr.do_page(args, "prompt", os.path.join(self.tmp, "p0001.jpg"))
        self.assertEqual(self.calls, 1)
        self.assertIn("content filtering", rec["error"])

    def test_judge_and_audit_not_retried(self):
        for mod in self.mods[1:]:
            self.calls = 0
            a, b = self.patched(mod)
            with a, b:
                res, info = mod.call("prompt", "opus", self.tmp)
            self.assertIsNone(res)
            self.assertEqual(self.calls, 1, mod.__name__)

    def test_corrections_without_draft_makes_no_call(self):
        from types import SimpleNamespace
        ocr = self.mods[0]
        ctx = os.path.join(self.tmp, "draft"); os.makedirs(ctx)
        args = SimpleNamespace(out=self.tmp, context_text=ctx, halves=False, corrections=True, model="sonnet")
        a, b = self.patched(ocr)
        with a, b:
            rec = ocr.do_page(args, "prompt", os.path.join(self.tmp, "p0002.jpg"))
        self.assertEqual(self.calls, 0)
        self.assertIn("no draft", rec["error"])


class Leaves(unittest.TestCase):
    """A leaf with no page file inside the run (a refused draft) is listed; folios alone cannot see it."""

    def test_gap(self):
        pages = [("p0010", "[[page 1]]"), ("p0011", "[[page 2]]"), ("p0014", "[[page 5]]")]
        self.assertEqual(preflight.check_leaves(pages), ["p0012: no page file", "p0013: no page file"])
        self.assertEqual(preflight.check_folios(pages), [])

    def test_none(self):
        self.assertEqual(preflight.check_leaves([("p0001", ""), ("p0002", "")]), [])
        self.assertEqual(preflight.check_leaves([]), [])

    def test_hidden_not_missing(self):
        pages = [("p0006", ""), ("p0009", ""), ("p0011", "")]
        self.assertEqual(preflight.check_leaves(pages, [0, 7, 8, 450]), ["p0010: no page file"])

    def test_enforced(self):
        self.assertEqual(preflight.CHECKS["leaves"][0], "enforce")


class Contents(unittest.TestCase):
    """Contents decided book by book (Tom, 2026-11-19): full summaries, entries inside a division, parts."""
    LONG = "The Start—" + "A Very Long Morning on the Road—" * 3 + "The Inn"

    def test_subtitles_all(self):
        pages = [f"# Chapter I.\n\n[[subtitle]] {self.LONG}\n\nText one.", "# Chapter II.\n\n[[subtitle]] The River\n\nText two."]
        book, w = comp(pages)
        self.assertEqual([d["title"] for d in book["divisions"]], ["Chapter I", "Chapter II. The River"])
        self.assertNotIn("toc_title", book["divisions"][0])
        book, w = comp(pages, toc={"subtitles": "all"})
        d1, d2 = book["divisions"]
        self.assertEqual(d1["title"], "Chapter I")                     # pager and page title stay short
        self.assertEqual(d1["toc_title"], "Chapter I. " + self.LONG)
        self.assertNotIn("toc_title", d2)                              # already whole
        self.assertEqual([n[0] for n in rh.toc_tree(book)], ["Chapter I. " + self.LONG, "Chapter II. The River"])

    def test_toc_title_in_divisions(self):
        book, _ = comp(["# Diary.\n\nText."], divisions=[{"at": "p0001", "kind": "chapter", "toc_title": "The Diary"}])
        self.assertEqual(book["divisions"][0]["title"], "Diary")
        self.assertEqual(rh.toc_tree(book)[0][0], "The Diary")

    def test_part_with_subtitle(self):
        book, _ = comp(["# Flying Leaves.\n\n[[subtitle]] From the East.", "# Leaf I.\n\nText.", "# Leaf II.\n\nMore."])
        self.assertEqual([d["kind"] for d in book["divisions"]], ["part", "chapter", "chapter"])
        tree = rh.toc_tree(book)
        self.assertEqual(len(tree), 1)
        self.assertEqual([k[0] for k in tree[0][3]], ["Leaf I", "Leaf II"])

    def test_entries(self):
        pages = ["# Diary.\n\n<i>Sunday</i>, June 12<i>th</i>.—Paris.\n\n13<i>th</i>.—Calais.",
                 "[[page 2]]\n\n1<i>st</i> July.—London.\n\nIn the evening, the theatre."]
        entries = [{"at": "p0001", "starts": "Sunday, June 12th", "title": "12–13 June: Paris and Calais"},
                   {"at": "p0002", "starts": "1st July", "title": "July: London"},
                   {"at": "p0002", "starts": "No such day", "title": "x"}]
        book, w = comp(pages, toc_entries=entries)
        d = book["divisions"][0]
        self.assertEqual(d["sections"], [{"title": "12–13 June: Paris and Calais", "block": 1, "editor": True},
                                         {"title": "July: London", "block": 3, "editor": True}])
        self.assertEqual(w, ["toc_entries: no block on p0002 starts with 'No such day'"])
        names = rh.file_names(book, ".xhtml")
        nav = rh.nav_list(book, names)
        self.assertIn('<li><a href="01.xhtml">Diary</a><ol><li><a href="01.xhtml#sec-1">12–13 June: Paris and Calais</a></li>', nav)
        html = rh.Ctx(book, "web", names).blocks(d)
        self.assertIn('<p id="sec-1" class="first">', html)
        self.assertIn('<p id="sec-2">', html)
        # the ODT's contents list links to bookmarks that exist
        odt = render_odt.render(book, None)
        content = zipfile.ZipFile(__import__("io").BytesIO(odt)).read("content.xml").decode()
        links = re.findall(r'xlink:href="#([^"]+)"', content)
        marks = set(re.findall(r'text:bookmark text:name="([^"]+)"', content))
        self.assertEqual(links, ["div-d001", "div-d001-sec-1", "div-d001-sec-2"])
        self.assertTrue(set(links) <= marks, (links, marks))

    def test_sample_with_entries_preflight_clean(self):
        tmp = tempfile.mkdtemp()
        try:
            d = os.path.join(tmp, "sample-journey-doe")
            shutil.copytree(SAMPLE, d)
            cfg = json.load(open(os.path.join(d, "book.json")))
            cfg["toc"] = {"subtitles": "all"}
            cfg["toc_entries"] = [{"at": "p0006", "starts": "The road is long", "title": "The carrier's song"}]
            json.dump(cfg, open(os.path.join(d, "book.json"), "w"))
            verdict, report, res = preflight.run(d, skip_epubcheck=True, skip_odt=True)
            enforce = {k: v for k, v in res.items() if preflight.CHECKS[k][0] == "enforce" and v}
            self.assertEqual(enforce, {}, report)
            book, _ = compile_book.compile_book(d)
            self.assertEqual(sum(len(x.get("sections", [])) for x in book["divisions"]), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class HyphenJoins(unittest.TestCase):
    """Review 2026-11-19: the look list drops joins the book itself settles (the whole word printed elsewhere)
    and marks those whose hyphenated form it prints elsewhere."""

    def warn(self, leaf, a, b):
        return f"hyphen join at {leaf}: …{a}|{b}… (hyphen removed; check)"

    def test_triage(self):
        pages = [("p0001", "In the afternoon we took the stepping-stones and a snow-plough."),
                 ("p0002", "We walked in the after-"), ("p0003", "[[cont]]noon; then the stepping-"),
                 ("p0004", "[[cont]]stones, the snow-"), ("p0005", "[[cont]]fences and a rare dis-"),
                 ("p0006", "[[cont]]cussion of <i>ship-</i>"), ("p0007", "[[cont]]<i>wreck</i>.")]
        items = [self.warn("p0003", "lked in the after-", "noon; then the "),
                 self.warn("p0004", " then the stepping-", "stones, the sno"),
                 self.warn("p0005", "ones, the snow-", "fences and a ra"),
                 self.warn("p0006", " and a rare dis-", "cussion of <i>s"),
                 self.warn("p0007", "of <i>ship-</i>", "<i>wreck</i>.")]
        out = preflight.triage_hyphen_joins(items, pages)
        self.assertEqual(len(out), 5)
        self.assertIn("“stepping-stones” elsewhere", out[0])
        self.assertIn("other “snow-” words", out[1])
        self.assertEqual(out[2:4], items[3:5])                  # not settled by the book (italics too): as before
        self.assertEqual(out[4], "(and 1 joins giving a word the book prints whole elsewhere: not listed)")

    def test_unparsed_item_listed(self):
        it = "hyphen join around an image at p0009: …is responsi-|[[image: x]]… (hyphen removed; check)"
        self.assertEqual(preflight.triage_hyphen_joins([it], []), [it])


class ShortSubtitle(unittest.TestCase):
    """Review 2026-11-19: a short chapter title under the heading is centred (it looked like a stray indented
    paragraph); a long list of topics stays a left-aligned summary. HTML/EPUB class and ODT style."""

    def test_classes_and_styles(self):
        long_ = "Topic—" * 20 + "End."
        book, _ = comp(["# Chapter VIII\n\n[[subtitle]] A Hawaiian Journey\n\n[[subtitle]] " + long_ + "\n\nText."])
        d = book["divisions"][0]
        html = "".join(rh.Ctx(book, "web", {x["id"]: "d.html" for x in book["divisions"]}).blocks(d))
        self.assertIn('<p class="subtitle short">A Hawaiian Journey</p>', html)
        self.assertIn('<p class="subtitle">Topic', html)
        odt = zipfile.ZipFile(__import__("io").BytesIO(render_odt.render(book, None))).read("content.xml").decode()
        self.assertIn('text:style-name="Chapter_20_Title">A Hawaiian Journey', odt)
        self.assertIn('text:style-name="Chapter_20_Summary">Topic', odt)
