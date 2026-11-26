# The Land of the Muskeg — H. Somers Somerset (1895)

IA: 31221012772286 (Edmonton Public Library; 318 leaves, 360 ppi). Other scans: landofmuskeg00someuoft (Robarts, Toronto),
landmuskeg00somegoog (NYPL, Google), cihm_16172 (Canadiana).
Eligibility: queue row (Opus subagent, 2026-11-25); re-checked 2026-11-26 (a web search: Canadiana and BHL page images
only, no text, no later edition). Started 2026-11-26.

## Status
Published v1 2026-11-26.

## Page map
Scan check (Opus subagent, 2026-11-26). p0000 colour card · p0001 cover (title readable; barcode label) · p0002–p0004 endpapers ·
p0005 half-title · p0006 blank · p0007 IA digitization sheet (not drafted) · p0008 frontispiece portrait · p0009 title page
(vignette) · p0010 imprint · p0011 dedication · p0012 blank · p0013–p0014 Contents vii–viii · p0015–p0018 List of Illustrations
ix–xii (and maps) · p0019–p0037 Preface by A. H. Pollen xiii–xxxi · p0038 blank (not drafted) · p0039 Map I opened · p0040 the
same map half folded (not drafted) · chapters (leaf/page): I 41/1 · II 64/24 · III 96/56 · IV 119/77 · V 141/99 · VI 162/120 ·
VII 178/136 · VIII 203/161 · IX 220/178 · X 262/220 · XI 281/237 · p0292 = p. 248 The End · p0055 Map II (laid over p. 15, its
top clipped) · p0055a = p. 15 from landofmuskeg00someuoft n58 · p0097 Map III opened (p0098 blank) · p0280 Map IV (p0279 blank)
· p0293–p0316 Heinemann advertisements · p0317–p0318 endpaper, back cover · p0319 colour card. Offset: page + 40 (leaves
41–96), + 42 (99–278), + 44 (281–292). About 110 pictures, most small cuts in the text with the text wrapped round them;
full-page plates p0025, p0046, p0145, p0213, p0253 (sideways). Footnotes; journal entries with italic dates from ch. VII.

## Decisions
- Divisions: half-title (front), title page (frontispiece moved to it), dedication, contents and list of illustrations (JSON
  only), Pollen's preface, Map I as a reading division before Chapter I, 11 chapters (title as `[[subtitle]]`), Heinemann's
  list (advertisements; its `#` headings made `##`). p0006, p0038 blank page files; p0007 (IA sheet) and p0040 (the map half
  folded) waived in `leaves`.
- Contents: chapter numbers and titles, as printed.
- p. 15 from landofmuskeg00someuoft n58 (p0055a); Map II cropped from the same copy (n56), whole, where this copy's is clipped.
- Corrections pass: 61 word spots, 69 changes; judge (Opus) 12 draft, 44 verified. 24 pages where the verifier moved a picture
  into the middle of its paragraph with `[[cont]]` (the judge agreed every time): those pages taken from the draft; 7 more pages
  where the draft itself left a picture mid-sentence: pictures moved after the paragraph by script (now `tools/move_pictures.py`,
  which on the verifier's pages gives the draft's pages exactly). p0218 `[[cont]]` removed by the verifier restored. Captions
  in plain upper and lower case (the judge's capitals left out).
- Printed misprints marked: p0300 “Physican”, p0314 “tbe” (publisher's list). “coyottes” (p0128) and “Portairs” (ch. X title,
  running heads, notes) left as printed.
- Spot-read (Opus subagent): title page split as printed (title in two lines, the statement of illustrations in three); p0223
  `M<sup>c</sup>Leod` typed plain like the rest. Assumed: the raised c of Mc names (about 35) typed as plain “Mc”, as in the
  other books; the map titles' “M‘Leod” kept as printed.
- Rendered look (Opus subagent): one picture still mid-sentence (p0102, the next paragraph opening with ‘): moved; the
  tool now catches that form (test).
- Pictures cropped by two Opus subagents (115 and the cover); the frontispiece's printed label “Frontispiece.” painted out.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-26 | opus | 310 | 20.83 | no refusals, no 〓 |
| corrections | 2026-11-26 | sonnet | 310 | 10.23 | 69 changes |
| judge | 2026-11-26 | opus | 61 spots | 1.47 | 12 draft, 44 verified, 5 kept pictures |
| audit | 2026-11-26 | opus | 6 | 0.35 | 26/27, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-26 | PASS tools@ecfc483b | 26/27, 0 real | first publication; waivers: leaves p0007 (IA sheet), p0040 (map half folded) |

## Known issues
- The title page's left- and right-set lines are centred; the last line of the verse on p. 187 is indented in print.
- The maps are shown at 1000 px: the smallest names are hard to read; the scan has them at full size.
