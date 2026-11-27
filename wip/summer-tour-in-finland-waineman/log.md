# A Summer Tour in Finland — Paul Waineman [Sylvia Borgström MacDougall] (1908)

IA: summertourinfinl00macdrich (University of California Libraries; 448 image files, no p0445; 500 ppi; RGB JP2s, working pages grey). Second scan of the same setting: summertourinfinl0000sylv (412 images).
Eligibility: re-checked 2026-11-27: not in pg_catalog.csv (fresh copy); web search: only an excerpt on tota.world (a passage on Borgå), other Finland books on Gutenberg and Doria; no reprint other than print on demand.

## Status
Stage reached: (a) scan checked (fails as it stands: fixed by three leaves from the second scan), Drive cache done, Opus draft running.   Next step: merge `draft-extra/` (the three extra leaves) into `draft/`, delete draft p0122 (the cut-off plate; waive), Sonnet corrections pass; plate crops from the JP2 (colour) meanwhile.

## Page map
p0001 cover (no title) · p0002–p0004 endpapers, IA leaf · p0005 half-title · p0006–p0007 blank · p0008 frontispiece “Helsingfors” (colour, sideways) · p0009–p0010 tissue (not drafted) · p0011 title · p0012 verso (“First Published in 1908”) · p0013–p0021 contents (v–xiii) · p0023–p0024 list of illustrations · p0025 = p. 1 · p0028–p0029 = pp. 4–5; p0030–p0031 the same two pages scanned again (not drafted; waived) · p0037 = p. 11; pp. 12–13 MISSING from this copy → p0037a, p0037b from summertourinfinl0000sylv n35, n36 (same setting: the joins line up; looked at by the session) · p0038 = p. 14 · p0398 = p. 312, end · p0399–p0404 index · p0407–p0436 Methuen catalogue dated July 1912 (this copy is a later issue of the 1908 sheets) · p0437 printer's imprint · p0438–p0449 back.
Chapters (leaf = page): I 25=1, II 40=16, III 63=33, IV 74=44, V 90=58, VI 104=70, VII 124=86, VIII 143=99, IX 165=117, X 182=132, XI 197=145, XII 218=162, XIII 242=180, XIV 259=195, XV 273=207, XVI 292=224, XVII 306=236, XVIII 315=245, XIX 340=262, XX 363=281, XXI 383=299.
Plates (32: 16 colour, 16 monotone; all sideways, caption reading bottom to top, except Queen Bianca, upright; blank facing leaf beside each): 8 c, 47, 52, 56, 76 c, 98 c, 108, 122 (cut off at the outer edge, caption lost → p0122a from the second scan, n121), 125 c, 131, 139, 149, 162, 178 c, 194 c, 209, 215 c, 222, 235 c, 239, 255 c, 267 c, 282 c, 293, 318, 323 c, 332 c, 338 c, 345 c, 356, 378 (upright), 392 c.
Scan check (Opus subagent, 2026-11-27): folios of every text leaf by OCR of the running heads; 12 sheets; about 40 leaves at full size, edges and feet. Session looked at p0037, p0037a, p0037b, p0038 and the second scan's n117–n122. Cover picture: title page p0011.
Notes: chapter synopses and index in small type; å ä ö frequent (Å sometimes with a loose ring); French phrases in italics; fractions; short verse quotations.

## Decisions
- Three leaves taken from the second scan (workflow §1.4): `source.extra_leaves`; said in `notes_on_text`.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft (extra leaves) | 2026-11-27 | opus | 3 | 0.19 | `draft-extra/` |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
- Draft (Opus, 429 pages, $29.66, 0 errors, 0 refused, no 〓); the three extra leaves merged in; draft p0122 (the cut-off plate) deleted: p0122a replaces it (waive `leaves` p0122, p0030, p0031, p0009, p0010).
- Plates cropped by an Opus subagent (colour plates in colour from the full-size RGB leaves, monotone `--gray`; all sideways ones `--rotate 270`); cover.jpg = title page.
