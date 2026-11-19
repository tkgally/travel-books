# Metrics

## Published versions

| Book and version | Date | Leaves | Pipeline | Spots judged | Judge sided with draft / verifier / neither | Scan checks that overturned the judge | Cost $ (Claude, API-equivalent) | OpenRouter $ | Preflight | Audit (recall; real errors / pages) | Errors reported after publication |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Diary of the Rajah of Kolhapoor v1 | 2026-11-19 | 183 | Opus draft → Sonnet corrections → Opus judge | 10 | 7 / 2 / 0 (1 structural) | 1 (p0170 name: judge "sure: high" was wrong) | 19.36 | 0 | PASS, 1 waived | 30/30; 0 / 6 | |
| Diary of the Rajah of Kolhapoor v2 | 2026-11-19 | 183 | (no new model calls) | – | – | – | 0 | 0 | PASS, 1 waived | as v1 | frontispiece missing from the reading editions (found by me on the live page) |
| Diary of the Rajah of Kolhapoor v3 | 2026-11-19 | 183 | (no new model calls) | – | – | – | 0 | 0 | PASS, 0 waived | as v1 | |

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
