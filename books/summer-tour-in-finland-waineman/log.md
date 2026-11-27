# A Summer Tour in Finland — Paul Waineman [Sylvia Borgström MacDougall] (1908)

IA: summertourinfinl00macdrich (University of California Libraries; 448 image files, no p0445; 500 ppi; RGB JP2s, working pages grey). Second scan of the same setting: summertourinfinl0000sylv (412 images).
Eligibility: re-checked 2026-11-27: not in pg_catalog.csv (fresh copy); web search: only an excerpt on tota.world (a passage on Borgå), other Finland books on Gutenberg and Doria; no reprint other than print on demand.

## Status
Stage reached: published v1 2026-11-27.

## Page map
p0001 cover (no title) · p0002–p0004 endpapers, IA leaf · p0005 half-title · p0006–p0007 blank · p0008 frontispiece “Helsingfors” (colour, sideways) · p0009–p0010 tissue (not drafted) · p0011 title · p0012 verso (“First Published in 1908”) · p0013–p0021 contents (v–xiii) · p0023–p0024 list of illustrations · p0025 = p. 1 · p0028–p0029 = pp. 4–5; p0030–p0031 the same two pages scanned again (not drafted; waived) · p0037 = p. 11; pp. 12–13 MISSING from this copy → p0037a, p0037b from summertourinfinl0000sylv n35, n36 (same setting: the joins line up; looked at by the session) · p0038 = p. 14 · p0398 = p. 312, end · p0399–p0404 index · p0407–p0436 Methuen catalogue dated July 1912 (this copy is a later issue of the 1908 sheets) · p0437 printer's imprint · p0438–p0449 back.
Chapters (leaf = page): I 25=1, II 40=16, III 63=33, IV 74=44, V 90=58, VI 104=70, VII 124=86, VIII 143=99, IX 165=117, X 182=132, XI 197=145, XII 218=162, XIII 242=180, XIV 259=195, XV 273=207, XVI 292=224, XVII 306=236, XVIII 315=245, XIX 340=262, XX 363=281, XXI 383=299.
Plates (32: 16 colour, 16 monotone; all sideways, caption reading bottom to top, except Queen Bianca, upright; blank facing leaf beside each): 8 c, 47, 52, 56, 76 c, 98 c, 108, 122 (cut off at the outer edge, caption lost → p0122a from the second scan, n121), 125 c, 131, 139, 149, 162, 178 c, 194 c, 209, 215 c, 222, 235 c, 239, 255 c, 267 c, 282 c, 293, 318, 323 c, 332 c, 338 c, 345 c, 356, 378 (upright), 392 c.
Scan check (Opus subagent, 2026-11-27): folios of every text leaf by OCR of the running heads; 12 sheets; about 40 leaves at full size, edges and feet. Session looked at p0037, p0037a, p0037b, p0038 and the second scan's n117–n122. Cover picture: title page p0011.
Notes: chapter synopses and index in small type; å ä ö frequent (Å sometimes with a loose ring); French phrases in italics; fractions; short verse quotations.

## Decisions
- Three leaves taken from the second scan (workflow §1.4): `source.extra_leaves`; said in `notes_on_text`.
- Corrections pass (Sonnet, $14.20): 41 changes; one `[[cont]]` proposal (p0433, in the catalogue) not applied. Judge (25 spots, $0.87): draft 17, verifier 7, could not undo 1 (p0413 “Illusstrated”, printed: marked `[[corr]]` by hand).
- Contents: chapters without titles: the editor's short titles (places), proposed by a Sonnet subagent from the text, trimmed by the session; `toc_title` per chapter; said in `notes_on_text`. The book's title above Chapter I is a `front` division.
- Spot-read (Opus subagent, with tesseract): the printer set o with a ring above (o̊) for ö in most Swedish names (Hango̊, Lo̊nnrot, Ho̊gholmen, Brändo̊ …), a true ö only in a few (Borgström, “Hangö Fjord”): typed as printed with U+030A (checked by the session on p0063; said in `notes_on_text`). All 18 openings in full capitals (4 fixed). Printed misprints marked: p0413 Illusstrated, p0423 tbe, p0280 contant, p0118 a comma for a full stop; “Neopolitan” (p0037b) kept. Title page and list of illustrations: small capitals as printed. keep_hyphens p0172 (damp-looking).
- Rendered look (Opus subagent, 390 and 1280 px): the catalogue's Part III (p0429) was a reading page: advertisements division added. o̊ renders as one letter. Joins round pp. 12–13 read on.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft (extra leaves) | 2026-11-27 | opus | 3 | 0.19 | `draft-extra/` |
| draft | 2026-11-27 | opus | 426 | 29.66 | 0 refused |
| corrections | 2026-11-27 | sonnet | 429 | 14.20 | |
| judge | 2026-11-27 | opus | 25 spots | 0.87 | |
| audit | 2026-11-27 | opus | 6 | 0.34 | 30/30, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |
|---|---|---|---|---|
| 1 | 2026-11-27 | preflight PASS: summer-tour-in-finland-waineman v1 — 0 to fix, 4 waived; to look at: folios 1, accents 7, rare-forms 1, serial-commas 4 — tools@430a8bef 2026-11-27 | 30/30, 0 real errors in 6 pages | First publication. |

## Known issues
- Draft (Opus, 429 pages, $29.66, 0 errors, 0 refused, no 〓); the three extra leaves merged in; draft p0122 (the cut-off plate) deleted: p0122a replaces it (waive `leaves` p0122, p0030, p0031, p0009, p0010).
- Plates cropped by an Opus subagent (colour plates in colour from the full-size RGB leaves, monotone `--gray`; all sideways ones `--rotate 270`); cover.jpg = title page.
