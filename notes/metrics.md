# Metrics

## Published versions

| Book and version | Date | Leaves | Pipeline | Spots judged | Judge sided with draft / verifier / neither | Scan checks that overturned the judge | Cost $ (Claude, API-equivalent) | OpenRouter $ | Preflight | Audit (recall; real errors / pages) | Errors reported after publication |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Diary of the Rajah of Kolhapoor v1 | 2026-11-19 | 183 | Opus draft → Sonnet corrections → Opus judge | 10 | 7 / 2 / 0 (1 structural) | 1 (p0170 name: judge "sure: high" was wrong) | 19.36 | 0 | PASS, 1 waived | 30/30; 0 / 6 | |
| Diary of the Rajah of Kolhapoor v2 | 2026-11-19 | 183 | (no new model calls) | – | – | – | 0 | 0 | PASS, 1 waived | as v1 | frontispiece missing from the reading editions (found by me on the live page) |
| Diary of the Rajah of Kolhapoor v3 | 2026-11-19 | 183 | (no new model calls) | – | – | – | 0 | 0 | PASS, 0 waived | as v1 | |
| Sketches Awheel in Modern Iberia v1 | 2026-11-19 | 338 | Opus draft → Sonnet corrections → Opus judge | 46 | 43 / 3 / 0 | 0 | 27.68 | 0 | PASS, 0 waived | 30/30; 0 / 6 | |
| Flying Leaves from East and West v1 | 2026-11-19 | 324 | Opus draft → Sonnet corrections → Opus judge; 5 pages by the OCR fallback (tesseract + Opus) | 13 | 13 / 0 / 0 | 0 | 30.01 | 0 | PASS, 0 waived | 30/30 + 25/25 on the fallback pages; 0 / 11 | |
| Diary of the Rajah of Kolhapoor v4 | 2026-11-19 | 183 | (no new model calls) | – | – | – | 0 | 0 | PASS, 1 waived | as v1 | contents: one entry for the diary (Tom); entries added |
| Sketches Awheel in Modern Iberia v2 | 2026-11-19 | 338 | (no new model calls) | – | – | – | 0 | 0 | PASS, 0 waived | as v1 | contents: entries unlike one another (Tom); full summaries |
| Flying Leaves from East and West v2 | 2026-11-19 | 324 | (no new model calls) | – | – | – | 0 | 0 | PASS, 0 waived | as v1 | contents: parts did not nest; Leaves by number only (Tom) |
| South by West v1 | 2026-11-19 | 454 | Opus draft → Sonnet corrections → Opus judge; 3 pages by the OCR fallback (tesseract + Opus) | 63 | 24 / 39 / 0 | 0 | 44.35 | 0 | PASS, 2 waived | 30/30 + 15/15 on the fallback pages; 0 / 9 | |
| Corona and Coronet v1 | 2026-11-19 | 490 drafted of 505 | Opus draft → Sonnet corrections → Opus judge | 14 | 12 / 2 / 0 | 0 (3 printer's errors confirmed on crops) | 44.95 | 0 | PASS, 2 waived | 30/30; 0 / 6 | |
| Corona and Coronet v2 | 2026-11-20 | 490 drafted of 505 | (no new model calls) | – | – | – | 0 | 0 | PASS, 2 waived | as v1 | one plate left out of v1 (an illustrator's unknown death date) added at Tom's word |
| Embassy to China v1 | 2026-11-20 | 1,322 page files (3 IA items + 3 Getty leaves) | Opus draft → Sonnet corrections → Opus judge | 70 | 26 / 44 / 0 | 1 (p1259 "stalks,": judge's ";" wrong) | 140.14 | 0 | PASS, 0 waived | 30/30; 0 / 6 | |
| Rambles through Japan without a Guide v1 | 2026-11-20 | 301 drafted (2 from a second scan) | Opus draft → Sonnet corrections → Opus judge | 25 | 15 / 8 / 0 (2 a moved paragraph judged both ways: lost by judge.py, restored, tool fixed) | 0 | 30.31 | 0 | PASS, 1 waived | 30/30 + 5/5 on the second-scan leaf; 0 / 7 | |

## Calibrations

| Date | Scan | What | Result |
|---|---|---|---|
| 2026-11-19 | triptomanitoba00fitz, 6 pages (1880, clean) | Opus draft → Sonnet corrections | 0 corrections proposed |
| 2026-11-19 | same | audit with 30 planted errors, Opus reader | 30/30 found; 0 other differences |
| 2026-11-19 | same | audit with 30 planted errors, Sonnet reader | 27/30 (missed 2 dropped words, 1 punctuation); 1 other difference (a spacing convention, not an error) |
| 2026-11-19 | same | cost per page | draft 0.070, corrections 0.035, audit 0.058 (Opus) / 0.028 (Sonnet) |

## Preflight checks: false alarms and promotions

| Date | Check | What happened |
|---|---|---|
| 2026-11-19 | all | first version; observe: hyphen-joins, joins, folios, quote-balance, contents, images, source |
| 2026-11-19 | conservation (JSON→ODT) | false alarm on a second mark for one note (ODT `text:note-ref` read as text); fixed in the check, with test; Rajah waiver dropped (v3) |
| 2026-11-19 | conservation (pages→JSON) | false alarm on images the compiler moves (plate inside a paragraph running over the page; captioned frontispiece) held *Sketches Awheel*; captions now compared apart from the text, and a long text's differences are listed when they lie close together (before: only the first, so no waiver could be narrow); tests `MovedImages`. Rajah v3 verdict unchanged. |
| 2026-11-19 | leaves (new, observe) | added after *Flying Leaves*: five leaves refused by the output filter had no page file and every other check (folios included, which allows gaps of up to 6) passed. First run: 5 real (Flying Leaves), 1 expected (Rajah p0009, the IA card, left out on purpose). Candidate for enforce with waivers. |
| 2026-11-19 | compile (builder) | *South by West*: `[[cont]]` after an engraving in mid-page was dropped with a warning (9 pages); the compiler now joins such a paragraph across the picture (test `ImageInParagraph`); the three published books' verdicts unchanged. Changed in the session that is working on the book: it is published by a later session. |
| 2026-11-19 | leaves → enforce | four books checked: 0 unexplained gaps (Flying Leaves' 5 refused pages now have fallback files). Leaves IA hides (`source.hidden_leaves`) no longer count, which clears South by West p0007–p0008 (tissue guard); Rajah p0009 (IA card, not hidden by IA) waived. Tests `Leaves`. No book published in this session. |
| 2026-11-19 | conservation (JSON→ODT) | the ODT gets a generated contents list after the title page (Tom: contents decided book by book, the same in HTML, EPUB and ODT); its paragraph styles `Contents_20_*` are now skipped like the title page's, ordinary text beside them still counts (test `test_odt_contents_list_is_not_text`). Changed in the session that redesigned the contents: the books whose editions it changes get their new versions from a later session. |
| 2026-11-19 | hyphen-joins (observe) | review of five books: 122 items, 6 real (compounds kept with `keep_hyphens`). Joins giving a word the book prints whole elsewhere (91) are no longer listed, only counted; a join whose hyphenated form, or whose first part with a hyphen, the book prints elsewhere is marked "keep_hyphens?". Same books: 27 items, all 6 keeps among them; verdicts unchanged. Test `HyphenJoins`. |
| 2026-11-20 | joins (observe) | *Rambles*: 10 "[[cont]] after a closed sentence", 0 real (all flush left); 1 missing [[cont]] real (p0225). With the 37 of the first review: 47 alarms of that half, 0 real. |
| 2026-11-19 | joins (observe) | review: 37 alarms in five books, 0 real (every one a page starting flush left: the paragraph goes on). Kept; if the next five books bring no real one, drop the "[[cont]] after a closed sentence" half. |
