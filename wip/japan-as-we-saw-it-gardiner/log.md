# Japan As We Saw It — Robert S. Gardiner (1892)

IA: japanaswesawit00gardrich (University of California Libraries; 152 leaves, 500 ppi). Other scans: Library of
Congress copy japanaswesawit00gard (not looked at; may have the maps).
Eligibility: queue row (JATSI 91; checked 2026-11-23). Started 2026-11-25 because Tom had Gemini transcribe it as
the first trial of help from other models (`notes/helpers.md`); there was no transcription of ours before that day.

## Status
Stage reached: scan fetched and checked; Opus draft of every leaf (`draft/`, normalized); Gemini's text as page
files (`helper/`, for comparison) and its 83 pictures (`images/`); every difference between the two looked at on
the scan. **Not yet cached in Drive** (the page images are in no Drive folder: fetch from IA once more, then
`drive_cache.py pack` and upload; said here so that the second request to IA is on record).
Next step: an ordinary book from stage 3 on, with the draft as the text:
1. `ia.py fetch`, `prep_pages.py`, cache in Drive (folder in "Travel Books").
2. Sonnet corrections pass on `draft/`, review, judge, `pages/`.
3. Apply what the comparison settled (table below), then structure, pictures, preflight, audit.
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

## The comparison of 2026-11-25 (Gemini's text against the Opus draft, each difference on the scan)

What to do to the draft (the print is as given; “G” = Gemini's reading was right):
- remove the `[[caption]]` lines the draft typed from lettering inside pictures (p0032, p0033, p0037, p0042 ×2,
  p0052 ×2, p0059 ×2, p0065, p0067 ×2, p0068, p0069, p0071, p0078, p0082, p0092 ×2, p0095, p0100, p0108, p0112,
  p0117); keep p0025, p0027, p0030, p0096;
- p0048 “women, are” (G; the draft has a full stop) · p0096 “Ah-koah-ko” (G) · p0123 “massugu.” (G) · p0133
  “etc),” no stop (G) · p0121 “1210 Tsubo is practically an acre.” is a line of its own (G);
- printer's errors to mark: p0010 “apan” → Japan (the J did not print), p0075 “nand” → hand, p0086 a full stop for a
  comma after “(Nee-gah-tsoo-doh)”, p0034 “closély” (a speck or damaged type over the e: type “closely”, no mark
  needed if the crop shows a speck);
- the draft was right at: p0036 schoolroom, p0056 neophite, p0080 Rah-koo-rah-koo-tay, p0098 “atten-” at the page
  foot, p0127 “irashaimas ka.”, p0128 “doshte”, the upright brackets round the italic pronunciations, the heading on
  p0017, the vocabulary pages as tables (p0121 two entries a line; p0136 two and three column pairs).
The full list: `helper-vs-draft-spots.json` (draft = Opus, verified = Gemini).

## Gemini's pictures (Opus subagent, each crop against its page)
83 pictures, 83 crops, none missed, none wrong, all in the right place in the text. **37 good; 13 with page text
inside; 29 with part of the picture or its lettering cut off; 4 both.** To re-cut from the full-size leaves, worst
first: p0026-1, p0053-1, p0065-1, p0069-1, p0082-1, p0092-1, p0092-2, p0094-1; then p0099-1, p0100-1, p0114-1,
p0052-2, p0115-1, p0031-1, p0075-1, p0095-1, p0105-1; then the rest of: p0023-1, p0024-1, p0024-2, p0025-2, p0030-1,
p0036-1, p0041-1, p0043-1, p0043-2, p0045-1, p0048-1, p0051-1, p0052-1, p0055-1, p0055-2, p0059-2, p0063-1, p0067-2,
p0070-1, p0078-1, p0085-1, p0089-1, p0096-1, p0103-1, p0107-1, p0108-1, p0110-1, p0112-1, p0117-1. With 46 of 83 to
redo it is simpler to cut all 83 ourselves; the 37 good ones in `images/` may be kept. No cover.jpg was made.
Alt text: p0042-1 is a girl grinding in a bowl.

## Decisions

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-25 | opus | 151 | 11.84 | no refusals; for the comparison and as the text |
| (trial) Sonnet corrections pass on Gemini's pages | 2026-11-25 | sonnet | 137 | 5.08 | 23 word changes, nearly all captions and pictures moved; none of Gemini's word faults found. Not kept |
| scan check and crop review; the differing readings | 2026-11-25 | Opus subagents | – | – | above |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
