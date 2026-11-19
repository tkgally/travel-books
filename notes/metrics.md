# Metrics

## Published versions

| Book and version | Date | Leaves | Pipeline | Spots judged | Judge sided with draft / verifier / neither | Scan checks that overturned the judge | Cost $ (Claude, API-equivalent) | OpenRouter $ | Preflight | Audit (recall; real errors / pages) | Errors reported after publication |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Diary of the Rajah of Kolhapoor v1 | 2026-11-19 | 183 | Opus draft → Sonnet corrections → Opus judge | 10 | 7 / 2 / 0 (1 structural) | 1 (p0170 name: judge "sure: high" was wrong) | 19.36 | 0 | PASS, 1 waived | 30/30; 0 / 6 | |
| Diary of the Rajah of Kolhapoor v2 | 2026-11-19 | 183 | (no new model calls) | – | – | – | 0 | 0 | PASS, 1 waived | as v1 | frontispiece missing from the reading editions (found by me on the live page) |

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
