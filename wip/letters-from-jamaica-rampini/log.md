# Letters from Jamaica — [Charles Rampini] (1873)

IA: lettersfromjamai00rampuoft (University of Toronto, Robarts; 220 images, 500 ppi). Other scans: none needed.
Eligibility: vetted 2026-11-28 (Opus subagent); re-checked 2026-11-28 (web search of the title: only the IA scan and print-on-demand listings).

## Status
Stage (a): scan checked (good), Drive cache uploading, Opus draft of leaves 5–212 running (started 2026-11-28 07:45 UTC).
Next: normalize, `grep -l 〓`, Sonnet corrections pass, review, judge.

## Page map
p0001 cover · p0002–p0004 pastedown, endpapers (not drafted) · p0005 half-title · p0006 its verso (printer, agents) · p0007 title (vignette: “Annancy Spider.”) · p0008 verso (library stamps) · p0009 dedication · p0010 blank · p0011 Preface (London, May 1873) · p0012 blank · p0013 Contents · p0014 blank ·
p0015–p0186 text pp. 11–182 (leaf − 4): I p0015, II p0023, III p0040, IV p0048, V p0054, VI p0063, VII p0071, VIII p0084, IX p0093, X p0107, XI p0115, XII p0119, XIII p0135, XIV p0147, XV p0156, XVI p0166, Appendix (Negro Proverbs) p0179–p0186 (printer's imprint) ·
p0187–p0188 blanks · p0189–p0212 publisher's list (pp. 1–24, May 1873) · p0213–p0221 endpapers, library pocket, back cover, colour charts (not drafted; IA has no image 0217).
Illustrations: the title vignette only. No list of illustrations, no index.
Scan check: all 6 sheets and 17 leaves at full size (Opus subagent, 2026-11-28): good; pencil ticks in the margins pp. 178–182.
Notes: the author's name is not on the title page (IA's record and the library card: Rampini). Footnotes ¹ ² ³ restarting each page; dialect throughout (ch. III, VII, XII Annancy stories, Appendix proverbs); ch. X letters misspelt on purpose with the author's glosses in [ ]; a court-room dialogue pp. 96–102 (italic speaker tags); tables p0073, p0088–p0089, p0092; verse in small type; a monument inscription p0050; quoted newspaper notices pp. 29–32.

## Decisions
- No front-cover title (plain cloth): `cover.jpg` is the title page (a 1990 microfilming stamp over the spider's legs stays).
- Author: the title page has no name; `authors` "[Charles Rampini]" from the library catalogues.
- Divisions: half-title with its verso (printer and agents), contents and the publishers' list (p0189–p0212) in the JSON only. Chapters take their printed titles (short); the appendix `toc_title` as in the printed contents.
- Letters of ch. X and the dialect kept as printed; `[[cont]]` on 13 lower-case run-ons after verse (the book sets every line after verse flush, so run-ons that start with a capital are left as new paragraphs).
- p0110, p0127, p0142 refused by the output filter in the draft: `ocr_fallback.py`; read in full on the scan by the spot-read (one fix) and audited (15/15).
- Printer's errors marked: the the (p0049), deoeptive (p0076), aquaintance (p0158), spendid (p0174). `keep_hyphens` p0066 (brick-built).
- p0161: note mark * in the text, 1 at the foot: linked as note 1 (`notes_on_text`).
- Assumed: period “c. 1872” (“seven years” after 1865, p0053; arrival in February, departure in spring).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| Draft | 2026-11-28 | Opus | 208 | 14.48 | 3 refused (p0110, p0127, p0142) → fallback $0.22; no 〓 |
| Corrections | 2026-11-28 | Sonnet | 208 | 7.07 | 22 changes; `[[cont]]` proposals p0110 (right: added) and p0128 (right: removed) |
| Judge | 2026-11-28 | Opus | 19 spots | 0.18 | draft 18 (printed contents in capitals), verified 1 (ads) |
| Spot-read | 2026-11-28 | Opus subagent | front matter, fallback pages, tables, verse, notices, notes, lists, tess_compare | — | 21 edits: 4 printer's errors marked, “tbe” → the (p0102, a draft error), egg-shell, 13 `[[cont]]` after verse, 2 italic story titles |
| Audit | 2026-11-28 | Opus | 6 + 3 fallback | 0.53 | 29/30 and 15/15; 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
