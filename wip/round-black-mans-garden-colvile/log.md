# Round the Black Man’s Garden — Zélie Colvile (1893)

IA: roundblackmansga01colv_0 (440 leaves, 350 ppi, greyscale; IA hides leaves 0, 9, 10, 439). Second scan roundblackmansga00colv (Boston University, 500 ppi) not needed.
Eligibility: re-checked 2026-11-27: not in pg_catalog.csv (fresh copy); web search: the IA scans and Wikimedia Commons page images only; no reprint other than print on demand.

## Status
Stage reached: (a) scan checked, Drive cache done, Opus draft running (p0005–p0008, p0011–p0432, p0435).   Next step: Sonnet corrections pass; plate crops meanwhile.

## Page map
p0001 cover (title readable: the cover picture) · p0002–p0004 bookplate, endpaper, blank · p0005 half-title · p0008 frontispiece (portrait, signed) · p0011 title (motto in French) · p0013 dedication (French) · p0015–p0018 preface (H. E. Colvile) · p0019 contents · p0021–p0023 list of illustrations · p0026 map of Africa · p0027 = p. 1 (Book I; offset grows by 2 for each plate) · text ends p0429 = p. 341 · p0431–p0432 index · p0435 pocket map of Central Madagascar, opened (p0436 its back) · p0433–p0438 back.
Books (leaf/page): I The Sea of Islam 27/1 · II The Land of Rocks 80/48 · III The Land of Bondage 95/57 · IV The Island of Mystery 126/80 · V The Land of Sleep 289/229 · VI The Land of Gold 302/240 · VII The Fortunate Isles 339/271 · VIII The Land of Death 348/278; within each, numbered sections (I, II …) without titles.
Plates (32, blank verso after each): 8, 33, 37, 55, 81, 85, 91, 97, 101, 107, 115, 127, 137, 145, 157, 211, 225, 285, 297, 305, 319, 333, 343, 349, 359, 367, 377, 383, 389, 397, 415, 421; upright: 8, 127, 285, 367, 383, 397, 415; the others sideways (top of picture at the left; caption along the right edge). Cuts in the text: 99, 161, 165 (full page, sideways, with a key), 179, 187, 216, 232, 242 (key), 245, 272, 292, 310 (full page, key), 340, 362, 370 (full page, key), 385 (text wrapped round it), 395, 400, 406, 428. Maps: 26, 435.
Scan check (Opus subagent, 2026-11-27): folios of all leaves by OCR; 11 sheets; about 20 leaves at full size; nothing missing or cut; no tissues. Session looked at p0001, p0008, p0011, p0027.
Notes: a two-column menu (p. 287), a tombstone address in small type (p. 259), an inscription (p. 261), a pidgin-English letter (p. 319); French phrases; Malagasy names with grave accents (Antànanarìvo).

## Decisions
- Corrections pass (Sonnet, $13.97): 29 changes; it typed 10 in-text pictures mid-paragraph with `[[cont]]`: `move_pictures.py` put 13 back after their paragraphs; its `[[cont]]` proposal at p0314 was wrong (flush). Judge (25 spots, $0.67): verifier 24, draft 1; 17 looked at by the spot-read: all held.
- Structure: the eight Books are the chapters; the book's title above Book I a `front` division; numbered sections of Books I, IV and VIII given editor's titles (places, from a Sonnet subagent reading the text) as `toc_entries`, so the long Books are split at them; said in `notes_on_text`. The Africa map (p0026, after the list of illustrations) and the Madagascar pocket map (p0435) are reading pages of their own (“Map of Africa”, “Map of Central Madagascar”; assumed). Picture keys made part of their `[[caption]]` lines (p0165, p0370). p0326 (a tombstone address in small type) set as `<blockquote>`. Title-page motto as `[[center]]` lines.
- Spot-read (Opus subagent, with tesseract): accents made as printed (Karàmbìly, Antànanarìvo in the index), a folio, ditto marks in the list of illustrations as ″, a letter heading in two lines; no printed misprint found. keep_hyphens p0172, p0208, p0221, p0380.

## Runs
| Stage | Date | Model | Pages | Cost $ | Notes |
|---|---|---|---|---|---|
| draft | 2026-11-27 | opus | 427 | 28.02 | 0 refused |
| corrections | 2026-11-27 | sonnet | 427 | 13.97 | |
| judge | 2026-11-27 | opus | 25 spots | 0.67 | |
| audit | 2026-11-27 | opus | 6 | 0.35 | 30/30, 0 candidates |

## Versions
| Version | Date | Preflight stamp | Audit | Notes |

## Known issues
- Draft (Opus, 427 pages, $28.02, 0 errors, 0 refused, no 〓).
- Pictures cropped by an Opus subagent (54 + cover): sideways plates and p0165 `--rotate 270`; the two maps in colour (a red route); keys printed outside p0165's picture are text; p0310 and p0370 keep the numbers inside the pictures. Four looked at by the session.
