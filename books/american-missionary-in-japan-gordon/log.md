# An American Missionary in Japan — M. L. Gordon (1893)

IA: americanmissiona00gord_0 (Princeton Theological Seminary Library; 312 leaves, 500 ppi). Other scans looked at: none yet.
Eligibility: queue row (JATSI 97; Opus subagent, 2026-11-23: rules 1–3 met, rule 4 partly: a missionary's reminiscences).
Re-checked 2026-11-26 (this session): Gutenberg catalogue and a web search, nothing new. Started 2026-11-26.

## Status
Published v1 2026-11-26.

## Page map
Scan check (Opus subagent, 2026-11-26): good; every printed page 1–276 present; outer edges complete. Leaf = page + 28
(arabic), page + 6 (roman). p0000 colour card (hidden) · p0001 cover (title readable; plum blossom) · p0002 bookplate ·
p0003–p0006 endpaper, flyleaves · p0007 title page (Riverside Press device) · p0008 imprint (Copyright 1892) · p0009
dedication · p0010 blank · p0011–p0014 Preface v–viii · p0015–p0020 Introductory Note by Wm. Elliot Griffis ix–xiv ·
p0021–p0028 Contents xv–xxii (22 chapters with summaries) · p0029 = p. 1 (book title above Chapter I) · chapters (leaf/page):
I 29/1 · II 42/14 · III 55/27 · IV 68/40 · V 81/53 · VI 93/65 · VII 105/77 · VIII 114/86 · IX 128/100 · X 145/117 · XI 164/136 ·
XII 177/149 · XIII 184/156 · XIV 193/165 · XV 201/173 · XVI 214/186 · XVII 227/199 · XVIII 237/209 · XIX 249/221 · XX 256/228 ·
XXI 268/240 · XXII 280/252 · p0286 blank · p0287–p0299 Appendix A–E (D a table sideways over p0296–p0297) · p0300 blank ·
p0301–p0304 Index · p0305 blank · p0306–p0310 slip, endpaper, boards, back cover · p0311 colour card (hidden).
No illustrations. Footnotes (e.g. p0031, p0052, p0090, p0106, p0180, p0219); romanized Japanese verse with translations
(p0281–p0285); a letter in small type (p0137–p0138); a price table (p0119).

## Decisions
- Divisions: title page (with the dedication), preface, Griffis's introductory note, contents (JSON only), the book's title
  above Chapter I (front), 22 chapters (title as `[[subtitle]]`), the appendix A–E as one division, the index (JSON only).
- Contents: chapter numbers and titles (the printed contents' summaries stay in the JSON); the appendix one entry.
- Title page typed line by line (the title is in two lines). The Riverside Press device on the title page cropped (p0007-1).
- Corrections pass: 4 markup changes, no spot to judge (so no judge run). [[cont]] at p0278 added by the verifier was wrong
  (a new paragraph of a quoted letter, opening “): the draft's page kept; p0304 removal right (a new index entry). p0156: verse
  at the page top had a stray `[[cont]]` (compile warning), removed.
- Spot-read (Opus subagent; front matter, footnote pages, verse, tables, letter, appendix, preflight lists, `tess_compare.py`'s
  103 word items — all tesseract's errors): printed misprints marked p0162 “begining”, p0255 “wiil”, p0219 “Theology.,”, p0294
  “Raymoud’s” (a turned n, marked by the session); p0296 “yen” lower case; table dashes. Accents all as printed (Kyōtō p0289,
  Kobe p0290, Kato/Katō, Osaka/Ōsaka, Heishiro/Héishiro). keep_hyphens p0172 (Fifty-five).
- `tess_compare.py` line pitch: 23 pages listed, all contents, appendix and index (small type by design): run it over the
  chapters only (`--leaves`).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-26 | opus | 298 | 19.15 | no refusals, no 〓 |
| corrections | 2026-11-26 | sonnet | 298 | 9.54 | 4 markup changes, 0 spots |
| audit | 2026-11-26 | opus | 6 | 0.33 | 30/30, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-26 | PASS tools@f712fbbc | 30/30, 0 real | first publication |

## Known issues
- Appendix D (pp. 268–269) is two tables in the editions, one per printed page; the header row is set as an ordinary row.
- p0039: the words after a verse quotation continue the sentence in print but start a new paragraph (the markup cannot continue a paragraph after verse).
