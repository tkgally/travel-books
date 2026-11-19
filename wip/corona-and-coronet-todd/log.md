# Corona and Coronet — Mabel Loomis Todd (1898)

IA: coronacoronetbei00toddiala (University of California Libraries; 504 leaves + colour cards, 400 ppi,
greyscale). Other scans looked at: none (this one is clean and complete); another IA scan exists
(coronacoronetbei00todd).
Eligibility: re-checked 2026-11-19: not in the Project Gutenberg catalogue (pg_catalog.csv: only Todd's
editions of Emily Dickinson); The Online Books Page lists only the IA scan; web searches find only a print-on-demand
OCR reprint (General Books, 2009) and dealers' copies of the 1898 and 1899 Houghton Mifflin printings; a PDF of
one chapter ("The Eclipse") on the New England Fireball/astronomy society site nefas.org is a brief excerpt.
Wikisource search rate-limited today (none found at the first check). Mabel Loomis Todd 1856–1932; Arthur
Curtiss James (author of "Deep-Sea Yachting", pp. xxiii–xxxvii) 1867–1941. **One drawing** ("Lighthouse on the
Beach at Esashi (from a Drawing by Mr. Thompson)", p0423) is by E. A. Thompson, the expedition's mechanician,
"a young man" in 1896 (p0074): death date not found, birth not before 1856 → under `selection.md` rule 5 the
drawing is left out of the editions (caption kept, with a note); assumed, question for Tom.

## Status
Stage reached: 1 (started; scan checked, cached in Drive, full-size leaves made); Opus draft running
(p0006, p0009–p0497).
Next step: when the draft finishes, `normalize.py`, then the Sonnet corrections pass (workflow §3).
Half-finished: draft run (resumable: re-run the same command and finished pages are skipped):
`python3 tools/ocr_claude.py --model opus --prompt prompts/transcribe.md --images $B/pages --out $W/draft --pages 6,9-497 --workers 6`

## Page map
p0001 front cover (cloth, crowns stamped; title and author) · p0002 pastedown · p0003 endpaper with an owner's
inscription (1898) · p0004 blank · p0005 blank · p0006 frontispiece "Mr. James's Schooner Yacht Coronet" (sideways)
· p0007 tissue guard · p0008 blank · p0009 title page · p0010 verso (copyright 1898; Riverside Press) · p0011
dedication · p0012 blank · p0013–p0016 Preface (signed M. L. T., Observatory House, Amherst, October 1898) ·
p0017–p0018 Contents · p0019–p0020 List of Illustrations (36 entries) · p0021–p0029 Introductory (xiii–) ·
p0030 blank · p0031–p0046 Deep-Sea Yachting by Arthur Curtiss James (xxiii–xxxvii) · p0047 = printed 1,
Chapter I (plates are unnumbered leaves, so the offset grows) · … · p0489 = 375 end of text (eclipse corona
vignette) · p0490 blank · p0491–p0497 Index (377–383) · p0498 library slip · p0499 back pastedown · p0500–p0505
back cover, colour cards.
Chapter openings (contact sheets): I p0047, II p0054, III p0062, IV p0074, V p0080, VI p0094, VII p0112,
VIII p0124, IX p0134, X p0146, XI p0155, XII p0166, XIII p0175, XIV p0189, XV p0205, XVI p0221, XVII p0240,
XVIII p0251, XIX p0258, XX p0264, XXI p0281, XXII p0292, XXIII p0305, XXIV p0321, XXV p0336, XXVI p0348,
XXVII p0358, XXVIII p0386, XXIX p0418, XXX p0431, XXXI p0440, XXXII p0449, XXXIII p0467.
Plates (full-page, each followed by a blank verso): p0006, p0057, p0069, p0087, p0103, p0119, p0137, p0157,
p0163, p0167, p0199, p0225 (map of Japan), p0249, p0277, p0285, p0289, p0307, p0317, p0329, p0343, p0353,
p0383, p0395, p0401, p0411, p0423 (Thompson drawing: left out), p0427, p0445, p0471, p0487;
p0462–p0463 folding map "Route of the Amherst Eclipse Expedition and Cruise of Mr. James's Schooner Yacht
Coronet, 1895–97", photographed opened in two halves (left and right) with a small overlap.
In-text cuts: p0365 (electric commutator), p0369, p0373, p0489 (corona vignette).
Music (staff notation, to be images): p0089, p0090, p0220 (Japanese national air), p0261, p0356, p0466.
Japanese characters: p0334 (a printed date, one line).
Footnotes: a few (p0086, p0113, p0115, p0183, p0391 …). Verse epigraphs at every chapter head; songs with
numbered verses (p0089–p0090, p0197–p0198, p0459).
Scan check: all 13 contact sheets looked at 2026-11-19; full size: p0017, p0019, p0020, p0021, p0462, p0463;
problems: none (every printed page present; the folding map was opened).

## Decisions
- Drafted p0006 and p0009–p0497; covers, endpapers with the owner's inscription, tissue guard, library slip and
  colour cards left out.
- The folding map: the two halves joined into one image (assumed; easily changed).
- Thompson's drawing (p0423) left out, caption and a note kept (assumed; question for Tom in `notes/preferences.md`).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
