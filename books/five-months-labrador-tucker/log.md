# Five Months in Labrador and Newfoundland, during the Summer of 1838 — Ephraim W. Tucker (1839)

IA: fivemonthsinlabr00tuck_0 (University of Toronto, Thomas Fisher Library; 166 leaves, colour cards p0000 and p0165 hidden).
Eligibility: re-checked 2026-11-27: pg_catalog.csv none; web search: page images only (Canadiana, HathiTrust, Memorial
University, Toronto PL), print-on-demand reprints only.

## Status
Published v1 2026-11-27.

## Page map
p0001 cover ("Tucker's Voyage") · p0002 bookplate · p0003–p0004 endpapers · p0005 half-title · p0006 blank · p0007 title ·
p0008 copyright · p0009–p0012 Preface (v–viii) · p0013–p0015 Contents (ix–xi) · p0016 blank · p0017 = printed 13 (offset 4)
… p0160 = 156 (end) · p0161–p0163 blank endpapers · p0164 back cover.
Chapters: I p0017, II p0035, III p0057, IV p0076, V p0093, VI p0110, VII p0129, VIII p0147. Each opens with a summary in
small type. Footnotes * †; a two-column fishery table p0091–p0092; verse p0145 (Mrs. Sigourney). No illustrations.
Scan check (Opus subagent, 2026-11-27): all sheets; folios read p0018–p0160 without a break; full size p0013, p0017,
p0039, p0091, p0100, p0145, p0160 and others; problems: none (foxing, show-through).

## Decisions
- p0016 is a blank verso; the draft had typed a made-up page of contents (Chapters VI–VIII) from the show-through of p0015,
  and the corrections pass and the judge kept it. Found by the spot-read; the page is `[[blank]]`. New list in
  `tess_compare.py` (pages tesseract finds nearly empty), test `test_empty_items`.
- Corrections pass: 8 changes, 4 spots judged (3 draft, 1 verified: “by-gone” p0068).
- Spot-read (Opus subagent; title page, preface, contents, chapter openings, footnotes p0039, table p0091–p0092, verse
  p0145, last page, preflight lists, tess_compare's 54 word items — all tesseract's errors): printed misprints marked p0025
  “dremay”, p0081 “duing”, p0091 “decription”, p0118 “numerons”; spacing p0015, p0091, p0145; the table's last row given its
  empty cell. “adore His” (p0027) as printed. Hyphen joins: “Newfoundland” and “southeast” joined (the book prints both
  solid).
- Contents: the chapters have only summaries; entries of the editor's (“Chapter I. Boston to Boone Bay” …), said in
  `notes_on_text`. The book's title above Chapter I (p0017) a `front` division, as in *An American Missionary in Japan*.
- Cover: the front cover reads only “Tucker's Voyage” (binder's title): the title page is the picture.
- Audit 29/30, 0 candidates. Draft and pages compared by length: only p0016 (blank) and p0007 (title page lines).

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| 1 | 2026-11-27 | PASS tools@2c612070 | 29/30, 0 real | first publication; no waivers |
| draft | 2026-11-27 | opus | 156 | 9.97 | no refusals, no 〓 |
| corrections | 2026-11-27 | sonnet | 156 | 5.03 | 8 changes |
| judge | 2026-11-27 | opus | 4 spots | 0.09 | 3 draft, 1 verified |
| audit | 2026-11-27 | opus | 6 | 0.33 | 29/30, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|

## Known issues
- The verse on p. 141 prints its even lines indented; the markup has no indent for them.
- The table on pp. 87–88 joined by `[[cont]]` (new markup, compiler and test `TableAcrossPages`; found by the rendered look). The rendered look also found a stray line break in p0029 (joined).
