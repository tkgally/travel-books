# ‘The Frosty Caucasus’ — F. C. Grove (1875)

IA: thefrostycaucasu00grov (Library of Congress; 382 leaves, 600 ppi). Other scans looked at: none.
Eligibility: queue row (Opus subagent, 2026-11-25): no text at Gutenberg, the Online Books Page, Wikisource or Faded
Page; print-on-demand reprints only (Outlook Verlag 2024). Grove 1838–1902; engravings by Edward Whymper (d. 1911)
from photographs by Horace Walker (d. 1908); the map lithographed by Edward Weller (1819–1884). Started 2026-11-26.

## Status
Published v1 2026-11-26.

## Status (before publication)
Stage reached: scan fetched, checked and mapped (Opus subagent), cached in Drive (35 parts); full-size leaves of the
plates, title vignette, map and cover extracted in the session's scratchpad; Opus draft of leaves 5–101, 104–376
running.
Next step: crops (frontispiece p0008, vignette p0009, plates p0092, p0173, p0209, p0251, p0325, map p0373, cover
p0001); then `workflow.md` §2 on (normalize, Sonnet corrections, review, judge).

## Page map
p0000, p0381 colour cards (hidden) · p0001 front cover · p0002 bookplate · p0003–p0004 endpapers · p0005 half-title ·
p0006 printer's imprint · p0007 blank · p0008 frontispiece “Elbruz from the South-East.” · p0009 title page (vignette
“House at Bezingi.”; pencil “lorence Craufurd” and LC stamps are later additions) · p0010 verso · p0011–p0015
Contents v–ix · p0016 List of Illustrations · p0017–p0369 text pp. 1–341 (imprint at the foot of p. 341).
Offset leaf − page: +16 to leaf 90; +18 from 93; +20 from 104; +22 from 175; +24 from 211; +26 from 253; +28 from 327.
p0102–p0103 hidden by IA: a second shot of pp. 84–85 (the good shots are p0104–p0105); nothing lost.
p. 239 (p0265) has its folio misprinted “229”.
Chapters (leaf, page): I 17/1, II 61/45, III 101/83, IV 138/118, V 162/142, VI 184/162, VII 204/182, VIII 232/208,
IX 267/241, X 294/268, XI 312/286, XII 337/309; each with a summary in small type, repeated in the contents.
Plates (sideways, captions in capitals): p0008 frontispiece; p0092 “The Men of Gebi.” (blank p0091); p0173 “The Gorge
of the Djilki-Su.”; p0209 “The Valley of the Baksan.”; p0251 “Tungsorun from the Slopes of Elbruz.”; p0325 “Distant
View of Elbruz.” (blank versos). p0370–p0372 blank; p0373 folding map “The Western Caucasus” (opened, whole);
p0374 blank; p0375–p0376 Longmans advertisement; p0377–p0380 endpapers and back cover.
For the draft: 6 footnotes (pp. 35, 36, 37, 74, 243, 263; Latin and French in p. 35); verse pp. 84, 225; Maundevile
in Middle English pp. 323–324; dialogue set like a play pp. 40–43, 79, 109–110, 157, 174–175, 263–266, 305–306; a
numbered list of stages pp. 29–30; Klütch, Pätigorsk, châlets.

## Decisions
- Divisions: half-title and imprint (front), title page (frontispiece moved to it), contents, list of illustrations,
  the title above Chapter I as its own non-reading division (as in Eyre), 12 chapters with title and summary as
  `[[subtitle]]`s (Chapter I's contents entry by `toc_title`, its italic “Introductory.” standing first), the map as
  a reading division at the end, the advertisement. The imprint at the foot of p. 341 stays in the last chapter.
- Printer's errors marked: p0056 expedidition, p0199 uncertaiu, p0207 chiet, p0222 bonour (found by the audit: the
  transcription had silently corrected it), p0257 Tc, p0375 nigh-road. Left as printed: p0166 “acknowlege”
  (mid-line), Middle English in Maundevile; p. 239's folio printed “229” (kept in `[[page]]`).
- `keep_hyphens` p0051 south-eastern, p0098 well-marked. [[cont]] restored on p0142 (removed by the verifier).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-26 | opus | 370 | 24.33 | no refusals, no 〓 |
| corrections | 2026-11-26 | sonnet | 370 | 12.21 | 3 spots; 2 [[cont]] removed (one wrong) |
| judge | 2026-11-26 | opus | 3 spots | 0.12 | 2 draft, 1 verified |
| audit | 2026-11-26 | opus | 6 | 0.34 | 30/30; 1 candidate real (bonour, printed; marked) |
| spot-read (front matter, notes, verse, Maundevile; tesseract on all text leaves) | 2026-11-26 | Opus subagent | – | – | 5 text fixes, title-page and imprint lines |
| rendered look | 2026-11-26 | Opus subagent | – | – | Chapter I's contents title; imprint wording |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-26 | PASS, 0 to fix, 0 waived (tools@c793daa3) | 30/30; 1 real error in 6 pages, fixed | first publication |

## Known issues
- The printed contents (JSON only) are typed in two styles: titles of chapters VI–X in small capitals, the others in upper
  and lower case; “Page” before the number only for chapters V–VII.
- Footnote marks are numbered per page as printed, so a chapter with notes on several pages shows several notes “1”.
