# Sunny Lands and Seas — Hugh Wilkinson (1883)

IA: cu31924023562204 (Cornell University Library; 378 leaves, Kirtas greyscale). Other scans looked at: none.
Eligibility: queue row (Opus subagent, 2026-11-23); re-checked 2026-11-26: pg_catalog.csv (full) none; a web search found
only page images (Tamil Digital Library) and booksellers' listings. JATSI 65. Started 2026-11-26.

## Status
Stage reached: draft, corrections, judge, pages/ done; p0025 replaced by p0025a (Google copy); pictures moved out of
mid-paragraph; crops and spot-read by an Opus subagent running.
Next step: apply the spot-read; preflight; audit (also --pages p0163,p0164,p0165); rendered look; publish.

## Page map
p0000 front cover (“ASIA” label) · p0001 Wason Collection bookplate · p0002 barcode · p0003 notice card · p0004–p0006 blank ·
p0007 route map (frontispiece, no caption) · p0008 title page (pencilled date and initials, later) · p0009 verso · p0010
dedication to Albert Wood · p0011 blank · p0012–p0015 Preface v–viii · p0016–p0022 Contents ix–xv (summaries) · p0023 blank ·
p0024 = printed 1 (offset 23; +2 after each of 11 full-page plates with blank versos: p0038, p0092, p0168, p0188, p0198, p0202,
p0214, p0224, p0228, p0244, p0290; offset 45 from p0292) · p0369 = 324 “The End” · p0370 Table of Distances · p0371–p0376
blank · p0377 back cover. No index, no list of illustrations, no ads. Folio of p. 311 (p0356) misprinted “31”.
Chapters (leaf/page): I 24/1 · II 34/11 · III 42/17 · IV 55/30 · V 68/43 · VI 86/61 · VII 104/77 · VIII 121/94 · IX 144/117 ·
X 157/130 · XI 172/143 · XII 194/163 · XIII 220/183 · XIV 243/202 · XV 262/219 · XVI 273/230 · XVII 282/239 · XVIII 300/255 ·
XIX 313/268 · XX 332/287 · XXI 352/307 · Conclusion 365/320. Japan: Chapters XII–XV (pp. 163–229).
Pictures (40 and the map): plates above; in the text p0047, p0058, p0062, p0063, p0078, p0085, p0088, p0102, p0135, p0138,
p0140, p0152, p0155, p0174, p0182, p0184, p0193, p0218, p0232, p0234, p0239, p0241, p0252, p0274, p0279 (map of the Sandwich
Islands), p0298, p0344 (a notice drawn as a picture), p0356, p0358.
Scan check (Opus subagent, 2026-11-26): all 10 sheets, the foot of every leaf, full-size views: GOOD. No Japanese or Chinese
script. For the draft: letters with datelines set right; footnotes (*); short verse and epigraphs; a Chinese menu in two
columns (p0191); a hotel bill of fare (p0336); the Table of Distances (p0370).

## Decisions
- p0025 (printed 2): the right edge of every line lost in the binding (missed by the scan check; the draft's 〓 showed it).
  Replaced by the Oxford/Google copy's leaf (IA sunnylandsandse00wilkgoog n26) as p0025a, drafted by Opus and checked by
  Sonnet (no differences); `source.extra_leaves`; Drive part pages-033.
- p0163–p0165 (printed 136–138) refused by the output filter in the draft; `ocr_fallback.py`, then the Sonnet pass.
- The corrections pass moved 13 in-text pictures to the exact line, mid-sentence, with `[[cont]]` (applied unjudged): pages
  restored from the draft (same words). Six pictures the draft had left mid-paragraph (p0047, p0078, p0218, p0252, p0298,
  p0358) moved after the end of their paragraph by script (p0252: the picture heads the page; the text first).
- Judge spots checked on crops: p0179 “ago.” (a full stop, against the judge); p0284 “illæ lachrymæ” (italic ligature, the
  Latin form); p0345 closing quote (judge right). Plate leaves' folios set `?` (the draft read signature numbers).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-26 | opus | 364 | see log.jsonl | 3 refused (p0163–p0165) |
| fallback | 2026-11-26 | tesseract + opus | 3 | 0.21 | |
| corrections | 2026-11-26 | sonnet | 367 | 12.25 | 46 spots; 13 [[cont]] added (pictures moved) |
| judge | 2026-11-26 | opus | 46 spots | 1.14 | 15 draft, 31 verified |
| p0025a | 2026-11-26 | opus + sonnet | 1 | 0.10 | no differences |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
