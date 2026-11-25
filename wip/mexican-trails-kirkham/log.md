# Mexican Trails — Stanton Davis Kirkham (1909)

IA: mexicantrailsrec00kirk_0 (Getty Research Institute; 382 leaves, 500 ppi). Other scans looked at: none.
Eligibility: checked 2026-11-25 (queue row, an Opus subagent the same day): no text at Gutenberg, Wikisource or
Faded Page; print-on-demand reprints only; Kirkham 1868–1944; the photographs are his own.

## Status
Stage reached: scan fetched from IA, checked and mapped, and cached in Drive; `book.json` begun (bibliographic
fields, `frontispiece`, `omitted_from_reading`; no divisions or summary yet). No model run yet.
The Drive cache is in the folder "Helper model workspace/References/mexican-trails-kirkham" (id in `source.json`),
not in "Travel Books": the book was prepared for a trial with Gemini that was stopped (`notes/improvement.md`
§"Tried and set aside"). Tom: leave those Drive files as they are. `drive_cache.py fetch` works on them as usual.
Next step: `python3 tools/drive_cache.py fetch wip/mexican-trails-kirkham/source.json $B/pages`, then the Opus draft
of leaves 8–375 (`--pages 8-10,13-375`; p0011–p0012 are hidden tissue leaves) and on from `workflow.md` §2.
Half-finished: nothing.

## Page map
(Opus subagent, 2026-11-25: all 10 sheets; 17 leaves at full size; the page number of every text leaf read.)
p0000 colour card · p0001 front cover (title readable: cover.jpg) · p0002–p0007 endpapers · p0008 publisher's list ·
p0009 blank · p0010 frontispiece · p0011–p0012 tissue (hidden) · p0013 title · p0014 verso · p0015 dedication ·
p0017–p0024 Foreword v–xii · p0025–p0026 Contents · p0027–p0029 Illustrations · p0031 = printed 1 (offset 30, +2
after each plate, 76 at the end) · chapters at p0031, p0045, p0059, p0074, p0083, p0098, p0115, p0128, p0146, p0173,
p0179, p0187, p0207, p0218, p0228, p0247, p0256, p0264, p0276, p0287, p0301, p0314, p0332, p0345, p0354 ·
p0357–p0369 Index 281–293 · p0371–p0375 advertisements · p0379 back endpaper · p0380 back cover · p0381 colour card.
Plates (24, photographs, blank backs, most sideways): p0010, p0047, p0071, p0087, p0095, p0101, p0117, p0125, p0129,
p0135, p0141, p0147, p0153, p0159, p0165, p0169, p0191, p0197, p0203, p0233, p0273, p0291, p0311, p0341.
Scan check: no page missing, doubled or cut; no folding plates or maps; no footnotes seen; verse pp. 86, 88.
Full-size leaves (the plates, p0001, p0013) are in Drive as `full-001.zip` … `full-014.zip` (`source.json`
`full_parts`: fetch each by id with curl, as `drive_cache.py` does, and unzip), so IA need not be asked again.
For the draft: Spanish words are frequent, in italics, some printed with accents and some without; verse in smaller
type pp. 86, 88; breaks marked by a row of dots (pp. 137, 251); a placard set as lines p. 146; catechism questions
pp. 265–266; the index in two columns of small type; no footnotes seen.

## Pictures (Opus subagent, 2026-11-26)
All 24 plates and `cover.jpg` cropped (`--gray`; 21 turned upright with `--rotate 270`; p0047, p0071, p0311 upright as
printed; p0197 and p0273 recropped after a first cut lost pale ground). Captions read on the plates: p0141 “The
fields are ploughed with a crooked stick” has no full stop as printed; p0169 “mediæval” with the ligature. Compare
the draft's `[[caption]]` lines with these after the judge.

## Decisions

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
