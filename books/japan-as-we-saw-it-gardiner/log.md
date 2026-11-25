# Japan As We Saw It — Robert S. Gardiner (1892)

IA: japanaswesawit00gardrich (University of California Libraries; 152 leaves, 500 ppi). Other scans: Library of
Congress copy japanaswesawit00gard (not looked at; may have the maps).
Eligibility: queue row (JATSI 91; checked 2026-11-23). Started 2026-11-25.

## Status
Published v1 2026-11-26.

## Status (before publication)
Stage reached: scan fetched, checked and mapped, cached in Drive (page images, and the full-size leaves of every
picture page, the cover and the title page: `source.json` `full_parts`, `full-NNN.zip`, fetched by id with curl);
Opus draft of every leaf (`draft/`, normalized). No `book.json` yet.
Next step: an ordinary book from `workflow.md` §3 on: `drive_cache.py fetch`, the Sonnet corrections pass on
`draft/`, review, judge, `pages/`; then the items under "Settled on the scan" below, structure, the 83 pictures
(all to be cut by us), preflight, audit.
Half-finished: nothing.

## Page map
(Opus subagent, 2026-11-25: all sheets, page numbers followed from 3 to 135.) Leaf = printed page + 6 throughout.
p0001 front cover (title readable in a disc at the top right; library labels at the top left: cover.jpg = the
right two-thirds) · p0002 bookplate · p0003 blank · p0004 IA leaf · p0005 title · p0006 verso (stamps only) ·
p0007 dedication · p0009–p0012 Preface 3–6 · p0013 Contents · p0015–p0016 Illustrations (83 entries) · p0017 = p. 11:
“Japan As We Saw It.” above “The Journey Westward” · p0019 full-page plate, sideways · chapters at p0017, p0023,
p0036, p0040, p0045, p0047, p0050, p0057, p0065, p0069, p0073, p0082, p0085, p0088, p0091, p0098, p0103, p0110 ·
p0119 text ends · p0121 Appendix · p0122–p0138 vocabulary · p0139–p0141 Index · p0142–p0148 endpapers, library slip
and pocket, back cover · p0150–p0153 targets and blanks. The scan has no leaf 0149 (the file numbering skips it;
nothing printed is lost): waive `leaves` for it if preflight asks.
**The map of Japan and four city plans “inside the back cover” are not in this copy** (a library pocket is pasted
there): publish without them, said in `notes_on_text` (Tom, 2026-11-22), unless the Library of Congress scan has them.
Pictures: 83, on the leaves the crop table names; no ornaments or pictorial initials. Real captions set in type:
p0025 “Bank Shroff.”, p0027 (passport), p0030 “Shimid.”, p0096 “Room Girl.”; every other title is lettering drawn
inside the engraving (not transcribed; it must be whole in the crop).

## Settled on the scan (Opus subagent, 2026-11-25)
The draft was compared with a transcription Gemini had made for Tom (a trial since stopped: `notes/improvement.md`
§"Tried and set aside"; that text and its pictures are not kept here), and every difference was looked at on the
scan. To do to the draft:
- remove the `[[caption]]` lines typed from lettering inside pictures (p0032, p0033, p0037, p0042 ×2, p0052 ×2,
  p0059 ×2, p0065, p0067 ×2, p0068, p0069, p0071, p0078, p0082, p0092 ×2, p0095, p0100, p0108, p0112, p0117); keep
  the captions set in type (p0025, p0027, p0030, p0096);
- the print has: p0048 “women, are” (the draft has a full stop) · p0096 “Ah-koah-ko” · p0123 “massugu.” · p0133
  “etc),” without a stop · p0121 “1210 Tsubo is practically an acre.” as a line of its own;
- printer's errors to mark: p0010 “apan” → Japan (the J did not print), p0075 “nand” → hand, p0086 a full stop for a
  comma after “(Nee-gah-tsoo-doh)”; p0034 “closély” (a speck or damaged type over the e: look at a crop);
- confirmed as the draft has them: p0036 schoolroom, p0056 neophite, p0080 Rah-koo-rah-koo-tay, p0098 “atten-” at
  the page foot, p0127 “irashaimas ka.”, p0128 “doshte”, upright brackets round the italic pronunciations, the
  heading on p0017, the vocabulary pages as tables (p0121 two entries a line; p0136 two and three column pairs).
Pictures: 83, none besides those in the printed list; hard to cut (irregular vignettes with the text wrapped round
them; the lettering is part of the drawing and must be whole): p0045, p0052, p0099, p0100 and p0114 have text in a
concave part that no rectangle avoids. p0019 is a full-page plate printed sideways.

## Decisions
- Lettering drawn inside the engravings is not a caption: 26 `[[caption]]` lines typed from it were removed and the
  words put into the picture's description (“lettered …”); the four captions set in type kept, in upper and lower case.
- Chapter openings are printed in full capitals after a drop initial (“THE two modes”, “NAGASAKI”): typed as capitals,
  not small capitals (p0103, and p0036, p0047, p0050, p0082, p0110 typed in small capitals by the draft, corrected).
- The book's title above the first chapter (p0017) is a `[[center]]` line in small capitals, left in the division
  before (the list of illustrations, not in the reading editions), as in *Here and There among the Alps*.
- Divisions: cover (front), title page, dedication, preface, contents, illustrations, 18 chapters, Appendix, “English
  and Japanese”, “Words and Phrases” (glossary; letter heads `##`, not in the contents), index, back cover (p0148).
- Printer's errors marked: p0010 apan, p0034 closély, p0075 nand, p0086 a stop for a comma, p0130 iuku (niku),
  p0134 “Tumble-,”, p0136 Jin (Jiu). Left as printed: p0132 *onaii* (perhaps a damaged j; not certain), “personel”,
  *tsai*. `keep_hyphens` p0105 (“abiding-place”, the book's only instance).
- Period “1892”: the book dates the exchange at Yokohama January 1892; four months in all.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-25 | opus | 151 | 11.84 | no refusals |
| scan check and crop review; the differing readings | 2026-11-25 | Opus subagents | – | – | above |
| corrections | 2026-11-26 | sonnet | 151 | 5.43 | 26 spots |
| judge | 2026-11-26 | opus | 26 spots | 1.06 | 10 draft, 14 verified, 2 by hand |
| spot-read (front matter, appendix, index; tesseract on pp. 11–113) | 2026-11-26 | Opus subagent | – | – | 1 markup fault, 2 misprints |
| audit | 2026-11-26 | opus | 6 | 0.38 | 26/27; 2 candidates, neither real |
| rendered look | 2026-11-26 | Opus subagent | – | – | vocabulary flat → sub-entries as blockquote runs (Opus subagent, 215 runs), glossary layout; specks trimmed from p0067-2 |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-26 | PASS, 0 to fix, 1 waived (leaves p0149) (tools@7a437cbd) | 26/27; 0 real errors in 6 pages | first publication |

## Known issues
- The vocabulary's indented phrases are typed as `<blockquote>` runs (215, one level: second-level indents are set at
  the first) and shown as a list with hanging indents in the web pages and the EPUB (`glossary`); the ODT shows them as
  indented quotations.
- The heading “Steamers of the Japanese Steamship Co., or Nippon Yusen Kaisha,” ends in a comma, as printed; its
  sentence runs on in the next paragraph.
