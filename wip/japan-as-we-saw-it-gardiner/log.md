# Japan As We Saw It — Robert S. Gardiner (1892)

IA: japanaswesawit00gardrich (University of California Libraries; 152 leaves, 500 ppi). Other scans: Library of
Congress copy japanaswesawit00gard (not looked at; may have the maps).
Eligibility: queue row (JATSI 91; checked 2026-11-23). Started 2026-11-25.

## Status
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

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-25 | opus | 151 | 11.84 | no refusals |
| scan check and crop review; the differing readings | 2026-11-25 | Opus subagents | – | – | above |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
